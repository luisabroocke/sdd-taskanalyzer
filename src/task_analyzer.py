"""Análise de duração e cumprimento de prazos de tarefas em memória."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import logging
from typing import TypedDict

logger = logging.getLogger(__name__)

PRIORIDADES: tuple[str, ...] = ("baixa", "media", "alta")
STATUS_VALIDOS: tuple[str, ...] = ("concluida", "pendente", "cancelada")


class ContratoInvalidoError(ValueError):
    """Indica incompatibilidade com o contrato de entrada."""


class DataInconsistenteError(ValueError):
    """Indica tipo, fuso ou sequência temporal inválida."""


class NenhumaTarefaConcluidaError(ValueError):
    """Indica ausência de tarefas concluídas para análise."""


@dataclass(frozen=True)
class Tarefa:
    """Representa uma tarefa imutável.

    Args:
        id_tarefa: Identificador positivo e único.
        data_criacao: Data de criação em UTC.
        prazo: Prazo em UTC.
        prioridade: `baixa`, `media` ou `alta`.
        status: `concluida`, `pendente` ou `cancelada`.
        data_inicio: Início opcional em UTC.
        data_conclusao: Conclusão opcional em UTC.
    """

    id_tarefa: int
    data_criacao: datetime
    prazo: datetime
    prioridade: str
    status: str
    data_inicio: datetime | None = None
    data_conclusao: datetime | None = None


class Metricas(TypedDict):
    """Indicadores de um conjunto de tarefas."""

    quantidade_tarefas: int
    tempo_medio_conclusao_min: float
    taxa_atraso_percentual: float


class RelatorioAnalise(TypedDict):
    """Relatório agregado geral e por prioridade."""

    geral: Metricas
    indicadores_por_prioridade: dict[str, Metricas]


class TaskAnalyzer:
    """Valida tarefas e calcula métricas sem manter estado entre chamadas."""

    def analisar(self, tarefas: list[Tarefa]) -> RelatorioAnalise:
        """Valida e analisa uma lista de tarefas.

        Args:
            tarefas: Lista de instâncias `Tarefa`.

        Returns:
            Relatório com métricas gerais e por prioridade.

        Raises:
            ContratoInvalidoError: Se a estrutura ou atributos não temporais forem inválidos.
            DataInconsistenteError: Se houver data ou sequência temporal inválida.
            NenhumaTarefaConcluidaError: Se não houver tarefas concluídas.
        """
        self._validar_formato_e_atributos(tarefas)
        self._validar_datas(tarefas)

        concluidas = [tarefa for tarefa in tarefas if tarefa.status == "concluida"]
        if not concluidas:
            logger.warning(
                "evento=analise_indisponivel quantidade_registros=%d motivo=nenhuma_tarefa_concluida",
                len(tarefas),
            )
            raise NenhumaTarefaConcluidaError(
                "Análise indisponível: nenhuma tarefa concluída"
            )

        geral = self._calcular_metricas(concluidas)
        por_prioridade = {
            prioridade: self._calcular_metricas(
                [tarefa for tarefa in concluidas if tarefa.prioridade == prioridade]
            )
            for prioridade in PRIORIDADES
        }
        logger.info(
            "evento=analise_concluida quantidade_registros=%d quantidade_concluidas=%d",
            len(tarefas),
            len(concluidas),
        )
        return {
            "geral": geral,
            "indicadores_por_prioridade": por_prioridade,
        }

    @staticmethod
    def _validar_formato_e_atributos(tarefas: list[Tarefa]) -> None:
        """Valida o formato da lista e os campos não temporais.

        Args:
            tarefas: Entrada a validar.

        Raises:
            ContratoInvalidoError: Se a lista ou algum atributo não temporal for inválido.
        """
        if not isinstance(tarefas, list):
            raise ContratoInvalidoError("Entrada inválida: tarefas deve ser uma lista")

        ids: set[int] = set()
        for tarefa in tarefas:
            if not isinstance(tarefa, Tarefa):
                raise ContratoInvalidoError("Entrada inválida: cada item deve ser Tarefa")

            identificador = tarefa.id_tarefa
            if isinstance(identificador, bool) or not isinstance(identificador, int) or identificador <= 0:
                raise ContratoInvalidoError(
                    f"id_tarefa inválido para tarefa {identificador!r}: deve ser inteiro positivo"
                )
            if identificador in ids:
                logger.warning(
                    "evento=validacao_falhou quantidade_registros=%d id_tarefa=%s motivo=id_duplicado",
                    len(tarefas), identificador,
                )
                raise ContratoInvalidoError(
                    f"id_tarefa duplicado: {identificador}"
                )
            ids.add(identificador)

            if not isinstance(tarefa.prioridade, str) or tarefa.prioridade not in PRIORIDADES:
                raise ContratoInvalidoError(
                    f"prioridade inválida para id_tarefa {identificador}: {tarefa.prioridade!r}"
                )
            if not isinstance(tarefa.status, str) or tarefa.status not in STATUS_VALIDOS:
                raise ContratoInvalidoError(
                    f"status inválido para id_tarefa {identificador}: {tarefa.status!r}"
                )
            if tarefa.status == "concluida" and tarefa.data_conclusao is None:
                raise ContratoInvalidoError(
                    f"data_conclusao obrigatória para tarefa concluída id_tarefa {identificador}"
                )
            if tarefa.status != "concluida" and tarefa.data_conclusao is not None:
                raise ContratoInvalidoError(
                    f"data_conclusao deve ser None para status {tarefa.status}, id_tarefa {identificador}"
                )

    @staticmethod
    def _validar_datas(tarefas: list[Tarefa]) -> None:
        """Valida os tipos, fusos e relações temporais.

        Args:
            tarefas: Entrada cujas datas serão validadas.

        Raises:
            DataInconsistenteError: Se alguma data não for UTC ou for cronologicamente inválida.
        """
        for tarefa in tarefas:
            identificador = tarefa.id_tarefa
            campos: tuple[tuple[str, datetime | None, bool], ...] = (
                ("data_criacao", tarefa.data_criacao, False),
                ("prazo", tarefa.prazo, False),
                ("data_inicio", tarefa.data_inicio, True),
                ("data_conclusao", tarefa.data_conclusao, True),
            )
            for nome, valor, opcional in campos:
                if valor is None and opcional:
                    continue
                if not isinstance(valor, datetime):
                    raise DataInconsistenteError(
                        f"{nome} deve ser datetime para id_tarefa {identificador}"
                    )
                if valor.tzinfo is None or valor.utcoffset() is None:
                    raise DataInconsistenteError(
                        f"{nome} deve conter fuso UTC explícito para id_tarefa {identificador}"
                    )
                if valor.utcoffset() != timedelta(0):
                    raise DataInconsistenteError(
                        f"{nome} deve estar em UTC (deslocamento zero) para id_tarefa {identificador}"
                    )

            # As datas obrigatórias já foram verificadas como datetime acima.
            if tarefa.prazo < tarefa.data_criacao:
                raise DataInconsistenteError(
                    f"prazo anterior à data_criacao para id_tarefa {identificador}"
                )
            if tarefa.data_inicio is not None and tarefa.data_inicio < tarefa.data_criacao:
                raise DataInconsistenteError(
                    f"data_inicio anterior à data_criacao para id_tarefa {identificador}"
                )
            referencia = tarefa.data_inicio or tarefa.data_criacao
            if tarefa.data_conclusao is not None and tarefa.data_conclusao < referencia:
                raise DataInconsistenteError(
                    f"data_conclusao anterior ao início de referência para id_tarefa {identificador}"
                )

    @staticmethod
    def _calcular_metricas(tarefas_concluidas: list[Tarefa]) -> Metricas:
        """Calcula métricas para tarefas concluídas de um grupo.

        Args:
            tarefas_concluidas: Tarefas concluídas já validadas.

        Returns:
            Quantidade, média de duração em minutos e taxa de atraso percentual.
        """
        quantidade = len(tarefas_concluidas)
        if quantidade == 0:
            return {
                "quantidade_tarefas": 0,
                "tempo_medio_conclusao_min": 0.0,
                "taxa_atraso_percentual": 0.0,
            }

        duracoes: list[float] = []
        atrasadas = 0
        for tarefa in tarefas_concluidas:
            referencia = tarefa.data_inicio or tarefa.data_criacao
            conclusao = tarefa.data_conclusao
            # A validação garante datetime nos dois campos.
            assert conclusao is not None
            duracao_minutos = (conclusao - referencia).total_seconds() / 60
            duracoes.append(duracao_minutos)
            if conclusao > tarefa.prazo:
                atrasadas += 1

        media = sum(duracoes) / quantidade
        taxa_atraso = (atrasadas / quantidade) * 100
        return {
            "quantidade_tarefas": quantidade,
            "tempo_medio_conclusao_min": float(round(media, 2)),
            "taxa_atraso_percentual": float(round(taxa_atraso, 2)),
        }

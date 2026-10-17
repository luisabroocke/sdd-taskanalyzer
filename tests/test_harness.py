"""Test Harness para os cenários de aceite AC01–AC12."""

from datetime import datetime, timedelta, timezone

import pytest

from src.task_analyzer import (
    ContratoInvalidoError,
    DataInconsistenteError,
    NenhumaTarefaConcluidaError,
    Tarefa,
    TaskAnalyzer,
)

UTC = timezone.utc
ANALISADOR = TaskAnalyzer()


def dt(hora: int, minuto: int = 0, dia: int = 2) -> datetime:
    """Cria datetime UTC para os exemplos do contrato."""
    return datetime(2026, 9, dia, hora, minuto, tzinfo=UTC)


def tarefa(
    identificador: int,
    prioridade: str,
    status: str,
    criacao: datetime,
    prazo: datetime,
    inicio: datetime | None = None,
    conclusao: datetime | None = None,
) -> Tarefa:
    """Cria uma tarefa com os campos do contrato."""
    return Tarefa(identificador, criacao, prazo, prioridade, status, inicio, conclusao)


def conjunto_ac01() -> list[Tarefa]:
    """Retorna o conjunto de referência AC01."""
    return [
        tarefa(101, "alta", "concluida", dt(7, 30), dt(8, 30), dt(8), dt(8, 45)),
        tarefa(102, "alta", "concluida", dt(8, 30), dt(10, 30), dt(9), dt(10, 15)),
        tarefa(103, "media", "concluida", dt(9, 30), dt(10, 30), dt(10), dt(10, 30)),
        tarefa(104, "media", "concluida", dt(10, 30), dt(12), dt(11), dt(12, 30)),
        tarefa(105, "baixa", "concluida", dt(13), dt(16), None, dt(15, 30)),
        tarefa(106, "alta", "pendente", dt(13), dt(17)),
        tarefa(107, "baixa", "cancelada", dt(13), dt(17)),
    ]


def test_ac01_metricas_gerais_e_por_prioridade() -> None:
    """AC01: valida contagens, médias e atrasos."""
    relatorio = ANALISADOR.analisar(conjunto_ac01())
    assert set(relatorio) == {"geral", "indicadores_por_prioridade"}
    assert relatorio["geral"] == {
        "quantidade_tarefas": 5,
        "tempo_medio_conclusao_min": 78.0,
        "taxa_atraso_percentual": 40.0,
    }
    assert relatorio["indicadores_por_prioridade"] == {
        "baixa": {"quantidade_tarefas": 1, "tempo_medio_conclusao_min": 150.0, "taxa_atraso_percentual": 0.0},
        "media": {"quantidade_tarefas": 2, "tempo_medio_conclusao_min": 60.0, "taxa_atraso_percentual": 50.0},
        "alta": {"quantidade_tarefas": 2, "tempo_medio_conclusao_min": 60.0, "taxa_atraso_percentual": 50.0},
    }


def test_ac02_conclusao_antes_do_inicio() -> None:
    """AC02: data de conclusão anterior ao início deve falhar."""
    itens = conjunto_ac01()
    itens[0] = Tarefa(101, dt(7, 30), dt(8, 30), "alta", "concluida", dt(8), dt(7, 50))
    with pytest.raises(DataInconsistenteError, match="data_conclusao"):
        ANALISADOR.analisar(itens)


@pytest.mark.parametrize("itens", [[], [
    tarefa(106, "alta", "pendente", dt(13), dt(17)),
    tarefa(107, "baixa", "cancelada", dt(13), dt(17)),
]])
def test_ac03_sem_tarefas_concluidas(itens: list[Tarefa]) -> None:
    """AC03: lista vazia ou sem concluídas lança exceção específica."""
    with pytest.raises(NenhumaTarefaConcluidaError, match="Análise indisponível: nenhuma tarefa concluída"):
        ANALISADOR.analisar(itens)


def test_ac04_limite_do_prazo_e_grupos_vazios() -> None:
    """AC04: concluir exatamente no prazo não é atraso."""
    relatorio = ANALISADOR.analisar([conjunto_ac01()[2]])
    assert relatorio["geral"] == {
        "quantidade_tarefas": 1,
        "tempo_medio_conclusao_min": 30.0,
        "taxa_atraso_percentual": 0.0,
    }
    assert relatorio["indicadores_por_prioridade"]["baixa"] == {
        "quantidade_tarefas": 0,
        "tempo_medio_conclusao_min": 0.0,
        "taxa_atraso_percentual": 0.0,
    }


def test_ac05_criacao_como_inicio_de_referencia() -> None:
    """AC05: usa criação quando data_inicio é None."""
    relatorio = ANALISADOR.analisar([conjunto_ac01()[4]])
    assert relatorio["geral"]["tempo_medio_conclusao_min"] == 150.0
    assert relatorio["geral"]["taxa_atraso_percentual"] == 0.0


def test_ac06_prioridade_desconhecida() -> None:
    """AC06: prioridade desconhecida não é normalizada."""
    original = conjunto_ac01()[0]
    invalida = Tarefa(original.id_tarefa, original.data_criacao, original.prazo, "urgente", original.status, original.data_inicio, original.data_conclusao)
    with pytest.raises(ContratoInvalidoError, match="prioridade inválida"):
        ANALISADOR.analisar([invalida])


def test_ac07_fuso_utc_obrigatorio() -> None:
    """AC07: data sem fuso lança erro temporal."""
    original = conjunto_ac01()[0]
    invalida = Tarefa(original.id_tarefa, original.data_criacao, original.prazo.replace(tzinfo=None), original.prioridade, original.status, original.data_inicio, original.data_conclusao)
    with pytest.raises(DataInconsistenteError, match="prazo.*fuso UTC"):
        ANALISADOR.analisar([invalida])


def test_ac08_identificador_duplicado() -> None:
    """AC08: IDs repetidos são rejeitados."""
    item = conjunto_ac01()[0]
    with pytest.raises(ContratoInvalidoError, match="id_tarefa duplicado"):
        ANALISADOR.analisar([item, item])


def test_ac09_arredondamento_sem_arredondamento_intermediario() -> None:
    """AC09: valida média e taxa de atraso de três tarefas."""
    relatorio = ANALISADOR.analisar(conjunto_ac01()[:3])
    assert relatorio["geral"]["quantidade_tarefas"] == 3
    assert relatorio["geral"]["tempo_medio_conclusao_min"] == 50.0
    assert relatorio["geral"]["taxa_atraso_percentual"] == pytest.approx(33.33)


def test_ac10_duracao_zero() -> None:
    """AC10: conclusão igual ao início é válida."""
    original = conjunto_ac01()[0]
    zero = Tarefa(original.id_tarefa, original.data_criacao, original.prazo, original.prioridade, original.status, original.data_inicio, original.data_inicio)
    relatorio = ANALISADOR.analisar([zero])
    assert relatorio["geral"]["tempo_medio_conclusao_min"] == 0.0
    assert relatorio["geral"]["taxa_atraso_percentual"] == 0.0


def test_ac11_mudanca_de_dia() -> None:
    """AC11: intervalo que atravessa a meia-noite calcula duração completa."""
    criacao = dt(22)
    inicio = dt(23, 30)
    prazo = dt(0, 30, dia=3)
    conclusao = dt(0, 30, dia=3)
    item = tarefa(108, "baixa", "concluida", criacao, prazo, inicio, conclusao)
    relatorio = ANALISADOR.analisar([item])
    assert relatorio["geral"]["tempo_medio_conclusao_min"] == 60.0
    assert relatorio["geral"]["taxa_atraso_percentual"] == 0.0


def test_ac12_ordem_entrada_e_chamadas_independentes() -> None:
    """AC12: não altera a lista e chamadas sucessivas são independentes."""
    itens = conjunto_ac01()
    original = itens.copy()
    primeiro = ANALISADOR.analisar(itens)
    segundo = ANALISADOR.analisar(list(reversed(itens)))
    terceiro = ANALISADOR.analisar([itens[2]])
    assert itens == original
    assert primeiro == segundo
    assert terceiro["geral"]["quantidade_tarefas"] == 1
    assert terceiro["geral"]["tempo_medio_conclusao_min"] == 30.0


@pytest.mark.parametrize("identificador", [0, -1, True, 1.5])
def test_id_tarefa_invalido(identificador: object) -> None:
    """IDs não positivos, bool ou não inteiros são inválidos."""
    item = conjunto_ac01()[0]
    invalida = Tarefa(identificador, item.data_criacao, item.prazo, item.prioridade, item.status, item.data_inicio, item.data_conclusao)  # type: ignore[arg-type]
    with pytest.raises(ContratoInvalidoError, match="id_tarefa inválido"):
        ANALISADOR.analisar([invalida])


def test_entrada_nao_e_lista() -> None:
    """Entrada que não seja lista deve gerar erro de contrato."""
    with pytest.raises(ContratoInvalidoError, match="deve ser uma lista"):
        ANALISADOR.analisar(())  # type: ignore[arg-type]


def test_item_nao_e_tarefa() -> None:
    """Itens que não são Tarefa devem gerar erro de contrato."""
    with pytest.raises(ContratoInvalidoError, match="cada item deve ser Tarefa"):
        ANALISADOR.analisar([{"id_tarefa": 1}])  # type: ignore[list-item]


@pytest.mark.parametrize("status, conclusao", [
    ("desconhecido", None),
    ("pendente", dt(14)),
    ("concluida", None),
])
def test_status_e_conclusao_incompativeis(status: str, conclusao: datetime | None) -> None:
    """Status inválido ou incompatível com conclusão gera erro de contrato."""
    item = Tarefa(501, dt(7), dt(9), "media", status, None, conclusao)
    with pytest.raises(ContratoInvalidoError):
        ANALISADOR.analisar([item])


def test_datas_fora_de_utc_sao_rejeitadas() -> None:
    """Um deslocamento diferente de UTC não é aceito."""
    item = conjunto_ac01()[0]
    fuso = timezone(timedelta(hours=-3))
    invalida = Tarefa(item.id_tarefa, item.data_criacao.astimezone(fuso), item.prazo, item.prioridade, item.status, item.data_inicio, item.data_conclusao)
    with pytest.raises(DataInconsistenteError, match="UTC"):
        ANALISADOR.analisar([invalida])


def test_prazo_antes_da_criacao() -> None:
    """Prazo anterior à criação é uma inconsistência temporal."""
    item = tarefa(601, "baixa", "concluida", dt(9), dt(8), dt(9), dt(9))
    with pytest.raises(DataInconsistenteError, match="prazo anterior"):
        ANALISADOR.analisar([item])


def test_inicio_antes_da_criacao() -> None:
    """Início anterior à criação é uma inconsistência temporal."""
    item = tarefa(602, "baixa", "concluida", dt(9), dt(10), dt(8), dt(9, 30))
    with pytest.raises(DataInconsistenteError, match="data_inicio anterior"):
        ANALISADOR.analisar([item])

# Especificação SDD — TaskAnalyzer
**Bootcamp III | Fase 1 | Versão 1.0**

## Objetivo e escopo
Receber registros de tarefas em memória, validar consistência, selecionar tarefas concluídas e calcular duração e cumprimento de prazo. Não há persistência, interface gráfica, rede ou integração externa. IA auxilia no desenvolvimento, mas não participa dos cálculos em tempo de execução.

## Interface e modelos
A interface pública é `TaskAnalyzer.analisar(self, tarefas: list[Tarefa]) -> RelatorioAnalise`.
`Tarefa` é uma dataclass imutável. `Metricas` e `RelatorioAnalise` são TypedDicts no mesmo módulo.

Campos de `Tarefa`:
- `id_tarefa: int`: positivo, único no conjunto; bool não é aceito.
- `data_criacao: datetime`: obrigatória, com UTC explícito.
- `prazo: datetime`: obrigatória, não anterior à criação.
- `prioridade: str`: `baixa`, `media` ou `alta`.
- `status: str`: `concluida`, `pendente` ou `cancelada`.
- `data_inicio: datetime | None`: padrão None; quando presente, não anterior à criação.
- `data_conclusao: datetime | None`: padrão None; obrigatória para concluída e deve ser None para outros status.

Todas as datas devem ser objetos datetime com fuso e deslocamento UTC igual a zero. Conclusão não pode anteceder o início de referência (`data_inicio`, ou `data_criacao` quando não informado). Começar após o prazo é permitido. Validar todas as tarefas, inclusive pendentes e canceladas, antes de calcular.

## Saída
`RelatorioAnalise` contém exatamente `geral` e `indicadores_por_prioridade`. A segunda chave contém `baixa`, `media` e `alta`. Cada grupo tem exatamente `quantidade_tarefas: int`, `tempo_medio_conclusao_min: float` e `taxa_atraso_percentual: float`.

## Cálculos
A população é somente status `concluida`. Duração individual = (conclusão - início de referência) em segundos / 60. Média = soma das durações sem arredondamento intermediário / quantidade. Atraso ocorre somente se `data_conclusao > prazo`; igualdade ao prazo não é atraso. Taxa = atrasadas / concluídas * 100. Médias e taxas arredondadas com `round(valor, 2)`. Para grupo sem concluídas, retornar zeros `0`, `0.0`, `0.0`. Lista vazia ou sem concluídas gera `NenhumaTarefaConcluidaError` com mensagem `Análise indisponível: nenhuma tarefa concluída`.

## Exceções
- `ContratoInvalidoError(ValueError)`: lista/objeto incompatível, ID inválido ou duplicado, prioridade/status desconhecidos e incompatibilidade status/conclusão.
- `DataInconsistenteError(ValueError)`: tipo temporal incorreto, fuso ausente/não UTC, prazo anterior à criação, início anterior à criação ou conclusão anterior ao início de referência.
- `NenhumaTarefaConcluidaError(ValueError)`: ausência de concluídas após validação.

## Cenários de aceite
- AC01: conjunto principal retorna geral 5 / 78.00 min / 40.00%; alta 2 / 60 / 50%; media 2 / 60 / 50%; baixa 1 / 150 / 0%.
- AC02: conclusão anterior ao início gera `DataInconsistenteError`.
- AC03: lista vazia ou apenas pendentes/canceladas gera `NenhumaTarefaConcluidaError`.
- AC04: somente tarefa 103 retorna média 30 min e atraso 0%; grupos sem dados são zeros.
- AC05: somente tarefa 105 usa criação como referência e retorna 150 min.
- AC06: prioridade desconhecida gera `ContratoInvalidoError`.
- AC07: data sem fuso gera `DataInconsistenteError`.
- AC08: ID duplicado gera `ContratoInvalidoError`.
- AC09: tarefas 101, 102 e 103 retornam 3, média 50 min e atraso 33.33%.
- AC10: duração zero é válida.
- AC11: mudança de dia é calculada corretamente.
- AC12: resultado independe da ordem, entrada não é mutada e chamadas sucessivas são independentes.

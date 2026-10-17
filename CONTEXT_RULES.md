# CONTEXT_RULES.md — Governança de IA

## Diretrizes técnicas obrigatórias
- Usar Python 3.11 ou superior.
- Usar type hints em funções, métodos, parâmetros e retornos.
- Preservar os contratos `Tarefa`, `Metricas` e `RelatorioAnalise`.
- Aplicar responsabilidade única (SRP), PEP 8 e funções pequenas e coesas.
- Documentar módulos, classes, funções e métodos com Google style docstrings; incluir Args, Returns e Raises quando aplicável.
- Usar as exceções previstas no contrato, com mensagens explicativas.
- Usar o módulo padrão `logging`, com eventos estruturados e sem conteúdo pessoal.
- Manter `Tarefa` imutável, não reorganizar nem alterar a lista recebida e não acumular resultados entre chamadas.
- Usar somente a biblioteca padrão no código de produção. `pytest` é a única dependência externa autorizada para desenvolvimento/testes.

## Restrições
- Não alterar os cenários de aceite para encobrir defeitos.
- Não mudar a organização de pastas nem as assinaturas públicas sem autorização.
- Não persistir tarefas ou resultados em arquivos/bancos de dados durante a execução do analisador.
- Não adicionar funcionalidades sem testes correspondentes ou dependências não autorizadas.
- Não inventar regras, resultados, campos ou funcionalidades fora da especificação.
- Não converter entradas silenciosamente para fazê-las parecer válidas.
- Não incluir segredos ou registros pessoais reais em exemplos, prompts, logs ou commits.
- Não fazer chamadas de rede para calcular métricas.

## Protocolo de geração e homologação
Antes de cada solicitação à IA, fornecer a versão do contrato, estas regras e os testes relacionados. Pedir à IA que explique entradas, cálculos e exceções. Depois de gerar alterações, comparar o código com o contrato, executar os testes e revisar legibilidade, tipos, logs e ausência de dependências indevidas. Qualquer mudança de regra deve ser decidida por uma pessoa e registrada antes de orientar nova geração.

## Registro de homologação humana
A aprovação final deve ser feita pela estudante: conferir manualmente AC01 (média ponderada por quantidade e atraso), datas de mudança de dia, grupos vazios, chamadas sucessivas, imutabilidade e mensagens de erro. A autoria assistida por IA não substitui revisão humana.

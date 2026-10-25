# Relatório de Governança, Segurança e Ética no Uso de IA

**Projeto:** TaskAnalyzer  
**Disciplina:** Bootcamp III  
**Etapa:** Fase 3 — Entrega Final  
**Repositório:** https://github.com/luisabroocke/sdd-taskanalyzer

## 1. Objetivo

Este relatório documenta as práticas de governança, segurança e ética adotadas no desenvolvimento do TaskAnalyzer com apoio de ferramentas de Inteligência Artificial (IA).

O projeto utiliza uma abordagem orientada por especificação (SDD — Specification-Driven Development), na qual o contrato técnico e as regras de contexto orientam a geração e a validação do código.

O objetivo é reduzir riscos de respostas incorretas da IA, preservar os requisitos definidos na Fase 1 e garantir que a implementação seja verificada por testes automatizados e revisão humana.

## 2. Governança de contexto e especificação

O desenvolvimento foi orientado pelos seguintes documentos:

- `CONTEXT_RULES.md`: estabelece as regras e restrições que devem orientar o trabalho assistido por IA.
- `specs/task_analyzer_spec.md`: define o contrato técnico, as validações, os cálculos, as exceções e os resultados esperados.
- `tests/test_harness.py`: contém os testes automatizados utilizados para verificar o comportamento da implementação.

Esses documentos cumprem funções complementares. A especificação define o comportamento esperado, as regras de contexto limitam as decisões do assistente e os testes verificam se a implementação atende aos cenários estabelecidos.

Alterações no contrato ou nos critérios de aceite devem ser submetidas à revisão humana, em vez de serem realizadas unilateralmente pelo assistente de IA.

## 3. Análise de alucinações da IA

Uma alucinação ocorre quando uma ferramenta de IA produz informações, regras ou código incorretos, sem fundamento suficiente nos requisitos fornecidos.

No contexto do TaskAnalyzer, foram considerados os seguintes riscos:

| Risco | Possível consequência | Medida de prevenção |
|---|---|---|
| Inventar regras de negócio | Resultados diferentes dos especificados | Consultar o contrato SDD antes de aceitar alterações |
| Omitir validações | Aceitação de tarefas inválidas | Executar os testes automatizados e revisar os casos de erro |
| Calcular indicadores incorretamente | Médias ou percentuais incorretos | Comparar os resultados com os cenários de aceite |
| Alterar nomes ou estruturas do contrato | Incompatibilidade com os consumidores do sistema | Conferir assinaturas, chaves de retorno e exceções |
| Introduzir dependências não autorizadas | Aumento da complexidade e descumprimento das regras | Conferir `requirements.txt` e as regras do projeto |
| Afirmar que algo funciona sem evidências | Aprovação indevida de código defeituoso | Exigir resultados verificáveis dos testes e do pipeline |

Esses itens representam riscos analisados para o projeto; não significam que todos tenham ocorrido durante a implementação.

A estratégia adotada é tratar as respostas da IA como propostas que precisam ser confrontadas com a especificação e com evidências de execução.

## 4. Segurança e qualidade do código

As práticas de segurança e qualidade consideradas no projeto incluem:

- Utilização de dependências declaradas em `requirements.txt`.
- Execução dos testes em ambiente automatizado no GitHub Actions.
- Utilização de Python 3.11 no pipeline e na imagem Docker.
- Isolamento do ambiente de execução dos testes por meio de contêiner.
- Versionamento das alterações por commits e branches.
- Preservação dos arquivos de especificação e das regras de contexto.
- Revisão das alterações antes de sua incorporação à branch principal.

O TaskAnalyzer realiza análises em memória e não necessita de banco de dados ou comunicação com serviços externos para calcular seus indicadores.

A containerização torna o ambiente de execução mais reproduzível, mas não elimina todos os riscos de segurança. A imagem, as dependências e as permissões de execução ainda devem ser mantidas e revisadas.

## 5. Validação humana e testes automatizados

A validação combina critérios definidos por pessoas com verificações automatizadas.

A revisão humana deve verificar:

1. A conformidade do código com `CONTEXT_RULES.md`.
2. A correspondência entre a implementação e `task_analyzer_spec.md`.
3. O tratamento de entradas inválidas e datas inconsistentes.
4. A correção dos cálculos e dos resultados retornados.
5. A ausência de alterações indevidas no contrato técnico.
6. Os resultados dos testes e da construção da imagem Docker.

Na Fase 3, o workflow do GitHub Actions foi atualizado para utilizar Python 3.11, executar os testes com pytest e validar a construção da imagem Docker.

As execuções verificadas após a inclusão dos arquivos de containerização apresentaram resultado positivo para os jobs de testes e Docker na branch `feature/fase3-cicd-docker`.

Esses resultados demonstram a aprovação das verificações executadas nesses commits. A homologação definitiva também depende da revisão do conteúdo, da conferência dos requisitos e da integração final das alterações.

## 6. CI/CD e containerização

A automação foi configurada em `.github/workflows/tests.yml`.

O workflow executa os seguintes procedimentos:

1. Obtém os arquivos do repositório.
2. Configura o Python 3.11.
3. Instala as dependências declaradas.
4. Executa os testes automatizados.
5. Constrói a imagem Docker após a aprovação dos testes.

O arquivo `Dockerfile` define o ambiente de execução dos testes, enquanto `docker-compose.yml` permite construir e executar o serviço de testes por meio do Docker Compose.

Essa configuração reduz a necessidade de preparar manualmente o ambiente e permite identificar falhas durante o desenvolvimento.

## 7. Responsabilidade ética

O uso de IA não transfere ao assistente a responsabilidade pela qualidade do software.

A responsabilidade pela aprovação da implementação permanece com a pessoa que desenvolve e homologa o sistema.

As principais diretrizes éticas adotadas são:

- Não aceitar automaticamente todas as sugestões produzidas pela IA.
- Não substituir requisitos definidos por suposições do assistente.
- Não declarar testes aprovados sem evidências verificáveis.
- Preservar a rastreabilidade das alterações por meio do Git.
- Documentar limitações e problemas encontrados.
- Submeter mudanças relevantes a revisão humana.

A IA é utilizada como ferramenta de apoio à produtividade, não como substituta do julgamento técnico.

## 8. Conclusão

O desenvolvimento do TaskAnalyzer combina especificação técnica, regras de contexto, testes automatizados, versionamento e containerização.

A integração contínua e a construção da imagem Docker foram verificadas com sucesso nas execuções mais recentes consultadas durante a Fase 3.

A abordagem adotada reduz os riscos de implementação divergente, facilita a identificação de erros e mantém a revisão humana como parte essencial da homologação.

A aprovação final do projeto deve considerar o contrato SDD, as regras de contexto, os resultados dos testes, a execução em contêiner e a revisão das alterações antes do merge na branch principal.

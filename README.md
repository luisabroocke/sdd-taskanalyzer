# TaskAnalyzer — Bootcamp III (Fase 2)

Implementação assistida por IA do contrato SDD da Fase 1, com validação humana e Test Harness `pytest`.

## Escopo
O TaskAnalyzer recebe uma lista de objetos `Tarefa` em memória, valida todos os registros e calcula quantidade de tarefas concluídas, média de duração em minutos e taxa de atraso geral e por prioridade. Não usa banco de dados, arquivos de dados, interface, rede ou serviços externos.

## Estrutura
```text
sdd-task-analyzer/
├── README.md
├── CONTEXT_RULES.md
├── .gitignore
├── requirements.txt
├── specs/
│   └── task_analyzer_spec.md
├── tests/
│   └── test_harness.py
└── src/
    ├── __init__.py
    └── task_analyzer.py
```

## Requisitos
- Python 3.11+
- `pytest` para desenvolvimento e testes
- Código de produção usando apenas biblioteca padrão

## Instalação e testes
Windows PowerShell, na raiz do repositório:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest tests/test_harness.py -v
```

Linux/macOS:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest tests/test_harness.py -v
```

## Exemplo mínimo
```python
from datetime import datetime, timezone
from src.task_analyzer import Tarefa, TaskAnalyzer

criado = datetime(2026, 9, 2, 9, 0, tzinfo=timezone.utc)
concluido = datetime(2026, 9, 2, 9, 30, tzinfo=timezone.utc)
tarefa = Tarefa(
    id_tarefa=1,
    data_criacao=criado,
    prazo=concluido,
    prioridade="media",
    status="concluida",
    data_inicio=criado,
    data_conclusao=concluido,
)
print(TaskAnalyzer().analisar([tarefa]))
```

## Contrato e governança
Leia `CONTEXT_RULES.md` e `specs/task_analyzer_spec.md` antes de solicitar alterações à IA. As regras e cenários AC01–AC12 não devem ser flexibilizados para fazer testes passarem.

## Git/GitHub — fluxo sugerido
- `main`: versão aprovada.
- `develop`: integração, se adotada no fluxo.
- `feature/sdd-specification`, `feature/test-harness`, `feature/task-analyzer-impl`: mudanças isoladas.
- Faça commits atômicos e abra PR para revisão humana antes de integrar.

Exemplos de mensagens:
- `docs: adiciona contrato SDD e regras de contexto`
- `test: adiciona Test Harness para cenários AC01–AC12`
- `feat: implementa validação e métricas do TaskAnalyzer`

## Checklist da entrega
- [ ] Repositório público `sdd-task-analyzer`
- [ ] Branches e commits descritivos
- [ ] Pelo menos um Pull Request documentado/revisado
- [ ] `pytest` aprovado e captura de tela do terminal
- [ ] Captura de tela da árvore de arquivos no GitHub
- [ ] Captura de tela do PR no GitHub
- [ ] Vídeo horizontal de 5 minutos, com áudio e câmera visíveis, publicado como Público ou Não listado
- [ ] PDF final com link do repositório, evidências, relato de prompts/homologação e link do vídeo

## Homologação humana
O código foi preparado para revisão, mas a estudante deve executar os testes no próprio ambiente, revisar as regras e registrar as evidências reais. Não declare resultados de testes, PRs ou vídeos que ainda não foram executados/criados.

 

---

## Fase 3 — CI/CD, Docker e Governança de IA

Esta etapa amplia o projeto TaskAnalyzer com integração contínua, execução isolada dos testes e documentação das práticas de governança e uso responsável de Inteligência Artificial. O escopo funcional e o contrato SDD definidos nas etapas anteriores devem ser preservados.

### Integração contínua — GitHub Actions

O workflow `.github/workflows/tests.yml` automatiza a validação do projeto por meio de:

- Configuração do Python 3.11.
- Instalação das dependências declaradas em `requirements.txt`.
- Execução dos testes automatizados com `pytest`.
- Construção da imagem Docker para verificar a configuração de containerização.

O workflow está configurado para executar em eventos de `push` nas branches `main`, `develop` e `feature/**`, além de `pull_request` direcionado a `main` e `develop`.

Os resultados das execuções devem ser consultados na aba **Actions** do GitHub. A aprovação de cada execução deve ser comprovada pelas evidências correspondentes.

### Docker e Docker Compose

O projeto utiliza os arquivos `Dockerfile` e `docker-compose.yml` para permitir a execução dos testes em um ambiente isolado, baseado em Python 3.11.

Para construir a imagem Docker:

```bash
docker build -t task-analyzer .
```

Para executar os testes no contêiner:

```bash
docker run --rm task-analyzer
```

Para executar os testes com Docker Compose:

```bash
docker compose up --build --abort-on-container-exit --exit-code-from task-analyzer-tests
```

Os comandos devem ser executados no terminal, na raiz do repositório, em um ambiente com Docker instalado e em execução.

### Governança e uso responsável da IA

A governança do projeto considera os seguintes elementos:

- `CONTEXT_RULES.md`: orientações e restrições para o desenvolvimento assistido por IA.
- `specs/task_analyzer_spec.md`: contrato técnico e critérios de aceite do sistema.
- `tests/test_harness.py`: validação automatizada do comportamento esperado.
- `RELATORIO_GOVERNANCA_ETICA_IA.md`: registro dos riscos, das medidas de controle e da responsabilidade humana no uso da IA.

As respostas e sugestões geradas por IA devem ser tratadas como propostas sujeitas a verificação. A especificação, as regras de contexto e os testes devem orientar a implementação. A revisão humana é necessária para identificar possíveis alucinações, avaliar alterações e confirmar a conformidade antes da integração.

### Homologação da Fase 3

A homologação deve verificar:

- [ ] Workflow do GitHub Actions executado com sucesso.
- [ ] Testes automatizados aprovados.
- [ ] Imagem Docker construída com sucesso.
- [ ] Testes executados no contêiner.
- [ ] Documentação de governança e ética revisada.
- [ ] Alterações revisadas antes do merge para a branch principal.
- [ ] Capturas de tela das evidências reais organizadas para a entrega.
- [ ] Vídeo técnico e PDF final preparados conforme as orientações do desafio.

Os itens devem ser marcados somente depois da verificação correspondente. Resultados, capturas de tela e homologações devem refletir o que foi efetivamente executado.

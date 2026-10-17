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

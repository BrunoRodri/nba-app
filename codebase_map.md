# 🏀 NBA Stats Explorer — Codebase Map

Este documento serve como um mapa da base de código do **NBA Stats Explorer**. Use-o em futuros prompts para rapidamente dar contexto a IA sobre como o projeto está estruturado e como suas partes se comunicam.

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.13, Django 6.0.5, Celery (Async Tasks)
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
- **API Externa:** `nba_api` (biblioteca oficial para acesso aos dados da NBA)
- **Banco de Dados:** PostgreSQL (Produção/Docker) / SQLite (Desenvolvimento Local)
- **Infraestrutura:** Docker & Docker Compose (Serviços: App, DB, Redis, Worker, Beat)
- **Cache & Message Broker:** Redis
- **Estilo:** Design Premium (Permanent Dark Mode), Gradientes Dinâmicos, Micro-animações de Scroll.

---

## 📂 Estrutura de Diretórios (Arquitetura)

```text
nba/
├── nba_explorer/           # ⚙️ Configurações e Inicialização do Django & Celery
├── static/                 # 🎨 Ativos Globais (CSS/JS customizado)
├── stats/                  # 🏀 App Principal (Lógica de Negócio)
│   ├── management/         # Comandos customizados (ex: populate_cache)
│   ├── templatetags/       # Filtros customizados (formatação de stats, datas e dicts)
│   ├── templates/stats/    # Interface do usuário (Django Templates)
│   ├── scratch/            # Scripts utilitários e testes de lógica (ex: Brackets, PP)
│   ├── services.py         # Abstração de chamadas à API da NBA
│   ├── tasks.py            # Definição de tarefas assíncronas (Celery)
│   └── views.py            # Lógica de rotas e orquestração de dados
├── theme/                  # 🖋️ Configuração e Build do Tailwind CSS
├── Dockerfile              # Receita da imagem da aplicação
├── docker-compose.yml      # Definição de containers (Multi-container setup)
├── requirements.txt        # Dependências do projeto
└── manage.py               # Utilitário de linha de comando do Django
```

---

## 🧠 Core Components (Módulos Principais)

### 1. `stats/services.py`
**O Coração dos Dados.** Abstrai a complexidade da `nba_api`.
*   **Playoff Bracket (`get_playoff_bracket`):** Mapeia toda a árvore de playoffs. Cruza dados de séries (`CommonPlayoffSeries`) com resultados de jogos para calcular o status de cada confronto em tempo real. Organiza os dados em uma estrutura hierárquica (Round 1 -> Semis -> Finals) separada por Conferência.
*   **Game Boxscore (V3):** Utiliza os novos endpoints da NBA (V3) para garantir dados precisos e scores por período em tempo real, evitando bugs de dados zerados presentes nas versões legadas.

### 2. `stats/tasks.py` & Celery
**Processamento em Segundo Plano.** Garante performance e dados sempre frescos.
*   `update_player_cache_task`: Roda via `Celery Beat` para atualizar o cache local de jogadores e times, evitando lentidões na busca e autocomplete.
*   `debug_ping`: Tarefa de diagnóstico para validar a conectividade entre App -> Redis -> Worker.

### 3. `stats/templatetags/stat_filters.py`
**Formatação Inteligente.** Filtros para garantir que os dados brutos da API sejam legíveis:
*   `format_pct`: Converte decimais (0.485) em percentuais (48.5%).
*   `format_stat`: Arredonda médias para uma casa decimal.
*   `format_date`: Padroniza datas da API (YYYY-MM-DD) para o formato brasileiro (DD-MM-YYYY).
*   `get_item`: Facilita o acesso dinâmico a chaves de dicionários dentro dos templates.

### 4. `stats/templates/stats/standings.html`
**Dashboard Central.** Exibe a Classificação da Temporada Regular e o **Playoff Bracket**.
*   **Bracket Design:** Utiliza uma estrutura CSS complexa para exibir chaves tradicionais. A lógica de renderização suporta "Seeds", placares de séries e estados de "concluído".
*   **Interatividade:** Usa o `app.js` para alternar entre as visões de Tabelas e Brackets sem refresh, mantendo uma experiência de SPA.

---

## 🏗️ Infraestrutura & Docker
O projeto agora é totalmente containerizado para garantir paridade entre ambientes:
*   **App:** O container Python/Django.
*   **Postgres:** Banco de dados relacional persistente.
*   **Redis:** Atua como Broker para o Celery e Backend para cache.
*   **Worker:** Executa as tarefas de `tasks.py`.
*   **Beat:** O agendador de tarefas cronometradas.

---

## 🐛 Pontos de Atenção (Gotchas)
1. **Conectividade Docker:** Em ambiente Docker, use os nomes dos serviços (ex: `redis`, `db`) nas variáveis de ambiente em vez de `localhost`.
2. **Skeleton Loading:** As views principais (`team_detail`, `player_detail`, `game_detail`, `standings`) usam o padrão de fetch em duas etapas. Se você adicionar uma nova página pesada, lembre-se de implementar o suporte ao parâmetro `?fetch=1`.

---
**Dica para os próximos prompts:** Referencie este `codebase_map.md` sempre que quiser adicionar novos recursos que envolvam tarefas assíncronas ou mudanças na infraestrutura Docker.

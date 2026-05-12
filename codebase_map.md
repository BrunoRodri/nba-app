# 🏀 NBA Stats Explorer — Codebase Map

Este documento serve como um mapa da base de código do **NBA Stats Explorer**. Use-o em futuros prompts para rapidamente dar contexto a IA sobre como o projeto está estruturado e como suas partes se comunicam.

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.13, Django 6.0.5
- **Frontend:** HTML5, Tailwind CSS (via `django-tailwind`), Vanilla JavaScript
- **API Externa:** `nba_api` (biblioteca oficial da comunidade para acessar a API da NBA)
- **Banco de Dados:** PostgreSQL (Docker) / SQLite (Local dev fallback)
- **Infraestrutura:** Docker & Docker Compose
- **Estilo:** Dark Mode Nativo, Design Responsivo, Gradientes Dinâmicos por Time.

---

## 📂 Estrutura de Diretórios (Arquitetura)

O projeto segue a estrutura padrão do Django, subdividido principalmente em `nba_explorer` (configurações) e `stats` (app principal).

```text
nba/
├── nba_explorer/           # Configurações globais do Django
├── static/                 # Arquivos estáticos (CSS/JS)
├── stats/                  # 🏀 App Principal de Estatísticas
├── theme/                  # App do Tailwind CSS
├── Dockerfile              # Definição da imagem da aplicação
├── docker-compose.yml      # Orquestração (App + PostgreSQL)
├── .env.example            # Modelo de variáveis de ambiente
├── requirements.txt        # Dependências Python
└── manage.py               # Entrypoint do Django
```

---

## 🧠 Core Components (Módulos Principais)

### 1. `stats/services.py`
**A Camada de Inteligência / Proxy da API.**
É o arquivo mais crítico do backend. Nenhuma View interage com a `nba_api` diretamente; elas chamam as funções do `services.py`.
*   `get_team_info(team_id)`: Retorna os dados básicos da franquia (`TeamDetails`).
*   `get_team_season_record(team_id, season)`: Calcula vitórias, derrotas e traz os últimos 10 jogos da temporada regular (`LeagueGameFinder`).
*   `get_team_history(team_id)`: Traz o histórico de vitórias/derrotas de todas as temporadas (`TeamYearByYearStats`).
*   `get_player_info(player_id)`: Traz dados biográficos (`CommonPlayerInfo`).
*   `get_player_career_stats(player_id)`: Estatísticas da carreira do jogador (`PlayerCareerStats`).
*   `get_game_boxscore(game_id)`: Traz o boxscore completo de uma partida, utilizando os **Endpoints V3** (`BoxScoreSummaryV3`, `BoxScoreTraditionalV3`, `BoxScoreMiscV3`) para resolver bugs de dados zerados em temporadas recentes.

### 2. `stats/views.py`
**Controladores de Rota.**
Lidam com a requisição do usuário. *Padrão de UX Moderno:* implementam retorno em **duas etapas** (Skeleton Pattern).
*   Se a requisição vier sem o parâmetro `?fetch=1`, as views retornam instantaneamente `loading_skeleton.html`.
*   Se a requisição contiver `?fetch=1`, elas invocam `services.py`, processam os dados, interceptam eventuais *Timeouts* da API da NBA (`api_error=True`) e retornam a página real.
*   **Rotas:** `index`, `search`, `player_detail`, `team_detail`, `team_season_games`, `game_detail`, `api_search`.

### 3. Templates HTML (`stats/templates/stats/`)
**A Camada de Apresentação.**
*   `base.html`: Navbar de navegação, barra de pesquisa, botão Dark Mode, carregamento de estilos.
*   `index.html`: Grid de times e lista de jogadores em destaque.
*   `loading_skeleton.html`: Tela de carregamento nativa. Ao ser renderizada, ela roda um script JS que usa `fetch()` para puxar silenciosamente o conteúdo real da rota e substituir a tela.
*   `team_detail.html` / `player_detail.html`: Exibição rica em detalhes. Têm suporte a tela de "Erro de Conexão" caso a view dispare a flag `api_error` (Timeouts da NBA).
*   `game_detail.html` & `_team_boxscore.html`: Visualização de pontuação quarto a quarto, estatísticas de equipes, lideranças e lista completa de pontuação dos jogadores, com tratamento de jogadores inativos (DNP).

### 4. Frontend (`static/js/app.js`)
*   **Autocomplete (`initAutocomplete`):** Intercepta o input de busca, faz fetch em `/api/search/` e desenha um dropdown com resultados e headshots instantaneamente.
*   **Animações (`initAnimations`):** Implementa um `IntersectionObserver` que adiciona efeitos de *fade-in* e *slide-up* conforme o usuário faz o scroll pela página.
*   **Design:** O tema claro foi removido em favor de um design premium permanentemente escuro.

---

## 🐛 Pontos de Atenção & Manutenção (Gotchas)
1. **API Timeouts:** A `nba_api` faz raspagem oficial de `stats.nba.com`. Este servidor bloqueia conexões em excesso (rate-limit) ou demora a responder (> 15s). O projeto mitiga isso usando `api_error` nas views e informando o usuário na tela de UI de erro.
2. **Endpoints V2 vs V3:** O Boxscore de partidas precisou ser migrado dos Endpoints V2 (descontinuados/zerados para a temporada 25-26) para os Endpoints V3. Se mais informações de jogos começarem a voltar com valores nulos, a solução será inspecionar a documentação da `nba_api` para atualizar outros módulos V2 remanescentes para V3.
3. **Skeleton Loading Pattern:** O fluxo atual é: URL muda instantaneamente -> Servidor retorna `loading_skeleton.html` vazio -> Javascript na página dispara um `fetch('...?fetch=1')` -> Resposta HTML substitui a tag `<main>` atual.

---
**Dica para os próximos prompts:** Você pode me pedir para ler este arquivo referenciando `codebase_map.md` sempre que mudarmos de contexto ou iniciarmos um novo dia de trabalho no projeto.

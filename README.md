<p align="center">
  <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/basketball.svg" width="80" alt="Basketball" />
</p>

<h1 align="center">🏀 NBA Stats Explorer</h1>

<p align="center">
  <strong>Explore estatísticas detalhadas de jogadores e times da NBA em tempo real.</strong>
</p>

  <img src="https://img.shields.io/badge/django-5.1+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/tailwind-css-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/lang-pt--BR-green?style=flat-square" alt="Language" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
</p>

---

## ✨ Funcionalidades

- 🔍 **Busca inteligente** — pesquise por nome de jogador ou time com autocomplete
- 🧑‍💼 **Perfil de jogador** — foto, bio, estatísticas por temporada e médias de carreira
- 🏟️ **Página do time** — elenco completo, recorde W-L, últimos jogos e histórico ano a ano
- 📊 **Game log** — todos os jogos de uma temporada (regular + playoffs) com placar
- 🏆 **Playoff Bracket** — visualização interativa das chaves de playoffs em tempo real
- 🎨 **Estilo Dinâmico** — perfis de jogadores com gradientes baseados nas cores do time atual
- 🌑 **Tema Escuro Nativo** — design premium focado em modo escuro permanente
- 📱 **Responsivo** — interface adaptada para desktop, tablet e mobile
- ⚡ **Cache local** — buscas instantâneas com SQLite + dados em tempo real da API da NBA

---

## 🚀 Começando

### Pré-requisitos

- Python 3.10+

### Instalação com Docker (Recomendado)

A maneira mais rápida de rodar o projeto é usando Docker:

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/nba-stats-explorer.git
cd nba-stats-explorer

# 2. Crie o arquivo .env
cp .env.example .env

# 3. Suba os containers
docker compose up --build
```

Acesse **http://localhost:8000**. O banco PostgreSQL será configurado automaticamente.

> [!IMPORTANT]
> **O CSS não aparece?** Como o Docker usa os arquivos estáticos pré-compilados, você deve gerar o CSS do Tailwind na sua máquina local pelo menos uma vez antes de rodar o Docker:
> ```bash
> python manage.py tailwind install
> python manage.py tailwind build
> ```

### 🐋 Docker sem sudo (Linux)
Se você receber um erro de "permission denied" ao rodar o Docker, execute o comando abaixo para ativar as permissões no seu terminal atual:
```bash
newgrp docker
```

### Instalação Manual (Desenvolvimento)

Se preferir rodar sem Docker:

```bash
# 1. Crie o ambiente virtual e instale dependências
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure o banco SQLite
python manage.py migrate
python manage.py populate_cache

# 3. Rodar Tailwind e Django em terminais separados
python manage.py tailwind start
python manage.py runserver
```

### Rodando o projeto

Em dois terminais separados:

```bash
# Terminal 1 — servidor Django
python manage.py runserver

# Terminal 2 — watch do Tailwind CSS
python manage.py tailwind start
```

Acesse **http://localhost:8000** no navegador.

---

## 🧭 Rotas da aplicação

| Rota                            | Descrição                                      |
| ------------------------------- | ---------------------------------------------- |
| `/`                             | Página inicial com grid dos 30 times           |
| `/search/?q=LeBron`            | Resultados de busca por jogadores e times      |
| `/player/<id>/`                 | Perfil detalhado do jogador                    |
| `/team/<id>/`                   | Perfil do time com elenco e jogos recentes     |
| `/team/<id>/season/2024-25/`    | Todos os jogos do time em uma temporada        |
| `/standings/`                  | Classificação da temporada e Bracket de Playoffs|
| `/api/search/?q=...`            | API de autocomplete (JSON)                     |
| `/admin/`                       | Django Admin                                   |

---

## 🗄️ Estrutura do projeto

```
nba/
├── nba_explorer/          # Configurações do Django (settings, urls, wsgi)
├── stats/                 # App principal
│   ├── models.py          # Modelos CachedPlayer e CachedTeam
│   ├── views.py           # Views (index, search, player_detail, team_detail, api)
│   ├── services.py        # Camada de abstração da API da NBA
│   ├── urls.py            # Rotas do app
│   ├── management/        # Comando populate_cache
│   └── templates/stats/   # Templates HTML (base, index, player_detail, team_detail, etc.)
├── theme/                 # Configuração do django-tailwind
├── static/                # CSS e JS customizados
├── requirements.txt       # Dependências do projeto
└── manage.py              # CLI do Django
```

---

## 🛠️ Tecnologias

| Tecnologia               | Uso                              |
| ------------------------ | -------------------------------- |
| [Django](https://www.djangoproject.com/) 5.1+ | Framework web        |
| [nba_api](https://github.com/swar/nba_api) | Dados oficiais da NBA em tempo real |
| [Tailwind CSS](https://tailwindcss.com/) + django-tailwind | Estilização moderna com dark mode |
| [PostgreSQL](https://www.postgresql.org/) | Banco de dados principal (via Docker) |
| [Docker](https://www.docker.com/) | Containerização e infraestrutura |
| [Vanilla JS](https://www.javascript.com/) | Autocomplete e animações |

---

## 📸 Screenshots

<table>
  <tr>
    <td><b>Home — Hero + Times</b></td>
    <td><b>Busca com Autocomplete</b></td>
  </tr>
  <tr>
    <td>Busca principal com sugestões populares e grid dos 30 times da NBA</td>
    <td>Resultados instantâneos conforme você digita, com fotos e logos</td>
  </tr>
  <tr>
    <td><b>Perfil do Jogador</b></td>
    <td><b>Playoff Bracket</b></td>
  </tr>
  <tr>
    <td>Bio, headshot, estatísticas por temporada e game log recente</td>
    <td>Chaveamento tradicional de playoffs com vitórias atualizadas ao vivo</td>
  </tr>
</table>

---

## ⚠️ Aviso

Este projeto **não é afiliado à NBA**. Os dados são fornecidos pela biblioteca open-source [nba_api](https://github.com/swar/nba_api), que consome a API pública do NBA.com. O uso é destinado apenas para fins educacionais e de estudo.

---

## 📄 Licença

MIT © 2025 NBA Stats Explorer
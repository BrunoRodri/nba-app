FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências do sistema para o PostgreSQL e build
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Instala o executável standalone do Tailwind e compila o CSS
RUN python manage.py tailwind install
RUN python manage.py tailwind build

# Coleta os arquivos estáticos para o Django
RUN python manage.py collectstatic --no-input --clear


# O comando de inicialização padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


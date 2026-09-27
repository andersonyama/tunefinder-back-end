# Define a imagem base
FROM python:3.13.15

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .
COPY .env .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o diretório de trabalho
COPY src/ .

# Executa a API
CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0", "--port", "5000"]
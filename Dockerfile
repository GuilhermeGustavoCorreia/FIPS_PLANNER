# Use uma imagem base do Python
FROM python:3.10
# Defina o diretório de trabalho no contêiner
WORKDIR /app


# Copie o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o contêiner
COPY . .

# Defina a variável de ambiente para o Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Exponha a porta que o Django irá rodar
EXPOSE 8000

# Comando para rodar o aplicativo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
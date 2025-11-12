# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão do Render
EXPOSE 10000

# Comando de inicialização
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "10000"]

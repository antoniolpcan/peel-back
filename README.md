# <img src="./docs/logo.png" width="150" height="150" alt="Logo" align="center" /> Peel (Back-end)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

O **Peel** é uma rede social baseada na simplicidade dos *post-its*. Este repositório concentra a inteligência do ecossistema, expondo uma API robusta, assíncrona e performática.

## Arquitetura e Tecnologias

O projeto foi construído utilizando **FastAPI (Python)** para a criação de rotas rápidas e assíncronas, e **PostgreSQL** como banco de dados relacional.

A API foi estruturada seguindo rigorosamente o padrão CSR (**Controller-Service-Repository**):

*   **Controllers (Rotas/Routers):** Funcionam como a porta de entrada da aplicação. Eles recebem as requisições HTTP do FastAPI, validam os dados de entrada (geralmente usando Pydantic) e apenas chamam os serviços necessários, sem conhecer as regras de negócio ou de banco.
*   **Services (Serviços):** É o coração da aplicação. Onde reside toda a lógica de negócios da rede social (como regras para criar um post-it, interações e validações de usuários). Eles orquestram o fluxo antes de enviar os dados para a persistência.
*   **Repositories (Repositórios):** A camada isolada responsável estritamente pelo acesso ao banco de dados. Ela executa as consultas SQL ou operações do ORM no PostgreSQL, garantindo que o resto do código não precise saber como os dados são salvos.

Essa abordagem — combinada com a poderosa injeção de dependências do FastAPI — garante que o código seja altamente testável, modular, fácil de manter e pronto para escalar.

## 📊 Modelagem do Banco de Dados

A estrutura e o relacionamento das tabelas do PostgreSQL foram mapeados no DrawSQL:

🔗 [Acessar versão interativa no DrawSQL](https://drawsql.app/teams/antonio-pereira/diagrams/peel/embed)

![Diagrama do Banco de Dados](docs/diagram_v5.webp)

## 🔒 Variáveis de Ambiente

O projeto utiliza o [**Cloudinary**](https://cloudinary.com/) para armazenamento de mídia, **PostgreSQL** para armazenamento de dados, envios de email via **SMTP** e **JWT** para autenticação. Na raiz do projeto, você encontrará um arquivo chamado **.env.example**, que obrigatoriamente deve ser preenchido para que esses serviços funcionem.

Duplique esse arquivo, renomeie a cópia para **.env** e preencha com seus respectivos valores.

## 🛠️ Executando o projeto

Para rodar o back-end localmente na sua máquina, siga os passos abaixo:

```cmd
    cd peel-backend

    # Instale as dependências necessárias:
    pip install -r requirements.txt

    # Inicialize o servidor de desenvolvimento do FastAPI:
    uvicorn app.main:app --reload
```

A API estará disponível por padrão em http://127.0.0.1:8000 e a documentação interativa automática (Swagger UI) em http://127.0.0.1:8000/docs.

## 🧪 Executando os Testes

Os testes assíncronos da aplicação foram desenvolvidos utilizando **pytest** e **HTTPX**.

```cmd
# Executar todos os testes:
pytest

# Executar com saída detalhada e sem os logs de SQL no terminal:
pytest -v --log-level=WARNING

# Gerar o relatório de cobertura de código (Coverage):
pytest --cov=app --cov-report=html
```
O relatório interativo em HTML será gerado na pasta htmlcov/. Para visualizá-lo, abra o arquivo htmlcov/index.html em seu navegador.

---
Desenvolvido por [Antonio Candioto](https://github.com/antoniolpcan) — Entre em contato no [LinkedIn](https://www.linkedin.com/in/antoniolpcan/)

AC 01 - 25/03/2026 ✅

AC 02 - 08/04/2026 ✅

AC 03 - 22/04/2026

AC 04 - 06/02/2026

AP1 - 15/05/2026 ✅

# Documentação da AP1 - Catálogo de Produtos

Esta atividade prática consiste em uma API desenvolvida em Django Rest Framework, com deploy automatizado na AWS Elastic Beanstalk.

## Domínio da API na AWS
[http://catalogo-produtos-env-2.eba-bis2mpaw.us-east-1.elasticbeanstalk.com/]
O login do admin não vai funcionar na nuvem, apenas rodando localmente
Para navegação das páginas temos:
admin: [http://catalogo-produtos-env-2.eba-bis2mpaw.us-east-1.elasticbeanstalk.com/admin/login/?next=/admin/]
api: [http://catalogo-produtos-env-2.eba-bis2mpaw.us-east-1.elasticbeanstalk.com/api/]
api produtos:["http://catalogo-produtos-env-2.eba-bis2mpaw.us-east-1.elasticbeanstalk.com/api/produtos/"]
api categorias: [http://catalogo-produtos-env-2.eba-bis2mpaw.us-east-1.elasticbeanstalk.com/api/categorias/]

## Tecnologias Utilizadas
- Python 3.14.3 / Django 6.0
- Django Rest Framework
- Gunicorn (Servidor de produção)
- SQLite (bando de dados local)
- AWS Elastic Beanstalk (PaaS)

## Como executar localmente
1. Clone o repositório
2. Abre o terminal do projeto na pasta AP1
3. Crie um ambiente virtual: 'python -m venv .venv'
4. Ative o ambiente virtual: '.\.venv\Scripts\activate'
5. Instale as dependências: 'pip install -r requirements.txt'
6. Execute as migrações: 'python manage.py migrate'
7. Inicie o servidor: 'python manage.py runserver'
8. Para acessar painel do admin o login e senha sao os mesmos: 'admin'

Para navegar entre as páginas da api é só colocar no final da url /admin ou /api ou /api/produtos ou /api/categorias

## Detalhes do Deploy na AWS

O Deploy foi realizado utilizando o pacote deploy.zip via console da AWS Elastic Beanstalk.

1. Foi preparado o pacote para deploy em .zip, nao incluindo venv/ ; .venv/ ; db.sqlite3 ; .git/ ; __pycache__/ ; arquivos .env
2. Foi criado o ambiente na plataforma de acordo com orientações do professor

- O arquivo .ebextensions/django.config automatiza as migrações e acoleta de estáticos no ambiente de nuvem
- O arquivo Procfile define o gunicorn como servidor de aplicação, garantindo uma boa perfomance e conformidade com os padrões de produção de qualidade
- Scripts de pós-instalação ajustam as permissões do banco de daods SQLite para permitir a persistência de dados no ambiente linux da AWS

## Preparação para o futuro

Futuramente o plano é migrar o armazenamento de arquivos de mídia para o Amazon s3.
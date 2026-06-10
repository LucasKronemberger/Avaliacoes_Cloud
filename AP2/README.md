# 🏆 Copa do Mundo 2026 — API E-commerce

API REST para um e-commerce temático da Copa do Mundo 2026. Construída com **Django REST Framework**, banco de dados **MySQL no AWS RDS**, mídia no **AWS S3** e deploy no **AWS Elastic Beanstalk**.

---

## Arquitetura: AP1 → AP2

```
AP1                              AP2
─────────────────────            ──────────────────────────────────────
Django REST + SQLite             Django REST + MySQL (RDS)
Produto (imagem local)    →      Produto + Seleção + Pedido + ItemPedido
Deploy no EB                     Imagens/bandeiras no S3
                                 Deploy no EB com RDS + S3 integrados
```

### Diagrama de infraestrutura

```
Internet
   │
   ▼
┌──────────────────────┐
│  Elastic Beanstalk   │  ← app.zip (gunicorn + Django)
│  EC2 Auto Scaling    │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐  ┌──────────┐
│  RDS    │  │   S3     │
│  MySQL  │  │  Bucket  │
│ (dados) │  │ (mídia)  │
└─────────┘  └──────────┘
```

---

## Modelos de dados

| Modelo       | Descrição                                          |
|--------------|----------------------------------------------------|
| `Produto`    | Camisetas, chuteiras, bolas e acessórios da Copa     |
| `Selecao`    | Seleções participantes (código FIFA, grupo, bandeira) |
| `Pedido`     | Carrinho/pedido de um cliente                      |
| `ItemPedido` | Produto + quantidade dentro de um pedido           |

---

## Endpoints da API

| Método | Endpoint                                      | Descrição                         |
|--------|-----------------------------------------------|-----------------------------------|
| GET    | `/api/health/`                                | Health check                      |
| GET    | `/api/produtos/`                              | Lista produtos                    |
| GET    | `/api/produtos/?categoria=camiseta`           | Filtra por categoria              |
| POST   | `/api/produtos/`                              | Cria produto (com imagem)         |
| PUT    | `/api/produtos/{id}/`                         | Atualiza produto                  |
| DELETE | `/api/produtos/{id}/`                         | Remove produto                    |
| GET    | `/api/selecoes/`                              | Lista seleções                    |
| GET    | `/api/selecoes/?grupo=A`                      | Filtra seleções por grupo         |
| POST   | `/api/selecoes/`                              | Cadastra seleção (com bandeira)   |
| GET    | `/api/pedidos/`                               | Lista pedidos                     |
| POST   | `/api/pedidos/`                               | Cria pedido                       |
| GET    | `/api/pedidos/{id}/`                          | Detalhe do pedido com itens       |
| POST   | `/api/pedidos/{id}/adicionar_item/`           | Adiciona produto ao pedido        |
| DELETE | `/api/pedidos/{id}/remover_item/{item_id}/`   | Remove item do pedido             |
| GET    | `/api/pedidos/{id}/itens/`                    | Lista itens + total do pedido     |

### Categorias de produto disponíveis
`camiseta` · `chuteira` · `bola` · `acessorio`

---

## Execução local

### Pré-requisitos
- Python 3.11+
- Git

### Passos

```bash
# 1. Clone o repositório
git clone <URL_DO_SEU_REPO>
cd apiawsEB

# 2. Crie e ative o ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrações (SQLite local)
python manage.py migrate

# 5. Crie o superusuário admin
python manage.py createsuperuser
# Sugestão de username: root

# 6. Inicie o servidor
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/api/`  
O admin em `http://localhost:8000/admin/`

---

## Deploy no AWS Elastic Beanstalk

### Pré-requisitos AWS
- Conta AWS com permissões em EB, RDS, S3 e IAM
- AWS CLI instalado e configurado (`aws configure`)
- EB CLI instalado (`pip install awsebcli`)

---

### Parte 1 — Criar banco MySQL no RDS

1. Acesse **RDS → Create database**
2. Selecione:
   - Engine: **MySQL**
   - Version: 8.x
   - Template: **Free Tier**
   - DB identifier: `copa2026-db`
   - Master username: `admin`
   - Master password: (guarde com segurança)
   - DB name: `copa2026`
3. Em **Connectivity**:
   - VPC: mesma do seu EB environment
   - Public access: **No** (acesso apenas interno)
4. Crie e anote o **endpoint** do banco (ex: `copa2026-db.xxxx.us-east-1.rds.amazonaws.com`)

**Security Group do RDS:**
- Adicione uma Inbound Rule: Tipo `MySQL/Aurora`, Porta `3306`, Source = Security Group do EB

---

### Parte 2 — Criar bucket S3

1. Acesse **S3 → Create bucket**
2. Nome: `copa2026-media` (deve ser único globalmente)
3. Região: `us-east-1` (mesma do EB)
4. Desmarque "Block all public access" (necessário para servir imagens)
5. Adicione esta Bucket Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::copa2026-media/*"
    }
  ]
}
```

6. Em **IAM → Roles**, adicione à role do EC2 do EB a policy **AmazonS3FullAccess** (ou crie uma policy mínima com `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject` no bucket).

---

### Parte 3 — Configurar variáveis no Elastic Beanstalk

No console EB → seu environment → **Configuration → Software → Environment properties**, adicione:

| Variável                  | Valor                                         |
|---------------------------|-----------------------------------------------|
| `DJANGO_SECRET_KEY`       | (gere uma chave segura)                       |
| `DJANGO_DEBUG`            | `False`                                       |
| `RDS_DB_NAME`             | `copa2026`                                    |
| `RDS_USERNAME`            | `admin`                                       |
| `RDS_PASSWORD`            | (senha do RDS)                                |
| `RDS_HOSTNAME`            | (endpoint do RDS)                             |
| `RDS_PORT`                | `3306`                                        |
| `AWS_STORAGE_BUCKET_NAME` | `copa2026-media`                              |
| `AWS_S3_REGION_NAME`      | `us-east-1`                                   |
| `DJANGO_ADMIN_USER`       | `root`                                        |
| `DJANGO_ADMIN_PASSWORD`   | (senha segura para o admin)                   |
| `DJANGO_ADMIN_EMAIL`      | `admin@copa2026.com`                          |

> **Importante:** NUNCA versione senhas ou chaves no código. Todas as informações sensíveis devem estar nas variáveis de ambiente.

---

### Parte 4 — Gerar e fazer deploy do app.zip

```bash
# Na raiz do projeto, excluindo arquivos desnecessários:
zip -r app.zip . \
  -x "*.git*" \
  -x ".venv/*" \
  -x "__pycache__/*" \
  -x "*.pyc" \
  -x "db.sqlite3" \
  -x "media/*" \
  -x "staticfiles/*" \
  -x "*.zip"
```

No console EB → seu environment → **Upload and Deploy** → selecione `app.zip`.

Ou via EB CLI:
```bash
eb deploy
```

---

### Parte 5 — Criar superusuário root

O script de predeploy (`.platform/hooks/predeploy/01_django_setup.sh`) já cria automaticamente o superusuário usando as variáveis `DJANGO_ADMIN_USER`, `DJANGO_ADMIN_PASSWORD` e `DJANGO_ADMIN_EMAIL`.

Se precisar criar manualmente via SSH:
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py createsuperuser
```

Acesse o admin em: `http://<seu-eb-url>/admin/`  
Login: **root** / (senha definida em `DJANGO_ADMIN_PASSWORD`)

---

## Link da API em produção

> 🔗 **http://<SEU-EB-URL>.elasticbeanstalk.com/api/**

---

## Evidências

### RDS MySQL
- Screenshot da instância RDS criada no console AWS
- Screenshot das migrações aplicadas com sucesso nos logs do EB
- Teste de `GET /api/produtos/` retornando dados do RDS

### S3
- Screenshot do bucket com arquivos de imagem de produtos
- URL de imagem retornada pelo endpoint: `https://copa2026-media.s3.amazonaws.com/produtos/...`

---

## Decisões técnicas

- **PyMySQL** como driver MySQL puro Python (sem dependência de `mysqlclient` C-binding, mais simples no EB)
- **django-storages + boto3** para integração S3 transparente via `DEFAULT_FILE_STORAGE`
- Preço unitário congelado no `ItemPedido.save()` para evitar variação de preço após a compra
- `prefetch_related('itens__produto')` no `PedidoViewSet` para evitar N+1 queries
- Superusuário criado automaticamente no hook de predeploy via variáveis de ambiente

---

## Troubleshooting

| Problema | Causa provável | Solução |
|----------|---------------|---------|
| `migrate` falha no EB | Security Group do RDS não libera porta 3306 para o EB | Adicione inbound rule no SG do RDS apontando para o SG do EB |
| Upload de imagem falha | Credenciais AWS não configuradas na role do EC2 | Adicione `AmazonS3FullAccess` à role do EB |
| Imagem retorna 403 | Bucket policy não permite acesso público | Revise a bucket policy e desmarque "Block all public access" |
| `Access Denied` no S3 | `AWS_DEFAULT_ACL = 'public-read'` mas ACLs desabilitadas no bucket | No bucket, ative "ACLs enabled" em Object Ownership |
| Admin não carrega CSS | `collectstatic` não rodou | Verifique os logs do predeploy hook |
| `502 Bad Gateway` | App não iniciou | Veja `/var/log/web.stdout.log` via `eb logs` |

---

## Referências

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Deploy Django no Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [Amazon RDS MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html)
- [django-storages S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)

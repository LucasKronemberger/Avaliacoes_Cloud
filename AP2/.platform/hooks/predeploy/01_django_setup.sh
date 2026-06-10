#!/bin/bash
# Ativa o ambiente virtual do Elastic Beanstalk
source /var/app/venv/*/bin/activate

# Garante que os comandos Django rodam no diretório correto do app
cd /var/app/staging

echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Aplicando migrações do banco ==="
if python manage.py migrate --noinput; then
    echo "=== Migrações aplicadas com sucesso ==="
else
    echo "=== AVISO: migrate falhou — verifique o Security Group do RDS e as variáveis de ambiente ==="
    echo "=== O app será iniciado mesmo assim; corrija o banco e faça redeploy ==="
fi

echo "=== Criando superusuário root (se não existir) ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_ADMIN_USER', 'root')
password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin1234')
email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@copa2026.com')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superusuário {username} criado.')
else:
    print(f'Superusuário {username} já existe.')
"

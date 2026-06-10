from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_produto_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='categoria',
            field=models.CharField(
                choices=[
                    ('camiseta', 'Camiseta Oficial'),
                    ('chuteira', 'Chuteira'),
                    ('bola', 'Bola'),
                    ('acessorio', 'Acessório'),
                ],
                default='camiseta',
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name='Selecao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('codigo_fifa', models.CharField(max_length=3, unique=True)),
                ('grupo', models.CharField(
                    choices=[('A','Grupo A'),('B','Grupo B'),('C','Grupo C'),('D','Grupo D'),
                             ('E','Grupo E'),('F','Grupo F'),('G','Grupo G'),('H','Grupo H')],
                    max_length=1
                )),
                ('bandeira', models.ImageField(blank=True, null=True, upload_to='selecoes/')),
            ],
            options={'ordering': ['grupo', 'nome'], 'verbose_name': 'Seleção', 'verbose_name_plural': 'Seleções'},
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente_nome', models.CharField(max_length=200)),
                ('cliente_email', models.EmailField()),
                ('status', models.CharField(
                    choices=[('aberto','Aberto'),('confirmado','Confirmado'),
                             ('enviado','Enviado'),('entregue','Entregue'),('cancelado','Cancelado')],
                    default='aberto',
                    max_length=20,
                )),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-criado_em'], 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='api.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itens_pedido', to='api.produto')),
            ],
            options={'verbose_name': 'Item do Pedido', 'verbose_name_plural': 'Itens do Pedido'},
        ),
    ]

from django.db import models


# ── Produto (mantido da AP1, com campo imagem para S3) ──────────────────────
class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ('camiseta', 'Camiseta Oficial'),
        ('chuteira', 'Chuteira'),
        ('bola', 'Bola'),
        ('acessorio', 'Acessório'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, default='')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    categoria = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default='camiseta'
    )
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


# ── Seleção (nova entidade AP2) ─────────────────────────────────────────────
class Selecao(models.Model):
    GRUPO_CHOICES = [(g, f'Grupo {g}') for g in 'ABCDEFGH']

    nome = models.CharField(max_length=100)
    codigo_fifa = models.CharField(max_length=3, unique=True)  # ex: BRA, ARG
    grupo = models.CharField(max_length=1, choices=GRUPO_CHOICES)
    bandeira = models.ImageField(upload_to='selecoes/', blank=True, null=True)

    class Meta:
        ordering = ['grupo', 'nome']
        verbose_name = 'Seleção'
        verbose_name_plural = 'Seleções'

    def __str__(self):
        return f'{self.codigo_fifa} — {self.nome}'


# ── Pedido (carrinho de compras) ────────────────────────────────────────────
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente_nome = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido #{self.pk} — {self.cliente_nome} ({self.status})'

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())


# ── ItemPedido ───────────────────────────────────────────────────────────────
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_pedido')
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def save(self, *args, **kwargs):
        # Congela o preço no momento da compra
        if not self.preco_unitario:
            self.preco_unitario = self.produto.preco
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido #{self.pedido.pk})'

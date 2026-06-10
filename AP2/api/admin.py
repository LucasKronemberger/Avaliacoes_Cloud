from django.contrib import admin
from .models import Produto, Selecao, Pedido, ItemPedido


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'criado_em')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')


@admin.register(Selecao)
class SelecaoAdmin(admin.ModelAdmin):
    list_display = ('codigo_fifa', 'nome', 'grupo')
    list_filter = ('grupo',)
    search_fields = ('nome', 'codigo_fifa')


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('preco_unitario', 'subtotal')

    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cliente_nome', 'cliente_email', 'status', 'criado_em')
    list_filter = ('status',)
    search_fields = ('cliente_nome', 'cliente_email')
    inlines = [ItemPedidoInline]

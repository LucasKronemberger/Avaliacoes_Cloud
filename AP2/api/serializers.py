from rest_framework import serializers
from .models import Produto, Selecao, Pedido, ItemPedido


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        read_only_fields = ('criado_em', 'atualizado_em')


class SelecaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selecao
        fields = '__all__'


class ItemPedidoSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']
        read_only_fields = ('preco_unitario',)


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ('criado_em', 'atualizado_em')


class AdicionarItemSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1, default=1)

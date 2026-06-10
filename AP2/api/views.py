from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import Produto, Selecao, Pedido, ItemPedido
from .serializers import (
    ProdutoSerializer, SelecaoSerializer,
    PedidoSerializer, ItemPedidoSerializer, AdicionarItemSerializer
)


@api_view(['GET'])
def health_check(request):
    """Endpoint de saúde — usado pelo EB para verificar se a app está no ar."""
    return Response({'status': 'ok', 'mensagem': 'API Copa do Mundo 2026 funcionando!'})


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Produtos (camisetas, chuteiras e bolas Copa 2026).

    - GET    /api/produtos/           → lista todos
    - POST   /api/produtos/           → cria novo (suporta upload de imagem)
    - GET    /api/produtos/{id}/      → detalhe
    - PUT    /api/produtos/{id}/      → atualiza
    - PATCH  /api/produtos/{id}/      → atualiza parcial
    - DELETE /api/produtos/{id}/      → remove
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.request.query_params.get('categoria')
        if categoria:
            qs = qs.filter(categoria=categoria)
        return qs


class SelecaoViewSet(viewsets.ModelViewSet):
    """
    CRUD de Seleções participantes da Copa do Mundo 2026.

    - GET    /api/selecoes/            → lista todas
    - GET    /api/selecoes/?grupo=A    → filtra por grupo
    - POST   /api/selecoes/            → cadastra seleção (com bandeira)
    """
    queryset = Selecao.objects.all()
    serializer_class = SelecaoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        grupo = self.request.query_params.get('grupo')
        if grupo:
            qs = qs.filter(grupo=grupo.upper())
        return qs


class PedidoViewSet(viewsets.ModelViewSet):
    """
    Carrinho de compras / Pedidos.

    Endpoints extras:
    - POST /api/pedidos/{id}/adicionar_item/   → adiciona produto ao pedido
    - DELETE /api/pedidos/{id}/remover_item/{item_id}/  → remove item
    - GET  /api/pedidos/{id}/itens/            → lista itens do pedido
    """
    queryset = Pedido.objects.prefetch_related('itens__produto').all()
    serializer_class = PedidoSerializer

    @action(detail=True, methods=['post'], url_path='adicionar_item')
    def adicionar_item(self, request, pk=None):
        pedido = self.get_object()

        if pedido.status != 'aberto':
            return Response(
                {'erro': f'Pedido com status "{pedido.status}" não pode ser alterado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AdicionarItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        produto_id = serializer.validated_data['produto_id']
        quantidade = serializer.validated_data['quantidade']

        try:
            produto = Produto.objects.get(pk=produto_id)
        except Produto.DoesNotExist:
            return Response({'erro': 'Produto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if produto.estoque < quantidade:
            return Response(
                {'erro': f'Estoque insuficiente. Disponível: {produto.estoque}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item, criado = ItemPedido.objects.get_or_create(
            pedido=pedido,
            produto=produto,
            defaults={'quantidade': quantidade, 'preco_unitario': produto.preco}
        )
        if not criado:
            item.quantidade += quantidade
            item.save()

        return Response(ItemPedidoSerializer(item).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path=r'remover_item/(?P<item_id>[^/.]+)')
    def remover_item(self, request, pk=None, item_id=None):
        pedido = self.get_object()
        try:
            item = pedido.itens.get(pk=item_id)
        except ItemPedido.DoesNotExist:
            return Response({'erro': 'Item não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def itens(self, request, pk=None):
        pedido = self.get_object()
        serializer = ItemPedidoSerializer(pedido.itens.all(), many=True)
        return Response({'pedido_id': pedido.pk, 'total': pedido.total, 'itens': serializer.data})

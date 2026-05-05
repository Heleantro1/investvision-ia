from django.urls import path
from .views import (
    listar_carteira,
    adicionar_posicao,
    editar_posicao,
    excluir_posicao,
)


urlpatterns = [
    path('', listar_carteira, name='listar_carteira'),
    path('adicionar/', adicionar_posicao, name='adicionar_posicao'),
    path('editar/<int:pk>/', editar_posicao, name='editar_posicao'),
    path('excluir/<int:pk>/', excluir_posicao, name='excluir_posicao'),
]
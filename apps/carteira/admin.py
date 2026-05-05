from django.contrib import admin
from .models import PosicaoCarteira


@admin.register(PosicaoCarteira)
class PosicaoCarteiraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ativo', 'quantidade', 'preco_medio', 'valor_investido')
    search_fields = ('usuario__username', 'ativo__codigo')
    list_filter = ('ativo__tipo',)
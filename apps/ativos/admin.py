from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Ativo


@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo', 'botao_excluir')
    search_fields = ('codigo', 'nome')
    list_filter = ('tipo',)

    def botao_excluir(self, obj):
        url = reverse('admin:ativos_ativo_delete', args=[obj.id])
        return format_html(
            '<a class="button" style="background:#ef4444; color:white; padding:6px 10px; border-radius:6px;" href="{}">Excluir</a>',
            url
        )

    botao_excluir.short_description = 'Ação'
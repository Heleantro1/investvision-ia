from django.db import models
from django.contrib.auth.models import User
from apps.ativos.models import Ativo


class PosicaoCarteira(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posicoes')
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE, related_name='posicoes')

    quantidade = models.DecimalField(max_digits=12, decimal_places=2)
    preco_medio = models.DecimalField(max_digits=12, decimal_places=2)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Posição da Carteira'
        verbose_name_plural = 'Posições da Carteira'
        unique_together = ('usuario', 'ativo')

    def valor_investido(self):
        return self.quantidade * self.preco_medio

    def __str__(self):
        return f'{self.usuario.username} - {self.ativo.codigo}'
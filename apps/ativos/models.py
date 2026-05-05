from django.db import models


class Ativo(models.Model):
    TIPO_ATIVO_CHOICES = [
        ('acao', 'Ação'),
        ('fii', 'FII'),
        ('cripto', 'Criptomoeda'),
        ('etf', 'ETF'),
    ]

    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_ATIVO_CHOICES)
    ativo_externo = models.BooleanField(default=True)  # ex: vem do yfinance

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
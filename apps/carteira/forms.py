from django import forms
from .models import PosicaoCarteira


class PosicaoCarteiraForm(forms.ModelForm):
    class Meta:
        model = PosicaoCarteira
        fields = ['ativo', 'quantidade', 'preco_medio']

        widgets = {
            'ativo': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_medio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
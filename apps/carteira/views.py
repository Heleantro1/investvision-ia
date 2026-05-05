from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PosicaoCarteira
from .forms import PosicaoCarteiraForm


@login_required
def listar_carteira(request):
    posicoes = PosicaoCarteira.objects.filter(usuario=request.user)

    return render(request, 'carteira/listar.html', {
        'posicoes': posicoes
    })


@login_required
def adicionar_posicao(request):
    if request.method == 'POST':
        form = PosicaoCarteiraForm(request.POST)

        if form.is_valid():
            posicao = form.save(commit=False)
            posicao.usuario = request.user
            posicao.save()
            return redirect('listar_carteira')
    else:
        form = PosicaoCarteiraForm()

    return render(request, 'carteira/form.html', {
        'form': form,
        'titulo': 'Adicionar ativo à carteira'
    })


@login_required
def editar_posicao(request, pk):
    posicao = get_object_or_404(PosicaoCarteira, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = PosicaoCarteiraForm(request.POST, instance=posicao)

        if form.is_valid():
            form.save()
            return redirect('listar_carteira')
    else:
        form = PosicaoCarteiraForm(instance=posicao)

    return render(request, 'carteira/form.html', {
        'form': form,
        'titulo': 'Editar posição'
    })


@login_required
def excluir_posicao(request, pk):
    posicao = get_object_or_404(PosicaoCarteira, pk=pk, usuario=request.user)

    if request.method == 'POST':
        posicao.delete()
        return redirect('listar_carteira')

    return render(request, 'carteira/confirmar_exclusao.html', {
        'posicao': posicao
    })
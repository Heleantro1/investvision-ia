import json, markdown
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import analisar_carteira, gerar_historico_carteira, gerar_alertas
from apps.ia.services import gerar_analise_ia


@login_required
def dashboard(request):
    dados = analisar_carteira(request.user)
    alertas = gerar_alertas(dados)

    # 👇 AQUI ESTAVA FALTANDO
    datas, valores = gerar_historico_carteira(request.user)

    try:
        texto_ia = gerar_analise_ia(request.user)
        analise_ia = markdown.markdown(texto_ia)
    except:
        analise_ia = "Erro ao gerar análise com IA."

    labels_grafico = [ativo["codigo"] for ativo in dados["ativos"]]
    valores_grafico = [round(ativo["valor_atual"], 2) for ativo in dados["ativos"]]

    return render(request, "dashboard.html", {
        "dados": dados,
        "analise_ia": analise_ia,
        "labels_grafico": json.dumps(labels_grafico),
        "valores_grafico": json.dumps(valores_grafico),
        "alertas": alertas,

        # 👇 ESSAS DUAS LINHAS PRECISAM DA VARIÁVEL
        "datas_grafico": json.dumps(datas),
        "valores_grafico_linha": json.dumps(valores),
    })
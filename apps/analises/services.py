import yfinance as yf
from apps.carteira.models import PosicaoCarteira
from django.core.cache import cache


def formatar_codigo_yfinance(codigo):
    codigo = codigo.upper()

    if codigo.endswith("-USD"):
        return codigo

    if "." not in codigo:
        return f"{codigo}.SA"

    return codigo


def buscar_preco_atual(codigo):
    cache_key = f"preco_atual_{codigo}"

    preco_cache = cache.get(cache_key)
    if preco_cache is not None:
        return preco_cache

    ticker = formatar_codigo_yfinance(codigo)
    dados = yf.Ticker(ticker)

    preco = dados.history(period="1d")["Close"]

    if preco.empty:
        return None

    preco_atual = float(preco.iloc[-1])

    cache.set(cache_key, preco_atual, timeout=300)  # 5 minutos

    return preco_atual

def calcular_score_investidor(dados):
    score = 0

    rentabilidade = dados.get("rentabilidade_total", 0)
    quantidade_ativos = dados.get("quantidade_ativos", 0)
    ativos = dados.get("ativos", [])

    if rentabilidade > 15:
        score += 35
    elif rentabilidade > 5:
        score += 25
    elif rentabilidade >= 0:
        score += 15
    else:
        score += 5

    if quantidade_ativos >= 5:
        score += 30
    elif quantidade_ativos >= 3:
        score += 20
    elif quantidade_ativos >= 2:
        score += 10
    else:
        score += 5

    if ativos:
        maior_posicao = max(a["valor_atual"] for a in ativos)
        total = dados.get("valor_atual_total", 0)

        concentracao = (maior_posicao / total) * 100 if total > 0 else 100

        if concentracao <= 30:
            score += 25
        elif concentracao <= 50:
            score += 15
        else:
            score += 5
    else:
        concentracao = 0

    if score >= 80:
        perfil = "Investidor equilibrado"
    elif score >= 60:
        perfil = "Investidor em evolução"
    elif score >= 40:
        perfil = "Investidor concentrado"
    else:
        perfil = "Investidor iniciante"

    return {
        "score": min(score, 100),
        "perfil": perfil,
        "concentracao_maior_ativo": concentracao,
    }


def analisar_carteira(usuario):
    posicoes = PosicaoCarteira.objects.filter(usuario=usuario)

    total_investido = 0
    valor_atual_total = 0
    ativos = []

    for posicao in posicoes:
        valor_investido = float(posicao.valor_investido())
        preco_atual = buscar_preco_atual(posicao.ativo.codigo)

        if preco_atual is None:
            valor_atual = 0
            lucro_prejuizo = 0
            rentabilidade = 0
        else:
            valor_atual = float(posicao.quantidade) * preco_atual
            lucro_prejuizo = valor_atual - valor_investido
            rentabilidade = (lucro_prejuizo / valor_investido) * 100

        total_investido += valor_investido
        valor_atual_total += valor_atual

        ativos.append({
            "codigo": posicao.ativo.codigo,
            "nome": posicao.ativo.nome,
            "quantidade": float(posicao.quantidade),
            "preco_medio": float(posicao.preco_medio),
            "preco_atual": preco_atual,
            "valor_investido": valor_investido,
            "valor_atual": valor_atual,
            "lucro_prejuizo": lucro_prejuizo,
            "rentabilidade": rentabilidade,
        })

    lucro_prejuizo_total = valor_atual_total - total_investido

    rentabilidade_total = (
        (lucro_prejuizo_total / total_investido) * 100
        if total_investido > 0 else 0
    )

    dados = {
        "usuario": usuario.username,
        "quantidade_ativos": posicoes.count(),
        "total_investido": total_investido,
        "valor_atual_total": valor_atual_total,
        "lucro_prejuizo_total": lucro_prejuizo_total,
        "rentabilidade_total": rentabilidade_total,
        "ativos": ativos,
    }

    dados["score_investidor"] = calcular_score_investidor(dados)

    return dados

def gerar_historico_carteira(usuario):
    cache_key = f"historico_carteira_{usuario.id}"

    historico_cache = cache.get(cache_key)
    if historico_cache is not None:
        return historico_cache

    posicoes = PosicaoCarteira.objects.filter(usuario=usuario)

    historico_total = None

    for posicao in posicoes:
        codigo = formatar_codigo_yfinance(posicao.ativo.codigo)

        dados = yf.download(codigo, period="1mo", progress=False)

        if dados.empty:
            continue

        fechamento = dados["Close"]

        if hasattr(fechamento, "columns"):
            fechamento = fechamento.iloc[:, 0]

        valores_posicao = fechamento * float(posicao.quantidade)

        if historico_total is None:
            historico_total = valores_posicao
        else:
            historico_total = historico_total.add(valores_posicao, fill_value=0)

    if historico_total is None:
        return [], []

    historico_total = historico_total.dropna()

    datas = historico_total.index.strftime("%d/%m").tolist()
    valores = historico_total.round(2).values.tolist()

    resultado = (datas, valores)

    cache.set(cache_key, resultado, timeout=900)  # 15 minutos

    return resultado

def gerar_alertas(dados):
    alertas = []

    ativos = dados.get("ativos", [])
    total = dados.get("valor_atual_total", 0)
    rentabilidade = dados.get("rentabilidade_total", 0)


    if ativos and total > 0:
        maior = max(ativos, key=lambda x: x["valor_atual"])
        percentual = (maior["valor_atual"] / total) * 100

        if percentual > 50:
            alertas.append(f"Alta concentração em {maior['codigo']} ({percentual:.1f}%)")

 
    if len(ativos) <= 2:
        alertas.append("Carteira com baixa diversificação")

    
    if rentabilidade < 0:
        alertas.append("Carteira com rentabilidade negativa")

   
    if len(ativos) == 1:
        alertas.append("Apenas 1 ativo na carteira (alto risco)")

    return alertas
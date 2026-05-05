import os
from django.core.cache import cache
from openai import OpenAI
from dotenv import load_dotenv
from apps.analises.services import analisar_carteira

load_dotenv(override=True)


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def gerar_fallback(dados):
    return f"""
Visão geral:
Sua carteira possui {dados['quantidade_ativos']} ativo(s), com rentabilidade total de {dados['rentabilidade_total']:.2f}%.

Pontos fortes:
- Você já possui uma carteira cadastrada e monitorada.
- O sistema acompanha valor atual, rentabilidade e concentração.

Riscos:
- Pode haver concentração elevada em poucos ativos.
- A carteira pode precisar de maior diversificação.

Recomendações:
- Avalie diversificar entre diferentes setores e classes de ativos.
- Acompanhe periodicamente a rentabilidade e os alertas.

Conclusão:
Análise gerada em modo automático porque a IA não respondeu no momento.
"""


def gerar_analise_ia(usuario):
    dados = analisar_carteira(usuario)

    cache_key = f"analise_ia_usuario_{usuario.id}"
    analise_cache = cache.get(cache_key)

    if analise_cache:
        return analise_cache

    uso_key = f"uso_ia_usuario_{usuario.id}"
    uso_atual = cache.get(uso_key, 0)

    LIMITE_DIARIO = 5

    if uso_atual >= LIMITE_DIARIO:
        return "Limite diário de análises atingido. Tente novamente amanhã."

    client = get_client()

    if not client:
        return gerar_fallback(dados)

    prompt = f"""
Você é um analista financeiro profissional.

Analise a carteira do usuário de forma clara, elegante e fácil de ler.

DADOS:
- Usuário: {dados['usuario']}
- Total investido: R$ {dados['total_investido']:.2f}
- Valor atual: R$ {dados['valor_atual_total']:.2f}
- Rentabilidade total: {dados['rentabilidade_total']:.2f}%
- Quantidade de ativos: {dados['quantidade_ativos']}

ATIVOS:
{[ativo['codigo'] for ativo in dados['ativos']]}

REGRAS:
- Não mostrar quantidade, preço médio, preço atual ou valores por ativo.
- Não usar markdown.
- Usar frases curtas.
- Separar blocos com linhas em branco.

FORMATO:

Visão geral:

Pontos fortes:

Riscos:

Recomendações:

Conclusão:
"""

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        texto = resposta.choices[0].message.content

        cache.set(cache_key, texto, timeout=1800)  # 30 min
        cache.set(uso_key, uso_atual + 1, timeout=86400)  # 24h

        print(f"[IA LOG] Usuário {usuario.username} gerou análise IA. Uso diário: {uso_atual + 1}")

        return texto

    except Exception as e:
        print(f"[IA ERRO] Usuário {usuario.username}: {str(e)}")
        return gerar_fallback(dados)
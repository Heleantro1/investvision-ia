from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import gerar_analise_ia


@login_required
def analise_ia(request):
    try:
        resultado = gerar_analise_ia(request.user)

        return JsonResponse({
            "analise": resultado
        })

    except Exception as e:
        return JsonResponse({
            "analise": f"Erro real da IA: {str(e)}"
        }, status=500)
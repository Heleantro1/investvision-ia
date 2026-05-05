from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect('/analises/dashboard/')


urlpatterns = [
    path('', home),  # 👈 ADICIONE ISSO
    path('admin/', admin.site.urls),
    path('analises/', include('apps.analises.urls')),
    path('carteira/', include('apps.carteira.urls')),
    path('ia/', include('apps.ia.urls')),
    path('accounts/', include('apps.usuarios.urls')),
]
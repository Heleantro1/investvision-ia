from django.urls import path
from .views import analise_ia

urlpatterns = [
    path('analise/', analise_ia, name='analise_ia'),
]
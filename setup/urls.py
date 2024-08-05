from django.contrib import admin
from django.urls import path, include

from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('previsao_trens.urls')),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    
    path('accounts/', include('django.contrib.auth.urls')),
]

#configure o urls.py do projeto para servir arquivos de mídia carregados pelo usuário durante o desenvolvimento (quando debug=True).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

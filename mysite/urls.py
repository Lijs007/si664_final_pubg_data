from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import path, include

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('pubg_data/')),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
    path('pubg_data/', include('pubg_data.urls')),
    path('pubg_data/api/rest-auth/', include('rest_auth.urls')),
    path('pubg_data/api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls')),
	path('pubg_data/api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
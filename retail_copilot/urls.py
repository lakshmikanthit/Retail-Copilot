"""
URL configuration for retail_copilot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventory import views, auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication URLs
    path('login/', auth_views.user_login, name='login'),
    path('register/', auth_views.user_register, name='register'),
    path('logout/', auth_views.user_logout, name='logout'),
    path('profile/', auth_views.user_profile, name='profile'),
    # Main app URLs
    path('', views.dashboard, name='dashboard'),
    path('api/copilot/', views.copilot_chat, name='copilot_chat'),
    path('alerts/', views.inventory_alerts, name='inventory_alerts'),
    path('api/generate-alerts/', views.generate_alerts, name='generate_alerts'),
    path('product/<int:product_id>/', views.product_analysis, name='product_analysis'),
    path('api/stores/', views.get_store_data, name='get_store_data'),
    path('api/products/', views.get_product_data, name='get_product_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

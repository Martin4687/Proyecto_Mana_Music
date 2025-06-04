from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('', views.ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('stats/', views.cliente_stats, name='cliente-stats'),
    path('roles/', views.roles_list, name='roles-list'),
    path('search/', views.search_clientes, name='search-clientes'),
]
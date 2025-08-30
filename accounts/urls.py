from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('apply_concession/', views.apply_concession, name='apply_concession'),

    path('epass/<int:id>/', views.epass_view, name='epass'),
    path('dashboard/showPass/', views.getActivePass, name='show_pass'),
]

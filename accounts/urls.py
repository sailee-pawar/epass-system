from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('apply_concession/', views.apply_concession, name='apply_concession'),
    path('dashboard/concession_form/', views.concession_form, name='concession_form'),

    path('epass/<int:id>/', views.epass_view, name='epass'),
    path('dashboard/showPass/', views.getActivePass, name='show_pass'),

    ### college admin ##
    path("approve-concession/<int:pk>/", views.approve_concession, name="approve_concession"),
    path("reject-concession/<int:pk>/", views.reject_concession, name="reject_concession"),
]

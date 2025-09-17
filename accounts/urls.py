from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view,{"active": "home"}, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('apply_concession/', views.apply_concession, name='apply_concession'),
    path('dashboard/concession_form/', views.concession_form, name='concession_form'),

    path('epass/<int:id>/', views.epass_view, name='epass'),
    path('dashboard/showPass/', views.getActivePass, name='show_pass'),

    ### college admin ##
    path("approve-concession/<int:pk>/", views.approve_concession, name="approve_concession"),
    path("reject-concession/<int:pk>/", views.reject_concession, name="reject_concession"),
    path('concession/<int:id>/verify/', views.verify_concession, name='verify_concession'),
    path("save_profile/", views.save_profile, name="save_profile"),

    ### Transporter Views ###
    path("generate_pass/<int:id>/", views.generate_pass, name="generate_pass"),
    path("passes-chart/", views.passes_chart_view, name="passes_chart"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

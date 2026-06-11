from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_waste, name='submit_waste'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('centers/', views.centers_view, name='centers'),
    path('reports/', views.reports_view, name='reports'),
    path('track/', views.track_view, name='track'),

    # API endpoints
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/centers/', views.api_centers, name='api_centers'),
    path('api/submit/', views.api_submit, name='api_submit'),
    path('api/mining/', views.api_mining, name='api_mining'),
    path('analytics/', views.analytics_view, name='analytics_page'),
]

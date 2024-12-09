from django.urls import path
from . import views


urlpatterns = [
    path('', views.configure_problem, name='configure_problem'),
    path('input/', views.input_data, name='input_data'),
    path('results/', views.results, name='results'),
]

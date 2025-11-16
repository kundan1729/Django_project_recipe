from django.urls import path
from .views import HomeView, RecipeDetailView, DashboardView, RegisterView, LoginView, logout_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recipe/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

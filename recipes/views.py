import time
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, SearchHistory
from .services.groq_ai import generate_recipe
from .services.youtube import search_videos


class HomeView(TemplateView):
    template_name = 'recipes/home.html'

    def post(self, request, *args, **kwargs):
        ingredients = request.POST.get('ingredients', '')
        sh = None
        if request.user.is_authenticated:
            sh = SearchHistory.objects.create(user=request.user, ingredients_raw=ingredients)
        start = time.time()
        recipe_json = generate_recipe(ingredients)
        elapsed = time.time() - start
        if sh:
            sh.response_time = elapsed
            sh.save()
        saved = None
        if request.user.is_authenticated:
            saved = Recipe.objects.create(
                user=request.user,
                title=recipe_json.get('title','AI Recipe'),
                description=recipe_json.get('description',''),
                ingredients=recipe_json.get('ingredients',[]),
                steps=recipe_json.get('steps',[]),
                time=recipe_json.get('time',''),
                difficulty=recipe_json.get('difficulty','easy')
            )
        videos = search_videos(recipe_json.get('title','recipe'))
        return render(request, 'recipes/recipe_detail.html', {'recipe': recipe_json, 'saved': saved, 'videos': videos})


class RecipeDetailView(TemplateView):
    template_name = 'recipes/recipe_detail.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['total_recipes'] = user.recipes.count()
        ctx['saved_recipes'] = user.saved_recipes.count()
        ctx['recent_searches'] = user.search_history.order_by('-created_at')[:5]
        ctx['analytics'] = {
            'labels': ['Easy','Medium','Hard'],
            'data': [
                user.recipes.filter(difficulty='easy').count(),
                user.recipes.filter(difficulty='medium').count(),
                user.recipes.filter(difficulty='hard').count(),
            ]
        }
        return ctx


class RegisterView(FormView):
    template_name = 'recipes/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'recipes/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        # Pass request to AuthenticationForm which expects it for validation
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        # Support ?next=... to redirect after login
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url or str(self.success_url)

    def form_valid(self, form):
        # AuthenticationForm already cleaned and provides get_user()
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('home')

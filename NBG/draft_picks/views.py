from django.shortcuts import render, redirect
from .models import Team, Player, Draft
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import DraftForm, UserForm
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginView):
    template_name = 'home.html'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def team_index(request):
    teams = Team.objects.filter(user=request.user)
    return render(request, 'teams/index.html', {'teams': teams})

@login_required
def team_detail(request, team_id):
    try:
        team = Team.objects.get(user=request.user, id=team_id)
    except Team.DoesNotExist:
        return redirect('team_index')
    players_team_doesnt_have = Player.objects.filter(user=request.user).exclude(id__in=team.players.all().values_list('id'))
    draft_form = DraftForm()
    return render(request, 'teams/details.html', {
        'team': team,
        'draft_form': draft_form,
        'players': players_team_doesnt_have
    })


class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['name', 'city', 'mascot']
    template_name = 'main/team_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    fields = ['city']
    template_name = 'main/team_form.html'

class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = '/teams/'
    template_name = 'main/team_delete.html'

def add_draft(request, team_id):
    form = DraftForm(request.POST)
    if form.is_valid():
        new_draft = form.save(commit=False)
        new_draft.team_id = team_id
        new_draft.save()
        
    return redirect('team_detail', team_id=team_id)

class PlayerCreate(LoginRequiredMixin, CreateView):
    model = Player
    fields = ['position']
    template_name = 'main/player_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlayerList(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'main/player_list.html'
    
    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class PlayerDetail(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'main/player_detail.html'
    
    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class PlayerUpdate(LoginRequiredMixin, UpdateView):
    model = Player
    fields = ['name', 'position', 'age']
    template_name = 'main/player_form.html'
    
    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class PlayerDelete(LoginRequiredMixin, DeleteView):
    model = Player
    success_url = '/players/'
    template_name = 'main/player_delete.html'
    
    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class DraftDelete(LoginRequiredMixin, DeleteView):
    model = Draft
    template_name = 'main/draft_delete.html'

    def get_success_url(self):
        return reverse('team_detail', kwargs={'team_id': self.object.team.id})
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('team_index')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

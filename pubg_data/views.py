from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Player, Match, PlayerInTeam, PlayerParticipate

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PlayerForm
from django.urls import reverse_lazy

from django_filters.views import FilterView
from .filters import PlayerFilter


def index(request):
	return HttpResponse("Hello, world. You're at the PUBG data index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'pubg_data/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'pubg_data/home.html'


class PlayerListView(generic.ListView):
	model = Player
	context_object_name = 'players'
	template_name = 'pubg_data/player.html'
	paginate_by = 200

	def get_queryset(self):
		return Player.objects.all().order_by('player_name')

class PlayerDetailView(generic.DetailView):
	model = Player
	context_object_name = 'player'
	template_name = 'pubg_data/player_detail.html'

@method_decorator(login_required, name='dispatch')
class MatchListView(generic.ListView):
	model = Match
	context_object_name = 'matches'
	template_name = 'pubg_data/match.html'
	paginate_by = 10

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Match.objects\
		.select_related('map')\
		.order_by('match_id_in_game')
		
@method_decorator(login_required, name='dispatch')
class MatchDetailView(generic.DetailView):
	model = Match
	context_object_name = 'match'
	template_name = 'pubg_data/match_detail.html'
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)		


@method_decorator(login_required, name='dispatch')
class PlayerCreateView(generic.View):
	model = Player
	form_class = PlayerForm
	success_message = "Player created successfully"
	template_name = 'pubg_data/player_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = PlayerForm(request.POST)
		if form.is_valid():
			player = form.save(commit=False)
			player.save()
			for match in form.cleaned_data['match']:
				PlayerParticipate.objects.create(player=player, match=match)
			for team in form.cleaned_data['team']:
				PlayerInTeam.objects.create(player=player, team=team)
			return redirect(player) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'pubg_data/player_new.html', {'form': form})

	def get(self, request):
		form = PlayerForm()
		return render(request, 'pubg_data/player_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class PlayerUpdateView(generic.UpdateView):
	model = Player
	form_class = PlayerForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'player'
	# pk_url_kwarg = 'site_pk'
	success_message = "Player updated successfully"
	template_name = 'pubg_data/player_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		player = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		player.save()

		# Current country_area_id values linked to site
		old_ids = PlayerParticipate.objects\
			.values_list('match_id', flat=True)\
			.filter(player_id=player.player_id)

		# New countries list
		new_matches = form.cleaned_data['match']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for match in new_matches:
			new_id = match.match_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				PlayerParticipate.objects \
					.create(player=player, match=match)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				PlayerParticipate.objects \
					.filter(player_id=player.player_id, match_id=old_id) \
					.delete()

		# Current country_area_id values linked to site
		old_ids = PlayerInTeam.objects\
			.values_list('team_id', flat=True)\
			.filter(player_id=player.player_id)

		# New countries list
		new_teams = form.cleaned_data['team']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for team in new_teams:
			new_id = team.team_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				PlayerInTeam.objects \
					.create(player=player, team = team)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				PlayerInTeam.objects \
					.filter(player_id=player.player_id, team_id=old_id) \
					.delete()

		return HttpResponseRedirect(player.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class PlayerDeleteView(generic.DeleteView):
	model = Player
	success_message = "Player deleted successfully"
	success_url = reverse_lazy('player')
	context_object_name = 'player'
	template_name = 'pubg_data/player_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		PlayerParticipate.objects \
			.filter(player_id=self.object.player_id) \
			.delete()

		PlayerInTeam.objects \
			.filter(player_id=self.object.player_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


class PlayerFilterView(FilterView):
	filterset_class = PlayerFilter
	template_name = 'pubg_data/site_filter.html'

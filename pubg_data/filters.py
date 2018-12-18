import django_filters
from pubg_data.models import Player, Match


class PlayerFilter(django_filters.FilterSet):
	player_name = django_filters.CharFilter(
		field_name='player_name',
		label='Player Name',
		lookup_expr='icontains'
	)

	player_kills = django_filters.RangeFilter(
		field_name='player_kills',
		label='Player Kills',
	)

	player_survive_time = django_filters.RangeFilter(
		field_name='player_survive_time',
		label='Player Survive Time(s)',
	)

	match = django_filters.ModelChoiceFilter(
		field_name='match',
		label='Match Attended',
		queryset=Match.objects.all(),
		lookup_expr='exact'
	)



	class Meta:
		model = Player
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []
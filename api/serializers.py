from pubg_data.models import Death, Map, Match, Player, PlayerInTeam, PlayerParticipate, Team, Weapon
from rest_framework import response, serializers, status


class MapSerializer(serializers.ModelSerializer):

	class Meta:
		model = Map
		fields = ('map_id', 'map_name')


class WeaponSerializer(serializers.ModelSerializer):

	class Meta:
		model = Weapon
		fields = ('weapon_id', 'weapon_name')

class PlayerInTeamSerializer(serializers.ModelSerializer):
	player_id = serializers.ReadOnlyField(source='player.player_id')
	team_id = serializers.ReadOnlyField(source='team.team_id')

	class Meta:
		model = PlayerInTeam
		fields = ('player_id', 'team_id')

class PlayerParticipateSerializer(serializers.ModelSerializer):
	player_id = serializers.ReadOnlyField(source='player.player_id')
	match_id = serializers.ReadOnlyField(source='match.match_id')

	class Meta:
		model = PlayerParticipate
		fields = ('player_id', 'match_id')

class MatchSerializer(serializers.ModelSerializer):
	map = MapSerializer(many=False, read_only=True)

	class Meta:
		model = Match
		fields = ('match_id', 'match_id_in_game', 'date', 'game_size', 'match_mode', 'party_size', 'map')

class TeamSerializer(serializers.ModelSerializer):
	match = MatchSerializer(many=False, read_only=True)

	class Meta:
		model = Team
		fields = ('team_id', 'match', 'team_id_in_match', 'team_placement')




class PlayerSerializer(serializers.ModelSerializer):
	player_name = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	player_kills = serializers.IntegerField(
		allow_null=True
	)
	player_dbno = serializers.IntegerField(
		allow_null=True
	)
	player_assists = serializers.IntegerField(
		allow_null=True
	)
	player_dmg = serializers.IntegerField(
		allow_null=True
	)
	player_dist_ride = serializers.IntegerField(
		allow_null=True
	)
	player_dist_walk = serializers.IntegerField(
		allow_null=True
	)
	player_survive_time = serializers.IntegerField(
		allow_null=True
	)
	# player_in_team = PlayerInTeamSerializer(
	# 	source='player_in_team_set', # Note use of _set
	# 	many=True,
	# 	read_only=True
	# )
	# player_in_team_ids = serializers.PrimaryKeyRelatedField(
	# 	many=True,
	# 	write_only=True,
	# 	queryset=Team.objects.all(),
	# 	source='player_in_team'
	# )
	player_participate = PlayerParticipateSerializer(
		source='player_participate_set', # Note use of _set
		many=True,
		read_only=True
	)
	player_participate_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Match.objects.all(),
		source='player_participate'
	)

	class Meta:
		model = Player
		fields = (
			'player_id',
			'player_name',
			'player_kills',
			'player_dbno',
			'player_assists',
			'player_dmg',
			'player_dist_ride',
			'player_dist_walk',
			'player_survive_time',
			# 'player_in_team',
			# 'player_in_team_ids',
			'player_participate',
			'player_participate_ids'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		matches = validated_data.pop('player_participate')
		player = Player.objects.create(**validated_data)

		if matches is not None:
			for match in matches:
				PlayerParticipate.objects.create(
					player_id=player.player_id,
					match_id=match.match_id
				)

		# teams = validated_data.pop('player_in_team')

		# if teams is not None:
		# 	for team in teams:
		# 		PlayerInTeam.objects.create(
		# 			player_id=player.player_id,
		# 			team_id=team.team_id
		# 		)

		return player

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		player_id = instance.player_id
		new_matches = validated_data.pop('player_participate')
		#new_teams = validated_data.pop('player_in_team')

		instance.player_name = validated_data.get(
			'player_name',
			instance.player_name
		)
		instance.player_kills = validated_data.get(
			'player_kills',
			instance.player_kills
		)
		instance.player_dbno = validated_data.get(
			'player_dbno',
			instance.player_dbno
		)
		instance.player_assists = validated_data.get(
			'player_assists',
			instance.player_assists
		)
		instance.player_dmg = validated_data.get(
			'player_dmg',
			instance.player_dmg
		)
		instance.player_dist_ride = validated_data.get(
			'player_dist_ride',
			instance.player_dist_ride
		)
		instance.player_dist_walk = validated_data.get(
			'player_dist_walk',
			instance.player_dist_walk
		)
		instance.player_survive_time = validated_data.get(
			'player_survive_time',
			instance.player_survive_time
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = PlayerParticipate.objects\
			.values_list('match_id', flat=True)\
			.filter(player_id__exact=player_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for match in new_matches:
			new_id = match.match_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				PlayerParticipate.objects \
					.create(player_id=player_id, match_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				PlayerParticipate.objects \
					.filter(player_id=player_id, match_id=old_id) \
					.delete()

		# old_ids = PlayerInTeam.objects\
		# 	.values_list('team_id', flat=True)\
		# 	.filter(player_id=player.player_id)

		# for team in new_teams:
		# 	new_id = team.team_id
		# 	new_ids.append(new_id)
		# 	if new_id in old_ids:
		# 		continue
		# 	else:
		# 		PlayerInTeam.objects \
		# 			.create(player=player, team = team)

		# # Delete old unmatched country entries
		# for old_id in old_ids:
		# 	if old_id in new_ids:
		# 		continue
		# 	else:
		# 		PlayerInTeam.objects \
		# 			.filter(player_id=player.player_id, team_id=old_id) \
		# 			.delete()

		return instance

class DeathSerializer(serializers.ModelSerializer):
	weapon = WeaponSerializer(many=False, read_only=True)
	victim = PlayerSerializer(many=False, read_only=True)
	killer = PlayerSerializer(many=False, read_only=True)
	match = MatchSerializer(many=False, read_only=True)

	class Meta:
		model = Death
		fields = ('death_id', 'weapon', 'killer', 'killer_placement', 'match', 'game_time', 'victim', 'victim_placement')
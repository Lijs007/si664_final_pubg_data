# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class Death(models.Model):
    death_id = models.AutoField(primary_key=True)
    weapon = models.ForeignKey('Weapon', on_delete=models.PROTECT, blank=True, null=True)
    killer = models.ForeignKey('Player', on_delete=models.PROTECT, blank=True, null=True, related_name='killer')
    killer_placement = models.CharField(max_length=45, blank=True, null=True)
    match = models.ForeignKey('Match', on_delete=models.PROTECT)
    game_time = models.IntegerField()
    victim = models.ForeignKey('Player', on_delete=models.PROTECT, blank=True, null=True, related_name='victim')
    victim_placement = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'death'
        ordering = ['match', 'victim']
        verbose_name = 'PUBG Death'
        verbose_name_plural = 'PUBG Deaths'

    def __str__(self):
        return self.killer + 'killed' + self.victim



class Map(models.Model):
    map_id = models.AutoField(primary_key=True)
    map_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'map'
        ordering = ['map_name']
        verbose_name = 'PUBG Map'
        verbose_name_plural = 'PUBG Maps'

    def __str__(self):
        return self.map_name    


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_id_in_game = models.CharField(max_length=100)
    date = models.CharField(max_length=45)
    game_size = models.IntegerField()
    match_mode = models.CharField(max_length=45)
    party_size = models.IntegerField()
    map = models.ForeignKey(Map, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'match'
        ordering = ['match_id_in_game']
        verbose_name = 'PUBG Match'
        verbose_name_plural = 'PUBG Matches'

    def __str__(self):
        return self.match_id_in_game   


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=45)
    player_kills = models.IntegerField(blank=True, null=True)
    player_dbno = models.IntegerField(blank=True, null=True)
    player_assists = models.IntegerField(blank=True, null=True)
    player_dmg = models.IntegerField(blank=True, null=True)
    player_dist_ride = models.IntegerField(blank=True, null=True)
    player_dist_walk = models.IntegerField(blank=True, null=True)
    player_survive_time = models.IntegerField(blank=True, null=True)
    match = models.ManyToManyField(Match, through='PlayerParticipate')
    team = models.ManyToManyField('Team', through='PlayerInTeam')

    class Meta:
        managed = False
        db_table = 'player'
        ordering = ['player_name']
        verbose_name = 'PUBG Player'
        verbose_name_plural = 'PUBG Players'

    def __str__(self):
        return self.player_name

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('player_detail', kwargs={'pk': self.pk})

    @property
    def matches(self):
        matches = self.match.order_by('match_id_in_game')

        m_ids = []
        for match in matches:
            m_id = match.match_id_in_game
            if m_id is None:
                continue
            if m_id not in m_ids:
                m_ids.append(m_id)

        return ', '.join(m_ids)

    @property
    def team_placements(self):
        teams = self.team.order_by('team_placement')

        tps = []
        for team in teams:
            tp = team.team_placement
            if tp is None:
                continue
            tps.append(str(tp))

        return ', '.join(tps)

    @property
    def deaths(self):

        p_id = self.player_id
        deaths = Death.objects.filter(victim__player_id = p_id)

        weapons = []
        for death in deaths:
            weapon = death.weapon.weapon_name
            if weapon is None:
                continue
            if weapon not in weapons:
                weapons.append(weapon)

        return ', '.join(weapons)

class PlayerInTeam(models.Model):
    player_in_team_id = models.AutoField(primary_key=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_in_team'
        ordering = ['team', 'player']
        verbose_name = 'PUBG Player In Team'
        verbose_name_plural = 'PUBG Players In Teams'




class PlayerParticipate(models.Model):
    player_participate_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_participate'
        ordering = ['match', 'player']
        verbose_name = "PUBG Player Participant"
        verbose_name_plural = "PUBG Player Participants"


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    team_id_in_match = models.IntegerField()
    team_placement = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'
        ordering = ['team_id']
        verbose_name = 'PUBG Team'
        verbose_name_plural = 'PUBG Teams'

    def __str__(self):
        return str(self.team_id_in_match)


class Weapon(models.Model):
    weapon_id = models.AutoField(primary_key=True)
    weapon_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'weapon'
        ordering = ['weapon_name']
        verbose_name = 'PUBG Weapon or Accident'
        verbose_name_plural = 'PUBG Weapons or Accidents'

    def __str__(self):
        return self.weapon_name

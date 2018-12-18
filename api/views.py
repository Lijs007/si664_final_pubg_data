from django.shortcuts import render

from pubg_data.models import Player, PlayerInTeam, PlayerParticipate
from api.serializers import PlayerSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class PlayerViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = Player.objects.order_by('player_name')
	serializer_class = PlayerSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		player = self.get_object(pk)
		self.perform_destroy(self, player)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()


'''
class SiteListAPIView(generics.ListCreateAPIView):
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
'''

'''
class SiteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
'''
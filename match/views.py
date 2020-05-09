"""
Using django rest framework
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist

from .models import Match
from .serializers import MatchSerializer, MatchListSerializer


# Create your views here.

class MatchView(APIView):

    def get(self, request, human_id):
        """
        Select all matches for provided human id
        human_id -- human entry pk
        """
        try:
            match = Match.objects.filter(matched_human=human_id)
            serializer = MatchSerializer(match, many=True)
            return Response({'objects': serializer.data})
        except ObjectDoesNotExist:
            return Response({'description': 'No match for human with such id or no human with such id.'}, status=404)


class MatchListView(ListAPIView):
    """
    List of matches with short descriptions of humans, they are matched to
    """

    queryset = Match.objects.all().select_related('matched_human')
    serializer_class = MatchListSerializer

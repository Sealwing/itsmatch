from django.shortcuts import render
from django.http import JsonResponse
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
        TODO docstring
        """
        try:
            match = Match.objects.filter(matched_human=human_id)
            serializer = MatchSerializer(match, many=True)
            return Response({'objects': serializer.data})
        except ObjectDoesNotExist:
            return Response({'description': 'No match for human with such id or no human with such id.'}, status=404)


class MatchListView(ListAPIView):
    queryset = Match.objects.all().select_related('matched_human')
    serializer_class = MatchListSerializer

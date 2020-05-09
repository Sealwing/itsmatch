from rest_framework import serializers

from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('first_name', 'second_name', 'age', 'gender')


class MatchListSerializer(MatchSerializer):
    matched_human = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = ('first_name', 'second_name', 'age', 'gender', 'matched_human')

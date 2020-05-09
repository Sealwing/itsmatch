from django.urls import path
from .views import MatchView, MatchListView

urlpatterns = [
    path('', MatchListView.as_view(), name='all_matches'),
    path('<int:human_id>', MatchView.as_view(), name='match')
]

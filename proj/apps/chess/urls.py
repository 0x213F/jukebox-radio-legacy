
from django.contrib import admin
from django.urls import path

from .views import CloseMatchView
from .views import CreateMatchView
from .views import GetMatchView
from .views import JoinMatchView
from .views import ListMatchesView
from .views import MovePieceView
from .views import ResignMatchView
from .views import SuggestMoveView
from .views import UndoRequestView
from .views import UndoResponseView


urlpatterns = [
    path('close-match/', CloseMatchView.as_view()),
    path('create-match/', CreateMatchView.as_view()),
    path('get-match/', GetMatchView.as_view()),
    path('join-match/', JoinMatchView.as_view()),
    path('list-matches/', ListMatchesView.as_view()),
    path('move-piece/', MovePieceView.as_view()),
    path('resign-match/', ResignMatchView.as_view()),
    path('suggest-move/', SuggestMoveView.as_view()),
    path('undo-request/', UndoRequestView.as_view()),
    path('undo-response/', UndoResponseView.as_view()),
]

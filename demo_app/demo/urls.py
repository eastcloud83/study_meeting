# ファイル自体を追加
from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionView.as_view(), name='question'),
    path('answer/', views.AnswerView.as_view(), name='answer'),
]

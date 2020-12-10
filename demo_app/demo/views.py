from django.shortcuts import render

# 追加
# どのページを表示するか決定する
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import QuestionForm

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import MeCab
m = MeCab.Tagger("-d /home/eastcloud83/Downloads/mecab-ipadic-2.7.0-20070801")  # MeCabオブジェクト


class QuestionView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'デモ',
            'form': QuestionForm()
        }

    def get(self, request):
        return render(request, 'demo/question.html', self.params)

    def post(self, request):
        question = request.POST['question']

        answers = '<table class="table" width="100%">'
        answers += '<tr>'
        answers = answers + '<td>' + "質問" + '</td>'
        answers = answers + '<td>' + question + '</td>'
        answers += '</tr>'
        answers += '<tr>'
        answers = answers + '<td>' + "回答" + '</td>'
        answers = answers + '<td>' + qa(question) + '</td>'
        answers += '</tr>'
        self.params['answer'] = answers + '</table>'

        return render(request, 'demo/answer.html', self.params)


class AnswerView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'デモ',
            'message': ''
        }

    def get(self, request):
        return render(request, 'demo/answer.html', self.params)


def qa(q):
    """
    質問文と最もコサイン類似度が高い答えを返す
    :param q: 質問文
    :return:　答え
    """
    condidate_answers = ["今日の天気は晴れです。", "今年は2020年です。", "日本の首都は東京です。"]
    vectorizer = TfidfVectorizer(tokenizer=tokenize_simple, token_pattern=u'(?u)\\b\\w+\\b', norm='l1')
    experiences_vec = vectorizer.fit_transform(condidate_answers)  # TF-IDF値計算
    scores = cosine_similarity(vectorizer.transform([q]), experiences_vec)[0]
    max_idx = np.argmax(scores)
    return condidate_answers[max_idx]


def tokenize_simple(txt):
    """
    テキストを単語リストにして返す
    :param txt: テキスト
    :return: 単語リスト
    """
    words = []
    node = m.parseToNode(txt)
    while node:
        word = node.surface  # 表層系
        if word != "" and word != "*":
            words.append(word)
        node = node.next
    return words

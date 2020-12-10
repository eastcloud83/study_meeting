# ファイル自体を追加
from django import forms


class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='')
from django import forms
from django.shortcuts import render
from .models import Post, BigCategory

# forms.pyを作るのが面倒だったので、ここでフォームセットクラスを定義しました。
PostFormSet = forms.modelformset_factory(Post, fields='__all__', extra=5)


def top(request):
    """表示するだけで、実際の登録処理は省略しています。"""
    context = {
        'formset': PostFormSet(request.POST or None),
        'bigcategory_list': BigCategory.objects.all(),
    }
    return render(request, 'app/top.html', context)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages  # メッセージフレームワーク
from django.urls import reverse_lazy
from .models import Book,Impression
from django.views import generic
from .forms import BookCreateForm,ImpressionCreateForm

class IndexView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'book_list.html'
    paginate_by = 7


class AddView(generic.CreateView):
    model = Book
    template_name = 'book_add.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('bookmanager:index')  # /bookmanager/

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        book = form.save(commit=False)
        # book.editer = str(request.user.id)
        book.save()
        messages.success(self.request, "追加しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "追加できませんでした")
        return super().form_invalid(form)

# 感想数をカウント
# p2 = Book.objects.filter(impressions__book__isnull=False).values('id').annotate(impre_count=Count('id'))

class UpdateView(generic.UpdateView):
    model = Book
    template_name = 'book_add.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('bookmanager:index')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        book = form.save(commit=False)
        book.editer = str(request.user)
        book.save()
        messages.success(self.request, "編集しました")
        return super().form_valid(form)


class DeleteView(generic.DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('bookmanager:index')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "削除しました")
        return super().form_valid(form)


class ImpressionList(generic.ListView):
    """感想の一覧"""
    model = Impression
    context_object_name = 'impressions'
    template_name = 'impression_list.html'
    paginate_by = 7  # １ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])  # 親の書籍を読む
        impressions = book.impressions.all().order_by('id')  # 書籍の子供の、感想を読む
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)



# class ImpressionAddView(generic.CreateView):
#     model = Impression
#     template_name = 'impression_add.html'
#     form_class = ImpressionCreateForm
#
#     def form_valid(self, form):
#         book_pk = self.kwargs['pk']
#         impression = form.save(commit=False)  # コメントはDBに保存されていません
#         impression.book = get_object_or_404(Book, pk=book_pk)
#         impression.save()  # ここでDBに保存
#         return redirect('bookmanager:impression_list', pk=book_pk)

def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:  # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:  # impression_id が指定されていない (追加時)
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():  # フォームのバリデーション
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            # impression.editer = str(request.user)
            impression.save()
            return redirect('impression_list', book_id=book_id)
    else:  # GET の時
        form = ImpressionForm(instance=impression)  # impression インスタンスからフォームを作成

    return render(request,
                  'impression_edit.html',
                  dict(form=form, book_id=book_id, impression_id=impression_id))
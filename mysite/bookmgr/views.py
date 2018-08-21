from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect,render,reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import messages  # メッセージフレームワーク
from django.urls import reverse_lazy
from bookmgr.models import Book,Impression
from django.views import generic
from .forms import BookCreateForm,BookFormSet #ImpressionCreateForm
from django.db.models import Q,Count,Sum

"""書籍一覧"""
@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'book_list.html'
    paginate_by = 7

    def get_queryset(self):
        # 子数を親の感想数にセット
        # qs = Book.objects.filter(impressions__isnull=False).values('id').annotate(impre_count=Count('id'))
        # for i in qs:
        #     Book.objects.filter(id=i['id']).update(impressionCount=i['impre_count']) # 辞書型のキーを指定して更新
        queryset = Book.objects.all().order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(bookType__icontains=keyword)
            )
        return queryset

"""書籍追加"""
@method_decorator(login_required, name='dispatch')
class AddView(generic.CreateView):
    model = Book
    template_name = 'book_add.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('bookmgr:index')  # /bookmgr/

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        book = form.save(commit=False)
        # book.editer = request.user.id
        form.instance.editer = str(self.request.user)
        book.save()
        # 追加のとき
        if 'save' in self.request.POST:
            messages.success(self.request, "追加しました")
            return redirect('bookmgr:index')

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "追加できませんでした")
        return super().form_invalid(form)


class multiAddView(generic.FormView):
    template_name = 'book_multiAdd.html'
    form_class = BookFormSet
    success_url = reverse_lazy('bookmgr:index')

    # なりとさんご教授
    def get_form(self, form_class=None):
         # return BookFormSet(self.request.POST or None)
         return BookFormSet(self.request.POST or None, queryset=Book.objects.none())

    # def form_valid(self, form):
    #     for fm in form:
    #         book = fm.save(commit=False)
    #         book.editer = str(self.request.user)
    #         book.save()
    #     return super().form_valid(form)

    # なりとさんご教授
    def form_valid(self, form):
        # instancesは、新たに作成されたbookと更新されたbookが入ったリスト
        instances = form.save(commit=False)

        # まず、削除チェックがついたbookを取り出して削除
        for book in form.deleted_objects:
            book.delete()

        # 新たに作成されたbookと更新されたbookを取り出して、新規作成or更新処理
        for book in instances:
            book.editer = str(self.request.user)
            book.save()

        return super().form_valid(form)


"""書籍の編集"""
@method_decorator(login_required, name='dispatch')
class UpdateView(generic.UpdateView):
    model = Book
    template_name = 'book_edit.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('bookmgr:index')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        book = form.save(commit=False)
        # book.editer = str(request.user)
        book.save()
        messages.success(self.request, "編集しました")
        return super().form_valid(form)


"""書籍の削除"""
@method_decorator(login_required, name='dispatch')
class DeleteView(generic.DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('bookmgr:index')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "削除しました")
        return super().form_valid(form)



from django.http import HttpResponse
from django.shortcuts import render

def ip(request):
    ip_addr = request.META['REMOTE_ADDR']
    return render(request,
        'ip.html',
        {'ip_addr' : ip_addr}
        )



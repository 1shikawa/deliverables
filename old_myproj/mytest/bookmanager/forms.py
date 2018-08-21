from django import forms
from .models import Book,Impression


class BookCreateForm(forms.ModelForm):
    """書籍のフォーム"""
    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Book
        fields = ('bookType', 'name', 'publisher', 'page', 'impressionCount',)


class ImpressionCreateForm(forms.ModelForm):
    """感想のフォーム"""
    def __init__(self, *args, **kwargs):
        super(ImpressionCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Impression
        fields = ('comment','readCount',)
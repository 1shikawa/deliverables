from django.db import models


class BigCategory(models.Model):
    name = models.CharField('大カテゴリ名', max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('中カテゴリ名', max_length=255)
    parent = models.ForeignKey(BigCategory, verbose_name='大カテゴリ', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Post(models.Model):
    big_category = models.ForeignKey(BigCategory, verbose_name='大カテゴリ', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, verbose_name='中カテゴリ', on_delete=models.PROTECT)

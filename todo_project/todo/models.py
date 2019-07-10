# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Enterprise(models.Model):
    """ Предприятие """
    name = models.CharField(max_length=255, verbose_name=u'Название предприятия')

    class Meta:
        verbose_name = u'Предприятие'
        verbose_name_plural = u'Предприятия'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class UserEnterprise(models.Model):
    """ Связка Юзера с предприятием """
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    enterprise = models.ForeignKey(Enterprise, verbose_name=u'Предприятие')

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.enterprise)

    class Meta:
        verbose_name = u'Пользователь предприятия'
        verbose_name_plural = u'Пользователи предприятий'
        unique_together = ('user', 'enterprise',)
        ordering = ('enterprise', 'user',)


TODO_STATUS = {
    1: u'Открыто',
    2: u'В работе',
    3: u'Выполнено'
}


class Todo(models.Model):
    """ Задача """
    enterprise = models.ForeignKey(Enterprise, verbose_name=u'Предприятие')
    text = models.TextField(verbose_name=u'Текст задачи')
    status = models.PositiveSmallIntegerField(choices=TODO_STATUS.items(), verbose_name=u'Статус', default=1)
    author = models.ForeignKey(User, related_name='author', verbose_name=u'Автор')
    performer = models.ForeignKey(User, related_name='performer', verbose_name=u'Исполнитель', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    time_edited = models.DateTimeField(auto_now=True, verbose_name=u'Дата редактирования')

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

    def __unicode__(self):
        return self.text


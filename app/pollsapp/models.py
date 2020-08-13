from typing import Final

from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


class Choice(models.Model):
    title = models.CharField(max_length=4096)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")


class Question(models.Model):
    TYPE_CHOICES: Final[tuple] = (
        ('text', gettext('Text')),
        ('one', gettext('One option')),
        ('many', gettext('Many options')),
    )

    title = models.CharField(verbose_name=_("Title"), max_length=4096)
    question_type = models.CharField(
        verbose_name=_("Type"),
        max_length=4,
        choices=TYPE_CHOICES
    )

    choices = models.ManyToManyField(
        Choice, verbose_name=_("Choices"),
        related_name='questions'
    )
    is_active = models.BooleanField(
        verbose_name=_("Question enabled"),
        default=True
    )

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        unique_together = ['title', 'question_type']


class Poll(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=120)

    started_at = models.DateTimeField(verbose_name=_("Start time"))

    finish_at = models.DateTimeField(verbose_name=_("Finish time"))

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True
    )

    is_active = models.BooleanField(
        verbose_name=_("Poll enabled"),
        default=True,
        db_index=True
    )

    questions = models.ManyToManyField(
        Question,
        verbose_name=_("Questions"),
        related_name='polls'
    )

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")


class Answer(models.Model):
    user = models.IntegerField()
    question = models.ForeignKey(
        Question,
        verbose_name=_("Question"),
        related_name='answers',
        on_delete=models.CASCADE,
    )
    choice = models.ForeignKey(
        Choice,
        verbose_name=_("Choice"),
        related_name='answers_one',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    choices = models.ManyToManyField(
        Choice,
        verbose_name=_("Choices"),
        related_name='answers_many',
        blank=True,
    )
    choice_text = models.TextField(
        verbose_name=_("Choice text"),
        blank=True,
        null=True,
    )
    poll = models.ForeignKey(
        Poll,
        verbose_name=_("Poll"),
        related_name='answers',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.choice.title

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        unique_together = ('user', 'question', 'poll',)

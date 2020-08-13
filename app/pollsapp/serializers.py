from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Poll, Question, Choice, Answer


class PollSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:poll-detail")
    questions = serializers.HyperlinkedRelatedField(
        view_name='api:question-detail',
        lookup_field='pk',
        many=True,
        read_only=False,
        queryset=Question.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('started_at').read_only = True

    class Meta:
        model = Poll
        fields = (
            'url',
            'title',
            'started_at',
            'finish_at',
            'description',
            'questions',
            'is_active',
        )


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    type_fields = {
        'text': 'choice_text',
        'one': 'choice',
        'many': 'choices',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if q_pk := kwargs['context']['request'].parser_context.get('kwargs', {}).get('question_pk'):
                if q := Question.objects.get(pk=q_pk):
                    self.choice_objects = q.choices.all()
                    self.fields['choice'].queryset = self.fields['choices'].queryset = self.choice_objects
                    missed_fields = [field for key, field in self.type_fields.items() if key != q.question_type]
                    for field in missed_fields:
                        self.fields.pop(field)
        except Question.DoesNotExist:
            raise NotFound(detail="Error 404, page not found", code=404)

    def to_representation(self, value):
        repr_dict = super().to_representation(value)
        return OrderedDict((k, v) for k, v in repr_dict.items()
                           if v not in [None, [], '', {}])

    user = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:answer-detail")

    choice_text = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        max_length=4096,
        read_only=False,
    )

    question = serializers.HyperlinkedRelatedField(
        view_name='api:question-detail',
        lookup_field='pk',
        read_only=True,
    )

    poll = serializers.HyperlinkedRelatedField(
        view_name='api:poll-detail',
        lookup_field='pk',
        read_only=True,
    )

    choice = serializers.HyperlinkedRelatedField(
        view_name='api:choice-detail',
        lookup_field='pk',
        read_only=False,
        allow_null=True,
        queryset=Choice.objects.all(),
    )

    choices = serializers.HyperlinkedRelatedField(
        view_name='api:choice-detail',
        lookup_field='pk',
        many=True,
        read_only=False,
        # TODO ограничить выборку
        queryset=Choice.objects.all(),
    )

    class Meta:
        model = Answer
        fields = ('user', 'url', 'poll', 'question', 'choice', 'choices', 'choice_text')


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:choice-detail")

    questions = serializers.HyperlinkedRelatedField(
        view_name='api:question-detail',
        lookup_field='pk',
        many=True,
        read_only=False,
        queryset=Question.objects.all(),
    )

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:question-detail")

    choices = serializers.HyperlinkedRelatedField(
        view_name='api:choice-detail',
        many=True,
        read_only=False,
        queryset=Choice.objects.all(),
    )

    class Meta:
        model = Question
        fields = (
            'url',
            'title',
            'question_type',
            'choices',
            'is_active',
        )

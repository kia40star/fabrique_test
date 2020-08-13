from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from pollsapp.models import Poll, Question, Answer, Choice
from pollsapp.serializers import PollSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer


class ActionBasedPermission(permissions.AllowAny):
    """Grant or deny access to a view"""

    def has_permission(self, request, view):
        for c_class, actions in getattr(view, 'action_permissions',
                                        {}).items():
            if view.action in actions:
                return c_class().has_permission(request, view)
        return False


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('rest_login', request=request, format=format),
        'logout': reverse('rest_logout', request=request, format=format),
        'polls': reverse('api:poll-list', request=request, format=format),
        'questions': reverse('api:question-list', request=request, format=format),
        'choices': reverse('api:choice-list', request=request, format=format),
        'answers': reverse('api:answer-list', request=request, format=format),
    })


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAdminUser: [
            'update',
            'partial_update',
            'destroy',
            'create',
        ],
        permissions.AllowAny: ['list', 'retrieve']
    }
    serializer_class = PollSerializer

    queryset = Poll.objects.all()


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = QuestionSerializer

    queryset = Question.objects.all()


class CreateAnswerView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        user = self.request.user.pk or 0
        try:
            question = Question.objects.get(pk=self.kwargs.get('question_pk'))
            poll = Poll.objects.get(pk=self.kwargs.get('poll_pk'))
            serializer.save(
                poll=poll,
                question=question,
                user=user,
            )
        except Exception:
            raise ValidationError(detail="Error 400, Bad Request", code=400)


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = ('user', 'poll')
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    http_method_names = ['get', 'head', 'options']


class ChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


class PollQuestionViewSet(QuestionViewSet):
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.AllowAny: ['list', 'retrieve', 'answer'],
    }

    def get_queryset(self):
        queryset = Question.objects.filter(polls__id=self.kwargs["poll_pk"]).prefetch_related()
        return queryset

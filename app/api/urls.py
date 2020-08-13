from django.urls import include, path
from rest_framework_nested import routers
from .views import *

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
polls_router = routers.NestedSimpleRouter(router, r'polls', lookup='poll')
polls_router.register(
    r'questions',
    PollQuestionViewSet,
    basename='polls-questions'
)
questions_router = routers.NestedSimpleRouter(
    polls_router,
    r'questions',
    lookup='question'
)
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'choices', ChoiceViewSet, basename='choice')

urlpatterns = [
    path('', api_root),
    path('', include(router.urls)),
    path('', include(polls_router.urls)),
    path('', include(questions_router.urls)),
    path(
        "polls/<int:poll_pk>/questions/<int:question_pk>/answer/",
        CreateAnswerView.as_view(),
        name="create_answer"
    )
]

urlpatterns += router.urls

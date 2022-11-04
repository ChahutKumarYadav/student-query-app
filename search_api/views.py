from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from question.models import Question
from rest_framework import viewsets
from rest_fuzzysearch import search, sort
from question.serializers import QuestionSerializer


class SearchQuestionViewSet(sort.SortedModelMixin,
                            search.SearchableModelMixin,
                            viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    lookup_field = 'question'
    lookup_value_regex = '[^/]+'
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_backends = (search.RankedFuzzySearchFilter, sort.OrderingFilter)
    min_rank = 0.001
    search_fields = ('question', 'tag')
    ordering_fields = ('rank', 'question', 'tag')
    ordering = ('-rank',)

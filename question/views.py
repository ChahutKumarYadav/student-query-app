from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers as slr
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Question, QLike, Answer, Comment, ALike
from .serializers import (
    QuestionSerializer, QLikeSerializer,
    AnswerSerializer, CommentSerializer,
    ALikeSerializer)


class QuestionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    @action(detail=True, methods=["POST"])
    def likeQuestion(self, request, pk=None):
        question = Question.objects.get(id=pk)
        user = request.user
        likes = QLike.objects.create(user=user, question=question)
        serializer = QLikeSerializer(likes, many=False)
        response = {"message": "Liked!", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def answer(self, request, pk=None):
        question = Question.objects.get(id=pk)
        user = request.user
        answer = Answer.objects.create(
            user=user, question=question, answer_text=request.data["answer_text"]
        )
        serializer = AnswerSerializer(answer, many=False)
        response = {"message": "answer to the question", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"])
    def answerDelete(self, request, pk=None):
        question = Question.objects.get(id=pk)
        user = request.user
        answer = Answer.objects.get(
            user=user, question=question
        )
        answer.delete()
        serializer = AnswerSerializer(answer, many=False)
        response = {"message": "Answer deleted!", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"])
    def dislikeQuestion(self, request, pk=None):
        question = Question.objects.get(id=pk)
        user = request.user
        likes = QLike.objects.get(user=user, question=question)
        likes.delete()
        serializer = QLikeSerializer(likes, many=False)
        response = {"message": "removed like", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)


class AnswerViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    @action(detail=True, methods=["POST"])
    def comment(self, request, pk=None):
        answer = Answer.objects.get(id=pk)
        user = request.user
        comment = Comment.objects.create(
            user=user, answer=answer, comment=request.data["comment"]
        )
        serializer = CommentSerializer(comment, many=False)
        response = {"message": "comment added.", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"])
    def commentDelete(self, request, pk=None):
        answer = Answer.objects.get(id=pk)
        user = request.user
        comment = Comment.objects.get(
            user=user, answer=answer
        )
        comment.delete()
        serializer = CommentSerializer(comment, many=False)
        response = {"message": "comment deleted..", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def likeAnswer(self, request, pk=None):
        answer = Answer.objects.get(id=pk)
        user = request.user
        likes = ALike.objects.create(user=user, answer=answer)
        serializer = ALikeSerializer(likes, many=False)
        response = {"message": "Liked!", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"])
    def dislikeAnswer(self, request, pk=None):
        answer = Answer.objects.get(id=pk)
        user = request.user
        likes = ALike.objects.get(user=user, answer=answer)
        likes.delete()
        serializer = ALikeSerializer(likes, many=False)
        response = {"message": "Remove Liked!", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

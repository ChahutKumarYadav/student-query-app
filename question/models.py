from django.db import models
from django.conf import settings


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_asked')
    question = models.TextField()
    tag = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "{} - {}".format(self.question, self.user)

    def no_of_like(self):
        likes = QLike.objects.filter(question=self)
        return len(likes)

    def no_of_answer(self):
        answer = Answer.objects.filter(question=self)
        return len(answer)


class QuestionImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    qImage = models.ImageField(upload_to='question_img/', blank=True, null=True)

    def __str__(self):
        return self.qImage


class QLike(models.Model):
    question = models.ForeignKey(Question, related_name='q_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='q_likes', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = (('user', 'question'),)
        index_together = (('user', 'question'),)


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answered_question')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answered_question')
    answer_text = models.TextField()
    reference = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.question.id, self.user)

    class Meta:
        ordering = ["-date"]

    def no_of_like(self):
        likes = ALike.objects.filter(answer=self)
        return len(likes)

    def no_of_answer(self):
        comments = Comment.objects.filter(answer=self)
        return len(comments)


class AnswerImage(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    aImage = models.ImageField(upload_to='question_img/', blank=True, null=True)

    def __str__(self):
        return self.aImage


class ALike(models.Model):
    answer = models.ForeignKey(Answer, related_name='a_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='a_likes', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = (('user', 'answer'),)
        index_together = (('user', 'answer'),)


class Comment(models.Model):
    answer = models.ForeignKey(Answer, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def no_of_like(self):
        likes = CommentLike.objects.filter(comment=self)
        return len(likes)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, related_name='c_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_likes', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = (('user', 'comment'),)
        index_together = (('user', 'comment'),)

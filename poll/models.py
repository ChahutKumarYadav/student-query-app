import datetime
from django.db import models
from django.utils import timezone

from django.conf import settings


class PollQuestion(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='poll')
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently'

    def user_can_vote(self, user):
        """
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    def __str__(self):
        return self.question_text


class PLike(models.Model):
    poll = models.ForeignKey(PollQuestion, related_name='p_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_likes', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = (('user', 'poll'),)
        index_together = (('user', 'poll'),)


class PollImage(models.Model):
    poll_question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    pImage = models.ImageField(upload_to='question_img/', blank=True, null=True)

    def __str__(self):
        return self.pImage


class PollChoice(models.Model):
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE, related_name="choice")
    answer = models.BooleanField(default=False)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

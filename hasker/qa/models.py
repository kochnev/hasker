from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Tag(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    has_answer =  models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    voters = models.ManyToManyField(get_user_model(), related_name='vote_questions', through='QuestionVote')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_tags_str(self):
        return ','.join([t.title for t in self.tags.all()])

    def cancel_vote(self, user):
        qv_up = QuestionVote.objects.filter(user=user, question=self, vote_type='up')
        qv_down = QuestionVote.objects.filter(user=user, question=self, vote_type='down')
        cancel = False
        if qv_up.exists():
            # cancel vote up
            qv_up.delete()
            self.rating -= 1
            cancel = True
        elif qv_down.exists():
            # cancel vote_down
            qv_down.delete()
            self.rating += 1
            cancel = True
        return cancel

    def upvote(self, user):
        if not self.cancel_vote(user):
            self.question_votes.create(user=user, question=self, vote_type='up')
            self.rating += 1
        self.save()

    def downvote(self, user):
        if not self.cancel_vote(user):
            self.question_votes.create(user=user, question=self, vote_type='down')
            self.rating -= 1

        self.save()


class Answer(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    is_correct = models.NullBooleanField()
    rating = models.IntegerField(default=0)
    voters = models.ManyToManyField(get_user_model(), related_name='vote_answers', through='AnswerVote')

    def cancel_vote(self, user):
        av_up = AnswerVote.objects.filter(user=user, answer=self, vote_type='up')
        av_down = AnswerVote.objects.filter(user=user, answer=self, vote_type='down')
        cancel = False
        if av_up.exists():
            # cancel vote up
            av_up.delete()
            self.rating -= 1
            cancel = True
        elif av_down.exists():
            # cancel vote_down
            av_down.delete()
            self.rating += 1
            cancel = True
        return cancel

    def upvote(self, user):
        if not self.cancel_vote(user):
            self.answer_votes.create(user=user, answer=self, vote_type='up')
            self.rating += 1
        self.save()

    def downvote(self, user):
        if not self.cancel_vote(user):
            self.answer_votes.create(user=user, answer=self, vote_type='down')
            self.rating -= 1

        self.save()


class QuestionVote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_votes')
    vote_type = models.CharField(max_length=4)

    class Meta:
        unique_together = ('user', 'question', 'vote_type')


class AnswerVote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_votes')
    vote_type = models.CharField(max_length=4)

    class Meta:
        unique_together = ('user', 'answer', 'vote_type')





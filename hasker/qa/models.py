from django.db import models, transaction
from django.db.models import Q
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.mail import send_mail


class Entity(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    @transaction.atomic
    def vote(self, user, vote_type):
        v = Votes.objects.filter(Q(question=self.id) | Q(answer=self.id), user=user)
        if v.exists():
            self.rating -= v[0].vote_type
            v.delete()
        else:
            if isinstance(self, Question):
                Votes.objects.create(user=user, question=self, vote_type=vote_type)
            elif isinstance(self, Answer):
                Votes.objects.create(user=user, answer=self, vote_type=vote_type)
            self.rating += vote_type
        self.save()

    class Meta:
        abstract = True


class Question(Entity):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', blank=True)
    correct_answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='correct_for_question')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'slug': self.slug})

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

    def set_tags(self, tags_str):
        tags_arr = tags_str.split(',')
        if len(tags_arr) <= 3:
            self.tags.clear()
            for tag in tags_arr:
                (t, created) = Tag.objects.get_or_create(title=tag)
                t.save()
                self.tags.add(t)
            self.save()
            return ''
        else:
            return 'You are allowed to input up to 3 tags'

    def notify_answer_added(self, answer, link):
        send_mail(
            'new answer was added',
            'The answer is:\n' +
            answer.text + '\n\n' +
            'Here is the link for your question ' + link,
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

    class Meta:
        app_label = 'qa'


class Answer(Entity):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL)


class Tag(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Votes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    vote_type = models.IntegerField()
    question = models.ForeignKey('Question', null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.CASCADE)






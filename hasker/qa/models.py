from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Votes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    vote_type = models.IntegerField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Entity(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    @transaction.atomic
    def vote(self, user, vote_type):
        content_type = ContentType.objects.get_for_model(self)
        v = Votes.objects.filter(user=user, content_type__pk=content_type.id, object_id=self.id)
        if v.exists():
            self.rating -= v[0].vote_type
            v.delete()
        else:
            Votes.objects.create(user=user, content_object=self, vote_type=vote_type)
            self.rating += vote_type
        self.save()

    class Meta:
        abstract = True


class Tag(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Question(Entity):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    correct_answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='correct_for_question')

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


class Answer(Entity):
    question = models.ForeignKey(Question)





# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import pgettext_lazy, ugettext_lazy as _

from oscar.apps.catalogue.reviews.abstract_models import AbstractProductReview
from django.contrib.sites.models import Site
from oscar.core import validators
from oscar.core.compat import AUTH_USER_MODEL, user_is_authenticated
from shop.catalogue.models import Product


def preview_text(value, length=116, ending='...'):
    if len(value) > length:
        return ''.join((value[:length - len(ending)].rsplit(' ', 1)[0], ending))
    return value


class ProductReview(AbstractProductReview):
    title = models.CharField(
        verbose_name=pgettext_lazy(u"Product review title", u"Title"),
        max_length=255,
        validators=[validators.non_whitespace],
        blank=True
    )
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)
    advantage = models.TextField('Преимущества', blank=True)
    disadvantage = models.TextField('Недостатки', blank=True)
    get_notification = models.BooleanField(
        'Получать уведомления об ответах',
        default=False
    )
    reply_to = models.ForeignKey('self', blank=True, null=True)


@receiver(post_save, sender=ProductReview)
def on_review_create(sender, instance, created, **kwargs):
    if not created or not instance.reply_to:
        return
    try:
        review = sender.objects.get(pk=instance.reply_to.pk,
                                    get_notification=True)
    except ObjectDoesNotExist:
        return
    to_email = review.email or review.user.email
    message = 'Your review has been commented, please follow the reference' \
              'to see the the comment http://{0}/{1}'.format(
        instance.site.domain, instance.product.get_absolute_url())
    send_mail('Notification about your review',
              message,
              settings.DEFAULT_FROM_EMAIL,
              [to_email],
              fail_silently=True)


class ProductQuestion(models.Model):
    class Meta:
        verbose_name = 'Вопрос о товаре'
        verbose_name_plural = 'Вопросы о товаре'

    product = models.ForeignKey(Product,
                                verbose_name="Товар",
                                on_delete=models.CASCADE)
    when_created = models.DateTimeField('Дата и время создания',
                                        auto_now_add=True)
    name = models.CharField('Имя', max_length=128)
    email = models.EmailField('Почта', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=10)
    text = models.TextField('Вопрос')

    def __unicode__(self):
        return u'{} - {}'.format(self.name, self.when_created)


class ReviewAnswer(models.Model):
    review = models.ForeignKey(ProductReview,
                               related_name="answers",
                               blank=True,
                               null=True)
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='answers')
    name = models.CharField("Имя", max_length=255)
    email = models.EmailField("Email")
    body = models.TextField("Комментарий")
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)
    get_notification = models.BooleanField(
        'Получать уведомления об ответах',
        default=False
    )
    date_created = models.DateTimeField("Дата создания", auto_now_add=True)
    reply_to = models.ForeignKey('self',
                                 blank=True,
                                 null=True,
                                 related_name='answer_to_answer')
    total_votes = models.IntegerField(
        _("Total Votes"), default=0)  # upvotes + down votes
    delta_votes = models.IntegerField(
        _("Delta Votes"), default=0, db_index=True)  # upvotes - down votes

    class Meta:
        verbose_name = 'Ответ на отзыв'
        verbose_name_plural = 'Ответы на отзывы'

    def __unicode__(self):
        return preview_text(self.body)

    def vote_up(self, user):
        self.votes.create(user=user, delta=VoteAnswer.UP)

    def vote_down(self, user):
        self.votes.create(user=user, delta=VoteAnswer.DOWN)

    @property
    def num_up_votes(self):
        """Returns the total up votes"""
        return int((self.total_votes + self.delta_votes) / 2)

    @property
    def num_down_votes(self):
        """Returns the total down votes"""
        return int((self.total_votes - self.delta_votes) / 2)

    def update_totals(self):
        """
        Update total and delta votes
        """
        result = self.votes.aggregate(
            score=Sum('delta'), total_votes=Count('id'))
        self.total_votes = result['total_votes'] or 0
        self.delta_votes = result['score'] or 0
        self.save()

    def can_user_vote(self, user):
        if not user_is_authenticated(user):
            return False, _(u"Only signed in users can vote")
        vote = self.votes.model(answer=self, user=user, delta=1)
        try:
            vote.full_clean()
        except ValidationError as e:
            return False, u"%s" % e
        return True, ""


@receiver(post_save, sender=ReviewAnswer)
def on_review_answer_create(sender, instance, created, **kwargs):
    if not created or not instance.review:
        return
    try:
        review = ProductReview.objects.get(pk=instance.review.pk,
                                    get_notification=True)
    except ObjectDoesNotExist:
        return
    to_email = review.email or review.user.email
    message = 'Your review has been commented, please follow the reference' \
              'to see the the comment http://{0}/{1}'.format(
        instance.site.domain, instance.review.product.get_absolute_url())
    send_mail('Notification about your review',
              message,
              settings.DEFAULT_FROM_EMAIL,
              [to_email],
              fail_silently=True)


@receiver(post_save, sender=ReviewAnswer)
def on_answer_to_answer_create(sender, instance, created, **kwargs):
    if not created or not instance.reply_to:
        return
    try:
        answer = ReviewAnswer.objects.get(pk=instance.reply_to.pk,
                                    get_notification=True)
    except ObjectDoesNotExist:
        return
    to_email = answer.email or answer.user.email
    message = 'Your review has been commented, please follow the reference' \
              'to see the the comment http://{0}/{1}'.format(
        instance.site.domain, instance.reply_to.review.product.get_absolute_url())
    send_mail('Notification about your review',
              message,
              settings.DEFAULT_FROM_EMAIL,
              [to_email],
              fail_silently=True)


class VoteAnswer(models.Model):
    answer = models.ForeignKey(
        ReviewAnswer,
        on_delete=models.CASCADE,
        related_name='votes')
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='answer_votes',
        on_delete=models.CASCADE)
    UP, DOWN = 1, -1
    VOTE_CHOICES = (
        (UP, _("Up")),
        (DOWN, _("Down"))
    )
    delta = models.SmallIntegerField(_('Delta'), choices=VOTE_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'reviews'
        ordering = ['-date_created']
        unique_together = (('user', 'answer'),)
        verbose_name = _('Vote answer')
        verbose_name_plural = _('Votes answer')

    def __str__(self):
        return u"%s vote for %s" % (self.delta, self.answer)

    def clean(self):
        previous_votes = self.answer.votes.filter(user=self.user)
        if len(previous_votes) > 0:
            raise ValidationError(_(
                "You can only vote once on a answer"))

    def save(self, *args, **kwargs):
        super(VoteAnswer, self).save(*args, **kwargs)
        self.answer.update_totals()



from oscar.apps.catalogue.reviews.models import *  # noqa

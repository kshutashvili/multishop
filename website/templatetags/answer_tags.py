from django import template

register = template.Library()


@register.filter
def may_vote_answer(answer, user):
    can_vote, __ = answer.can_user_vote(user)
    return can_vote

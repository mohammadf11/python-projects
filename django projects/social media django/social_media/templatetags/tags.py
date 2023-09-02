from django import template
from account.models import User

register = template.Library()


@register.simple_tag(takes_context=True)
def is_like_post(context, post_id):
    return context['request'].user.is_like_post(post_id)

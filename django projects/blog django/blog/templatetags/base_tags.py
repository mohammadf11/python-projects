from django import template
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/partials/navbar.html' , takes_context=True)
def navbar(context): 
    return {
        'categories': Category.objects.active(),
        'request' : context['request']
        }
    
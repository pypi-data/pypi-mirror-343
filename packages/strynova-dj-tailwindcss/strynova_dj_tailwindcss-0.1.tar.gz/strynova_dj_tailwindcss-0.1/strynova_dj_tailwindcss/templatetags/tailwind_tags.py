"""
Template tags for Tailwind CSS integration.
"""
from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def tailwind_css():
    """
    Include Tailwind CSS from local build.

    Usage:
        {% load tailwind_tags %}
        {% tailwind_css %}
    """
    # Get the path to the compiled output.css file
    css_path = getattr(settings, 'TAILWIND_OUTPUT_PATH', None)

    if not css_path:
        raise template.TemplateSyntaxError(
            'TAILWIND_OUTPUT_PATH must be defined in settings.py'
        )

    # Return a link tag to the compiled CSS file
    return mark_safe(
        f'<link href="{static(css_path)}" rel="stylesheet">'
    )




@register.filter
def tailwind_class(value, classes):
    """
    Add Tailwind CSS classes to an existing class attribute.

    Usage:
        <div class="{{ existing_classes|tailwind_class:'bg-blue-500 text-white' }}">
    """
    if value:
        return f"{value} {classes}"
    return classes

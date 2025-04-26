"""
Tests for the template tags in the strynova_dj_tailwindcss package.
"""
from django.test import TestCase
from django.template import Context, Template


class TailwindTagsTests(TestCase):
    """
    Tests for the Tailwind CSS template tags.
    """

    def test_tailwind_css_tag(self):
        """
        Test that the tailwind_css tag renders correctly.
        """
        template = Template("{% load tailwind_tags %}{% tailwind_css %}")
        rendered = template.render(Context({}))
        self.assertIn("tailwindcss", rendered)
        self.assertIn("rel=\"stylesheet\"", rendered)


    def test_tailwind_class_filter(self):
        """
        Test that the tailwind_class filter adds classes correctly.
        """
        template = Template("{% load tailwind_tags %}{{ 'existing-class'|tailwind_class:'bg-blue-500' }}")
        rendered = template.render(Context({}))
        self.assertEqual(rendered, "existing-class bg-blue-500")

        # Test with empty value
        template = Template("{% load tailwind_tags %}{{ ''|tailwind_class:'bg-blue-500' }}")
        rendered = template.render(Context({}))
        self.assertEqual(rendered, "bg-blue-500")

        # Test with None value
        template = Template("{% load tailwind_tags %}{{ none_value|tailwind_class:'bg-blue-500' }}")
        rendered = template.render(Context({'none_value': None}))
        self.assertEqual(rendered, "bg-blue-500")

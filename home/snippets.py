from __future__ import unicode_literals
from wagtail.wagtailsnippets.models import register_snippet
from django.db import models

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=55)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

@register_snippet
class Teammate(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    initial_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    secondary_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('initial_photo'),
        ImageChooserPanel('secondary_photo'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name

@register_snippet
class Address(models.Model):
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    language_code = models.CharField(max_length=2)

    panels = [
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('address'),
        FieldPanel('language_code')
    ]

    def __str__(self):
        return self.address

from __future__ import unicode_literals
from wagtail.wagtailsnippets.models import register_snippet
from django.db import models

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel

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

@register_snippet
class FooterService(models.Model):
    service_title = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    COUNTRY_CHOICES = (
        ('en','en'),
        ('bg','bg'),
        ('ro', 'ro'),
        )
    language_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='en')
    panels = [
        FieldPanel('service_title'),
        PageChooserPanel('link_page'),
        FieldPanel('language_code'),
    ]

    def __str__(self):
        return self.service_title

@register_snippet
class FooterNew(models.Model):
    news_title = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    COUNTRY_CHOICES = (
        ('en','en'),
        ('bg','bg'),
        ('ro', 'ro'),
        )
    language_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='en')
    panels = [
        FieldPanel('news_title'),
        PageChooserPanel('link_page'),
        FieldPanel('language_code'),
    ]

    def __str__(self):
        return self.news_title

@register_snippet
class FooterContactU(models.Model):
    contact_us_title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    COUNTRY_CHOICES = (
        ('en','en'),
        ('bg','bg'),
        ('ro', 'ro'),
        )
    language_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='en')
    panels = [
        FieldPanel('contact_us_title'),
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('mail'),
        FieldPanel('language_code'),
    ]

    def __str__(self):
        return self.contact_us_title

# @register_snippet
# class FooterTitles(models.Model):
#     services = models.CharField(max_length=255)
#     latest_news = models.CharField(max_length=255)

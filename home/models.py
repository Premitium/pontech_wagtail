from __future__ import absolute_import, unicode_literals

from django.db import models
from django import forms
import django

from wagtail.wagtailcore.models import Page, Orderable
from wagtailtrans.models import TranslatablePage
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, \
    FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, \
    MultiFieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel, \
    TabbedInterface, ObjectList
from wagtail.wagtailsearch import index
from datetime import datetime

from .snippets import Category, Teammate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'),
        ('mid', 'Mid width'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"

class DemoStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    api_fields = ['link_external', 'link_page', 'link_document']

    class Meta:
        abstract = True


class HomePage(TranslatablePage, Page):
    body = StreamField(DemoStreamBlock())

    search_fields = Page.search_fields + [
        index.SearchField('body', classname="full"),
    ]

    title_featured_service = models.CharField(max_length=255,
        help_text="Featured services title", default="Why choose Pontech")

    title_partners = models.CharField(max_length=255,
        help_text="Partners title", default="Our Partners")

    title_about_us = models.CharField(max_length=255,
    help_text="About us faq title", default="About Us")

    title_testimonials = models.CharField(max_length=255,
    help_text="Testimonials title", default="Testimonials")

    api_fields = ['body', 'carousel_items', 'related_links',
        'title_featured_service', 'title_about_us',
        'title_partners', 'feature_service_title', 'title_testimonials']

    class Meta:
        verbose_name = "Homepage"

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('carousel_items', label="Carousel items"),
        InlinePanel('related_links', label="Related links"),
        FieldPanel('title_featured_service', classname="Featured services title"),
        InlinePanel('featured_service_items', label="Featured service"),
        InlinePanel('what_we_do_items', label="What we do"),
        FieldPanel('title_partners', classname="Partners title"),
        InlinePanel('partners_items', label="Our Partners"),
        FieldPanel('title_about_us', classname="About us faq title"),
        InlinePanel('about_us_home', label="About us"),
        InlinePanel('about_us_accoridon', label="About us accordion"),
        FieldPanel('title_testimonials', classname="Testimonials title"),
        InlinePanel('testimonials', label="Testimonials"),
    ]

    # def get_context(self, request):
    #     context = super(HomePage, self).get_context(request)
    #     # import ipdb; ipdb.set_trace()
    #     hpo = HomePageAboutUsHome.objects.all()
    #     for hp in hpo:
    #         # import ipdb; ipdb.set_trace()
    #     return context



# Related links

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['title'] + LinkFields.api_fields

    class Meta:
        abstract = True

 # Carousel items

class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['image', 'embed_url', 'caption'] + LinkFields.api_fields

    class Meta:
        abstract = True

# Home Page

class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('home.HomePage', related_name='carousel_items')

class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.HomePage', related_name='related_links')

#Featured Service

class FeaturedServiceItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    icon_graphic = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    icon_graphic_text = models.CharField(max_length=255, blank=True)
    embed_url = models.URLField("Embed URL", blank=True)
    text = models.TextField(blank=True)


    caption = models.CharField(max_length=255, blank=True)


    panels = [
        ImageChooserPanel('image'),
        ImageChooserPanel('icon_graphic'),
        FieldPanel('icon_graphic_text'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        FieldPanel('text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['image', 'icon_graphic', 'icon_graphic_text',
        'embed_url', 'caption', 'text'] + LinkFields.api_fields

    class Meta:
        abstract = True

#Featured Service Pontech section

class FeaturedServicePontechItem(Orderable, FeaturedServiceItem):
    page = ParentalKey('home.HomePage', related_name='featured_service_items')

#What we do

class WhatWeDoItem(LinkFields):
    #Part valid only for the title and sub text.
    section_title = models.CharField(max_length=255, blank=True)
    section_text = models.TextField(blank=True)

    #Part valid for the repeater Part
    caption = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)

    icon_graphic_text = models.CharField(max_length=255, blank=True)
    embed_url = models.URLField("Embed URL", blank=True)

    panels = [
        FieldPanel('section_title'),
        FieldPanel('section_text'),
        FieldPanel('icon_graphic_text'),
        FieldPanel('caption'),
        FieldPanel('text'),
        FieldPanel('embed_url'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['section_title', 'section_text', 'icon_graphic_text',
    'caption', 'text', 'embed_url' ] + LinkFields.api_fields

    class Meta:
        abstract = True

class WhatWeDoPontechItem(Orderable, WhatWeDoItem):
    page = ParentalKey('home.HomePage', related_name='what_we_do_items')

#Our Partners
class PartnersItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    tooltip = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('tooltip'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['image', 'embed_url', 'tooltip'] + LinkFields.api_fields

    class Meta:
        abstract = True

#Partners home page binding
""" partners_items is the varible that you use in the template to show
    the data.
    In the html file include this
    {% include "home/includes/partners.html" with partners_items=self.partners_items.all only%}"""

class PartnersPontechItem(Orderable, PartnersItem):
    page = ParentalKey('home.HomePage', related_name='partners_items')


class AboutUsHome(LinkFields):
    paragraph_title = models.CharField(max_length=255)
    paragraph_text = StreamField(DemoStreamBlock())
    button_text = models.CharField(max_length=20)

    panels = [
        FieldPanel('paragraph_title'),
        StreamFieldPanel('paragraph_text'),
        FieldPanel('button_text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['paragraph_title', 'paragraph_text', 'button_text'] + LinkFields.api_fields

    class Meta:
        abstract = True

class HomePageAboutUsHome(Orderable, AboutUsHome):
    page = ParentalKey('home.HomePage', related_name='about_us_home')

class AboutUsAccordion(LinkFields):
    accordion_title = models.CharField(max_length=255)
    accordion_text = StreamField(DemoStreamBlock())

    panels = [
        FieldPanel('accordion_title'),
        StreamFieldPanel('accordion_text'),
    ]

    class Meta:
        abstract = True


class HomePageAccordion(Orderable, AboutUsAccordion):
    page = ParentalKey('home.HomePage', related_name='about_us_accoridon')


class Testimonials(LinkFields):
    testi_person = models.CharField(max_length=255)
    testi_city = models.CharField(max_length=255)
    testi_text = StreamField(DemoStreamBlock())

    panels = [
        FieldPanel('testi_person'),
        FieldPanel('testi_city'),
        StreamFieldPanel('testi_text'),
    ]

    class Meta:
        abstract = True

class HomePageTestimonials(Orderable, Testimonials):
    page = ParentalKey('home.HomePage', related_name='testimonials')


class BlogPostsPage(TranslatablePage, Page):
    header_text = models.CharField(max_length=255)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        ImageChooserPanel('header_image'),
    ]

    subpage_types = ['home.BlogPost']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        language_separated_blogs = []
        context = super(BlogPostsPage, self).get_context(request)
        blogpages = BlogPost.objects.all().live().order_by('-first_published_at')
        # blogpages = self.get_children().live().order_by('-first_published_at')
        #take the language from the request
        language_code = request.LANGUAGE_CODE
        #filter blogposts by language_id
        for blog in blogpages:
            if blog.language.code == language_code:
                language_separated_blogs.append(blog)

        paginator = Paginator(language_separated_blogs, 6)

        page = request.GET.get('page')
        try:
            language_separated_blogs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            language_separated_blogs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            language_separated_blogs = paginator.page(paginator.num_pages)

        context['blogpages'] = language_separated_blogs
        return context


class BlogPost(TranslatablePage, Page):
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    blog_title = models.CharField(max_length=255)
    blog_title_short = models.CharField(max_length=255, blank=True)
    blog_text = StreamField(DemoStreamBlock())
    category = ParentalManyToManyField(Category)
    blog_authors = ParentalManyToManyField(Teammate)
    date = models.DateTimeField(default=django.utils.timezone.now, blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover_image'),
        FieldPanel('blog_title'),
        FieldPanel('blog_title_short'),
        StreamFieldPanel('blog_text'),
        FieldPanel('category'),
        FieldPanel('blog_authors'),
        FieldPanel('date')
    ]

    parent_page_types = ['home.BlogPostsPage']

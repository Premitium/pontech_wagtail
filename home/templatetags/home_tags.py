import re
from datetime import date
from django import template
from django.conf import settings

from home.models import Page, BlogPostsPage
from home.snippets import Address, FooterService, FooterNew, FooterContactU
# from blog.models import BlogPage
register = template.Library()


# settings value
@register.assignment_tag
def get_google_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_KEY', "")


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    try:
        result = context['request'].site.root_page
    except KeyError:
        result = context['calling_page'].get_url_parts()[1]
    return result


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('home/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    request = context['request']
    language_code = request.LANGUAGE_CODE
    # menuitems = parent.get_children().live().in_menu().filter(title = language_code)
    menuitems = parent.get_children().live().in_menu().filter(title = language_code)[0].get_children()

    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.path.startswith(menuitem.path)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('home/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves all live pages which are children of the calling page
#for standard index listing
@register.inclusion_tag(
    'home/tags/standard_index_listing.html',
    takes_context=True
)
def standard_index_listing(context, calling_page):
    pages = calling_page.get_children().live()
    return {
        'pages': pages,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Person feed for home page
@register.inclusion_tag(
    'home/tags/person_listing_homepage.html',
    takes_context=True
)
def person_listing_homepage(context, count=2):
    people = PersonPage.objects.live().order_by('?')
    return {
        'people': people[:count].select_related('feed_image'),
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Blog feed for home page
@register.inclusion_tag(
    'home/tags/blog_listing_homepage.html',
    takes_context=True
)
def blog_listing_homepage(context, count=2):
    blogs = BlogPostsPage.objects.live().order_by('-date')
    return {
        'blogs': blogs[:count].select_related('feed_image'),
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Events feed for home page
@register.inclusion_tag(
    'home/tags/event_listing_homepage.html',
    takes_context=True
)
def event_listing_homepage(context, count=2):
    events = EventPage.objects.live()
    events = events.filter(date_from__gte=date.today()).order_by('date_from')
    return {
        'events': events[:count].select_related('feed_image'),
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Advert snippets
@register.inclusion_tag('home/tags/adverts.html', takes_context=True)
def adverts(context):
    return {
        'adverts': Advert.objects.select_related('page'),
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 3:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=3)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }

@register.inclusion_tag('home/tags/latest_news.html', takes_context=True)
def latest_news(context):
    blogs = []
    result = []
    request = context['request']
    language_code = request.LANGUAGE_CODE
    blog_posts = Page.objects.type(BlogPostsPage)

    for blog_group in blog_posts:
        lang_title = blog_group.get_parent().title
        if lang_title == language_code:
            blogs += blog_group.get_children().order_by('-first_published_at')
            for blog in blogs:
                result.append(blog.blogpost)

    return{
        'latest_news': result,
        'request': context['request'],
    }

@register.inclusion_tag('home/tags/latest_news_feed.html', takes_context=True)
def latest_news_feed(context):
    #print(dir(blogs[0]))
    blogs = []
    result = []
    request = context['request']
    language_code = request.LANGUAGE_CODE
    blog_posts = Page.objects.type(BlogPostsPage)

    for blog_group in blog_posts:
        lang_title = blog_group.get_parent().title
        if lang_title == language_code:
            blogs += blog_group.get_children().order_by('-first_published_at')[:3]
            for blog in blogs:
                result.append(blog.blogpost)

    return{
        'latest_news_feed': result,
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/language_selector.html', takes_context=True)
def language_selector(context):
    page = context['calling_page']
    return{
        'page': page,
        'request': context['request'],
    }

# Address snippets
@register.inclusion_tag('home/tags/address.html', takes_context=True)
def address(context):
    request = context['request']
    language_code = request.LANGUAGE_CODE
    return {
        'address': Address.objects.all().filter(language_code = language_code),
        'request': request,
    }

@register.inclusion_tag('home/tags/go_back_to_index.html', takes_context=True)
def go_to_index(context, parent, calling_page):
    try:
        page = context['calling_page']
    except KeyError:
        page = calling_page

    index_url = page.get_url_parts()[1] +'/'+page.language.code+'/'

    return{
        'index_url': index_url
    }


@register.inclusion_tag('home/tags/footer_tag.html', takes_context=True)
def footer_tag(context, parent, calling_page):
    request = context['request']
    language_code = request.LANGUAGE_CODE

    #Services for the footer
    services = FooterService.objects.all().filter(language_code=language_code)

    for service in services:
        service.__dict__['full_url'] = service.link_page.get_full_url()

    #Latest news for the footer
    news_all = FooterNew.objects.all().filter(language_code=language_code)

    for news in news_all:
        news.__dict__['full_url'] = news.link_page.get_full_url()
        news.__dict__['date_posted'] = news.link_page.blogpost.date

    #Contacts for the footer
    contact = FooterContactU.objects.all().filter(language_code=language_code).first()

    return {
        'calling_page': calling_page,
        'services': services,
        'news_all': news_all,
        'contact': contact
        }

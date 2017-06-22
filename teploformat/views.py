import os
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import requires_csrf_token
from django import http
from django.template import Context, Engine, TemplateDoesNotExist, loader
from shop.catalogue.models import Category


@requires_csrf_token
def page_not_found_with_site_templates(request):

    site = get_current_site(request)
    site_template = site.config.template

    base_template_name = os.path.join(
        site_template,
        'base.html'
    )

    side_menu = {
        cat: [descendant for descendant in cat.get_descendants()] for cat in
        Category.objects.filter(site=site) if cat.is_root()}

    context = {
        'request_path': request.path,
        'base_template_name': base_template_name,
        'site_template': site_template,
        'side_menu': side_menu
    }

    try:
        template = loader.get_template('404.html')
        body = template.render(context, request)
        content_type = None             # Django will use DEFAULT_CONTENT_TYPE
    except TemplateDoesNotExist:
        template = Engine().from_string(
            '<h1>Not Found</h1>'
            '<p>The requested URL {{ request_path }} '
            'was not found on this server.</p>')
        body = template.render(Context(context))
        content_type = 'text/html'
    return http.HttpResponseNotFound(body, content_type=content_type)

from django import template
from django.db import connection
from menu_app.models import MenuItem
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


def render_menu(items, current_url):
    menu_html = '<ul>'
    for item in items:
        menu_html += '<li>'
        i_url = item['url'] if item['url'].startswith('/') else reverse(
            item['url'])
        menu_html += f'<a href="{i_url}">{item["name"]}</a>'
        if 'child_menu' in item:
            menu_html += render_menu(item['child_menu'], current_url)
        menu_html += '</li>'
    menu_html += '</ul>'
    return menu_html


def build_tree(tree_list, current_url, parent_id=None):
    menu_tree = list()
    for item in tree_list:
        if item['parent_id'] == parent_id:
            children = build_tree(tree_list, current_url, item['id'])
            if children and (item['url'] in current_url):
                item['child_menu'] = children
            menu_tree.append(item)
    return menu_tree


@register.simple_tag(takes_context=True)
def draw_menu(context, name):
    request = context['request']
    current_url = request.path
    menu_items = MenuItem.objects.filter(menu__title=name)
    menu_items_list = [item for item in menu_items.values()]
    tree = build_tree(menu_items_list[:], current_url)
    print("Количество обращений к БД: ", len(connection.queries))
    return mark_safe(render_menu(tree, current_url))

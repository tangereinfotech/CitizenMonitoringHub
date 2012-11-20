from django import template

register = template.Library()

@register.filter
def col_number(val):
   return val

@register.filter
def col_name(val,dict):
   return dict[val]['name']

@register.filter
def col_code(val,dict):
   return dict[val]['code']

@register.filter
def col_search_description_name(val,dict):
   return dict[val]['search_str']

@register.filter
def col_type(val,dict):
   return dict[val]['type']

@register.filter
def is_col_searchable(val, dict):
    if (dict[val]['searchable'] == True):
        return 'true'
    else:
        return 'false'

@register.filter
def is_col_sortable(val, dict):
    if (dict[val]['sortable'] == True):
        return 'true'
    else:
        return 'false'

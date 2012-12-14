from django import template

register = template.Library()

@register.filter
def col_number(val):
   return val

@register.filter
def col_sort_number(val,dict):
    if 'sort_col' in dict[val]:
        return dict[val]['sort_col']
    else:
        return val

@register.filter
def col_name(val,dict):
   return dict[val]['name']

@register.filter
def col_width(val,dict):
   return dict[val]['width']

@register.filter
def col_class(val,dict):
   return dict[val]['sClass']

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

@register.filter
def is_type_input(val,dict):
    if (dict[val]['inputtype'] == 'input'):
        return 'true'
    else:
        return 'false'

@register.filter
def is_type_select(val,dict):
    if (dict[val]['inputtype'] == 'select'):
        return 'true'
    else:
        return 'false'

@register.filter
def select_option(val,dict):
    return dict[val]['select_option']()

@register.filter
def is_col_visible(val, dict):
    if (dict[val]['bVisible'] == True):
        return 'true'
    else:
        return 'false'


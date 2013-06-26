from django import template

from myjobs.templatetags import form_tags

register = template.Library()

@register.filter(name='process_field_types')
def process_field_types(item):
    """
    Pretty-formats model fields based on field type.

    Inputs:
    :item: Instance of a ProfileUnit subclass (Name, SecondaryEmail, etc)

    Outputs:
    :fields: List of lists containing the field label, pretty-formatted value,
        and field type
    """
    fields = item.get_fields()

    for field in fields:
        if field[2] == 'DateField':
            field[1] = template.defaultfilters.date(field[1])
        else:
            field[1] = form_tags.readable_boolean(field[1])
    return fields

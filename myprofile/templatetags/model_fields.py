from django.template import defaultfilters, loader, Library

from myjobs.templatetags import form_tags

register = Library()


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
            field[1] = defaultfilters.date(field[1])
        else:
            field[1] = form_tags.readable_boolean(field[1])
    return fields


@register.filter(name='custom_template')
def custom_template(module):
    """
    Checks to see if there is a custom template for module's fields on profile
    page

    Inputs:
    :module:    module instance (ProfileUnit)

    Outputs:
                Custom template location if exists otherwise returns None for
                boolean check reasons.
    """
    m_type = module.content_type.name
    try:
        loaded = loader.get_template('myprofile/modules/%s.html' % m_type)
        if loaded:
            return 'myprofile/modules/%s.html' % m_type
    except loader.TemplateDoesNotExist:
        return None
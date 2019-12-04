# -*- coding: utf-8 -*-
from collections import OrderedDict
from plone.restapi.serializer.converters import IJsonCompatible
from plone.restapi.types.interfaces import IJsonSchemaProvider
from plone.restapi.types.utils import get_jsonschema_for_portal_type
from Products.PloneFormGen.content.fields import FGFieldsetEnd
from Products.PloneFormGen.content.fields import FGFieldsetStart
from Products.PloneFormGen.interfaces import IPloneFormGenFieldset
from Products.PloneFormGen.widgets import FieldsetEndWidget
from Products.PloneFormGen.widgets import FieldsetStartWidget
from zope.component import queryMultiAdapter


def get_jsonschema_properties(form, request, prefix="", excluded_fields=None):
    """Build a JSON schema 'properties' list, based on a list of fieldset
    dicts as returned by `get_fieldsets()`.
    """
    properties = OrderedDict()
    if excluded_fields is None:
        excluded_fields = []

    properties = OrderedDict()

    for field in form.fgFields():
        fieldname = field.getName()
        if fieldname not in excluded_fields:
            # We need to exclude also the fieldset start and fieldset end fields
            field_object = form.get(fieldname)

            if (not isinstance(field_object, FGFieldsetStart)) and (
                not isinstance(field_object, FGFieldsetEnd)
            ):

                adapter = queryMultiAdapter(
                    (field_object, form, request),
                    interface=IJsonSchemaProvider,
                    name=field.__name__,
                )

                adapter = queryMultiAdapter(
                    (field_object, form, request), interface=IJsonSchemaProvider
                )

                adapter.prefix = prefix
                if prefix:
                    fieldname = ".".join([prefix, fieldname])

                properties[fieldname] = adapter.get_schema()

    return properties


def get_json_schema_for_form_contents(form, request, excluded_fields=None):

    # Build JSON schema properties
    properties = get_jsonschema_properties(
        form, request, excluded_fields=excluded_fields
    )

    # Determine the fieldset
    fieldsets = [{"id": "default", "title": "Default", "fields": properties.keys()}]

    # Determine required fields
    required = []
    for fieldname, fieldproperties in properties.items():
        if fieldproperties.get("required"):
            required.append(fieldname)
        del fieldproperties["required"]

    return {
        "type": "object",
        "title": form.Title(),
        "properties": IJsonCompatible(properties),
        "required": required,
        "fieldsets": fieldsets,
    }

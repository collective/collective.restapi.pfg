# -*- coding: utf-8 -*-
from collective.restapi.pfg import _
from plone.restapi.types.interfaces import IJsonSchemaProvider
from Products.PloneFormGen.content.fields import BaseFormField
from Products.PloneFormGen.content.fields import FGBooleanField
from Products.PloneFormGen.content.fields import FGFileField
from Products.PloneFormGen.content.fields import FGIntegerField
from Products.PloneFormGen.content.fields import FGSelectionField
from Products.PloneFormGen.content.fields import FGStringField
from Products.PloneFormGen.content.fields import FGTextField
from Products.PloneFormGen.content.fields import StringVocabularyField
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface


try:
    from cs.pfg.multifile.content.formmultifilefield import FormMultiFileField
except ImportError:
    FormMultiFileField = None


@adapter(BaseFormField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class DefaultJsonSchemaProvider(object):
    def __init__(self, field, context, request):
        self.field = field
        self.context = context
        self.request = request

    def additional(self):
        """Additional info for field."""
        return {}

    def get_title(self):
        # return self.field.widget.Label(self.field)
        return self.field.Title()

    def get_description(self):
        # return self.field.widget.Description(self.field)
        return self.field.Description()

    def is_required(self):
        return self.field.fgField.required

    def get_schema(self):
        """Get jsonschema for field.

        You should override `additional` method to provide more properties
        about the field."""
        schema = {
            "type": self.get_type(),
            "title": self.get_title(),
            "description": self.get_description(),
            "required": self.is_required(),
        }

        widget = self.get_widget()
        if widget:
            schema["widget"] = widget

        widget_options = self.get_widget_params()
        if widget_options:
            schema["widgetOptions"] = widget_options

        schema.update(self.additional())
        return schema

    def get_type(self):
        raise NotImplementedError

    def get_widget(self):
        return None

    def get_widget_params(self):
        return []


@adapter(FGStringField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FGStringFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "string"


@adapter(FGIntegerField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FGIntegerFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "number"


@adapter(FGTextField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FGTextFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "string"

    def get_widget(self):
        return "textarea"

    def additional(self):
        if self.field.fgField.widget.maxlength:
            return {"maxLength": int(self.field.fgField.widget.maxlength)}


@adapter(FGSelectionField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FGSelectionFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "string"

    def additional(self):
        display_list = self.field.fgField.Vocabulary(self.context)
        return {
            "choices": list(display_list.items()),
            "enum": [i[0] for i in display_list.items()],
            "enumNames": [i[1] for i in display_list.items()],
        }


@adapter(FGBooleanField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FGBooleanFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "boolean"


@adapter(FGFileField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FGFileFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "object"

    def additional(self):
        display_list = self.field.Vocabulary(self.field.aq_parent)
        return {
            "properties": {
                "{}.contentType".format(self.field.fgField.getName()): {
                    "default": "",
                    "description": _("The content type identifies the type of data."),
                    "title": "Content Type",
                    "type": "string",
                },
                "{}.data".format(self.field.fgField.getName()): {
                    "default": "",
                    "description": _(u"The actual content of the object."),
                    "title": "Data",
                    "type": "string",
                },
                "{}.filename".format(self.field.fgField.getName()): {
                    "description": "",
                    "title": "Filename",
                    "type": "string",
                },
            }
        }


# XXX This adapter should go away from here
@adapter(FormMultiFileField, Interface, Interface)
@implementer(IJsonSchemaProvider)
class FormMultiFileFieldJsonSchemaProvider(DefaultJsonSchemaProvider):
    def get_type(self):
        return "array"

    def additional(self):

        return {
            "additionalItems": True,
            "default": [],
            "items": {
                "type": "object",
                "title": "",
                "description": "",
                "properties": {
                    "{}.contentType".format(self.field.fgField.getName()): {
                        "default": "",
                        "description": _(
                            "The content type identifies the type of data."
                        ),
                        "title": "Content Type",
                        "type": "string",
                    },
                    "{}.data".format(self.field.fgField.getName()): {
                        "default": "",
                        "description": _(u"The actual content of the object."),
                        "title": "Data",
                        "type": "string",
                    },
                    "{}.filename".format(self.field.fgField.getName()): {
                        "description": "",
                        "title": "Filename",
                        "type": "string",
                    },
                },
            },
        }

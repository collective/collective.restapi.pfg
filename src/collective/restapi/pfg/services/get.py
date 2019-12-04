# -*- coding: utf-8 -*-
from collective.restapi.pfg.serializers.utils import get_json_schema_for_form_contents
from plone.restapi.services import Service


class PloneFormGenSchemaGet(Service):
    def reply(self):
        result = get_json_schema_for_form_contents(self.context, self.request)
        self.content_type = "application/json+schema"
        return result

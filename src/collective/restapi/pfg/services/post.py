# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from ZPublisher.HTTPRequest import FileUpload
from StringIO import StringIO


class PloneFormGenPost(Service):
    def reply(self):
        data = json_body(self.request)

        self.request.form = self.process_form(data)
        self.context.fgProcessActionAdapters(
            errors=[], fields=None, REQUEST=self.request
        )
        self.request.response.setStatus(201)

    def process_form(self, data):
        data = self.fix_attachments(data)
        return data

    def fix_attachments(self, data):
        # XXX dirty way to fix file uploads
        if "adjuntos" in data:
            items = []
            for item in data["adjuntos"]:
                if isinstance(item, FileUpload):
                    # Element comes as a standard FileUpload
                    items.append(item)
                else:
                    # Element comes as plone.restapi file representation
                    # dict, with 'filename', 'content_type' and 'data' keys
                    items.append(FileUpload(Item(item)))

            data["adjuntos"] = items

        return data


class Item:
    def __init__(self, data_dict):
        self.filename = data_dict.get("filename", "")
        self.headers = {
            "content-type": data_dict.get("content_type"),
            "size": data_dict.get("size"),
        }
        self.file = StringIO(data_dict.get("data").decode(data_dict.get("encoding")))

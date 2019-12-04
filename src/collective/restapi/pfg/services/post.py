# -*- coding: utf-8 -*-
from plone.restapi.services import Service


class PloneFormGenPost(Service):
    def reply(self):
        self.request.response.setStatus(501)
        return dict(error=dict(message="Not Implemented Yet"))

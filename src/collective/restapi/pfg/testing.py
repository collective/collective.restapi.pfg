# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.restapi.pfg


class CollectiveRestapiPfgLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        import Products.PloneFormGen

        self.loadZCML(package=Products.PloneFormGen)
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.restapi.pfg)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.restapi.pfg:default")


COLLECTIVE_RESTAPI_PFG_FIXTURE = CollectiveRestapiPfgLayer()


COLLECTIVE_RESTAPI_PFG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RESTAPI_PFG_FIXTURE,),
    name="CollectiveRestapiPfgLayer:IntegrationTesting",
)


COLLECTIVE_RESTAPI_PFG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RESTAPI_PFG_FIXTURE,),
    name="CollectiveRestapiPfgLayer:FunctionalTesting",
)


COLLECTIVE_RESTAPI_PFG_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_RESTAPI_PFG_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveRestapiPfgLayer:AcceptanceTesting",
)

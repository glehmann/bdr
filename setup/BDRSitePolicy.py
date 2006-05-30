from Products.CMFPlone.Portal import addPolicy
from Products.CMFPlone.interfaces.CustomizationPolicy import ICustomizationPolicy
from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy

class BDRSitePolicy(DefaultCustomizationPolicy):
    """ Customizes a fresh Plone Site """
    __implements__ = ICustomizationPolicy

    availableAtConstruction = 1

    def customize(self,portal):
        pass # customization code goes here

def register(context, app_state):
    addPolicy('BDR Site',BDRSitePolicy())
    
    

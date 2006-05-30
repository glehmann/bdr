from Products.CMFCore.permissions import ListPortalMembers
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from AccessControl.Permissions import take_ownership

def membreParId(self,idMembre):
	if _checkPermission(ListPortalMembers,self):
		return self.portal_membership.getMemberById(idMembre)
	else:
		return None
	    
def devenirRedacteur(self):
	# l'utilisateur courant devient proprietaire de l'objet courant
	if _checkPermission(take_ownership,self):
		portal_membership= getToolByName(self, 'portal_membership')
        	currentUser = portal_membership.getAuthenticatedMember().getId()
	
		plone_utils= getToolByName(self, 'plone_utils')
        	plone_utils.changeOwnershipOf(self,currentUser)
        	catalog_tool = getToolByName(self, 'portal_catalog')
		catalog_tool.reindexObject(self)
		return True
	else:
		raise Unauthorized
	
def peutDevenirRedacteur(self):
	# si l'utilisateur courant peut devenir proprietaire de l'objet courant
	portal_membership= getToolByName(self, 'portal_membership')
        currentUser = portal_membership.getAuthenticatedMember()
	
	if _checkPermission(take_ownership,self):
		if not(currentUser.has_role(['Owner'],self)):
			return 1
		else:
			# retourne 2 si il est deja proprietaire
			return 2
	return 0
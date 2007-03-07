from Products.CMFCore.permissions import ListPortalMembers
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from AccessControl.Permissions import take_ownership


def devenirRedacteur(self):
	""" l'utilisateur courant devient proprietaire de l'objet courant (self) """
	if self.peutDevenirRedacteur(): # verifie qu'il est autorise
		
		# retrouve le nom de l'utilisateur
		portal_membership= getToolByName(self, 'portal_membership')
        	currentUser = portal_membership.getAuthenticatedMember().getId()
		
		# change le proprietaire
		plone_utils= getToolByName(self, 'plone_utils')
        	plone_utils.changeOwnershipOf(self,currentUser)
		
		#  reindexe l'objet
        	catalog_tool = getToolByName(self, 'portal_catalog') 
		catalog_tool.reindexObject(self)
		return True
	else:
		raise Unauthorized
	
def peutDevenirRedacteur(self):
	""" si l'utilisateur courant peut devenir proprietaire de l'objet courant"""
	portal_membership= getToolByName(self, 'portal_membership')
        currentUser = portal_membership.getAuthenticatedMember()
	
	
	if not _checkPermission(take_ownership,self):
		return 0
	if not hasattr(self,"archetype_name"):
		return 0
	if not self.archetype_name in ["Document","Event","Favorite","Page","News Item","Favorite"]:
		""" on ne peut prendre la propriete que de ces types """
		return 0
	if not(currentUser.has_role(['Owner'],self)):
		return 1
	else:
		# retourne 2 si il est deja proprietaire
		return 2

def membreParId(self,idMembre):
	if _checkPermission(ListPortalMembers,self):
		return self.portal_membership.getMemberById(idMembre)
	else:
		return None
	

def listeGroupesIntranetUtilisateur(self):
	""" renvoit la liste des noms des zones intranet dont l'utilisateur est membre """
	listeObjetsIntranetUtilisateur = []
	
	try:
		
		userId = self.portal_membership.getAuthenticatedMember().getId()
		
		# la liste des ids des groupes de l'utilisateur
		userGroupIdsList = [group.getId() for group in self.portal_groups.getGroupsByUserId(userId)]
		
		# l'ensemble des zones intranet... (et leurs enfants)
		listeObjetsIntranet = [folderIntranet for folderIntranet in self.Intranet.listFolderContents() if hasattr(folderIntranet,'groupeIntranet')]
		
		# dont le groupe intranet correspond a un des groupes de l'utilisateur
		listeObjetsIntranetUtilisateur = [zoneIntranet for zoneIntranet in listeObjetsIntranet if "group_"+zoneIntranet.groupeIntranet in userGroupIdsList]
	
	
	except Unauthorized:
		pass
	
	return listeObjetsIntranetUtilisateur

def equipeUtilisateur(self):
	""" renvoit le le repertoire de l'equipe de l'utilisateur """ 
	try:
		userId = self.portal_membership.getAuthenticatedMember().getId()
		
		userGroupIdsList = [group.getId() for group in self.portal_groups.getGroupsByUserId(userId)]
		
		#verifie pour chaque sous repertoire du repertoire equipes
		for zoneEquipe in \
		   [objetEquipe for objetEquipe in self.equipes.listFolderContents() if hasattr(objetEquipe,'groupeEquipe')]:
			# s'il correspond a un des groupes de l'utilisateur
			if "group_"+zoneEquipe.groupeEquipe in userGroupIdsList:
				return zoneEquipe
		
		return False
		
	except Unauthorized: # erreur de securite
		return False

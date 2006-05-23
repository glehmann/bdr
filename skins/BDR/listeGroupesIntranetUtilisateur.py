## Script (Python) "listeGroupesIntranetUtilisateur"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# renvoie la liste des noms des zones intranet dont l'utilisateur est membre

listeObjetsIntranetUtilisateur = []

try:

   userId = context.portal_membership.getAuthenticatedMember().getId()

   # la liste des ids des groupes de l'utilisateur
   userGroupIdsList = [group.getId() for group in context.portal_groups.getGroupsByUserId(userId)]

   # l'ensemble des zones intranet... (et leurs enfants)
   listeObjetsIntranet = [folderIntranet for folderIntranet in context.intranet.listFolderContents() if hasattr(folderIntranet,'groupeIntranet')]
   
   # dont le groupe intranet correspond a un des groupes de l'utilisateur
   listeObjetsIntranetUtilisateur = [zoneIntranet for zoneIntranet in listeObjetsIntranet if "group_"+zoneIntranet.groupeIntranet in userGroupIdsList]



except:
   pass

return listeObjetsIntranetUtilisateur

## Script (Python) "equipeUtilisateur"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=nom de l'equipe de l'utilisateur
##
# renvoie le nom de l'equipe dont l'utilisateur authentifie est membre
# présuppose une équipe maximum par utilisateur

if 1:
   userId = context.portal_membership.getAuthenticatedMember().getId()

   userGroupIdsList = [group.getId() for group in context.portal_groups.getGroupsByUserId(userId)]

   #verifie pour chaque sous repertoire du repertoire equipes
   for zoneEquipe in [objetEquipe for objetEquipe in context.equipes.listFolderContents() if hasattr(objetEquipe,'groupeEquipe')]:
         # s'il correspond a un des groupes de l'utilisateur
         if "group_"+zoneEquipe.groupeEquipe in userGroupIdsList:
            return zoneEquipe

   return False

else: # erreur de securite
   return False

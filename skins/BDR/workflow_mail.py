## Script (Python) "workflow_mail"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change,nomTransition
##title=mail de workflow
##
# cree un mail de notification
# prend en argument un state_change (objet transition)
# est appele depuis un script de notification



if str(state_change).startswith("<Products.DCWorkflow.Expression.StateChangeInfo instance"):

   # ############ infos sur la transition


   # texte de la transition

   texteTransitionDico = {"accepter_internet":"a accepte la publication de",
   "demander_internet":"a soumis pour publication le document",
   "refuser_internet":"a refusé la publication du document",
   "remettre_intranet_moderation":"a remis sur intranet par modération le document",
   "reserver_moderation":"a masqué par moderation le document",
   "demander_internet_dossier":"demande l'affichage du dossier",
   "refuser_internet_dossier":"a refuse l'affichage du dossier",
   "remettre_intranet_moderation_dossier":"a masque par moderation le dossier",
   "accepter_internet":"a accepte l'affichage du dossier"}
   
   if texteTransitionDico.has_key(nomTransition):
      texteTransition = texteTransitionDico[nomTransition]
   else:
      texteTransition = "a effectue "+nomTransition+" sur le document"
   

   # roles destinataires de la transition

   if nomTransition in ["demander_internet","demander_internet_dossier"]:
      listeRolesDestinataires = ["Owner","Reviewer"]
   
   else:
      listeRolesDestinataires = ["Owner"]
 
   object = state_change.object
   utilisateur = context.portal_membership.getAuthenticatedMember()
   administratorEmailAddress = object.email_from_address




   # ########## cree la liste des destinataires

   userList = []
   groupList = []

   for user, roles, type, name in object.plone_utils.getInheritedLocalRoles(object) + object.acl_users.getLocalRolesForDisplay(object):

      for roleDestinataires in [role for role in roles if role in listeRolesDestinataires]:
         if type == 'user':
            if name not in userList :
               userList.append(name)
         elif type == 'group':
            group = object.portal_groups.getGroupById(user)
            if group not in groupList:
               groupList.append(group)
            for userGroup in group.getGroupMembers():
               if name not in userList :
                  userList.append(userGroup.getId())
         break

   strListeMailsDestinataires = ""
   strListeMailsGroupes = ""

   for name in userList :
      user = context.membreParId(name)
      if user and user.email:
         strListeMailsDestinataires += user.email+", "

   for groupe in groupList:
      if groupe.email:
         strListeMailsGroupes += groupe.email+", "

   if not strListeMailsGroupes:
      strListeMailsGroupes = administratorEmailAddress

   # ########## renvoit le message s'il y a des destinataires

   if strListeMailsDestinataires:

      # template du message
      message = """
From: """+administratorEmailAddress+"""
To: """+strListeMailsGroupes+"""
Bcc: """+strListeMailsDestinataires+"""
Subject: [BDR] """+utilisateur.getId()+" "+texteTransition+" : "+object.TitleOrId()+"""

"""+utilisateur.getId()+" "+texteTransition+" : "+object.TitleOrId()+"""

URL: """+object.absolute_url()+"""

"""

      state_change.object.MailHost.send(message)

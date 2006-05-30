## Script (Python) "devenirRedacteur"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE =  request.RESPONSE


if context.peutDevenirRedacteur()==2:
   RESPONSE.redirect(context.absolute_url()+"?portal_status_message=Vous%20etes%20deja%20redacteur%20de%20ce%20document")

elif context.peutDevenirRedacteur():
   if context.devenirRedacteur_():
      RESPONSE.redirect(context.absolute_url()+"?portal_status_message=Vous%20etes%20maintenant%20redacteur%20de%20ce%20document")
   else:
      RESPONSE.redirect(context.absolute_url()+"?portal_status_message=erreur")
else:
   RESPONSE.redirect(context.absolute_url()+"?portal_status_message=Vous%20ne%20pouvez%20pas%20devenir%20redacteur%20de%20ce%20document")

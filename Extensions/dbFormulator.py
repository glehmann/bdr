from Products.Formulator import Form, Field, StandardFields
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.permissions import ModifyPortalContent
import re


def add_form(self,id,unicode_mode=1,REQUEST=None,title=""):
	if _checkPermission(ModifyPortalContent,self):
		Form.manage_add(self, id, title,unicode_mode,REQUEST)
	else:
		return None

def add_field(form,id,fieldType,title=""):
		#if _checkPermission(ModifyPortalContent,self):
		print type(form)
		form.manage_addField(id,title,fieldType)
		#self.manage_addField(StandardFields.StringField(id))
		#else:
		#	raise "erreur !!!!"


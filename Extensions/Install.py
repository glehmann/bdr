from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.BDR import product_globals

from StringIO import StringIO
import string

new_properties = {"title":"Site du BDR","default_page":"accueil","email_from_name":"Portail BDR",
	"right_slots":[],
	"left_slots":
	 ["here/portlet_navigation/macros/portlet",
	"here/portlet_related/macros/portlet",
	"here/portlet_review/macros/portlet",
	"here/portlet_logos/macros/portlet",
	"here/portlet_zonesUtilisateur/macros/portlet"]
	}

def install(self):
	"""Register skin layer with skin tool, and other setup in the future """
	directory_name = 'BDR'
	
	out = StringIO() # setup stream for status messages
	
	# setup the skins
	skinstool = getToolByName(self, 'portal_skins')
	if directory_name not in skinstool.objectIds():
		# we need to add FileSystem Directory Views for any
		# directories in our skins/ directory
		# These directories should already be configured
		# ajoute le skin dans le portal_skins
		addDirectoryViews(skinstool, 'skins', product_globals)
		out.write("Added %s directory view to portal_skins\n" % directory_name)
	
		
	# Now we need to go through the skin configurations and insert directory_name into the configurations.
	# preferabily, this should be right after where 'custom' is placed.
	# Otherwise, we append it to the end
	
	# ajoute le skin dans les configurations, si possible apres custom, pour le mettre le plus haut dans les priorites
	skins = skinstool.getSkinSelections()
	for skin in skins:
		path=skinstool.getSkinPath(skin)
		path=map(string.strip, string.split(path,','))
		if directory_name not in path:
			try: path.insert(path.index('custom')+1, directory_name)
			except ValueError:
				path.append(directory_name)
			path = string.join(path,', ')
			skinstool.addSkinSelection(skin, path)
			out.write("Added %s to %s skin \n" % (directory_name, skin))

		else:
			out.write("Skipping %s skin, %s is already set up\n" % (skin, directory_name))
	
	
	
	# portal Properties
	
	
	urltool = getToolByName(self,'portal_url')
	portal = urltool.getPortalObject()
	if not(hasattr(portal,'old_properties')):
		portal.old_properties={}

	# sauvegarde les anciennes proprietes dans la propriete old_properties
	
	
	for new_property in new_properties:
		portal.old_properties[new_property] = getattr(portal,new_property)
	
	# et met a jour les proprietes courantes
	portal.manage_changeProperties(new_properties)
	
	return out.getvalue()


def uninstall(self):
	out = StringIO()
	urltool = getToolByName(self,'portal_url')
	portal = urltool.getPortalObject()
	
	
	try:
		portal.manage_changeProperties(portal.old_properties)
	except Exception, e:
		print >> out, "Error: %s" % e
	
	return out.getvalue()
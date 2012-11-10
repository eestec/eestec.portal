"""Custom GenericSetup import step.

Ordinarily, GenericSetup handlers check for the existence of XML files.
Here, we are not parsing an XML file, but we use a text file as a
flag to check that we actually meant for this import step to be run.
The file is found in profiles/democontent. If file is found we run some code
to prepare demo content for eestec.net portal.
"""


def deletePloneFolders(portal):
    """Delete the standard Plone stuff that we don't need."""
    # Delete standard Plone stuff..
    existing = portal.objectIds()
    for item in ['Members', 'news', 'events']:
        if item in existing:
            portal.manage_delObjects(item)


def setupVarious(context):
    """GS import step handler.

    This is called whenever you install a product in Plone. We need to check
    that out custom import step code is ran only when 'democontent' profile
    is being installed.

    @param context: Products.GenericSetup.context.DirectoryImportContext
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for 'democontent' or any other proudtc
    if not context.readDataFile('quintagroup.transmogrifier-import.txt'):
        return  # skip

    portal = context.getSite()
    deletePloneFolders(portal)

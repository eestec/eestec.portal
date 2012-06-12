Rules and Assumptions
=====================


Some rules and guidelines we internally agreed on. Along with assumptions in code.

First page
----------

We assume that there is a Page content type object in root of Plone site with id 'what-is-eestec'. The source of this file should be handled with care as it's divs have special ids, that show one part of content for anonymous and another part for authenticated users. Div with id 'blob' is displayed for anonymous visitors and 'blob-login' is displayed for authenticated members.

Components folder
-----------------

This is a normal Plone folder with id 'components' residing in root of Plone site. Only managers have direct access to this folder. The folder contains components that are used as building blocks of the site. Example: collections for building footer sitemap, first page footer images, ...

Footer navigation
-----------------

We have a collection that is listing child objects for every important top-level folder. We display these collections in footer with a little help of Products.ContentWellPortlets.

LCs Folder
----------

This is a normal Plone folder that contains only LC content objects. All LCs must be added to this folder.

LC titles
---------

LC's do not have their status in the name of the LC. Their status is controlled by a custom workflow enabling different states: Inactive, Observer, JLC, LC. The actual presentation title is then build from the status of the LC and it's name. Ergo, for LC name use just the city, do not prefix it with status.

Remember and self-registration
------------------------------

Since Plone 3.3.2 Remeber's self-registration is broken: http://plone.org/products/remember/issues/64

We fixed this by going to http://eestec.net/portal_memberdata/manage -> click tab Security -> uncheck 'Aquire security settings' and check row Anonymous. Save.


Groups
------

LC Group
""""""""

Each LC has a dedicated group for assigning LC specific permissions on portal object. When administrators create a new LC they must also manually create a group and assign local role "LC" for this group on the LC (this can later on be automatized but we now have more important issues to address). When Member object is created by the registration form this group is automatically assigned local role "LC" over the Member object, and member is added to LC Group (e.g. Ljubljana). This ensures that CPs have permissions over their LC's members.

Administrators
""""""""""""""

Senior IT Team members with managerial permissions. 

Board
"""""

International Board members with special permissions like approving event participants, etc. Boardies also have a dedicated private workspace on the site, where they can share documents, know-how, tasks, ...

Roles
-----

CP 
""

A member with this role has CP related permissions: adding events, accepting event applications, managing it's LCs members, etc. 

Board 
"""""

A role for the Board group.

LC
""

A role that is assigned on LC object for the LC's "LC Group".
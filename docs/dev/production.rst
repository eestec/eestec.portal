.. _production_env:

======================
Production environment
======================

Auto-deploying to production
============================

Whenever a new tag is detected in our Git repository, our production server
fetches the latest tag and deploys it. This is done with a cronjob invoked
script that does the following:

#. Check if there are any new tags.
#. Backup ``Data.fs`` and ``blobstorage``.
#. Get latest tag.
#. Run ``bin/buildout -c production``.
#. Restart all Zope servers.

.. note:: The script is invoked every 5 minutes.


TODO: How is production server actually set up? Permissions? What OS?
TODO: crontab script that I describe below doesn't exist yet


Deployment checklist
====================

As seen above, deployment to production is invoked by simply creating a Git
tag. To ensure everything goes smoothly, follow these steps:

* Checkout the code locally and run all tests.
* Bump version in ``version.txt`` and make sure ``HISTORY.txt`` has been
  updated.
* Commit and push all changes.
* Confirm that the code works fine on live data on staging server.
* Create & push a tag: ``git tag -a v0.14`` and ``git push --tags``.
* Verify that production deployment went well.


Reverting a bad deployment
==========================

If a deployment goes bad you can easily revert to the previous tag and
pre-deployment database snapshot by running the following Fabric script:

.. sourcecode:: bash
    [you@local eestec.portal]$ bin/fab production revert




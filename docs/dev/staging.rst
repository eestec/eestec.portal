.. _staging_env:

===================
Staging environment
===================

Auto-deploying to staging
=========================

On every change to the ``master`` branch, our development server builds a
staging environment with latest code on fresh live data. This is done
with a cronjob invoked script that does the following:

#. Check if there were any changes from last time.
#. Get latest changes.
#. Run ``bin/buildout -c staging``.
#. Rsync ``Data.fs`` from the production server.
#. Rsync ``blobstorage`` from the production server.
#. Restart Zope.

.. note:: The script is invoked every 5 minutes.

.. note:: There is no need to purge the staging environment for every re-build
    as we don't need to test the entire build process -- Travis already does
    that for us.


TODO: How is staging server actually set up? Permissions
TODO: crontab script that I describe below doesn't exist yet


AppCove - The Internal Application
==================================

This is a modern (2012) AppStruct project.  That means that it uses nginx on the front end, apache+mod_wsgi on the middle, and redis+postgresql on the backend.

It consists of:

* A primary site with login
* etc...

## Notes

nginx must handle common web files on its own.  

All other requests are passed to apache.

Apache passes everything on to mod_wsgi.


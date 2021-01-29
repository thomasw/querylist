Changelog
=========

**0.5.0**

* Dropped support for Python 2
* Dropped support for all Python 3 versions below Python 3.6.
* Dropped support for PyPy based on Python 2.7.

**0.4.0**

* Fixed an issue building wheels caused by an empty string as a requirement in
  setup.py.
* Improved `querylist.list.NotFound` exception output.
* Moved `querylist.list.NotFound` so that it is automatically imported and
  available for exception handling when `QueryList` is imported:

  >>> from querylist import QueryList
  >>> QueryList.NotFound
  <class 'querylist.list.NotFound'>

**0.3.0**

* Adds Python 3 support.

**0.2.0**

* Added a new field lookup called `call`. It uses the passed value as a callable
  to test the specified attribute of QueryList objects.
* Fixed a bug in the QueryList implementation that would cause
  querylist+querylist addition and querylist+list addition to return lists. These
  operations now return a new QueryList instance containing the combined data.

**0.1.0**

* Renamed QueryList's 'limit' method to 'filter' so that the QueryList API is
  more consistent with Django's QuerySets.

**0.0.1**

* Initial relase

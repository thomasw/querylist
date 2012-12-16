# Performance

* Performance can be improved dramatically by adopting a lazy evaluation
approach. Instead of evaluating filtering/exclusion methods when they are
called, those constraints can be passed on to output QueryLists and simply
accumulated.
* Instead of wrapping all elements with the wrapper on instantiation, that
can wait until the data is accessed.

# Complex queries (or)

There is currently no way to do logical OR combinations of field lookups. We
should investigate an approach similar to Django's Q object.

# Improved aggregation

Currently, QueryLists only support counting. Standard aggregation functions
would be easy to implement.

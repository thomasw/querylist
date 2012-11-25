# Performance

* Performance can be improved dramatically by adopting a lazy evaluation
approach. Instead of evaluating limiting/exclusion methods when they are
called, those constraints can be passed on to output QueryList and simply
accumulated.
* Instead of wrapping all elements with the wrapper on instantiation, that
can wait until the data is accessed.
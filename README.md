# Recurring\_Venmo

Use Venmo CLI and Gmail API to read recurring shared charges and request money.

# Musings

* The current implementation has the following psuedo-structure:

```
For all monthly bills:
    find all emails that match the specified string:
        for all emails that match the specified string:
	    if the date of the email is later than the last run date:
	        create the venmo request
```

When this is written out in a more psuedo-code style:

```python
# for bill in bill dictionary:
    # create EmailParser() instance
    # find all emails that match the specified string 

    # for all emails that match the specified string:
	# create Bill() instance
	# if the date of the email is later than the last run date:
	    # create the venmo request
```

However this algorithm isn't the most efficient; since only some of the
emails that match the specified string will be later than the last run date
(call this set of emails M, which is a subset of N, all emails that matched
the specified string), there will be N - M `Bill()` instantiations, including
all the computation that goes along with a `Bill()` instantiation, that happens
unnecessarily.

By checking if the email date is later than the last run date prior to the `Bill()`
instantiation, this inefficiency is removed:

```python
# for bill in bill dictionary:
    # create EmailParser() instance
    # find all emails that match the specified string 

    # for all emails that match the specified string:
    # if the date of the email is later than the last run date:
        # create Bill() instance
        # create the venmo request
```

# TODO

* At which level of the "problem hierarchy" should exceptions be handled??

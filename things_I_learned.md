# Algorithmic Musings

## 1

The first implementation had the following pseudo-structure:

```
# For all monthly bills:
    # find all emails that match the specified string:
        # for all emails that match the specified string:
	    # if the date of the email is later than the last run date:
	        # create the venmo request
```

When this is written out in a more pseudo-code style, using the classes written
for this problem, this becomes:

```
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
the specified string), there will be N - M unnecessary `Bill()` instantiations.

By checking if the email date is later than the last run date prior to the `Bill()`
instantiation, this inefficiency is removed:

```
# for bill in bill dictionary:
    # create EmailParser() instance
    # find all emails that match the specified string 

    # for all emails that match the specified string:
    # if the date of the email is later than the last run date:
        # create Bill() instance
        # create the venmo request
```

## 2

There could be a case to be made that once the date of the email is identified,
if that date is prior to the last run date, then no more computation should be
expended on the parsing of that email. In order for this to occur (with the
current framework), the `last_run_date` would have to be passed to the `EmailParser()`
constructor (or the `EmailParser()` instance would have to know about it in
some other manner...).

In my opinion, this starts to "muddy the waters" of one of the design principals
of OOP, *Encapsulation.* Since the ideal is to group **logically related** types,
variables and methods, a variable that isn't related to the concept that the
`EmailParser()` class is made for shouldn't be included in said class.


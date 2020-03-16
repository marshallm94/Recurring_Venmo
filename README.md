# Recurrin\_Venmo
Use Venmo CLI and Gmail API (?) to read recurring shared charges and request money.

# Notes/TODO:

* In terms of keeping track of the most recent date the program was run,
would it make sense to write a text file to the file system at the absolute
end of execution? This could then be read in at the start of the program, and
used in the following psuedo-code way:

```python
if date_of_bill is before date_read_in_from_text_file:
	# don't charge twice for same thing.
	pass
```

* At which level of the "problem hierarchy tree" should exceptions be handled??

* Separate setup logic into separate, appriopriately named file (so there is one
'main.py' whose structure easily maps onto the problem structure).

* If no charges are made, have a log that says "No new charges registered since
last run".

* Current implementation has the parsing of an email snippet separated into one
function per bill/montly payment. The only difference between these functions is
how the email snippet is parsed. Is it worth...:
	* Combining all the functionality into one function and separating the
	different parsing mechanisms using `if/else` clauses?
	* Creaing a meta-class that handles most of the logic, and create a sub-class
	for each bill/email that needs a separate parsing scheme?

* Had to reinstall and reconfigure venmo CLI credentials in order to fix 401
error. Not sure if this will be a recurring issue.

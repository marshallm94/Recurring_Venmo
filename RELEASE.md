# Release 2.0

* No longer using the Venmo API since it has been deprecated (apparently this has
been [the case for some time](https://github.com/zackhsi/venmo/issues/58))
	* Moving to a framework that uses [textbelt](https://github.com/typpo/textbelt)
	to send the user a text with all the necessary information for a charge,
	and then the onus is on the user to actually make the request.
	* Note that this doesn't require any additional installations; a `curl`
	command is called within `main.py` and the text is sent to textbelt which
	sends the text via SMS.

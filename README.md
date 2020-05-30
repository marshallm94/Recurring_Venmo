# Recurring\_Venmo

Use Venmo CLI and Gmail API to create and request recurring monthly charges.

For a look at some of the takeaways I thought about during this micro-project,
check out [things_I_learned.md](things_I_learned.md)

# Setup

`token.json` and `credentials.json` are the two files that
[EmailParser.py](EmailParser.py) needs in order to run. These can be obtained
using [Google's Cloud Platform](https://console.developers.google.com/apis/dashboard?project=recurring-venmo)

The [setup.sh](setup.sh) file includes all the installations necessary for
this program (in addition to some installations on a raspberry pi).

If you would like to manually run this at whatever time interval you like, 
simply run `bash run_program.sh` from the CL. Alternatively, this could be setup
to run at a specified interval using crontab (which is how it is currently setup
on previously mentioned raspberry pi).

**If the requests do not complete,** but every other part of the program runs
properly, check `request_logs.log`. If the last line of the traceback is:

```
  users = response.json()['data']
KeyError: 'data'
```

...then the credentials for the venmo package have timed out. You will need to
reconfigure by running `venmo configure` at the command line. See
[this issue](https://github.com/zackhsi/venmo/issues/57) for more information.
**At the time of the writing, there is no way around the credientials timing out.**

# TODO

* The current exception that is thrown if there is an error parsing an email
isn't very descriptive; it is simply `print("Error parsing email with specified search string.")`.
Should there be more information in this error message? email ID? Date? (This 
currently only happens for old emails that are prior to the last run date, so it
isn't "really" a problem.)

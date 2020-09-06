# Recurring\_Venmo

Use [textbelt](https://github.com/typpo/textbelt) and Gmail API to identify
recurring monthly charges and send myself a text to request money.

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

## Textbelt Setup

I set up an API key with Textbelt (not tracked via Git for obvious reasons - this
must be `scp`'d to the Raspberry Pi) and whenever the number of texts I have
remaining (`resp.json()['quotaRemaining']`) reaches 0, my card will be charged
(since this is setup to only run monthly I don't expect this to be a huge expense).

# TODO

* The current exception that is thrown if there is an error parsing an email
isn't very descriptive; it is simply `print("Error parsing email with specified search string.")`.
Should there be more information in this error message? email ID? Date? (This 
currently only happens for old emails that are prior to the last run date, so it
isn't "really" a problem...then again I'm sure everyone says that until it
bites them in the ass...)

#!/usr/bin/env python

"""
Keep only files dated for the last few days or from a specific weekday;
remove all others
"""

import os,sys
from datetime import date,timedelta

from optparse import OptionParser
 
parser = OptionParser()
parser.add_option("--keep",
                  help="keep files from the last DAYS days",
                  default=14, # by default, keep last 14 day backups
                  type=int,
                  metavar="DAYS")

parser.add_option("--keepday",
        help="keep files from the speficied cron weekday (1:Mon, ..., 7:Sun)",
                  default=7, #keep Sunday's backups
                  metavar="DAY")
 
parser.add_option("--run",
                  action="store_true", 
                  default=False,
                  help="actually remove the files")
 
(options, args) = parser.parse_args()

def get_date_mtime(filename):
    'Return last modification time from file filename as a datetime.date object'
    return date.fromtimestamp(os.stat(filename).st_mtime)

def execute(filename):
    'Execute the commands on filename'

    sys.stdout.write('Removing file %s' %filename)

    if options.run:
        sys.stdout.write('\n')
        os.remove(filename)
    else:
        sys.stdout.write(' **DRY-RUN**\n')


#get directory listing
dirlist = os.listdir('.')

#get modification times
mtimes = [ get_date_mtime(afile) for afile in dirlist ]

today = date.today()
threshold = timedelta(options.keep)

#evaluate files
for f,d in zip(dirlist,mtimes):
    if today-d > threshold and d.isoweekday() != options.keepday:
        execute(f)
    else:
        print 'Keeping', f


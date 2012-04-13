import optparse
import json
import urllib2
import commands
import time
import os
import gntp.notifier

interval = 30 #interval in seconds
duration = 3 #duration of check in hours
threshold = 199.0 #alert threshold
n = 0

parser = optparse.OptionParser()
parser.add_option("-g", "--growl",
                  dest="growl", default=False,
                  action="store_true",
                  help="Enable Growl notifications. Must have 'growlnotify' installed")
parser.add_option("-i", "--interval",
                  dest="interval", default="60",
                  help="Update interval",
                  metavar="SECONDS")
parser.add_option("-d", "--duration",
                  dest="duration", default="3",
                  help="Duration to continue checking",
                  metavar="HOURS")
parser.add_option("-t", "--threshold",
                  dest="threshold", default="50",
                  help="Threshold to notify",
                  metavar="DOLLARS")
(options, args) = parser.parse_args()

while n < (int(options.duration)*60*60/int(options.interval)):
    try:
        result = json.loads(urllib2.urlopen('http://jonathanstark.com/card/api/latest').read())
    except (urllib2.HTTPError, urllib2.URLError):
        print "Error loading resource."
        result = None
        if options.growl:
            gntp.notifier.mini("Error loading resource.")
    balance = float(result['balance']['amount']) if result else 0
    n += 1
    if balance >= float(options.threshold):
        if options.growl:
            gntp.notifier.mini("It worked!")
        else:
            commands.getstatusoutput('open ./play.app') #Play your iTunes library
        print "BALANCE IS %s" % balance
    else:
        print "%s is not over %s" % (balance, options.threshold)
    time.sleep(int(options.interval))

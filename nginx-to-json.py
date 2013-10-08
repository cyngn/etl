import re
import sys
import datetime
import json
import time
import os

if len(sys.argv) != 2:
    print "Usage: %s [tag]" % (sys.argv[0])
    sys.exit(1)

PATTERN = r'^(?P<remote>[\d+\.]*) (?P<host>[^ ]*) (?P<user>[^ ]*) \[(?P<time>[^\]]*)\] "(?P<method>\S+)(?: +(?P<path>[^\"]*) +\S*)?" (?P<code>[^ ]*) (?P<size>[^ ]*)(?: "(?P<referer>[^\"]*)" "(?P<agent>[^\"]*)")?$'
TAG = sys.argv[1]
TARGET_SIZE = 133169152  # 127MB
FILES = {}
BYTES_WRITTEN = {}


def write_entry(entry):
    date = entry['time'].split(" ")[0]
    fd = get_fd(entry)
    BYTES_WRITTEN[date] += os.write(fd.fileno(), json.dumps(entry) + "\n")


def get_fd(entry):
    date = entry['time'].split(" ")[0]

    bytes_written = BYTES_WRITTEN.get(date, None)
    if bytes_written is None or bytes_written >= TARGET_SIZE:
        if not os.path.exists("out/dt=%s" % date):
            os.makedirs("out/dt=%s" % date)
        filename = "out/dt=%s/%s" % (date, int(time.time()))

        print "Creating new file: %s" % filename
        old_fd = FILES.get(date, None)
        if old_fd is not None:
            old_fd.close()

        BYTES_WRITTEN[date] = 0
        FILES[date] = open(filename, 'a')
        return FILES[date]
    else:
        return FILES[date]


for line in sys.stdin:
    match = re.search(PATTERN, line)
    if not match:
        continue

    timestamp = datetime.datetime.strptime(match.group('time').split(" ")[0], "%d/%b/%Y:%H:%M:%S")
    entry = {
        'remote': match.group('remote'),
        'host': match.group('host'),
        'user': match.group('user'),
        'time': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'method': match.group('method'),
        'path': match.group('path'),
        'code': match.group('code'),
        'size': match.group('size'),
        'referer': match.group('referer'),
        'agent': match.group('agent'),
        'tag': TAG,
    }
    write_entry(entry)

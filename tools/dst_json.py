from datetime import datetime
import subprocess
import sys
import glob
import os
import json

def zdump(tz):
    cmd = "zdump -v %s | grep isdst=1 | awk '{print $2,$3,$4,$5,$6,$7}'" % tz
    child = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = child.communicate()
    return stdout.decode().strip().split('\n')

def daylight_saving_times():
    args = sys.argv
    files = glob.glob(os.path.join(args[1], '**'), recursive=True)
    timezones = [x.strip(args[1]) for x in files]
    
    daylight_savings = {}
    
    for tz in timezones:
        
        if tz == "":
            continue
        
        dates = zdump(tz)
        if len(dates) <= 1:
            continue
    
        daylight_savings[tz] = {}
        starts = []
        ends = []
        i = 1
        for dtstr in dates:
            if dtstr == "":
                break
    
            dt = datetime.strptime(dtstr, "%c %Z")
            if i % 2 == 0:
                ends.append(dt)
            else:
                starts.append(dt)
    
            i = i + 1
    
        if len(starts) > len(ends):
            starts.pop(-1)
    
        for l in range(len(starts)):
            start = starts[l]
            end = ends[l]
    
            daylight_savings[tz]["%d-%d" % (start.year, end.year)] = [int(start.timestamp()), int(end.timestamp())]
    
    print(json.dumps(daylight_savings))

if __name__ == "__main__":
    daylight_saving_times()

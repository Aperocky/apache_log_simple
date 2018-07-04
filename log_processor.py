"""

This script is designed to analyze apache server logs

Numerous function with specific goals are here

"""
import os, sys

command_list = [
    "unique_ips",
    "unique_ip_num",
    "os_type",
    "os_type_ip",
    "os_type_full_count",
    "os_type_count",
    "FULL_LOG",
]

# Returns a generator for the rest of methods.
class LogReader:

    def __init__(self, fn):
        self.file = fn
        self.generator = self.file_proc(fn)

    def set_file(self, fn):
        self.file = fn
        self.generator = self.file_proc(fn)

    def file_proc(self, fn):
        with open(fn, 'r') as fin:
            while(True):
                line = fin.readline()
                if not line:
                    return
                yield line

    @staticmethod
    def splitstrip(line, delimiter):
        split = line.split(delimiter, 1)
        return split[0], split[1]

    def lineproc(self, line, log=False):
        ip, line = LogReader.splitstrip(line, " - - [")
        time, line = LogReader.splitstrip(line, "] \"")
        request, line = LogReader.splitstrip(line, "\" ")
        status, line = LogReader.splitstrip(line, " \"")
        url, line = LogReader.splitstrip(line, "\" \"")
        browser = line[:-2]
        # Test lineproc
        if log:
            print("ip : " + ip)
            print("time : " + time)
            print("request : " + request)
            print("status : " + status)
            print("address : " + url)
            print(browser)
        return ip, time, request, status, url, browser

    def browserproc(self, line, log=False):
        mozilla = "Mozilla/5.0"
        system = os = chip = ""
        try:
            mozilla, line = LogReader.splitstrip(line, " (")
            # print(line)
            system, line = LogReader.splitstrip(line, ")")
            # print(line)
            os, chip = LogReader.splitstrip(system, ";")
        except Exception as e:
            os = "Not Identified"
            chip = "Not Identified"
        # Test browserproc
        if log:
            print("compat : " + mozilla)
            print("system : " + system)
            print("browser: " + line)
        return mozilla, os, system, chip, line

# prepare general function
def prep():
    fn = sys.argv[1]
    lr = LogReader(fn)
    return lr

# PRINT FULL LOG
def FULL_LOG():
    lr = prep()
    while(True):
        try:
            line = next(lr.generator)
        except Exception:
            break
        lr.browserproc(lr.lineproc(line, log=True)[5], log=True)
        print("\n")

# Return a list of all unique IP in the log.
def unique_ips():
    lr = prep()
    uniset = set()
    while(True):
        try:
            line = next(lr.generator)
        except Exception:
            break
        ip = lr.lineproc(line)[0]
        uniset.add(ip)
    return list(uniset)

# Return number of all unique IP in the log
def unique_ip_num():
    return len(unique_ips())

def os_type():
    lr = prep()
    uniset = set()
    while(True):
        try:
            line = next(lr.generator)
        except Exception:
            break
        system = lr.browserproc(lr.lineproc(line)[5])[2]
        uniset.add(system)
    return list(uniset)

def os_type_ip():
    lr = prep()
    uniset = dict()
    while(True):
        try:
            line = next(lr.generator)
        except Exception:
            break
        ip = lr.lineproc(line)[0]
        system = lr.browserproc(lr.lineproc(line)[5])[2]
        if system in uniset:
            uniset[system].add(ip)
        else:
            uniset[system] = {ip}
    return uniset

def os_type_full_count():
    uniset = os_type_ip()
    for k, v in uniset.items():
        uniset[k] = len(v)
    return uniset

def os_type_count():
    uniset = os_type_full_count()
    newset = dict()
    newset["Windows"] = 0
    newset["Mac"] = 0
    newset["Linux"] = 0
    newset["Android"] = 0
    newset["iOS"] = 0
    newset["Others"] = 0
    for k, v in uniset.items():
        if "Windows" in k:
            newset["Windows"] += v
        elif "Macintosh" in k:
            newset["Mac"] += v
        elif "Linux" in k:
            if "Android" in k:
                newset["Android"] += v
            else:
                newset["Linux"] += v
        elif "iPhone" in k:
            newset["iOS"] += v
        else:
            newset["Others"] += v
    return newset

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("not enough arguments.")
    if not sys.argv[2] in command_list:
        sys.exit("command not recognized")
    myfunc = globals()[sys.argv[2]]
    result = myfunc()
    if type(result) is dict:
        for key, value in result.items():
            print(key + ": " + str(value))
    elif(type(result) is list):
        if len(result) < 50:
            for rec in result:
                print(rec)
        else:
            print(result)
    else:
        print(result)
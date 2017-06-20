# coding:utf8
import json
import bisect

try:
    _data = json.loads(open("ip_location.json").read())
except IOError as e:
    print("[error] %s" % e)
    exit()
for d in _data:
    _data[d] = _data[d].split("|")


def ip2int(s):
    ss = s.split('.')
    int_ip = 0
    for i, d in enumerate(ss):
        int_ip = int_ip * 256 + int(d)
    return int_ip


def find_ip_location(s):
    ip_int = str(ip2int(s))
    for d in _data:
        x_loc = bisect.bisect_left(_data[d], ip_int)
        l, r = _data[d][x_loc - 1].split('-')
        if l < ip_int < r:
            return d
    return "Other Country"


print(find_ip_location("10.0.0.1"))

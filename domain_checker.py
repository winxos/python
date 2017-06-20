# coding:utf8
#域名有效性批量检测
#winxos 2017-06-11
import urllib
from urllib import request
import json
import itertools
from multiprocessing.pool import ThreadPool


def get_html(url, retry=10):
    try:
        proxy = {'http': '60.167.135.146:808'}
        proxy_support = request.ProxyHandler(proxy)
        opener = request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
        request.install_opener(opener)
        data = request.urlopen(url).read()
    except Exception as e:
        print(e)
        if retry <= 0:
            return None
        return get_html(url, retry - 1)
    return data.decode('utf8')


def get_domain_available(domain):
    # url = "https://sg.godaddy.com/zh/domainsapi/v1/search/exact?q=%s" % domain #godaddy
    url = "https://checkapi.aliyun.com/check/checkdomain?domain=%s" % domain + \
          "&token=check-web-hichina-com%3Ao29tutf4w4fhfzhmvibxagd4odw3lew5&_=1497839736973" #token 需要更新
    try:
        j = json.loads(get_html(url))
        return domain, j["module"][0]["avail"]
    except Exception as e:
        print(e)
        return domain, 0


THREAD_NUMS = 2


def multi_thread_do_job(l, size=THREAD_NUMS):  # 容易被办
    p = ThreadPool(size)
    tasks = []
    for i, d in enumerate(l):
        tasks.append(p.apply_async(get_domain_available, args=(d,)))
    p.close()
    results = []
    for i, d in enumerate(tasks):
        t = d.get()
        if t[1] != 0:
            results.append(t[0])
            print(t)
        print("\rprogress: %.2f" % (100 * i / len(l)), end="")
        return results

def anti_robot(l):
    results = []
    for i, d in enumerate(l):
        print("\rprogress: %.2f" % (100 * i / len(l)), end="")
        t = get_domain_available(d)
        if t[1] != 0:
            results.append(t[0])
            print(t)

    return results


# ds = list(itertools.permutations('abcdefghijklmnopqrstuvwxyz', 3))
ds = list(itertools.permutations('abcdefghijklmnopqrstuvwxyz', 3))
ds = ["g" + "".join(d) + ".com" for d in ds]

print(len(ds))
print(anti_robot(ds))

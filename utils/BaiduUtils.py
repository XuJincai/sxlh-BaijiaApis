import time


def get_common_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://cn.bing.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

def get_detail_headers():
    return {
        "Host": "mbd.baidu.com",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://author.baidu.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
def get_home_headers():
    return {
        "Host": "mbd.baidu.com",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://author.baidu.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
def trans_cookies(cookies):
    items = cookies.split('; ')
    return {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in items}

def get_content_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
# 1710294666转换为YYYY-MM-DD HH:MM:SS
def trans_date(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))


if __name__ == '__main__':
    cookies = {
        "BIDUPSID": "AE5A499738C8AA69ED3EBD1E6B248BCA",
        "PSTM": "1728716960",
        "BAIDUID": "6AB7B3F6A2B64299756F17EEAC56D270:FG=1",
        "H_WISE_SIDS": "61027_61054_61068_60851_61119_61129_61128_61113_61140_61133",
        "BAIDUID_BFESS": "6AB7B3F6A2B64299756F17EEAC56D270:FG=1",
        "H_WISE_SIDS_BFESS": "61027_61054_61068_60851_61119_61129_61128_61113_61140_61133",
        "ZD_ENTRY": "bing",
        "Hmery-Time": "2426579607",
        "ppfuid": "FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGlcv8RcA1xQKfriWJVc7a+LGEimjy3MrXEpSuItnI4KDy6SdkoVDBfnPMf6rio6M04KUxD4QgTImMHTTY4+nES24R/FnOemjNRCuI1DYLMopx8XUPJGV6+o409dgWc+CNLGgLbz7OSojK1zRbqBESR5Pdk2R9IA3lxxOVzA+Iw1TWLSgWjlFVG9Xmh1+20oPSbrzvDjYtVPmZ+9/6evcXmhcO1Y58MgLozKnaQIaLfWRIXZy/8llaWZittcIfh39p9NjGCbnYWN73rxtX036bU+lqe3DyQvjDt6TZ+KXd2BKtnTNS/pLMWceus0e757/UN2nsqw9F4aiTP2No0RRtYGAAv3LCf1Y7/fHL3PTSf9vid/u2VLX4h1nBtx8EF07eCMhWVv+2qjbPV7ZhXk3reaWRFEeso3s/Kc9n/UXtUfNU1sHiCdbrCW5yYsuSM9SPGDZsl7FhTAKw7qIu38vFZiq+DRc8Vbf7jOiN9xPe0lOdZHUhGHZ82rL5jTCsILwcRVCndrarbwmu7G154MpYiKmTXZkqV7Alo4QZzicdyMbWvwvmR2/m//YVTM8qeZWgDSHjDmtehgLWM45zARbPujeqU0T92Gmgs89l2htrSKIYLLWfltu9WytXU+9UuhRnDUbaB2zdFteLHu3sjGERkKmOZCd2fUy3QQ5XrLGYgIP5dImdyxYIjA1uSy2hfTFv/d3cnXH4nh+maaicAPllDgrppZTr0lDf2Vsiy73L8egP9ck5gsaaSE4obz9V1JGvy/5mva47HoW3qwE6QdWoFG0AuEJyvqDMA2g1qlLzP197jLwshUeYAVxVRBnbmSqciVpX0cU4NHwEy/Bqr1kOP1AxyNZHhQVZ2Gp0uL7HNFb+K+jseqgkgNhlYW3G8vU2dGT/8PDdrVN+aMZbHqtS1oD7ul7bRoEgw96s3k/oqBkZVYaMKnX0dWh5E7VnhqRSIp26nF1P0+H9oSyCPQ94PP1SRaarSoV0g9/mcXvXTKKL2ifvDtmvBaDgOtQDUHWkidYGoNGUGHvoUGEVeuGNvevqVlP+R70AF9nPDu1HNMYJ4rii+VMKitDllMOLt2Pn8x2CMSIC2cqmzbCUy4+VlV80NhgOXofGoldJwzhprX4YmDY27NjcT9GnAIAKTXdHs=",
        "RT": "\"z=1&dm=baidu.com&si=ede40218-0a58-46c1-b303-cb0b7b0e6026&ss=m43qa0f5&sl=2&tt=zr&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1hu&ul=bmpv&hd=bmq9\"",
        "H_PS_PSSID": "61027_61216_61210_61213_61209_61245_61287_61297_61247",
        "BA_HECTOR": "858ka4al802g0l85018h24048f0h101jklav91v",
        "ZFY": "RjE0fl0VN6VI6U8DjaQuW:BeHRAlVLOw2FgAL7P76I6U:C",
        "PSINO": "3",
        "delPer": "0",
        "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
        "ab_sr": "1.0.1_MGIzMDA4MjU5YmMwOWQ5MDhjMTQyNGMzZTg0ZWM2MTgxM2Q5MzJiNzZlMjE3ZTNhZGEzYWM2NWRjMjM0NDRiZGMxNzZkZjQxYzg4YWE2ZTMxMWY0MTc0OTY1MTJhY2YzZjg3MGY0ZjdmODYwZjc1YWVjMDNiMDc1ZGY4MjI4YWIzMzZkOTM4MzE1M2E3YTI5Mzc2N2RmMWQ5N2ZlMDgyNA=="
    }
    cookies_str = 'BIDUPSID=AE5A499738C8AA69ED3EBD1E6B248BCA; PSTM=1728716960; BAIDUID=6AB7B3F6A2B64299756F17EEAC56D270:FG=1; H_WISE_SIDS=61027_61054_61068_60851_61119_61129_61128_61113_61140_61133; BAIDUID_BFESS=6AB7B3F6A2B64299756F17EEAC56D270:FG=1; H_WISE_SIDS_BFESS=61027_61054_61068_60851_61119_61129_61128_61113_61140_61133; ZD_ENTRY=bing; Hmery-Time=2426579607; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGlcv8RcA1xQKfriWJVc7a+LGEimjy3MrXEpSuItnI4KDy6SdkoVDBfnPMf6rio6M04KUxD4QgTImMHTTY4+nES24R/FnOemjNRCuI1DYLMopx8XUPJGV6+o409dgWc+CNLGgLbz7OSojK1zRbqBESR5Pdk2R9IA3lxxOVzA+Iw1TWLSgWjlFVG9Xmh1+20oPSbrzvDjYtVPmZ+9/6evcXmhcO1Y58MgLozKnaQIaLfWRIXZy/8llaWZittcIfh39p9NjGCbnYWN73rxtX036bU+lqe3DyQvjDt6TZ+KXd2BKtnTNS/pLMWceus0e757/UN2nsqw9F4aiTP2No0RRtYGAAv3LCf1Y7/fHL3PTSf9vid/u2VLX4h1nBtx8EF07eCMhWVv+2qjbPV7ZhXk3reaWRFEeso3s/Kc9n/UXtUfNU1sHiCdbrCW5yYsuSM9SPGDZsl7FhTAKw7qIu38vFZiq+DRc8Vbf7jOiN9xPe0lOdZHUhGHZ82rL5jTCsILwcRVCndrarbwmu7G154MpYiKmTXZkqV7Alo4QZzicdyMbWvwvmR2/m//YVTM8qeZWgDSHjDmtehgLWM45zARbPujeqU0T92Gmgs89l2htrSKIYLLWfltu9WytXU+9UuhRnDUbaB2zdFteLHu3sjGERkKmOZCd2fUy3QQ5XrLGYgIP5dImdyxYIjA1uSy2hfTFv/d3cnXH4nh+maaicAPllDgrppZTr0lDf2Vsiy73L8egP9ck5gsaaSE4obz9V1JGvy/5mva47HoW3qwE6QdWoFG0AuEJyvqDMA2g1qlLzP197jLwshUeYAVxVRBnbmSqciVpX0cU4NHwEy/Bqr1kOP1AxyNZHhQVZ2Gp0uL7HNFb+K+jseqgkgNhlYW3G8vU2dGT/8PDdrVN+aMZbHqtS1oD7ul7bRoEgw96s3k/oqBkZVYaMKnX0dWh5E7VnhqRSIp26nF1P0+H9oSyCPQ94PP1SRaarSoV0g9/mcXvXTKKL2ifvDtmvBaDgOtQDUHWkidYGoNGUGHvoUGEVeuGNvevqVlP+R70AF9nPDu1HNMYJ4rii+VMKitDllMOLt2Pn8x2CMSIC2cqmzbCUy4+VlV80NhgOXofGoldJwzhprX4YmDY27NjcT9GnAIAKTXdHs=; RT="z=1&dm=baidu.com&si=ede40218-0a58-46c1-b303-cb0b7b0e6026&ss=m43qa0f5&sl=2&tt=zr&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1hu&ul=bmpv&hd=bmq9"; H_PS_PSSID=61027_61216_61210_61213_61209_61245_61287_61297_61247; BA_HECTOR=858ka4al802g0l85018h24048f0h101jklav91v; ZFY=RjE0fl0VN6VI6U8DjaQuW:BeHRAlVLOw2FgAL7P76I6U:C; PSINO=3; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_N2FjYmE2MTdjYWI4YmQ4OWEzODUxMWI1ZjAwYWFjYjBkMWMxMTk5ZDZkYmQ1YmM1OTIxYzU5OTYxNDc4MjhmZDBjZTQ1MjU4NDVmOTg0ZDIyMjVkNTU4MDZlMTVjY2YwZDFlMmRlZWI0MTNiYWE2NzMyZWZjNTRhMzkyNmQyMDdkMDM2ZmFmOWFkNjNlZGZiNDdkZTkwMjUwNDc0NTA1Mw=='
    ck = trans_cookies(cookies_str)
    for k,v in ck.items():
        print(f'{v}')
        print(cookies[k])

def timestamp_to_str(timestamp):
    time_local = time.localtime(timestamp / 1000)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

# %Y-%m-%d %H:%M:%S 转时间戳 10位
def str_to_timestamp(str):
    time_array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(time_array))
    return timestamp

# 判断日期与当前日期是否在n天内
def is_n_days_ago(date, n):
    now = time.time()
    date = str_to_timestamp(date)
    if now - date > n * 24 * 60 * 60:
        return False
    return True

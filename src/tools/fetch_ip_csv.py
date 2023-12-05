import requests
import re

response = requests.get("http://ip.bczs.net/country/CN")
# print(" content: %s" % response.text)
result = re.findall(
    r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b-\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", response.text)
# print("result: %s" % result)
schema = "ip, province, operator"
fp = open("ipinfo.csv", "w+")
fp.write(schema.replace(' ', '') + "\n")
for ip_seg in result:
    start_ip = ip_seg.split('-')[0]
    print("### start_ip: %s" % start_ip)
    # get the ip information
    url = "http://ip.bczs.net/%s" % start_ip
    response = requests.get(url)
    if response.text is None:
        continue
    find_result = re.findall("参考数据.*<br/>", response.text)
    if find_result is None or len(find_result) == 0:
        continue
    test = re.sub("<br/>IP数据.*", '', find_result[0])
    test2 = re.sub("参考数据：", '', test).split()
    print("#### response: %s" % response.text)
    print("### find result: %s" % test2)
    if len(test2) != 3:
        continue
    fp.write(test2[0] + ",")
    fp.write(test2[1] + ",")
    fp.write(test2[2] + "\n")
fp.close()

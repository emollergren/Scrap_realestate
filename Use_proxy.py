import requests
import random
import time

proxies = [
    "http://203.243.63.16:80",
    "http://3.24.58.156:3128",
    "http://95.217.104.21:24815",
    "http://103.151.41.7:80",
    "http://190.113.40.202:999",
    "http://142.11.222.22:80",
    "http://109.111.212.78:8080",
    "http://191.97.16.160:999",
    "http://102.216.69.176:8080",
    "http://154.239.9.94:8080",
    "http://107.178.9.186:8080",
    "http://190.5.77.211:80",
    "http://201.229.250.21:8080",
    "http://146.59.243.214:80",
    "http://181.212.45.226:8080",
    "http://46.160.129.189:3128",
    "http://5.78.89.192:8080",
    "http://95.217.195.146:9999",
    "http://82.165.105.48:80",
    "http://190.111.209.207:3128",
    "http://144.91.106.93:3128",
    "http://34.87.103.220:80",
    "http://188.34.164.99:8080",
    "http://190.238.231.65:1994",
    "http://152.231.25.114:8080",
    "http://45.238.12.4:3128",
    "http://94.231.192.97:8080",
    "http://119.93.129.34:80",
    "http://181.74.81.195:999",
    "http://34.29.41.58:3128",
    "http://13.209.156.241:80",
    "http://212.192.31.37:3128",
    "http://45.159.150.23:3128",
    "http://103.76.253.66:3129",
    "http://137.184.197.190:80",
    "http://139.5.73.71:8080",
    "http://201.182.251.142:999",
    "http://46.101.102.134:3128",
    "http://200.52.148.10:999",
    "http://41.65.160.171:1981",
    "http://181.212.41.171:999",
    "http://41.65.55.10:1976",
    "http://181.57.131.122:8080",
    "http://201.249.152.172:999",
    "http://102.38.17.193:8080",
    "http://103.174.102.127:80",
    "http://174.126.217.110:80",
    "http://154.79.254.236:32650",
    "http://85.172.0.30:8080",
    "http://181.65.169.35:999",
    "http://163.44.253.160:80",
    "http://38.51.49.84:999",
    "http://217.219.74.130:8888"
]

def get_proxy():
    proxy_str = random.choice(proxies)
    return {
        "http": proxy_str,
        "https": proxy_str
    }

def fetch(url):
    for attempt in range(5):
        proxy = get_proxy()
        try:
            print(f"Using proxy: {proxy['http']}")
            response = requests.get(url, proxies=proxy, timeout=10)
            if response.status_code == 429:
                print("429 Too Many Requests. Switching proxy...")
                time.sleep(5)
                continue
            return response.text
        except requests.RequestException as e:
            print("Error:", e)
            time.sleep(2)
            continue
    return None
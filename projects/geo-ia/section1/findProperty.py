import requests
import time

url = "https://hk.centanet.com/findproperty/api/estate/Search"
size = 30
resultCount = 10000#19448
maxPages = int(resultCount / size)+1

for pageCount in range(maxPages):
    payloadJSON = {
        "size": size,
        "sort": "NUnitPrice",
        "order": "Ascending",
        "offset": pageCount*size
    }

    r = requests.request("POST", url, data=str(payloadJSON), headers={'Content-Type': 'application/json'})

    with open(f"data/{pageCount}asc.json", "w+", encoding='utf-8') as f:
        f.write(r.text)

    print(f"{pageCount+1}/{maxPages} done.")

    if pageCount % 440 == 0:
        # after 450 consecutive connections, centaline will block requests,
        # so wait for 10 seconds before proceeding.
        time.sleep(10)
        print("Sleeping for 10 seconds.")
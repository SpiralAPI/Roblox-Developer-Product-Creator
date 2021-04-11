import requests # pip install requests
import time
# its a bit buggy at some times but it works pretty well

universeId = 1  # edit me to your games universe id
cookie = ""  # edit me to your cookie
amount = 1000 # edit me to your amount of dev products u want

cookies = {'.ROBLOSECURITY': str(cookie)}

price = 0  # dw, the price will go up to 1 2 3 4 etc
tokenQ = input("What is your X-CSRF Token? If you don't know, input any key and we will get it for you!: ") # question
token = tokenQ
print("estimated time: " + str(time.strftime('%H:%M:%S', time.gmtime(amount * 7))))

while True:
    if price >= amount:
        break
    else:
        try:
            price = price + 1
            DevelopAPIUrl = "https://www.roblox.com/places/developerproducts/add?universeId=" + str(universeId) + "&name=" + str(price) + "&developerProductId=0&priceInRobux=" + str(price) + "&description=Donation&imageAssetId="
            id = requests.post(DevelopAPIUrl, 
            cookies=cookies,
            headers={'x-csrf-token': str(token)})
            if id.status_code == 401:
                print("cookie invalid")
                break
            if id.status_code == 400:
                print("Bad request")
                break
            
            if id.status_code == 403:
                print("No access to creating developer products. Trying to get token value.")
                auth = 'https://auth.roblox.com/v2/logout'

                e = requests.post(
                    auth,
                    cookies=cookies,
                    )
                f = e.headers
                print(f.get("x-csrf-token") + " has been set as your CSRF Token!")
                token = f.get("x-csrf-token")
                price = price - 1
                
            if id.status_code == 404:
                print("universe not found or shopid invalid")
                print("you were on the dev product: " + str(price-1)) 
                break
            if id.status_code == 429:
                print("haha get ratelimited noob")
                print("you were on the dev product: " + str(price-1)) 
                break
            if id.status_code == 500:
                print("unknown error lol")
                print("you were on the dev product: " + str(price-1)) 
                break

            print("Developer Product #" + str(price) +
                " has been Created!")
            time.sleep(7) # i know its long but ratelimits be like that.
        except requests.exceptions.RequestException as e:
            print(e)
            

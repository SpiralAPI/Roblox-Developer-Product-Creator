# FlowTech Donation Center: How It's Made
## [Support FlowTech here!](https://www.roblox.com/games/13834736044/Support-FlowTech)

### Why explain the process?
FlowTech aims to be fully transparent and open source, and hopefully explaining this process can allow you to learn and expand your knowledge, especially if your just starting out!

## The Process
Firstly, i used an [old script](https://github.com/SpiralAPI/Roblox-Developer-Product-Creator/blob/main/main.py) i made about 2 years ago for mass creating developer products. I tried to make about 5000 developer products, but quickly realized a lot of developer products did not go through.

To combat this, I scraped the developer products using a script below to make a json file.

```py
import  requests
import  time
import  json
count = 1

while  True:
	r = requests.get(f"https://apis.roblox.com/developer-products/v1/universes/4797600429/developerproducts?pageNumber={count}&pageSize=100", cookies={'.ROBLOSECURITY': str("MY COOKIE HERE")})

	jsonn = r.json()
	try:
		jsonn[0]
	except:
		print("finished")
		break
	with  open("Untitled-1.json", "a") as  f:
	f.write(json.dumps(jsonn))
	print("saved page " + str(count))
	f.close()
	count = count + 1
	time.sleep(1)
```

This saved all the currently made developer products in to Untitled-1.json

Afterwards, I used [json to csv](https://www.convertcsv.com/json-to-csv.htm) converter, and then used an [online csv editor](https://www.convertcsv.com/csv-viewer-editor.htm) to remove all rows besides the id and name, and renamed the "name" row to "value"

I then used a [csv to json](https://www.convertcsv.com/csv-to-json.htm) converter and was returned with my new json file!

afterwards, I used an online [json sorter](https://codeshack.io/json-sorter/) to sort the "value" from lowest to highest. then I overwrote the Untitled-1.json file with the new sorted and edited json!

Afterwards, it was time to find and note down the missing values! I made the below script to automize this for me and put all the missing values in to a Python list object
```py
import  json

hi = None

values = []

missingvalues = []

with  open("Untitled-1.json", "r") as  f:
	hi = f.read()
	f.close()

j = json.loads(hi)

for  obj  in  j:
	list.append(values, obj["value"])

for  x  in  range(1, 5001):
	if  not  x  in  values:
		list.append(missingvalues, x)

print(*missingvalues, sep=",")
```
This successfully printed out a of missing values (I wont place it here because it was very long)

Finally, I made the following fork of my original script to help loop through the new list ive made and create the missing products!

```py
missingValues = [1, 2, 3, "etc..."]

import  requests  # pip install requests
import  time
from  os  import  system

# its a bit buggy at some times but it works pretty well
universeId = 4797600429  # edit me to your games universe id
cookie = "my cookie here"  # edit me to your cookie
cookies = {'.ROBLOSECURITY': str(cookie)}
tokenQ = input("What is your X-CSRF Token? If you don't know, input any key and we will get it for you!: ") # question
token = tokenQ

for  price  in  missingValues:
	try:
		DevelopAPIUrl = "https://www.roblox.com/places/developerproducts/add?universeId=" + str(universeId) + "&name=" + str(price) + "&developerProductId=0&priceInRobux=" + str(price) + "&description=Donation&imageAssetId="
		id = requests.post(DevelopAPIUrl, cookies=cookies, headers={'x-csrf-token': str(token)})
		
		if  id.status_code == 401:
			print("cookie invalid")
			print("you were on the dev product: " + str(price))
			break
		if  id.status_code == 400:
			print("Bad request")
			print(id.json())
			print("you were on the dev product: " + str(price))
			break
		if  id.status_code == 403:
			print("No access to creating developer products. Trying to get token value.")
			auth = 'https://auth.roblox.com/v2/logout'
			e = requests.post(auth, cookies=cookies)
			f = e.headers
			print(f.get("x-csrf-token") + " has been set as your CSRF Token!")
			token = f.get("x-csrf-token")
		if  id.status_code == 404:
			print("universe not found or shopid invalid")
			print("you were on the dev product: " + str(price))
			break
		if  id.status_code == 429:
			print("haha get ratelimited noob")
			print("you were on the dev product: " + str(price))
			break
		if  id.status_code == 500:
			print("unknown error lol")
			print("you were on the dev product: " + str(price))
			break

		print("Developer Product #" + str(price) + " has been Created!")
		system("title "+ "Estimated Time: " + str(time.strftime('%H:%M:%S', time.gmtime(len(missingValues) - list.index(missingValues, price)))))
		
		time.sleep(1) # i know its long but ratelimits be like that.
	except  requests.exceptions.RequestException  as  e:
		print(e)
```

Now that we had all our developer products finished, it was time to turn it in to a lua table! We repeat the steps from before:
> This saved all the currently made developer products in to Untitled-1.json

> Afterwards, I used [json to csv](https://www.convertcsv.com/json-to-csv.htm) converter, and then used an [online csv editor](https://www.convertcsv.com/csv-viewer-editor.htm) to remove all rows besides the id and name, and renamed the "name" row to "value"

> I then used a [csv to json](https://www.convertcsv.com/csv-to-json.htm) converter and was returned with my new json file!

and then used [LuaRocks](https://luarocks.org/) and [Lua5.4](https://www.lua.org/), running on the [Windows Linux Subsystem](https://learn.microsoft.com/en-us/windows/wsl/install), to run the following lua script and encode our json file in to a lua table

```lua
JSON = require("JSON")

local open = io.open

--both the below functions were pulled from stackoverflow
local  function  read_file(path)
	local file = open(path, "r") -- r read mode and b binary mode
	if  not file then  return  nil  end
	local content = file:read  "*a" -- *a or *all reads the whole file
	file:close()
	return content
end

function  dump(o)
	if  type(o) == 'table' then
		local s = '{ '
		for k,v in  pairs(o) do
			if  type(k) ~= 'number' then  k = '"'..k..'"' end
			s = s .. '['..k..'] = ' .. dump(v) .. ','
		end
		return s .. '} '
	else
		return  tostring(o)
	end
end

  

local fileContent = read_file("Untitled-1.json");
local decode = JSON:decode(fileContent)
local newFile = open("finalTable.lua", "w")

newFile:write(dump(decode))
newFile:close()
```

and that was it! We had a new file, "finalTable.lua", containing a lua table of all our developer products!

After some formatting, i was able to put the developer products in to a module in the game and then the rest was basic scripting! [The game is uncopylocked](https://www.roblox.com/games/13834736044/Support-FlowTech) for anyone who is curious, but I must warn you the table is very large and can cause lag! 

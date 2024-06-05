# Divar 🇮🇷


Developed by V1Z/Palas - 2024

# 1. Setup and Instalation
```
pip3 install divar
```

# Usage
Divar lib support both async and sync programming so youre free to use which one you like

```python
from divar import Client # its async client.
from divar import sync_client # its sync client as its name seggests!

AsyncDivarBot = Client()
SyncDivarBot = sync_client()
```

# Getting Category posts ( Agahi ha )
For that you just to need to call `GetCategory` method on your client object.
Example : 
```python
#async version be like :
await AsyncDivarBot.GetCategory('CityName', 'Category-Name' , *args , *kwargs)

#sync version be like :
SyncDivarBot.GetCategory('CityName', 'Category-Name' , *args , *kwargs)
```

# Searching in posts ( New Feature )
Its new feature added to lib for your requests and support <3
as method above i saied you need to call it from the client instance.
pass the query and also you can pass city codes to get more accurate posts from your city

Examples:
```python
#async version without cities specified returns posts all over IRAN 
await AsyncDivarBot.Search(query = 'iPhone 13')

#async version but cities specified > code hints : mashhad -> 3 , tehran -> 1 , isfahan -> 4
await AsyncDivarBot.Search(query = 'iPhone 13' , cities = [1,3,4])

#<-------------------------Sync version-------------------------/>
#sync version without cities specified returns posts all over IRAN 
syncDivarBot.Search(query = 'iPhone 13')

#sync version but cities specified > code hints : mashhad -> 3 , tehran -> 1 , isfahan -> 4
syncDivarBot.Search(query = 'iPhone 13' , cities = [1,3,4])
```

# Getting post info
Every post in Divar.ir has a Unique identifier named as **Token**.
you can find them at the end of url bar of a post or in methods below.

with `GetPost` method you can get info about the post like :
-Images
-Location
-Price
-Description
and etc.
```python
#<---------------------------Async Version-------------------------/>
await AsyncDivarBot.GetPost('Token')

#<---------------------------sync Version-------------------------/>
SyncDivarBot.GetPost('Token')
```

# Authentication (Login/Sign-Up)
Its new Feature implented abvisouly for your requests. 

Authentication is 2 step process , first you need to get otp code to your phone number
you can get that with `sign` method which is not friendly cause can be used for spamming since 
divar doesnt have anti spam algorithm or preventaion with their message service 
Second you need to login with that otp code on your phone number which returns a jwt-token to 
work with special methods (login needed) like `GetNumber` , you can do the second one with 
`login` method which needs your phone number and otp code.

Example:
```python
#<---------------------------Async Version-------------------------/>
await AsyncDivarBot.sign('0987654321') # send otp code (6digits) to the number if returns True else Flase.

#Now you need to login with the otp code (if login successful youre free to use special methods i said above)
await AsyncDivarBot.login('0987654321' , '123456')

#<---------------------------Sync Version-------------------------/>
syncDivarBot.sign('0987654321') # send otp code (6digits) to the number if returns True else Flase.

#Now you need to login with the otp code (if login successful youre free to use special methods i said above)
syncDivarBot.login('0987654321' , '123456')
```

# Getting Number of a post
Its login required method so if you didnt login with above method it will ask for your number 
and your otp code and itll login you if youre not , **pass the Token of post as first arg**.

```python
#<---------------------------Async Version-------------------------/>
await AsyncDivarBot.GetNumber('PostToken')

#<---------------------------Sync Version-------------------------/>
syncDuvarBot.GetNumber('PostToken')
```

# New Feature Comming in v2.5:
- Divar Chat 
- Map specifing
- and more...

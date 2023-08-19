# DivarApi 

Under construction! Not compelitly ready for use yet! Currently experimenting and planning!

English / [فارسی - Farsi](README_fa.md)

Developed by Palas - 2023

# Examples - getting newest annon from a city (Buggy Alpha Version)

## 1. Install the pkg using pip
```
pip3 install DivarApi
```

Creating A Client

```python
from DivarApi.core import Client

Bot = Client()
# on this example we want to get the data from mashhad city and buy-apartment category
Bot.get_newest_category('mashhad' , 'buy-apartment')

# it returns a bs4 instance , you can specify if you want to have it as json with jsonify = true argument and more...
```

## Getting Number from Token and id
Every post and annon in Divar.ir contains a Token that you can use to get phone number 

e.x -> https://divar.ir/v/title/AZgVLMTF
Token is after the title (end of the url) and in this example its { AZgVLMTF }
you can get the phone number using the get_number method as :

```python
from DivarApi.core import Client

Bot = Client()

# if method doesnt work correctly plz use your own jwt token in header
Bot.get_number(AZgVLMTF)
# if this token exists and has a phone number youll get it 
# but if the number is hidden , itll returns Hidden Number!
```

## Getting Image of a post ( annon )
To use this feature you should pass an ID and Token of a post , also you should specify headers fully
how to get ID of a post?
in every image link related to a post you can find it , also you can use the get_newest_category() and there you can find related field get tagged there before the token , i mean :

https://s101.divarcdn.com/static/pictures/1692404705/AZVD2hGi.jpg

in this example , the id is 1692404705 and the token is AZVD2hGi
so you can get the image through get_post_pic:

```python
from DivarApi.core import Client

Bot = Client(header:dict)
Bot.get_post_pic(1692404705 , 'AZVD2hGi' , path = 'E:\\download\basefolder')

#if your jwt token which should be in cookie inside header was expired you'll get this error:
#the cookie you specified is not correct! or jwt is expired
# or if the link was incorrect you'll get statuscode - Bad request

```

## Check out GitHub for more: https://GitHub.com/PalasOnGithub
## star the rep on github <3
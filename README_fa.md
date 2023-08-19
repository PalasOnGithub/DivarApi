# DivarApi 
# دیوار Api

فارسی - Farsi / [English](README.md)

توسعه داده شده توسط پالاس" 2023 - 1402

# راهنمای سریع - به دست اوردن جدیدترین اگهی های یک شهر

## 1. Install the pkg using pip
## 1. در مرحله اول کتابخانه را نصب کنید
```
pip3 install DivarApi
```

2. یک کلاینت بسازید 
یک کلاینت میتواند ورودی های زیادی داشته باشد به طور مثال 
```
from DivarApi.core import Client

Bot = Client(header:dict , db_usage:bool , db_name:str)
```
در مثال بالا ما یک کلاینت ساختیم و به ان مقدار هدر در قالب دیکشنری پایتون را دادیم
همینطور اگر میخواهید اطلاعاتتان در دیتابیس ساخته شود نیاز است دی بی یوزیج را ترو تعریف کنید
اگر دی بی یوزیج برابر ترو باشد باید نامی برای دیتابیس تعریف کنید که باید پسوند زیر را داشته باشد.
```
Bot = Client(header:dict , db_usage=True , db_name='<yourdbname>.sqlite3)
```

میتوانید از متد زیر برای دریافت جدیدترین اگهی ها استفاده کنید
به عنوان ورودی باید شهر و دسته بندی را وارد کنید

```python
from DivarApi.core import Client

Bot = Client()
# on this example we want to get the data from mashhad city and buy-apartment category
Bot.get_newest_category('mashhad' , 'buy-apartment')

# it returns a bs4 instance , you can specify if you want to have it as json with jsonify = true argument and more...
```

## به دست اوردن شماره تلفن با توکن اگهی
هر اگهی در دیوار یک توکن دارد که با ان میتوانید اطلاعات اگهی را به دست اورید

https://divar.ir/v/title/AZgVLMTF <- به طور مثال  
AZgVLMTF توکن بعد از تایتل قرار دارد در این مثال برابر است با 

میتوانید با استفاده از متد زیر اطلاعات تلفن یک اگهی را به دست اروید 
دقت کنید نیاز است تا هدر را ست کنید و کوکی یا جی تی دبل توکن خود را جایگذین کنید

```python
from DivarApi.core import Client

Bot = Client(header = {'USER-AGENT' : ....... , 'Cookie':.......})

# if method doesnt work correctly plz use your own jwt token in header
Bot.get_number(AZgVLMTF)
# if this token exists and has a phone number youll get it 
# but if the number is hidden , itll returns Hidden Number!
```

## به دست اوردن تصاویر یک اگهی در دیوار

برای استفاده از این قابلیت نیاز است ایدی و توکن اگهی را وارد کنید
چطور ایدی یک اگهی را به دست اورید؟

میتوانید در هر لینک یک اگهی ان را پیدا کتید قبل از توکن قرار دارد یا میتوانید از اولین متد استفاده کنید
به طور مثال در لینک زیر به این صورت است

https://s101.divarcdn.com/static/pictures/1692404705/AZVD2hGi.jpg

در این لینک ایدی برابر 1692404705 است

ID = 1692404705
Token = AZVD2hGi

برای به دست اوردن عکس میتوانید از متد زیر استفاده کنید

```python
from DivarApi.core import Client

Bot = Client(header:dict)
Bot.get_post_pic(1692404705 , 'AZVD2hGi' , path = 'E:\\download\basefolder')

#if your jwt token which should be in cookie inside header was expired you'll get this error:
#the cookie you specified is not correct! or jwt is expired
# or if the link was incorrect you'll get statuscode - Bad request

```

## https://GitHub.com/PalasOnGithub برای اطلاعات بیشتر گیت هاب را دنبال کنید
## با ستاره دادن به این پروژه از ما حمایت کنید
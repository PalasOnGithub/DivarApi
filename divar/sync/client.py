import logging
#import locals
from .raw import *

log = logging.getLogger(__name__)

class Client:
	__slots__ = ('header' , 'jwt_token' , 'timeout')
	Unique_JWT = None

	def __init__(self , header: dict=None , jwt_token: str | dict=None , timeout: int=5):
		"""Divar Client.

		Parameters:
			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			jwt_token (``str``, ``dict``, *optional*):
				jwt token for authenthicating and getting phone numbers. 
				Examples - > `Basic iquhieh78y8fhiuwefnc87h3nqjkncjknweuicnw78n78yuguy`

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`Client` a Client obj will return if everything is ok.
		"""

		self.header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
		self.jwt_token = jwt_token
		self.timeout = timeout

	def GetCategory(self ,city: str, category_name: str, pagination: int=1, header: str | dict=None , timeout: int=None) -> list:
		"""Getting category posts.

		Parameters:
			city (``str``):
				Unique identifier ( str ) of the target city.
				its on the url usuaaly when you visit divar.ir 
				Examples -> mashhad - tehran - tabriz - karaj and etc.

			category_name (``str``):
				caregory name in the url bar of divar.ir.
				Examples -> vehicles - electronic-devices - mobile-tablet and etc.

			pagination (``int``, *optional*):
				The pagination to be applied on each search.
				Defaults to 1 (each page returns last 23 posts)
				The algorithm of it :
				1st pagination : first 23 objects
				2nd pagination : last 23-46 objects
				and etc. 

			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`list` a list will return if the request and response was ok.

		Example:
			.. code-block:: python

				# Simple example
				client.get_catrgory("tehran", "mobile-tablet" , pagination = 5 , *args , *kwargs)

		Errors:
			`divar.errors.invalid_url`: happens when the city/category is not correct.
			`divar.errors.empty_pagination`: happens when the category doesnt have that much posts for the pag.
			`divar.errors.invalid_header`: happens when the request header is invalid.
		"""
		if header is None:
			header = self.header
		if timeout is None:
			timeout = self.timeout

		return get_category(city, category_name, pagination, header , timeout)

	def GetPost(self ,Token:str , header: str | dict=None , timeout: int=None) -> dict:
		"""Getting post info.

		Parameters:
			Token (``str``):
				Unique identifier ( str ) of the target post.
				its on the url usuaaly when you visit divar.ir 
				Examples -> ABCD45YH - 7656hBtUn - 7854GFvfg and etc.

			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`dict` a dictionary will return if the request and response was ok.

		Example:
			.. code-block:: python

				# Simple example
				client.get_post("ABCD45YH", header = {...}, timeot = 3 , *args , *kwargs)

		Errors:
			`divar.errors.invalid_url`: happens when the city/category is not correct.
			`divar.errors.invalid_header`: happens when the request header is invalid.
			`divar.errors.rpc_error`: happens when the user is forbidden for divar servers.
		"""
		if header is None:
			header = self.header

		return get_post(Token , header)

	def Search(self ,query: str,cities: list=None, header: dict=None, timeout: int=3) -> list:
		"""Search for posts.

		Parameters:
			Query (``str``):
				the query you wanna use for search
				Example - > iPhone 13 Pro max - ساعت اپل واچ

			Cities (``list[Union[int]]`` , *optional*):
				exact code of cities you wanna search in (all cities if not provided).
				Example - > Tehran code : 1
				Mashhad code : 3
				Isfahan code : 4
				you can find your city code in search bar of divar.ir

			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`list` a list will return if the request and response was ok.

		Example:
			.. code-block:: python

				# Simple example
				client.search_posts("اپل iPhone 11 با حافظهٔ ۱۲۸ گیگابایت", header = {...}, timeout = 3 , *args , *kwargs)

		Errors:
			`divar.errors.invalid_url`: happens when the city/category is not correct.
			`divar.errors.invalid_header`: happens when the request header is invalid.
			`divar.errors.rpc_error`: happens when the user is forbidden for divar servers.
		"""
		if header is None:
			header = self.header
		if timeout is None:
			timeout = self.timeout

		return search_posts(query , cities , header , timeout)

	def sign(self , phone_number: str, header: dict=None, timeout: int=None) -> bool:
		"""Otp requester.

		Parameters:
			PhoneNumber (``str``):
				The PhoneNumber to recieve otp code for authenticating.
				Examples -> 09987654321 (dont use +98 at beginning)

			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`Boolean` a Boolean will return if the request and response was ok (True if ok, Flase if not).

		Example:
			.. code-block:: python

				# Simple example
				client.authmaker(09987654321, header = {...}, timeout = 3 , *args , *kwargs)

		Errors:
			`divar.errors.invalid_url`: happens when the city/category is not correct.
			`divar.errors.invalid_header`: happens when the request header is invalid.
		"""
		if header is None:
			header = self.header
		if timeout is None:
			timeout = self.timeout

		return authmaker(phone_number , header , timeout)

	def login(self, phone_number: str, otp_code: str | int, header: dict=None, timeout: int=None) -> str:
		"""Authenticater( login/sign-up ).

		Parameters:
			PhoneNumber (``str``):
				The PhoneNumber to recieve otp code for authenticating.
				Examples -> 09987654321 (dont use +98 at beginning)

			OtpCode (``str``, ``int``):
				The otp code you recieved when calling authmaker method.
				Its 6 digit number.

			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`Jwt Token(str)` a String will return if the request and response was ok (True if ok, Flase if not).

		Example:
			.. code-block:: python

				# Simple example
				client.auth(09987654321, 123456, header = {...}, timeout = 3 , *args , *kwargs)

		Errors:
			`divar.errors.invalid_url`: happens when the city/category is not correct.
			`divar.errors.invalid_header`: happens when the request header is invalid.
		"""
		if header is None:
			header = self.header
		if timeout is None:
			timeout = self.timeout
		return auth(phone_number , otp_code , header , timeout)

	def GetNumber(self ,Token: str , _authorization: str | dict=None, header: dict=None, timeout: int=None) -> int | str:
		"""Getting post phone number.

		Parameters:
			Token (``str``):
				Unique identifier ( str ) of the target post.
				its on the url usuaaly when you visit divar.ir 
				Examples -> ABCD45YH - 7656hBtUn - 7854GFvfg and etc.

			_authorization (``str``, ``dict``, *JWT TOKEN type*):
				jwt token in form of string or dict (Login required method). 
				Example -> Basic iwhfieuhfihwef8723y8hiu34f4cgui4ckb4uc34c7v634b

			header (``str``, ``dict``, *optional*):
				header of the request to send for divar servers. 
				Examples - > {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

			timeout (``int``, *optional*):
				maximum time to wait for response or request to arrive.
				Defaults to 3 seconds.

		Returns:
			`dict` a dictionary will return if the request and response was ok.

		Example:
			.. code-block:: python

				# Simple example
				client.get_number("ABCD45YH", _authorization = {...} | 'bluhbluhbluh', timeout = 3 , *args , *kwargs)

		Errors:
			`divar.errors.invalid_url`: happens when the city/category is not correct.
			`divar.errors.invalid_header`: happens when the request header is invalid.
			`divar.errors.rpc_error`: happens when the user is forbidden for divar servers.
			`divar.errors.invalid_auth`: happens when the user isnt authenticated or jwt token expired.
		"""
		if header is None:
			header = self.header
		if timeout is None:
			timeout = self.timeout

		if _authorization is not None:
			return get_number(Token , _authorization , header , timeout)
		
		elif (_authorization is None) and Client.Unique_JWT is not None:
			return get_number(Token , Client.Unique_JWT , header , timeout)

		else:
			co_loop = False
			while not co_loop:
				try:
					number = input('Please insert a number to login : ')
					code_req = self.sign(number , header , timeout)
					code = input(f'Sent OTP code to {number}' + '\nPlease insert the otp code to login : ')
					jwt = auth(number , code , self.header , self.timeout)
					Client.Unique_JWT = jwt

					co_loop = True
				except Exception as error:
					print(error)
					log.info(error)
			
			return get_number(Token , Client.Unique_JWT , header , timeout)

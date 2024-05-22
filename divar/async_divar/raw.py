import aiohttp
import logging

#local imports
from .errors import *

log = logging.getLogger(__name__)

async def get_category(city:str , category_name:str , pagination: int=1 , header: str | dict=None , timeout: int=3) -> list:
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
			await client.get_catrgory("tehran", "mobile-tablet" , pagination = 5 , *args , *kwargs)

	Errors:
		`divar.errors.invalid_url`: happens when the city/category is not correct.
		`divar.errors.empty_pagination`: happens when the category doesnt have that much posts for the pag.
		`divar.errors.invalid_header`: happens when the request header is invalid.
	"""
	try:
		async with aiohttp.ClientSession() as session:
			header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
			url = f'https://api.divar.ir/v8/web-search/{city.lower()}/{category_name.lower()}?page={pagination}'
			resp_list = list.__call__()

			try:
				async with session.get(headers=header, url=url, timeout=timeout) as response:
					if response.status == 200 or 201:
						try:
							data = await response.json()
						except:
							data = await response.json(content_type=None)

						for item in data['web_widgets']['post_list']:
							if item['data']:
								try:
									respon_dict = dict()
									respon_dict['Price'] = item['data']['middle_description_text']

									respon_dict['Title'] = item['data']['title'] 
									respon_dict['Status'] = item['data']['top_description_text']
									respon_dict['Loc_time']= item['data']['bottom_description_text'] 
									respon_dict['Exact_loc'] = item['data']['action']['payload']['web_info']['district_persian']  
									respon_dict['Slug'] = item['data']['action']['payload']['web_info']['category_slug_persian'] 
									respon_dict['Token'] = item['data']['token']
									respon_dict['IsVerified'] = item['data']['is_checked'] 
									respon_dict['CanChat'] = item['data']['has_chat'] 
									respon_dict['ImgCount'] = int(item['data']['image_count'])
									respon_dict['MainImg'] = item['data']['image_url'][1]['src']

									resp_list.append(respon_dict)
								except KeyError:
									raise invalid_url('invalid token / city / category')

								except Exception as e:
									raise e
						return resp_list

					else:
						raise rpc_error('Response status from divar servers show that youre forbidden user. (Try changing ip and header)')

			except aiohttp.ClientConnectionError:
				raise invalid_url(f'Tried to make request to city: {city} / category: {category_name} failed due to invalid url.')
			
			except ValueError as val_error:
				raise invalid_header(f'Tried to make request to divar servers but the provided headers are not correct.\n\nMore info: {val_error}')

	except Exception as unk_error:
		raise unk_error

async def get_post(Token:str , header: str | dict=None) -> dict:
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
			await client.get_post("ABCD45YH", header = {...}, timeot = 3 , *args , *kwargs)

	Errors:
		`divar.errors.invalid_url`: happens when the city/category is not correct.
		`divar.errors.invalid_header`: happens when the request header is invalid.
		`divar.errors.rpc_error`: happens when the user is forbidden for divar servers.
	"""
	try:
		async with aiohttp.ClientSession() as session:
			header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
			url = f'https://api.divar.ir/v8/posts-v2/web/{Token}'

			try:
				async with session.get(url=url, headers=header) as response:
					if response.status == 200 or 201:
						try:
							data = await response.json()
						except:
							data = await response.json(content_type=None)

						result_dict = dict.__call__()
						try:
							title = data["sections"][1]["widgets"][0]["data"]["title"]
							result_dict["عنوان"] = title
							# Get the description
							try:
								description = data["sections"][2]["widgets"][1]["data"]["text"]
								result_dict["توضیحات"] = description

							except IndexError:
								description = data["sections"][3]["widgets"][1]["data"]["text"]
								result_dict["توضیحات"] = description
								
							# Get all images
							images = [item["image"]["url"] for item in data["sections"][3]["widgets"][0]["data"]["items"]]
							result_dict["images"] = images
							
							for field in data["sections"][4]["widgets"]:
								try:
									result_dict[field["data"]["title"]] = field["data"]["value"]
								except Exception:
									pass
									
							return result_dict
						except KeyError:
							raise invalid_url('invalid token / city / category')

						except Exception as e:
							raise e

					else:
						raise rpc_error('Response status from divar servers show that youre forbidden user. (Try changing ip and header)')

			except aiohttp.ClientConnectionError:
				raise invalid_url(f'Tried to make request to city / category failed due to invalid url.')
			
			except ValueError as val_error:
				raise invalid_header(f'Tried to make request to divar servers but the provided headers are not correct.\n\nMore info: {val_error}')

	except Exception as unk_error:
		raise unk_error

async def get_number(Token: str , _authorization: str | dict , header: dict=None, timeout: int=3) -> int | str:
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
			await client.get_number("ABCD45YH", _authorization = {...} | 'bluhbluhbluh', timeout = 3 , *args , *kwargs)

	Errors:
		`divar.errors.invalid_url`: happens when the city/category is not correct.
		`divar.errors.invalid_header`: happens when the request header is invalid.
		`divar.errors.rpc_error`: happens when the user is forbidden for divar servers.
		`divar.errors.invalid_auth`: happens when the user isnt authenticated or jwt token expired.
	"""
	try:
		async with aiohttp.ClientSession() as session:
			header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
			header = _authorization | header if type(_authorization) == dict else {'Authorization' : 'Basic ' + _authorization} | header
			url = f"https://api.divar.ir/v8/postcontact/web/contact_info/{Token}"

			try:
				async with session.get(url=url, headers=header) as response:
					if response.status == 200 or 201:
						try:
							data = await response.json()
						except:
							data = await response.json(content_type=None)

						try:
							if data['widget_list'][0]['data']['title'] == '\u0634\u0645\u0627\u0631\u0647 \u0645\u062e\u0641\u06cc \u0634\u062f\u0647 \u0627\u0633\u062a':
								return 'Hidden Number!'
							
							else:
								return int(data['widget_list'][0]['data']['action']['payload']['phone_number'])

						except KeyError as e:
							raise invalid_url('invalid token provided')

						except Exception as e:
							raise e

					else:
						raise rpc_error('Response status from divar servers show that youre forbidden user. (Try changing ip and header)')

			except aiohttp.ClientConnectionError:
				raise invalid_url(f'Tried to make request to city / category failed due to invalid url.')
			
			except ValueError as val_error:
				raise invalid_header(f'Tried to make request to divar servers but the provided headers are not correct.\n\nMore info: {val_error}')

	except Exception as unk_error:
		raise invalid_auth('invalid jwt token or expired!')

async def search_posts(query: str,cities: list=None, header: dict=None, timeout: int=3) -> list:
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
			await client.search_posts("اپل iPhone 11 با حافظهٔ ۱۲۸ گیگابایت", header = {...}, timeout = 3 , *args , *kwargs)

	Errors:
		`divar.errors.invalid_url`: happens when the city/category is not correct.
		`divar.errors.invalid_header`: happens when the request header is invalid.
		`divar.errors.rpc_error`: happens when the user is forbidden for divar servers.
	"""

	try:
		async with aiohttp.ClientSession() as session:
			header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
			cities = [str(city) for city in cities] if cities is not None else None
			url = f'https://api.divar.ir/v8/web-search/iran?cities={",".join(cities)}&q={query}' if cities is not None else f'https://api.divar.ir/v8/web-search/iran?q={query}'
			resp_list = list.__call__()

			try:
				async with session.get(headers=header, url=url, timeout=timeout) as response:
					if response.status == 200 or 201:
						try:
							data = await response.json()
						except:
							data = await response.json(content_type=None)

						for item in data['web_widgets']['post_list'][1:]:
							if item['data']:
								try:
									respon_dict = dict()
									respon_dict['Price'] = item['data']['middle_description_text']

									respon_dict['Title'] = item['data']['title'] 
									respon_dict['Status'] = item['data']['top_description_text']
									respon_dict['Loc_time']= item['data']['bottom_description_text'] 
									respon_dict['Exact_loc'] = item['data']['action']['payload']['web_info']['district_persian']  
									respon_dict['Slug'] = item['data']['action']['payload']['web_info']['category_slug_persian'] 
									respon_dict['Token'] = item['data']['token']
									respon_dict['IsVerified'] = item['data']['is_checked'] 
									respon_dict['CanChat'] = item['data']['has_chat'] 
									respon_dict['ImgCount'] = int(item['data']['image_count'])
									respon_dict['MainImg'] = item['data']['image_url'][1]['src']

									resp_list.append(respon_dict)
								except KeyError as err:
									log.info(err)
									pass

								except Exception as e:
									raise e
						return resp_list

					else:
						raise rpc_error('Response status from divar servers show that youre forbidden user. (Try changing ip and header)')

			except aiohttp.ClientConnectionError as err:
				raise invalid_url(f'Tried to make request to city / category failed due to invalid url.')
			
			except ValueError as val_error:
				raise invalid_header(f'Tried to make request to divar servers but the provided headers are not correct.\n\nMore info: {val_error}')

	except Exception as unk_error:
		raise unk_error

async def authmaker(phone_nubmber: str, header: dict=None, timeout: int=5) -> bool:
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
			await client.authmaker(09987654321, header = {...}, timeout = 3 , *args , *kwargs)

	Errors:
		`divar.errors.invalid_url`: happens when the city/category is not correct.
		`divar.errors.invalid_header`: happens when the request header is invalid.
	"""
	try:
		async with aiohttp.ClientSession() as session:
			header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
			url = f'https://api.divar.ir/v5/auth/authenticate'
			payload = {'phone' : str(phone_nubmber)}

			try:
				async with session.post(headers=header, json=payload, url=url, timeout=timeout) as response:
					if response.status == 200 or 201:
						return True
					return False

			except aiohttp.ClientConnectionError as err:
				raise invalid_url(f'Tried to make request to city / category failed due to invalid url.')
			
			except ValueError as val_error:
				raise invalid_header(f'Tried to make request to divar servers but the provided headers are not correct.\n\nMore info: {val_error}')

	except Exception as unk_error:
		raise unk_error

async def auth(phone_number: str, otp_code: str | int, header: dict=None, timeout: int=5) -> str:
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
			await client.auth(09987654321, 123456, header = {...}, timeout = 3 , *args , *kwargs)

	Errors:
		`divar.errors.invalid_url`: happens when the city/category is not correct.
		`divar.errors.invalid_header`: happens when the request header is invalid.
	"""
	try:
		async with aiohttp.ClientSession() as session:
			header = header if header is not None else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
			url = f'https://api.divar.ir/v5/auth/confirm'
			payload = {'phone' : str(phone_number), 'code' : str(otp_code)}

			try:
				async with session.post(headers=header, json=payload, url=url, timeout=timeout) as response:
					if response.status == 200 or 201:
						res = await response.json()
						return res['token']

			except aiohttp.ClientConnectionError as err:
				raise invalid_url(f'Tried to make request to city / category failed due to invalid url.')
			
			except ValueError as val_error:
				raise invalid_header(f'Tried to make request to divar servers but the provided headers are not correct.\n\nMore info: {val_error}')

	except Exception as unk_error:
		raise unk_error

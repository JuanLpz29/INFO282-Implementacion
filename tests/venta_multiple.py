import requests
from concurrent.futures import ThreadPoolExecutor

workers = 4


def post_url(args):
    return requests.post(args)

# url = 'http://127.0.0.1:5000/ventas/?nombre=tester'
url = 'https://hiawvp.pythonanywhere.com/ventas/?nombre=tester'

list_of_urls = [f"{url}{i}&codigoBarra=7804300122140" for i in range(workers)]


with ThreadPoolExecutor(max_workers=workers) as pool:
    response_list = list(pool.map(post_url, list_of_urls))


for response in response_list:
    print(response, response.json())

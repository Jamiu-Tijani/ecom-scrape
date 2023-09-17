import subprocess
from bs4 import BeautifulSoup as bs
import asyncio
from .models import Products
def ebay_scraper():

    # Define the Bash command you want to run
    bash_command = """curl 'https://www.ebay.com/globaldeals' \
  -H 'authority: www.ebay.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: max-age=0' \
  -H 'cookie: ak_bmsc=4159F22D028997A60F5F5283A2456E58~000000000000000000000000000000~YAAQb9MRAiO51nmKAQAAjV+NohWc8ijzl7/oKEPnAi94QbZNYKnHNt+3b1cQud61YKUHhVvpcq+gd00FmK1vsi5WlRKbFyV1WghVg37azjmc+A7K69fuydlza2vpzc2Dt5KHVFjDr9yxF5vL40RTOl/+bKo7agAWTMGBYzw5bGpIu3LHzkPXDGur9ZoDznjKDxyRdO7ui8Dwj8r0ESRZ1lKP5h6d0g3XOhLv2PXFM5QoUkE4z+1Vmw1mstH3X7n4cJoORoAk0K/mls97jQNoIuqRiJvFN81zRBTlo7x1H+HT1I3NXZlaIDD3TS1OYeOPDxxsx5c3+0oMDO1f9HWfk75HU+1/YdCnv6USQPxYfOCcHSYtj+TJm7ywuSvUVW/sgDK5177c9LA=; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=c57621db-4c3e-4d56-ac05-0a37e1844f81; __uzmbj2=1694944290; s=CgAD4ACBlCB2qYTI4ZDVlY2MxOGEwYTY0NjllOGI0NTg5ZmZmZDhkZWMlaAzj; bm_sv=52ABA35B7890B294CBBEA81CFC9F40A9~YAAQb9MRAnu71nmKAQAAqMKNohUoQHxFI6aa/vokRUuyTdtNVLo8MYk8z1+g64YVeBT8tKHrBSOxRVMcRipF12Awgz+YcktYRfIvjSMaNpKp/5Wz+YQeraieZlNZeNaI/lINAklpGyvAyzTXS/BNGS69XVnvfxTOcuVfDIXiB6HJ8aKzNFyqOoINopaNUq5COd35aDd8SiHbL0PCZ+LRKd0OePo33vFFM+GPtxJF3zjVvtly0gqeTR9sTiR9dw==~1; __uzmcj2=576872243879; __uzmdj2=1694944314; ebay=%5Ejs%3D1%5Esbf%3D%23000000%5Epsi%3DAjbpgHTM*%5E; dp1=bpbf/%238000e0000000000000000066e7ffd1^bl/NG68c93351^; nonsession=BAQAAAYpI47hYAAaAADMABmbn/9ExMDAyMTEAygAgaMkzUWEyOGQ1ZWNjMThhMGE2NDY5ZThiNDU4OWZmZmQ4ZGVjAMsAAmUG01kxNpOM76VyaquYgLrddKAoHD9952OE; __deba=8gYlI5du7D-AVePBqVGisH5ILsCcRnUBzTKqsasexVKuWzoNOC07jp2Tq0N96RA5XR8UW1J2_XMwSXzXGqPFGPHRv6C6s6FzkPiOrD2JrRuZfKoVwfb0yuYyxXmIgJIa79HxN6fQQaYpUnWBmWIx4g==; ds2=asotr/b8yMyzh2z2zz^sotr/b8yMyzzzzzzz^' \
  -H 'sec-ch-ua: "Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"' \
  -H 'sec-ch-ua-full-version: "112.0.5615.49"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-model: ""' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-ch-ua-platform-version: "6.1.0"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' \
  --compressed"""

    # Run the Bash command
    try:
        result = subprocess.run(bash_command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    li = bs(result.stdout,'html.parser').find_all("div", {"class":"dne-itemtile-detail"})
    data = {
    "product_title": [x.find("h3").text for x in li ],
    "product_url": [x.find("a").get("href") for x in li],
    "product_price": [x.find("div", {"class":"dne-itemtile-price"}).text for x in li],
    "product_image": [x.find("img").get("href") for x in li if x.find("img")]

}
    return data


class Scraper:

    @staticmethod
    async def scrape_product():
        loop = asyncio.get_event_loop()

        def scrape_product_data(data):
            i = 0
            while i < len(data):
                p  = Products.objects.create(title= data["product_title"][i],price= data["product_price"][i], url =data["product_url"][i] )
                p.save()
                i = i +1
        data = ebay_scraper()
        loop.run_in_executor(None, scrape_product_data, data)
        return {'status': 200, 'success': 'Scraper started successfully'}
        

class ProductService:

    @staticmethod
    def serialize_product(product):
        data = {
            'title': product.title,
            'price': product.price,
            'url': product.url,
            'source': product.source
            #'image': product.image  # Add image field if available in your model
        }
        return data

    @staticmethod
    def fetch_products():
        products = Products.objects.all()
        serialized_products = [ProductService.serialize_product(product) for product in products]
        return {'status': 200, 'success': 'Product fetch successful', 'data': serialized_products}













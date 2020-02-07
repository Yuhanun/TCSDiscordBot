import aiohttp
from pyquery import PyQuery


async def get(self, brand):
    host = "https://www.biernet.nl"
    biernet_url = host + "/bier/merken/" + brand + "/"
    try:
        session = self.bot._session
        async with session.get(biernet_url) as resp:
            webpage = await resp.text()
    except aiohttp.ClientConnectorError as e:
        raise e
    root = PyQuery(webpage)

    title = root('title').html()
    if title.startswith("Biermerken") or title.startswith("404"):
        raise ValueError(brand + ' not found')

    image = root('div#verrander')("img").attr('data-src')
    if image is None:
        raise ValueError(brand + ' not found')
    image = host + image

    cheapest_div = root('div#BekijkAlleWinkels')
    url_element = cheapest_div('a')
    shop_url = host + url_element.attr('href')
    shop_image = host + url_element('img').attr('data-src')
    shop_name = shop_url.split('--')[-1]
    shop_name = shop_name.replace('-', ' ').title()
    text = cheapest_div('p')
    original_price = text('.van_prijs')[0].text
    sale_price = text('.aanbiedingPrijsPPC')[0].text
    return [biernet_url, image, shop_name, shop_url, shop_image, original_price, sale_price]
import aiohttp
from pyquery import PyQuery
import re
import urllib.parse


async def get_search(self, args):
    biernet_url = "https://www.biernet.nl/site/php/data/aanbiedingen.php"
    try:
        session = self.bot._session
        # Send a post request with the provided arguments
        async with session.post(biernet_url, data=args) as resp:
            # Return the webpage
            return await resp.text()
    except aiohttp.ClientConnectorError as e:
        raise e


async def search(self, search_term):
    search_term = search_term.replace(" ", "-")
    # First try finding crates with the search term as brand name
    webpage = await get_search(self, {'zoeken': 'true', 'merk': search_term, 'kratten': 'krat-alle'})
    url = PyQuery(webpage)('a.merkenUrl').attr('href')
    if url is None:
        # Try finding crates with the search term as search term
        webpage = await get_search(self, {'zoeken': 'true', 'zoek': search_term, 'kratten': 'krat-alle'})
        url = PyQuery(webpage)('a.merkenUrl').attr('href')
        if url is None:
            # Try finding other offers (not crates) with the search term as brand name
            webpage = await get_search(self, {'zoeken': 'true', 'merk': search_term})
            url = PyQuery(webpage)('a.merkenUrl').attr('href')
            if url is None:
                # Try finding other offers with the search term as search term
                webpage = await get_search(self, {'zoeken': 'true', 'zoek': search_term})
                url = PyQuery(webpage)('a.merkenUrl').attr('href')
                if url is None:
                    # If nothing is found, we could always try the search term as result
                    return search_term
    # Return only the last part of /bier/merken/[name]
    return url.split("/")[-1]


async def get(self, brand):
    host = "https://www.biernet.nl"
    biernet_url = host + "/bier/merken/" + brand + "/"
    try:
        session = self.bot._session
        # Get the biernet page for the provided beer
        async with session.get(biernet_url) as resp:
            webpage = await resp.text()
    except aiohttp.ClientConnectorError as e:
        raise e
    root = PyQuery(webpage)

    title = root('title').html()
    # Check if the beer could be found
    if title.startswith("Biermerken") or title.startswith("404"):
        raise ValueError(brand + ' not found, or not on sale')

    image = root('div#verrander')("img").attr('data-src')
    # Sometimes we get a webpage with another title than "Biermerken" or "404" but there is no sale information
    #   (i.e. there is no img (and other data) where we would expect it), if this happens, also return not found
    if image is None:
        raise ValueError(brand + ' not found, or not on sale')
    image = host + image

    # Get all the various information from the HTML page
    cheapest_div = root('div#BekijkAlleWinkels')

    url_element = cheapest_div('a')
    shop_url = host + url_element.attr('href')
    shop_image = host + url_element('img').attr('data-src')

    shop_name = shop_url.split('--')[-1]
    shop_name = shop_name.replace('-', ' ').title()

    text = cheapest_div('p')

    try:
        original_price = text('.van_prijs')[0].text
        sale_price = text('.aanbiedingPrijsPPC')[0].text
    except IndexError:
        # Sometimes we find a beer that is not on sale so there is no '.van_prijs' or '.aanbiedingPrijsPPC',
        # we can then find the sale price using this regex
        sale_price = re.search("€.*(?= per )", text.text()).group()
        original_price = " "

    # Encode the URLs that we found, so Discord does not freak out over URLs with spaces, etc.
    biernet_url = urllib.parse.quote(biernet_url, safe=':/%')
    image = urllib.parse.quote(image, safe=':/%')
    shop_url = urllib.parse.quote(shop_url, safe=':/%')
    shop_image = urllib.parse.quote(shop_image, safe=':/%')

    return {'url': biernet_url, 'name': title.split("|")[0], 'img': image,
            'shop_name': shop_name, 'shop_url': shop_url, 'shop_img': shop_image, 'original_price': original_price,
            'sale_price': sale_price}

from pyquery import PyQuery    

async def get(self, brand):
    host = "https://www.biernet.nl"
    try:
        session = self.bot._session
        async with session.get(host+"/bier/merken/"+brand+"/") as resp:
            webpage = await resp.text()
    except aiohttp.ClientConnectorError as e:
        raise e
    root = PyQuery(webpage)

    title = root('title').html()
    if title.startswith("Biermerken") or title.startswith("404"):
        raise ValueError(brand+' not found')

    image = root('div#verrander')("img").attr('data-src')
    if image == None:
        raise ValueError(brand+' not found')
    
    return host+image
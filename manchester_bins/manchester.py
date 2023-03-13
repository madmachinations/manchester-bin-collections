#!/usr/bin/env python3

import aiohttp
from bs4 import BeautifulSoup
import datetime
import hashlib
# import asyncio


async def post_request_result_text(url, payload={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            return await response.text()


async def get_street_address_options(post_code):
    soup = BeautifulSoup(await post_request_result_text(
        "https://www.manchester.gov.uk/bincollections",
        {
            "mcc_bin_dates_search_term": post_code,
            "mcc_bin_dates_submit": "Go"
        }
    ), "html.parser")

    select = soup.find("select",{"id":"mcc_bin_dates_uprn"})
    found = []
    if select != None:
        for address in select.find_all("option"):
            found.append({"id": address["value"], "address": address.get_text()})
    return found


class ManchesterBinCollectionApi:
    
    def __init__(self, street_address_id):
        self.street_address_id = street_address_id
    
    
    async def connect(self):
        try:
            await self.__update()
        except:
            self.failed = True
        else:
            self.failed = False


    def __convert_bin_name_to_system_name(self, bin_name):
        return bin_name.replace("/ ", "").replace(" ", "_").lower()


    def __convert_bin_date_to_date_obj(self, bin_date):
        split = bin_date.split(" ")

        months = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
        
        year = int(split[3])
        month = months[split[2].lower()]
        day = int(split[1])

        return datetime.date(year, month, day)


    async def __update(self):
        soup = BeautifulSoup(await post_request_result_text(
            "https://www.manchester.gov.uk/bincollections",
            {
                "mcc_bin_dates_uprn": str(self.street_address_id),
                "mcc_bin_dates_submit": "Go"
            }
        ), "html.parser")

        bins = {}

        collections = soup.find_all("div", {"class": "collection"})
        for collection in collections:
            bin_name = collection.find("h3").find("img")['alt']
            next_date = str(collection.find("p", {"class": "caption"}).get_text()).replace("Next collection ", "")
            
            bins[self.__convert_bin_name_to_system_name(bin_name)] = {
                "name": bin_name,
                "date": self.__convert_bin_date_to_date_obj(next_date)
            }
        
        self.bin_data = bins
        self.last_updated = datetime.datetime.now()
    

    async def update(self):
        now = datetime.datetime.now()

        if now.strftime("%d") != self.last_updated.strftime("%d"):
            await self.__update()
            return True
        else:
            return False
    

    def get_bin_keys(self):
        found = []
        for bin_key in self.bin_data.keys():
            found.append(bin_key)
        return found


    def get_bin_name(self, bin_key):
        return self.bin_data[bin_key]['name']
    

    def get_bin_collection_date(self, bin_key):
        return self.bin_data[bin_key]['date']
    

    def get_bin_unique_id(self, bin_key):
        unique_name = str(self.street_address_id)+"__"+bin_key
        return hashlib.md5(str(unique_name).encode("utf-8")).hexdigest()


    def get_next_collected_bin_keys(self):
        found = []

        next_date = self.get_next_collection_date()
        for bin_key in self.bin_data.keys():
            if self.get_bin_collection_date(bin_key) == next_date:
                found.append(bin_key)
        
        return found


    def get_next_collection_date(self):
        today = datetime.date.today()

        lowest_diff = 100
        lowest_date = None
        for bin_key in self.bin_data.keys():
            diff = self.get_bin_collection_date(bin_key) - today

            if diff.days < lowest_diff:
                lowest_diff = diff.days
                lowest_date = self.get_bin_collection_date(bin_key)
        
        return lowest_date
    

    def get_days_until_next_collection(self):
        today = datetime.date.today()
        diff = self.get_next_collection_date() - today
        return diff.days


# async def __test():
#     print("Start")
#     api = ManchesterBinCollectionApi("000077180397")
#     await api.connect()
#     print(api.failed)
#     print(api.get_bin_keys())

# asyncio.run(__test())
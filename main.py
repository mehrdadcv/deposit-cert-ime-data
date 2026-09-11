import requests
import pandas as pd
import datetime as dt
import yaml
from dateutil.relativedelta import relativedelta


# more information on CommodityID and their names:
# {ID: 2, Code: "GoldBar", IsOnline: 1, Description: "گواهی سپرده پیوسته شمش طلای +995"}
 
# {ID: 4, Code: "GoldCoin", IsOnline: 1, Description: "گواهی سپرده پیوسته تمام سکه بهار آزادی طرح جدید"}

# {ID: 21, Code: "SilverBar", IsOnline: 1, Description: "گواهی سپرده پیوسته شمش نقره 999.9"}
 
# {ID: 14, Code: "CopperCthd", IsOnline: 1, Description: "گواهی سپرده پیوسته مس کاتد"}

# {ID: 26, Code: "Bitumen", IsOnline: 1, Description: "گواهی سپرده پیوسته قیر"}

# {ID: 30, Code: "ZincIngot", IsOnline: 1, Description: "گواهی سپرده پیوسته شمش روی"}

# {ID: 29, Code: "SteelRebar", IsOnline: 1, Description: "گواهی سپرده پیوسته میلگرد"}

# {ID: 28, Code: "IronOrePlt", IsOnline: 1, Description: "گواهی سپرده پیوسته گندله سنگ آهن"}

# {ID: 27, Code: "KMCT9", IsOnline: 1, Description: "گواهی سپرده پیوسته وانت کرمان خودرو"}

# {ID: 34, Code: "LeadIngot", IsOnline: 1, Description: "گواهی سپرده پیوسته شمش سرب"}

# {ID: 11, Code: "PistaCL", IsOnline: 1, Description: "گواهی سپرده پیوسته پسته "}

with open("settings.yaml", 'r') as file:
    settings = yaml.safe_load(file)


url = "https://dataapi.ime.co.ir/api/CDC/CDCTrades"

# we start the page with a default number, and then update it 
# after we send the first POST request
max_pages = 10
page_num = 1

# we first save each row in data_list and then turn it into a Dataframe
data_list = []


# the max time line we can send a request for is 3 months. beside this restriction,
# the site doesn't care how old we set our fromDate.
# "from_date" is a really old date so we don't miss any data.
today = dt.date.today()
# you can change from_date to a specific date from settings.yaml
# otherwise, the program automatically downloads from 2026-01-01
from_date = dt.date.strptime(settings["start_collection_from"], "%Y-%m-%d")
to_date = from_date + relativedelta(months=3)

print("preparations complete. sending request from date: ", from_date)
while to_date < today:

    while page_num < max_pages:
        print("page number started: ", page_num)

        data = {
            # I've tried different key-values for POST request but the site 
            # doesn't have a strict filter for commodity code and might return different 
            # commodity data as well, so we have to parse the data ourselves to gather the data we want.
            "fromDate": str(from_date),
            "toDate": str(to_date),
            "pageNumber": page_num,
            # I tried 1,000 pageSize but the request automatically changes it to 100
            "pageSize": 100,
        }

        response = requests.post(url, json=data)
        # if there was an error, we can check if it was from the site
        response.raise_for_status()

        # after sending the POST request, increment page_num to prepare it for next request
        page_num += 1

        response_in_json = response.json()
        max_pages = response_in_json["TotalPages"]
        total_data_available = response_in_json["TotalCount"]

        ### filter by commodity
        # change CommodityID to only save data of commodity you need
        # info about CommodityID and their names are listed at the top
        # you can change the filter from settings.yaml (by default it filters GoldBar)
        for row in response_in_json["Data"]:
            if row["CommodityID"] == settings["filter_commodity"]:
                data_list.append(row)

    # after the pages of a time line ends, we move the 3 month window:
    # 1- set "from_date" as "to_date"
    # 2- increase "from_date" by 3 months, and set it as "to_date"
    from_date = to_date
    to_date = from_date + relativedelta(months=3)
    new_df = pd.DataFrame(data_list)

    # we have to set "encoding" as 'utf-8-sig' so Persian names are saved correctly and are readable
    # you can change what the name of the output file should be in settings.yaml
    new_df.to_csv(settings["output_file_name"], index=None, encoding='utf-8-sig')


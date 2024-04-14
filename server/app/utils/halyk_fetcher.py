import re
import time

import requests

halyk_city_to_our_city = {
    "1001": "23",
    "1101": "11",
    "1201": "9",
    "1202": "7",
    "1301": "19",
    "1401": "8",
    "1402": "5",
    "1501": "1",
    "1601": "14",
    "1701": "16",
    "1802": "2",
    "1901": "24",
    "2001": "26",
    "2201": "12",
    "2301": "10",
    "0101": "3",
    "0601": "4",
    "0702": "6",
    "0701": "13",
    "0501": "15",
    "0301": "17",
    "0901": "18",
    "0401": "20",
    "0802": "21",
    "0201": "22",
    "0801": "25",
}

halyk_category_to_our_category = {
    "952": "11",
    "953": "1",
    "954": "2",
    "955": "10",
    "956": "11",
    "957": "14",
    "958": "1",
    "959": "15",
    "960": "11",
    "961": "5",
    "962": "6",
    "963": "11",
    "964": "8",
    "965": "11",
    "966": "17",
    "967": "12",
}


def get_categories(city_id):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru",
        "authorization": "Bearer MABC7M7QMNCT01WOPSEJWQ",
        "city_id": city_id,
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://halykbank.kz/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    response = requests.get(
        "https://pelican-api.homebank.kz/halykclub-api/v1/dictionary/categories",
        headers=headers,
    )
    return response.json()


def get_cities():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru",
        "authorization": "Bearer MABC7M7QMNCT01WOPSEJWQ",
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://halykbank.kz/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    response = requests.get(
        "https://pelican-api.homebank.kz/halykclub-api/v1/dictionary/cities",
        headers=headers,
    )
    return response.json()


def get_merchants(city_id, category_code):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru",
        "authorization": "Bearer MABC7M7QMNCT01WOPSEJWQ",
        "city_id": city_id,
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://halykbank.kz/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    url = f"https://pelican-api.homebank.kz/halykclub-api/v1/terminal/devices?category_code={category_code}&filter="
    response = requests.get(url, headers=headers)
    return response.json()


def parse():
    cities_data = get_cities()
    categories = set()
    all_city_categories = {}
    all_city_merchants = {}

    for city in cities_data:
        city_id = city["city_id"]

        if city_id not in ("1501", "1802"):
            continue

        category_data = get_categories(city_id)
        all_city_categories[city_id] = category_data
        for category in category_data:
            categories.add(category["code"])
        time.sleep(1)

    for city in cities_data:
        city_id = city["city_id"]

        if city_id not in ("1501", "1802"):
            continue

        for category_code in categories:
            try:
                print(city_id, category_code)
                merchant_data = get_merchants(city_id, category_code)
                if city_id not in all_city_merchants:
                    all_city_merchants[city_id] = {}
                all_city_merchants[city_id][category_code] = merchant_data
            except Exception as e:
                print(e)
            time.sleep(1)

    # with open("halyk_categories.json", "w") as file:
    #     json.dump(list(categories), file)
    # with open("halyk_all_city_categories.json", "w") as file:
    #     json.dump(all_city_categories, file)
    # with open("halyk_all_city_merchants.json", "w") as file:
    #     json.dump(all_city_merchants, file)

    # file = open("halyk_all_city_merchants.json", "r", encoding="utf-8")
    # all_city_merchants = json.load(file)

    res = []

    for city_key, city_val in all_city_merchants.items():
        for partner in city_val["all_partners"]:
            for tag in partner["tags"]:
                new_val = {}
                new_val["city_id"] = int(halyk_city_to_our_city[city_key])
                new_val["name"] = partner["name"]
                new_val["address"] = partner["address"]
                if partner["category_id"] not in halyk_category_to_our_category:
                    continue
                new_val["category_id"] = int(
                    halyk_category_to_our_category[partner["category_id"]]
                )
                new_val["cashback_percent"] = float(
                    "".join(re.findall(r"\d+", tag["text"]))
                )
                new_val["description"] = tag["text"]
                new_val["bank_id"] = 1
                new_val["card_type"] = 4
                res.append(new_val)

    return res


# with open("final_halyk.json", "w") as file:
#     json.dump(parse(), file)

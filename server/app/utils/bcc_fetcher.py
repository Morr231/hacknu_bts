import time

import requests

bcc_city_to_our_city = {
    21: "1",
    5: "2",
    3: "5",
    4: "3",
    7: "4",
    9: "7",
    10: "8",
    11: "9",
    15: "11",
    16: "10",
    17: "12",
    18: "14",
    20: "13",
    22: "15",
    23: "16",
    27: "17",
    29: "18",
    30: "19",
    31: "20",
    38: "21",
    33: "22",
    34: "23",
    36: "25",
    37: "26",
}

bcc_category_to_our_category = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "11",
    12: "12",
    13: "13",
    14: "14",
    15: "15",
    16: "16",
    17: "17",
    18: "18",
    19: "19",
    20: "20",
    21: "21",
    22: "22",
    23: "23",
    24: "24",
}


def get_categories(city_id, card):
    url = f"https://partners.org.kz/api/getall?card={card}&city={city_id}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://club.bcc.kz/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_cities():
    url = "https://partners.org.kz/api/city"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://club.bcc.kz/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_partners(city_id, card):
    url = f"https://partners.org.kz/api/getpartner?card={card}&city_id={city_id}&cashback=true"
    response = requests.get(
        url,
        headers={
            # headers as above
        },
    )
    return response.json()


def parse():
    data = get_cities()
    res = []
    cards = ["kartakarta", "ironcard", "juniorcard"]
    card_to_id = {"kartakarta": 1, "ironcard": 2, "juniorcard": 3}

    for city in data:
        city_id = city["city_id"]

        if city_id not in [21, 5]:
            continue

        for card in cards:
            print(city_id, card)
            partners_data = get_partners(city_id, card)

            for partner in partners_data["data"]:
                for place in partner["places"]:
                    if not partner["category"]:
                        continue
                    new_val = {
                        "city_id": int(bcc_city_to_our_city[city_id]),
                        "name": partner["title"],
                        "address": place["city_address"],
                        "category_id": int(partner["category"]),
                        "cashback_percent": float(partner["cashback"]),
                        "description": partner["description"],
                        "card_type": int(card_to_id[card]),
                    }
                    res.append(new_val)

            time.sleep(0.5)  # Pause to mimic previous delay

    return res


# with open("final_bcc.json", "w") as file:
# json.dump(parse(), file)

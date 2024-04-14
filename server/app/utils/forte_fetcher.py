import json

import requests
from bs4 import BeautifulSoup


def fetch_script_data(url):
    try:
        # Sending a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parsing the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Finding the script tag with the specific ID
        script_tag = soup.find("script", id="__NEXT_DATA__")

        if script_tag:
            return script_tag.text
        else:
            return "Script tag with ID '__NEXT_DATA__' not found."

    except requests.RequestException as e:
        # Handling exceptions related to the requests library
        return f"An error occurred: {e}"


# URL to fetch
url = "https://club.forte.kz/partneroffers"

# Execute the function and print the result
data = fetch_script_data(url)
# print(result)


# Write the data to a JSON file if it's not an error message
if not data.startswith("An error occurred") and not data.startswith(
    "Script tag with ID '__NEXT_DATA__' not found."
):
    with open("forte_data.json", "w") as f:
        # The data is expected to be in JSON format, dump it into the file

        data = json.loads(data)
        cities = data["props"]["pageProps"]["navigation"]["cities"]
        with open("forte_cities.json", "w") as fl:
            json.dump(cities, fl)

        partners = data["props"]["pageProps"]["dynamicComponents"]
        partners = list(
            filter(
                lambda x: x["__typename"] == "ComponentDynamicPagePartners", partners
            )
        )
        with open("forte_partners.json", "w") as fp:
            json.dump(partners[0]["partners"], fp)

        all_categories = []
        partners_categories = partners[0]["partners"]
        for partner in partners_categories:
            if partner["subCategory"]["parentCategory"] not in all_categories:
                all_categories.append(partner["subCategory"]["parentCategory"])

        with open("forte_categories.json", "w") as fc:
            json.dump(all_categories, fc)

        json.dump(data, f)

        print("Data saved to 'forte_data.json'.")

import requests
from bs4 import BeautifulSoup
import re

def scrape_town_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    town_names = []
    # Regex pattern to match only Latin alphabet characters
    latin_pattern = re.compile(r'^[A-Za-z\s]+$')

    # Find all table rows in the specified table
    for row in soup.find_all('tr'):
        # Get all <td> elements in the row
        cells = row.find_all('td')
        # Check if there are at least two <td> elements
        if len(cells) > 1:
            town_name = cells[1].get_text(strip=True)  # Get the second <td>
            # Check if the town name contains only Latin characters
            if latin_pattern.match(town_name):
                town_names.append(town_name + " Canada")

    return town_names

def append_to_file(town_names, filename='towns.txt'):
    with open(filename, 'a') as file:
        for town in town_names:
            file.write(f"{town}\n")

if __name__ == "__main__":

    for i in range(76):
        x = i + 1
        url = "https://geokeo.com/database/town/ca/" + str(x) +"/"
        towns = scrape_town_names(url)

    # Append the filtered town names to the file
        append_to_file(towns)
        print(f"Appended {len(towns)} towns to towns.txt")
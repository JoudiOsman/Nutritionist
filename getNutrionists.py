import requests
from bs4 import BeautifulSoup
import re
import time

def get_nutritionists_in_town(town):
    search_query = f"nutritionist {town}"
    url = f"https://www.google.com/search?q={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        print(f"Received 429 Too Many Requests for {town}.")
        return None  # Return None to indicate rate limit issue

    if response.status_code != 200:
        print(f"Error fetching results for {town}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # Find Google Maps places results
    places = soup.find_all("div", class_="VkpGBb")
    
    if not places:
        print(f"No places found for {town}.")
        return []

    nutritionists_info = []

    for place in places:
        # Extracting name
        title_element = place.find("span", class_="OSrXXb")  # Place name
        title = title_element.text.strip() if title_element else "Name not found"

        # Extracting the entire text from the place div for regex searching
        place_text = place.get_text()

        # regex to find phone number
        phone_number_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)-\d{3}-\d{4}|\d{10}', place_text)
        phone_number = phone_number_match.group(0) if phone_number_match else "No number found"

        # Attempt to find website from tags in the place div
        website = "No website found"
        website_elements = place.find_all("a", href=True)
        
        for link in website_elements:
            # Check for website link patterns
            if 'http' in link['href']:
                website = link['href']
                break

        nutritionists_info.append({
            "Name": title,
            "Phone Number": phone_number,
            "Website": website
        })

    return nutritionists_info

# get towns from file
def read_towns(filename='towns.txt'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# writes all non used towns back intofile (so script can be quit and ran without losing track)
def save_towns(towns, filename='towns.txt'):
    """Overwrite towns.txt with the remaining towns."""
    with open(filename, 'w') as file:
        for town in towns:
            file.write(f"{town}\n")

def save_to_file(data, filename='all.txt'):
    with open(filename, 'a') as file:
        for entry in data:
            file.write(f"{entry['Name']}, {entry['Phone Number']}, {entry['Website']}\n")

if __name__ == "__main__": 
    towns = read_towns()  # Read towns from towns.txt
    total_entries = 0

    for i, town in enumerate(towns):
        nutritionists = get_nutritionists_in_town(town)
        
        # Handle 429 error by truncating the list of towns and timing out for 2 hours
        if nutritionists is None:
            print(f"429 error encountered in {town}. Removing previous towns and waiting 2 hours.")
            remaining_towns = towns[i:]  # Keep the current town and those after it
            save_towns(remaining_towns)  # Save the updated towns list
            
            print("Sleeping for 2 hours before retrying...")
            time.sleep(7200) #7200 seconds in 2 hours
            
            continue  # Retry after the timeout period

        save_to_file(nutritionists)
        total_entries += len(nutritionists)

    print(f"Appended {total_entries} entries to all.txt")

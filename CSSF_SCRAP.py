import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Base URL of the website to scrape
base_url = 'DELETED FOR SECURITY'

# Create an empty list to store extracted data
data = []

# Loop through the pages from 1 to 31
for page in range(1, 32): # Change this value in case you only want to scrap a certain amount of pages. 
    # Generate the URL for each page
    url = f"{base_url}{page}/"
    
    # Make a GET request to fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    # Find all the <h3> elements with the class 'library-element__title'
    warnings = soup.find_all('h3', class_='library-element__title')

    # Find all the <span> elements with the class 'date--published'
    dates = soup.find_all('span', class_='date--published')

    # Loop through the extracted warnings and dates and store them
    for warning, date in zip(warnings, dates):
        # Extract the href and the text of the <a> element
        href = f"DELETED FOR SECURITY{warning.a['href']}"  # Add base URL
        title = warning.a.text.strip()

        # Extract the published date
        published_date = date.text.replace('Published on ', '').strip()

        # Visit the individual warning page to extract additional information
        warning_response = requests.get(href)
        warning_soup = BeautifulSoup(warning_response.content, 'lxml')

        # Extract additional details from the page
        try:
            warning_type = warning_soup.find('td', string='Warning:').find_next_sibling('td').text.strip()
        except AttributeError:
            warning_type = ''  # Leave blank if not found
        
        try:
            entity_name = warning_soup.find('td', string='Entity name used:').find_next_sibling('td').text.strip()
        except AttributeError:
            entity_name = ''  # Leave blank if not found

        try:
            website_used = warning_soup.find('td', string='Website used:').find_next_sibling('td').text.strip()
        except AttributeError:
            website_used = ''  # Leave blank if not found

        # Append the extracted data to the list
        data.append({
            'date_added': datetime.now().strftime('%d-%m-%Y'),  # Current date
            'country': 'Luxemburg',  # Static value
            'source': 'DELETED FOR SECURITY',  # Static value
            'name': entity_name,  # Entity name
            'pulled_links': website_used,  # Website used
            'cleaning': '',  # Empty
            'notes': warning_type,  # Notes
            'date_added_to_website': published_date,  # Date added on website
            'case': href  # The href link
        })
    
    print(f"Scraped page {page}/31")

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Drop duplicates if necessary
df.drop_duplicates(inplace=True)

# Save the DataFrame to an Excel file
today = datetime.now().strftime('%Y-%m-%d')
df.to_excel(f'DELETED FOR SECURITY{today}.xlsx', index=False)

print(f"Scraping completed. Data saved to DELETED FOR SECURITY{today}.xlsx")
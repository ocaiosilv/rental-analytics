import cloudscraper
from bs4 import BeautifulSoup
import csv
import os
import random

def pseudoPriceAdjustment(rent, bedrooms, bathrooms, parking_spaces, property_size):
    """
    This function ideia it's to synthetically adjust the rent price for
    properties. The original problem was that when simulating new rentals, within
    the number of rooms and square meters would change, but the price would
    stay the same, which wasn't realistic even for a syntetical aproach.

    A statistical aproach, using our own data analysis exploring the (Catalog.csv) without the
    multRentals, was initially explored but proved unreliable for discrete features like 
    bedrooms or bathrooms. The source data showed too much price variance due the lack of 
    "congruent" ad's, for an example it was hard to have 3-4 apartments with minimum 
    variances between them in the same neighboorhood to see how the price changed.

    The implemented solution therefore uses a data-driven average 'price per square meter' 
    from the "no multiple rentals" analysis, complemented by heuristic-based multipliers 
    for other features.

    note: if you run this in a bigger city vivareal page, and then get a more dense dataframe
    (without the pseudoRentals active) you can have a gratter result about the real changes
    for each bedroom,bathroom, parking spaces and even the priceperSQM, so then the pseudoRentals
    can be more precise and accurrate.
    """
    price = rent

    # Searched estimates used due to inconsistencies in the source data.
    bedrooms_multiplier= 1.30  # 30% increase per bedroom
    bathroom_smultiplier = 1.15 # 15% increase per bathroom
    parkings_multiplier = 1.10  # 10% increase per parking space

    # Value derived from the data analysis in our notebook.
    priceSqm = 35         

    if isinstance(bedrooms, tuple):
        diff = bedrooms[1] - bedrooms[0]
        if diff > 0:
            price = price * (1.30) ** diff

    if isinstance(bathrooms, tuple):
        diff = bathrooms[1] - bathrooms[0]
        if diff > 0:
            price = price * (1.15) ** diff

    if isinstance(parking_spaces, tuple):
        diff = parking_spaces[1] - parking_spaces[0]
        if diff > 0:
            price = price * (1.10) ** diff

    if isinstance(property_size, tuple) and property_size[0] !=0:
        print(property_size)
        diff = property_size[1] - property_size[0]
        if diff > 0:
            price = price + abs((25) * diff)

    return round(price, 0)


def select_value_from_range(value):
    """
    Handles cases where the site gives a range, like "2-4 bathrooms",
    or just a single number.

    If it's a list (a range), 
        it returns a tuple like (2, 4) 
    to calculate the price difference. 
    Else if it's a single number, 
        it returns (3, 3).
    in order to this value not affect the price due the lack of an
    list.

    Opted to do this way because: it's a clean way to ensure only
    actual ranges trigger a price change.
    """
    if isinstance(value, list):
        return  int(value[0]), int(random.choice(value))
    else:
        return int(value), int(value)

def pseudoMultRentals(multipleRentals, item, catalog, neighborhood, street, rent, condo_fee):
    """
    The function exists to solve a specific problem on the website where
    multiple apartments are grouped in a single button ("See 5 more
    apartments"), and their details couldn't be accessed within the current html page.

    This approach try to most accurrate simulate the hidden rentals. It reads 
    the quantity from the button's text and then creates that many "pseudo" 
    rentals. If the rental ad has ranges for its features (like "2-4 rooms"), 
    each new simulated rental will have its pseudorandomized features and a simulated
    adjusted price.
    """
    multNumber = numbers_from_string(multipleRentals.get_text())
    for i in range(1,multNumber):
        property_size = extract_info("rp-cardProperty-propertyArea-txt", item)
        bedrooms = extract_info("rp-cardProperty-bedroomQuantity-txt", item)
        bathrooms = extract_info("rp-cardProperty-bathroomQuantity-txt", item)
        parking_spaces = extract_info("rp-cardProperty-parkingSpacesQuantity-txt", item)

        property_size_vals = select_value_from_range(property_size)
        bedrooms_vals = select_value_from_range(bedrooms)
        bathrooms_vals = select_value_from_range(bathrooms)
        parking_spaces_vals = select_value_from_range(parking_spaces)
        rent_adjusted = pseudoPriceAdjustment(rent, bedrooms_vals, bathrooms_vals, parking_spaces_vals, property_size_vals)
        property_item = {
            "neighborhood": neighborhood,
            "street": street,
            "rent": rent_adjusted,
            "condo_fee": condo_fee,
            "total_monthly_value": rent_adjusted + condo_fee,
            "property_size": property_size_vals[1],
            "bedrooms": bedrooms_vals[1],
            "bathrooms": bathrooms_vals[1],
            "parking_spaces": parking_spaces_vals[1],
        }
        catalog.append(property_item)
 


def withRangeNumbers_from_string(text):
    """
    It takes a string as "Area: 60-80m²" and gives me back a clean list
    of integers: [60, 80].
    """
    range = (''.join(i for i in text if i.isdecimal() or i == "-"))
    return list(map(int, range.split("-")))

def numbers_from_string(text):
    """
    Takes only the digits of a whole string
    input : "$1.400 USD"
    output: 1400
    """
    return int(''.join(i for i in text if i.isdecimal()))
    
def extract_info(info_type, property_html):
    """
    This function it's for DRY (Don't Repeat Yourself) purposes, instead of writing the 
    same find/get_text logic over and over for each piece of data, I just call 
    this one function. It detects if the text is a single number "3 bathrooms"
    or a range ("60-80 m²") and uses the correct function to each one.
    """
    info_element = property_html.find("li", attrs={"data-cy": f"{info_type}"})
    if info_element:
        element = (info_element.find("h3", attrs={"class": "flex row items-center gap-0-5"})).get_text()
        if not "-" in element:
            return numbers_from_string(element)
        else:
            return withRangeNumbers_from_string(element)
    else:
        return 0    

def web_scraping():
    """
    Executes the Scrapping.

    It first sends an initial request to determine the total number of
    listings and calculates the total pages that need to be scraped based
    in the page limits for rental ads, then iterates trought each page

    On each page, it finds all property listings and extracts core information
    like address, rent, and condo fees, handling cases where data is missing.
    
    Then it proceeds to build and append the dictionary to the catalog, in this
    building step, there's a "feature" that you can turn on and off, called the
    multRentals, that, as already been explained, comes to bypass a little problem 
    with the grouped rentals in the html. 
    The two, multRentals True or False, provides great results and satisfying dataframes.
    """
    scraper = cloudscraper.create_scraper()
    base_url = "https://www.vivareal.com.br/aluguel/sergipe/aracaju/apartamento_residencial/"

    page_zero = scraper.get(base_url)
    soup = BeautifulSoup(page_zero.text, "html.parser") 

    total_properties = soup.find("div", attrs={"id": "mobile-result-scroll-point", "class": "UpperFilter_upper-filters__wrapper__7m8g9"})
    total_properties = total_properties.find("h1", attrs={"class": "font-medium text-2 text-neutral-130 font-bold"}).get_text()
    total_properties = numbers_from_string(total_properties)

    if total_properties % 30 != 0:
        total_pages = total_properties // 30 + 1
    else:
        total_pages = total_properties // 30

    property_catalog = []
    for i in range(1,total_pages):
        url = (base_url + "?onde=%2CSergipe%2CAracaju%2C%2C%2C%2C%2Ccity%2CBR%3ESergipe%3ENULL%3EAracaju%2C-10.92654%2C-37.073115%2C&tipos=apartamento_residencial"f"&pagina={i}" "&transacao=aluguel")

        page = scraper.get(url)
        soup = BeautifulSoup(page.text, "html.parser") 

        properties_info = soup.find_all("li", attrs={"data-cy": "rp-property-cd"})
        for item in properties_info:
            property_item = {}
            neighborhood = item.find("h2", attrs={"data-cy": "rp-cardProperty-location-txt"})
            neighborhood = neighborhood.find("span", attrs={"class": "block font-secondary text-1-5 font-regular text-neutral-110 mb-1"}).next_sibling.split(",")[0]

            street = item.find("p", attrs={"data-cy": "rp-cardProperty-street-txt"}).get_text()

            rent = item.find("div", attrs={"data-cy": "rp-cardProperty-price-txt"})
            try: 
                rent = numbers_from_string(rent.find("p", attrs={"class": "text-2-25"}).get_text())
            except:
                continue
            
            condo_fee = item.find("p", attrs={"class": "text-1-75 text-neutral-110 overflow-hidden text-ellipsis"})
            if condo_fee:
                condo_fee = numbers_from_string((condo_fee.get_text().split("•")[0]))
            else:
                condo_fee = 0

            total_monthly_value = rent + condo_fee
            
            """
            If you wish to get a more dense dataframe with pseudogenerated rentals due
            the fact the grouped rentals in the website that im scrapping do not show 
            in the same page as the html:
                let pseudoMultGenerate = True
            Else turn it False
            """
            pseudoMultGenerate = False

            multipleRentals = item.find("button", attrs={"data-cy": "listing-card-deduplicated-button"})
            if pseudoMultGenerate == True:
               pseudoMultRentals(multipleRentals, item, property_catalog, neighborhood, street, rent, condo_fee)
               pass
            elif multipleRentals:
                pass
            else:
                property_size = extract_info("rp-cardProperty-propertyArea-txt", item)
                bedrooms = extract_info("rp-cardProperty-bedroomQuantity-txt", item)
                bathrooms = extract_info("rp-cardProperty-bathroomQuantity-txt", item)
                parking_spaces = extract_info("rp-cardProperty-parkingSpacesQuantity-txt", item)
                property_item = {
                    "neighborhood": neighborhood,
                    "street": street,
                    "rent": rent,
                    "condo_fee": condo_fee,
                    "total_monthly_value": total_monthly_value,
                    "property_size": property_size, 
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "parking_spaces": parking_spaces,
                }            
                property_catalog.append(property_item)
                
    return property_catalog

#Runs the main scraper and saves the collected data to catalog.csv.
catalog = web_scraping()

# Defines the path for the output file .../data/catalog.csv) ( works in any path )
rent_analysis_folder = os.path.dirname(os.path.dirname(__file__))
data_folder = os.path.join(rent_analysis_folder, "data")
catalog_file_path = os.path.join(data_folder, "catalog.csv")

# Writes the list of dictionaries to the CSV file
with open(catalog_file_path, 'w', newline='') as csvfile:
    fieldnames = ["neighborhood", "street", "rent", "condo_fee", "total_monthly_value", "property_size", "bedrooms", "bathrooms", "parking_spaces"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in catalog:
        writer.writerow(i)

print("Scraping complete.")
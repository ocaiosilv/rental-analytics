import cloudscraper
from bs4 import BeautifulSoup
import csv
import os

def numbers_from_string(text):
    return int(''.join(i for i in text if i.isdecimal()))
    
def extract_info(info_type, property_html):
    info_element = property_html.find("li", attrs={"data-cy": f"{info_type}"})
    if info_element:
        return numbers_from_string((info_element.find("h3", attrs={"class": "flex row items-center gap-0-5"})).get_text())
    else:
        return 0    

def web_scraping():
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
    for i in range(total_pages):
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


catalog = web_scraping()
rent_analysis_folder = os.path.dirname(os.path.dirname(__file__))
data_folder = os.path.join(rent_analysis_folder, "data")
catalog_file_path = os.path.join(data_folder, "catalog.csv")

with open(catalog_file_path, 'w', newline='') as csvfile:
    fieldnames = ["neighborhood", "street", "rent", "condo_fee", "total_monthly_value", "property_size", "bedrooms", "bathrooms", "parking_spaces"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in catalog:
        writer.writerow(i)

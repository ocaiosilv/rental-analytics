import cloudscraper
from bs4 import BeautifulSoup
import csv

def numbersFromString(text):
    return int(''.join(i for i in text if i.isdecimal()))
    

def extract_Info(infoType, propertyHtml):
    infoElement = (propertyHtml.find("li", attrs={"data-cy": f"{infoType}"}))
    if infoElement:
        return numbersFromString((((infoElement.find("h3", attrs={"class": "flex row items-center gap-0-5"}))).get_text()))
    else:
        return 0    

def webScrapping():
    scraper = cloudscraper.create_scraper()
    urlZero = "https://www.vivareal.com.br/aluguel/sergipe/aracaju/apartamento_residencial/"

    pageZero = scraper.get(urlZero)
    soup = BeautifulSoup(pageZero.text, "html.parser") 

    totalImoveis = soup.find("div", attrs={"id": "mobile-result-scroll-point", "class": "UpperFilter_upper-filters__wrapper__7m8g9"})
    totalImoveis = totalImoveis.find("h1", attrs={"class": "font-medium text-2 text-neutral-130 font-bold"}).get_text()
    totalImoveis = numbersFromString(totalImoveis)

    if totalImoveis % 30 != 0:
        totalPaginas = totalImoveis//30 + 1
    else:
        totalPaginas = totalImoveis // 30

    catalgoImoveis = []
    for i in range(totalPaginas):
        url = (urlZero + "?onde=%2CSergipe%2CAracaju%2C%2C%2C%2C%2Ccity%2CBR%3ESergipe%3ENULL%3EAracaju%2C-10.92654%2C-37.073115%2C&tipos=apartamento_residencial"f"&pagina={i}""&transacao=aluguel")

        page = scraper.get(url)
        soup = BeautifulSoup(page.text, "html.parser") 

        infosImoveis = soup.find_all("li", attrs={"data-cy": "rp-property-cd"})
        for item in infosImoveis:
            imovel = {}
            
            bairro = ((item.find("h2", attrs={"data-cy": "rp-cardProperty-location-txt"})))
            bairro = bairro.find("span", attrs={"class": "block font-secondary text-1-5 font-regular text-neutral-110 mb-1"}).next_sibling.split(",")[0]

            rua = (item.find("p", attrs={"data-cy": "rp-cardProperty-street-txt"})).get_text()

            aluguel = item.find("div", attrs={"data-cy": "rp-cardProperty-price-txt"})
            try: 
                aluguel = numbersFromString(((aluguel.find("p", attrs={"class": "text-2-25"})).get_text()))
            except:
                continue
            
            taxaCondominial = item.find("p", attrs={"class": "text-1-75 text-neutral-110 overflow-hidden text-ellipsis"})
            if taxaCondominial:
                taxaCondominial = numbersFromString((((taxaCondominial.get_text()).split("•"))[0]))
            else:
                taxaCondominial = 0

            valorTotalMensal = (aluguel +  taxaCondominial)
        
            tamanhoImovel = extract_Info("rp-cardProperty-propertyArea-txt", item)
            quantidadeQuartos = extract_Info("rp-cardProperty-bedroomQuantity-txt", item)
            quantidadeBanheiros = extract_Info("rp-cardProperty-bathroomQuantity-txt", item)
            quantidadeVagasGaragem = extract_Info("rp-cardProperty-parkingSpacesQuantity-txt", item)
            
            imovel = {
            "bairro": bairro,
            "rua": rua,
            "aluguel": aluguel,
            "taxaCondominial": taxaCondominial,
            "valorTotalMensal": valorTotalMensal,
            "tamanhoImovel": tamanhoImovel, 
            "quartos": quantidadeQuartos,
            "banheiros": quantidadeBanheiros,
            "vagasGaragem": quantidadeVagasGaragem,
            }            
            
            catalgoImoveis.append(imovel)
    return catalgoImoveis

catalogo = webScrapping()

with open('catalogo.csv', 'w',newline='') as csvfile:
    fieldnames = ["bairro", "rua", "aluguel", "taxaCondominial", "valorTotalMensal", "tamanhoImovel",  "quartos", "banheiros", "vagasGaragem"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in catalogo:
        writer.writerow(i)

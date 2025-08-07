import cloudscraper
from bs4 import BeautifulSoup
import time

start_time = time.time()
scraper = cloudscraper.create_scraper()
urlZero = "https://www.vivareal.com.br/aluguel/sergipe/aracaju/apartamento_residencial/"

pageZero = scraper.get(urlZero)

soup = BeautifulSoup(pageZero.text, "html.parser") 
a = 0
totalImoveis = int("".join(i for i in (((soup.find("div", attrs={"id": "mobile-result-scroll-point", "class": "UpperFilter_upper-filters__wrapper__7m8g9"})).find("h1", attrs={"class": "font-medium text-2 text-neutral-130 font-bold"})).get_text()) if i.isdecimal()))
if totalImoveis % 30 != 0:
    totalPaginas = totalImoveis//30 + 1
else:
    totalPaginas = totalImoveis // 30

catalgoImoveis = []
for i in range(totalPaginas):
    url = (
    urlZero +
    "?onde=%2CSergipe%2CAracaju%2C%2C%2C%2C%2Ccity%2CBR%3ESergipe%3ENULL%3EAracaju"
    "%2C-10.92654%2C-37.073115%2C"
    "&tipos=apartamento_residencial"
    f"&pagina={i}"
    "&transacao=aluguel")

    page = scraper.get(url)
    soup = BeautifulSoup(page.text, "html.parser") 


    items = soup.find_all("li", attrs={"data-cy": "rp-property-cd"})
    for item in items:
        imovel = {}
        pularitem = 0
        
        bairro = ((item.find("h2", attrs={"data-cy": "rp-cardProperty-location-txt"})).find("span", attrs={"class": "block font-secondary text-1-5 font-regular text-neutral-110 mb-1"})).next_sibling.split(",")[0]
        rua = (item.find("p", attrs={"data-cy": "rp-cardProperty-street-txt"})).get_text()
        try: 
            aluguel = int("".join(((item.find("p", attrs={"class": "text-2-25"})).get_text()).strip("R$/mês ").split(".")))
        except:
            continue
        
        a +=1
        taxaCondominial = item.find("p", attrs={"class": "text-1-75 text-neutral-110 overflow-hidden text-ellipsis"})
        if taxaCondominial == None:
            taxaCondominial = 0
        else:
            taxaCondominial = int("".join((((taxaCondominial.get_text()).strip("Cond.R$ IPTU").split("•"))[0]).split(".")))

        valorTotalMensal = (aluguel +  taxaCondominial)
    
        tamanhoImovel = int(''.join(i for i in ((((item.find("li", attrs={"data-cy": "rp-cardProperty-propertyArea-txt"})).find("h3", attrs={"class": "flex row items-center gap-0-5"}))).get_text()) if i.isdecimal()))
        quantidadeQuartos = int(''.join(i for i in ((((item.find("li", attrs={"data-cy": "rp-cardProperty-bedroomQuantity-txt"})).find("h3", attrs={"class": "flex row items-center gap-0-5"}))).get_text()) if i.isdecimal()))
        quantidadeBaheiros = int(''.join(i for i in ((((item.find("li", attrs={"data-cy": "rp-cardProperty-bathroomQuantity-txt"})).find("h3", attrs={"class": "flex row items-center gap-0-5"}))).get_text()) if i.isdecimal()))
        if (item.find("li", attrs={"data-cy": "rrp-cardProperty-parkingSpacesQuantity-txt"})) == None:
            quantidadeVagasGaragem = 0
        else:
            quantidadeVagasGaragem = int(''.join(i for i in ((((item.find("li", attrs={"data-cy": "rrp-cardProperty-parkingSpacesQuantity-txt"})).find("h3", attrs={"class": "flex row items-center gap-0-5"}))).get_text()) if i.isdecimal()))
    
        
        imovel = {
        "bairro": bairro,
        "rua": rua,
        "aluguel": aluguel,
        "taxaCondominial": taxaCondominial,
        "valorTotalMensal": valorTotalMensal,
        "tamanhoImovel": tamanhoImovel, 
        "quartos": quantidadeQuartos,
        "banheiros": quantidadeBaheiros,
        "vagasGaragem": quantidadeVagasGaragem,
        }
        
        catalgoImoveis.append(imovel)


print(catalgoImoveis)
print("--- %s seconds ---" % (time.time() - start_time))
print(a)

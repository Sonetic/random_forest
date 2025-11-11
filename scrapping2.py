import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://deweloperuch.pl/ceny-ofertowe/warszawa/mieszkania?page="
rows = []

for page in range(1, 847):
    response = requests.get(base_url + str(page))
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if not table:
        break

    for row in table.find_all("tr")[1:]:
        # finding all cells
        tds = row.find_all("td")
        if len(tds) == 7:
            # only purple adress
            address_tag = row.find("a", class_="text-purple-600")
            address = address_tag.get_text(strip=True) if address_tag else ""

            oferta, inwestycja, metraz, cena_m2, cena, zmiana, _ = [td.text.strip() for td in tds]

            if "2025" in zmiana:
                rows.append([oferta, address, metraz, cena_m2, cena, zmiana])

df = pd.DataFrame(rows, columns=["Apartment", "Address", "Area_m2", "Price_m2", "Price_total", "Ostatnia zmiana"])

df["Address"] = df["Address"].str.split("\n").str[0].str.strip()
df["Area_m2"] = df["Area_m2"].str.replace(",", ".").str.replace("m²", "").str.strip().astype(float)
df["Price_total"] = df["Price_total"].str.split("zł").str[0].str.replace("\xa0", "").str.replace(" ", "").str.replace("zł", "").astype(float)
df["Price_m2"] = df["Price_m2"].str.replace("\xa0", "").str.replace(" ", "").str.replace("zł", "").astype(float)



df = df.drop(columns=["Apartment", "Ostatnia zmiana"], axis = 1)

df.to_csv("deweloperuch_offers.csv", index=False)
print("saved as deweloperuch_offers.csv")

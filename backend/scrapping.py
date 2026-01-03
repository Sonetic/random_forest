import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://deweloperuch.pl/ceny-transakcyjne/warszawa/mieszkania?page="
all_data = []

for page in range(1, 526):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr", class_="border-b")

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        # fioletowy adres
        address_tag = row.find("a", class_="text-purple-600")
        address = address_tag.get_text(strip=True) if address_tag else ""

        # nowa kolejność: adres, metraż, pokoje, piętro, cena_m2, cena
        if len(cols) >= 6:
            cols = [
                "",          # Apartment
                address,     # Address (TYLKO fioletowy tekst)
                cols[6],     # Price_total
                cols[2],     # Area_m2
                cols[5],     # Price_m2
                cols[3],     # Rooms
                cols[4],     # Floor
                ""           # Date
            ]
            all_data.append(cols)

    print(f"pobrano strone {page}")

columns = ["Apartment", "Address", "Price_total", "Area_m2",
           "Price_m2", "Rooms", "Floor", "Date"]

df = pd.DataFrame(all_data, columns=columns)

# czyszczenie liczb
df["Area_m2"] = df["Area_m2"].str.replace(r"[^\d.,]", "", regex=True).str.replace(",", ".").astype(float)
df["Price_total"] = df["Price_total"].str.replace(r"[^\d.,]", "", regex=True).str.replace(",", ".").astype(float)
df["Price_m2"] = df["Price_m2"].str.replace(r"[^\d.,]", "", regex=True).str.replace(",", ".").astype(float)

df = df.drop(columns=["Apartment", "Date"])

df.to_csv("deweloperuch_transactions.csv", index=False)
print("Saved as deweloperuch_transactions.csv")

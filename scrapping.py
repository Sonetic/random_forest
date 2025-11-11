import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://deweloperuch.pl/ceny-transakcyjne/warszawa/mieszkania?page="
all_data = []

for page in range(1, 529):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr", class_="border-b")

    for row in rows:
        # downloading only purple text from webstie (as it is the exact adress whithout any further useless info)
        address_tag = row.find("a", class_="text-purple-600")
        address = address_tag.get_text(strip=True) if address_tag else ""

        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) == 8:
            # applying adress
            cols[1] = address
            all_data.append(cols)

# heads
columns = ["Apartment", "Address", "Price_total", "Area_m2",
           "Price_m2", "Rooms", "Floor", "Date"]

df = pd.DataFrame(all_data, columns=columns)


# conversion
df["Area_m2"] = df["Area_m2"].str.replace(",", ".").str.replace("m²", "").str.strip().astype(float)
df["Price_total"] = df["Price_total"].str.replace("\xa0", "").str.replace(" ", "").str.replace("zł", "").astype(float)
df["Price_m2"] = df["Price_m2"].str.replace("\xa0", "").str.replace(" ", "").str.replace("zł", "").astype(float)

# 2025 up
df = df[df["Date"].str.contains("2025")]
df = df.drop(columns=["Apartment", "Date"], axis = 1)

df.to_csv("deweloperuch_transactions.csv", index=False)
print("Saved as deweloperuch_transactions.csv")

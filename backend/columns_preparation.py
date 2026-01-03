import pandas as pd
import warnings
from sklearn.linear_model import LinearRegression
warnings.simplefilter(action="ignore", category=FutureWarning) # annoying warning about panda's concatenation


df_trans = pd.read_csv("deweloperuch_transactions.csv")
df_trans = df_trans.dropna(subset=["Floor"])
df_offers = pd.read_csv("deweloperuch_offers.csv")

# predicting room number and floor number via linear regression
model = LinearRegression()
model.fit(df_trans[["Area_m2"]], df_trans["Rooms"])
df_offers["Rooms"] = model.predict(df_offers[["Area_m2"]]).round().astype(int)




features = ["Area_m2", "Price_m2", "Price_total", "Rooms"]
model.fit(df_trans[features], df_trans["Floor"])
df_offers["Floor"] = model.predict(df_offers[features]).round()

# setting in order
df_offers = df_offers[df_trans.columns]


# adding flags, for later usement during dividing samples
df_trans["source"] = "transactions"
df_offers["source"] = "offers"


# concatenation
df = pd.concat([df_trans, df_offers], ignore_index=True)


df.to_csv("deweloperuch_all.csv", index = False)
print("saved as deweloperuch_full.csv")
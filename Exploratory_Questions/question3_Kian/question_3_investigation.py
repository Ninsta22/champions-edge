import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

df1 = pd.read_csv("/workspaces/uds-2024-pangolin/Exploratory_Questions/question3_Kian/MER_T02_01A.csv")
df2 = pd.read_csv("/workspaces/uds-2024-pangolin/Exploratory_Questions/question3_Kian/MER_T02_01B.csv")
df = pd.concat([df1, df2])

df["YYYYMM"] = df["YYYYMM"].astype("string")
df["Year"] = df["YYYYMM"].str[:4]
df["Month"] = df["YYYYMM"].str[4:]
df = df[["Year", "Month", "Value", "Unit", "Description"]]

list_of_sectors = ['Primary Energy Consumed by the Residential Sector', 'Primary Energy Consumed by the Commercial Sector',
                   'Primary Energy Consumed by the Industrial Sector', 'Primary Energy Consumed by the Electric Power Sector',
                    'Total Primary Energy Consumed by the Transportation Sector']

df = df[df["Description"].isin(list_of_sectors)]


final_df = df.pivot(index=["Year", "Month"], columns="Description", values="Value").reset_index()
graph_df = final_df.rename(columns={"Total Primary Energy Consumed by the Transportation Sector":"Transportation Sector", 
                         "Primary Energy Consumed by the Electric Power Sector":"Electric Power Sector",
                         "Primary Energy Consumed by the Industrial Sector":"Industrial Sector",
                         "Primary Energy Consumed by the Commercial Sector":"Commercial Sector",
                         "Primary Energy Consumed by the Residential Sector":"Residential Sector"})

graph_sector_list = ["Electric Power Sector", "Transportation Sector", "Industrial Sector", "Residential Sector", "Commercial Sector"]
graph_sector_short = ["Electric", "Transportation", "Industrial", "Residential", "Commercial"]

fig, ax = plt.subplots(figsize=(10,7))

df_2022 = graph_df[(graph_df["Year"] == "2022") & (graph_df["Month"]=="13")]

plot2 = sns.barplot(
    df_2022, x=graph_sector_short, y=df_2022[graph_sector_list].values[0]
)
plot2.xaxis.set_label_text("Sector")
plot2.yaxis.set_label_text("Energy Output (in Trillion Btu)")
plot2.set_title("Total Energy Output Per Sector in 2022")

stacked_df = graph_df[graph_df["Month"] == "13"]
stacked_df = stacked_df[
    [
        "Year",
        "Electric Power Sector", "Transportation Sector", "Industrial Sector", "Residential Sector", "Commercial Sector"
    ]
]

stacked_df.plot(
    kind="bar",
    x="Year",
    stacked=True,
    figsize=(10, 7),
    title="Total Energy Output Per Sector from 1949-2022",
    xlabel="Year",
    ylabel="Energy Output (in Btu)",
)
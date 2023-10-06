import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_monthDist(df):
    monthDist = df_clean.groupby(by=["year", "month"]).registered.sum().reset_index()
    return monthDist

def create_seasonDist(df):
    seasonDist = df_clean.groupby("season").total_count.sum().reset_index()
    return seasonDist

def create_meandDf(df):
    mean_df = df_clean.groupby("workingday").total_count.mean().reset_index()
    mean_df['workingday'] = mean_df['workingday'].apply(lambda x: "weekend" if x == 0 else "weekday" )
    return mean_df

def create_hourTrend(df):
    hourTrend = df_clean.groupby(by=["hour", "season"]).total_count.sum().reset_index()
    return hourTrend

df_clean = pd.read_csv("df_clean.csv")

# Memastikan bahwa kolom date bertipe datetime
datetime_columns = ["date"]
df_clean.sort_values(by="date", inplace=True)
df_clean.reset_index(inplace=True)
 
for column in datetime_columns:
    df_clean[column] = pd.to_datetime(df_clean[column])



min_date = df_clean["date"].min()
max_date = df_clean["date"].max()


with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_clean[(df_clean["date"] >= str(start_date)) & 
                (df_clean["date"] <= str(end_date))]

monthDist = create_monthDist(main_df)
seasonDist = create_seasonDist(main_df)
mean_df = create_meandDf(main_df)
hourTrend = create_hourTrend(main_df)


st.header("Bike Sharing Dashboard")

# Bar plot 1
st.subheader("Tren Penggunaan Sepeda")

fig = plt.figure(figsize=(10,5))
colors = ["#bc5090", "#ffa600"] 
sns.barplot(
    x="month",
    y="registered",
    hue="year",
    data=monthDist,
    palette=colors
)

plt.xlabel(None)
plt.ylabel(None)
st.pyplot(fig)

# Bar plot 2
st.subheader("Distribusi Pengguna Sepeda Berdasarkan Musim")
from matplotlib.ticker import FuncFormatter

def format_million(value, _):
    return f"{value / 1e6:.1f}M"

fig=plt.figure(figsize=(10,5))
colors = ["#197278", "#C51605", "#279EFF", "#F7D060"]
sns.barplot(
    x="season",
    y="total_count",
    data=seasonDist.sort_values(by="total_count", ascending=False),
    palette=colors
)

plt.title("Distribusi Pengguna Sepeda Berdasarkan Musim", loc="center", fontsize=15)
plt.xlabel(None)
plt.ylabel(None)
# Atur formatter untuk sumbu x
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_million))
st.pyplot(fig)

# Bar plot 3
st.subheader("Rata-Rata Jumlah Pengguna Sepeda")

fig=plt.figure(figsize=(10,5))
sns.barplot(
    x="workingday",
    y="total_count",
    data = mean_df,
    palette=["#279EFF","#ffa600"]
)

plt.title("Perbandingan Rata-Rata Jumlah Pengguna Sepeda", loc="center", fontsize=15)
plt.xlabel(None)
plt.ylabel(None)
st.pyplot(fig)

# Line Plot
st.subheader("Tren Penggunaan Sepeda Per Jam")
fig=plt.figure(figsize=(10,5))

sns.lineplot(
    x="hour",
    y="total_count",
    hue="season",
    data=hourTrend,
    palette=["#F7D070", "#C51605", "#197278", "#279EFF" ]
)
plt.title("Tren Pengguna Sepeda Per Jam", loc="center", fontsize=15)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(hourTrend['hour'])
st.pyplot(fig)
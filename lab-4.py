import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px


covid_data_url = "countries-aggregated.csv"
covid_data = pd.read_csv(covid_data_url)


covid_data['Date'] = pd.to_datetime(covid_data['Date'])
covid_data = covid_data.groupby(['Date', 'Country']).sum().reset_index()


geo_data_url = "countries_without_geometry.csv"
geo_data = gpd.read_file(geo_data_url)


merged_data = geo_data.merge(covid_data, how='left', left_on='ADMIN', right_on='Country')

cleaned_data = merged_data.dropna(subset=['Country'])    # видаляє рядки, де в 'Country' є NaN


cleaned_data['Confirmed'] = cleaned_data['Confirmed'].fillna(0)  # Перевірка, чи є NaN у 'Confirmed', і заповняєє їх нулями


cleaned_data['Country'] = cleaned_data['Country'].astype(str)   # Перетворює назви країн на рядкові значення


def plot_histogram(data, title):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Country'], data['Confirmed'])
    plt.title(title)
    plt.xticks(rotation=90)
    plt.xlabel('Countries')
    plt.ylabel('Total Cases')
    plt.tight_layout()
    plt.show()


plot_histogram(cleaned_data, "Total COVID-19 Cases by Country")


filtered_data = covid_data[covid_data['Date'] == covid_data['Date'].max()]

fig = px.choropleth(
    filtered_data,
    locations='Country',
    locationmode='country names',
    color='Confirmed',
    hover_name='Country',
    color_continuous_scale=px.colors.sequential.Viridis
)

fig.show()



covid_data['new_cases'] = covid_data.groupby('Country')['Confirmed'].diff().fillna(0)   #різниця
covid_data['growth_rate'] = covid_data.groupby('Country')['Confirmed'].pct_change().fillna(0) #%


print(covid_data[['Country', 'Date', 'Confirmed', 'new_cases', 'growth_rate']].tail())



fastest_growth = covid_data.loc[covid_data['new_cases'].idxmax()]
print(f"Country with fastest growth: {fastest_growth['Country']} with {fastest_growth['new_cases']} new cases on {fastest_growth['Date']}.")



selected_countries = ['Ukraine', 'Zimbabwe', 'Niger']
filtered_countries_data = covid_data[covid_data['Country'].isin(selected_countries)]


plt.figure(figsize=(12, 6))
for country in selected_countries:
    country_data = filtered_countries_data[filtered_countries_data['Country'] == country]
    plt.plot(country_data['Date'], country_data['Confirmed'], marker='o', label=country)

plt.title('COVID-19 Confirmed Cases Dynamics')
plt.xlabel('Date')
plt.ylabel('Total Confirmed Cases')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

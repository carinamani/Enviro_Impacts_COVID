#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:02:40 2024

@author: carinamanitius
"""

import os
import pandas as pd


# Get the current working directory
cd = os.getcwd()



###### Import and clean data


# UNWTO tourism arrivals 

tourist_arrivals = pd.read_csv(f"{cd}/DATA/RAW/UNWTO_tourist_arrivals.csv")

#tourist_arrivals['source'] = 'UNWTO'
#tourist_arrivals['geography'] = 'Global'


# IEA aviation emissions
aviation_emissions = pd.read_csv(f"{cd}/DATA/RAW/IEA_aviation_emissions.csv")

#aviation_emissions['source'] = 'IEA'
#aviation_emissions['geography'] = 'Global'


# Friedlingstein et al (2023) global carbon emissions 

# aggregated FF and LUC emissions 
GHG_emissions = pd.read_excel(
    f"{cd}/DATA/RAW/Data supplement to the Global Carbon Budget 2023/Global_Carbon_Budget_2023v1.1.xlsx",
    sheet_name="Global Carbon Budget",
    skiprows=21  
)

GHG_emissions = GHG_emissions.filter(items=["Year", "fossil emissions excluding carbonation", "land-use change emissions"])

GHG_emissions = GHG_emissions.rename(columns={
    "Year": "Year",
    "fossil emissions excluding carbonation": "fossil_fuel_emissions_GtCarbon",
    "land-use change emissions": "land_use_emissions_GtCarbon"
})

GHG_emissions['total_emissions_GtCarbon'] = GHG_emissions['fossil_fuel_emissions_GtCarbon'] + GHG_emissions['land_use_emissions_GtCarbon']

#GHG_emissions['source'] = 'Friedlingstein et al (2023)'
#GHG_emissions['geography'] = 'Global'

# deforestation only 
deforestation_emissions = pd.read_excel(
    f"{cd}/DATA/RAW/Data supplement to the Global Carbon Budget 2023/Global_Carbon_Budget_2023v1.1.xlsx",
    sheet_name="Land-Use Change Emissions",
    skiprows=37  
)

deforestation_emissions = deforestation_emissions.filter(items=["Unnamed: 0", "deforestation (total)"])

deforestation_emissions = deforestation_emissions.rename(columns={
    "Unnamed: 0": "Year",
    "deforestation (total)": "deforestation_emissions_GtCarbon"
})

#deforestation_emissions['source'] = 'Friedlingstein et al (2023)'
#deforestation_emissions['geography'] = 'Global'


# GFW deforestation 

GFW_deforestation = pd.read_csv(f"{cd}/DATA/RAW/Global Primary Forest loss/treecover_loss__ha.csv")

GFW_deforestation_global = GFW_deforestation.groupby('umd_tree_cover_loss__year')[['umd_tree_cover_loss__ha', 'gfw_gross_emissions_co2e_all_gases__Mg']].sum().reset_index()

GFW_deforestation_global = GFW_deforestation_global.rename(columns={
    "umd_tree_cover_loss__year": "Year",
    "umd_tree_cover_loss__ha": "deforestation_HA", 
    "gfw_gross_emissions_co2e_all_gases__Mg": "deforestation_emissions_Mg_co2e"
})

#GFW_deforestation_global['source'] = 'GFW'
#GFW_deforestation_global['geography'] = 'Global'


# UNCTAD shipping emissions

shipping_emissions = pd.read_csv(f"{cd}/DATA/RAW/UNCTAD_shipping_emissions.csv")

shipping_emissions['shipping_emissions_all_types_Mt_co2'] = shipping_emissions['Tankers'] + shipping_emissions['Dry bulk and general cargo'] + shipping_emissions['Container'] + shipping_emissions['Other']

shipping_emissions['Date'] = pd.to_datetime(shipping_emissions['Date'], format='%b-%y')
shipping_emissions['Year'] = shipping_emissions['Date'].dt.year
shipping_emissions = shipping_emissions[shipping_emissions['Year'] != 2023]
shipping_emissions = shipping_emissions.drop(columns=['Date'])

shipping_emissions_annual = shipping_emissions.groupby('Year').sum().reset_index()
shipping_emissions_annual = shipping_emissions_annual.filter(items=["Year", "shipping_emissions_all_types_Mt_co2"])

#shipping_emissions_annual['source'] = 'UNCTAD'
#shipping_emissions_annual['geography'] = 'Global'


# UNCTAD shipping volumne

shipping_volume = pd.read_csv(f"{cd}/DATA/RAW/UNCTAD_shipping_volume.csv")

shipping_volume = shipping_volume[(shipping_volume['Economy_Label'] == 'World') & (shipping_volume['CargoType_Label'] == 'Total goods discharged')]

value_columns = [col for col in shipping_volume.columns if col.endswith('_Value')]
shipping_volume = shipping_volume[value_columns]

shipping_volume.columns = [col.split('_')[0] for col in shipping_volume.columns]

shipping_volume_long = shipping_volume.reset_index().melt(id_vars=['index'], value_vars=shipping_volume.columns,
                                                                 var_name='Year', value_name='shipping_volume_million_metric_tons')

shipping_volume_long = shipping_volume_long.drop(columns=['index'])


# import growth rates for 2022/23
shipping_volume_gr = pd.read_csv(f"{cd}/DATA/RAW/UNCTAD_shipping_volume_growth_rates.csv")

shipping_volume_gr['growth_rate_multiplier'] = (shipping_volume_gr['Tons']+100)/100
shipping_volume_gr = shipping_volume_gr.drop(columns=['Tons'])

shipping_gr_2022 = shipping_volume_gr[shipping_volume_gr['Date'] == 2022]['growth_rate_multiplier'].iloc[0]
shipping_gr_2023 = shipping_volume_gr[shipping_volume_gr['Date'] == 2023]['growth_rate_multiplier'].iloc[0]

shipping_2021 = shipping_volume_long[shipping_volume_long['Year'] == '2021']['shipping_volume_million_metric_tons'].iloc[0]
shipping_2022 = shipping_2021 * shipping_gr_2022
shipping_2023 = shipping_2022 * shipping_gr_2023

row_2022 = pd.DataFrame({'Year': ['2022'], 'shipping_volume_million_metric_tons': [shipping_2022]})
row_2023 = pd.DataFrame({'Year': ['2023'], 'shipping_volume_million_metric_tons': [shipping_2023]})

shipping_volume_long = pd.concat([shipping_volume_long, row_2022, row_2023], ignore_index=True)
shipping_volume_long['Year'] = shipping_volume_long['Year'].astype(int)

#shipping_volume_long['source'] = 'UNCTAD'
#shipping_volume_long['geography'] = 'Global'


# Our World in Data / IEA car sales

car_sales = pd.read_csv(f"{cd}/DATA/RAW/OWD_car_sales.csv")
car_sales = car_sales.drop(columns=['Entity', 'Code'])

car_sales = car_sales.rename(columns={
    "Year": "Year",
    "Electric cars sold": "cars_sold_EV", 
    "Non-electric car sales": "cars_sold_non_EV"
})

car_sales['cars_sold_total'] = car_sales['cars_sold_EV'] + car_sales['cars_sold_non_EV']

#car_sales['source'] = 'Our World in Data - IEA'
#car_sales['geography'] = 'Global'


# USGS cement production 

cement_production = pd.read_csv(f"{cd}/DATA/RAW/USGS_cement.csv")
cement_production = cement_production.filter(items=["Year", "cement_production_thousand_metric_tons"])

#cement_production['source'] = 'USGS'
#cement_production['geography'] = 'Global'


# IPSOS happiness

happiness = pd.read_csv(f"{cd}/DATA/RAW/IPSOS_happiness.csv")

#happiness['source'] = 'IPSOS'
#happiness['geography'] = 'Global average'


# US NPS visits

US_park_visits = pd.read_csv(f"{cd}/DATA/RAW/US_NPS_visits.csv")

#US_park_visits['source'] = 'NPS'
#US_park_visits['geography'] = 'USA'


# FAO fish landings 
fishing = pd.read_csv(f"{cd}/DATA/RAW/FAO_fish_landed.csv")
fishing = fishing.loc[:, ~fishing.columns.str.contains('Flag')]
fishing = fishing[fishing['Unit Name'] != 'Number']

fishing_global = fishing.drop(columns=['Country Name En', 'Unit Name']).sum()

fishing_global = fishing_global.reset_index()
fishing_global.columns = ['Year', 'tonnes_fish_landed']

fishing_global['Year'] = fishing_global['Year'].astype(int)

#fishing.to_csv(f"{cd}/DATA/CLEAN/fish_data.csv")

#fishing_global['source'] = 'FAO'
#fishing_global['geography'] = 'Global'


# IEA passenger cars and vans
emissions_cars_vans = pd.read_csv(f"{cd}/DATA/RAW/IEA_emissions_cars_vans.csv")

emissions_cars_vans = emissions_cars_vans.rename(columns={
    "Unnamed: 0": "Year",
    "Car and vans emissions": "passenger_vehicle_emissions_Gt_co2"
})

#emissions_cars_vans['source'] = 'IEA'
#emissions_cars_vans['geography'] = 'Global'


# OEC timber trade 
timber_trade = pd.read_csv(f"{cd}/DATA/RAW/OEC_timber_trade.csv")

timber_trade = timber_trade.drop(columns=['Continent ID', 'Continent', 'Country ID', 'Country', 'ISO 3', 'share'])
timber_trade = timber_trade.groupby('Year')[['Trade Value']].sum().reset_index()

timber_trade = timber_trade.rename(columns={
    "Year": "Year",
    "Trade Value": "exports_timber_products_USD"
})

#timber_trade['source'] = 'OEC'
#timber_trade['geography'] = 'Global'


# NBER US WFH 
US_WFH = pd.read_excel(
    f"{cd}/DATA/RAW/NBER_WFH.xlsx",
    sheet_name="WFH 1965 - present",
)

US_WFH = US_WFH.drop(columns=['Source_historical_series', 'fullremote_hist', 'Source_fullremote_hist', 'Notes', 'License', 'Citation'])

US_WFH['Year'] = US_WFH['date'].dt.year
US_WFH = US_WFH.drop(columns=['date'])

US_WFH_yearly_avg = US_WFH.groupby('Year').mean().reset_index()

US_WFH_yearly_avg = US_WFH_yearly_avg.rename(columns={
    "Year": "Year",
    "WFH_share": "USA_WFH_share"
})

#US_WFH_yearly_avg['source'] = 'NBER'
#US_WFH_yearly_avg['geography'] = 'USA'


# OECD municipal waste  
OECD_waste = pd.read_csv(f"{cd}/DATA/RAW/OECD_municipal_waste.csv")

OECD_waste = OECD_waste[['TIME_PERIOD', 'OBS_VALUE']]

OECD_waste = OECD_waste.rename(columns={
    "TIME_PERIOD": "Year",
    "OBS_VALUE": "total_municipal_waste_tonnes"
})

#OECD_waste['source'] = 'OECD'
#OECD_waste['geography'] = 'OECD'


# Outdoor participation

outdoor_participation = pd.read_csv(f"{cd}/DATA/RAW/outdoor_participation.csv")

#outdoor_participation['source'] = 'UNWTO'
#outdoor_participation['geography'] = 'Global'


# US Census gardening spend

gardening_spend = pd.read_csv(f"{cd}/DATA/RAW/gardening_spend.csv")

#gardening_spend['source'] = 'UNWTO'
#gardening_spend['geography'] = 'Global'


# US paid fishing license holders

fishing = pd.read_csv(f"{cd}/DATA/RAW/USFWS_Paid_Fishing_License_Holders.csv")

#gardening_spend['source'] = 'UNWTO'
#gardening_spend['geography'] = 'Global'


# US paid hunting license holders

hunting = pd.read_csv(f"{cd}/DATA/RAW/USFWS_Paid_Hunting_License_Holders.csv")

#gardening_spend['source'] = 'UNWTO'
#gardening_spend['geography'] = 'Global'


# US oudoor recreation participation

outdoor_parcipitation = pd.read_csv(f"{cd}/DATA/RAW/outdoor_trends.csv")

#gardening_spend['source'] = 'UNWTO'
#gardening_spend['geography'] = 'Global'

# Finland outdoor visits

Finland_outdoor_visits = pd.read_csv(f"{cd}/DATA/RAW/Finland_outdoor_visits.csv")

#gardening_spend['source'] = 'UNWTO'
#gardening_spend['geography'] = 'Global'

###### Merge data

merged_data = tourist_arrivals.copy()  
merged_data = pd.merge(merged_data, aviation_emissions, on='Year', how='outer')
merged_data = pd.merge(merged_data, GHG_emissions, on='Year', how='outer')
merged_data = pd.merge(merged_data, deforestation_emissions, on='Year', how='outer')
merged_data = pd.merge(merged_data, GFW_deforestation_global, on='Year', how='outer')
merged_data = pd.merge(merged_data, shipping_emissions_annual, on='Year', how='outer')
merged_data = pd.merge(merged_data, shipping_volume_long, on='Year', how='outer')
merged_data = pd.merge(merged_data, car_sales, on='Year', how='outer')
merged_data = pd.merge(merged_data, cement_production, on='Year', how='outer')
merged_data = pd.merge(merged_data, happiness, on='Year', how='outer')
merged_data = pd.merge(merged_data, US_park_visits, on='Year', how='outer')
merged_data = pd.merge(merged_data, fishing_global, on='Year', how='outer')
merged_data = pd.merge(merged_data, emissions_cars_vans, on='Year', how='outer')
merged_data = pd.merge(merged_data, timber_trade, on='Year', how='outer')
merged_data = pd.merge(merged_data, US_WFH_yearly_avg, on='Year', how='outer')
merged_data = pd.merge(merged_data, OECD_waste, on='Year', how='outer')
merged_data = pd.merge(merged_data, outdoor_participation, on='Year', how='outer')
merged_data = pd.merge(merged_data, gardening_spend, on='Year', how='outer')
merged_data = pd.merge(merged_data, fishing, on='Year', how='outer')
merged_data = pd.merge(merged_data, hunting, on='Year', how='outer')
merged_data = pd.merge(merged_data, outdoor_parcipitation, on='Year', how='outer')
merged_data = pd.merge(merged_data, Finland_outdoor_visits, on='Year', how='outer')

merged_data.to_csv(f"{cd}/DATA/CLEAN/merged_data_gross.csv")






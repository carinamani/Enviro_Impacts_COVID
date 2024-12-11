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



###### Import data


# UNWTO tourism arrivals 

tourist_arrivals = pd.read_csv(f"{cd}/DATA/RAW/UNWTO_tourist_arrivals.csv")

tourist_arrivals['source'] = 'UNWTO'
tourist_arrivals['geography'] = 'Global'

# IEA aviation emissions
aviation_emissions = pd.read_csv(f"{cd}/DATA/RAW/IEA_aviation_emissions.csv")

aviation_emissions['source'] = 'IEA'
aviation_emissions['geography'] = 'Global'

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

GHG_emissions['source'] = 'Friedlingstein et al (2023)'
GHG_emissions['geography'] = 'Global'

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

deforestation_emissions['source'] = 'Friedlingstein et al (2023)'
deforestation_emissions['geography'] = 'Global'








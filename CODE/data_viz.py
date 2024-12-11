#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:59:13 2024

@author: carinamanitius
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the current working directory
cd = os.getcwd()


# Load data 
gross_impact = pd.read_csv(f"{cd}/DATA/CLEAN/merged_data_gross.csv", index_col=False)
gross_impact = gross_impact.drop(columns=['Unnamed: 0'])


# Normalize data 

normalized_impact = gross_impact.copy()

for column in normalized_impact.columns:
    if column != 'Year':
        value_2019 = normalized_impact.loc[normalized_impact['Year'] == 2019, column].values[0]
        normalized_impact[column] = (normalized_impact[column] / value_2019) * 100

normalized_impact.to_csv(f"{cd}/DATA/CLEAN/merged_data_normalized.csv")


#### SELECT YEARS
normalized_impact_filtered = normalized_impact[(normalized_impact['Year'] >= 2000)]

##### SELECT VARS 
column_names = normalized_impact.columns.tolist()
print(column_names)

normalized_impact_filtered = normalized_impact_filtered[['Year', 
                                                'int_tourist_arrivals_millions',
                                                'fossil_fuel_emissions_GtCarbon',
                                                'deforestation_emissions_GtCarbon',
                                                'deforestation_HA', 
                                                'shipping_volume_million_metric_tons', 
                                                'cars_sold_non_EV', 
                                                'cement_production_thousand_metric_tons',
                                                'tonnes_fish_landed'
                                               ]]

# Plot
plt.figure(figsize=(10, 6))

for column in normalized_impact_filtered.columns:
    if column != 'Year':
        plt.plot(normalized_impact_filtered['Year'], normalized_impact_filtered[column], label=column)

plt.xlabel('Year')
plt.ylabel('Normalized Impact')
plt.title('Normalized Impact Over Time')

# Add a legend
plt.legend()

# Show the plot
plt.show()











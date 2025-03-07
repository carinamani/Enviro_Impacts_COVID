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
                                                'total_municipal_waste_tonnes'
                                               ]]

# Plot
plt.figure(figsize=(10, 6))

for column in normalized_impact_filtered.columns:
    if column != 'Year':
        plt.plot(normalized_impact_filtered['Year'], normalized_impact_filtered[column], label=column)

plt.xlabel('Year')
plt.ylabel('Normalized Impact')
plt.title('Normalized Impact Over Time')

plt.legend()

plt.savefig(f"{cd}/FIGURES/normalized_line_ugly.png", dpi=300)  

plt.show()


# Plot PRETTY 

final_plot = normalized_impact[(normalized_impact['Year'] >= 2010)]

final_plot = final_plot[['Year', 
                         'int_tourist_arrivals_millions',
                         'fossil_fuel_emissions_GtCarbon', 
                         'shipping_volume_million_metric_tons', 
                         'cement_production_thousand_metric_tons', 
                         'millions_sales_garden_equipment',
                         'Finland_outdoor_visits',
                         'USA_WFH_share'
                          ]]

line_styles = {
    'int_tourist_arrivals_millions': {'color': 'red', 'linestyle': '-'},
    'fossil_fuel_emissions_GtCarbon': {'color': 'red', 'linestyle': '--'},
    'shipping_volume_million_metric_tons': {'color': 'black', 'linestyle': '-'},
    'cement_production_thousand_metric_tons': {'color': 'black', 'linestyle': '--'},
    'millions_sales_garden_equipment': {'color': 'green', 'linestyle': '-'},
    'Finland_outdoor_visits': {'color': 'green', 'linestyle': ':'},
    'USA_WFH_share': {'color': 'green', 'linestyle': '--'}
}

plt.figure(figsize=(10, 6))

for column in final_plot.columns:
    if column != 'Year':
        plt.plot(
            final_plot['Year'], 
            final_plot[column], 
            label=column, 
            color=line_styles[column]['color'], 
            linestyle=line_styles[column]['linestyle']
        )
        
plt.axhline(y=100, color='grey', linestyle=':', linewidth=1)

plt.xlabel('Year')
plt.ylabel('Index, 2019=100')
plt.title('Normalized Impact Over Time')
plt.legend()

plt.ylim(30, 160)

plt.savefig(f"{cd}/FIGURES/normalized_line_pretty.png", dpi=300)  

plt.show()




# Plot PRETTY WFH

final_plot = normalized_impact[(normalized_impact['Year'] >= 2010)]

final_plot = final_plot[['Year', 
                         'USA_WFH_share'
                          ]]

line_styles = {
    'USA_WFH_share': {'color': 'green', 'linestyle': '-'},
}

plt.figure(figsize=(10, 6))

for column in final_plot.columns:
    if column != 'Year':
        plt.plot(
            final_plot['Year'], 
            final_plot[column], 
            label=column, 
            color=line_styles[column]['color'], 
            linestyle=line_styles[column]['linestyle']
        )
        
plt.axhline(y=100, color='grey', linestyle=':', linewidth=1)

plt.xlabel('Year')
plt.ylabel('Index, 2019=100')
plt.title('Normalized Impact Over Time')
plt.legend()

plt.savefig(f"{cd}/FIGURES/normalized_line_pretty_WFH.png", dpi=300)  

plt.show()




# Outdoor rec test

outdoor_test = normalized_impact[(normalized_impact['Year'] >= 2010)]

final_plot = outdoor_test[['Year', 
                         'participation_in_outdoor_rec_percent',
                         'participation_in_outdoor_rec_million',
                         'number_of_outdoor_excursions'
                          ]]

line_styles = {
    'participation_in_outdoor_rec_percent': {'color': 'green', 'linestyle': '--'},
    'participation_in_outdoor_rec_million': {'color': 'green', 'linestyle': '-'},
    'number_of_outdoor_excursions': {'color': 'green', 'linestyle': ':'}
}

plt.figure(figsize=(10, 6))

for column in final_plot.columns:
    if column != 'Year':
        plt.plot(
            final_plot['Year'], 
            final_plot[column], 
            label=column, 
            color=line_styles[column]['color'], 
            linestyle=line_styles[column]['linestyle']
        )
        
plt.axhline(y=100, color='grey', linestyle=':', linewidth=1)

plt.xlabel('Year')
plt.ylabel('Index, 2019=100')
plt.title('Normalized Impact Over Time')
plt.legend()

plt.savefig(f"{cd}/FIGURES/outdoor_rec_test.png", dpi=300)  

plt.show()







# Plot PRETTY 

final_plot = normalized_impact[(normalized_impact['Year'] >= 2010)]

final_plot = final_plot[['Year', 
                         'land_use_emissions_GtCarbon',
                         'fossil_fuel_emissions_GtCarbon'
                          ]]

line_styles = {
    'land_use_emissions_GtCarbon': {'color': 'red', 'linestyle': '-'},
    'fossil_fuel_emissions_GtCarbon': {'color': 'red', 'linestyle': '--'}
}

plt.figure(figsize=(10, 6))

for column in final_plot.columns:
    if column != 'Year':
        plt.plot(
            final_plot['Year'], 
            final_plot[column], 
            label=column, 
            color=line_styles[column]['color'], 
            linestyle=line_styles[column]['linestyle']
        )
        
plt.axhline(y=100, color='grey', linestyle=':', linewidth=1)

plt.xlabel('Year')
plt.ylabel('Index, 2019=100')
plt.title('Normalized Impact Over Time')
plt.legend()

plt.ylim(30, 160)

plt.savefig(f"{cd}/FIGURES/normalized_line_pretty_LU.png", dpi=300)  

plt.show()







# Plot PRETTY 

final_plot = normalized_impact[(normalized_impact['Year'] >= 2010)]

final_plot = final_plot[['Year', 
                         'Finland_outdoor_visits'
                          ]]

line_styles = {
    'Finland_outdoor_visits': {'color': 'green', 'linestyle': '-'}
}

plt.figure(figsize=(10, 6))

for column in final_plot.columns:
    if column != 'Year':
        plt.plot(
            final_plot['Year'], 
            final_plot[column], 
            label=column, 
            color=line_styles[column]['color'], 
            linestyle=line_styles[column]['linestyle']
        )
        
plt.axhline(y=100, color='grey', linestyle=':', linewidth=1)

plt.xlabel('Year')
plt.ylabel('Index, 2019=100')
plt.title('Normalized Impact Over Time')
plt.legend()

plt.ylim(30, 160)

plt.savefig(f"{cd}/FIGURES/Finland_visits.png", dpi=300)  

plt.show()


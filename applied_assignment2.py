# -*- coding: utf-8 -*-
"""
Created on Sun Dec 8 11:43:54 2022

@author: ThinkPad E590
"""

import pandas as pd

# list of countries (global variable)
countries = ['Pakistan', 'India', 'New Zealand', 'China', 'United Kingdom']

def data_frame(data, indicator):
    """
    Produces a data frame.
    data: list of data values
    incdicator: data column
    
    this function is used to read the file using pandas. use to filter indicator and make  new 
    data frames, in last this function returns three variable data frame countries,years 
    and original form of data.
    """
    
    df_worldBank = pd.read_csv(data, skiprows=(4), index_col=(False))  # read csv file
    df_worldBank = df_worldBank.loc[:, ~df_worldBank.columns.str.contains(
        'Unnamed')]  # remove unnamed column

    df_countries = df_worldBank.loc[df_worldBank['Country Name'].isin(countries)] #
    df_countries = df_worldBank.loc[df_worldBank['Indicator Code'].eq(indicator)]
    df_years = df_countries.melt(id_vars=['Country Name', 'Country Code',
                  'Indicator Name', 'Indicator Code'], var_name='Years')
    # df_years = df_worldBank.drop(['Country Code'],axis=1)
    del df_years['Country Code']  # Deleting column
    df_years = df_years.pivot_table('value', ['Years', 'Indicator Name', 'Indicator Code'],
                          'Country Name').reset_index()
    return df_countries, df_years, df_worldBank

df = data_frame('climate_data.csv', 'SP.URB.TOTL')
print(df)
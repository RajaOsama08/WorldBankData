# -*- coding: utf-8 -*-
"""
Created on Sun Dec 8 11:43:54 2022

@author: ThinkPad E590
"""

import pandas as pd
import matplotlib.pyplot as plt

# list of countries (global variable)
countries = ['Pakistan', 'India', 'New Zealand', 'China', 'United Kingdom']


def data_frame(data, indicator):
    """
    Produces a data frame.
    data: list of data values
    incdicator: data column

    this function is used to read the file using pandas. use to filter
    indicator and make  new data frames, in last this function returns three
    variable data frame countries,years and original form of data.
    """
    # read csv file
    df_worldBank = pd.read_csv(data, skiprows=(
        4), index_col=(False))
    # removing unnecessary column which are unnamed
    df_worldBank = df_worldBank.loc[:, ~df_worldBank.columns.str.contains(
        'Unnamed')]

    # .isin() is pandas method used to filter data frames
    df_countries = df_worldBank.loc[df_worldBank['Country Name'].isin(
        countries)]

    # .eq is a wrapper use for comparison in dataframe objects with constants,
    # below indicator is constant
    df_countries = df_worldBank.loc[df_worldBank['Indicator Code'].eq(
        indicator)]

    # .melt is a another type of transpose in this all column remain same.
    # Below Just change Years into rows
    df_years = df_countries.melt(id_vars=['Country Name', 'Country Code',
                                          'Indicator Name', 'Indicator Code'],
                                 var_name='Years')
    # usign del funtion drop out the column
    del df_years['Country Code']

    df_years = df_years.pivot_table('value', ['Years', 'Indicator Name', 'Indicator Code'],
                                    'Country Name').reset_index()
    return df_countries, df_years, df_worldBank

# Line plot


def line_plot(data, indicator_name, file_name):
    # set figure size
    plt.figure(dpi=144)

    # filter years
    data = data[(data['Years'] >= "1990") & (
        data['Years'] <= "2020")]
    data['Years'] = pd.to_numeric(data['Years'])
    data.plot("Years", countries, title=indicator_name,
              legend='leftbottom', linestyle="-.")
    # setting lable on y axis
    plt.ylabel('Data Growth')
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, bbox_inches='tight')
    return plt.show()


# line chart 1
# passing file name and indicator in data_frame function
df_countries, df_years, df_data = data_frame('climate_data.csv', 'SP.URB.TOTL')
# passing year data frame and Urban population in line_plot function
line_plot(df_years, 'Urban population', 'line_urban.png')

# line chart 2
# passing file name and indicator in data_frame function
df_countries, df_year, df_data = data_frame(
    'climate_data.csv', 'AG.YLD.CREL.KG')
# passing year data frame and Cereal yield in line_plot function
line_plot(df_years, 'Cereal yield', 'line_creal.png')

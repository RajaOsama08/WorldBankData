# -*- coding: utf-8 -*-
"""
Created on Sun Dec 8 11:43:54 2022

@author: ThinkPad E590
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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

# Line plot accepts file, indicator, image name


def line_plot(data, indicator_name, image_name):
    """
    Produces a line plot.
    data: list of data values
    incdicator: a constant value contain name of indicator
    image_name: name of plot image

    this function is used to take three arguments. first filter the data on based on countries name
    then match the data with a constant variable named indicator. When data is match further we plot
    the data. Also, save the plot image before return
    """
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
    # take constant file name. second argumend is used to remove extra spaces in image
    plt.savefig(image_name, bbox_inches='tight')
    return plt.show()


# Bar chart accepts file, y-axis label, indicator, image name


def bar_chart(data, indicator_name, y_label, image_name):
    """
    Produces a Bar Chart.
    data: list of data values
    incdicator: a constant value contain name of indicator
    y_label: a constant value contain name of label
    file_name: name of plot image

    this function is used to take four arguments. first filter the data on based on countries name
    then match the data with a constant variable named indicator.Third argument is a constant
    name of label y-axis. In last, when data is match further we plot the bar chat of data.
    Also, save the plot image before return
    """
    data = data.loc[data['Years'].isin(
        ['1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005'])]

    num = np.arange(10)
    width = 0.2
    # Used (tolist) to convert array values to list
    years = data['Years'].tolist()

    plt.figure()
    plt.title(indicator_name)
    plt.bar(num+0.2, data['India'], width, label='India')
    plt.bar(num-0.2, data['China'], width, label='China')
    plt.bar(num, data['United Kingdom'], width, label='united Kingdom')

    plt.xticks(num, years)  # This is for showing years in x asis
    plt.xlabel('Years')
    plt.ylabel(y_label)
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    # take constant file name. second argumend is used to remove extra spaces in image
    plt.savefig(image_name, bbox_inches='tight')
    return plt.show()


def heat_map(data, country, image_name):
    """
    Produces a Heat Map.
    data: list of data values
    country: a constant variable contain country name
    file_name: name of plot image

    this function is used to take three arguments. first filter the data on based on indicators
    then match the data with a constant variable of countries.Third argument is a constant
    name of heat map image. After ploting the heat map correlation matrix. In last, we save the
    heat map image before return
    """
    data = data.drop(['Country Code', 'Indicator Name'], axis=1)
    # create data frame
    new_df = pd.DataFrame()

    # get indicator data
    Indicator_data = data[data["Indicator Code"] == "SP.URB.TOTL"]

    # finding country data
    Indicator_data = Indicator_data[Indicator_data['Country Name'] == country].drop(
        ['Country Name', 'Indicator Code'], axis=1).T
    # drop nan values and taking transpose
    Indicator_data = Indicator_data.dropna().T
    # urban population data
    new_df["Urban population"] = Indicator_data.iloc[0]
    #  cereal yield data
    Indicator_data = data[data["Indicator Code"] == 'AG.YLD.CREL.KG']

    Indicator_data = Indicator_data[Indicator_data['Country Name'] == country].drop(
        ['Country Name', 'Indicator Code'], axis=1).T

    Indicator_data = Indicator_data.dropna().T

    new_df['Cereal yield (kg per hectare)'] = Indicator_data.iloc[0]

    #  electricity form coal data
    Indicator_data = data[data["Indicator Code"] == 'EG.ELC.COAL.ZS']

    Indicator_data = Indicator_data[Indicator_data['Country Name'] == country].drop(
        ['Country Name', 'Indicator Code'], axis=1).T

    Indicator_data = Indicator_data.dropna().T

    new_df['Electricity form coal'] = Indicator_data.iloc[0]

    # CO2 emission data
    Indicator_data = data[data["Indicator Code"] == 'EN.ATM.CO2E.KT']

    Indicator_data = Indicator_data[Indicator_data['Country Name'] == country].drop(
        ['Country Name', 'Indicator Code'], axis=1).T

    Indicator_data = Indicator_data.dropna().T
    new_df['CO2 emissions (kt)'] = Indicator_data.iloc[0]

    ax = plt.axes()
    # add title
    ax.set_title(country)
    # Create correlation matrix
    corr_matrix = new_df.corr()
    # plot heatmap
    plt.figure(figsize=(10, 8))
    sns.set(font_scale=1.2)
    sns.heatmap(corr_matrix,
                cmap='crest',
                vmin=-1,
                vmax=1,
                center=0,
                annot=True,
                annot_kws=dict(size=14, weight='bold'),
                linecolor='black',
                linewidths=0.5,
                ax=ax)
    # take constant file name. second argumend is used to remove extra spaces in image
    plt.savefig(image_name)
    return plt.show()


# line chart 1
# passing file name and indicator in data_frame function
df_countries, df_years, df_data = data_frame('climate_data.csv', 'SP.URB.TOTL')
# passing year data frame and Urban population in line_plot function
line_plot(df_years, 'Urban population', 'line_urban.png')

# line chart 2
# passing file name and indicator in data_frame function
df_countries, df_years, df_data = data_frame(
    'climate_data.csv', 'AG.YLD.CREL.KG')
# passing year data frame and Cereal yield in line_plot function
line_plot(df_years, 'Cereal yield', 'line_creal.png')


# bar chart
# passing file name and indicator in data_frame function
df_countries, df_years, df_data = data_frame(
    'climate_data.csv', 'EG.ELC.COAL.ZS')
# electricity form coal
bar_chart(df_years, 'Electricity production from coal sources (% of total)',
          'Total population', 'barplot_coal.png')

# passing file name and indicator in data_frame function
df_countries, df_years, df_data = data_frame(
    'climate_data.csv', 'EN.ATM.CO2E.KT')
# passing file name, indicator and image name
bar_chart(df_years, 'CO2 emissions (kt)',
          'Carbon Growth', 'barplot_carbon.png')


# passing file, country name and image name
heat_map(df_data, 'Pakistan', 'heatmap_pak.png')
heat_map(df_data, 'United Kingdom', 'heatmap_uk.png')
heat_map(df_data, 'New Zealand', 'heatmap_nz.png')

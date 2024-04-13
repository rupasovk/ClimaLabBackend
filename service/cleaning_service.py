# -*- coding: utf-8 -*-
"""NEW_CleanningData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-os4HPhxg-Kw0NNY3jw84rGG23HzSaFh
"""

import pandas as pd
import numpy as np


def cleaning_data(output_weather_file, min_error_bound, max_error_bound, output_filename='output_clean_data_test.csv'):
    # station_ids = pd.read_csv('/content/list_of_station_id.csv', sep=';', error_bad_lines=False)
    # station_ids = station_ids['Index'].values
    # output_weather = pd.read_csv('/content/output_weather.csv', error_bad_lines=False)

    # station_ids = pd.read_csv(stations_ids_file, sep=stations_sep)
    # station_ids = station_ids['Index'].values
    output_weather = pd.read_csv(output_weather_file)

    # Создание словаря для отображения старых и новых имен столбцов
    columns_mapping = {
        'Year': 'year',
        'Jan': 'jan',
        'Feb': 'feb',
        'March': 'mar',
        'April': 'apr',
        'May': 'may',
        'June': 'jun',
        'July': 'jul',
        'August': 'aug',
        'September': 'sep',
        'October': 'oct',
        'November': 'nov',
        'December': 'dec',
        'Annual': 'per_year',
        'Station_Number': 'station_number',
        'y_y': 'y',
        'x_y': 'x',
    }

    # Переименование столбцов с использованием метода rename()
    output_weather_renamed = output_weather.rename(columns=columns_mapping)

    # output_weather_renamed

    df = pd.DataFrame(output_weather_renamed)

    # Список столбцов, требующих восстановления
    columns_to_check = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'per_year']

    # Замена значений, которые больше 998 и меньше -998, на NaN для каждого столбца
    for column in columns_to_check:
        # Преобразование столбца в числовой тип данных
        df[column] = pd.to_numeric(df[column], errors='coerce')

        print("min_error_bound + 1: ", min_error_bound + 1)
        print("max_error_bound - 1: ", max_error_bound - 1)

        df.loc[(df[column] >= (max_error_bound - 1)) | (df[column] <= (min_error_bound + 1)), column] = np.nan

        # Вычисление среднего значения и стандартного отклонения для каждого столбца
        means = df[columns_to_check].mean()
        stds = df[columns_to_check].std()

        # Определение границ трех сигм для каждого столбца
        lower_bounds = means - 3 * stds
        upper_bounds = means + 3 * stds

    # Замена значений, которые находятся за пределами трех сигм, на NaN для каждого столбца
    for column in columns_to_check:
        df.loc[(df[column] < lower_bounds[column]) | (df[column] > upper_bounds[column]), column] = np.nan

    df.to_csv(output_filename, index=False)
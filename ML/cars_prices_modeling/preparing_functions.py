import pandas as pd
import numpy as np
import re


def treat_torque(dataframe):
    """
    Function extract Nm and rpm from torque feature and delete it

    :param dataframe: pd.DataFrame treat the torque feature to
    :return: pd.DataFrame
    """
    # rpm
    dataframe['rpm_torque'] = dataframe['torque'].apply(
        lambda x: x if type(x) == float else ' '.join(x.split(" ")[1:]).replace(',', '')
    ).apply(
        lambda x: x if type(x) == float else re.findall('\d+', str(x))
    ).apply(
        lambda x: x if type(x) == float else np.mean([int(i) for i in x])
    )
    # Nm
    dataframe['nm_torque'] = dataframe['torque'].apply(
        lambda x: x if type(x) == float else x.split(' ')[0]
    ).apply(
        lambda x: re.findall('\d+', str(x))
    ).apply(
        lambda x: x if type(x) == float else ('.'.join([i for i in x]) if len(x) <= 2 else x[0])
    ).replace('', np.nan).apply(
        lambda x: float(x) if float(x) > 25 else float(x) * 9.8
    )
    # delete original feature
    dataframe.drop('torque', axis=1, inplace=True)

    return dataframe


def extract_numbers(data):
    """
    Function extracts numbers from mileage, max_power and engine

    :param data: pd.DataFrame extract numbers from
    :return: pd.DataFrame
    """
    for col in ['mileage', 'max_power', 'engine']:
        data[col] = data[col].apply(
            lambda x: '.'.join((re.findall('\d+', str(x))))
        ).replace('', np.nan).apply(
            lambda x: float(x)
        )
    data[['mileage', 'max_power', 'engine']] = data[['mileage', 'max_power', 'engine']].astype(float)

    return data


def preprocess_data(data, target, torque_treatment, nums_extractor, imputer, scaler, encoder, features):
    """
    Function preprocess data for predicting

    :param data: pd.DataFrame predict to
    :param target: str name of target
    :param torque_treatment: function
    :param nums_extractor: function
    :param imputer: sklearn.imputer
    :param scaler: sklearn.preprocessing.StandardScaler
    :param encoder: sklearn.preprocessing.OneHotEncoder
    :param features: list of features which are used for training
    :return: pd.DataFrame
    """
    data.drop('name', axis=1, inplace=True)
    # numbers extracting
    data = torque_treatment(data)
    data = nums_extractor(data)
    # filling nans
    nans_cols = data.columns[data.isna().sum() > 0]
    if len(nans_cols) > 0:
        data[nans_cols] = imputer.transform(data[nans_cols])
    # scaling and encoding
    num_cols = data.drop(target, axis=1).columns[data.drop(target, axis=1).dtypes != 'object']
    cat_cols = data.drop(target, axis=1).columns[data.drop(target, axis=1).dtypes == 'object']
    cat_data = data[cat_cols]
    num_data = data[num_cols]
    scaled_data = pd.DataFrame(scaler.transform(num_data), columns=num_data.columns)
    encoded_data = pd.DataFrame(encoder.transform(cat_data), columns=encoder.get_feature_names())
    # concat categorical and numerical data
    whole_data = pd.concat([encoded_data, scaled_data], axis=1)
    # keep only features which are used for training
    whole_data = whole_data[features]

    return whole_data

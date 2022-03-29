import pytest
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os
from pyspark.sql.functions import col, isnan, when, count
from ex1 import *

names_of_tables_and_pkey = {
    'film': [14],
    'content_rating': [10],
    'movie_person': [11, 12, 13],
    'actor': [13],
    'author': [12],
    'director': [11],
    'oscar_award': [14],
    'genre': [7],
    'IMDB ': [14],
    'rates': [14],
    'authored': [12, 14],
    'acted_in': [13, 14],
    'directed': [11, 14],
    'type_of': [7, 14]
}


@pytest.fixture(scope='session')
def spark_builder():
    """
    Returns:
        a spark builder for get the DataFrame from csv files

    """
    a = SparkSession.builder.appName('Dataframe').getOrCreate()
    return a


@pytest.fixture(scope='session')
def get_data_frames(spark_builder):
    """Organize all the csv files as data frames.

    Returns:
        A dictionary that map: table_name -> DataFrame. Where the df contain the data from the table_name.csv file.

    """
    process_file()
    data_frames = dict()
    for table_name in NAMES_TO_COLUMNS.keys():
        path_to_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{table_name}.csv")
        data_frames[table_name] = spark_builder.read.csv(path_to_csv, header=True, inferSchema=True)
    return data_frames


def test_schema(get_data_frames):
    """Checks whether the column names (schema) we wanted for all the tables appear in the csv files.

    Args:
        get_data_frames:  A dictionary that map: table_name -> DataFrame. Where the df contain the data from the table_name.csv file

    """
    for table_name in NAMES_TO_COLUMNS.keys():
        curr_df = get_data_frames[table_name]
        wanted_columns = [TITLES[i] for i in NAMES_TO_COLUMNS[table_name]]
        wanted_columns = wanted_columns if table_name != "movie_person" else ["&&".join(wanted_columns)]
        print(f"\nThe schema in table: {table_name}")
        curr_df.printSchema()
        assert list(curr_df.columns) == wanted_columns, f"wanted schema: {wanted_columns}, got {list(curr_df.colunms)}"


def test_duplicates(get_data_frames):
    """Check there is no duplicate in the all csv files.

    Args:
        get_data_frames:  A dictionary that map: table_name -> DataFrame. Where the df contain the data from the table_name.csv file

    """
    for table_name in NAMES_TO_COLUMNS.keys():
        curr_df = get_data_frames[table_name]
        duplicate_df = curr_df.groupBy(list(curr_df.columns)).count().filter("count != 1")
        assert duplicate_df.count() == 0, duplicate_df.show()

def test_unique_key(get_data_frames):
    """Checks in the all csv files whether the columns we wanted to be a primary key do not contain duplicates.
    i.e if in the table we have primary_key(col1, col2) the in the csv there will be no two rows (a,b,..) and (a,b...)

    Args:
        get_data_frames:  A dictionary that map: table_name -> DataFrame. Where the df contain the data from the table_name.csv file

    """
    for table_name in NAMES_TO_COLUMNS.keys():
        curr_df = get_data_frames[table_name]
        pkey = [TITLES[j] for j in names_of_tables_and_pkey[table_name]]
        pkey = pkey if table_name != "movie_person" else ["&&".join(pkey)]
        duplicate_df = curr_df.groupBy(pkey).count().filter("count != 1")
        assert duplicate_df.count() == 0, duplicate_df.show()


def test_nan_value(get_data_frames):
    """Checks that there are no missing values in the all tables.

    Args:
        get_data_frames:  A dictionary that map: table_name -> DataFrame. Where the df contain the data from the table_name.csv file

    """
    for table_name in NAMES_TO_COLUMNS.keys():
        curr_df = get_data_frames[table_name]
        nan_df = curr_df.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in curr_df.columns])
        row_list = nan_df.collect()[0] # the first and the only row.
        assert any([row_list[col_name] == 0 for col_name in curr_df.columns]), f"nan values in table {table_name}:\n {nan_df.show()}"

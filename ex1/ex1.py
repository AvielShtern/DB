import csv
from io import TextIOWrapper
from zipfile import ZipFile

"""
dictionary that maps from table name to relevant columns
"""
NAMES_TO_COLUMNS = {
    'film': [1, 3, 5, 6, 14],
    'content_rating': [10],
    'movie_person': [11, 12, 13],
    'actor': [13],
    'author': [12],
    'director': [11],
    'oscar_award': [2, 4, 14],
    'genre': [7],
    'IMDB': [8, 9, 14],
    'rates': [10, 14],
    'authored': [12, 14],
    'acted_in': [13, 14],
    'directed': [11, 14],
    'type_of': [7, 14]
}

TABLE_NAMES = ['film', 'content_rating', 'movie_person', 'actor', 'author',
               'director', 'oscar_award', 'genre', 'IMDB', 'rates', 'authored',
               'acted_in', 'directed', 'type_of']

SETS_FOR_NAMES = [set() for _ in range(len(TABLE_NAMES))]

"""
dictionary that maps table name -> set of relevant rows (for avoiding duplicates)
"""
NAMES_TO_SETS = dict(zip(TABLE_NAMES, SETS_FOR_NAMES))

"""
indices for columns with list values.
"""
LISTS_VALUES_INDICES = [7, 11, 12, 13]

outfiles = [open(f"{name}.csv", 'w', ) for name in TABLE_NAMES]
outwriters = [csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_NONE)
              for outfile in outfiles]

TITLES = ['', 'Film', 'Oscar Year', 'Film Studio/Producer(s)', 'Award',
          'Year of Release', 'Movie Time', 'Movie Genre',
          'IMDB Rating', 'IMDB Votes', 'Content Rating', 'Directors',
          'Authors', 'Actors', 'Film ID']


# process_file goes over all rows in original csv file, and sends each row to process_row()
# DO NOT CHANGE!!!
def process_file():
    with ZipFile('archive.zip') as zf:
        with zf.open('oscars_df.csv', 'r') as infile:
            reader = csv.reader(TextIOWrapper(infile, 'utf-8'))
            for row in reader:
                # remove some of the columns
                chosen_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16,
                                  29]
                row = [row[index] for index in chosen_indices]
                # change "," into && in list values
                lists_values_indices = [7, 11, 12, 13]
                for list_value_index in lists_values_indices:
                    row[list_value_index] = row[list_value_index].replace(',',
                                                                          '&&')

                # pre-process : remove all quotation marks from input and turns NA into null value ''.
                row = [v.replace(',', '') for v in row]
                row = [v.replace("'", '') for v in row]
                row = [v.replace('"', '') for v in row]
                row = [v if v != 'NA' else "" for v in row]

                # In the first years of oscars in the database they used "/" for example 1927/28, so we will change these.
                row[2] = row[2].split("/")[0]

                # In 1962 two movies were written as winners, then we change one of them to nominee.
                if row[4] == "Winner" and row[2] == "1962" and row[
                    14] == "8d5317bd-df12-4f24-b34d-e5047ef4665e":
                    row[4] = "Nominee"

                # In 2020 Nomadland won and marked as nominee by mistake.
                if row[2] == "2020" and row[1] == "Nomadland":
                    row[4] = "Winner"

                process_row(row)

    # writes all sets of values for rows and closes files
    write_to_files()


# return a list of all the inner values in the given list_value.
# you should use this to handle value in the original table which
# contains an inner list of values.
# DO NOT CHANGE!!!
def split_list_value(list_value):
    return list_value.split("&&")


# process_row should splits row into the different csv table sets
def process_row(row):
    for table_name in TABLE_NAMES:
        curr_rows_to_add = [[]]
        for col_index in NAMES_TO_COLUMNS[table_name]:
            if col_index not in LISTS_VALUES_INDICES:
                if not row[col_index] and table_name != "movie_person":
                    curr_rows_to_add = [[]]
                    break
                curr_rows_to_add = [row_to_add + [row[col_index]] for
                                    row_to_add in curr_rows_to_add]
            else:
                list_of_values = split_list_value(row[col_index])
                if (not list_of_values or not list_of_values[
                    0]) and table_name != "movie_person":
                    curr_rows_to_add = [[]]
                    break
                curr_rows_to_add = [row + [val] for row in curr_rows_to_add for
                                    val in list_of_values]

        curr_rows_for_set = [tuple(curr_row) for curr_row in curr_rows_to_add
                             if curr_row] if table_name != "movie_person" \
            else [(name,) for curr_row in curr_rows_to_add for name in
                  curr_row if name]
        NAMES_TO_SETS[table_name] = NAMES_TO_SETS[table_name].union(
            set(curr_rows_for_set))


def write_to_files():
    """
    write all sets to relevant files including title handling
    """
    for i, table_name in enumerate(TABLE_NAMES):
        titles = tuple([TITLES[j] for j in NAMES_TO_COLUMNS[table_name]])
        titles_to_subtruct = {titles} if table_name != "movie_person" else {
            (title,) for title in titles}
        NAMES_TO_SETS[table_name] = NAMES_TO_SETS[
                                        table_name] - titles_to_subtruct
        titles = titles if table_name != "movie_person" else ("movie_person",)
        rows_to_write = NAMES_TO_SETS[table_name]
        outwriters[i].writerow(titles)
        outwriters[i].writerows(rows_to_write)
        outfiles[i].close()


# return the list of all tables
# CHANGE!!!
def get_names():
    return TABLE_NAMES


if __name__ == '__main__':
    process_file()
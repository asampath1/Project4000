# Import Open-Tamil
import sys
sys.path.append("[path to open tamil goes here]")

# Import statements
import tamil
import csv
import pandas as pd
from transliterate import azhagi, jaffna, combinational, UOM, ISO, itrans, algorithm
from unidecode import unidecode

# Get data from csv and ISO from Open Tamil package
ISO_table = ISO.ReverseTransliteration.table

# Read input file
csv_data = pd.read_csv('/Users/asampathkuma/Downloads/4K Pasuram/திருப்பாவை.csv')

# Helper function to save to an output file
def save_to_csv(data: list) -> None:
    """ Takes a two dimensional list as input,
    with each nested list being a column of data,
    and saves it to an output.csv file
    """
            
    # Zip lists into format suitable for csv
    zipped_list = zip(*data)

    # Open csv file for writing
    with open('outputwords.csv', "w") as f: 
        writer = csv.writer(f)
        
        # Add each row to the csv file
        for row in zipped_list:
            writer.writerow(row)

# Helper function to check for unknown column names
def filter_column_list(column_list: list) -> list:
    """ Takes a list of arguments and returns
    a list containing only the arguments which
    are column titles in the csv file
    """
    
    # Create list to store valid column names
    found_titles = []
    
    # Loop through arguments
    for title in column_list:
        if title in csv_data:
            # If column name is in the file, keep it
            found_titles.append(title)
        else:
            # If column name is not in the file, skip it and alert user
            print("[Argument '" + title + "' was not found in csv file. Make sure your arguments are titles of the columns.]")
            
    return found_titles
# Helper function to get transliterated columns
def transliterate_index(col_name: str) -> list:
    """ Given a column title of the csv file,
    gets the data from both the ISO transliteration
    and original Tamil column and returns it as
    a nested array
    """
    
    # Create lists to store transliterated data, with the title being the 
    # first entry for the csv file
    eng_list = [col_name + "_iso_15919"]
    tamil_list = [col_name]

    # Loop through column
    for index, row in csv_data.iterrows():
        
        # Get cell data
        tamil_str = row[col_name]

        # Check if content exists
        if tamil_str != tamil_str:
            # If cell is empty, add empty strings
            eng_list.append("")
            tamil_list.append("")
        else:
            # If cell has data, transliterate string and add to list
            eng_str = algorithm.Direct.transliterate(ISO_table, tamil_str)
            cleaned_word = unidecode(eng_str)
            eng_list.append(cleaned_word)
            tamil_list.append(tamil_str)
                
    return [eng_list, tamil_list]
# Main function to be called on
def transliterate_csv(column_list: list) -> None:
    """ Given a list of column titles, saves the
    Tamil and ISO transliterated data of each column
    to a csv file
    """

    # Check for unknown arguments
    titles = filter_column_list(column_list)
    
    # Create list to be saved to csv format
    output_csv_list = []
    
    # Loop over all the columns in csv file
    for index, col in csv_data.items():
        
        # Check if title of column matches argument
        if index in titles:                
            # Transliterate row and add both tamil and english to output list
            data = transliterate_index(index)
            output_csv_list.append(data[0])
            output_csv_list.append(data[1])
    
    # Save the data as a csv file
    save_to_csv(output_csv_list)

    # Script is ran here!
# Example list from example.csv
titles = ['Padham']
transliterate_csv(titles)
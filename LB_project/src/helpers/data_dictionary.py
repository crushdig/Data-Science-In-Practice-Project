from os import path
import pandas as pd
from datetime import datetime

def save(dataset,                                      # The source dataset.      
         summary,                                      # User defined summary str.
         include='all',                                # Summarise all cols in df.
         reader='read_csv',                            # How to read df.
         float_format = lambda x: "{:.2f}".format(x),  # A formatter for floats.
         *args, **kwargs):
    
    """ Create and save a data dictionary from a dataset file.

        #Generate a column based summary description from the dataset using Pandas describe
        function and related methods. Numeric and categorical fields are handled by Pandas.
        Missing data counts are added separately. The resulting data description is written
        to a file, named after the source dataset, with the addition of .txt and saved in
        the same directory as the source.
        
        Args:
        dataset: pathname to dataset file.
        summary: user provided summary text to add to data dictionary.
        reader:  a reader for the dataset filetype (default: read_pickle).
        float_format: a floating point formatter for floats.
    """
    
    # The dataset basename.
    dataset_basename = path.basename(dataset)
    
    # Generate a name for the resulting data dictionary file.
    dd_filename = dataset + '.txt'

    # Read the dataset using the reader and any args provided.
    df = getattr(pd, reader)(dataset, *args, **kwargs)
    
    # Generate the data dictionary as a dataframe.
    dd = df.describe(include=include).T
    
    # Add cols to count missing values.
    missing = df.isnull().sum()
    dd['Missing'] = missing
    dd['%Missing'] = 100*missing/len(df)
    
    # Save dictionary and summary info.
    with open(dd_filename, 'w') as f:
        
        # Write the header info.
        f.write('Data dictionary for {} @ {}\n'.format(
            dataset_basename, str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))
        f.write('Dataset shape, {} rows x {} columns.\n\n'.format(df.shape[0], df.shape[1]))

        f.write(summary+'\n\n\n')    # Write the summary.
        f.write('Data Dictionary\n---------------\n')
        
        f.write(dd.to_string(na_rep='-', float_format=float_format))  # Write the dataframe description.
    
    return dd
    
__author__ = 'Daniel Dittenhafer'
__version__ = '0.1'
__date__ = '2015-03-23'

import pandas as pd
import gviz_data_table as gv
import numpy

def ToGvizDataTable(dataframe):

    table = gv.Table()
    dt = dataframe.dtypes

    for col in dataframe.columns.values:
        gvdt = dt[col]
        if dt[col] == object:
            # Skip
            gvdt = str
        elif dt[col] == "float64":
            gvdt = float

        if gvdt != None:
            table.add_column(col, gvdt)

    for row in dataframe.iterrows():
        vals = row[1].values
        newVals = []
        for v in vals:
            nv = v
            if not (type(v) is str) and numpy.isnan(v):
               nv = None
            newVals.append(nv)

        table.append(newVals)

    return table

def main():
    """Our cheap unit test main function."""
    data = pd.read_table("C:\Code\R\IS608-VizAnalytics\FinalProject\Data\Natality, 2007-2013-StateCounty.txt")

    dataStateSum = data.groupby(["State", "Year"])["Births"].sum().reset_index()
    print(dataStateSum.head())


    # Call our helper function
    dt = ToGvizDataTable(dataStateSum)

    # Convert to the JSON encoding
    dtJson = dt.encode()

    # Save to a file
    with open("Output.json", "w") as text_file:
        text_file.write(dtJson)

# This is the main of the program.
if __name__ == "__main__":
    main()

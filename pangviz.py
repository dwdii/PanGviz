__author__ = 'Daniel Dittenhafer'
__version__ = '0.1'
__date__ = '2015-03-23'

import pandas as pd
import gviz_data_table as gv
import numpy
from datetime import datetime

def ToGvizDataTable(dataframe):

    table = gv.Table()
    dt = dataframe.dtypes

    # Loop to add the columns from the dataframe to the gviz datatable
    for col in dataframe.columns.values:
        gvdt = dt[col]
        if dt[col] == object:
            # Skip
            gvdt = str
        elif dt[col] == "float64":
            gvdt = float
        elif dt[col] == "datetime64[ns]":
            gvdt = datetime
        elif dt[col] == "int64":
            gvdt = int

        # If a datatype was specified, then add the column
        if gvdt != None:
            table.add_column(col, gvdt)

    for row in dataframe.iterrows():
        vals = row[1].values
        newVals = []
        for v in vals:
            nv = v
            if (type(v) is float) and numpy.isnan(v):
               nv = None
            elif type(v) is long:
                nv = int(v)
            elif type(v) is pd.tslib.Timestamp:
                nv = datetime(v.year, v.month, v.day)
            newVals.append(nv)

        table.append(newVals)

    return table

def parseDateYearMonth(year, month):
    """
    Helper method for converting individual year and month columns into a first of the month date.
    :param year:
    :param month:
    :return: the first of the month, year datetime object
    """
    if type(year) is str:
        year = int(year)

    if type(month) is str:
        month = int(month)

    if numpy.isnan(year) or numpy.isnan(month):
        dt = None
    else:
        dt = datetime(year, month, 1)
    return dt

def main():
    """Our cheap unit test main function."""
    #dataFile = "C:\Code\R\IS608-VizAnalytics\FinalProject\Data\Natality, 2007-2013-StateCounty.txt"
    #dataFile = "C:\Code\R\IS608-VizAnalytics\FinalProject\Data\LA-Natality-Combined.csv"
    dataFile = "C:\Code\R\IS608-VizAnalytics\FinalProject\Data\LA-Natality-Census-Combined.csv"
    data = pd.read_table(dataFile, sep=",",
                         parse_dates={'Date': ["Year.Code", "Month.Code"]}, date_parser=parseDateYearMonth)
    data["Date"] = pd.to_datetime(data["Date"])

    dataStateSum = data.groupby(["State", "Date", "UnemploymentRate", "BirthsPer1000Pop"])["Births"].sum().reset_index()
    #dataStates
    print(dataStateSum.head())

    # Call our helper function
    dt = ToGvizDataTable(dataStateSum)

    # Convert to the JSON encoding
    dtJson = dt.encode()

    # Save to a file
    with open("C:\Code\R\IS608-VizAnalytics\FinalProject\Data\PanGvizOutput.json", "w") as text_file:
        text_file.write(dtJson)

# This is the main of the program.
if __name__ == "__main__":
    main()

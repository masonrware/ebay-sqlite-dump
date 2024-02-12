"""
FILE: ebay_data_parser.py
------------------
Author: Mason R. Ware (mrware@wisc.edu)
Modified: 02/12/2024
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"
nullIndicator = "NULL"

items = list()
bids = list()
users = list()

# Dictionary of months used for date transformation
MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


def isJson(f):
    """
    Returns true if a file ends in .json
    """
    return len(f) > 5 and f[-5:] == ".json"


def transformMonth(mon):
    """
    Converts month to a number, e.g. 'Dec' to '12'
    """
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


def transformDttm(dttm):
    """
    Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
    """
    dttm = dttm.strip().split(" ")
    dt = dttm[0].split("-")
    date = "20" + dt[2] + "-"
    date += transformMonth(dt[0]) + "-" + dt[1]
    return date + " " + dttm[1]


def transformDollar(money):
    """
    Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
    """
    if money == None or len(money) == 0:
        return money
    return sub(r"[^\d.]", "", money)


def parseJson(json_file):
    """
    Parses a single json file. Currently, there's a loop that iterates over each
    item in the data set. Your job is to extend this functionality to create all
    of the necessary SQL tables for your database.
    """
    with open(json_file, "r") as f:
        temp_items = loads(f.read())[
            "Items"
        ]  # creates a Python dictionary of Items for the supplied json file
        for item in temp_items:
            # create entry in items array
            items.append([item["ItemID"],
                          item["Name"],
                          item["Category"],
                          item["Currently"],
                          item["Category"],
                          transformDollar(item["Buy_Price"]) if item["Buy_Price"] else nullIndicator],
                          transformDollar(item["First_Bid"]),
                          item["Number_of_Bids"],
                          transformDttm(item["Started"]),
                          transformDttm(item["Ends"]),
                          
                          )
    

def main(argv):
    """
    Loops through each json files provided on the command line and passes each file
    to the parser
    """
    if len(argv) < 2:
        print(
            "Usage: python ebay_data_parser.py <path to json files>",
            file=sys.stderr,
        )
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)


if __name__ == "__main__":
    main(sys.argv)

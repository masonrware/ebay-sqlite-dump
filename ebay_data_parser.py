"""
FILE: ebay_data_parser.py
------------------
Author: Mason R. Ware (mrware@wisc.edu)
Modified: 02/12/2024
"""

import sys
import time
from json import loads
from re import sub

COLUMN_SEPARATOR = "|"
NULL_INDICATOR = "\'NULL\'"

items = list()
bids = list()
users = list()
categories = list()

registered_usernames = list()
registered_categories = list()

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
            items.append(
                [
                    item["ItemID"],
                    "\"{body}\"".format(body=item["Name"].replace('"', '""')),
                    transformDollar(item["Currently"]),
                    (
                        transformDollar(item["Buy_Price"])
                        if "Buy_Price" in item
                        else NULL_INDICATOR
                    ),
                    transformDollar(item["First_Bid"]),
                    item["Number_of_Bids"],
                    "\"{body}\"".format(body=transformDttm(item["Started"].replace('"', '""'))),
                    "\"{body}\"".format(body=transformDttm(item["Ends"].replace('"', '""'))),
                    "\"{body}\"".format(body=item["Seller"]["UserID"].replace('"', '""')),
                    "\"{body}\"".format(body=str(item["Description"]).replace('"', '""')),
                ]
            )

            # create bids entry
            if item["Bids"]:
                for bid in item["Bids"]:
                    bids.append(
                        [
                            item["ItemID"],
                            "\"{body}\"".format(body=bid["Bid"]["Bidder"]["UserID"].replace('"', '""')),
                            "\"{body}\"".format(body=transformDttm(bid["Bid"]["Time"].replace('"', '""'))),
                            transformDollar(bid["Bid"]["Amount"]),
                        ]
                    )

            # create a user entry
            if item["Seller"]["UserID"] not in registered_usernames:
                registered_usernames.append(item["Seller"]["UserID"])
                
                users.append(
                    [
                        "\"{body}\"".format(body=item["Seller"]["UserID"].replace('"', '""')),
                        "\"{body}\"".format(body=item["Location"].replace('"', '""')),
                        "\"{body}\"".format(body=item["Country"].replace('"', '""')),
                        item["Seller"]["Rating"],
                    ]
                )
                
            # create user entries for each bidder -- we do not care about redundancy at this step
            if item["Bids"]:
                for bid in item["Bids"]:
                    if item["Seller"]["UserID"] not in registered_usernames:
                        registered_usernames.append(item["Seller"]["UserID"])
                        
                        users.append(
                            [
                                "\"{body}\"".format(body=bid["Bid"]["Bidder"]["UserID"].replace('"', '""')),
                                (
                                    "\"{body}\"".format(body=bid["Bid"]["Bidder"]["Location"].replace('"', '""'))
                                    if "Location" in bid["Bid"]["Bidder"]
                                    else NULL_INDICATOR
                                ),
                                (
                                    "\"{body}\"".format(body=bid["Bid"]["Bidder"]["Country"].replace('"', '""'))
                                    if "Country" in bid["Bid"]["Bidder"]
                                    else NULL_INDICATOR
                                ),
                                bid["Bid"]["Bidder"]["Rating"],
                            ]
                        )

            # TODO implement duplicate checking for categories
            # create category entries
            for category in item["Category"]: 
                if "{a}{b}".format(a=item["ItemID"], b=category) not in registered_categories:
                    registered_categories.append("{a}{b}".format(a=item["ItemID"], b=category))
                    
                    categories.append([
                        item["ItemID"],
                        "\"{body}\"".format(body=category.replace('"', '""'))
                    ])
        
        count = 0

        # write items.dat
        with open("./items.dat", "w") as file:
            for item in items:
                for ele in item:
                    if count != len(item) - 1:
                        file.write(f"{ele}{COLUMN_SEPARATOR}")
                        count += 1
                    else:
                        file.write(f"{ele}\n")
                        count = 0

        # write users.dat
        with open("./users.dat", "w") as file:
            for user in users:
                for ele in user:
                    if count != len(user) - 1:
                        file.write(f"{ele}{COLUMN_SEPARATOR}")
                        count += 1
                    else:
                        file.write(f"{ele}\n")
                        count = 0

        # write bids.dat
        with open("./bids.dat", "w") as file:
            for bid in bids:
                for ele in bid:
                    if count != len(bid) - 1:
                        file.write(f"{ele}{COLUMN_SEPARATOR}")
                        count += 1
                    else:
                        file.write(f"{ele}\n")
                        count = 0
                        
        # write categories.dat
        with open("./categories.dat", "w") as file:
            for category in categories:
                for ele in category:
                    if count != len(category) - 1:
                        file.write(f"{ele}{COLUMN_SEPARATOR}")
                        count += 1
                    else:
                        file.write(f"{ele}\n")
                        count = 0


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
    total_start_time = time.time()
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            start_time = time.time()
            parseJson(f)
            end_time = time.time()

            running_time = end_time - start_time

            print(f"Parsed File: \t\t{f}\nExecution Time: \t{running_time}s\n")

    total_end_time = time.time()
    total_running_time = total_end_time - total_start_time

    print(
        f"=================================================\nSuccessfully Finished Parsing!\nExecution Time: \t{total_running_time}s\n"
    )


if __name__ == "__main__":
    main(sys.argv)


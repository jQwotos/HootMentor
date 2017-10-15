import re
from random import randint

import webserver2
import csv

FILE = "data/automation_new.csv"
del_pat = r'[$\s,]'

def clean(text):
    return text.strip(',')


def reg_clean(text):
    return re.sub(del_pat, '', text)


def main():
    with open(FILE) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        first = True
        for row in readCSV:
            print(row)
            if first:
                first = False
            else:
                webserver2.db.session.add(
                    webserver2.Position(
                        id = randint(1, 99999),
                        noc_code = int(row[0]),
                        group = clean(row[1]),
                        occupation = clean(row[2]),
                        automation_risk = float(row[6].strip('%')),
                        average_income = int(reg_clean(str(row[4]))),
                        level_of_education = row[-1],
                    )
                )

                webserver2.db.session.commit()

if __name__ == "__main__":
    main()

import noc2

FILE = "data/automation.csv"
OUTPUT = "data/automation_new.csv"
data = noc2.scrape()

inputData = []

def match(noc_code):
    for item in data:
        if item['noc_code'].text == noc_code:
            return item['level']

with open(FILE) as i:
    for line in i:
        inputData.append(
            line.strip('\n').split(',')
        )
        inputData[-1].append(
            match(inputData[-1][0])
        )

with open(OUTPUT, "w+") as out:
    for item in inputData:
        out.write(",".join(item) + "\n")

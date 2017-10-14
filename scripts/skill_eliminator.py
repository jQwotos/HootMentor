import pandas

positions_updated = "data/positions_updated.csv"


def _load_rel_skills():
    with open(positions_updated) as f:
        return f.readline().strip('\n').split(',')[4:]

def _load_data():
    # Converts data from
    skills = _load_rel_skills()
    positions = []
    index = []
    stuff = [[] for x in skills]
    with open(positions_updated) as f:
        f.readline()
        for l in f:
            split = l.strip('\n').split(',')
            positions.append({
                'title': split[2],
                'skills': split[4:],
            })
            index.append(split[2])
            for s in range(len(split[4:])):
                stuff[s].append(split[4:][s])

    return [
        pandas.DataFrame({
            skills[x]: pandas.Series(
                stuff[x],
                index=index,
            )
        }) for x in range(len(skills))
    ]

def eliminate(has_skills, rel_skills):
    output = []
    for x in rel_skills:
        print('Trying to find %s' % x)
        if x in has_skills:
            output.append(0)
        else:
            output.append(1)
    return output

'''
def eliminate(has_skills, rel_skills):
    output = []
    for s in rel_skills:
        val = None
        for k, v in has_skills.items():
            if s == rel_skills['s'] and v != 0:
                val = v
                break
        if val is not None:
            output.append(v)
        else:
            output.append(0)

    return output
'''

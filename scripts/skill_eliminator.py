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


def eliminate(has_skills, *rel_skills):
    output = []
    if rel_skills is None:
        rel_skills = global_rel_skills

    for skill in has_skills:
        if skill in rel_skills:
            output.append(skill)

    return output

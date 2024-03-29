import os
import logging

DATA_FILE = 'data/positions2.csv'
POSITIONS_FILE = 'data/positions_updated.csv'
JOBS_FILE = "data/matching_jobs.csv"


def soundex(word):
    replacements = ['a', 'e', 'i', 'o', 'u', 'y', 'h', 'w']
    vals = {
        '1': ['b', 'f', 'p', 'v'],
        '2': ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z'],
        '3': ['d', 't'],
        '4': ['l'],
        '5': ['m', 'n'],
        '6': ['r'],
    }
    cache = word[1:]
    output = word[0]
    for x in cache:
        if len(output) > 4:
            break
        if x not in replacements:
            for k, v in vals.items():
                if x in v:
                    print("Comparing %s and %s" % (output[-1], k,))
                    if output[-1] != k:
                        output += (k)
    return output[:4]


def custom_reqs(reqs):
    with open(DATA_FILE) as f:
        logging.info('Stage 1')
        jobs = []
        for j in rows:
            split = j.split(',')
            jobs.append({
                'title': split[0:3],
                'reqs': split[4:],
            })

def databasify():
    with open(JOBS_FILE) as f:
        matching_jobs = [
            l.strip('\n') for l in f
        ]

    with open(DATA_FILE) as f:
        rows = [l.strip('\n') for l in f]
        jobs = []

        logging.info('Stage 1')
        for j in rows:
            split = j.split(',')
            print(split[0:4])
            if (split[2]) in matching_jobs:
                jobs.append({
                    'title': split[0:4],
                    'reqs': split[4:],
                })
        logging.info('Stage 2')
        reqs = []
        for j in jobs:
            for r in j['reqs']:
                if r not in reqs:
                    reqs.append(r)

    with open(DATA_FILE) as f:
        rows = [l.strip('\n') for l in f]
        positions = []
        for r in rows:
            split = r.split(',')
            skills = split[4:]
            updatedSkills = []

            for req in reqs:
                if req in skills:
                    updatedSkills.append(1)
                else:
                    updatedSkills.append(0)
            positions.append({
                'noc_code': split[0],
                'link': split[1],
                'title': split[2],
                'proficiency': split[3],
                'skills': updatedSkills,
            })
    return {
        'positions': positions,
        'skills': reqs,
    }


def simplify():
    '''
    with open(JOBS_FILE) as f:
        badChars = [' ', '\n']
        matching_jobs = [
            soundex(
            l.translate(
            maketrans("", "",),
            badChars)) for l in f
        ]
    '''
    with open(JOBS_FILE) as f:
        matching_jobs = [
            l.strip('\n') for l in f
        ]

    with open(DATA_FILE) as f:
        rows = [l.strip('\n') for l in f]
        jobs = []

        logging.info('Stage 1')
        for j in rows:
            split = j.split(',')
            print(split[0:4])
            if (split[2]) in matching_jobs:
                jobs.append({
                    'title': split[0:4],
                    'reqs': split[4:],
                })
        logging.info('Stage 2')
        reqs = []
        for j in jobs:
            for r in j['reqs']:
                if r not in reqs:
                    reqs.append(r)

        logging.info('Stage 3')
        for j in range(len(jobs)):
            tba = []
            for r in reqs:
                if r not in reqs:
                    reqs.append(r)

        logging.info('Stage 4')
        for j in range(len(jobs)):
            tba = []
            for r in reqs:
                if r not in jobs[j]['reqs']:
                    tba.append('0')
                else:
                    tba.append('1')
            jobs[j]['updated_reqs'] = tba

        logging.info('Stage 5')
        with open(POSITIONS_FILE, 'w+') as p:
            row = 'noc_code,link,title,rank,%s\n' % (
                ','.join(reqs)
            )
            p.write(row)

            for j in jobs:
                row = '%s,%s\n' % (
                    ','.join(j['title']),
                    ','.join(j['updated_reqs']),
                )
                p.write(row)

def main():
    with open(DATA_FILE) as f:
        rows = [l.strip('\n') for l in f]
        jobs = []

        logging.info('Stage 1')
        for j in rows:
            split = j.split(',')
            jobs.append({
                'title': split[0:3],
                'reqs': split[4:],
            })

        # Get all possible requirements
        logging.info('Stage 2')
        reqs = []
        for j in jobs:
            for r in j['reqs']:
                if r not in reqs:
                    reqs.append(r)

        logging.info('Stage 3')
        for j in range(len(jobs)):
            tba = []
            for r in reqs:
                if r not in jobs[j]['reqs']:
                    tba.append('0')
                else:
                    tba.append('1')
            jobs[j]['updated_reqs'] = tba


        logging.info('Stage 4')
        with open(POSITIONS_FILE, 'w+') as p:
            row = '%s,%s,%s,%s\n' % (
                'noc_code', 'link', 'title',
                ','.join(reqs)
            )
            p.write(row)

            for j in jobs:
                row = '%s,%s\n' % (
                    ','.join(j['title']),
                    ','.join(j['updated_reqs']),
                )
                p.write(row)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG
    )
    # main()
    simplify()

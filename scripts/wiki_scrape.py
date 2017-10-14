import requests

from bs4 import BeautifulSoup

OUT_FILE = '../data/disciplines.csv'

def main():
    data = BeautifulSoup(
        requests.get(
            'https://en.wikipedia.org/wiki/Outline_of_academic_disciplines'
        ).content,
        'html.parser',
    )
    divs = data.find_all('div', {'class': 'div-col columns column-count column-count-2'})
    results = []
    for d in divs:
        results += d.findAll('a')

    return [x.text for x in results]

if __name__ == "__main__":
    #results = main()
    print(main())
    '''
    with open(OUT_FILE, 'w+') as f:
        for r in results:
            f.write('%s\n' % (r,))
    '''

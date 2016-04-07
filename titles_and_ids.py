import csv


def main():

    with open('u.item') as f:
        reader = csv.reader(f, delimiter='|')
        with open('README.md', a) as w:
        for row in f:
            w.write(row[0] + ": " + row[1])



if __name__ == '__main__':
    main()

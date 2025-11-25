import csv
import argparse


def open_file(filename, n=4):
    content = []
    with open(filename, encoding='utf-8') as f:
        r = csv.DictReader(f)
        for i, row in enumerate(r):
            content.append(row)
            if i == n - 1:
                break

    return content

def parse_args():
    p = argparse.ArgumentParser(description="Print first [n]=4 lines from[filename]")

    p.add_argument('filename', help='CSV file')
    p.add_argument('-n', '--lines', type=int, help='number of lines to print')

    return p

def main():
    parser = parse_args()
    args = parser.parse_args() 

    print(open_file(args.filename, args.lines))


if __name__ == '__main__':
    main()
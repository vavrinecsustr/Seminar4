import csv


def read_csv(input_path):
    content = []
    with open (input_path, encoding='utf-8') as f:
            r = csv.DictReader(f)
            for i, row in enumerate(r):
                content.append(row)
                if i == 4:
                    break

    return content

def write_csv(rows, output_path):
    fieldnames = list(rows[0].keys())
    print(fieldnames)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args():
    p = argparse.ArgumentParser(description="Add description")

    p.add_argument('input_file', help='input file')
    p.add_argument('output_file', help='output file')

    return p

def main():
    parser = parse_args()
    args = parser.parse_args() 

    sample = read_csv(args.input_file)
    write_csv(sample, args.output_file)

if __name__ == '__main__':
    main()
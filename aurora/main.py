import csv
import argparse
from dataclasses import dataclass
from typing import Optional, List, Iterable, Dict, Any


@dataclass
class FilterCriteria:
    country: Optional[List[str]] = None
    status: Optional[List[str]] = None





class DataRepository:
    def __init__(self, path):
        self.path = path

    def read_all(self) -> Iterable[Dict[str, Any]]:
        with open (self.path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

class DataProcessor:
    def __init__(self, repo):
        self.repo = repo

        def filter_rows(self, criteria: FilterCriteria) -> List[Dict[str, Any]]:
            result = []
            for row in self.repo.read_all():
                if criteria.match(row):
                    result.append(row)
            return result

    def write_csv(self, rows: List[Dict[str, Any]], output_path):
        if not rows:
            print('Warning: No rows on output.')
            return
        fieldnames = list(rows[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

class AuroraApp:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.criteria = FilterCriteria
        
        self.repo = DataRepository(args.input)
        self.processor = Dataprocessor(self.repo)


        
    def run(self):
        print("Loading and filtering data ...")
        rows = self.processor.filter_rows(self.criteria)



def parse_args():
    p = argparse.ArgumentParser(description="Add description")

    p.add_argument('--input', required=True, help='Path to input CSV file')
    p.add_argument('--output', required=True, help='Path to output CSV file')

    p.add_argument('--country', help="Comma separated list of countries, e.g. CZ,DE")
    p.add_argument('--risk-level', help="Comma sšeparated list of risk levels, e.g. HIGH,CRITICAL")
    p.add_argument('--status', help="Comma separated list of statuses")
    p.add_argument('--triage', help="Comma separated list of triage priorities, e.g. P1,P2")

    p.add_argument('--from-date', help="Start date YYYY-MM-DD")
    p.add_argument('--to-date', help="End date YYYY-MM-DD")

    p.add_argument('--min-threat', type=int, help="Minimum overall threat score")
    p.add_argument('--max-threat', type=int, help="Maximum overall threat score")
    p.add_argument('--min-money', type=int, help="Minimum money-moved-usd")

    p.add_argument('--channel-darknet', action='store-true', help="Ohly include events with channel_darknet=Y")

    p.add_argument('--sort-by', help="Comma separated list of columns to sort by")
    p.add_argument('--sort-desc', action='store-true', help="Sort in descending order")

    p.add_argument('--summary-only', action='store-true', help ="Do not write CSV, only print summary")

    return p


def main():
    parser = parse_args()
    args = parser.parse_args() 
    app = AuroraApp(args)
    app.run()

if __name__ == '__main__':
    main()
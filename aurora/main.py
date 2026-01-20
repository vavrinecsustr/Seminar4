#usr/bin/env python3

import csv
import argparse
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Iterable, Dict, Any


DATE_FMT = '%Y-%m-%d'
TS_FMT = '%Y-%m-%d %H:%M:%S'

@dataclass
class FilterCriteria:
    country: Optional[List[str]] = None
    status: Optional[List[str]] = None
    risk_level: Optional[List[str]] = None
    triage: Optional[List[str]] = None
    from_date: Optional[List[str]] = None
    to_date: Optional[List[str]] = None
    min_threat: Optional[List[str]] = None
    max_threat: Optional[List[str]] = None
    min_money: Optional[List[str]] = None
    channel_darknet_only: bool = False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "FilterCriteria":
        def split_opt(val: Optional[str]) -> Optional[List[str]]:
            if val is None:
                return None
            return [x.strip().upper() for x in val.split(',') if x.strip()]
        
        def parse_date(val: Optional[str]) -> Optional[datetime]:
            if not val:
                return None
            return datetime.striptime(val, DATE_FMT)

        return cls(
            country = split_opt(args.country),
            status = split_opt(args.status),
            risk_level = split_opt(args.risk_level),
            triage = split_opt(args.triage),
            from_date = split_opt(args.from_date),
            to_date = split_opt(args.to_date),
            min_threat = split_opt(args.min_threat),
            max_threat = split_opt(args.max_threat),
            min_money = split_opt(args.min_money),
            channel_darknet_only = split_opt(args.channel_darknet)
        )

    def match(self,row:Dict[str, str]) -> bool:
        if self.country and row.get("country", "").upper not in self.country:
            return False
        if self.status and row.get ("status", "").upper not in self.status:
            return False
        if self.risk_level and row.get ("target_risk_level", "").upper not in self.risk_level:
            return False
        if self.triage and row.get ("triage", "").upper not in self.triage:
            return False
        if self.from_date or self.to_date:
            ts_str = row.get("timestamp_utc")
            if not ts_str:
                return false
            ts = datetime.striptime(ts_str, TS_FMT)
            if self.from_date and ts.date() < self.from_date.date():
                return False
            if self.to_date and ts.date() > self.to_date.date():
                return False
        if self.min_threat is not None:
            val = int(row.get("threat_score_overall", "0"))
            if val < self.min_threat:
                return False

        if self.max_threat is not None:
            val = int(row.get("threat_score_overall", "0"))
            if val > self.max_threat:
                return False

        if self.min_money is not None:
            val = int(row.get("money_moved_usd", "0"))
            if val < self.min_money:
                return False

        if self.channel_darknet_only:
            if row.get("channel_darknet", "N") != "Y":
                return False


        return True

@dataclass
class SortSpec:
    columns: List[str]
    descending: bool = False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> Optinal["SortSpec"]:
        if not args.sort_by:
            return None
        cols = [c.strip() for c in args.sort_by.split(",") if c.strip()]
        return cls(columns=cols, descendig=args.sort_desc)

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
    
    def sort_rows(self, rows, spec):
        if not spec:
            return rows

        def sort_key(row: Dict[str, Any]):
            values = []
            for col in spec.columns:
                val = row.get(col)
                try:
                    values.append(float(val))
                except (TypeError, ValueError):
                    values.append(val)
            return tuple(values)

        return sorted(rows, key=sort_key, reverse=spec.descending)

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

    def sumarize(self, rows: List[Dict[str, Any]]):
        total = len(rows)
        print(f'Total rows: {total}')
        if total == 0:
            return



        by_risk = {}
        for r in rows:
            rl = r.get('target_risk_level', 'UNKNOWN')
            by_risk[rl] = by_risk.get(rl, 0) + 1
        print('By risk level:')
        #vratit srovnany risk_level
        #print(f' {rl}: {count}') 

        #prumerne threat skore
        vals = [int(r.get('threat_score_overall', "0")) for r in rows]
        avg_threat = sum(vals) / len(vals)
        print(f'Average threat_score_overall: {avg_threat:.2f}')

class AuroraApp:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.criteria = FilterCriteria.frpm_args(args)
        self.sort_spec = SortSpec.from_args(args)
        self.repo = DataRepository(args.input)
        self.processor = DataProcessor(self.repo)


        
    def run(self):
        print("Loading and filtering data...")
        rows = self.processor.filter_rows(self.criteria)
        print(f"Filtered rows: {len(rows)}")

        if self.sort_spec:
            print(f"Sorting by: {self.sort_spec.columns}, "
                  f"descending={self.sort_spec.descending}")
            rows = self.processor.sort_rows(rows, self.sort_spec)

        if not self.args.summary_only:
            print(f"Writing output to {self.args.output}")
            self.processor.write_csv(rows, self.args.output)

        print("Summary:")
        self.processor.sumarize(rows)

        

def parse_args():
    p = argparse.ArgumentParser(description="Add description")

    p.add_argument('--input', required=True, help='Path to input CSV file')
    p.add_argument('--output', required=True, help='Path to output CSV file')

    p.add_argument('--country', help="Comma separated list of countries, e.g. CZ,DE")
    p.add_argument('--risk-level', help="Comma separated list of risk levels, e.g. HIGH,CRITICAL")
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
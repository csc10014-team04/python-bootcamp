import csv
from pathlib import Path

def main():
    path=Path(__file__).parent/"sample.csv"
    with path.open("r",encoding="utf-8",newline="") as file:
        tasks=list(csv.DictReader(file))
    for task in tasks:
        print(task)

if __name__=="__main__":
    main()
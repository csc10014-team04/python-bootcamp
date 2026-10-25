
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"w2"))

from io_utils import load_tasks


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--hours",type=float,required=True)
    parser.add_argument("--today",type=date.fromisoformat,default=date.today())
    args=parser.parse_args()

    try:
        tasks=load_tasks(args.file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}",file=sys.stderr)
        return 1
    except (ValueError,OSError) as error:
        print(f"Error: {error}",file=sys.stderr)
        return 1

    if args.hours<0:
        print("Error: --hours must be non-negative",file=sys.stderr)
        return 1

    selected=[]
    remaining=args.hours

    for task in sorted(tasks,key=lambda task:(task.deadline,task.title)):
        if task.deadline<args.today:
            continue
        if task.effort_h<=remaining:
            selected.append(task)
            remaining-=task.effort_h

    print(f"Tonight ({args.hours:.1f} h):")
    if not selected:
        print("No tasks fit the available time.")
    else:
        for index,task in enumerate(selected,start=1):
            print(f"{index}. {task.title} ...... {task.effort_h:.1f} h")

    return 0

if __name__=="__main__":
    sys.exit(main())

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--num", type=int, default=42, help="Enter an integer")

args = parser.parse_args()
result = args.num * 2
print(result)

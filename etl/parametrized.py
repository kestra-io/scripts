import argparse

parser = argparse.ArgumentParser()

parser.add_argument("num", type=int, help="Enter an integer")

# Read arguments from command line
args = parser.parse_args()

result = args.num * 2
print(result)

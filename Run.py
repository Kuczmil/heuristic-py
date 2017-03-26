from core import Start
import sys

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Not enough arguments are given. Please run script with paths to file with network and input settings")
    else:
        start = Start
        start.start(sys.argv[1], sys.argv[2])
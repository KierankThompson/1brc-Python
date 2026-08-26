from dataclasses import dataclass
import cProfile
import sys
import csv

@dataclass
class FileStatistics():
    count: int
    sum: float
    maxNum: float
    minNum: float


def main(fileName: str = "measurements.txt"):
    fileStats: FileStatistics = FileStatistics(0, 0.0, 0.0, float('inf'))
    with open(fileName, "r") as f:
        csvReader = csv.reader(f, delimiter=';')
        for line in csvReader:
            cleanedNum: float = float(line[1])

            fileStats.count += 1
            fileStats.sum += cleanedNum
            fileStats.maxNum = max(fileStats.maxNum, cleanedNum)
            fileStats.minNum = min(fileStats.minNum, cleanedNum)
    print(f"Mean: {fileStats.count/fileStats.sum}, Max: {fileStats.maxNum}, Min: {fileStats.minNum}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fileName: str = sys.argv[1]
        cProfile.run('main(fileName)', sort='cumtime')
    else:
        cProfile.run('main()', sort='cumtime')

    
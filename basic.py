from dataclasses import dataclass
import math
import sys
import time

@dataclass(slots=True)
class StationStatistics():
    count: int
    sum: int
    maxNum: float
    minNum: float


def main(fileName: str = "measurements.txt") -> None:
    stationMap: dict[str, StationStatistics] =  {}
    
    with open(fileName, "r", encoding="utf-8") as f:
        for line in f:
            splitLine: list[str] = line.split(";")
            stationName: str = splitLine[0]
            cleanedNum: float = float(splitLine[1])

            if stationName not in stationMap:
                stationStats: StationStatistics = StationStatistics(1, int(cleanedNum*10), cleanedNum, cleanedNum)
                stationMap[stationName] = stationStats
            else:
                stationStats = stationMap[stationName]
                stationStats.count += 1
                stationStats.sum += int(cleanedNum * 10)
                stationStats.maxNum = max(stationStats.maxNum, cleanedNum)
                stationStats.minNum = min(stationStats.minNum, cleanedNum)

    stationNames: list[str] = sorted(stationMap.keys())
    totalStations: int = len(stationNames)

    print("{", end="")
    for i, station in enumerate(stationNames):
        stationStats = stationMap[station]

        endChar: str = ", " if i < totalStations - 1 else "}"

        regAverage: float = math.floor((stationStats.sum / stationStats.count) + 0.5) / 10

        print(f"{station}={round(stationStats.minNum,1)}/{regAverage}/{round(stationStats.maxNum, 1)}", end = endChar)



if __name__ == "__main__":
    startTime = time.perf_counter()
    if len(sys.argv) > 1:
        fileName: str = sys.argv[1]
        main(fileName)
    else:
        main()
    endTime = time.perf_counter()
    if sys.stdout.isatty():
        print(f"\nTook {endTime - startTime} seconds")

    
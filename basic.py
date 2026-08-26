from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import sys


@dataclass
class StationStatistics():
    count: int
    sum: float
    maxNum: float
    minNum: float


def main(fileName: str = "measurements.txt"):
    stationMap: dict[str, StationStatistics] =  {}
    
    with open(fileName, "r", encoding="utf-8") as f:
        for line in f:
            splitLine: list[str] = line.strip().split(";")
            stationName: str = splitLine[0]
            cleanedNum: float = float(splitLine[1])

            if stationName not in stationMap:
                stationStats: StationStatistics = StationStatistics(1, cleanedNum, cleanedNum, cleanedNum)
                stationMap[stationName] = stationStats
            else:
                stationStats = stationMap[stationName]
                stationStats.count += 1
                stationStats.sum += cleanedNum
                stationStats.maxNum = max(stationStats.maxNum, cleanedNum)
                stationStats.minNum = min(stationStats.minNum, cleanedNum)

    stationNames: list[str] = sorted(stationMap.keys())
    totalStations: int = len(stationNames)

    print("{", end="")
    for i, station in enumerate(stationNames):
        stationStats = stationMap[station]

        endChar: str = ", " if i < totalStations - 1 else "}"

        decSum: Decimal = Decimal(str(stationStats.sum))
        decCount: Decimal = Decimal(str(stationStats.count))
        decAverage: Decimal = decSum / decCount
        decAverageRounded: Decimal = decAverage.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

        print(f"{station}={round(stationStats.minNum,1)}/{decAverage}/{round(stationStats.maxNum, 1)}", end = endChar)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fileName: str = sys.argv[1]
        main(fileName)
    else:
        main()

    
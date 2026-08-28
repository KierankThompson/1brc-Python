from dataclasses import dataclass
import math
import sys
import mmap
import time

@dataclass
class StationStatistics():
    count: int
    sum: int
    maxNum: int
    minNum: int



def main(fileName: str = "measurements.txt"):
    stationMap: dict[bytes, StationStatistics] =  {}
    
    with open(fileName, "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
            currentPos: int = 0
            fileSize: int = m.size()

            while currentPos != -1:
                semiPos: int = m.find(b';', currentPos)

                if semiPos == -1:
                    break

                stationName: bytes = m[currentPos:semiPos]
                newlinePos: int = m.find(b'\n', semiPos)

                if newlinePos == -1:
                    newlinePos = fileSize

                byteNum: bytes = m[semiPos+1:newlinePos]

                sign: int = 1
                startIdx: int = 0
            
                if byteNum[0] == 45: #Check if first byte is "-"
                    sign = -1
                    startIdx = 1
            
                #b'0' is 48
                if len(byteNum) - startIdx == 4:
                    cleanedNum: int = sign * ((byteNum[startIdx] - 48) * 100 + (byteNum[startIdx + 1] - 48) * 10 + (byteNum[startIdx + 3] - 48))
                else:
                    cleanedNum = sign * ((byteNum[startIdx] - 48) * 10 + (byteNum[startIdx + 2] - 48))
                    
                try:
                    stationStats: StationStatistics = stationMap[stationName]
                    stationStats.count += 1
                    stationStats.sum += cleanedNum

                    if cleanedNum > stationStats.maxNum:
                        stationStats.maxNum = cleanedNum
                    elif cleanedNum < stationStats.minNum:
                        stationStats.minNum = cleanedNum

                except KeyError:
                    stationMap[stationName] = StationStatistics(1, cleanedNum, cleanedNum, cleanedNum)
                    
                currentPos = newlinePos + 1


    stationNames: list[bytes] = sorted(stationMap.keys())
    totalStations: int = len(stationNames)

    print("{", end="")
    for i, stationNameBytes in enumerate(stationNames):
        stationStats = stationMap[stationNameBytes]
        stationNameStr: str = stationNameBytes.decode("utf-8")
        endChar: str = ", " if i < totalStations - 1 else "}"
        
        regAverage: float = math.floor((stationStats.sum / stationStats.count) + 0.5) / 10

        print(f"{stationNameStr}={stationStats.minNum / 10}/{regAverage}/{stationStats.maxNum / 10}", end = endChar)


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

    
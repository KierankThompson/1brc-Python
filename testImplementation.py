import time
import sys
import subprocess
from pathlib import Path
import argparse
from typing import Sequence, Optional, Any

def getTestCases() -> tuple[list[str], list[str]]:
    testCaseDir: Path = Path("testCases")

    
    inputFileNames: list[str] = [file.name for file in testCaseDir.glob("*.txt") if file.is_file()]
    outputFileNames: list[str] = [file.name for file in testCaseDir.glob("*.out") if file.is_file()]

    expectedOutputs: list[str] = []

    try:
        for outputName in outputFileNames:
            with open(f"testCases/{outputName}", "r", encoding="utf-8") as f:
                expectedOutputs.append(f.read().replace("\n", ""))
    except Exception as e:
        print((f"Failed at {outputName}"))
        raise e

    return inputFileNames, expectedOutputs

def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("fileName", help="File name for implementation to test")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args: argparse.Namespace = parser.parse_args(argv)

    inputFileNames, expectedOutputs = getTestCases()

    testCaseResults: list[tuple[str, float] | tuple[bool]] = []
    codeFile: str = args.fileName

    for testCase, expectedOutput in zip(inputFileNames, expectedOutputs):
        testCaseStart: float = time.time()

        if args.verbose:
            print(f"Testing {testCase}")

        cmd = [sys.executable, '-u', codeFile, f"testCases/{testCase}"]
        try:
            runProcess: subprocess.CompletedProcess[str] = subprocess.run(cmd, 
                                                                          text=True, capture_output=True, timeout=120, 
                                                                          encoding="utf-8",
                                                                          errors="replace")

            testCaseEnd: float = time.time()
            elapsedTime: float = round(testCaseEnd - testCaseStart, 4)
            testCaseOutput: str = runProcess.stdout

            testCaseResults.append((testCaseOutput, elapsedTime))

            if args.verbose:
                print(f"Took {elapsedTime} seconds")
                if len(expectedOutput) > 500:
                    print(f"Testcase too long to output, {"got right" if expectedOutput == testCaseOutput else "got wrong"}")
                else:
                    print(f"Expected {expectedOutput}\nGot {testCaseOutput}")
            
        except Exception as e:
            print(e)
            testCaseResults.append((False,))

        if args.verbose:
            print("-" * 20)

    for idx, result in enumerate(testCaseResults):
        if len(result) == 1:
            print(f"{inputFileNames[idx]}: Failed")
        elif expectedOutputs[idx] != result[0]:
            print(f"{inputFileNames[idx]}: Took {result[1]} and failed")
        else:
            print(f"{inputFileNames[idx]}: Took {result[1]} and passed")





if __name__ == "__main__":
    main()
    

    









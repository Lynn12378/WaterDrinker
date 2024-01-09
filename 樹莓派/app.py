from speak import record_and_transcribe
from pump import outflow
from lcd import show
import re

if __name__ == "__main__":
    com=record_and_transcribe()
    print(com)
    if ( '給我' in com):
        match = re.search(r'\d+', com)
        if match:
            num = match.group()
            ml = int(num)
            print("提取的數字:", ml)

            show(ml)
            outflow(ml/5)
        else:
            print("請再試一次")


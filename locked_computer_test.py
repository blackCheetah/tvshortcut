import time
from datetime import datetime

for i in range(0, 1000):
    now = datetime.now()

    print( '{}'.format(i), '\t', '{}'.format(now), flush=True)

    time.sleep(5)
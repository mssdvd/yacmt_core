#!/usr/bin/env python3.6
import json
import random
import time


def main():
    start_time = time.time()
    while True:
        with open("/tmp/yacmt.json", "w") as f:
            run_time = int(time.time() - start_time)
            data_demo = {
                "eng_rpm": random.randint(1200, 1600),
                "speed": random.randint(60, 70),
                "eng_load": random.randint(40, 70),
                "eng_cool_temp": random.randint(80, 85),
                "control_mod_voltage": random.randint(12, 13),
                "run_time": run_time
            }
            f.write(json.dumps(data_demo))
        time.sleep(1)


if __name__ == "__main__":
    main()

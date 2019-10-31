import sys
import os
import logging
import subprocess
from time import sleep
from typing import List

apk_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "../../dataset/Twitter_v7.93.4-release.04_apkpure.com.apk")
device = "emulator-5554"
package_name = "invalid.package.name"
output_folder = "."


def execute_shell_cmd(*args) -> str:
    # https://stackoverflow.com/a/4760517
    result = subprocess.run(args, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return result.stdout.decode('utf-8')


def clear_logcat():
    execute_shell_cmd("adb -s", device, "logcat -c")


def run_with_monkey(seed: str, events: str, run_number: int) -> str:
    monkey_trace = os.path.join(output_folder, "monkey_dump"+str(run_number)+".txt")
    execute_shell_cmd("adb -s", device, "shell monkey -p", package_name, "-c android.intent.category.LAUNCHER 1 >",
                      monkey_trace)
    sleep(5)
    execute_shell_cmd("adb -s", device, "shell monkey -p", package_name, "-v --pct-appswitch 0 -s", str(seed),
                      "--throttle 5000", str(events))
    sleep(60)
    return monkey_trace


def pull_slicing_traces_from_logcat(run_number: int) -> None:
    slicing_trace = os.path.join(output_folder, "slicing_trace"+str(run_number)+".txt")
    execute_shell_cmd("adb -s", device, "logcat >", slicing_trace)
    return slicing_trace


def diff(trace1: List[str], trace2: List[str]) -> float:
    raise NotImplementedError


if __name__ == "__main__":
    try:
        apk_name = sys.argv[1]
    except IndexError:
        logging.warning("No argument provided, using the default app: " + apk_name)
    try:
        device = sys.argv[2]
    except IndexError:
        logging.warning("No argument provided, using the default device: " + device)
    try:
        output_folder = sys.argv[3]
    except IndexError:
        logging.warning("No argument provided, using the default output_folder: " + output_folder)
    
    package_name = execute_shell_cmd("aapt dump badging "+ apk_name + " | grep package | awk '{print $2}' | sed s/name=//g | sed s/\\'//g")

    # Check if device is active

    # first run
    clear_logcat()
    monkey_trace1 = run_with_monkey(0, 1000, 1)
    slice_trace1 = pull_slicing_traces_from_logcat()

    # second run
    clear_logcat()
    monkey_trace2 = run_with_monkey(0, 1000, 2)
    slice_trace2 = pull_slicing_traces_from_logcat()

    # diff the traces
    difference = diff(slice_trace1, slice_trace2)
    if difference:
        logging.warning("The traces are different by " + str(difference))


import sys
import serial
import time
import argparse
import subprocess
import serial.tools.list_ports
import datetime
import tkinter as tk
from tkinter import filedialog
SEP = "#"*100

NRFUTIL_MAP = {"linux": "nrfutil-linux", "linux2": "nrfutil-linux", "darwin": "nrfutil-mac", "win32": ".\\nrfutil.exe"}

def read_from_ble(ble_ser):
    ble_ser_bytes = ble_ser.readline()
    input = ble_ser_bytes.decode("utf-8", "ignore").strip()
    if input:
        print(input)
    return input

class Command:
    def __init__(self, cmd, expected, delay=0):
        self.cmd = cmd
        self.cmd_exec = b'\r\n!'+bytes(cmd, encoding='utf-8')+b'\r\n'
        self.expected = expected
        self.delay = delay
    def exec_cmd(self, ble_ser):
        print("==>> !{}".format(self.cmd))
        ble_ser.write(self.cmd_exec)
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).seconds < 2:
            if self.expected in read_from_ble(ble_ser):
                print("success!\n{}".format(SEP))
                return 0
        print("failure!\n{}".format(SEP))
        return 1

GW_COMMANDS = [
    Command(cmd="version", expected="WILIOT_GW_BLE_CHIP_SW_VER"),
    Command(cmd="move_to_bootloader", expected='')
]

def run_cmd(cmd):
    print("Running: " + cmd)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    if p.returncode:
        print(f"\nFailed running : {cmd}\n")
        sys.exit(-1)
    else:
        print(f"\nSuccess running : {cmd}\n")

def main():

    ports = serial.tools.list_ports.comports()
    print(SEP + "\nAvailable ports:")
    for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
    print(SEP + "\n")

    parser = argparse.ArgumentParser(description='Used to load gw image')
    parser.add_argument('--p', type=str, help='COM for the ble - meaning loading gw zip file from UART')
    args = parser.parse_args()


    if args.p:
        ble_ser = serial.Serial(port=args.p, baudrate=921600, timeout=0.1)
        ble_ser.flushInput()

        failures = 0
        
        for cmd in GW_COMMANDS:
            failures += cmd.exec_cmd(ble_ser)
            time.sleep(cmd.delay)
        if failures == 0:
            ble_ser.close()
            time.sleep(2)
            print("Please pick a file! (<X.Y.Z>_app.zip)")
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            print(file_path)
            cmd = f'{NRFUTIL_MAP[sys.platform]} dfu serial --package "{file_path}" -p {args.p} -fc 0 -b 115200 -t 10'
            run_cmd(cmd)
        else:
            print("ERROR: failed to run UART commands!")


if __name__ == "__main__":
    main()
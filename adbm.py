# Reference: https://github.com/mfinkle/web-adb/blob/master/server.py

import os
from re import sub
import sys
import subprocess
import os
import re
import json
from sys import stderr
from typing import Dict
import urllib
import ssl
from argparse import ArgumentParser
from flask import jsonify, make_response
from flask.wrappers import Response
from PIL import Image


class ADB_Modules:

    def __init__(self) -> None:
        self.VERIFY_ADB = "adb --version"
        self.SHOW_ADB_DEVICES = "adb devices"
        self.SHOW_BATTERY_INFO = "adb shell dumpsys battery"
        self.GET_SCREENSHOT = "time adb shell screencap"
        self.path = os.path

    def get_device_info(self):
        device = []
        """
        Retrives the device relevant information at the start of the script
        """
        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.build.id'"]).strip().decode()
        self.deviceId = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.vendor.model'"]).strip().decode()
        self.deviceModel = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.vendor.name'"]).strip().decode()
        self.deviceName = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.vendor.device'"]).strip().decode()
        self.device = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.board'"]).strip().decode()
        self.board = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.cpu.abilist'"]).strip().decode()
        self.supportedABIs = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.cpu.abilist32'"]).strip().decode()
        self.supported32BitABI = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "getprop", "| grep 'ro.product.cpu.abilist64'"]).strip().decode()
        self.supported64BitABI = output_string.split(":")[1]

        output_string = subprocess.check_output(
            ["adb", "shell", "dumpsys", "SurfaceFlinger | grep GLES"]).strip().decode()
        self.gpuInfo = output_string.split(":")[1]

        device.append({
            "id": self.deviceId,
            "device_model": self.deviceModel,
            "device_name": self.deviceName,
            "device": self.device,
            "board": self.board,
            "supported_abi": self.supportedABIs,
            "supported_32_bit_ABI": self.supported32BitABI,
            "supported_64_bit_ABI": self.supported64BitABI,
            "gpu_info": self.gpuInfo,
        })
        return make_response(jsonify(device), 200)

    def verifyAdb(self) -> Response:
        try:
            subprocess.call(self.VERIFY_ADB.split())
        except:
            return make_response(jsonify(True), 404)
        return make_response(jsonify(True), 200)

    # Show list of devices connected through adb
    def showDevices(self) -> Response:
        p = subprocess.Popen(self.SHOW_ADB_DEVICES.split(),
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return make_response(jsonify([p.returncode, stdout.decode(), stderr]), 200)

    # Get Battery Stats
    def getBatteryStats(self) -> Dict:
        p = subprocess.Popen(self.SHOW_BATTERY_INFO.split(),
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        errorcode = p.returncode
        if errorcode != 0:
            print(stderr)
        battery = {
            'level': 0,
            'status': 0,
            'health': 0,
        }
        stats = stdout.decode().split("\n", 1)[1]
        for line in stats.split("\n"):
            tokens = line.split(': ')
            if len(tokens) < 2:
                continue
            key = tokens[0].strip().lower()
            value = tokens[1].strip().lower()
            if key == 'level':
                battery['level'] = value
            elif key == 'status':
                battery['status'] = value
            elif key == 'health':
                battery['health'] = value
        return battery

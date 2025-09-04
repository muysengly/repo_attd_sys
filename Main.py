#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


os.environ["QT_SCALE_FACTOR"] = "1"  # Set scaling factor
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # Enable automatic scaling
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"  # Set screen scaling

os.chdir("./resource/view/main_attendance_form/")

os.system("python Controller.py")

#!/usr/bin/env python3


def mount_googledrive():
  from google.colab import drive
  drive.mount('/content/drive')


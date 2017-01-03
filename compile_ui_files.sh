#!/bin/bash

pyuic5 -x src/ui/Downloader.ui -o src/ui/Downloader.py
pyuic5 -x src/ui/MainWindow.ui -o src/ui/MainWindow.py
pyuic5 -x src/ui/AddFileDialog.ui -o src/ui/AddFileDialog.py

# pyuic5 -x src/ui/MainWindow_test.ui -o src/ui/MainWindow_test.py

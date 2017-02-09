#!/bin/bash

function compile {
	pyuic5 -x app/ui/$1.ui -o app/ui/$1.py
}

compile MainWindow
compile Downloader
compile AddFileDialog
compile SettingsDialog

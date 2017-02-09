"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

APP = ['main.py']
APP_NAME = "Bad Player"
APP_VERSION = "0.0.2"
DATA_FILES = [
    ('', ['config.yml',]),
    ('app/images/player/', ['app/images/player/animation.gif',
                            'app/images/player/play.png',
                            'app/images/player/pause.png',
                            'app/images/player/stop.png']),
]
OPTIONS = {
            'argv_emulation': True,
            'iconfile': 'app/images/badicon.icns',
            'includes': ['sip','PyQt5']
            }

setup(
	name=APP_NAME,
    app=APP,
    version=APP_VERSION,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'PyQt5', 'sqlalchemy', 'pyyaml', 'eyed3', 'youtube_dl'],
    # packages=['sqlalchemy', 'pyyaml', 'eyed3', 'youtube_dl'],
    # ressources=[includedir( "macbinaries/vlc_plugins" )],
    author = "Sebastien Treille",
    author_email = "c2ViYXN0aWVudHJlaWxsZUBnbWFpbC5jb20=",
    description = ("A bad player that play good playlists !"),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)

# BadPlayer

Not that bad, this player can play and add to a playlist some music from different sources like youtube, soundcloud, dailymotion, vimeo, facebook ...


###Instructions
```
git clone git@github.com:SebastienTr/BadPlayer.git
cd BadPlayer/
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

###Run
`./main.py`

###Create .app
```
python3 setup.py py2app --packages=PyQt5,sqlalchemy
./dist/Bad\ Player.app/Contents/MacOS/Bad\ Player
```

###Create .dmg
This is the best way i've found for the moment.

```
npm install -g appdmg
appdmg spec.json "Bad Player.dmg"
```
---------------------

There is a lot of things to improve but the basis is done.

###Contact
c2ViYXN0aWVudHJlaWxsZUBnbWFpbC5jb20=
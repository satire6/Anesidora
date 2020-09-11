cd toonsrv
call STOPALL.BAT
call UNINSTALLALL.BAT
copy ..\toon.dc .
copy ..\*.dna .
copy ..\NameMaster* .
call INSTALLALL.BAT
call STARTALL.BAT
cd ..
set PATH=lib
set PYTHONPATH=.;lib-tk
set TTMODELS=.
set DMODELS=.
python.exe AIStart.py

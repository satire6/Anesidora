set PATH=lib
set PYTHONPATH=.;lib-tk
set TTMODELS=.
set DMODELS=.
set CFG_PATH=.
set CONFIG_CONFIG=:configpath=CFG_PATH

python otp\switchboard\sbdebug.py -n dummy -p 1 -e
python otp\switchboard\sbdebug.py -n pirates -p 2 -e
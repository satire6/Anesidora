set PATH=lib
set PYTHONPATH=.;lib-tk
set TTMODELS=.
set DMODELS=.
set CFG_PATH=.
set CONFIG_CONFIG=:configpath=CFG_PATH

python -O -tt -c "import Pyro.naming,sys; Pyro.naming.main(sys.argv[1:])" %*

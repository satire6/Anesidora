------  SWITCHBOARD HOW-TO  ------



- Installation Overview -
1. Install Python - http://www.python.org/download/
2. Install Pyro - http://pyro.sourceforge.net/
3. Install Switchboard - Put the source files in this directory someplace convenient!



- Usage Overview -
1. Start the Pyro Nameserver
2. Start Switchboard node/wedge pairs
3. Issue commands
4. Shutdown/cleanup



- Step-by-Step Usage Example -


Setup: Start the Pyro Nameserver

> ns

(Pyro should have installed this in python/lib/site-packages/Pyro/bin or to a bin directory in your path)


Setup: Start two node/wedge pairs

> python startNode.py -n pirates
> python startWedge.py -n pirates
> python startNode.py -n toontown
> python startWedge.py -n toontown


Command: Enter two players

> python sbdebug.py -n pirates -p 1234 -e
> python sbdebug.py -n toontown -p 5678 -e


Command: Send a whisper from 1234 to 5678

> python sbdebug.py -n pirates -p 1234 -w 5678 -m "Hey, what's up?"


Command: Exit players

> python sbdebug.py -n pirates -p 1234 -x
> python sbdebug.py -n toontown -p 5678 -x


Command: Cleanly shut down nodes and wedges

> python sbdebug.py -n pirates -s
> python sbdebug.py -n toontown -s


Cleanup: Shut down the name server (clears all entries)

> nsc shutdown

(Another Pyro binary, same location as ns)


Cleanup: Clear the name server without shutting down

> nsc deletegroup :sb


Debugging: List the contents of the name server

> nsc listall



import time
import os
import sys

# Initialize ihooks importer On the production servers, we run genPyCode -n
# meaning no squeeze, so nobody else does this. When we squeeze, the
# unpacker does this for us and it does not hurt to do in either case.
import ihooks
ihooks.install()

print "Initializing..."
    
from otp.ai.AIBaseGlobal import *
import UtilityAIRepository

simbase.mdip = simbase.config.GetString("msg-director-ip", "localhost")
simbase.mdport = simbase.config.GetInt("msg-director-port", 6665)
simbase.esip = simbase.config.GetString("event-server-ip", "localhost")
simbase.esport = simbase.config.GetInt("event-server-port", 4343)

districtType = 0
ssId = simbase.config.GetInt("utility-ssid", 20100000)
utilityChannel = simbase.config.GetInt("utility-channel", 399900000)

if simbase.config.GetBool("want-dev", 0):
    # In development, the dcfiles are specified in prc files
    dcFileNames = None
else:
    # In production we have to list them out
    dcFileNames = ['otp.dc', 'toon.dc']

simbase.air = UtilityAIRepository.UtilityAIRepository(simbase.mdip,
                                                      simbase.mdport,
                                                      simbase.esip,
                                                      simbase.esport,
                                                      dcFileNames,
                                                      1,
                                                      "Utility",
                                                      districtType,
                                                      ssId,
                                                      utilityChannel,
                                                      utilityChannel + 1)

# How we let the world know we are not running a service
simbase.aiService = 0

from otp.otpbase.OTPLocalizer import SpeedChatStaticText, CustomSCStrings

# this script prints all static speedchat strings

msgs = set()

msgs.update(SpeedChatStaticText.values())
msgs.update(CustomSCStrings.values())

print '=== START SC STRINGS ==='

for msg in msgs:
    if len(msg):
        print msg
    

import string, os.path, sys

filelist_raw = "/cygwin/" + sys.argv[2] + "/src/publish/filelist"
f = open(filelist_raw)
filelist = []

lines = f.readlines()
for line in lines:
    # Ignore comment lines and blank lines (newline
    # is considered a char, hence the "< 2")
    if line[0] == "#" or len(line) < 2:
        continue
    else:
        words = string.split(line)
        # lines beginning in "file" have the filename in the 3rd column
        if words[0] == "file":
            filelist.append(words[2])
        # lines beginning in "squeeze" have the filename in the 2nd column
        elif words[0] == "squeeze":
            filelist.append(words[1])

f.close()
filelist.sort()

cvs_output_file = "/cygwin" + sys.argv[1] + "/cvsout.txt"
f = open(cvs_output_file)
cvslist = []

lines = f.readlines()
for line in lines:
    words = string.split(line)
    # Ignore and __init.py files and files with "AI" or "UD" in them
    hasAI = "AI" in words[3]
    hasUD = "UD" in words[3]
    hasIN = "__init__.py" in words[3]
    if hasIN or hasAI or hasUD:
        continue
    else:
        word = "" + words[3]
        word = word.replace("/cvsroot/panda3d/direct","$DIRECT")
        word = word.replace("/cvs/otp","$OTP")
        word = word.replace("/cvs/toontown","$TOONTOWN")
        cvslist.append(word[:-2])

f.close()
cvslist.sort()


for file in cvslist:
    if file in filelist:
        continue
    else:
        print file
        

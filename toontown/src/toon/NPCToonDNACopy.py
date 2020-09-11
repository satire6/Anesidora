import os, sys

npcDNA = {}

def parseAndCopyDNA():
    loadDNA()
    
    if not os.path.isfile("/cygwin/home/abhinath/player/toontown/src/toon/NPCToons.py"):
        print "NPCToons.py not found"
    else:
        npcToonsFile = open("/cygwin/home/abhinath/player/toontown/src/toon/NPCToons.py", "r+")
        npcToons = npcToonsFile.read()
        #npcToons.replace("\n", "\n ")
        npcCount = 0
        while npcCount < len(npcDNA):
            npcId = npcDNA.keys()[npcCount]
            lineStart = npcToons.find(npcId+" :")
            lineEnd = npcToons.find("\n", lineStart)
            randPos = npcToons.find(" \"r\"", lineStart, lineEnd)
            
            oldLine = npcToons[lineStart:lineEnd]
            newLine = oldLine.replace(" \"r\"", npcDNA[npcId])
            
            npcToons = npcToons.replace(oldLine, newLine)
        
            npcCount += 1
            
        # print npcToons
        npcToonsFile.seek(0,0)
        npcToonsFile.write(npcToons)           
    
def loadDNA():
    if not os.path.isfile("/cygwin/home/abhinath/player/toontown/src/toon/RTDNAFile.txt"):
        print "RTDNAFile.txt not found"
        return 1
    else:
        npcDNAFile = open("/cygwin/home/abhinath/player/toontown/src/toon/RTDNAFile.txt", "r")
        while 1:
            NPCLine = npcDNAFile.readline()
            if NPCLine == "":
                break
            if NPCLine.find("NPC Id: ")>-1:
                break
                
        while NPCLine != "":
            DNALine = npcDNAFile.readline()
            if (NPCLine.find("NPC Id: ")>-1):
                NPCLine = NPCLine.replace("NPC Id: ", "")
                NPCLine = NPCLine.replace("\n", "")
            if(DNALine.find("DNA: ")>-1):
                DNALine = DNALine.replace("DNA: ", "")
                DNALine = DNALine.replace("\n", "")
                npcDNA[NPCLine] = DNALine
                
            while 1:
                NPCLine = npcDNAFile.readline()
                if NPCLine == "":
                    break
                if NPCLine.find("NPC Id: ")>-1:
                    break
                
        # print npcDNA
        return 0
        
        
parseAndCopyDNA()
        
import time
import os
from os import error
target="./"
allDirs=os.listdir(target)
for dir in allDirs:
    filesOfDir=target+dir
    try:
        for txt in os.listdir(filesOfDir):
            #print(txt)
            if txt[-4:]!=".jpg":
                print(txt)
                os.rename(target+dir+"/"+txt,target+dir+"/"+txt+".txt")
    except:
        pass
time.sleep(5)
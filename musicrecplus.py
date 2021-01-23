"""
Burak Yesil & Frank Orlando
We pledge our honor that we have abided by the Stevens Honor System
November 20, 2020
"""

from cs115 import *
prefName = "musicrecplus_ex2_b.txt"

def loadUsers(fileName):
    "Creates and prints a dictionary of artists liked by specific users from text file, fileName"
    open(fileName,"a")
    file = open(fileName, "r")
    userDict = {}
    for line in file:
        [username,artists] = line.strip().split(":")
        artistList = artists.split(",")
        artistList.sort()
        userDict[username] = artistList
    file.close()
    return userDict

def getUserInfo(userDict):
    "Takes a dictionary of users and their preferences"
    "If user not yet created, asks for preferences and add to dictionary"
    "If user already exists, prints menu"
    nameInput = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private):\n")
    nameInput=nameInput.title()
    if not(nameInput in userDict):
        enterPreferences(nameInput,userDict)
    while True:
        optionLetter = input("""Enter a letter to choose an option:\ne - Enter preferences\nr - Get recommendations\np - Show most popular artists\nh - How popular is the most popular\nm - Which user has the most likes\nq - Save and quit\n""")
        if(optionLetter=="e"):
            enterPreferences(nameInput,userDict)
        elif(optionLetter=="r"):
            getRecommendations(nameInput,userDict)
        elif(optionLetter=="p"):
            popularArtists(userDict,False)
        elif(optionLetter=="h"):
            amountPopularity(userDict)
        elif(optionLetter=="m"):
            mostUserLikes(userDict)
        elif(optionLetter=="q"):
            addUserToFile(prefName,userDict)
            break
    return userDict

def enterPreferences(userName,userDict):
    "Takes string userName and dictionary userDict"
    "Adds new prefrences to userName and changes userDict"
    prefList = []
    while True:
        artistInput = input("Enter an artist that you like (Enter to finish):\n")
        if not artistInput:
            break
        prefList += [artistInput]
    prefList = map(lambda x: x.title(),prefList)
    prefList.sort()
    userDict[userName]=prefList

def getRecommendations(userName,userDict):
    "Returns recommendations for user, userName"
    curBest=["",0]
    for key in userDict:
        if not(key[-1]=="$"):
            val = similar(userDict[userName],userDict[key],0)
            if (val>curBest[1] and not(userDict[key]==userDict[userName])):
                curBest=[key,val]
    recList=[]
    if not(curBest[0]==""):
        for item in userDict[curBest[0]]:
            if not(item in userDict[userName]):
                recList+=[item]
    if not(recList==[]):
        for i in recList:
            print(i)
    else:
        print("No recommendations available at this time.")
            
def similar(uL1,uL2,simVal):
    "Returns amount of similar artists between two users preferences"
    if (uL1==[] or uL2==[]):
        return simVal
    elif uL1[0]==uL2[0]:
        return similar(uL1[1:],uL2[1:],simVal+1)
    elif uL1[0]<uL2[0]:
        return similar(uL1[1:],uL2,simVal)
    else:
        return similar(uL1,uL2[1:],simVal)

def popularArtists(userDict,amountPopBool):
    "Returns most popular artists"
    artistDict={}
    for key in userDict:
        if not(key[-1]=="$"):
            for item in userDict[key]:
                if item in artistDict:
                    artistDict[item]+=1
                else:
                    artistDict[item]=1
    popArtistLst=[["",0],["",0],["",0]]
    for artist in artistDict:
        artCur=artistDict[artist]
        for i in range(3):
            if artCur>popArtistLst[i][1]:
                popArtistLst[i]=[artist,artCur]
                break
    if amountPopBool:
        return popArtistLst[0][1]
    else:
        if popArtistLst[0][1]==0:
            print("Sorry, no artists found.")
        else:
            for i in range(3):
                print(popArtistLst[i][0])

def amountPopularity(userDict):
    "Returns how popular the most popular artists are"
    count=popularArtists(userDict,True)
    if count==0:
        print("Sorry, no artists found.")
    else:
        print(count)

def mostUserLikes(userDict):
    "Returns userName of user with most favortite artists"
    maxLikes = [0,""]
    for key in userDict:
        if not(key[-1]=="$"):
            if len(userDict[key])>maxLikes[0]:
                maxLikes = [len(userDict[key]),key]
    if maxLikes[0]==0:
        print("Sorry, no artists found.")
    else:
        print(maxLikes[1])

def sort(userDict):
    '''Sorts the keys of the inputed dictionary alphabetically and returns them in a list '''
    l = []
    for i in userDict:
        l += [i]
    l.sort()
    return l

def sortDictionary(userDict):
    '''Sorts userDict and returns a new dictionary with the elements of userDict sorted '''
    L = sort(userDict)
    temp = {}
    for i in L:
        temp[i] = userDict[i]
    return temp

def addUserToFile(fileName,userDict):
    "Add user information into the desired text file"
    newDict = sortDictionary(userDict)
    temp = open(fileName,"w")
    for key in newDict:
        S = str(key) + ":" + ",".join(newDict[key]) + "\n"
        temp.write(S)
    temp.close()

def main():
    userDict = loadUsers(prefName)
    getUserInfo(userDict)

if __name__=="__main__":
    main()

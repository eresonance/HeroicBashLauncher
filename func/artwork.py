#DISCLAIMER - The logic of the code on Line 18 has been taken from SteamGridDB (https://github.com/SteamGridDB/steamgriddb-manager) [MIT License].   


import os, binascii, json, wget, ssl, traceback, sys
import configpath
from gameName import rspchar

def checkartworkexists(artwork_path, image):
    
    check_flag = 0

    for i in os.listdir(artwork_path):
           
        if image == i:
            check_flag = 1
            break

    if check_flag == 1:

        return True
    else:

        return False


def addartwork(appname, exe, userid, simplified_gamename):
    

    #As Steam does not store AppIDs of Non-Steam games in any config file, this makes it difficult to add artwork without knowing the AppID.
    #One way is to add the game, let Steam assign the AppID and then try to find the AppID using regex.
    #Fortunately, SteamGridDB (MIT License) has found a simple and efficient solution to calculate the AppID. 
    
    #ALL CREDIT GOES TO THE STEAMGRIDDB DEVS FOR THIS IMPLEMENTATION (Line 18).
    #Here's how the it's explained in their source code - 
        #To create a grid image we must compute the Steam ID, which is just crc32(target + label) + "02000000", using IEEE standard polynomials.
    appid = binascii.crc32(str.encode(exe + appname)) | 0x80000000
    print("Steam AppID for " + appname + " is " + str(appid))

    #Path to Steam grid folder
    artwork_path = os.path.expanduser("~") + '/.steam/steam/userdata/' + str(userid) + '/config/grid'


    #Artwork types
    coverart =  str(appid) + 'p.jpg'
    backgroundart = str(appid) + '_hero.jpg'
    bigpictureart = str(appid) + '.jpg'


    #Check if the folder exists, create if not
    grid_exists = os.path.isdir(artwork_path)

    if not grid_exists:
        os.makedirs(artwork_path)
        print("Created grid folder in ", artwork_path)

    

    try:

        print("Checking Artwork...")

        #GameFiles dir if non-Flatpak
        if configpath.is_flatpak == True:
            GameFiles = ""
        else:
            GameFiles = "GameFiles/"

        #Reading from file
        openscript = open(GameFiles + simplified_gamename + ".sh", 'r')
        readscript = openscript.read()
        openscript.close()

        #Avoid SSL certificate error
        ssl._create_default_https_context = ssl._create_unverified_context

        #Check if game is Epic or GOG
        if "EPIC" in readscript:
            
            #print("Epic")

            with open(configpath.heroiclibrarypath, encoding='utf-8') as l:
                epicinstalled = json.load(l)

            for i in epicinstalled['library']:

                gamename = rspchar(i['title'])
                
                if appname == gamename:

                    #Cover Art
                    if checkartworkexists(artwork_path, coverart) == False:
                    
                        image_url = i['art_square']
                        print("Downloading Cover Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + coverart)
                    else:
                        print("Covert Art exists")

                    #Background Art
                    if checkartworkexists(artwork_path, backgroundart) == False:
                    
                        image_url = i['art_cover']
                        print("Downloading Background Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + backgroundart)
                    else:
                        print("Background Art exists")

                    #BigPicture Art
                    if checkartworkexists(artwork_path, bigpictureart) == False:
                    
                        image_url = i['art_cover']
                        print("Downloading BigPicture Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + bigpictureart)
                    else:
                        print("BigPicture Art exists")
        elif "GOG" in readscript:
            
            #print("GOG")

            with open(configpath.goglibrarypath, encoding='utf-8') as l:
                goginstalled = json.load(l)

            for i in goginstalled['games']:

                gamename = rspchar(i['title'])
                
                if appname == gamename:

                    #Cover Art
                    if checkartworkexists(artwork_path, coverart) == False:
                    
                        image_url = i['art_square']
                        print("Downloading Cover Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        extract_image_url = image_url.split("/")[-1]
                        os.rename(artwork_path + '/' + extract_image_url.split("?")[0], artwork_path + '/' + coverart)
                    else:
                        print("Covert Art exists")

                    #Background Art
                    if checkartworkexists(artwork_path, backgroundart) == False:
                    
                        image_url = i['art_cover']
                        print("Downloading Background Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + backgroundart)
                    else:
                        print("Background Art exists")

                    #BigPicture Art
                    if checkartworkexists(artwork_path, bigpictureart) == False:
                    
                        image_url = i['art_cover']
                        print("Downloading BigPicture Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + bigpictureart)
    except Exception:

        print(traceback.format_exc())
        os.system('zenity --error --title="Process Failed" --text="Failed to add artwork. Please check the log for the error and consider reporting it as an issue on Github." --width=400')  
        sys.exit()  

#!/usr/bin/env python3
import ftplib
import os, sys, os.path
from glob import glob
########################################################################################################################
"""This part of code concern both functions fromFtp and send2Ftp"""

recipes = ['recipe1','recipe2','recipe3','recipe4','recipe5','recipe6']# lists of directories containing files to
                                                                              # be downloaded
dest_path = r"output-dir" # a local directory where will be stored downloaded files
local_dir = r"intput-dir" # Where are the files to be sent to the ftp server

########################################################################################################################

def fromFtp(recipes,folder_stock):
    for fold in recipes:
        print(f"******************* Processing {fold} station files **************************".center(100, '*'))
        ftp_resto = ftplib.FTP_TLS('ftp.resto.org')
        ftplib.FTP.login(ftp_resto ,user='userird',passwd='password')
        ftp_resto.encoding = "utf-8"
        ftp_resto.cwd('recipes/'+fold)#"recipes" is the parent directory on ftp, to be replaced by your parent directory
        list_ftp = ftp_resto.nlst()

#""" ------------ the two lines below just allow you to create folders and have a tree structure identical to
#ftp tree                                                                                                       """
        if not os.path.exists(os.path.join(folder_stock, fold)):
            os.mkdir(os.path.join(folder_stock, fold))
        dir_out = (os.path.join(folder_stock, fold))

# """ --------------- This is where the file download begins   ------------------------------------------------------"""
        for file in list_ftp:
            if not os.path.exists(dir_out + "/" + file):
                with open(dir_out + "/" + file, 'wb') as fp:
                    if file.endswith(".csv"):

                        ftp_resto.retrbinary(f"RETR {file}", fp.write)

        ftp_resto.quit()


dowload = fromFtp(recipes,dest_path)

########################################################################################################################

#UPLOAD files ##########################################################################################################


"""This below function allow to send files to server FTP. For example, we want to upload .csv files from our computer
to the ftp server "ftp.resto.org". """

def send2Ftp(recipes, local_dir):
    ftp_resto = ftplib.FTP_TLS('ftp.resto.org.org')
    ftplib.FTP.login(ftp_resto,user='userird',passwd='password')
    ftp_resto.encoding = "utf-8"
    ftp_resto.cwd('/recipes')

    for folders in recipes:
        for file in glob(os.path.join(local_dir,folders)+"/*.csv"):
            filename = (file.split("/")[-1])
            filename1 = filename
            if '_2023' in filename1:  # for example we desire to upload just files contening the year 2023 in the name
                with open(file,"rb") as f:
                    ftp_resto.storbinary('STOR '+filename1,f)

    list_ftp = ftp_resto.nlst() # Lists all files in the resto_recipes directory
    print(list_ftp)


dowload = send2Ftp(recipes,local_dir)


print("By Junior-Muyumba : muyumbaj2@gmail.com")
print("OK JAZZ".center(80,"♠"))






















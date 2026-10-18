# -*- coding: utf-8 -*-
from datetime import datetime
import sqlite3
import os
import json

def getProfilePath(profile):
    profile = str(profile)
    if profile == "1" or profile == "Default":      db_path = "/root/.config/google-chrome/Default"
    else:                                           db_path = "/root/.config/google-chrome/Profile %s" % (profile)
    return db_path

def extract_val(obj):
    result = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "children":
                result.extend(value)
            else:
                result.extend(extract_val(value))
    elif isinstance(obj, list):
        for item in obj:
            result.extend(extract_val(item))
    return result

def getChromeHistory(profile=2):
    db_path = "%s/History" % getProfilePath(profile)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM urls")
        rows = cursor.fetchall()

        url_list = ""
        for row in rows:
            url_list += row[1] + "\n"
            print(row[1])
        conn.close()

        with open("profile_{}_url_list_{}.txt".format(profile, datetime.now().strftime("%y%m%d_%H%M%S")), "w", encoding="utf-8") as fp:
            fp.write(url_list)
    except Exception as e:
        if str(e).strip() == "database is locked":
            print("사용중인 Chrome 브라우저를 종료해주세요")
        else:
            print(e)

def getBookMarks(profile=2):
    db_path = "%s/Bookmarks" % getProfilePath(profile)
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        bookmark_list = ""
        bookmarks = extract_val(data)
        for bmark in bookmarks:
            print(bmark['name'])
            bookmark_list += bmark['url']+"\n"
        with open("profile_{}_bookmark_list_{}.txt".format(profile, datetime.now().strftime("%y%m%d_%H%M%S")), "w", encoding="utf-8") as fp:
            fp.write(bookmark_list)
    except Exception as e:
        print(e)
        
def backupAll(num=10):
    for i in range(1, num):
        getChromeHistory(i)   
        getBookMarks(i)

def mergeTxt(output_file = "merged.txt"):
    folder_path = os.getcwd()
    output_path = os.path.join(folder_path, output_file)

    with open(output_path, "w", encoding="utf-8") as outfile:
        files = sorted(os.listdir(folder_path))

        for filename in files:
            if filename.endswith(".txt") and filename != output_file:
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")

if __name__ == '__main__':
    #openHistoryDB()
    #backupAll(10)
    mergeTxt()
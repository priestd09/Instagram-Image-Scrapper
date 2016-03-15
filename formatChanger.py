import json

currentHashtag = "airmax"

def load_info_from_json_file():
    path = currentHashtag + r'/ImagesInfo.json'
    database = []
    with open(path) as f:
        for line in f:
            database.append(line)
    if (len(database)>0):
        return json.loads(database[0])
    else:
        return []


def save_str_as_txt(fileName, str):
    outputPath = fileName
    fout = open(outputPath, 'w')
    fout.write(str.encode('utf8'))
    fout.close()

db = load_info_from_json_file()
likesFile = ""
followersFile = ""
hashtagsFile = ""

k = 0
for obj in db:
    k += 1
    if str(obj[1]) == "":
        likesFile += str(obj[0]) + "=0\n"
    else:
        startIndex = str(obj[1]).find(",")
        if startIndex == -1:
            likesFile += str(obj[0]) + "=" + str(obj[1]) + "\n"
        else:
            likesFile += str(obj[0]) + "=" + str(obj[1])[:startIndex] + str(obj[1])[startIndex+1:] + "\n"


    if str(obj[2]) == "":
        followersFile += str(obj[0]) + "=0\n"
    else:
        startIndex = str(obj[2]).find(",")
        if startIndex == -1:
            followersFile += str(obj[0]) + "=" + str(obj[2]) + "\n"
        else:
            followersFile += str(obj[0]) + "=" + str(obj[2])[:startIndex] + str(obj[2])[startIndex+1:] + "\n"

    hashtagsFile += str(obj[0]) + "="
    for hashtag in obj[3]:
        hashtagsFile += "#" + hashtag
    hashtagsFile += "\n"

    print "\r",k,"/",len(db),

save_str_as_txt(currentHashtag + "/likes_file.txt", likesFile)
save_str_as_txt(currentHashtag + "/hashtags_file.txt", hashtagsFile)
save_str_as_txt(currentHashtag + "/followers_file.txt", followersFile)
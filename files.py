from os import listdir, mkdir
from os.path import isfile, join, exists
import shutil
import json


def keys():
    return {f.split('.')[0] for f in listdir("./static/imgs")
            if isfile(join("./static/imgs", f))}


def metadata(key):
    key = format(int(key), '06d')
    ret = json.load(open(f"./static/tags/{key}.json", "r"))
    return ret

def getUsers():
    ret = json.load(open("./static/users.json", "r"))
    return ret

def add_user(new_user):
    users = json.load(open("./static/users.json", "r"))
    users[new_user["username"]] = {"age": new_user["age"],
                                   "favorites": []}
    json.dump(users, open("./static/users.json", "w"))


def add_tag(key, tag):
    img_metadata = json.load(open(f"./static/tags/{key}.json", "r"))
    if not tag in img_metadata["tags"]:
        img_metadata["tags"].append(tag)
    json.dump(img_metadata,
              open(f"./static/tags/{key}.json", "w"))


def list_tags():
    if isfile("./static/tagsList.txt"):
        return {line[:-1] for line in open("./static/tagsList.txt", "r")}
    else:
        return {}

def update_tagSet(tagsSet, new_tag):
    tagsSet.add(new_tag)
    with open("./static/tagsList.txt", "w") as f:
        for line in tagsSet:
            f.write(line + "\n")
    return tagsSet

if __name__ == "__main__":

    files = [f for f in listdir("./static/imgs")
             if isfile(f"./static/imgs/{f}")]
    print(len(files))
    files = sorted(files)
    if not exists("./static/tags"):
        mkdir("./static/tags")
    for i, f in enumerate(files):
        key = format(i, '06d')
        path = f"imgs/{key}.{f.split('.')[1]}"
        shutil.move(f"./static/imgs/{f}",
                    f"./static/imgs/{key}.{f.split('.')[1]}")
        json.dump({"id": key,
                   "path": path,
                   "tags": ["test"]},
                  open(f"./static/tags/{key}.json", "w"))
    with open("./static/tagsList.txt", "w") as f:
        f.write("test\n")

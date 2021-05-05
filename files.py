from os import listdir, scandir
from os.path import isfile, join
import shutil
import json


def keys():
    return {f.split('.')[0] for f in listdir("./static/imgs")
            if isfile(join("./static/imgs", f))}


def tags(key):
    key = format(int(key), '06d')
    ret = json.load(open(f"./static/tags/{key}.json", "r"))
    return ret


if __name__ == "__main__":

    files = [f for f in listdir("./static/imgs")
             if isfile(f"./static/imgs/{f}")]
    print(len(files))
    files = sorted(files)
    for i, f in enumerate(files):
        key = format(i, '06d')
        path = f"imgs/{key}.{f.split('.')[1]}"
        shutil.move(f"./static/imgs/{f}",
                    f"./static/imgs/{key}.{f.split('.')[1]}")
        json.dump({"id": key,
                   "path": path,
                   "tags": ["test"]},
                  open(f"./static/tags/{key}.json", "w"))

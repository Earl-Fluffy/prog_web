from os import listdir
from os.path import isfile, join
import shutil
import json


def keys():
    return {f.split('.')[0]
            for f in listdir("./static/imgs")
            if isfile(join("./static/imgs", f))}


if __name__ == "__main__":

    files = [f for f in listdir("./static/imgs")
             if isfile(join("./static/imgs", f))]
    for i, f in enumerate(files):
        key = format(i, '06d')
        path = f"./static/imgs/{key}.{f.split('.')[1]}"
        shutil.move(f"./static/imgs/{f}",
                    path)
        json.dump({"id": key,
                   "path": path,
                   "tags": ["test"]},
                  open(f"./static/tags/{key}.json", "w"))

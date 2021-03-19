from os import listdir
from os.path import isfile, join
import shutil
import json


files = [f for f in listdir("./imgs") if isfile(join("./imgs", f))]
for i, f in enumerate(files):
    key = format(i, '06d')
    path = f"./imgs/{key}.{f.split('.')[1]}"
    shutil.move(f"./imgs/{f}",
                path)
    json.dump({"id": key,
               "path": path,
               "tags": ["test"]},
              open(f"./tags/{key}.json", "w"))

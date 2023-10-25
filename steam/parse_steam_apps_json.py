#!/usr/bin/env python3

import json

with open("apps.json") as f:
    data = json.load(f)
    for i in data["applist"]["apps"]:
        print(i)

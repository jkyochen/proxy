#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, base64, json, sys
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

v2ray_subscribe = os.getenv("V2RAY_SUBSCRIBE")
if not v2ray_subscribe:
    print("Lose v2ray subscribe url, you need create .env file like .env.example")
    exit(1)

# Proxy
proxy = []
proxyName = []

r = requests.get(v2ray_subscribe)
d = base64.b64decode(r.text + "==").decode("utf-8")[:-1]
for v in d.split("\n"):
    conf = json.loads(base64.b64decode(v.split(r"//")[1] + "==").decode("utf-8"))
    proxy.append(
        ", ".join(
            [
                conf["ps"] + " = vmess",
                conf["add"],
                conf["port"],
                "username=" + conf["id"],
                "tls=true",
            ]
        )
    )
    proxyName.append(conf["ps"])

# Rule
r = requests.get(
    "https://raw.githubusercontent.com/Hackl0us/SS-Rule-Snippet/master/LAZY_RULES/Surge/Surge%203.conf"
)
d = r.text

surgeConfig = "\n".join(
    [
        d[: d.index("[Proxy]")],
        "[Proxy]",
        "\n".join(proxy),
        "[Proxy Group]",
        "Proxy = select," + ", ".join(proxyName),
        d[d.index("[Rule]") :],
    ]
)
with open(os.getcwd() + "/surge.conf", "w") as f:
    f.write(surgeConfig)

surgePath = os.path.expanduser("~") + "/Library/Application Support/Surge/Profiles"
if Path(surgePath).exists():
    with open(surgePath + "/surge.conf", "w") as f:
        f.write(surgeConfig)

import os
import re
import json
import time
import sys
from urllib.parse import urlparse
import requests


OUT_ROOT = "downloaded_assets"
OUT_ASSET_MAP = "asset_map.local.js"


def guess_ext(url: str) -> str:
    path = urlparse(url).path
    _, ext = os.path.splitext(path)
    return ext if ext else ".bin"


def load_assets(js_path: str) -> dict:
    text = open(js_path, "r", encoding="utf-8").read()
    m = re.search(r"const\s+assets\s*=\s*(\{.*\})\s*;", text, flags=re.S)
    if not m:
        raise RuntimeError("Không tìm thấy `const assets = {}` trong file")
    return json.loads(m.group(1))


def download(session, url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with session.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(1024 * 256):
                if chunk:
                    f.write(chunk)


def main():
    js_path = sys.argv[1] if len(sys.argv) > 1 else "asset_map.js"

    assets = load_assets(js_path)
    session = requests.Session()
    session.headers["User-Agent"] = "asset-localizer"

    new_assets = {}
    total = len(assets)

    for i, (key, data) in enumerate(assets.items(), 1):
        url = data["url"]
        a_type = data.get("type", "misc")

        ext = guess_ext(url)
        local_path = f"{OUT_ROOT}/{a_type}/{key}{ext}"
        disk_path = local_path.replace("/", os.sep)

        print(f"[{i}/{total}] {key}")

        if not os.path.exists(disk_path):
            download(session, url, disk_path)
            time.sleep(0.05)

        # copy data + replace url
        new_data = dict(data)
        new_data["url"] = local_path
        new_assets[key] = new_data

    # ghi file asset_map.local.js
    with open(OUT_ASSET_MAP, "w", encoding="utf-8") as f:
        f.write("// AUTO-GENERATED - LOCAL ASSET MAP\n")
        f.write("const assets = ")
        json.dump(new_assets, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n✅ DONE")
    print(f"📁 Assets  : {OUT_ROOT}/")
    print(f"📄 JS file : {OUT_ASSET_MAP}")


if __name__ == "__main__":
    main()

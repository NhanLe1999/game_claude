import os
import json

#D:\CodeHtml\unity-webview-master\unity-webview-master\sample\Assets\StreamingAssets\downloaded_assets

ROOT_FOLDER = r"D:/CodeHtml/unity-webview-master/unity-webview-master/sample/Assets/StreamingAssets/downloaded_assets"   # folder gốc
OUTPUT_JSON = "files.json"

files = []

for root, dirs, filenames in os.walk(ROOT_FOLDER):
    for filename in filenames:
        # Bỏ qua file .meta
        if filename.endswith(".meta"):
            continue

        full_path = os.path.join(root, filename)

        # Đường dẫn tương đối (rất tiện cho Unity)
        relative_path = os.path.relpath(full_path, ROOT_FOLDER)

        files.append(relative_path.replace("\\", "/"))

# Ghi JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(files, f, ensure_ascii=False, indent=2)

print(f"Đã export {len(files)} file")

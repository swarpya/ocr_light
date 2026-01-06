import requests
import os
import json

API_URL = "http://localhost:8000/ocr"
INPUT_FOLDER = "./documents_to_scan"
OUTPUT_FOLDER = "./ocr_results"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(INPUT_FOLDER, exist_ok=True)

def scan_file(filename):
    file_path = os.path.join(INPUT_FOLDER, filename)
    print(f"🚀 Sending {filename}...")
    
    try:
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            # No engine selection needed, server handles it auto-magically
            response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return None

if __name__ == "__main__":
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.pdf', '.png', '.jpg', '.pptx', '.xlsx', '.xls'))]
    
    if not files:
        print(f"⚠️  No files in {INPUT_FOLDER}")
    else:
        print(f"Found {len(files)} files.\n")
        for filename in files:
            result = scan_file(filename)
            if result:
                out_name = f"{os.path.splitext(filename)[0]}_result.json"
                out_path = os.path.join(OUTPUT_FOLDER, out_name)
                with open(out_path, "w") as f:
                    json.dump(result, f, indent=4)
                print(f"✅ Saved: {out_name}")
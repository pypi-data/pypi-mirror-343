import os, zipfile
def install(zip_path, cache_path):
    if os.path.exists(zip_path):
        print(f"📦 복원: {zip_path} → {cache_path}")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(cache_path)
    else:
        raise FileNotFoundError(f"❌ 립 파일 없음: {zip_path}")
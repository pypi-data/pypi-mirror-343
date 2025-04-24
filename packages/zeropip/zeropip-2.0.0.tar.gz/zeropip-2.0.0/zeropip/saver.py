import os, zipfile, shutil
def save(cache_path, zip_path):
    tmp_dir = "/tmp/zeropip_tmp"
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    shutil.copytree(cache_path, tmp_dir)
    base_path = zip_path.replace(".zip", "")
    shutil.make_archive(base_path, 'zip', tmp_dir)
    shutil.rmtree(tmp_dir)
    print(f"💾 저장 완료: {zip_path}")
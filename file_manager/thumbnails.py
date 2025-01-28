import os
import shutil
from PIL import Image

# 원본 이미지 디렉토리와 미리보기 저장 디렉토리 설정
source_dir = '/home/hong/python-workspace/file-cloud/static/images'
thumbnail_dir = '/home/hong/python-workspace/file-cloud/static/images/thumbnails'

# 미리보기 이미지 크기 설정
thumbnail_size = (300, 200)

# 미리보기 폴더 생성
os.makedirs(thumbnail_dir, exist_ok=True)

# 폴더 복사 및 이미지 변환 함수
def process_folders(folder_names, source_base, target_base, size):
    for folder in folder_names:
        source_folder = os.path.join(source_base, folder)
        target_folder = os.path.join(target_base, folder)
        
        # 폴더 복사
        if not os.path.exists(target_folder):
            shutil.copytree(source_folder, target_folder)
            print(f"Copied folder: {folder} to thumbnails/")
        
        # 이미지 변환
        for root, _, files in os.walk(target_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.png', '.gif')):
                    original_path = os.path.join(root, file)
                    try:
                        with Image.open(original_path) as img:
                            img.thumbnail(size)
                            # 화질(quality) 설정 추가
                            img.save(original_path, quality=85, optimize=True)
                            print(f"Thumbnail created: {original_path}")
                    except Exception as e:
                        print(f"Error processing {original_path}: {e}")

# 변환 대상 폴더 이름
folders_to_process = ['4waves', 'hari', 'hoon', 'jaelin', 'soyeon']

# 실행
process_folders(folders_to_process, source_dir, thumbnail_dir, thumbnail_size)

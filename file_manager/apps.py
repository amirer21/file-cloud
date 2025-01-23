from django.apps import AppConfig
import os
from PIL import Image
from django.conf import settings


class FileManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_manager'

    # def ready(self):
    #     # 서버 시작 시 변환 작업 수행
    #     self.perform_conversion_at_startup()

    def perform_conversion_at_startup(self):
        """
        서버 시작 시 NEF 파일 변환 작업을 수행합니다.
        """
        print("Starting NEF to JPG conversion...")
        #BASE_DIR = "/mnt/e/사진 정리 64(2025.01 피아노)"  # 원본 NEF 파일 경로
        #r"E:\내보내기\2025-01-피아노"
        BASE_DIR = "/mnt/e/내보내기/2025-01-피아노"
        OUTPUT_DIR = settings.MEDIA_ROOT  # 변환된 파일 저장 경로

        # 저장 경로가 없으면 생성
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # 변환되지 않은 NEF 파일 확인 및 변환
        nef_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.NEF')]
        converted_files = {f.replace('.jpg', '.NEF') for f in os.listdir(OUTPUT_DIR)}

        for nef_file in nef_files:
            if nef_file not in converted_files:  # 변환되지 않은 파일만 변환
                nef_path = os.path.join(BASE_DIR, nef_file)
                jpg_path = os.path.join(OUTPUT_DIR, nef_file.replace('.NEF', '.jpg'))
                self.convert_nef_to_jpg(nef_path, jpg_path)
                print(f"Converted: {nef_file}")
            else:
                print(f"Already converted: {nef_file}")

    @staticmethod
    def convert_nef_to_jpg(nef_path, jpg_path):
        """
        NEF 파일을 JPG로 변환합니다.
        """
        try:
            with Image.open(nef_path) as img:
                img.convert('RGB').save(jpg_path, 'JPEG')
            print(f"Converted: {nef_path} -> {jpg_path}")
        except Exception as e:
            print(f"Failed to convert {nef_path}: {e}")

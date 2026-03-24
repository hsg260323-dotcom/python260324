import os
import shutil
from pathlib import Path

# 다운로드 폴더 경로
DOWNLOADS_PATH = r"C:\Users\student\Downloads"

# 파일 분류 규칙
FILE_CATEGORIES = {
    'images': ['.jpg', '.jpeg'],
    'data': ['.csv', '.xlsx'],
    'docs': ['.txt', '.doc', '.pdf'],
    'archive': ['.zip']
}

def create_folders_if_not_exist(base_path):
    """필요한 폴더들을 생성합니다"""
    for folder_name in FILE_CATEGORIES.keys():
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"폴더 생성: {folder_path}")

def get_file_category(file_extension):
    """파일 확장자에 따라 카테고리를 반환합니다"""
    file_extension = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return None

def organize_downloads():
    """다운로드 폴더의 파일들을 자동으로 분류합니다"""
    
    # 폴더가 존재하는지 확인
    if not os.path.exists(DOWNLOADS_PATH):
        print(f"다운로드 폴더를 찾을 수 없습니다: {DOWNLOADS_PATH}")
        return False
    
    # 필요한 폴더 생성
    create_folders_if_not_exist(DOWNLOADS_PATH)
    
    # 다운로드 폴더의 모든 파일 처리
    moved_count = 0
    error_count = 0
    
    for filename in os.listdir(DOWNLOADS_PATH):
        file_path = os.path.join(DOWNLOADS_PATH, filename)
        
        # 폴더는 건너뛰기
        if os.path.isdir(file_path):
            continue
        
        # 파일 확장자 가져오기
        file_extension = os.path.splitext(filename)[1]
        
        # 카테고리 확인
        category = get_file_category(file_extension)
        
        if category:
            destination_folder = os.path.join(DOWNLOADS_PATH, category)
            destination_path = os.path.join(destination_folder, filename)
            
            try:
                # 같은 이름의 파일이 이미 있는 경우 처리
                if os.path.exists(destination_path):
                    base_name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(destination_folder, f"{base_name}_{counter}{ext}")):
                        counter += 1
                    destination_path = os.path.join(destination_folder, f"{base_name}_{counter}{ext}")
                
                # 파일 이동
                shutil.move(file_path, destination_path)
                print(f"이동 완료: {filename} → {category}/")
                moved_count += 1
                
            except Exception as e:
                print(f"오류 발생: {filename} - {str(e)}")
                error_count += 1
    
    # 결과 출력
    print(f"\n{'='*50}")
    print(f"작업 완료!")
    print(f"이동된 파일: {moved_count}개")
    print(f"오류 발생: {error_count}개")
    print(f"{'='*50}")
    
    return True

if __name__ == "__main__":
    print("Windows 다운로드 폴더 자동 분류 시작...\n")
    organize_downloads()

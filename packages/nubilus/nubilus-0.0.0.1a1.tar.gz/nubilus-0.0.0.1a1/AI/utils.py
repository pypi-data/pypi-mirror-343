import os

def mkdir(path):
    """
    지정된 경로에 폴더를 생성하는 함수
    이미 같은 이름의 폴더가 있으면 뒤에 숫자를 추가하여 생성
    
    Args:
        path (str): 생성할 폴더의 경로
    
    Returns:
        str: 생성된 폴더의 경로
    """
    try:
        original_path = path
        count = 1

        # 중복 방지: 동일한 폴더명이 있으면 뒤에 숫자 추가
        while os.path.exists(path):
            path = f"{original_path}_{count}"
            count += 1
        
        os.makedirs(path)
        print(f"✅ 폴더 생성 완료: {path}")
        return path  # 메시지 대신 경로만 반환

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return path  # 오류 발생 시에도 경로 반환
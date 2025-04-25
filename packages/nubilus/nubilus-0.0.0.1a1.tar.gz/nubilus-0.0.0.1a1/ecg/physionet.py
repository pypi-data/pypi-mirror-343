import os, numpy as np
import wfdb
from wfdb.io import Annotation
from glob import glob

SYMBOL = ['N',      # 정상 박동 (Normal beat)
          'L',      # 좌각 차단 박동 (Left bundle branch block beat)
          'R',      # 우각 차단 박동 (Right bundle branch block beat)
          'B',      # 각 차단 박동 (Bundle branch block beat, unspecified)
          'A',      # 심방 조기 박동 (Atrial premature beat)
          'a',      # 이상 심방 조기 박동 (Aberrated atrial premature beat)
          'J',      # 방실 접합부 조기 박동 (Nodal (junctional) premature beat)​
          'S',      # 상심실성 조기 박동 (Supraventricular premature or ectopic beat)​
          'V',      # 심실 조기 수축 (Premature ventricular contraction)
          'r',      # 이상 심실 조기 수축 (R-on-T premature ventricular contraction)
          'F',      # 심실 이탈 박동 (Ventricular escape beat)
          'e',      # 방실 접합부 이탈 박동 (Nodal (junctional) escape beat)
          'j',      # 심방 이탈 박동 (Supraventricular escape beat)
          'E',      # 심실 조기 수축 (Ventricular escape beat)
          '/',      # 심방 조기 수축 (Paced beat)
          'f',      # 심방 세동 파형 (Fusion of paced and normal beat)
          'Q',      # 심실 조기 수축 (Unclassifiable beat)
          '?',      # 분류 불가능한 박동 (Unclassifiable beat)
          '!',      # 리듬 변화 (Rhythm change)
          '[',      # 주석 시작 (Annotation start)
          ']',      # 주석 종료 (Annotation end)
          'x',      # 심실 조기 수축 (Non-conducted P-wave (blocked APB))
          '~',      # 노이즈 (Signal quality change)
          '|',      # 심실 조기 수축 (Isolated QRS-like artifact)
          '+',      # 리듬 주석 (Rhythm annotation)
          '****',   # 리듬 주석 (Rhythm annotation)
          '"',      # 주석 텍스트 (Comment annotation)
          '=',      # 심실 조기 수축 (Measurement annotation)
          '@']      # 심실 조기 수축 (Link to external data)

R_PEAK_SYMBOL = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e', 'j', 'E']

def extract_symbol_samples(annotation:Annotation, target_symbols=R_PEAK_SYMBOL):
    """
    주어진 wfdb.Annotation 객체에서 원하는 심볼들만 필터링하여 sample index 배열을 반환함.

    Parameters:
        annotation (wfdb.Annotation): wfdb.rdann()으로 생성된 주석 객체
        target_symbols (str 또는 list of str): 추출하고자 하는 심볼 또는 심볼들의 리스트

    Returns:
        np.ndarray: 선택된 심볼에 해당하는 sample index 배열

    Raises:
        TypeError: annotation이 wfdb.Annotation이 아닌 경우
        ValueError: target_symbols가 str 또는 list of str이 아닌 경우
    """
    # target_symbols를 리스트 형태로 통일
    if isinstance(target_symbols, str):
        target_symbols = [target_symbols]
    elif isinstance(target_symbols, list):
        if not all(isinstance(sym, str) for sym in target_symbols):
            raise ValueError("target_symbols는 str 또는 str의 리스트여야 합니다.")
    else:
        raise ValueError("target_symbols는 str 또는 str의 리스트여야 합니다.")

    # 심볼 필터링
    mask = [sym in target_symbols for sym in annotation.symbol]
    return np.array(annotation.sample, dtype=np.uint32)[mask]

def load_data(folder_path:str, target_extender='atr'):
    files = glob(os.path.join(folder_path, f'*.{target_extender}'))
    files.sort()
    record, ann = [None for i in range(len(files))], [None for i in range(len(files))]
    non_exist_r, non_exist_a = [], []
    for i in range(len(files)):
        try:
            record[i] = wfdb.rdrecord(files[i][:-4])
        except FileExistsError as F:
            non_exist_r.append(files[i][:-4]+'.dat')
        try:
            ann[i] = wfdb.rdann(files[i][:-4], target_extender)
        except FileExistsError as F:
            non_exist_a.append(files[i])
    return record, ann, non_exist_r, non_exist_a
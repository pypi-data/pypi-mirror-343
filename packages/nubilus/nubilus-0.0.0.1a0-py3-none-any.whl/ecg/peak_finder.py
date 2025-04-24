import numpy as np
from numba import njit
from scipy import signal
from .processor import *
# ==================================
# ========== 01. R finder ==========
# ==================================

@njit
def thresholding(ecg: np.ndarray, th, fs=None):
    R = []
    N = len(ecg)

    if isinstance(th, float) or isinstance(th, int):
        # --- Case 1: th is scalar ---
        if fs is not None:
            skip_time = int(fs * 0.15)
            ecg_len, i = N - 2, 1
            while i < ecg_len:
                if (ecg[i] > ecg[i+1]) and (ecg[i] > ecg[i-1]) and (ecg[i] > th):
                    R.append(i)
                    i += skip_time
                else:
                    i += 1
        else:
            ecg_len, i = N - 1, 1
            while i < ecg_len:
                if (ecg[i] > ecg[i+1]) and (ecg[i] > ecg[i-1]) and (ecg[i] > th):
                    R.append(i)
                i += 1

    else:
        # --- Case 2: th is array ---
        if fs is not None:
            i = 0
            while i < N:
                if ecg[i] > th[i]:
                    win = int(fs * 0.25)
                    end = min(i + win, N)
                    max_val = ecg[i]
                    max_idx = i
                    for j in range(i + 1, end):
                        if ecg[j] > max_val:
                            max_val = ecg[j]
                            max_idx = j

                    R.append(max_idx)
                    i = end  # skip overlapping region
                else:
                    i += 1

    return np.array(R, dtype=np.int32)

@njit
def adaptive_th(sig: np.ndarray, fs: int, window_sec: float = 2.0, scale: float = 2.0) -> np.ndarray:
    """
    Adaptive threshold 계산 (2초 이동 윈도우 + 표준편차 기반)

    Parameters:
        signal (np.ndarray): 입력 신호 PT(n)
        fs (int): 샘플링 주파수 (Hz)
        window_sec (float): 이동 윈도우 길이 (초 단위, 기본값 2.0)
        scale (float): 표준편차에 곱할 계수 (기본값 2.0)

    Returns:
        np.ndarray: Adaptive threshold 배열 (signal과 동일 길이)
    """
    N = len(sig)
    win_size = int(fs * window_sec)
    threshold = np.zeros(N)

    for i in range(N):
        if i < win_size:
            segment = sig[:i+1]
        else:
            segment = sig[i - win_size + 1:i + 1]

        # std 계산 수동 구현 (numba는 np.std 지원이 제한적)
        mean = 0.0
        for v in segment:
            mean += v
        mean /= len(segment)

        std = 0.0
        for v in segment:
            std += (v - mean)**2
        std = (std / len(segment))**0.5

        threshold[i] = std * scale

    return threshold

def detect_r_peaks(ecg_signal: np.ndarray, fs: int, window_sec=2, scale=2) -> np.ndarray:
    """
    TKEO + EWMA 기반 R-peak 검출 함수 (adaptive threshold 방식)

    Parameters:
        ecg_signal (np.ndarray): 1D ECG 입력
        fs (int): 샘플링 주파수

    Returns:
        np.ndarray: R-peak 인덱스 배열
    """
    # 1. Band-pass filtering (8~50Hz FIR)
    _bpf = BPF(fs, (8, 50), 1000, 'FIR')(ecg_signal)

    # 2. Teager-Kaiser Energy Operator 적용
    tkeo_signal = TKEO(_bpf)

    # 3. Envelope smoothing
    envelope = EWMA(tkeo_signal)

    # 4. Adaptive threshold 계산 (2초 이동 윈도우, 표준편차 기반)
    threshold = adaptive_th(envelope, fs, window_sec, scale)

    # 5. thresholding 기반 R-peak 검출
    r_peak_indices = thresholding(envelope, threshold, fs)

    return r_peak_indices

@njit
def _detect_t_wave_core(filtered_ecg: np.ndarray, r_peaks: np.ndarray, fs: int) -> np.ndarray:
    """
    JIT 최적화된 T파 탐지 핵심 로직
    """
    N = len(r_peaks)
    t_peaks = []

    for i in range(N):
        # RR 계산
        if i < N - 1:
            rr = r_peaks[i+1] - r_peaks[i]
        elif i > 0:
            rr = r_peaks[i] - r_peaks[i-1]
        else:
            rr = int(0.8 * fs)  # fallback

        # 탐색 구간 설정
        start = r_peaks[i] + int(0.12 * rr)
        end = r_peaks[i] + int(0.57 * rr) + int(0.06 * fs)

        if start >= len(filtered_ecg) or end > len(filtered_ecg) or start >= end:
            continue

        rv = 0.1
        max_val = -1e10
        max_idx = start

        for j in range(start, end):
            val = np.arctan(filtered_ecg[j] / rv)
            if val > max_val:
                max_val = val
                max_idx = j

        t_peaks.append(max_idx)

    return np.array(t_peaks, dtype=np.int32)

def detect_t_peaks(ecg_signal, r_peaks, fs=250):
    """
    전체 T wave 탐지 함수 (필터링 + JIT)
    """
    # 1. BPF 전처리 (JIT 불가능하므로 여기서 처리)
    _ecg_signal = BPF(fs, (0.5, 40), 1000, 'FIR')(ecg_signal)

    # 2. JIT 최적화된 T wave 탐지 함수 호출
    t_peaks = _detect_t_wave_core(_ecg_signal, r_peaks, fs)

    return t_peaks

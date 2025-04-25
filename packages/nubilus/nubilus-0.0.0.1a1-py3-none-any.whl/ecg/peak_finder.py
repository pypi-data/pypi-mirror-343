import numpy as np
from numba import njit
from .processor import *
import pywt
from matplotlib import pyplot as plt


@njit
def thresholding(ecg: np.ndarray, th, fs=None):
    R = []
    N = len(ecg)

    if isinstance(th, float) or isinstance(th, int):
        # Case 1: Scalar threshold
        i = 1
        while i < N - 1:
            if ecg[i] > th and ecg[i] > ecg[i - 1] and ecg[i] > ecg[i + 1]:
                R.append(i)
                if fs is not None:
                    i += int(fs * 0.15)
                    continue
            i += 1

    else:
        # Case 2: Array threshold → 개선된 버전
        i = 0
        in_peak_zone = False
        peak_val = -1e9
        peak_idx = -1

        while i < N:
            if ecg[i] > th[i]:
                # 임계값을 넘은 구간에 진입
                if not in_peak_zone:
                    in_peak_zone = True
                    peak_val = ecg[i]
                    peak_idx = i
                else:
                    if ecg[i] > peak_val:
                        peak_val = ecg[i]
                        peak_idx = i
            else:
                # 임계값 아래로 내려왔으면 이전 zone의 최고점 저장
                if in_peak_zone:
                    R.append(peak_idx)
                    in_peak_zone = False
            i += 1

        # 만약 끝까지 in_peak_zone이면 마지막 최고점 저장
        if in_peak_zone:
            R.append(peak_idx)

    return np.array(R, dtype=np.int32)


@njit
def _std(x):
    mean = 0.0
    for v in x:
        mean += v
    mean /= len(x)

    var = 0.0
    for v in x:
        var += (v - mean)**2
    return (var / len(x))**0.5

@njit
def adaptive_th(sig: np.ndarray, fs: int, window_sec: float = 0.5, scale: float = 0.5) -> np.ndarray:
    """
    Adaptive threshold 계산 (forward + reverse 평균) - zero phase shift

    Parameters:
        sig (np.ndarray): 입력 신호
        fs (int): 샘플링 주파수 (Hz)
        window_sec (float): 이동 윈도우 시간 (초)
        scale (float): std에 곱할 계수

    Returns:
        np.ndarray: phase 보정된 adaptive threshold
    """
    N = len(sig)
    win_size = int(fs * window_sec)

    th_fwd = np.zeros(N)
    th_rev = np.zeros(N)

    # 순방향 계산
    for i in range(N):
        if i < win_size:
            segment = sig[:i+1]
        else:
            segment = sig[i - win_size + 1:i + 1]

        th_fwd[i] = _std(segment) * scale

    # 역방향 계산
    for i in range(N):
        j = N - 1 - i  # 역방향 인덱스
        if j + win_size > N:
            segment = sig[j:]
        else:
            segment = sig[j:j + win_size]

        th_rev[j] = _std(segment) * scale

    return (th_fwd + th_rev) / 2

@njit
def refine_peaks(signal: np.ndarray, r_peaks: np.ndarray, fs: int, left_ms: int, right_ms: int) -> np.ndarray:
    """
    Numba JIT 기반 빠른 R-peak 보정 함수 (±ms 범위 내 최댓값으로 이동)

    Parameters:
        signal (np.ndarray): 원본 ECG 신호
        r_peaks (np.ndarray): 초기 R-peak 인덱스 배열
        fs (int): 샘플링 주파수 (Hz)
        left_ms (int): R-peak 기준 왼쪽 탐색 범위 (ms)
        right_ms (int): R-peak 기준 오른쪽 탐색 범위 (ms)

    Returns:
        np.ndarray: 보정된 R-peak 인덱스 배열
    """
    refined = []
    left_offset = int(left_ms * fs / 1000)
    right_offset = int(right_ms * fs / 1000)
    N = len(signal)

    for i in range(len(r_peaks)):
        idx = r_peaks[i]
        start = max(idx - left_offset, 0)
        end = min(idx + right_offset + 1, N)

        max_val = signal[start]
        max_idx = start
        for j in range(start + 1, end):
            if signal[j] > max_val:
                max_val = signal[j]
                max_idx = j

        refined.append(max_idx)

    return np.array(refined, dtype=np.int32)


def detect_r_peaks(ecg_signal: np.ndarray, fs: int, window_sec=2, scale=2, outlier=4, debuging:bool=False, xlim=[0,-1]) -> np.ndarray:
    """
    Wavelet + TKEO + EWMA 기반 R-peak 검출 함수 (adaptive threshold 방식)

    Parameters:
        ecg_signal (np.ndarray): 1D ECG 입력
        fs (int): 샘플링 주파수

    Returns:
        np.ndarray: R-peak 인덱스 배열
    """
    # 1. Band-pass filtering (8~50Hz FIR)
    _bpf = BPF(fs, (10, 30), (2, 1000), 'HYBRID')(ecg_signal)

    # 2. Wavelet transform - level 8
    coeffs = pywt.wavedec(_bpf, 'db4', level=5)
    cD8 = coeffs[-2]  # 마지막 detail coefficient 사용
    # outlier = cD8.std()*outlier
    # cD8[cD8>outlier] = outlier
    # cD8[cD8<-outlier] = -outlier
    
    # 4. Teager-Kaiser Energy Operator 적용
    tkeo_signal = TKEO(cD8)
    outlier = tkeo_signal.std()*outlier
    tkeo_signal[tkeo_signal>outlier] = outlier
    tkeo_signal[tkeo_signal<-outlier] = -outlier
    
    # 5. Envelope smoothing
    envelope = EWMA(tkeo_signal, 0.2)
    
    # 6. Adaptive threshold 계산
    threshold = adaptive_th(envelope, fs, window_sec, scale)

    # 7. thresholding 기반 R-peak 검출
    r_peak_indices = thresholding(envelope, threshold, fs)
    
    if debuging:
        plt.figure(figsize=(20,18))
        time = np.arange(len(ecg_signal))/fs
        plt.subplot(5, 1, 1);plt.grid();plt.plot(time, ecg_signal);plt.title('Original');plt.xlim(xlim[0], xlim[1] if xlim[1] != -1 else time[-1])
        plt.subplot(5, 1, 2);plt.grid();plt.plot(time, _bpf);plt.title('BPF');plt.xlim(xlim[0], xlim[1] if xlim[1] != -1 else time[-1])
        time = np.arange(len(cD8))/fs*4
        plt.subplot(5, 1, 3);plt.grid();plt.plot(time, cD8);plt.title('WT');plt.xlim(xlim[0], xlim[1] if xlim[1] != -1 else time[-1])#;plt.plot([time[0],time[-1]], [std,std])
        plt.subplot(5, 1, 4);plt.grid();plt.plot(time, tkeo_signal);plt.title('TKEO');plt.xlim(xlim[0], xlim[1] if xlim[1] != -1 else time[-1])
        plt.subplot(5, 1, 5);plt.grid();plt.plot(time, envelope);plt.title('Evelope');plt.xlim(xlim[0], xlim[1] if xlim[1] != -1 else time[-1])
        plt.plot(time, threshold);plt.plot(time[r_peak_indices], envelope[r_peak_indices], 'o')

    return r_peak_indices*4


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

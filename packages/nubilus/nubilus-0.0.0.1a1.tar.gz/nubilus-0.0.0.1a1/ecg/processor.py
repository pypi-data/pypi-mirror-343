import numpy as np
from scipy.signal import butter, firwin, filtfilt
from numba import njit

class BPF:
    def __init__(self, fs, cutoff, order, method: str = 'iir'):
        self.method = method.upper()
        self.fs = fs
        self.order = order
        if self.method == 'IIR':
            nyq = fs * 0.5
            low = cutoff[0] / nyq
            high = cutoff[1] / nyq
            self.b, self.a = butter(order, [low, high], btype='band')
        elif self.method == 'FIR':
            self.taps = firwin(order + 1, cutoff, pass_zero=False, fs=fs)
        elif self.method == 'HYBRID':
            nyq = fs * 0.5
            low = cutoff[0] / nyq
            high = cutoff[1] / nyq
            self.b, self.a = butter(order[0], [low, high], btype='band')
            self.taps = firwin(order[1] + 1, cutoff, pass_zero=False, fs=fs)

    def __call__(self, input_signal: np.ndarray):
        pad_len = int(self.fs * 1.0)  # 1초 패딩

        # 앞뒤 반복 padding
        head = input_signal[:pad_len][::-1] if len(input_signal) > pad_len else np.zeros(pad_len)
        tail = input_signal[-pad_len:][::-1] if len(input_signal) > pad_len else np.zeros(pad_len)
        padded = np.concatenate([head, input_signal, tail])

        # 필터 적용
        if self.method == 'IIR':
            filtered = filtfilt(self.b, self.a, padded)
        elif self.method == 'FIR':
            filtered = filtfilt(self.taps, [1.0], padded)
        elif self.method == 'HYBRID':
            tmp = filtfilt(self.b, self.a, padded)
            filtered = filtfilt(self.taps, [1.0], tmp)

        # 원래 신호 길이만 추출
        return filtered[pad_len:-pad_len]

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


@njit
def TKEO(sig: np.ndarray) -> np.ndarray:
    n = len(sig)
    tkeo = np.empty(n, dtype=np.float64)

    for i in range(n):
        x_n = sig[i]
        x_prev = sig[i - 1] if i > 0 else 0.0
        x_next = sig[i + 1] if i < n - 1 else 0.0

        tkeo[i] = x_n * x_n - x_prev * x_next

    return tkeo

@njit
def EWMA(sig: np.ndarray, alpha: float = 0.1, phase_lag=False) -> np.ndarray:
   """
    Envelope detection using exponential decay with JIT compilation
    EWMA: Exponential Weighted Moving Average
    Phase lag: A phenomenon in which a signal is skewed slower than the original time
        False: Output after removing phase lag(delay)
        True: Output as is with delay
   """
   n = len(sig)
   envelope = np.zeros(n, dtype=np.float64)
   
   # Set first value
   first_val = sig[0]
   envelope[0] = first_val if first_val >= 0 else -first_val
   
   # Calculate remaining values
   for i in range(1, n):
       curr_val = sig[i]
       abs_val = curr_val if curr_val >= 0 else -curr_val
       envelope[i] = alpha * abs_val + (1 - alpha) * envelope[i-1]
   
   # Phase lag(delay) compensation
   if not phase_lag:
       # Reverse envelope calculation
       rev_envelope = np.zeros(n, dtype=np.float64)
       rev_sig = sig[::-1]  # signal reversal
       
       first_val = rev_sig[0]
       rev_envelope[0] = first_val if first_val >= 0 else -first_val
       
       for i in range(1, n):
           curr_val = rev_sig[i]
           abs_val = curr_val if curr_val >= 0 else -curr_val
           rev_envelope[i] = alpha * abs_val + (1 - alpha) * rev_envelope[i-1]
       
       # Convert the reverse envelope back to the forward direction and average it
       envelope = (envelope + rev_envelope[::-1]) / 2
   
   return envelope

def PT(x:np.ndarray, Rv=0.01):
    '''Phaser Transform'''
    return np.arctan(x/Rv)
import numpy as np
from matplotlib import pyplot as plt


def calculate_rr_intervals(rpeaks, sampling_rate=128):
    """R-피크 위치에서 RR 및 dRR 간격 계산"""
    rr_intervals = np.diff(rpeaks) * (1000 / sampling_rate)  # ms 단위 변환
    drr_intervals = np.diff(rr_intervals)  # dRR 계산
    return rr_intervals[:-1], drr_intervals  # 길이 맞춤

def create_rdr_map(rr_intervals, drr_intervals, bin_size=25):
    """RdR Map 생성 및 NEC (Non-Empty Cell) 계산"""
    rr_min, rr_max = min(rr_intervals), max(rr_intervals)
    drr_min, drr_max = min(drr_intervals), max(drr_intervals)

    rr_bins = np.arange(rr_min, rr_max + bin_size, bin_size)
    drr_bins = np.arange(drr_min, drr_max + bin_size, bin_size)
    hist, _, _ = np.histogram2d(rr_intervals, drr_intervals, bins=[rr_bins, drr_bins])

    nec_count = np.sum(hist > 0)  # NEC (Non-Empty Cell) 카운트
    return nec_count

def detect_af(nec_count, window_size):
    """NEC 카운트를 기반으로 AF 감지 (범위 기준)"""
    thresholds = {
        32: 20,
        64: 30,
        128: 40
    }

    # 해당 윈도우 크기에 맞는 임계값 범위 사용
    th = thresholds[window_size]
    return th <= nec_count

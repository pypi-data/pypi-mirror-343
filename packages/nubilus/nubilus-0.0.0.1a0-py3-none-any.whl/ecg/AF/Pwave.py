import numpy as np
from scipy.signal import butter, firwin, filtfilt

def detect_t_waves(ecg_signal, r_peaks, fs=250):
    """
    T wave detection function.
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    t_peaks : array
        Indices of the detected T wave peaks.
    """
    t_peaks = []
    
    for i in range(len(r_peaks)):
        # Calculate RR interval for the current beat
        if i < len(r_peaks) - 1:
            rr_interval = r_peaks[i+1] - r_peaks[i]
        else:
            # For the last beat, use the previous RR interval
            rr_interval = r_peaks[i] - r_peaks[i-1] if i > 0 else len(ecg_signal) - r_peaks[i]
        
        # Define search area for T wave: from R + 0.12*RR to R + 0.57*RR + 60ms
        start_idx = r_peaks[i] + int(0.12 * rr_interval)
        end_idx = min(r_peaks[i] + int(0.57 * rr_interval) + int(0.06 * fs), len(ecg_signal) - 1)
        
        if start_idx >= end_idx or start_idx < 0 or end_idx >= len(ecg_signal):
            continue
        
        # Apply phasor transform with RV = 0.1
        rv = 0.1
        search_segment = ecg_signal[start_idx:end_idx]
        phasor_transformed = np.arctan(search_segment / rv)
        
        # Find the maximum of the phase signal as T wave
        t_peak_local = np.argmax(phasor_transformed)
        t_peak = start_idx + t_peak_local
        
        t_peaks.append(t_peak)
    
    return np.array(t_peaks)

def detect_pvc(ecg_signal, r_peaks, fs=250):
    """
    PVC (Premature Ventricular Contraction) detection function.
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    pvc_labels : array
        Boolean array indicating if each beat is a PVC (True) or not (False).
    """
    # First, apply high-pass filter to remove baseline wander
    nyquist = fs / 2
    cutoff = 0.67 / nyquist
    b, a = butter(4, cutoff, 'high')
    filtered_ecg = filtfilt(b, a, ecg_signal)
    
    # Calculate area under the QRS complex for each beat
    auc_values = []
    for r_peak in r_peaks:
        start_idx = max(0, r_peak - int(0.15 * fs))  # 150 ms before R peak
        end_idx = min(len(filtered_ecg) - 1, r_peak + int(0.15 * fs))  # 150 ms after R peak
        
        # Calculate area under the curve (AUC)
        segment = filtered_ecg[start_idx:end_idx]
        auc = np.sum(np.abs(segment))
        auc_values.append(auc)
    
    auc_values = np.array(auc_values)
    
    # Determine if each beat is PVC based on the AUC threshold
    pvc_labels = np.zeros(len(r_peaks), dtype=bool)
    
    for i in range(len(r_peaks)):
        # Calculate the median AUC from all previous beats
        if i > 0:
            median_auc = np.median(auc_values[:i])
            # PVC detection: If AUC is 1.3 times larger than the median AUC
            if auc_values[i] > 1.3 * median_auc:
                pvc_labels[i] = True
    
    # Check if more than 75% of beats are labeled as PVC
    # If so, consider it a mistake (likely a bundle branch block)
    if np.mean(pvc_labels) > 0.75:
        pvc_labels[:] = False
    
    return pvc_labels

def detect_afib(ecg_signal, r_peaks, fs=250):
    """
    AFIB (Atrial Fibrillation) detection function.
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    afib_labels : array
        Boolean array indicating if each beat is during AFIB (True) or not (False).
    """
    # Calculate RR intervals
    rr_intervals = np.diff(r_peaks) / fs  # Convert to seconds
    
    # Prepare for symbolic dynamics
    afib_labels = np.zeros(len(r_peaks), dtype=bool)
    
    # Use a 3-symbol template to convert RR intervals to symbols
    # Calculate heart rate sequence from RR intervals
    hr_sequence = 60 / rr_intervals
    
    # Generate symbol sequence based on differences
    # (simplified version of the paper's symbolic dynamics approach)
    symbol_sequence = np.zeros(len(hr_sequence), dtype=int)
    for i in range(1, len(hr_sequence)):
        diff = hr_sequence[i] - hr_sequence[i-1]
        if diff > 10:  # Large increase
            symbol_sequence[i-1] = 2
        elif diff < -10:  # Large decrease
            symbol_sequence[i-1] = 0
        else:  # Small change
            symbol_sequence[i-1] = 1
    
    # Calculate Shannon entropy for segments (using a window of 59 beats)
    window_size = 59
    for i in range(len(r_peaks)):
        if i >= window_size//2 and i < len(symbol_sequence) - window_size//2:
            start_idx = i - window_size//2
            end_idx = i + window_size//2
            segment = symbol_sequence[start_idx:end_idx]
            
            # Calculate probabilities of symbols
            unique, counts = np.unique(segment, return_counts=True)
            probabilities = counts / len(segment)
            
            # Calculate Shannon entropy
            shannon_entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
            
            # If Shannon entropy is higher than threshold (0.737), mark as AFIB
            if shannon_entropy > 0.737:
                afib_labels[i] = True
    
    # Check if high entropy is due to PVCs
    # For simplicity, we'll use the PVC detection from above
    pvc_labels = detect_pvc(ecg_signal, r_peaks, fs)
    
    # If a segment has more than 30 PVCs in 59 consecutive beats, don't consider it AFIB
    for i in range(len(afib_labels)):
        if afib_labels[i]:
            if i >= window_size//2 and i < len(pvc_labels) - window_size//2:
                start_idx = i - window_size//2
                end_idx = i + window_size//2
                pvc_count = np.sum(pvc_labels[start_idx:end_idx])
                
                if pvc_count > 30:
                    afib_labels[i] = False
    
    return afib_labels

def check_pathology(pvc_labels, afib_labels):
    """
    Determine whether to search for P waves based on detected pathologies.
    
    Parameters:
    -----------
    pvc_labels : array
        Boolean array indicating if each beat is a PVC.
    afib_labels : array
        Boolean array indicating if each beat is during AFIB.
        
    Returns:
    --------
    search_p_wave : array
        Boolean array indicating whether to search for P waves for each beat.
    """
    # Create array to indicate whether to search for P waves
    search_p_wave = np.ones(len(pvc_labels), dtype=bool)
    
    # Don't search for P waves during AFIB or PVC
    for i in range(len(search_p_wave)):
        if afib_labels[i] or pvc_labels[i]:
            search_p_wave[i] = False
            
    return search_p_wave


def detect_normal_p_waves(ecg_signal, r_peaks, t_peaks, search_p_wave, fs=250):
    """
    Normal P wave detection function.
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    t_peaks : array
        Indices of the T wave peaks.
    search_p_wave : array
        Boolean array indicating whether to search for P waves for each beat.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    p_wave_candidates : array
        Indices of the P wave candidates.
    """
    p_wave_candidates = np.full(len(r_peaks), -1)  # Initialize with -1 (no P wave)
    
    for i in range(len(r_peaks)):
        if not search_p_wave[i]:
            continue
        
        # Define search area for P wave
        if i > 0:
            # From R(i-1) + 0.71*RR(i) to R(i) - 0.07*RR(i) - 60ms
            rr_interval = r_peaks[i] - r_peaks[i-1]
            start_idx = r_peaks[i-1] + int(0.71 * rr_interval)
            end_idx = max(start_idx + 1, r_peaks[i] - int(0.07 * rr_interval) - int(0.06 * fs))
        else:
            # For the first beat, use a fixed interval
            start_idx = max(0, r_peaks[i] - int(0.3 * fs))  # 300 ms before R peak
            end_idx = max(start_idx + 1, r_peaks[i] - int(0.08 * fs))  # 80 ms before R peak
            
        if start_idx >= end_idx or start_idx < 0 or end_idx >= len(ecg_signal):
            continue
            
        # Apply phasor transform with RV = 0.05
        rv = 0.05
        search_segment = ecg_signal[start_idx:end_idx]
        phasor_transformed = np.arctan(search_segment / rv)
        
        # Find the maximum of the phase signal as P wave
        p_wave_local = np.argmax(phasor_transformed)
        p_wave = start_idx + p_wave_local
        
        p_wave_candidates[i] = p_wave
    
    return p_wave_candidates


def detect_dissociated_p_waves(ecg_signal, r_peaks, t_peaks, p_wave_candidates, pvc_labels, fs=250):
    """
    Dissociated P wave detection function (for 2nd degree AV block).
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    t_peaks : array
        Indices of the T wave peaks.
    p_wave_candidates : array
        Indices of the P wave candidates from normal detection.
    pvc_labels : array
        Boolean array indicating if each beat is a PVC.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    p_wave_candidates : array
        Updated indices of the P wave candidates.
    """
    # For each beat, check if we need to look for dissociated P waves
    for i in range(1, len(r_peaks)):
        # Calculate RR intervals
        rr_current = r_peaks[i] - r_peaks[i-1]
        
        # Check if there is a dissociated P wave in the previous RR interval
        dissociated_p_in_prev = False
        if i > 1 and p_wave_candidates[i-1] != -1:
            # Complex logic to determine if previous wave was a dissociated P wave
            # For simplicity, we'll use a basic check
            prev_pr_interval = r_peaks[i-1] - p_wave_candidates[i-1]
            if prev_pr_interval > 0.3 * fs:  # If PR interval is long
                dissociated_p_in_prev = True
        
        search_for_dissociated = False
        
        if not dissociated_p_in_prev:
            # Criteria 1: RR(i) > 1.6*RR(i-1) and RR(i) > 1.6s and current beat is not PVC
            if i > 1:
                rr_prev = r_peaks[i-1] - r_peaks[i-2]
                if (rr_current > 1.6 * rr_prev and
                    rr_current > 1.6 * fs and
                    not pvc_labels[i]):
                    search_for_dissociated = True
        else:
            # Criteria 2: If dissociated P wave in previous interval, check RR(i) > 0.8*RR(i-1)
            rr_prev = r_peaks[i-1] - r_peaks[i-2] if i > 1 else rr_current
            if rr_current > 0.8 * rr_prev:
                search_for_dissociated = True
        
        if search_for_dissociated:
            # Define search area for dissociated P wave
            if i > 0 and i-1 < len(t_peaks):
                # From T(i-1) + 200ms to P(i) - 400ms
                t_idx = min(i-1, len(t_peaks)-1)
                if t_idx >= 0 and t_peaks[t_idx] > 0:
                    start_idx = t_peaks[t_idx] + int(0.2 * fs)
                    
                    if p_wave_candidates[i] > 0:
                        end_idx = p_wave_candidates[i] - int(0.4 * fs)
                    else:
                        end_idx = r_peaks[i] - int(0.4 * fs)
                    
                    if start_idx < end_idx and start_idx >= 0 and end_idx < len(ecg_signal):
                        # Apply phasor transform with RV = 0.05
                        rv = 0.05
                        search_segment = ecg_signal[start_idx:end_idx]
                        phasor_transformed = np.arctan(search_segment / rv)
                        
                        # Find the maximum of the phase signal as P wave
                        p_wave_local = np.argmax(phasor_transformed)
                        dissociated_p_wave = start_idx + p_wave_local
                        
                        # Add this as an additional P wave (could be stored differently in a real implementation)
                        # For simplicity, we'll update the existing candidate if it was -1
                        if p_wave_candidates[i] == -1:
                            p_wave_candidates[i] = dissociated_p_wave
    
    return p_wave_candidates


def verify_p_waves(ecg_signal, r_peaks, t_peaks, p_wave_candidates, fs=250):
    """
    Verify P wave candidates.
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    t_peaks : array
        Indices of the T wave peaks.
    p_wave_candidates : array
        Indices of the P wave candidates.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    p_peaks : array
        Indices of the verified P wave peaks.
    """
    p_peaks = []
    
    for i in range(len(r_peaks)):
        if p_wave_candidates[i] == -1:
            continue
        
        # Check amplitude criterion: UP(i) > 0.05*UQRS(i)
        if p_wave_candidates[i] >= 0 and p_wave_candidates[i] < len(ecg_signal):
            p_amplitude = abs(ecg_signal[p_wave_candidates[i]])
            r_amplitude = abs(ecg_signal[r_peaks[i]])
            
            if p_amplitude < 0.05 * r_amplitude:
                continue
            
            # Check position criterion: P wave should be after previous T wave
            if i > 0 and i-1 < len(t_peaks) and t_peaks[i-1] >= 0:
                if p_wave_candidates[i] <= t_peaks[i-1]:
                    continue
            
            p_peaks.append(p_wave_candidates[i])
    
    return np.array(p_peaks)


def detect_p_waves(ecg_signal, r_peaks, fs=250):
    """
    Complete P wave detection pipeline.
    
    Parameters:
    -----------
    ecg_signal : array
        The ECG signal.
    r_peaks : array
        Indices of the R peaks.
    fs : int, optional
        Sampling frequency in Hz. Default is 250 Hz.
        
    Returns:
    --------
    p_peaks : array
        Indices of the detected P wave peaks.
    """
    # Step 1: Detect T waves
    t_peaks = detect_t_waves(ecg_signal, r_peaks, fs)
    
    # Step 2: Detect PVC
    pvc_labels = detect_pvc(ecg_signal, r_peaks, fs)
    
    # Step 3: Detect AFIB
    afib_labels = detect_afib(ecg_signal, r_peaks, fs)
    
    # Step 4: Check pathology
    search_p_wave = check_pathology(pvc_labels, afib_labels)
    
    # Step 5: Detect normal P waves
    p_wave_candidates = detect_normal_p_waves(ecg_signal, r_peaks, t_peaks, search_p_wave, fs)
    
    # Step 6: Detect dissociated P waves
    p_wave_candidates = detect_dissociated_p_waves(ecg_signal, r_peaks, t_peaks, p_wave_candidates, pvc_labels, fs)
    
    # Step 7: Verify P waves
    p_peaks = verify_p_waves(ecg_signal, r_peaks, t_peaks, p_wave_candidates, fs)
    
    return p_peaks
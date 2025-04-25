import torch
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

def ndarray2tensor(arr, device='cpu'):
    if isinstance(arr, torch.Tensor):
        return arr.to(device)
    elif isinstance(arr, np.ndarray):
        return torch.tensor(arr, device=device)
    else:
        raise TypeError("입력은 torch.Tensor, list 또는 tuple이어야 합니다.")

# Prediction 변환 (이진 + 다중 클래스)
def _process_predictions(y_pred, threshold=0.5):
    if y_pred.dim() == 1:
        y_pred = y_pred.unsqueeze(1)
        return (y_pred > threshold).int()

    elif y_pred.dim() == 2:
        if y_pred.size(1) == 1:
            return (y_pred > threshold).int()

        elif y_pred.size(1) >= 2:
            max_indices = torch.argmax(y_pred, dim=1).unsqueeze(1)
            one_hot = torch.zeros_like(y_pred).scatter_(1, max_indices, 1)
            return one_hot.int()

    else:
        raise ValueError("y_pred는 1차원 또는 2차원 텐서여야 합니다.")

# Confusion Matrix 생성 (벡터화 연산 기반)
def confusion_matrix(y_true, y_pred, threshold=0.5):
    # 원-핫 벡터를 정수 레이블로 변환
    if y_true.dim() == 2:
        y_true = _process_predictions(y_true, threshold)
        y_true = torch.argmax(y_true, dim=1)
    if y_pred.dim() == 2:
        y_pred = _process_predictions(y_pred, threshold)
        y_pred = torch.argmax(y_pred, dim=1)

    # 클래스 수 자동 탐지
    num_classes = max(y_true.max().item(), y_pred.max().item()) + 1

    # Confusion Matrix 생성
    conf_matrix = torch.zeros((num_classes, num_classes), dtype=torch.int64, device=y_true.device)

    for t, p in zip(y_true, y_pred):
        conf_matrix[t, p] += 1

    return conf_matrix


class Accuracy:
    def __init__(self, threshold=0.5, device='cpu'):
        self.threshold=threshold
        self.device=device
    
    def __call__(self, y_true, y_pred):
        # 텐서 변환
        y_true_tensor = ndarray2tensor(y_true, self.device).int()
        y_pred_tensor = ndarray2tensor(y_pred, self.device)
        
        # Confusion Matrix 생성
        conf_matrix = confusion_matrix(y_true_tensor, y_pred_tensor, self.threshold)

        # 정확도 계산
        total = conf_matrix.sum().item()    # 전체 샘플 수
        correct = torch.trace(conf_matrix).item()  # 대각선 합 (True Predictions)

        # 정확도 반환
        return correct / total if total > 0 else 0.0

class Precision:
    def __init__(self, threshold=0.5, device='cpu'):
        self.threshold=threshold
        self.device=device
    
    def __call__(self, y_true, y_pred):
        # 텐서 변환
        y_true_tensor = ndarray2tensor(y_true, self.device)
        y_pred_tensor = ndarray2tensor(y_pred, self.device)
        
        # Confusion Matrix 생성
        conf_matrix = confusion_matrix(y_true_tensor, y_pred_tensor, self.threshold)
        
        # 이진 분류 (2x2 행렬)
        if conf_matrix.size(0) == 2:
            TP = conf_matrix[1, 1].item()
            FP = conf_matrix[0, 1].item()

            # Precision 계산
            precision_value = TP / (TP + FP) if (TP + FP) != 0 else 0.0
        
        # 다중 클래스 (N x N 행렬)
        else:
            TP_per_class = torch.diag(conf_matrix)
            FP_per_class = conf_matrix.sum(dim=0) - TP_per_class
            
            # 클래스별 Precision 평균 (Macro-averaged Precision)
            precision_value = (TP_per_class / (TP_per_class + FP_per_class).clamp(min=1e-9)).mean().item()

        return precision_value

class Sensitivity:
    def __init__(self, threshold=0.5, device='cpu'):
        self.threshold=threshold
        self.device=device
    
    def __call__(self, y_true, y_pred):
    # 텐서 변환
        y_true_tensor = ndarray2tensor(y_true, self.device)
        y_pred_tensor = ndarray2tensor(y_pred, self.device)
        
        # Confusion Matrix 생성
        conf_matrix = confusion_matrix(y_true_tensor, y_pred_tensor, self.threshold)
        
        # 이진 분류 (2x2 행렬)
        if conf_matrix.size(0) == 2:
            TP = conf_matrix[1, 1].item()
            FN = conf_matrix[1, 0].item()

            # Sensitivity 계산
            sensitivity_value = TP / (TP + FN) if (TP + FN) != 0 else 0.0
        
        # 다중 클래스 (N x N 행렬)
        else:
            TP_per_class = torch.diag(conf_matrix)
            FN_per_class = conf_matrix.sum(dim=1) - TP_per_class
            
            # 클래스별 Sensitivity 평균 (Macro-averaged Sensitivity)
            sensitivity_value = (TP_per_class / (TP_per_class + FN_per_class).clamp(min=1e-9)).mean().item()

        return sensitivity_value


class Specificity:
    def __init__(self, threshold=0.5, device='cpu'):
        self.threshold=threshold
        self.device=device
    
    def __call__(self, y_true, y_pred):
        # 텐서 변환
        y_true_tensor = ndarray2tensor(y_true, self.device)
        y_pred_tensor = ndarray2tensor(y_pred, self.device)
        
        # Confusion Matrix 생성
        conf_matrix = confusion_matrix(y_true_tensor, y_pred_tensor, self.threshold)
        
        # 이진 분류 (2x2 행렬)
        if conf_matrix.size(0) == 2:
            TN = conf_matrix[0, 0].item()
            FP = conf_matrix[0, 1].item()

            # Specificity 계산
            specificity_value = TN / (TN + FP) if (TN + FP) != 0 else 0.0
        
        # 다중 클래스 (N x N 행렬)
        else:
            TN_per_class = conf_matrix.sum() - conf_matrix.sum(dim=0) - conf_matrix.sum(dim=1) + torch.diag(conf_matrix)
            FP_per_class = conf_matrix.sum(dim=0) - torch.diag(conf_matrix)
            
            # 클래스별 Specificity 평균 (Macro-averaged Specificity)
            specificity_value = (TN_per_class / (TN_per_class + FP_per_class).clamp(min=1e-9)).mean().item()

        return specificity_value

class F1Score:
    def __init__(self, threshold=0.5, average='macro',device='cpu'):
        self.threshold=threshold
        self.device=device
        self.average=average
        
    def __call__(self, y_true, y_pred):
        # 텐서 변환
        y_true_tensor = ndarray2tensor(y_true, self.device)
        y_pred_tensor = ndarray2tensor(y_pred, self.device)
        
        # Confusion Matrix 생성
        conf_matrix = confusion_matrix(y_true_tensor, y_pred_tensor, self.threshold)

        # 이진 분류 (2x2 행렬)
        if conf_matrix.size(0) == 2:
            TP = conf_matrix[1, 1].item()
            FP = conf_matrix[0, 1].item()
            FN = conf_matrix[1, 0].item()

            precision = TP / (TP + FP) if (TP + FP) != 0 else 0.0
            recall = TP / (TP + FN) if (TP + FN) != 0 else 0.0

            # F1 Score 계산
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0.0
        
        # 다중 클래스 (N x N 행렬)
        else:
            TP_per_class = torch.diag(conf_matrix)
            FP_per_class = conf_matrix.sum(dim=0) - TP_per_class
            FN_per_class = conf_matrix.sum(dim=1) - TP_per_class

            precision = TP_per_class / (TP_per_class + FP_per_class).clamp(min=1e-9)
            recall = TP_per_class / (TP_per_class + FN_per_class).clamp(min=1e-9)

            # F1 Score per class
            f1_per_class = 2 * (precision * recall) / (precision + recall).clamp(min=1e-9)

            # Macro F1 (평균)
            if self.average == 'macro':
                f1 = f1_per_class.mean().item()

            # Weighted F1 (샘플 수 비율 기반)
            elif self.average == 'weighted':
                class_counts = conf_matrix.sum(dim=1)  # 각 클래스의 샘플 수
                f1 = (f1_per_class * class_counts / class_counts.sum()).sum().item()

            else:
                raise ValueError("average must be 'macro' or 'weighted'")

        return f1

class AUC:
    def __init__(self, threshold=0.5, average='macro',device='cpu'):
        self.threshold=threshold
        self.device=device
        self.average=average
    
    def __call__(self, y_true, y_pred):
        # PyTorch tensor를 NumPy 배열로 변환
        if isinstance(y_true, torch.Tensor):
            y_true = y_true.detach().cpu().numpy()
        if isinstance(y_pred, torch.Tensor):
            y_pred = y_pred.detach().cpu().numpy()

        # 입력이 1차원인 경우 처리 (Binary Classification)
        if y_true.ndim == 1:
            return roc_auc_score(y_true, y_pred)

        # 입력이 2차원인 경우 처리 (Multi-class Classification)
        elif y_true.ndim == 2:
            if y_true.shape[1] == 1 or y_pred.shape[1] == 1:  # Binary Classification 형태
                return roc_auc_score(y_true.ravel(), y_pred.ravel())
            else:  # Multi-class Classification (One-vs-Rest 방식)
                return roc_auc_score(y_true, y_pred, average=self.average, multi_class='ovr')

        # 지원되지 않는 차원의 경우 예외 처리
        else:
            raise ValueError("Input dimensions not supported. Only 1D or 2D tensors/arrays are accepted.")



class PRAUC:
    def __init__(self, threshold=0.5, average='macro',device='cpu'):
        self.threshold=threshold
        self.device=device
        self.average=average
    
    def __call__(self, y_true, y_pred):
        if isinstance(y_true, torch.Tensor):
            y_true = y_true.detach().cpu().numpy()
        if isinstance(y_pred, torch.Tensor):
            y_pred = y_pred.detach().cpu().numpy()

        # 입력이 1차원인 경우 처리 (Binary Classification)
        if y_true.ndim == 1:
            return average_precision_score(y_true, y_pred)

        # 입력이 2차원인 경우 처리 (Multi-class Classification)
        elif y_true.ndim == 2:
            if y_true.shape[1] == 1 or y_pred.shape[1] == 1:  # Binary Classification 형태
                return average_precision_score(y_true.ravel(), y_pred.ravel())
            else:  # Multi-class Classification (One-vs-Rest 방식)
                return average_precision_score(y_true, y_pred, average=self.average)

        # 지원되지 않는 차원의 경우 예외 처리
        else:
            raise ValueError("Input dimensions not supported. Only 1D or 2D tensors/arrays are accepted.")
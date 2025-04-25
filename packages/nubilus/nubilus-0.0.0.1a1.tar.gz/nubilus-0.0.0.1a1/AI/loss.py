import torch
import torch.nn as nn
import torch.nn.functional as F
from torchmetrics import Accuracy, AUROC, PrecisionRecallCurve, FBetaScore

class AccuracyLoss:
    def __init__(self, device='cpu'):
        self.device = device

    def __call__(self, y_true, y_pred):
        num_classes = 1 if y_pred.ndim == 1 else y_pred.shape[1]
        acc = Accuracy(task='binary' if num_classes == 1 else 'multiclass', num_classes=num_classes).to(self.device)
        y_pred = torch.sigmoid(y_pred) if num_classes == 1 else F.softmax(y_pred, dim=1)
        return 1.0 - acc(y_pred, y_true)

class AUCLoss:
    def __init__(self, device='cpu'):
        self.device = device

    def __call__(self, y_true, y_pred):
        num_classes = 1 if y_pred.ndim == 1 else y_pred.shape[1]
        auc = AUROC(task='binary' if num_classes == 1 else 'multiclass', num_classes=num_classes).to(self.device)
        y_pred = torch.sigmoid(y_pred) if num_classes == 1 else F.softmax(y_pred, dim=1)
        return 1.0 - auc(y_pred, y_true)

class PRAUCLoss:
    def __init__(self, device='cpu'):
        self.device = device

    def __call__(self, y_true, y_pred):
        num_classes = 1 if y_pred.ndim == 1 else y_pred.shape[1]
        pr_curve = PrecisionRecallCurve(task='binary' if num_classes == 1 else 'multiclass', num_classes=num_classes).to(self.device)
        y_pred = torch.sigmoid(y_pred) if num_classes == 1 else F.softmax(y_pred, dim=1)
        precision, recall, _ = pr_curve(y_pred, y_true)
        precision = torch.cat(precision)
        recall = torch.cat(recall)
        pr_auc = torch.trapz(precision, recall)
        return 1.0 - pr_auc

class FBetaLoss(nn.Module):
    def __init__(self, beta=1.0, device='cpu'):
        super(FBetaLoss, self).__init__()
        self.beta = beta
        self.fbeta = None  # 초기화는 forward에서 수행
        self.device = device
    def forward(self, y_true, y_pred):
        # 클래스 수 강제 설정
        # num_classes = torch.max(y_true).item() + 1
        num_classes = int(torch.max(y_true).item()) + 1
        
        # FBetaScore 초기화
        if self.fbeta is None:
            self.fbeta = FBetaScore(task='binary' if num_classes == 2 else 'multiclass', 
                                    num_classes=num_classes, beta=self.beta).to(self.device)
        
        # 확률 변환
        if num_classes == 2:
            # Binary Classification (이진 분류) → 1차원 확률값으로 변환
            y_pred = torch.sigmoid(y_pred)[:, 1]
        else:
            # Multi-class Classification (다중 클래스) → 2차원 확률값으로 유지
            y_pred = F.softmax(y_pred, dim=1)


        # y_true가 2차원 (one-hot)인 경우 정수형 레이블로 변환
        if y_true.ndim == 2 and y_true.shape[1] == num_classes:

            y_true = torch.argmax(y_true, dim=1)

        # 다중 클래스일 경우 y_true를 one-hot으로 변환 (FBetaScore 요구사항)
        if num_classes > 2:
            y_true = F.one_hot(y_true, num_classes).float()

        # y_true 차원 정리 (squeeze 적용)
        y_true = y_true.squeeze()

        # 최종 형태 확인

        # FBetaScore 계산
        try:
            result = 1.0 - self.fbeta(y_pred, y_true)

            return result
        except Exception as e:
            print(f"Error during FBeta calculation: {e}")
            raise e

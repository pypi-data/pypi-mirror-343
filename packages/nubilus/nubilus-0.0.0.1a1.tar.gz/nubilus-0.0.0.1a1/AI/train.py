import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import time
import os
import numpy as np
from AI.utils import mkdir
from AI.metrics import Accuracy


class Trainer:
    def __init__(self, model, loss, optimizer, metrics=[Accuracy()], device='cpu', save_folder:str='./result'):
        self.device = device
        self.model = model.to(self.device)
        self.loss = loss.to(self.device)
        self.optimizer = optimizer
        try:
            _ = len(metrics)
            self.metrics = list(metrics)
        except:
            self.metrics = [metrics]

        self.save_folder = save_folder
        mkdir(self.save_folder)

    def _convert_to_loader(self, data, batch_size):
        if (isinstance(data, tuple) or isinstance(data, list)) and len(data) == 2:  # (x, y) 튜플 형식
            x, y = data
            if isinstance(x, np.ndarray):
                x = torch.tensor(x, dtype=torch.float32)
            if isinstance(y, np.ndarray):
                y = torch.tensor(y, dtype=torch.float32)
            dataset = TensorDataset(x, y)
            return DataLoader(dataset, batch_size=batch_size, shuffle=True)
        return data

    def fit(self, train_set, valid_set=None, test_set=None, batch_size=1, epochs=10):
        train_loader = self._convert_to_loader(train_set, batch_size)
        valid_loader = self._convert_to_loader(valid_set, batch_size) if valid_set is not None else None
        test_loader = self._convert_to_loader(test_set, batch_size) if test_set is not None else None

        history = {
            'train': {'loss': [], **{m.__class__.__name__: [] for m in self.metrics}},
            'valid': {'loss': [], **{m.__class__.__name__: [] for m in self.metrics}} if valid_loader else None,
            'test': {'loss': [], **{m.__class__.__name__: [] for m in self.metrics}} if test_loader else None,
        }

        best_epoch = 0
        best_valid_loss = float('inf')
        start_time = time.time()

        for epoch in range(1, epochs + 1):
            train_results = self._train_epoch(train_loader)
            for key, value in train_results.items():
                history['train'][key].append(value)

            if valid_loader:
                valid_results = self._valid_epoch(valid_loader)
                for key, value in valid_results.items():
                    history['valid'][key].append(value)

                # Best Model Save
                if valid_results['loss'] < best_valid_loss:
                    best_valid_loss = valid_results['loss']
                    best_epoch = epoch
                    torch.save(self.model.state_dict(), os.path.join(self.save_folder, 'best_model.pth'))

            # Last Model Save
            torch.save(self.model.state_dict(), os.path.join(self.save_folder, 'last_model.pth'))

            # Print Logs
            print(f"Epoch [{epoch}/{epochs}]\nTrain - Loss: {train_results['loss']:.4f} - " +
                  " - ".join([f"{metric}: {train_results[metric]:.4f}" for metric in history['train'] if metric != 'loss']))

            if valid_loader:
                print(f"			Valid - Loss: {valid_results['loss']:.4f} - " +
                      " - ".join([f"{metric}: {valid_results[metric]:.4f}" for metric in history['valid'] if metric != 'loss']))

        if test_loader:
            test_results = self._valid_epoch(test_loader)
            for key, value in test_results.items():
                history['test'][key].append(value)

        return history

    def _train_epoch(self, train_loader):
        self.model.train()
        total_loss = 0.0
        metric_sums = {metric.__class__.__name__: 0.0 for metric in self.metrics}
        total_batches = 0

        for batch_x, batch_y in tqdm(train_loader, desc="Training", leave=False):
            batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model(batch_x)
            loss_value = self.loss(outputs, batch_y)
            loss_value.backward()
            self.optimizer.step()

            total_loss += loss_value.item()
            for metric in self.metrics:
                metric_sums[metric.__class__.__name__] += metric(outputs, batch_y)#.item()
            total_batches += 1

        avg_loss = total_loss / total_batches
        avg_metrics = {metric: metric_sums[metric] / total_batches for metric in metric_sums}

        return {'loss': avg_loss, **avg_metrics}

    def _valid_epoch(self, valid_loader):
        self.model.eval()
        total_loss = 0.0
        metric_sums = {metric.__class__.__name__: 0.0 for metric in self.metrics}
        total_batches = 0

        with torch.no_grad():
            for batch_x, batch_y in tqdm(valid_loader, desc="Validation", leave=False):
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                outputs = self.model(batch_x)
                loss_value = self.loss(outputs, batch_y)

                total_loss += loss_value.item()
                for metric in self.metrics:
                    metric_sums[metric.__class__.__name__] += metric(outputs, batch_y).item()
                total_batches += 1

        avg_loss = total_loss / total_batches
        avg_metrics = {metric: metric_sums[metric] / total_batches for metric in metric_sums}

        return {'loss': avg_loss, **avg_metrics}
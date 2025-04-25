"""
PyTorch GPU 진단 및 테스트 라이브러리
- 시스템 환경(CPU, GPU) 정보 확인
- 모든/가용/활성 디바이스 정보 제공
- 간단한 모델 학습을 통한 GPU 작동 여부 검사

변수 및 함수:
- DEVICES: 모든 디바이스 목록 (변경되지 않음)
- get_available_devices(): 현재 사용 가능한 디바이스 목록 반환
- get_active_devices(): 현재 활성화된 디바이스 목록 반환
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import platform
import subprocess
import os
import sys
from typing import Dict, List, Union, Tuple, Optional
import json
from IPython.display import clear_output


class DeviceInfo:
    """시스템의 CPU 및 GPU 정보를 수집하는 클래스"""
    
    # 모든 디바이스 리스트 (CPU + GPU) - 한 번만 초기화
    DEVICES = []
    
    @classmethod
    def initialize_devices(cls):
        """모든 디바이스 리스트를 초기화합니다. (한 번만 실행)"""
        if cls.DEVICES:  # 이미 초기화되었으면 다시 하지 않음
            return cls.DEVICES
            
        cls.DEVICES = []
        
        # CPU 추가
        cpu_info = {
            "name": "cpu", 
            "type": "CPU", 
            "device": torch.device("cpu"),
            "status": "available"
        }
        cls.DEVICES.append(cpu_info)
        
        # GPU 추가 (사용 가능한 경우)
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                # GPU 상태 확인 시도
                try:
                    # 간단한 연산으로 GPU 작동 여부 확인
                    with torch.cuda.device(i):
                        test_tensor = torch.ones(1, device=f'cuda:{i}')
                        _ = test_tensor * 2
                        # 테스트 후 메모리 해제
                        del test_tensor
                        torch.cuda.empty_cache()
                    
                    status = "available"
                    
                except Exception as e:
                    status = "unavailable"
                    error = str(e)
                
                device_info = {
                    "name": f"cuda:{i}",
                    "type": "GPU",
                    "device": torch.device(f"cuda:{i}"),
                    "gpu_name": torch.cuda.get_device_name(i),
                    "status": status
                }
                
                if status == "unavailable":
                    device_info["error"] = error
                    
                cls.DEVICES.append(device_info)
        
        return cls.DEVICES
    
    @classmethod
    def get_devices(cls) -> List[Dict]:
        """모든 디바이스 목록을 반환합니다."""
        if not cls.DEVICES:
            cls.initialize_devices()
        return cls.DEVICES
    
    @classmethod
    def get_available_devices(cls) -> List[Dict]:
        """현재 사용 가능한 디바이스 목록을 반환합니다."""
        devices = cls.get_devices()
        return [d for d in devices if d.get('status') == 'available']
    
    @classmethod
    def get_active_devices(cls) -> List[Dict]:
        """현재 사용 중인 디바이스 목록을 실시간으로 확인하여 반환합니다."""
        devices = cls.get_devices()
        active_devices = []
        
        # CPU는 항상 활성화된 것으로 간주
        cpu_device = next((d for d in devices if d['type'] == 'CPU'), None)
        if cpu_device:
            active_devices.append(cpu_device)
        
        # GPU 상태 실시간 확인
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                # 현재 메모리 사용량 확인
                try:
                    memory_allocated = torch.cuda.memory_allocated(i)
                    memory_reserved = torch.cuda.memory_reserved(i)
                    
                    # 메모리가 할당되어 있으면 활성 상태
                    if memory_allocated > 0:
                        device = next((d for d in devices if d['name'] == f'cuda:{i}'), None)
                        if device:
                            # 깊은 복사로 원본 디바이스 정보를 수정하지 않음
                            active_device = device.copy()
                            # 현재 메모리 정보 추가
                            active_device.update({
                                "memory_allocated_gb": memory_allocated / (1024**3),
                                "memory_reserved_gb": memory_reserved / (1024**3)
                            })
                            active_devices.append(active_device)
                except Exception:
                    # 예외가 발생하면 해당 GPU는 활성 상태가 아님
                    pass
        
        return active_devices
    
    @staticmethod
    def get_cpu_info() -> Dict[str, str]:
        """CPU 관련 정보를 반환합니다."""
        cpu_info = {}
        
        # 운영체제 정보
        cpu_info['os'] = f"{platform.system()} {platform.release()}"
        
        # Python 및 PyTorch 버전
        cpu_info['python_version'] = sys.version.split()[0]
        cpu_info['pytorch_version'] = torch.__version__
        
        # CPU 정보 (Linux 시스템용)
        if platform.system() == "Linux":
            try:
                cpu_details = subprocess.check_output('lscpu', shell=True).decode('utf-8')
                for line in cpu_details.split('\n'):
                    if "Model name" in line:
                        cpu_info['model'] = line.split(':')[1].strip()
                    if "CPU(s)" in line and "NUMA" not in line and "On-line" not in line:
                        cpu_info['cores'] = line.split(':')[1].strip()
            except:
                cpu_info['model'] = platform.processor()
        else:
            cpu_info['model'] = platform.processor()
            
        # PyTorch 스레드 정보
        cpu_info['pytorch_threads'] = str(torch.get_num_threads())
        
        return cpu_info
    
    @staticmethod
    def get_gpu_info() -> List[Dict[str, Union[str, int, float, bool]]]:
        """GPU 관련 정보를 실시간으로 조회하여 반환합니다."""
        result = []
        
        if not torch.cuda.is_available():
            return [{"error": "CUDA not available"}]
        
        # 기본 CUDA 정보
        result.append({
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda,
            "device_count": torch.cuda.device_count(),
            "current_device": torch.cuda.current_device()
        })
        
        # 각 GPU 정보 (실시간)
        for i in range(torch.cuda.device_count()):
            gpu_info = {
                "device_index": i,
                "device_name": torch.cuda.get_device_name(i)
            }
            
            # 메모리 정보 (GB 단위) - 실시간 조회
            gpu_info["memory_allocated_gb"] = torch.cuda.memory_allocated(i) / (1024**3)
            gpu_info["memory_reserved_gb"] = torch.cuda.memory_reserved(i) / (1024**3)
            
            # 컴퓨트 능력 (Compute Capability)
            major, minor = torch.cuda.get_device_capability(i)
            gpu_info["compute_capability"] = f"{major}.{minor}"
            
            result.append(gpu_info)
        
        return result
    
    @staticmethod
    def get_all_info() -> Dict[str, Union[Dict, List]]:
        """CPU 및 GPU 정보를 모두 실시간으로 반환합니다."""
        return {
            "cpu": DeviceInfo.get_cpu_info(),
            "gpu": DeviceInfo.get_gpu_info()
        }
    
    @staticmethod
    def print_info() -> None:
        """시스템 정보를 포맷팅하여 출력합니다."""
        info = DeviceInfo.get_all_info()
        
        print("=" * 50)
        print("CPU Information:")
        print("=" * 50)
        for key, value in info["cpu"].items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("\n" + "=" * 50)
        print("GPU Information:")
        print("=" * 50)
        
        for i, gpu in enumerate(info["gpu"]):
            if i == 0:  # 첫 번째는 CUDA 기본 정보
                print("CUDA Information:")
                for key, value in gpu.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
                print("-" * 50)
            else:
                print(f"GPU {gpu.get('device_index', i-1)} Information:")
                for key, value in gpu.items():
                    if key != "device_index":  # 이미 출력한 정보는 건너뜀
                        if key.endswith('_gb'):
                            print(f"{key.replace('_', ' ').title()}: {value:.2f} GB")
                        else:
                            print(f"{key.replace('_', ' ').title()}: {value}")
                if i < len(info["gpu"]) - 1:
                    print("-" * 50)
    
    @staticmethod
    def print_all_devices() -> None:
        """모든 디바이스 목록을 출력합니다."""
        devices = DeviceInfo.get_devices()
        
        print("=" * 50)
        print(f"모든 디바이스 목록 (총 {len(devices)}개):")
        print("=" * 50)
        
        for i, device in enumerate(devices):
            status_str = f"[{device.get('status', '알 수 없음')}]"
            print(f"{i+1}. {device['name']} ({device['type']}) {status_str}", end="")
            if device['type'] == "GPU":
                print(f" - {device['gpu_name']}")
            else:
                print()
    
    @staticmethod
    def print_available_devices() -> None:
        """사용 가능한 디바이스 목록을 출력합니다."""
        devices = DeviceInfo.get_available_devices()
        
        print("=" * 50)
        print(f"사용 가능한 디바이스 목록 (총 {len(devices)}개):")
        print("=" * 50)
        
        for i, device in enumerate(devices):
            print(f"{i+1}. {device['name']} ({device['type']})", end="")
            if device['type'] == "GPU":
                print(f" - {device['gpu_name']}")
            else:
                print()
    
    @staticmethod
    def print_active_devices() -> None:
        """현재 사용 중인 디바이스 목록을 출력합니다."""
        devices = DeviceInfo.get_active_devices()
        
        print("=" * 50)
        print(f"현재 사용 중인 디바이스 목록 (총 {len(devices)}개):")
        print("=" * 50)
        
        for i, device in enumerate(devices):
            print(f"{i+1}. {device['name']} ({device['type']})", end="")
            if device['type'] == "GPU":
                memory_allocated = device.get('memory_allocated_gb', 0)
                memory_reserved = device.get('memory_reserved_gb', 0)
                print(f" - {device['gpu_name']}")
                print(f"   할당된 메모리: {memory_allocated:.2f} GB")
                print(f"   예약된 메모리: {memory_reserved:.2f} GB")
            else:
                print()


class SimpleCNN(nn.Module):
    """간단한 MNIST용 CNN 모델"""
    
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc = nn.Linear(14 * 14 * 8, 10)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


class GPUChecker:
    """GPU 기능 검사를 위한 클래스"""
    
    @staticmethod
    def check_gpu(batch_limit: int = 1, clear_screen: bool = False) -> Tuple[bool, Optional[str]]:
        """
        GPU 작동 여부를 검사합니다.
        
        Args:
            batch_limit: 테스트할 배치 수 (기본값: 1)
            clear_screen: 진행 상태를 출력할 때 화면을 지울지 여부
            
        Returns:
            (성공 여부, 오류 메시지(있는 경우))
        """
        if not torch.cuda.is_available():
            return False, "CUDA is not available"
        
        device = torch.device("cuda")
        print(f"PyTorch 사용 디바이스: {device}")
        
        try:
            # 모델 준비
            model = SimpleCNN().to(device)
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            criterion = nn.CrossEntropyLoss()

            # 데이터 준비
            transform = transforms.ToTensor()
            train_loader = DataLoader(
                datasets.MNIST('.', train=True, download=True, transform=transform),
                batch_size=64, shuffle=True
            )

            # 테스트 학습 실행
            model.train()
            for batch_idx, (data, target) in enumerate(train_loader):
                if batch_idx >= batch_limit:
                    break
                    
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                if clear_screen:
                    clear_output(wait=True)
                
                print(f"배치 {batch_idx+1}/{batch_limit} 처리 완료 - Loss: {loss.item():.4f}")
                
                # 현재 GPU 상태 출력
                for i in range(torch.cuda.device_count()):
                    allocated = torch.cuda.memory_allocated(i) / (1024**3)
                    reserved = torch.cuda.memory_reserved(i) / (1024**3)
                    print(f"GPU {i} 메모리 - 할당: {allocated:.2f} GB, 예약: {reserved:.2f} GB")
            
            return True, None
            
        except Exception as e:
            return False, str(e)


def check_gpu(clear_screen: bool = False):
    """
    PyTorch GPU 정보를 확인하고 간단한 모델 학습을 통해 GPU 작동 여부를 검사합니다.
    
    Args:
        clear_screen: 진행 상태를 출력할 때 화면을 지울지 여부
    """
    # 모든 디바이스 목록 출력
    DeviceInfo.print_all_devices()
    
    # 사용 가능한 디바이스 목록 출력
    DeviceInfo.print_available_devices()
    
    # 현재 사용 중인 디바이스 목록 출력
    DeviceInfo.print_active_devices()
    
    # 시스템 정보 출력
    DeviceInfo.print_info()
    
    # GPU 사용 가능 여부 확인
    if not torch.cuda.is_available():
        print("\n⚠️ GPU를 사용할 수 없습니다. CPU만 사용 가능합니다.")
        return
    
    print("\n" + "=" * 50)
    print("GPU 작동 테스트 (MNIST 데이터셋):")
    print("=" * 50)
    
    # GPU 작동 테스트
    success, error = GPUChecker.check_gpu(batch_limit=1, clear_screen=clear_screen)
    
    # 테스트 후 활성 디바이스 출력
    print("\n현재 활성 디바이스 상태:")
    DeviceInfo.print_active_devices()
    
    if success:
        print("\n✅ GPU 테스트 성공! PyTorch가 GPU에서 정상적으로 작동합니다.")
    else:
        print(f"\n❌ GPU 테스트 실패: {error}")
        print("PyTorch가 GPU를 인식했지만 연산 중 오류가 발생했습니다.")


# 디바이스 목록 초기화 (DEVICES만 전역 변수로 유지)
DeviceInfo.initialize_devices()
DEVICES = DeviceInfo.DEVICES

# 함수로 제공 (실시간 상태 반영)
def available_devices():
    """사용 가능한 디바이스 목록을 반환합니다."""
    return DeviceInfo.get_available_devices()

def active_devices():
    """현재 활성화된 디바이스 목록을 반환합니다."""
    return DeviceInfo.get_active_devices()
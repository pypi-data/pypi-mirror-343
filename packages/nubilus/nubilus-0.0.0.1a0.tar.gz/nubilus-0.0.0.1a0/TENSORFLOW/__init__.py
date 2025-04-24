"""
TensorFlow GPU 진단 및 테스트 라이브러리
- 시스템 환경(CPU, GPU) 정보 확인
- 모든/가용/활성 디바이스 정보 제공
- 간단한 모델 학습을 통한 GPU 작동 여부 검사

변수 및 함수:
- DEVICES: 모든 디바이스 목록 (변경되지 않음)
- get_available_devices(): 현재 사용 가능한 디바이스 목록 반환
- get_active_devices(): 현재 활성화된 디바이스 목록 반환
"""

import os
import json
import platform
import subprocess
from typing import Dict, List, Union, Tuple, Optional, Any

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.python.client import device_lib
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
        
        # TensorFlow 디바이스 정보 가져오기
        devices = device_lib.list_local_devices()
        
        for device in devices:
            device_type = device.device_type
            device_name = device.name
            
            # 디바이스 정보 생성
            device_info = {
                "name": device_name,
                "type": device_type,
                "memory_limit_bytes": device.memory_limit,
                "memory_limit_gb": round(device.memory_limit / (1024**3), 2),
                "physical_desc": getattr(device, 'physical_device_desc', 'N/A')
            }
            
            # 디바이스 가용성 확인
            try:
                # 간단한 텐서 연산으로 디바이스 작동 여부 확인
                with tf.device(device_name):
                    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                    b = tf.constant([[1.0, 1.0], [1.0, 1.0]])
                    c = tf.matmul(a, b)
                    # 결과가 실제로 계산되었는지 확인
                    _ = c.numpy()
                
                device_info["status"] = "available"
                
            except Exception as e:
                device_info["status"] = "unavailable"
                device_info["error"] = str(e)
            
            cls.DEVICES.append(device_info)
        
        return cls.DEVICES
    
    @classmethod
    def get_devices(cls) -> List[Dict[str, Any]]:
        """모든 디바이스 목록을 반환합니다."""
        if not cls.DEVICES:
            cls.initialize_devices()
        return cls.DEVICES
    
    @classmethod
    def get_available_devices(cls) -> List[Dict[str, Any]]:
        """현재 사용 가능한 디바이스 목록을 반환합니다."""
        devices = cls.get_devices()
        return [d for d in devices if d.get('status') == 'available']
    
    @classmethod
    def get_active_devices(cls) -> List[Dict[str, Any]]:
        """현재 사용 중인 디바이스 목록을 실시간으로 확인하여 반환합니다."""
        devices = cls.get_devices()
        active_devices = []
        
        # CPU는 항상 활성화된 것으로 간주
        cpu_device = next((d for d in devices if d['type'] == 'CPU'), None)
        if cpu_device:
            active_devices.append(cpu_device)
        
        # GPU 상태 확인 - 더 안정적인 방법 사용
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            for i, gpu in enumerate(gpus):
                # 해당 GPU의 디바이스 정보 찾기
                device_name = f"/device:GPU:{i}"
                device_info = next((d for d in devices if d['name'] == device_name), None)
                
                if device_info:
                    # GPU 활성 상태 확인 - 간단한 텐서 생성 테스트
                    try:
                        with tf.device(device_name):
                            # 작은 텐서를 생성하고 연산 수행
                            test_tensor = tf.constant([1.0, 2.0])
                            result = tf.reduce_sum(test_tensor)
                            # 실제로 실행되는지 확인
                            result_value = result.numpy()
                            
                            # 텐서가 생성되고 연산이 수행되면 활성 상태로 간주
                            active_device = device_info.copy()
                            active_device["active_reason"] = "Tensor operations detected"
                            active_devices.append(active_device)
                            
                            # 테스트용 텐서 정리
                            del test_tensor
                            del result
                    except Exception as e:
                        # 오류 발생 시 활성 상태가 아님
                        pass
        
        return active_devices
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """시스템 기본 정보를 반환합니다."""
        system_info = {}
        system_info['os'] = f"{platform.system()} {platform.release()}"
        system_info['python_version'] = platform.python_version()
        system_info['tensorflow_version'] = tf.__version__
        
        # CPU 정보 (Linux 시스템용)
        if platform.system() == "Linux":
            try:
                cpu_details = subprocess.check_output('lscpu', shell=True).decode('utf-8')
                for line in cpu_details.split('\n'):
                    if "Model name" in line:
                        system_info['cpu_model'] = line.split(':')[1].strip()
                    if "CPU(s)" in line and "NUMA" not in line and "On-line" not in line:
                        system_info['cpu_cores'] = line.split(':')[1].strip()
            except:
                system_info['cpu_model'] = platform.processor()
        else:
            system_info['cpu_model'] = platform.processor()
            
        return system_info
    
    @staticmethod
    def get_all_info() -> Dict[str, Any]:
        """모든 시스템 및 디바이스 정보를 실시간으로 반환합니다."""
        return {
            'system': DeviceInfo.get_system_info(),
            'devices': DeviceInfo.get_devices(),
            'available_devices': DeviceInfo.get_available_devices(),
            'active_devices': DeviceInfo.get_active_devices()
        }
    
    @staticmethod
    def print_info() -> None:
        """시스템 정보를 포맷팅하여 출력합니다."""
        info = DeviceInfo.get_system_info()
        
        print("=" * 50)
        print("시스템 정보:")
        print("=" * 50)
        for key, value in info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    @staticmethod
    def print_all_devices() -> None:
        """모든 디바이스 목록을 출력합니다."""
        devices = DeviceInfo.get_devices()
        
        print("=" * 50)
        print(f"모든 디바이스 목록 (총 {len(devices)}개):")
        print("=" * 50)
        
        for i, device in enumerate(devices):
            status_str = f"[{device.get('status', '알 수 없음')}]"
            print(f"{i+1}. {device['name']} ({device['type']}) {status_str}")
            print(f"   메모리 제한: {device['memory_limit_gb']} GB")
            if device['physical_desc'] != 'N/A':
                print(f"   물리적 설명: {device['physical_desc']}")
            print()
    
    @staticmethod
    def print_available_devices() -> None:
        """사용 가능한 디바이스 목록을 출력합니다."""
        devices = DeviceInfo.get_available_devices()
        
        print("=" * 50)
        print(f"사용 가능한 디바이스 목록 (총 {len(devices)}개):")
        print("=" * 50)
        
        for i, device in enumerate(devices):
            print(f"{i+1}. {device['name']} ({device['type']})")
            print(f"   메모리 제한: {device['memory_limit_gb']} GB")
            if device['physical_desc'] != 'N/A':
                print(f"   물리적 설명: {device['physical_desc']}")
            print()
    
    @staticmethod
    def print_active_devices() -> None:
        """현재 사용 중인 디바이스 목록을 출력합니다."""
        devices = DeviceInfo.get_active_devices()
        
        print("=" * 50)
        print(f"현재 사용 중인 디바이스 목록 (총 {len(devices)}개):")
        print("=" * 50)
        
        for i, device in enumerate(devices):
            print(f"{i+1}. {device['name']} ({device['type']})")
            print(f"   메모리 제한: {device['memory_limit_gb']} GB")
            
            # 활성 이유 표시 (있는 경우)
            if 'active_reason' in device:
                print(f"   활성 이유: {device['active_reason']}")
                
            if device['physical_desc'] != 'N/A':
                print(f"   물리적 설명: {device['physical_desc']}")
            print()


class SimpleModel:
    """간단한 TensorFlow 모델을 정의하는 클래스"""
    
    @staticmethod
    def create_mlp() -> tf.keras.Model:
        """간단한 MLP 모델을 생성합니다."""
        model = models.Sequential([
            layers.Input(shape=(784,)),
            layers.Dense(128, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model


class GPUChecker:
    """GPU 기능 검사를 위한 클래스"""
    
    @staticmethod
    def set_memory_growth() -> None:
        """GPU 메모리 증가 설정 (초기화 전에 호출해야 함)"""
        try:
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                print("GPU 메모리 증가 설정이 활성화되었습니다.")
        except Exception as e:
            print(f"GPU 메모리 설정 중 오류 발생: {e}")
    
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
        available_gpus = tf.config.list_physical_devices('GPU')
        print("TensorFlow 사용 디바이스:", available_gpus)
        
        if not available_gpus:
            return False, "TensorFlow에서 사용 가능한 GPU가 없습니다."
        
        try:
            # TensorFlow 환경 설정
            os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # OneDNN 최적화 비활성화 (문제 해결에 도움)
            os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'  # 메모리 할당자 설정
            
            # 데이터 불러오기
            (x_train, y_train), _ = mnist.load_data()
            x_train = x_train.reshape(-1, 28*28).astype("float32") / 255.0
            
            # 모델 생성
            model = SimpleModel.create_mlp()
            
            # 단일 배치만 처리하기 위한 콜백
            class StopAfterBatches(tf.keras.callbacks.Callback):
                def __init__(self, batch_limit, clear_screen=False):
                    super().__init__()
                    self.batch_limit = batch_limit
                    self.batch_count = 0
                    self.clear_screen = clear_screen
                    
                def on_batch_end(self, batch, logs=None):
                    self.batch_count += 1
                    
                    if self.clear_screen:
                        clear_output(wait=True)
                        
                    print(f"배치 {self.batch_count}/{self.batch_limit} 처리 완료 - Loss: {logs.get('loss'):.4f}")
                    
                    # 디바이스 상태 출력 시도
                    print("\n현재 활성 디바이스:")
                    active_devices = DeviceInfo.get_active_devices()
                    for device in active_devices:
                        if device['type'] == 'GPU':
                            print(f"- {device['name']} 활성화")
                    
                    if self.batch_count >= self.batch_limit:
                        self.model.stop_training = True
            
            # 모델 학습 (배치 제한 적용)
            model.fit(
                x_train, y_train,
                epochs=1,
                batch_size=64,
                callbacks=[StopAfterBatches(batch_limit, clear_screen)]
            )
            
            return True, None
            
        except Exception as e:
            return False, str(e)


def check_gpu(clear_screen: bool = False):
    """
    TensorFlow GPU 정보를 확인하고 간단한 모델 학습을 통해 GPU 작동 여부를 검사합니다.
    
    Args:
        clear_screen: 진행 상태를 출력할 때 화면을 지울지 여부
    """
    # TensorFlow GPU 메모리 증가 설정 (가장 먼저 실행)
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(f"GPU 메모리 설정 오류: {e}")
    
    # 환경 변수 설정 (CUDA/cuDNN 관련 문제 해결에 도움)
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
    
    # 모든 디바이스 목록 출력
    DeviceInfo.print_all_devices()
    
    # 사용 가능한 디바이스 목록 출력
    DeviceInfo.print_available_devices()
    
    # 현재 사용 중인 디바이스 목록 출력
    DeviceInfo.print_active_devices()
    
    # 시스템 정보 출력
    DeviceInfo.print_info()
    
    # GPU 사용 가능 여부 확인
    if not gpus:
        print("\n⚠️ TensorFlow에서 사용 가능한 GPU가 없습니다. CPU만 사용 가능합니다.")
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
        print("\n✅ GPU 테스트 성공! TensorFlow가 GPU에서 정상적으로 작동합니다.")
    else:
        print(f"\n❌ GPU 테스트 실패: {error}")
        print("TensorFlow가 GPU를 인식했지만 연산 중 오류가 발생했습니다.")
        print("다음 환경 변수 설정을 시도해 보세요:")
        print("  - export TF_ENABLE_ONEDNN_OPTS=0")
        print("  - export TF_GPU_ALLOCATOR=cuda_malloc_async")
        print("  - export CUDA_VISIBLE_DEVICES=0  # 특정 GPU만 사용")


# GPU 메모리 증가 설정 (가장 먼저 실행)
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
except RuntimeError as e:
    print(f"GPU 메모리 설정 오류: {e}")

# 환경 변수 설정 (문제 해결에 도움됨)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

# 디바이스 목록 초기화 (DEVICES만 전역 변수로 유지)
DeviceInfo.initialize_devices()
DEVICES = DeviceInfo.DEVICES

# # 함수로 제공 (실시간 상태 반영)
# def available_devices():
#     """사용 가능한 디바이스 목록을 반환합니다."""
#     return DeviceInfo.get_available_devices()

# def active_devices():
#     """현재 활성화된 디바이스 목록을 반환합니다."""
#     return DeviceInfo.get_active_devices()
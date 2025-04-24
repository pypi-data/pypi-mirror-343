# nubilus

(EN) `nubilus` is a Python open source library for ECG signal processing, deep learning-based arrhythmia detection, and intelligent pipeline development.

(KR) `nubilus`는 ECG(심전도) 신호 처리, 부정맥 검출 AI 개발, 지능형 워크플로우 구축을 위한 파이썬 오픈소스 라이브러리입니다.

---

## Background and Motivation

(EN) This library was developed to accelerate the workflow of AI research in arrhythmia detection, particularly from 12-lead ECG data. It automates signal preprocessing, segmentation, and model input formatting based on biomedical standards.

(KR) 이 라이브러리는 12유도 심전도 데이터를 기반으로 부정맥 진단 AI 연구의 워크플로우를 가속화하기 위해 개발되었습니다. 의료 신호 표준에 기반하여 전처리, 구간 추출, 모델 입력 구성 등의 과정을 자동화합니다.

---

## Features

(EN)
- MUSE XML 기반 12-lead ECG 파싱
- R-peak 기반 beat segmentation 및 QRS 전후 신호 추출
- P-wave, F-wave, HRV feature extractor (개발 중)
- Deep learning 학습용 입력 텐서 생성 자동화
- PyTorch / TensorFlow 기반 학습 템플릿
- 향후: 멀티프로세스, 병렬 인퍼런스 지원 예정

(KR)
- MUSE XML 기반의 12유도 ECG 파싱 기능
- R-peak를 기준으로 한 beat 분할 및 입력 구성
- P파, F파, HRV 특성 자동 추출 (추후 확장)
- 딥러닝 학습을 위한 텐서 자동 생성
- PyTorch 및 TensorFlow 기반 템플릿 제공
- 향후 다중 프로세스 및 병렬 연산 지원 예정

---

## Installation

(EN) To install the nubilus library, you can use pip:

(KR) `nubilus` 라이브러리를 설치하려면, pip를 사용할 수 있습니다:

```sh
pip install nubilus

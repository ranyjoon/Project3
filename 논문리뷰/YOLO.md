# You Only Look Once

✨ [논문 링크](https://arxiv.org/pdf/1506.02640.pdf) ✨
-----
<br>

## Introduction

```
🔸 객체 감지에 대한 새로운 접근 방식 🔸
- **You Only Look Once**: 어떤 물체가 있고 어디에 있는지 예측하기 위해 이미지를 한 번만 봄
- **단일 컨볼루션**: 하나의 네트워크는 여러 경계 상자와 해당 상자에 대한 클래스 확률을 동시에 예측
- **통합 네트워크**: 전체 검출 파이프라인이 하나의 네트워크이므로 검출 성능에 대한 최적화가 직접적으로 가능
- **매우 빠르고 높은 mean average precision(mAP) 달성**: 위치적 오류를 범할 수는 있으나 false positives를 예측하는 경우는 적음
- **객체의 일반화 가능한 표현을 학습**: 예상치 못한 입력에 적용할 때도 실패할 가능성이 적음
```
<br>

## Unified Detection

입력 이미지를 S × S 그리드로 나누기
각 그리드 셀은 B개의 바운딩 박스와 해당 박스에 대한 신뢰도 점수를 예측
- 신뢰도 점수(Confidence Score) : 
$Pr(Object) * IOU_{pred}^{truth}$
  - 상자에 개체가 포함되어 있다고 확신하는 정도 
  - 상자의 예측에 대한 정확성
  
* IOU: intersection over union
- (겹쳐진 넓이) / (전체 넓이)
- 완전히 겹쳐져 있다면 IOU = 1





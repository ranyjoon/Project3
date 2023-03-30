# You Only Look Once

✨ [논문 링크](https://arxiv.org/pdf/1506.02640.pdf) ✨
-----
<br>

## Introduction

🔸 객체 감지에 대한 새로운 접근 방식 🔸
- **You Only Look Once**: 어떤 물체가 있고 어디에 있는지 예측하기 위해 이미지를 한 번만 봄
- **단일 컨볼루션**: 하나의 네트워크는 여러 경계 상자와 해당 상자에 대한 클래스 확률을 동시에 예측
- **통합 네트워크**: 전체 검출 파이프라인이 하나의 네트워크이므로 검출 성능에 대한 최적화가 직접적으로 가능
- **매우 빠르고 높은 mean average precision(mAP) 달성**: 위치적 오류를 범할 수는 있으나 false positives를 예측하는 경우는 적음
- **객체의 일반화 가능한 표현을 학습**: 예상치 못한 입력에 적용할 때도 실패할 가능성이 적음
<br>

## Unified Detection
![image](https://user-images.githubusercontent.com/115753833/228888747-599d4286-668b-429b-afd4-1d08fe92503d.png)

<br>

### 1. 입력 이미지를 S × S 그리드로 나누기
<img src="https://user-images.githubusercontent.com/115753833/228887745-7b8e8a66-299d-4b5e-99cc-a63620a01b6d.png" width="230">
<br>

### 2. 각 그리드 셀: 

### 2.1. B(bounding boxes)와 각각의 Box에 대한 Confidence를 예측

<img src="https://user-images.githubusercontent.com/115753833/228889430-98733319-6f5e-43f0-845f-57718aadb1e3.png" width="300">
<br>


&ensp; **Bounding Box(바운딩 박스) = [x, y, w, h, confidence**]
  - **(x, y)**: Bounding box의 중심점이며, grid cell의 범위에 대한 상대값으로 입력
  - **(w, h)**: 전체 이미지의 width, height에 대한 상대값이 입력
  - **confidence**: 예측 box와 실제 정답 사이의 IOU를 의미

```
• Confidence Score(신뢰도 점수) 
   - 상자에 개체가 포함되어 있다고 확신하는 정도 
   - 상자의 예측에 대한 정확성
   
• IOU(intersection over union)
   - (겹쳐진 넓이) / (전체 넓이)
   - 완전히 겹쳐져 있다면 IOU = 1
```
> Confidence Score = $Pr(Object) * IOU_{pred}^{truth}$

<br><br>


### 2.2. C(conditional class probability) 예측

<img src="https://user-images.githubusercontent.com/115753833/228890398-9a41df94-a339-43f2-9972-d3af08fa21f0.png" width="230">

```
• 해당 그리드 셀이 객체를 포함하는 것을 조건으로 함
• B(바운딩 박스의 개수)와 상관없이 각 그리드 셀당 하나의 클래스 확률 세트를 예측
```
> Conditional Class probability = $Pr (class _{i} | Object)$

<br><br>

### 3. 평가시, 각 박스에 대한 class-specific confidence scores(클래스별 신뢰도 점수)를 가짐

```
• Class Specific Confidence Score = Conditional Class probability * Confidence Score

  - Conditional Class probability: C(각 그리드 셀의 클래스 확률)
  - Confidence Score: 각 개별 바운딩 박스의 신뢰도
```
> $=Pr(Class _{i} |Object) * Pr (Objects) * IOU _{pred}^{truth}$

> $=Pr (Class _{i}) * IOU _{pred}^{truth}$

<br><br>
### 논문에서의 YOLO 평가
- Object Detection Dataset: PASCAL VOC
```
• S(그리드) = 7
• B(바운딩박스) = 2
• C = 20(PASCAL VOC에는 20개의 지정된 클래스가 저장되어 있음)
```
> 최종 예측 텐서 `S × S × (B × 5 + C)` 

> = 7 × 7 × ((2 × 5) + 20) = 7 × 7 × 30



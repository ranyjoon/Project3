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

-----
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
  - 5개의 인자 값들은 모두 (0,1)범위의 값으로 정규화

```
• Confidence Score(신뢰도 점수) 
   - 상자에 개체가 포함되어 있다고 확신하는 정도 
   - 상자의 예측에 대한 정확성
   
• IOU(intersection over union)
   - (겹쳐진 넓이) / (전체 넓이)
   - 완전히 겹쳐져 있다면 IOU = 1

• grid cell 내에 
  객체가 존재할 경우, Pr(obj) = 1 → Confidence Score = IOU
  객체가 존재하지 않을 경우, Confidence Score = 0
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

### 4. 논문에서의 YOLO 평가
- Object Detection Dataset: PASCAL VOC
```
• S(그리드) = 7
• B(바운딩박스) = 2
• C = 20(PASCAL VOC에는 20개의 지정된 클래스가 저장되어 있음)
```
> 최종 예측 텐서 `S × S × (B × 5 + C)` 

> = 7 × 7 × ((2 × 5) + 20) = 7 × 7 × 30

<br><br>
=====

### Network Design

![image](https://user-images.githubusercontent.com/115753833/228909039-5fd1bf8e-f8c8-4a24-b871-78ae2b9f3b35.png)

- **컨볼루션 신경망으로 구현하고 PASCAL VOC 탐지 데이터 세트에서 평가**
- **24개의 컨볼루션 레이어: 이미지 특징 추출 / 2개의 완전 연결 레이어: 출력 확률과 좌표를 예측**
- GoogLeNet 모델에서 영감을 받음 <br>
&ensp; (차이점: 인셉션 모듈 대신 1 × 1 reduction layers와 그에 뒤따르는 3 × 3 convolutional layers 사용)

<br><br>
=====

### Training
- **Pretrained Network**: 처음 20개의 Conv층 → ImageNet의 1000-class competition dataset으로 pre-training(사전 훈련)
- **Training Network**: 추가 4개의 Conv층 + FC layer = 최종적으로 1470(7 x 7 x 30)의 Tensor 출력
  - bounding box의 x , y , w , h 를 0~1사이의 값으로 **정규화**
  - **활성화 함수**: 
    - 최종 layer: 선형 활성화 함수
    - 다른 모든 layer: Leaky ReLU
  - **최적화(Optimize)**
    - SSE(sum-squared error)

```
• SSE(sum-squared error)
  - 장점: 최적화 쉬움
  
  - 단점1: 모델을 불안정하게 만들 수 있음
    ① localization, classifiaction 오류에 같은 가중치를 부여하므로 이상적이진 않음 
    ② 많은 그리드셀이 객체를 포함하지 않아 신뢰도점수(confidence score)가 0으로 수렴하여 overpowering gradient를 유발
    → 해결방안: object를 포함하고 있지 않은 bbox의 가중치를 0.5로 설정하여 패널티를 낮추고, 
               object를 포함하는 경우 5의 가중치를 주어 패널티 증가
  
  - 단점2: 박스 크기에 상관없이 가중치 부여
    → 해결방안: bounding box의 width와 height 연산에 sqaure root를 직접 사용
```
> $λ_{coord} = 5$ , $λ_{noobj} =0.5$

<br>

🔶 **PASCAL VOC 2007 및 2012 훈련 및 검증**
```
epochs = 135
batch size = 64
momentum = 0.9
decay = 0.0005

* 과적합 방지 *
dropout과 extensive data augmentation 사용
```

<br><br>
=====

<img src="https://blog.kakaocdn.net/dn/wOJlj/btqF3S3iQAa/wM8SggFkxA2YYDfAOcZFDK/img.png" width="850">
<img src="https://blog.kakaocdn.net/dn/bd6D6J/btqLq2TkKUX/4KH0HZB1GT8hBRvprlKckk/img.png">

![image](https://user-images.githubusercontent.com/115753833/229745850-83d3e6d4-71d7-4079-a5d2-5a7f5f407643.png)

                                                                                         
<br><br>                                                                                   
=====

### YOLO의 한계
- bounding box 예측에 강력한 공간적 제약, 작은 객체 탐지에 어려움
- 새롭거나 일반적이지 않은 비율과 구성을 가진 객체는 일반화하기 어려움
- 손실 함수에 대해 훈련하는 동안 작은 경계 상자와 큰 경계 상자에서 오류를 동일하게 처리

<br><br>

-----
## Experiments

### 다른 객체탐지 시스템과의 비교
- **R-CNN** : 영역 제안을 사용하여 이미지에서 객체를 탐지
  - 복잡한 파이프라인의 각 단계는 독립적으로 정확하게 조정되어야 하며 결과 시스템은 매우 느림

- **Fast and Faster R-CNN** :R-CNN 프레임워크의 속도를 높이는 데 중점
  - 속도와 정확도가 향상되었지만 둘 다 여전히 실시간 성능에는 미치지 못함
  - YOLO는 파이프라인을 사용하지 않으며, 다양한 물체를 동시에 감지하는 방법을 학습하는 범용 감지기

<img src="https://user-images.githubusercontent.com/115753833/229744255-bdb9b181-83cb-46e4-9a9a-dadd329d49d9.png" width="49%"><img src="https://user-images.githubusercontent.com/115753833/229744364-a63fa7f6-1d7a-4ea7-bf4c-fb51a2a69d93.png" width="49%">

### VOC 2007 오류 분석
- YOLO는 지역화 오류가 많이 발생
- Fast R-CNN은 지역화 오류는 훨씬 적지만 배경 오류는 훨씬 더 많음
- Fast R-CNN은 YOLO보다 배경 감지를 예측할 가능성이 거의 3배 더 높음

<br><br>

### Fast R-CNN과 YOLO의 결합

![image](https://user-images.githubusercontent.com/115753833/229805083-d2537d4f-bee4-4898-af9b-5c4ef847e311.png)

- Fast R-CNN 모델은 VOC 2007 테스트 세트에서 71.8%의 mAP를 달성
- YOLO와 결합하면 mAP가 3.2% 증가하여 75.0%
- YOLO 속도의 이점을 얻지 못함

<br><br>

### VOC 2012 결과
  - YOLO는 57.9% mAP기록, 작은 객체 탐지의 어려움
  - Fast R-CNN + YOLO 모델은 최고 성능의 탐지 방법

<br><br>

### 일반화 가능성: 아트워크에서 사람 감지
🔸 **Picasso Dataset 및 People-Art Dataset 비교**

![image](https://user-images.githubusercontent.com/115753833/229809808-961ec2e6-69b1-4b48-bfd6-ef06102c58e1.png)
![image](https://user-images.githubusercontent.com/115753833/229809955-8f4af5f2-5f4e-40b0-aae8-dd2d91953811.png)

- R-CNN은 예술 작품에 적용될 때 성능이 떨어지는 편 / 자연이미지에서는 성능이 괜찮음
- DPM은 예술 작품에서 AP를 잘 유지
- YOLO는 예술작품, 자연이미지 모두에서 AP를 잘 유지하는 편이며 바운딩박스와 감지 성능이 좋음

<br><br>

-----
## 결론
- YOLO는 객체 감지를 위한 통합 모델이며
- 모델의 구성이 간단
- 직접적으로 해당하는 손실 함수에 대해 학습
- 전체 모델이 공동으로 학습

**이미지 객체 탐지시 걸리는 시간이 빠르고 성능이 좋은 모델**

<br><br><br><br>

-----
# YOLO모델의 발전

- **YOLOv1**: 정확도가 너무 낮은 문제가 있었고 이 문제는 **v2**까지 이어짐
- **YOLOv3**: 엔지니어링적으로 보완, v2보다 살짝 속도는 떨어지더라도 정확도를 대폭 높인 모델
- **YOLOv4**: YOLOv3에 비해 AP, FPS가 각각 10%, 12% 증가 / 다양한 딥러닝 기법(WRC, CSP ...) 등을 사용해 성능을 향상
- YOLOv4,**YOLOv5**:
   - CSPNet 기반의 Backbone(CSPDarkNet53)을 설계
   - **Backbone**은 이미지로부터 **Feature map을 추출**하는 부분으로, CSP-Darknet를 사용
   - **Head**는 추출된 Feature map을 바탕으로 **물체의 위치**를 찾는 부분 / predict classes 와 bounding boxes 작업이 수행
      - Anchor Box(Default Box)를 처음에 설정하고 이를 이용하여 최종적인 Bounding Box를 생성
      - YOLO v3와 동일하게 3가지의 scale(8 pixel /16 pixel / 32 pixel)에서 바운딩 박스를 생성 + 3개의 앵커박스 = 총 9개의 앵커박스
   - YOLOv5가 YOLOv4에 비해 낮은 용량과 빠른 속도 (성능은 비슷)
     

# Tanner-Whitehouse 3

✨ [논문 링크](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8660640) ✨
-----
### Abstract
```
딥러닝 기술은 최근 몇 년간 빠르게 발전하였으며, 
골 연령 평가(BAA)는 딥러닝의 이점을 얻을 수 있는 전형적인 객체감지 및 분류 문제이다.
Tanner-Whitehouse 3 기법은 소아 및 청소년의 뼈 성숙도를 평가하는 데 널리 사용되는 기술이며,
이를 자동화하여 정확성과 효율성 향상 및 임상 결과를 개선 가능하게 할 수 있다.

* TW3 기법: 13개의 다른 뼈에서 뼈의 양 끝인 골단과 관절주의의 성장 영역을 지역화하여 해당 뼈의 골 연령을 추정하는 방법
```
### Index Trems
Bone age assessment(BAA), deep learning, GP, TW3

-----
<br>

## Introduction

### 1) TW 골연령 추정 방식
1.	관심 영역(ROI)을 구성된 손과 손목의 특정한 뼈의 성숙도를 평가
2.	사전 정의된 골격 성숙도 점수는 성숙도 수준에 따라 개별 ROI에 할당
3.	2.의 점수를 합산하여 총 성숙도 점수를 계산
4.	마지막으로 성숙도 점수와 BAs 간의 상관 행렬을 사용하여 BA로 변환
<br>

### 2) TW3 방식 요약, 장점 및 단점
```
• 현재 TW3는 노뼈(Radius), 자뼈(ulna) 및 단골(RUS)을 ROI로 분석
• 골 연령 평가에 딥러닝 방식을 적용할 경우, 입력된 값(환자의 왼손과 손목 X-선 이미지)에 해당하는 클래스(예: BA에 해당하는 클래스)가 예측
• 합성곱 신경망(CNN)과 그 변형이 BAA 자동화에 점점 더 많이 사용되고 있으며, 유망한 결과를 보임
```

<img src="https://user-images.githubusercontent.com/115753833/228771900-46598d56-7f5b-4a86-85bd-f618430b5e40.png" width="500">

🔸 **장점**: <br>
- 상관 행렬이 0.1년 단위로 구성되기 때문에 더 정확하고 재현성이 높음

🔸 **단점**: <br>
- 왼손과 손목의 X-선 이미지 내의 모든 ROI를 정확하게 위치시키는 것이 쉽지 않음<br>
  : 단일 ROI의 성장 영역에 대한 정확한 위치 정보를 획득하지 못하면 평가 정확도가 저하
  
- 대규모 레이블 트레이닝 데이터셋을 구성하기 어려움<br>
  : 개별 ROI의 성숙도와 BA에 대한 방사선과학자 판독에는 상당한 시간과 비용이 필요
<br>

## TW3 적용방식
![image](https://user-images.githubusercontent.com/115753833/228784839-52e699be-cadc-44d1-90ab-08f34e035fcd.png)
-----
<br>

### 1) 경계 ROI(bROI) 사용
```
TW3 방법에서 사용되는 실제 ROI를 포함하여 손목, 엄지, 중지, 새끼손가락의 충분히 넓은 영역을 추출
```
<img src="https://user-images.githubusercontent.com/115753833/228784506-dfe99781-f1ad-403f-aba2-7c50f08b6137.png" width="400">

- 손목의 bROI: 노뼈(radius), 자뼈(ulna).
- 엄지의 bROI: 엄지의 첫마디뼈, 끝마디뼈, 손목과 손가락 사이의 중수골
- 중지의 bROI: 중지의 첫마디뼈, 중간마디뼈, 끝마디뼈, 손목과 손가락 사이의 중수골 
- 소지의 bROI: 소지의 첫마디뼈, 중간마디뼈, 끝마디뼈, 손목과 손가락 사이의 중수골
<br>

### 2) bROI에서 13개의 실제 ROI를 추출
### 3) 개별 ROI의 골격 성숙도 수준을 분류하고 이를 점수로 변환
### 4) 골 연령 예측
<br>

-----
<br>

## 논문의 이미지 추출 및 CNN 구성 방식
### STEP 1. bROIs추출(OpenCV 적용)
**1. 원본 이미지의 손목을 수직으로 회전**

<img src="https://user-images.githubusercontent.com/115753833/228792650-1960587d-6394-4cf6-bfe3-9b142f69326f.png" width="700">

```
(1) 그레이 스케일 이미지로 변환 / 이진화
(2) 손의 윤곽을 추출
(3) 각 행의 흰색 픽셀 좌표가 저장
(4) 회귀 분석: 픽셀 포인트를 사용하여 손목의 중간점을 계산한 다음 이 포인트에 근접한 직선을 계산
(5) 직선의 기울기를 계산하고 이미지를 회전
```
<br>

**2. 손목과 손가락에 따라 다른 알고리즘이 적용**
<img src="https://user-images.githubusercontent.com/115753833/228793728-1f8f2fea-285a-4983-baf9-b008a79ea276.png" width="700">
<br>

### STEP 2. bROIs에서 실제 ROI를 추출(CNN적용)
**Faster R-CNN사용**

<img src="https://user-images.githubusercontent.com/115753833/228802139-618b5a70-526c-439f-a84d-285a36713a74.png" width="400">

```
(1) 첫 번째 컨볼루션: 입력 이미지의 특징 맵을 추출 → 9개의 앵커 박스 결정
(2) ROI 풀링: 고정 크기 특징 벡터를 추출
(3) 완전 연결 계층
   ➡ 두 개의 완전 연결 레이어: 최종 영역의 크기와 위치, 예측 점수 결정
```
<br>

### STEP 3. 골 연령 측정(CNN적용)
**VGGNet-BA**

<img src="https://user-images.githubusercontent.com/115753833/228805457-fe0e90ec-7ae3-47d0-a927-9ce89d9b0e89.png" width="800">

```
 ◆ VGGNet을 기본 네트워크 아키텍처로 사용 
 
 ◆ VGGNet과 차이점 
  (1) 각 레이어의 수와 구조가 조금씩 변경
      : 매개 변수의 수가 크게 감소하며, 기존의 VGGNet 구성보다 약 750배 축소  
  (2) 입력 이미지 크기(112 × 112로 변경)

 ◆ 골 성숙도 점수 분류: 간단한 voting ensemble model사용
  (1) 각각 뼈 성숙도 수준과 확률을 예측 → 개별 모델의 예측을 평균
  (2) 각각 대응하는 ROI의 뼈 성숙도 수준을 분류하기 위해 13개의 평균 투표 앙상블로 구성
```
<br>

## 논문의 딥러닝 적용 결과
### 1) Dataset
**18세 미만 한국 어린이의 왼손 및 손목 X-ray 이미지 3,344개**
<br>
```
X-ray 이미지 = bROI 이미지 4개 + 주석 파일 1개
                                (13개 실제 ROI 좌표, 개별 ROI의 골격 성숙도 수준, 예상 BA(방사선과 전문의 판독))
```


### 2) Faster R-CNN
- 검증 데이터셋20% + 학습 데이터 80%
```
• mini-batch size: 256
• momentum: 0.9
• weight decay: 0.0005
• learning-rate: 0.001
• epoch: 30
 ```
 
 ### 3) VGGNet-BA
- 데이터를 증식하여 사용(검증 데이터셋20% + 학습 데이터 80%)
```
• Optimizer: Adam
  - mini-batch size: 256
  - momentum: 0.9
• learning-rate: 0.001
• dropout: 0.5
• epoch: 30
• early stopping 사용
```

### 4) 골 연령 예측
- voting ensemble model
- 각 ROI마다 다른 골 성숙도 레벨 적용
<img src="https://user-images.githubusercontent.com/115753833/228816098-f5de6990-1a07-498a-bd7c-9570467072c0.png" width="400">
<br>

### 5) 최종 결과
- 약 3,300개의 X-ray 이미지 데이터셋을 기반으로 제안된 딥러닝 기반 뼈나이 판독 시스템의 MAE와 RMSE를 측정
- 13개의 ROI에 대한 뼈 성숙도의 평균 top-1 및 top-2 예측 정확도는 각각 79.6%와 97.2%
- 연령 예측에 대한 MAE와 RMSE는 각각 0.46년과 0.62년
- 실제 데이터와의 1년 이내의 정확도는 97.6%

<img src="https://user-images.githubusercontent.com/115753833/228818196-9c559d74-ecb8-4b65-bc9e-be409d1398c4.png" width="33%"><img src="https://user-images.githubusercontent.com/115753833/228819699-477dd588-7bdc-49c0-a7ae-91259d29f67a.png" width="33%"><img src="https://user-images.githubusercontent.com/115753833/228819813-d3fef5cc-8631-445c-a4c9-a9aef7df6ae7.png" width="33%">





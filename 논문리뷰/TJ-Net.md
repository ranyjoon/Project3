# TJ-Net / Automatic Radiographic Bone Age Assessment Using Deep Joint Learning with Attention Modules 

✨ [논문 링크](https://pdfs.semanticscholar.org/6342/afdefe3ecb2af3706240a6b57108d2534705.pdf) ✨
-----
### Abstract
```
손 및 손목 골격 방사선 사진은 뼈 나이 평가와 관련된 다양한 의료 및 법의학 작업을 위한 중요한 매개체 역할을 한다.
기존의 아틀라스 기반 뼈 나이 식별 기술의 대안으로 딥 러닝 알고리즘은 심층신경망(DNN)을 제안하는데, 
이는 large scale annotated datasets로 잘 훈련된 경우 X-ray사진을 미리 정의된 뼈 나이 클래스로 자동 분류할 수 있다.

논문에서는 골연령 예측을 위해 특별히 설계된 multi-scale attention enhanced classifier with a convolutional neural network을 소개한다.
- 피험자의 골연령과 성별을 공동으로 학습하도록 훈련
- RSNA dataset과 Tongji dataset에서 훈련
  ➡ RSNA dataset에서 0.41년, Tongji dataset에서 0.36년 오차 발생(mean absolute difference)
```
### Keywords
Attention mechanism, bone age, convolutional neural networks, joint learning

-----
<br>

## Introduction

- X-ray이미지는 방사선 전문의가 어린이의 뼈 나이를 추정할 수 있는 증거를 제공
- 개인의 뼈 성장은 유전학, 호르몬 수준, 식습관, 그리고 대사 장애 등과 같은 많은 다른 요소들에 의해 영향
- 뼈 나이를 정확하게 추정하는 것은 성장과 관련된 많은 문제를 식별하는 데 중요

<br>

### 1) 골 연령 측정 기법

- **the Greulich and Pyle method(GP기법): 일반 방사선 전문의의 판단기법**
  - X-ray이미지와 유사한 이미지를 시각적으로 검색하여 일치하는 연령을 Atlas에서 검색
  - 기존 Atlas 방식과 개인 판단에 의존
  - 동일한 방사선 사진에서 다른 예측 가능

- **the Tanner and Whitehouse method(TW기법)**
  - 더 구체적인 방법으로 방사선 사진의 특정 부위를 평가
  - 체계적인 점수 매기기를 위한 상세한 특징 집합을 도입하여 계산

<br>

➡ **인지 편향적 오류를 줄이기 위해 TW기법 사용**

![image](https://user-images.githubusercontent.com/115753833/229844227-66b9a3ef-d990-4ffc-98af-c760436eb6f3.png)

<br>

### 2) 논문의 골 연령 측정 모델 TJ-Net
- 연령 그룹 분류에 중요한 특징을 강조하기 위해 attention mechanism 사용
- 성별과 뼈 연령을 동시에 학습하는 프레임워크
- 학습된 특징들이 전통적인 아틀라스 기반 평가와 일치, 다른 데이터셋으로 전이 가능 <br>
&ensp;`전이 학습(transfer learning): 새로운 응용 프로그램이 다른 도메인에서 배운 지식을 활용할 수 있도록 함`

<br><br>

## Related Work

- 방사선 사진에서 중요한 영역에 집중하기 위해 전처리 단계에서, 사람들은 수동 또는 자동으로 손 뼈에서 이러한 영역을 감지
- 데이터 확대는 일부 모델의 과적합을 완화하는 데 도움
- 손의 세 부분에서의 estimates를 통합하는 앙상블을 제안
- 방사선 사진의 픽셀 외에도, 성별 정보 입력은 골 연령 평가를 개선하는 데 도움이 되는 것으로 입증

<br><br>

## Proposed Method

### 이 논문에서는 "TJ-Net"이라고 불리는 골 연령 분류 네트워크를 제안한다.
<br>

![image](https://user-images.githubusercontent.com/115753833/229986979-aef44dcc-57b5-4584-a5f3-d494ef0ce059.png)

<br>

- 입력 이미지를 77개의 골 연령 클래스 중 하나(3개월 기본 단위로 0-19세에 해당)와 이진 성별 레이블에 매핑
- **블록 1~4**
  - 입력에서 중요한 feature를 추출
  - 컨볼루션/풀링 부분
  - 최종 출력은 softmax 함수
- **블록 5**
  - multi-scale features를 고수준 특징으로 융합
  - dense layer(fully connected layer)를 통해 성별 분류기
- **블록 6**은 
  - dense layer(fully connected layer)를 통한 연령 분류기로, 이미지 특징과 입력된 성별을 사전 정의된 연령 범주와 매칭
    - 별도의 성별 입력은 연령 분류기가 결과를 조정할 수 있도록 추가 정보를 제공
    - 성별 분류는 뼈 특징을 학습하는 데 도움을 줌
- **Attention mechanism, residual learning, multi-scale features**
  - TJ-Net에 CBAM(Convolutional Block Attention Module), IncRes(Inception ResNet) 모듈을 도입하여 골 연령 관련 feature 추출을 강화

<br><br>

### Convolution-based Attention Modules(Block 1,2)
- 앞부분의 컨볼루션 블록에서 감지된 채널 및 공간 특징 중 convolution-filtered features는 뼈 연령을 식별하는 데에 있어서 다양한 중요도를 가짐
- CBAM의 도입함으로써 채널 및 공간 차원에서 전체 목표와 더 관련이 있는 특징을 강화하는 것이 목적
- TJ-Net의 각각의 세 CBAM은 순차적으로 channel attention(채널주목) 과 spatial attention(공간주목) 모듈로 구성

<br>

```
◆ channel attention module
1. 입력 feature는 average / maximum pooling layers를 병렬로 통과
2. dense layer에서 sigmoid 활성화를 통해 channel attention scale vector 생성
3. 원래의 입력 feature는 스케일에 의해 가중치가 부여된 새로운 텐서를 형성

◆ spatial attention module
1. 위의 정제된 텐서는 이후 이전 모듈과 동일한 두 개의 병렬 풀링 레이어를 통과
2. 1 × 7 × 7 convolution kernel로 처리
3. sigmoid 활성화 함수를 통해 spatial attention scale matrix를 출력
```

<img src="https://user-images.githubusercontent.com/115753833/229991624-983734cd-e08c-4f0a-ad05-95cc994fe448.png" width="600">

<br><br>

### Inception Residual Modules(Block 3,4 + Inception Module)

- Block IncRes1과 IncRes2는 다양한 컨볼루션 커널 크기를 가진 여러 분기로 구성(서로 다른 구조를 가짐)
  - 1 × 1 및 3 × 3 컨볼루션 커널을 결합

- Block Inception1 및 Inception2 모듈에는 각각 1 × 1, 3 × 3, 1 × 3, 3 × 1, 5 × 5, 1 × 7 및 7 × 1의 조합인 4개의 다중 스케일 분기

![image](https://user-images.githubusercontent.com/115753833/229994128-a78170e2-2f9a-443c-93e5-1f90e4967d9e.png)

<br><br>

### Loss Function for Joint Learning 
정확한 성별 입력으로 나이를 정확하게 판단하는 데 도움이 됨 <br>
→ 성별과 뼈 연령 모두의 배치별로 교차 엔트로피를 동시에 최소화함으로써 훈련 데이터에서 P(연령 | 성별, I)를 공동 분배하여 학습 

![image](https://user-images.githubusercontent.com/115753833/230000426-a7e96077-53e4-4592-8abb-304837809ff5.png)

- $Y_g, Y_a, P_g, P_a$: 실측값 성별/연령 
- $|C_i|, |C_j|$: 성별 클래스 i 또는 연령 클래스 j로 레이블링된 샘플 수
- $C_t$: 배치의 크기

<br><br>

## Experiments
### 1) Datasets and Preprocessing 
- Datasets
  - RSNA dataset: 12611개의 X-ray사진 (Train:Validation:Test = 0.8:0.1:0.1)
  - Tongji dataset: 0세에서 22세 사이의 1385개 X-ray사진(여성 768개, 남성 617개) 

- Preprocessing
  - 해상도: 500 x 500 픽셀로 축소
  - data augmentation

<br>

### 2) Implementation 
- Python 3.6/ TensorFlow 1.7
- batch size: 16
- optimizer: ADAM
- learning rate : 0.001
<br>

```
◆ 모델 특징
- 처음 두 개의 컨볼루션 블록: 3 x 3 커널

- 블록 5: 성별 분류(이진 분류)
  - softmax 함수
  - 256개의 뉴런으로 dense layer사용
  - 추가적인 성별 입력 블록은 64개의 뉴런 사용

- 블록 6: 연령 분류
  - 각각 512개와 256개의 노드가 있는 두 개의 Dense layers
  - 정규화된 softmax 함수
```
<br>

### 3) Results and Analysis 

🔸 **다른 모델과 비교** : VGG16, ResNet50, Inception V4 등

<img src="https://user-images.githubusercontent.com/115753833/230007056-d3b635cd-f68a-463b-b966-bfbb3cb9e543.png" width="570">

<br>

🔸 **다양한 동결 방법을 사용한 전이 학습 결과 비교**

<img src="https://user-images.githubusercontent.com/115753833/230013127-de2c14db-4d32-4e95-81f9-a6318596a886.png" width="700">
&ensp;→ 블록 1-3에서 MAD(mean absolute difference)가 0.36년이라는 최상의 결과를 달성

<br><br>

🔸 **다양한 구성요소별 효과 검증**
- IncRes 모듈에서 shortcuts 제거 시: MAD 0.571년
- CBAM 모듈이 없을 경우: MAD 0.578년
- 성별 분류와 관련 손실을 뺄 경우: MAD 0.578년

<br><br>

🔸 **CBAM 모듈 유무 비교**

&ensp;: CBAM이 훈련된 모델에 미치는 영향을 시각화하기 위해 블록 4에서 학습한 활성화된 기능의 열 지도

<img src="https://user-images.githubusercontent.com/115753833/230016155-e40e03a9-ca37-48ed-ad85-8e745e26f5dc.png" width="700">

&ensp;→ 오른쪽은 TW 방법으로 조사한 ROI와 유사한 주요 위치 강조됨 <br> 
&ensp;→ 왼쪽은 attention mechanisms 없어 넓은 영역에 걸쳐 퍼져있음

<br><br>

🔸 **각 데이터 셋의 성별 동시 학습 유무에 따른 예측 오차 분포 비교**

<img src="https://user-images.githubusercontent.com/115753833/230014899-5f3153de-d481-4d6b-8d52-c4cefa333068.png" width="700">
&ensp;→ RSNA와 Tongji 데이터 모두 예측이 기본적으로 편향되지 않고 오차의 분포가 비슷 <br>
&ensp;→ TJ-Net에 성별 동시 학습을 추가하면 대부분의 연령 계층에 대해 더 정확한 예측

<br><br>

🔸 **joint learning(성별입력)이 적용된 모델에서 사용되는 가중치 행렬의 시각화 결과**
&ensp;:
<img src="https://user-images.githubusercontent.com/115753833/230020389-41e26b31-1934-44b2-b304-1035dfc59d9c.png" width="700">

&ensp;→ 회색 척도가 가중치의 강점을 나타냄 <br>
&ensp;→ Joint learning이 적용된 모델에서 성별 입력이 뼈 연령에 미치는 영향이 더 강화

<br><br>

## Conclusions 
```
본 논문에서는 자동 방사선골 연령 평가를 위해 특별히 설계된 딥러닝 신경망인 TJ-Net을 제안하였다.
TJ-Net에서는 attention module이 인간이 탐색한 초점(focal points)과 유사한 특징을 찾아내는 데 도움이 되었고, 
성별 레이블에 대한 조건부 연령 예측을 향상시키기 위한 Joint sex/age learning이 사용되었다.
```

- RSNA 데이터에서 학습한 저수준 특징이 Tongji데이터로 전이될 수 있다는 것이 입증
- 제안된 모델은 RSNA와 Tongji 데이터에서 각각 0.41년과 0.36년의 MAD (Mean Absolute Deviation)를 기록

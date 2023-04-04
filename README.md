# Project3 : 손 엑스레이 분석을 통한 골 연령 및 키 성장 예측
<img src="https://user-images.githubusercontent.com/115753833/228257283-e1f854c2-2ca1-4847-baad-8930594c0658.png" width="400">

-----
## 관련 논문

- [TW3](https://github.com/ranyjoon/Project3/blob/main/%EB%85%BC%EB%AC%B8%EB%A6%AC%EB%B7%B0/TW3.md): 이미지 추출(OpenCV) 및 라벨링 방법 제시
- [YOLO](https://github.com/ranyjoon/Project3/blob/main/%EB%85%BC%EB%AC%B8%EB%A6%AC%EB%B7%B0/YOLO.md): 이미지 라벨링(객체탐지)
-----
<br>

## 1. 개요
### 1) 데이터
 - X-ray 검사 이미지(골 연령 판독 검사 기준)
   - 손목을 포함한 왼손 X-ray
   - 만 2세~17세
   - 남자 665명/ 여자 572명
- 검사대상자의 기본 신체 검사 기록
- 전문의 2명의 골연령 판독 데이터
- 2017 소아 청소년 성장도표 (출처: 질병관리청)
<br>

### 2) 제작환경 및 모듈사용
<img src="https://user-images.githubusercontent.com/115753833/228258560-2890c929-baa9-430f-8a7f-469528e453a4.png" width='200'>
<br>

### 3) 주제선정 배경
- **이슈**: 아이들의 키성장과 호르몬 치료에 대한 관심증대, 키성장 클리닉에 대한 수요증가
- **주요점**: 현재 대상 소아가 정상적으로 자라고 있는지 파악하고 키 성장 예측하는 것
- **골 연령 측정의 중요점**: 
  - 키성장과정 진단, 잔여성장 예측
  - 호르몬 치료나 성장관련 질환 치료에 도움
  - 골연령, 키성장 예측은 전문적 지식과 많은 경험의 축적 요구
  - 시간과 비용이 많이 소요됨

#### ➡ 효율적으로 골 연령을 예측하여 성장 가능 키를 예측하는 도구 필요

<br>

### 4) 프로젝트 진행 순서
<img src="https://user-images.githubusercontent.com/115753833/228264806-68f26327-9a10-48a0-affe-b869a86b6a55.png" width='700'>
<br>

## 2. 이미지 전처리: OpenCV 활용
### 1) X-ray에서 손 영역만 추출
<img src="https://user-images.githubusercontent.com/115753833/228265668-164f3dc7-a27a-47c2-a86f-d8d5f2be7da1.png" width="49%"><img src="https://user-images.githubusercontent.com/115753833/228265895-704d1f23-1ab0-4069-92cf-eeaa9a12d96a.png" width="49%">

<br>

### 2) 손목 회전: 정확도 높이기
<img src="https://user-images.githubusercontent.com/115753833/228266456-6a6537c1-f61f-4929-bb57-cd9b0d3bc43e.png" width="550">
<br>

### 3) 모폴로지 연산을 통한 뼈 도출: TOPHAT 연산 사용
<img src="https://user-images.githubusercontent.com/115753833/228592281-d9efa145-140c-4f1c-bf9e-02568f325bb9.png" width="500">

```
◆ 모폴로지 연산이란?
  • 팽창과 수축의 형태학적 변환을 결합 하여 사용
  • 연산에 도움: 연산 시 형태가 변형되기도 하므로 두 방법을 결합할 경우 오류가 적음
  
◆ TOPHAT옵션 사용 이유
  • 형태의 변형은 줄이고, 밝기가 크게 튀는 부분만을 강조
  • 뼈 도출이 가장 잘됨
```
> <img src="https://user-images.githubusercontent.com/115753833/228268282-4cfd632a-717a-47c8-bb0c-1bd1bd72bc86.png" width="50%">

<br>

### 4) 최종 마스크 생성 및 비트연산을 통한 뼈 도출
<img src="https://user-images.githubusercontent.com/115753833/228599337-064ec332-4de1-4e68-a5c6-c28d8af03be2.png" width="66%"><img src="https://user-images.githubusercontent.com/115753833/228599894-d1462338-0086-49b7-b804-9c5da88760d6.png" width="5%"><img src="https://user-images.githubusercontent.com/115753833/228599566-08dd6222-894d-4094-a18a-1c07a4bf7909.png" width="28%">
<br>

```
◆ 히스토그램 균등화: CLAHE
    • 이미지를 작은 블록으로 나눔
    • 블록별 히스토그램 균일화
    • 이미지 전체에 히스토그램 균일화 달성
```
<br>

## 3. 이미지 라벨링
### 1) 관절 탐색을 위해 골연령 측정 방법 연구: TW3
  - [관련 논문](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8660640) / [논문리뷰 참조](https://github.com/ranyjoon/Project3/blob/main/%EB%85%BC%EB%AC%B8%EB%A6%AC%EB%B7%B0/TW3.md)
  - 측정요소: 성별 / 왼손 엄지,중지,소지 뼈 11개 + 손목 뼈 2개
  - 측정방법: 골 성숙점수 산출 → 골 연령 표를 통해 골연령 측정
  - 장점: 골연령표가 0.1년 단위로 구분되므로 정확도가 높고, 객관적 평가가 가능
  - 단점: 성숙점수 산출 및 골 연령 표 비교에 비교적 평가시간이 긺
<br>

### 2) TW3를 활용하여 객체 선정
<img src="https://user-images.githubusercontent.com/115753833/228273470-50e2a73e-4f7d-4349-b120-78fc8ae5113f.png" width="700">
<br>

### 3) roboflow를 활용한 관절 Annotation(샘플 객체)
<img src="https://user-images.githubusercontent.com/115753833/228274409-42822a34-f77e-4823-a25a-4316dfb86a12.png" width="700">
<br>

### 3) YOLOv5를 활용한 관절 객체 탐지(모델 적용)
- [YOLO 논문](https://arxiv.org/pdf/1506.02640.pdf) / [논문 리뷰 참조](https://github.com/ranyjoon/Project3/blob/main/%EB%85%BC%EB%AC%B8%EB%A6%AC%EB%B7%B0/YOLO.md)
- **기본값 설정**
  - YOLOx (mAP50: 0.990 / mAP50-95: 0.521)
  - YOLOm (mAP50: 0.991 / mAP50-95: 0.512)
- **YOLOx/YOLOm Fine Tuning**

  <img src="https://user-images.githubusercontent.com/115753833/228275594-794ba07d-4a7b-4431-a8a7-c3e2c7b0b9e9.png" width="700">
  <img src="https://user-images.githubusercontent.com/115753833/228276697-5444914b-0f30-469b-9a07-11af5d601db1.png" width="700">
<br>

### 4) 이미지 라벨링 결과
<img src="https://user-images.githubusercontent.com/115753833/228277304-463272eb-ca02-4f87-9c5a-ce68b11ef4ed.png" width="700">
<br>

## 4. 골 연령 예측
### 1) 데이터 준비
<img src="https://user-images.githubusercontent.com/115753833/228277900-aaf1c8fc-f56b-4b88-883e-2977eb69adf3.png" width="700">
<br>

### 2) 모델 구축: TJ-Net
- **TJ-Net관련 논문 참조**
  - TJ-Net은 이미지 특징을 학습하면서, 이미지의 특정 영역에 더 많은 중요도를 부여하여 골연령을 측정
  - Self-attention-mechanism:     
    - 상대적 중요도 계산
    - 특징 맵의 각 위치를 가중치로 조정 = 더 많은 중요도
<br>

- **모델 구축**
<br>

**`전체 구조`**
<br>

<img src="https://user-images.githubusercontent.com/115753833/228278952-763b622b-4b66-431f-91e5-419ce8ef4747.png" width="700">
<br>

**`각 관절(라벨) 분석`**
<br>

<img src="https://user-images.githubusercontent.com/115753833/228279612-83c0527e-156b-4b73-9546-7948876ce226.png" width="700">
<br>

### 3) Fine Tuning 결과(활성화함수, 옵티마이저 변경)
<img src="https://user-images.githubusercontent.com/115753833/228281257-88ff7ed7-fdbd-477a-bdc9-3f209973a89c.png" width="700">

```
◆ 검증 지표
  • MSE: 손실 값으로 평가를 하게 되며, MSE는 오차의 민감도가 높아 회귀 예측 시 중요한 평가 지표로 사용
  • MAE(보조수단): 10진수로 표기 되므로 오차의 범위를 직관적으로 알기 쉬워 보조적인 평가 지표로 사용
```
<br>

### 4) 최적모델 학습 결과
<img src="https://user-images.githubusercontent.com/115753833/228281671-3b7770d7-67eb-4494-b969-83701e148986.png" width="700">
<br>

## 5. 키 성장 예측(만 18세 기준)
### 1) 키 성장 공식 성립
<img src="https://user-images.githubusercontent.com/115753833/228281899-d44ec0b0-00c2-42d3-9512-d1fe993726bc.png" width="700">
<br>

### 2) 함수화 하여 계산
<img src="https://user-images.githubusercontent.com/115753833/228282259-0e6a1011-2b3b-4e09-ab01-21b8264a5bd4.png" width="700">
<br>

### 3) 백분위 도표 그리기
<img src="https://user-images.githubusercontent.com/115753833/228282894-5ea59005-ab56-4249-b40e-35e66f4f7646.png" width="700">
<br>

## 6. 결과
- **기대효과**: 
  - GUI를 통해 전문의나 환자가 쉽게 이용 가능하도록 함
  - 딥러닝 학습을 통한 시간 절약
  - 단계축소로 인한 비용 유리
- **한계점**:
  - 현재 모델로 전문의보다 오차범위가 1개월 정도 더 크게 나오므로 정확도 개선 필요
  - 최종 키 예측 시 외부적 변수를 고려하기 어려움
  - 현재 표본의 최종 키 데이터가 없어 정확도 판별의 어려움
  
  






  





 






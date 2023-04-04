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

🔸 골 연령 측정 기법
1. the Greulich and Pyle method(GP기법): 일반 방사선 전문의의 판단기법
  - X-ray이미지와 유사한 이미지를 시각적으로 검색하여 일치하는 연령을 Atlas에서 검색
  - 기존 Atlas 방식과 개인 판단에 의존
  - 동일한 방사선 사진에서 다른 예측 가능

2. the Tanner and Whitehouse method(TW기법)  
  - 더 구체적인 방법으로 방사선 사진의 특정 부위를 평가
  - 체계적인 점수 매기기를 위한 상세한 특징 집합을 도입하여 계산

➡ 인지 편향적 오류를 줄이기 위해 TW기법 사용




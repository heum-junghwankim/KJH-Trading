# Buy/Sell Volume + Abnormal Volume

트레이딩뷰에서 사용할 수 있는 Pine Script 지표 설명서입니다.

대상 스크립트:
- [`main.pine`](/Users/kjh/Workspace/KJH-Trading/pinescript/Volume%20Trancker/main.pine)

## 개요

이 지표는 전체 거래량을 단순히 하나의 막대로만 보는 대신, 캔들 구조를 기준으로 `Buy Volume`과 `Sell Volume`을 나누어 표시합니다.

여기에 최근 평균 거래량 대비 비정상적으로 큰 거래량이 발생했는지도 함께 구분해서, 평소 거래량과 강한 거래량 유입 구간을 한눈에 확인할 수 있도록 구성된 스크립트입니다.

## 트레이딩뷰 적용 방법

1. 트레이딩뷰에서 `Pine Editor`를 엽니다.
2. [`main.pine`](/Users/kjh/Workspace/KJH-Trading/pinescript/Volume%20Trancker/main.pine) 파일의 전체 내용을 복사합니다.
3. Pine Editor에 붙여넣습니다.
4. `Add to chart` 또는 `차트에 추가`를 클릭합니다.
5. 필요하면 `Save`로 개인 스크립트로 저장합니다.

## 예시 화면

![지표 예시 화면](./img.png)

위 예시 화면에서는 아래 요소를 확인할 수 있습니다.

- 회색 막대: 일반 `Sell Volume`
- 흰색 막대: 일반 `Buy Volume`
- 빨간색 막대: 비정상 거래량이 동반된 `Sell Volume`
- 연두색 막대: 비정상 거래량이 동반된 `Buy Volume`

즉, 거래량 크기 자체뿐 아니라, 현재 봉에서 어느 쪽 압력이 상대적으로 컸는지와 비정상 거래량 발생 여부를 함께 볼 수 있습니다.

## 기본 정보

- Pine Script 버전: `@version=5`
- 표시 위치: 별도 패널
- 포맷: `format.volume`
- 지표명: `Buy/Sell Volume + Abnormal Volume`

## 주요 기능

### 1. Buy / Sell Volume 분리 계산

스크립트는 캔들의 고가, 저가, 종가 위치를 바탕으로 거래량을 매수 우위와 매도 우위로 나누어 계산합니다.

- `buyVolume`: 종가가 저가 대비 얼마나 위에서 마감했는지 기준으로 계산
- `sellVolume`: 종가가 고가 대비 얼마나 아래에서 마감했는지 기준으로 계산

고가와 저가가 같은 특수한 봉에서는 0으로 처리해 분모 0 오류를 방지합니다.

### 2. 비정상 거래량 감지

- `length`: 평균 거래량을 계산할 비교 봉 수
- `multiplier`: 평균 대비 얼마나 커야 비정상 거래량으로 볼지 정하는 배수

현재 거래량이 아래 조건을 만족하면 비정상 거래량으로 판단합니다.

- `volume > ta.sma(volume, length) * (1 + multiplier)`

예를 들어:
- `length = 20`
- `multiplier = 1.0`

이면 최근 20개 봉 평균 거래량보다 2배를 초과하는 거래량이 발생했을 때 비정상으로 표시됩니다.

### 3. 색상 구분

기본 색상 설정:

- `normalBuyColor`: 일반 Buy 거래량 색상
- `normalSellColor`: 일반 Sell 거래량 색상
- `abnormalBuyColor`: 비정상 Buy 거래량 색상
- `abnormalSellColor`: 비정상 Sell 거래량 색상

비정상 거래량이 감지되면 일반 색상 대신 비정상 색상이 적용됩니다.

### 4. 거래량 시각화

아래 두 개의 컬럼 plot이 함께 표시됩니다.

- `Sell Volume`: 전체 거래량 막대
- `Buy Volume`: 매수 우위로 계산된 거래량 막대

이 방식으로 바닥에는 전체 거래량 흐름이 유지되고, 그 위에 Buy 성격의 거래량이 겹쳐 표시되어 상대 강도를 직관적으로 볼 수 있습니다.

## 추천 사용 흐름

1. 현재 봉의 전체 거래량 크기를 먼저 확인합니다.
2. Buy Volume 비중이 큰지, Sell Volume 성격이 강한지 확인합니다.
3. 비정상 색상으로 바뀐 봉이 있는지 봅니다.
4. 추세 전환 구간이나 돌파 구간에서 비정상 거래량이 동반되는지 확인합니다.

이 지표는 진입 신호 자체를 주는 스크립트라기보다, 거래량의 성격과 강도를 보조적으로 해석하는 데 적합합니다.

## 주의사항

- 실제 체결 데이터를 매수/매도로 직접 분리한 것이 아니라, 캔들 구조를 기반으로 비중을 추정하는 방식입니다.
- `multiplier`를 너무 낮게 두면 비정상 거래량 표시가 과도하게 많아질 수 있습니다.
- 종목과 타임프레임에 따라 적절한 `length`, `multiplier` 값이 달라질 수 있습니다.
- 거래량이 적은 종목에서는 색상 신호가 왜곡되거나 해석 가치가 낮아질 수 있습니다.

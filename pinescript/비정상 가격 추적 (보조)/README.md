# cRSI + MFI Gap Highlight

트레이딩뷰에서 사용할 수 있는 Pine Script 지표 설명서입니다.

대상 스크립트:
- [`main.pine`](/Users/kjh/Workspace/KJH-Trading/pinescript/RSI%20MFI%20Tracker/main.pine)

## 개요

이 지표는 하나의 보조지표 패널 안에 아래 기능을 함께 제공합니다.

- cRSI와 MFI를 동시에 표시
- 최근 cRSI 분포를 기준으로 한 동적 밴드 표시
- cRSI와 MFI 간 괴리가 커질 때 배경색 강조
- 배경색 신호를 MACD와 함께 해석할 수 있는 구조 제공

차트 아래 보조지표 영역에서 가격 모멘텀과 자금 흐름의 차이를 빠르게 확인하고, MACD와 함께 반등 또는 조정 후보 구간을 해석하려는 목적에 맞춰 구성된 스크립트입니다.

## 트레이딩뷰 적용 방법

1. 트레이딩뷰에서 `Pine Editor`를 엽니다.
2. [`main.pine`](./main.pine) 파일의 전체 내용을 복사합니다.
3. Pine Editor에 붙여넣습니다.
4. `Add to chart` 또는 `차트에 추가`를 클릭합니다.
5. 필요하면 `Save`로 개인 스크립트로 저장합니다.

## 예시 화면

![지표 예시 화면](./img.png)

위 예시 화면에서는 아래 요소를 한 번에 확인할 수 있습니다.

- 노란색 선: `cRSI`
- 파란색 선: `MFI`
- 회색 밴드: 최근 cRSI 분포를 기준으로 만든 동적 밴드
- 빨간 점선: 과매수 기준선 `80`
- 회색 점선: 중립선 `50`
- 초록 점선: 과매도 기준선 `20`
- 노란색 계열 배경: `cRSI > MFI` 괴리 구간
- 파란색 계열 배경: `MFI > cRSI` 괴리 구간
- 하단 MACD: 배경색 신호를 추가 확인하는 참고 지표

즉, 한 화면에서 cRSI와 MFI의 상대 강도, 과열/침체 위치, 괴리 발생 구간, 그리고 MACD 확인 신호를 함께 볼 수 있습니다.

## 기본 정보

- Pine Script 버전: `@version=6`
- 표시 위치: `overlay=false`
- 지표명: `cRSI + MFI Gap Highlight`

## 주요 기능

### 1. cRSI 계산

- `Source`: RSI 계산 기준 가격
- `cRSI Dominant Cycle`: 순환 길이 추정값
- `cRSI Vibration`: cRSI 반응 속도
- `cRSI Leveling %`: 동적 밴드 계산용 퍼센타일 비율

cRSI는 일반 RSI보다 가격 반응 속도를 더 빠르게 반영하도록 구성되어 있으며, 가격 모멘텀의 선행 움직임을 보기 위한 용도로 사용합니다.

### 2. MFI 계산

- `MFI Length`: 자금 흐름 계산 길이

MFI는 거래량이 반영된 오실레이터로, 단순 가격 반응이 아니라 실제 자금 유입/유출 강도를 확인하는 데 사용합니다.

### 3. cRSI 동적 밴드

- 최근 `cyclicmemory` 구간의 cRSI 값을 기준으로 상단 밴드와 하단 밴드를 계산합니다.
- 밴드는 고정 80/20선과 별도로, 현재 종목과 타임프레임의 상대적인 cRSI 분포를 보여줍니다.

최근 코드 개선 사항:

- 초기 바에서 `na` 값을 `0`으로 치환하던 부분을 제거했습니다.
- 동적 밴드 계산 시 실제 유효한 `cRSI` 표본 수만 사용하도록 수정했습니다.
- 유효 데이터가 부족한 초반 구간에서는 밴드가 왜곡되지 않도록 `na` 기반으로 처리했습니다.

### 4. cRSI-MFI 괴리 배경 강조

- `cRSI-MFI Gap Threshold`: 배경색을 켜는 최소 괴리값
- `Show Gap Background`: 배경색 표시 여부
- `Gap Color (cRSI > MFI)`: cRSI가 더 높을 때 표시할 배경색
- `Gap Color (MFI > cRSI)`: MFI가 더 높을 때 표시할 배경색
- `Gap Background Transparency`: 배경 투명도

조건이 충족되면:

- `cRSI > MFI`일 때는 노란색 계열 배경으로 가격 모멘텀이 자금 흐름보다 앞서는 상태를 강조합니다.
- `MFI > cRSI`일 때는 파란색 계열 배경으로 자금 흐름이 가격 모멘텀보다 강한 상태를 강조합니다.

또한 `cRSI` 또는 `MFI`가 아직 준비되지 않은 상태에서는 배경색이 켜지지 않도록 보정되어 있습니다.

## MACD와 같이 보는 방법

이 지표는 배경색만 단독으로 보기보다, 아래 MACD와 같이 볼 때 해석이 더 쉬워집니다.

참고 MACD:
- [CM MACD Custom Indicator - Multiple Time Frame - V2](https://kr.tradingview.com/script/XFr7xHqZ-CM-MACD-Custom-Indicator-Multiple-Time-Frame-V2/)

### 1. 저점에서 반등 찾기

- `MFI > cRSI` 배경이 나오고 상단 지표가 `20` 근처면 먼저 반등 후보로 봅니다.
- 이때 MACD 막대 음수가 점점 짧아지거나 MACD선이 위로 꺾이면 반등 가능성이 커집니다.
- 한마디로 `저점 배경색 + MACD 바닥 확인 = 롱 후보`로 해석하면 됩니다.

### 2. 고점에서 조정 찾기

- `cRSI > MFI` 배경이 나오고 상단 지표가 `80` 근처면 과열 후보로 봅니다.
- 이때 MACD 막대 양수가 줄어들거나 MACD선이 아래로 꺾이면 힘이 빠지는 구간일 수 있습니다.
- 한마디로 `고점 배경색 + MACD 둔화 = 익절 또는 숏 후보`로 해석하면 됩니다.

### 3. 중립 구간은 약하게 보기

- 상단 지표가 `40~60` 근처인데 배경색만 잠깐 나오면 강한 신호로 보지 않습니다.
- MACD도 같이 애매하면 관망하는 편이 낫습니다.
- 한마디로 `중립 구간 배경색 단독 신호는 약함`으로 보면 됩니다.

## 추천 사용 흐름

1. 먼저 상단 패널에서 배경색이 나온 위치를 봅니다.
2. 그 위치가 과매수권인지 과매도권인지 확인합니다.
3. `cRSI > MFI`인지 `MFI > cRSI`인지로 선행 주체가 가격인지 자금인지 판단합니다.
4. 하단 MACD 히스토그램이 확대 중인지 축소 중인지 확인합니다.
5. 마지막으로 MACD 라인과 시그널 라인의 방향 전환 여부로 실행 타이밍을 잡습니다.

요약하면:

- `저점권 + MFI > cRSI 배경 + MACD 하락 둔화` = 반등 준비 가능성
- `고점권 + cRSI > MFI 배경 + MACD 상승 둔화` = 조정 또는 익절 가능성
- `중립권 배경색` 단독 신호 = 우선순위 낮음

이 지표는 확정 진입 신호보다는 후보 구간 탐색 용도로 보는 편이 더 적절합니다.

## 입력값 요약

### cRSI 관련

- `Source`
- `cRSI Dominant Cycle`
- `cRSI Vibration`
- `cRSI Leveling %`

### MFI 관련

- `MFI Length`

### 괴리 배경 관련

- `cRSI-MFI Gap Threshold`
- `Show Gap Background`
- `Gap Color (cRSI > MFI)`
- `Gap Color (MFI > cRSI)`
- `Gap Background Transparency`

## 주의사항

- 자동 매매 전략이 아니라 시각화 중심의 보조지표입니다.
- 강한 추세장에서는 과매수/과매도와 괴리 신호가 오래 유지될 수 있습니다.
- `gapThreshold`를 너무 낮추면 배경색이 과도하게 많아져 해석력이 떨어질 수 있습니다.
- 가격 구조, 지지/저항, 거래량, 상위 타임프레임 방향과 함께 보는 것이 좋습니다.

## 참고 자료

- RSI/MFI 괴리 인디케이터: [`main.pine`](/Users/kjh/Workspace/KJH-Trading/pinescript/RSI%20MFI%20Tracker/main.pine)
- 예시 이미지: `img.png`
- MACD 참고 스크립트: [CM MACD Custom Indicator - Multiple Time Frame - V2](https://kr.tradingview.com/script/XFr7xHqZ-CM-MACD-Custom-Indicator-Multiple-Time-Frame-V2/)

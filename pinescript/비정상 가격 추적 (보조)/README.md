# cRSI + MFI Reversal Risk Signal

트레이딩뷰에서 사용할 수 있는 Pine Script 보조지표 설명서입니다.

대상 스크립트:
- [`main.pine`](./main.pine)

## 개요

이 지표는 별도 패널에서 아래 내용을 함께 보여줍니다.

- `cRSI`와 `MFI` 동시 표시
- 최근 `cRSI` 분포 기반 동적 밴드
- `cRSI - MFI` 괴리 배경 강조
- `Bearish Reversal Risk` / `Bullish Reversal Risk` 라벨
- 강도별 알람 조건

핵심 목적은 `반전 위험 후보 압축`입니다.

단순히 괴리가 큰지만 보는 것이 아니라, 아래 조건을 함께 점수화합니다.

- 괴리 크기
- 가격 연장 여부
- EMA 대비 가격 과신장 여부
- 거래량 통과 여부
- `cRSI` 극단 구간 진입 여부
- 괴리 축소 여부
- `cRSI` 또는 `MFI` 턴 발생 여부

## 트레이딩뷰 적용 방법

1. 트레이딩뷰에서 `Pine Editor`를 엽니다.
2. [`main.pine`](./main.pine) 파일 전체를 복사합니다.
3. Pine Editor에 붙여넣습니다.
4. `차트에 추가`를 누릅니다.
5. 필요하면 저장합니다.

## 예시 화면

![지표 예시 화면](./img.png)

## 어떻게 읽는지

주요 요소는 아래와 같습니다.

- 노란색 선: `cRSI`
- 파란색 선: `MFI`
- 회색 밴드: 최근 `cRSI` 분포 기반 동적 상단/하단 밴드
- 노란색 계열 배경: `cRSI > MFI` 괴리 구간
- 파란색 계열 배경: `MFI > cRSI` 괴리 구간
- 라벨 `H / M / L`: 최종 반전 위험 강도

해석은 아래처럼 보면 됩니다.

- 노란 배경 = 가격 모멘텀이 자금 흐름보다 앞선 상태
- 파란 배경 = 자금 흐름 대비 가격이 더 눌린 상태
- `H / M / L` = 반전 위험 강도
  - `H`: 높음
  - `M`: 중간
  - `L`: 낮음

이 지표는 단독 진입 신호라기보다, `지금 구간이 되돌림 또는 반전 위험이 커지는가`를 먼저 거르는 용도입니다.

## 기본 정보

- Pine Script 버전: `@version=6`
- 표시 위치: `overlay=false`
- 지표명: `cRSI + MFI Reversal Risk Signal`
- short title: `cRSI+MFI RRS`

## 신호 구조

### 1. 배경색

배경은 괴리 방향만 보여줍니다.

- `cRSI > MFI` 이고 차이가 `Gap Background Threshold` 이상이면 노란 계열 배경
- `MFI > cRSI` 이고 차이가 `Gap Background Threshold` 이상이면 파란 계열 배경

즉, 배경은 `경고 구간`입니다. 아직 최종 신호는 아닙니다.

### 2. Reversal Risk 라벨

라벨은 배경 구간 안에서 추가 조건까지 통과했을 때만 표시됩니다.

- `Bearish Reversal Risk`
  - `cRSI > MFI` 괴리 배경
  - 양봉에서만 발생
  - 과열 이후 되밀릴 위험 후보

- `Bullish Reversal Risk`
  - `MFI > cRSI` 괴리 배경
  - 음봉에서만 발생
  - 과매도 이후 되돌릴 위험 후보

즉 현재 기준은 아래와 같습니다.

- `양봉에서 Bearish`
- `음봉에서 Bullish`

### 3. 점수화 기준

각 방향별로 아래 요소를 점수화합니다.

- 괴리 배경 진입 여부
- 약한 괴리 / 강한 괴리
- 최근 `trendLength` 기준 가격 연장 여부
- 거래량 평균 통과 여부
- `cRSI`가 지정 구간 또는 동적 밴드 극단부에 있는지
- 괴리가 줄어드는지
- `cRSI` 또는 `MFI`가 실제로 꺾이기 시작했는지

강도는 최종적으로 아래처럼 단순화됩니다.

- `H`: 높은 반전 위험
- `M`: 중간 반전 위험
- `L`: 낮은 반전 위험

### 4. 중복 신호 제한

같은 괴리 배경 구간에서는 신호를 한 번만 표시합니다.

- 새로운 노란 배경이 시작되면 `Bearish` 신호 가능 상태 초기화
- 새로운 파란 배경이 시작되면 `Bullish` 신호 가능 상태 초기화
- 같은 배경 구간 안에서는 첫 최종 신호만 표시

또한 `barstate.isconfirmed` 기준으로 확정봉에서만 최종 신호가 발생합니다.

## 추천 사용 흐름

1. 먼저 배경색으로 괴리 방향을 확인합니다.
2. 현재 `cRSI`가 `80/20` 또는 동적 밴드 극단부 근처인지 봅니다.
3. `H / M / L` 라벨이 붙는지 확인합니다.
4. `H`부터 우선 감시하고, `M`, `L`은 보조 후보로 봅니다.
5. 실제 매매 판단은 가격 구조, 추세, 거래량, 상위 타임프레임과 함께 확인합니다.

간단히 해석하면:

- 파란 배경 + `H/M/L` = 눌림 이후 반등 위험 증가 후보
- 노란 배경 + `H/M/L` = 과열 이후 조정 위험 증가 후보
- 배경만 있고 라벨 없음 = 아직 조건이 덜 모인 상태

## 알람

이 스크립트에는 `alertcondition(...)`이 포함되어 있어서 트레이딩뷰 알람으로 바로 사용할 수 있습니다.

제공되는 알람:

- `Bearish Reversal Risk`
- `Bullish Reversal Risk`
- `Bearish Reversal Risk (3)`
- `Bearish Reversal Risk (2)`
- `Bearish Reversal Risk (1)`
- `Bullish Reversal Risk (3)`
- `Bullish Reversal Risk (2)`
- `Bullish Reversal Risk (1)`

강한 신호만 받고 싶으면 `(3)` 위주로 쓰면 됩니다.

## 입력값 요약

### cRSI 관련

- `Source`
- `cRSI Dominant Cycle`
- `cRSI Vibration`
- `cRSI Leveling %`

### MFI 관련

- `MFI Length`

### 선 표시 관련

- `cRSI Color`
- `MFI Color`
- `cRSI Line Width`
- `MFI Line Width`

### 괴리 배경 관련

- `Show Gap Background`
- `Gap Background Threshold`
- `Gap Color (cRSI > MFI)`
- `Gap Color (MFI > cRSI)`
- `Gap Background Transparency`

### Reversal Risk 관련

- `Show Reversal Risk Labels`
- `Weak Gap Threshold`
- `Strong Gap Threshold`
- `Bearish Risk cRSI Zone`
- `Bullish Risk cRSI Zone`
- `Volume Average Length`
- `Volume Multiplier`
- `Trend Length`
- `Price Stretch (%)`
- `Use Gap Fade Condition`
- `Gap Fade Lookback`
- `Risk Label Transparency`
- `Bearish Label Offset`
- `Bullish Label Offset`

## 주의사항

- 자동 매매 전략이 아니라 보조 해석용 지표입니다.
- `Reversal Risk`는 확정 반전이 아니라 `반전 위험 증가 후보`를 의미합니다.
- `Gap Background Threshold`, `Weak Gap Threshold`, `Strong Gap Threshold`를 너무 낮추면 신호가 과도하게 많아질 수 있습니다.
- 거래량이 적거나 횡보가 긴 종목에서는 괴리와 신호가 자주 흔들릴 수 있습니다.
- 가격 구조, 추세, 지지/저항, 상위 타임프레임 방향과 반드시 같이 봐야 합니다.

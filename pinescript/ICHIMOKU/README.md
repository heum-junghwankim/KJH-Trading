# Advanced Ichimoku

트레이딩뷰용 Pine Script Ichimoku 확장 버전입니다.

대상 스크립트:
- [`advanced-ichimoku.pine`](./advanced-ichimoku.pine)

이 버전은 기본 Ichimoku 계산을 유지하면서 아래 3가지를 추가했습니다.

- 이미지 기준 기본 표시 상태를 맞춘 라인/클라우드 구성
- `래깅 스팬 vs 래깅 위치 캔들 종가` + `현재 컨버전 라인 vs 베이스 라인` 조합의 매수/매도 신호
- 매수 신호 / 매도 신호를 각각 1개 시리즈로 관리하는 표시 구성

## 기본 표시값

기본값은 요청하신 이미지 기준으로 맞췄습니다.

| 항목 | 기본값 |
| --- | --- |
| Conversion Line | 표시, 핑크, 2px |
| Base Line | 표시, 라임, 2px |
| Lagging Span | 표시, 노랑, 2px |
| Leading Span A | 숨김 |
| Leading Span B | 숨김 |
| Kumo Cloud Upper Line | 숨김 |
| Kumo Cloud Lower Line | 숨김 |
| Cloud Fill | 표시, 기본 투명도 45% |
| 매수 신호 | 표시, 하늘색, `삼각형`, `캔들 아래`, 고정 `작게` |
| 매도 신호 | 표시, 분홍색, `역삼각형`, `캔들 위`, 고정 `작게` |

참고:
- 신호는 `plotshape()`를 사용해 `size.small`로 고정했습니다.
- 색상, 모양, 위치는 TradingView 스타일 탭의 `매수 신호` / `매도 신호` 항목에서 조정합니다.
- 크기는 입력으로 두지 않았습니다.

## 신호 로직

### 매도 신호

매도 신호는 아래 두 묶음이 동시에 만족할 때 발생합니다.

1. `래깅 스팬`이 `래깅 스팬이 존재하는 캔들의 종가`를 하향 이탈하거나, 이미 그 아래에 있음
2. `현재 컨버전 라인`이 `베이스 라인`을 데드 크로스하거나, 이미 그 아래에 있음

현재 봉 기준 계산은 아래처럼 해석했습니다.

- 래깅 스팬: 현재 `close`
- 래깅 위치 캔들 종가: `close[displacement - 1]`
- 래깅 약세 확인: `ta.crossunder(close, close[displacement - 1])` 또는 `close < close[displacement - 1]`
- 전환선 약세 확인: `ta.crossunder(conversionLine, baseLine)` 또는 `conversionLine < baseLine`

### 매수 신호

매수 신호는 위의 정확한 반대입니다.

1. `래깅 스팬`이 `래깅 스팬이 존재하는 캔들의 종가`를 상향 돌파하거나, 이미 그 위에 있음
2. `현재 컨버전 라인`이 `베이스 라인`을 골든 크로스하거나, 이미 그 위에 있음

현재 봉 기준 계산은 아래처럼 해석했습니다.

- 래깅 강세 확인: `ta.crossover(close, close[displacement - 1])` 또는 `close > close[displacement - 1]`
- 전환선 강세 확인: `ta.crossover(conversionLine, baseLine)` 또는 `conversionLine > baseLine`

## 신호 순서 제한

같은 방향 신호가 연속으로 찍히지 않게 제한했습니다.

- 매도 신호가 나온 뒤에만 매수 신호가 다시 나올 수 있습니다.
- 매수 신호가 나온 뒤에만 매도 신호가 다시 나올 수 있습니다.

즉, 같은 방향 상태가 계속 유지돼도 첫 신호만 1번 찍히고, 반대 방향 신호가 나온 뒤에야 다시 같은 방향 신호가 허용됩니다.

## 옵션 구성

입력 탭에서는 아래만 제어합니다.

- `매수 신호 표시`
- `매도 신호 표시`

스타일 탭에서는 아래를 제어합니다.

- `매수 신호`: 색상, 모양, 위치
- `매도 신호`: 색상, 모양, 위치

크기는 코드에서 `size.small`로 고정했습니다.

## 알림

아래 `alertcondition()`도 포함했습니다.

- `Advanced Ichimoku Buy Signal`
- `Advanced Ichimoku Sell Signal`

## 적용 방법

1. TradingView Pine Editor를 엽니다.
2. [`advanced-ichimoku.pine`](./advanced-ichimoku.pine) 내용을 붙여 넣습니다.
3. 저장 후 차트에 추가합니다.
4. 스타일 탭의 `매수 신호`, `매도 신호`에서 색상/모양/위치를 조정합니다.

## 참고

- 이 스크립트는 Pine Script `//@version=6` 기준입니다.
- 로컬에서 TradingView 컴파일러를 직접 돌릴 수는 없어서 문법은 정적 검토 기준으로 맞췄습니다.

# Advanced Ichimoku

트레이딩뷰용 Pine Script Ichimoku 확장 버전입니다.

대상 스크립트:
- [`advanced-ichimoku.pine`](./advanced-ichimoku.pine) — 인디케이터 (신호만 표시)
- [`advanced-ichimoku-strategy.pine`](./advanced-ichimoku-strategy.pine) — 전략 (백테스트 + 신호)

이 버전은 기본 Ichimoku 계산을 유지하면서 아래를 추가했습니다.

- 이미지 기준 기본 표시 상태를 맞춘 라인/클라우드 구성
- `래깅 스팬 vs 래깅 위치 캔들 종가` + `현재 컨버전 라인 vs 베이스 라인` 조합의 매수/매도 신호
- 같은 방향 신호가 연속으로 찍히지 않게 하는 신호 순서 제한
- (전략) 다음 봉에서 신호가 나올 가능성을 미리 보여주는 `매수 후보 / 매도 후보` 표시
- (전략) 동일 신호 로직으로 Strategy Tester에서 수익률을 확인하는 백테스트

## 기본 기간값

인디케이터와 전략의 기본 기간이 다릅니다. 인디케이터는 표준 Ichimoku 값을, 전략은 백테스트용으로 조정한 값을 씁니다.

| 항목 | 인디케이터 | 전략 |
| --- | --- | --- |
| 컨버전 라인 길이 | 9 | 8 |
| 베이스 라인 길이 | 26 | 22 |
| 리딩 스팬 B 길이 | 52 | 44 |
| 레깅 스팬 길이 (displacement) | 26 | 22 |

## 기본 표시값

기본값은 요청하신 이미지 기준으로 맞췄습니다.

| 항목 | 기본값 |
| --- | --- |
| Conversion Line | 표시, 핑크(`#E91E63`), 2px |
| Base Line | 표시, 그린(`#00FF00`), 2px |
| Lagging Span | 표시, 노랑(`#FFEB3B`), 2px |
| Leading Span A | 숨김 |
| Leading Span B | 숨김 |
| Kumo Cloud Upper Line | 숨김 |
| Kumo Cloud Lower Line | 숨김 |
| Cloud Fill | 표시, 기본 투명도 45% |

전략 전용 마커:

| 항목 | 기본값 |
| --- | --- |
| 롱 진입 | 표시, 하늘색, `삼각형`, `캔들 아래`, `작게` |
| 롱 청산 | 표시, 주황색, `역삼각형`, `캔들 위`, `작게` |
| 숏 진입 | 표시, 분홍색, `역삼각형`, `캔들 위`, `작게` |
| 숏 청산 | 표시, 초록색, `삼각형`, `캔들 아래`, `작게` |
| 매수 후보 | 표시, 하늘색, `원`, `캔들 아래`, `아주 작게` |
| 매도 후보 | 표시, 분홍색, `원`, `캔들 위`, `아주 작게` |

인디케이터는 마커 대신 매수 신호(하늘색 삼각형, 캔들 아래) / 매도 신호(분홍색 역삼각형, 캔들 위) 1쌍만 표시합니다.

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

## 매수 / 매도 후보 (전략 전용)

전략 스크립트에는 `매수 후보 / 매도 후보` 원형 마커가 있습니다. 이는 확정 신호가 아니라 **다음 봉에서 신호가 발생할 가능성**을 현재 봉에서 미리 보여 주는 표시입니다.

- 래깅 비교 기준을 한 칸 앞당긴 `close[displacement - 2]`(없으면 현재 `close`)로 다음 봉 상태를 추정합니다.
- 전환선 조건은 현재 봉과 동일하게 적용합니다.
- 같은 방향 신호 순서 제한을 그대로 따르며, 같은 봉에서 확정 매수/매도 신호가 나오면 후보는 표시하지 않습니다.

확정 신호와 다음 봉 가격 흐름에 따라 후보가 그대로 실현되지 않을 수 있습니다. 진입 확정용이 아니라 참고용 표시입니다.

## 전략 스크립트

[`advanced-ichimoku-strategy.pine`](./advanced-ichimoku-strategy.pine)은 인디케이터와 동일한 `buySignal / sellSignal` 로직을 그대로 사용해서 Strategy Tester에서 수익률을 확인할 수 있게 만든 버전입니다.

진입/청산 방식은 아래와 같습니다.

- 각 `매수 신호`에서는 먼저 숏 포지션을 청산하고, `롱` 모드인 경우 롱 포지션을 엽니다.
- 각 `매도 신호`에서는 먼저 롱 포지션을 청산하고, `숏` 모드인 경우 숏 포지션을 엽니다.
- 차트의 삼각형 마커는 원시 신호가 아니라 `실제 체결 후 포지션 변화` 기준으로만 표시됩니다.
- 그래서 `롱 진입 / 롱 청산 / 숏 진입 / 숏 청산` 마커가 Strategy Tester의 거래 흐름과 직접 대응됩니다.

전략 옵션:

- `포지션 방향`: `롱` 또는 `숏` (한 방향만 선택)
- `숏 하드 안전청산 기준 (% of 마진콜 가격)`: 기본 `95%`

기본 설정은 `100% of equity`, `pyramiding 0`, `process_orders_on_close=true`, `use_bar_magnifier=true`, `margin_long=100`, `margin_short=100`, `initial_capital=10000`입니다. 숏 포지션은 `strategy.margin_liquidation_price`에 도달하기 전에 빠져나오도록, 마진콜 가격의 일정 비율(`숏 하드 안전청산 기준`)에 하드 스탑을 거는 안전청산 로직을 추가했습니다. 수수료와 슬리피지는 코드에서 가정하지 않았습니다. 실제 거래소 기준으로 보려면 TradingView 전략 속성에서 수수료와 슬리피지를 직접 넣어 주세요.

## 옵션 구성

### 인디케이터 입력 탭

- `기본 설정`: 컨버전 / 베이스 / 리딩 스팬 B / 레깅 스팬 길이
- `표시`: 각 라인과 Cloud Fill 표시 여부
- `매수 신호 표시`, `매도 신호 표시`

### 전략 입력 탭

- `기본 설정`: 컨버전 / 베이스 / 리딩 스팬 B / 레깅 스팬 길이
- `전략`: `포지션 방향`, `숏 하드 안전청산 기준 (% of 마진콜 가격)`
- `표시`: 각 라인과 Cloud Fill 표시 여부
- `포지션 표시`: `롱 진입 표시`, `롱 청산 표시`, `숏 진입 표시`, `숏 청산 표시`
- `후보 신호`: `매수 후보 표시`, `매도 후보 표시`

## 알림

### 인디케이터

- `Advanced Ichimoku Buy Signal`
- `Advanced Ichimoku Sell Signal`

### 전략

- `Advanced Ichimoku Strategy Buy Signal`
- `Advanced Ichimoku Strategy Sell Signal`

## 적용 방법

1. TradingView Pine Editor를 엽니다.
2. 시그널만 보고 싶으면 [`advanced-ichimoku.pine`](./advanced-ichimoku.pine)을 사용합니다.
3. 수익률 백테스트를 하려면 [`advanced-ichimoku-strategy.pine`](./advanced-ichimoku-strategy.pine)을 사용합니다.
4. 저장 후 차트에 추가합니다.
5. 전략 수익률은 TradingView의 `Strategy Tester` 탭에서 확인합니다.
6. 거래 수가 이상해 보이면 `List of Trades` 탭에서 실제 체결 목록을 함께 확인합니다.

## 참고

- 두 스크립트 모두 Pine Script `//@version=6` 기준입니다.
- 로컬에서 TradingView 컴파일러를 직접 돌릴 수는 없어서 문법은 정적 검토 기준으로 맞췄습니다.
</content>
</invoke>

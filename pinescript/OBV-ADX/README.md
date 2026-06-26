# OBV-ADX

트레이딩뷰용 Pine Script 보조지표 설명서입니다.

대상 스크립트:
- [`obv-adx-extreme-background.pine`](./obv-adx-extreme-background.pine)

이 지표는 `OBV` 기반 `+DI / -DI / ADX` 구조를 유지하면서, 기존 고정 임계값 배경 대신 `DI Difference`의 상대적 극단값을 이용해 `낙폭과대`와 `초과매수`를 배경색으로 보여주는 버전입니다.

## 현재 소스 기준으로 보이는 것

| 요소 | 현재 표시 방식 |
| --- | --- |
| `+DI / -DI / ADX` 선 | 옵션을 켜면 OBV 기반 방향성과 강도를 선으로 표시합니다. |
| `DI Difference` 히스토그램 | 옵션이 꺼져 있으면 `plus - minus` 차이를 `50` 기준 막대로 보여줍니다. |
| 녹색 배경 | `DI Difference`가 최근 분포 대비 과도하게 눌린 `낙폭과대` 구간일 때 켜집니다. |
| 빨간 배경 | `DI Difference`가 최근 분포 대비 과도하게 치우친 `초과매수` 구간일 때 켜집니다. |
| 극단 표시 | 낙폭과대 / 초과매수는 배경색과 우측 상단 상태판으로 표시합니다(별도 삼각형 마커는 없음). |

참고:
- 기본값은 `DI Length = 20`, `ADX Smoothing = 20`입니다.
- 극단값은 고정 `20 / 18 / 20`이 아니라, `Extreme Lookback` 구간의 `DI Difference z-score`로 측정합니다.

## 내부 로직

### 1. ADX / DI 계산

기본 골격은 원본과 같습니다.

- `plusDM`, `minusDM`은 `OBV` 변화량 기준으로 계산합니다.
- `trur`는 `OBV` 표준편차를 `rma`로 부드럽게 만든 값입니다.
- `plus`, `minus`, `adx`는 그 위에서 방향성과 강도를 계산합니다.

### 2. 낙폭과대 / 초과매수 배경

배경은 `DI Difference = plus - minus`를 최근 구간 기준으로 표준화해서 판단합니다.

- `diDiffBasis = sma(diDiff, Extreme Lookback)`
- `diDiffStdev = stdev(diDiff, Extreme Lookback)`
- `diDiffZScore = (diDiff - diDiffBasis) / diDiffStdev`

기본 조건은 아래와 같습니다.

- `낙폭과대`: `diDiffZScore <= -Oversold Z-Score`
- `초과매수`: `diDiffZScore >= Overbought Z-Score`
- 둘 다 `ADX >= ADX Minimum`을 만족해야 합니다.
- 옵션이 켜져 있으면 방향도 함께 확인해서, 낙폭과대는 `-DI > +DI`, 초과매수는 `+DI > -DI`일 때만 켭니다.

즉 이 지표는 절대 수치보다 `최근 분포 대비 얼마나 과도하게 한쪽으로 벌어졌는가`를 배경으로 읽는 도구에 가깝습니다.

## 우측 상단 상태판

| 행 | 내용 |
| --- | --- |
| ADX | 값 + `충분`(≥ ADX Minimum) / `약함` |
| DI 방향 | `+DI 우위(상승)` / `-DI 우위(하락)` |
| 극단 배경 | `낙폭과대(녹)` / `초과매수(빨)` / `-` |
| 포지션 | `롱 유리` / `숏 유리` / `중립(휩쏘)` |

`포지션` 판정:
- `롱 유리`: ADX 충분 + `+DI 우위`
- `숏 유리`: ADX 충분 + `-DI 우위`
- `중립(휩쏘)`: ADX가 약하면 추세 힘이 없어 휩쏘 위험 → 관망 (1차 필터 역할)

## 자주 만지는 설정

| 설정 | 언제 조정하나 |
| --- | --- |
| `DI Length`, `ADX Smoothing` | ADX / DI 반응 속도를 바꾸고 싶을 때 |
| `Extreme Lookback` | 극단값 분포 기준을 더 짧게 또는 길게 보고 싶을 때 |
| `Oversold Z-Score`, `Overbought Z-Score` | 낙폭과대 / 초과매수 판정을 더 엄격하게 또는 느슨하게 만들 때 |
| `ADX Minimum` | 힘이 약한 구간을 더 많이 걸러내고 싶을 때 |
| `Require DI Direction Match` | 극단값일 뿐 아니라 실제 방향 우위도 같이 확인하고 싶을 때 |
| `ADX Line or Histogram` | 선 모드와 히스토그램 모드를 바꿔 보고 싶을 때 |
| `Background Highlighting`, `Background Transparency` | 배경 가독성을 조절하고 싶을 때 |

## 해석 팁

- 녹색 배경은 `즉시 매수`보다 `낙폭이 과도했는지 확인`하는 구간으로 보는 편이 좋습니다.
- 빨간 배경은 `즉시 매도`보다 `과열과 피로`를 경계하는 구간으로 읽는 편이 좋습니다.
- 배경 하나보다 `DI 방향`, `ADX 강도`, `가격 구조`를 같이 보는 편이 더 안정적입니다.

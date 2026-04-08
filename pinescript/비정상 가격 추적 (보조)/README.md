# 비정상 가격 추적 (보조)

트레이딩뷰용 Pine Script 보조지표 설명서입니다.

대상 스크립트:
- [`abnormal-price-tracker-helper.pine`](./abnormal-price-tracker-helper.pine)

이 지표는 `cRSI + MFI`를 한 패널에 모아 두고, 메인 진입 신호 뒤에서 `과열/과매도 확인`과 `반대 방향 위험 알림`을 보조하는 용도로 씁니다.

## 지금 보이는 것

| 요소 | 현재 표시 방식 |
| --- | --- |
| MFI | 노란 선 |
| 과매수 / 과매도 기준선 | 회색 점선 |
| MFI 극단 구간 | 과매수는 빨강, 과매도는 라임 채움 |
| MFI 극단 마커 | 과매수/과매도 구간에서 동그라미 표시 |
| cRSI 밴드 | 하늘색 밴드 + 파란 배경 채움 |
| cRSI 본선 | 기본값은 숨김 |

즉 차트에서 먼저 보는 것은 `MFI가 극단 구간에 들어갔는지`, 그리고 `cRSI 밴드 안팎에서 같이 눌리거나 과열되는지`입니다.

## 내부 로직

차트에 보이는 것과 별개로, 내부에서는 반전 위험 점수를 계속 계산합니다.

- `cRSI - MFI` 괴리 크기
- 가격 연장 정도
- 거래량 평균 대비 확장 여부
- cRSI 극단 구간 진입 여부
- 괴리 둔화 여부
- cRSI / MFI 방향 전환 여부

이 점수는 최종적으로 아래 알림 조건에 연결됩니다.

- `Bearish Reversal Risk`
- `Bullish Reversal Risk`

즉 이 지표는 `신규 진입 트리거`보다 `지금 추격해도 되는지 다시 거르는 필터`에 더 가깝습니다.

## 차트 해석

| 상황 | 해석 |
| --- | --- |
| MFI가 과매수 구간에 오래 머묾 | 위쪽 추격보다 익절 / 관망 쪽이 유리할 수 있음 |
| MFI가 과매도 구간에 오래 머묾 | 공포 매도보다 반등 후보 확인이 유리할 수 있음 |
| cRSI 밴드 상단에서 MFI 과매수 | 과열 구간 확인용 |
| cRSI 밴드 하단에서 MFI 과매도 | 투매 구간 확인용 |
| 반전 위험 알림 발생 | 메인 지표 신호와 반대로 힘이 꺾이는지 재확인할 구간 |

실전에서는 보통 이렇게 씁니다.

1. [`비정상 가격 추적 (캔들)`](../비정상%20가격%20추적%20(캔들)/README.md)에서 자리 후보를 먼저 봅니다.
2. 이 보조 지표에서 `MFI 극단 구간`과 `cRSI 밴드 위치`를 확인합니다.
3. 내부 위험 알림까지 겹치면 추격 진입보다 속도 조절이나 분할 대응을 우선합니다.

## 자주 만지는 설정

| 설정 | 용도 |
| --- | --- |
| `MFI Length` | MFI 반응 속도 조절 |
| `Gap Threshold` | cRSI와 MFI 괴리 민감도 조절 |
| `Weak Gap Threshold`, `Strong Gap Threshold` | 내부 위험 점수 강도 조절 |
| `Bearish Risk cRSI Zone`, `Bullish Risk cRSI Zone` | cRSI 극단 기준 조절 |
| `Volume Average Length`, `Volume Multiplier` | 거래량 필터 강도 조절 |
| `Trend Length`, `Price Stretch (%)` | 가격 연장 판정 속도 조절 |
| `Use Gap Fade Condition`, `Gap Fade Lookback` | 괴리 둔화 조건 조절 |
| `cRSI Band Color`, `cRSI Band Width` | cRSI 밴드 선 스타일 조절 |
| `cRSI Band Fill Color`, `cRSI Band Fill Transparency` | cRSI 밴드 배경 조절 |
| `MFI Extreme Fill Transparency` | 과매수 / 과매도 채움 강도 조절 |

## 주의사항

- `cRSI` 본선은 기본적으로 숨겨져 있고, 필요할 때만 켜서 봅니다.
- 이 지표는 극단 구간 확인과 위험 필터용이라서, 단독 진입 신호기로 쓰는 것보다 메인 지표와 같이 보는 편이 안전합니다.
- 과매수 / 과매도 채움이 나온다고 바로 반대 포지션을 잡기보다, 가격 구조와 거래량을 함께 보는 쪽이 안정적입니다.

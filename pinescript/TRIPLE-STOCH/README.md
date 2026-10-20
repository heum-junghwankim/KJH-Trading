# 삼중 Stoch (Triple Stochastic Wave, 삼중 스토캐스틱 웨이브)

트레이딩뷰용 Pine Script **보조 지표** 설명서입니다.

대상 스크립트:
- [`triple-stochastic-wave.pine`](./triple-stochastic-wave.pine)

> Pine Script **v6** 기준. 별도 패널(`overlay` 아님)에 그려지는 **모멘텀·타이밍 보조 지표**입니다.

CEO 확정 제공 "Triple-Stochastic-Wave" 소스코드를 기반으로 합니다. **웨이브 배경 조건은 CEO 지시로 스토캐스틱 정배열/역배열(세 스토캐스틱 서열)로 재정의**했고, 이후 CEO 지시로 **차트를 단순화**했습니다(아래).

> **단순화 (CEO 지시):** 다음 요소를 **제거**했습니다.
> - Fast **골든/데드 크로스** 전체 — 원 마커, 트리거 계산(`fast_*_trigger`), `Golden Cross`/`Dead Cross` alert, 관련 입력(`Cross Trigger Basis`·`Cross Mode`·`Full Alignment Rule`)과 완전배열 방향 래치.
> - **우측 상단 상태 테이블** 전체 — 종합·정렬/추세·모멘텀 행 판정, 완성봉 오프셋 로직, `slow_*_trend` 컨텍스트와 `Slow Context Lookback` 입력.
>
> 남은 것: 6개 라인, 웨이브 배경, 수평선 3개, 3중 정렬 alert 2종. `Wave Background Basis` 기본값은 **`D선`** 으로 바뀌었습니다.

> **기본 표시 전환 (CEO 지시):** 기본으로 **%D 3선만** 보이고 %K 3선은 숨김(`display.none`)입니다. 우측 스케일 라벨이 %D에 붙도록 plot title을 맞바꿨습니다 — %D = `Slow`/`Mid`/`Fast`, %K = `Slow %K`/`Mid %K`/`Fast %K`.

> **웨이브 배경 재정의 (CEO 지시, 이전 변경):** 원본 배경 조건 `slow_*_trend and mid_*_reset`(컨텍스트+리셋)을 **정확한 정배열/역배열**로 교체했습니다. 이에 따라 `mid_bull_reset`/`mid_bear_reset` 및 `Mid Pullback Lookback` 입력이 제거되었습니다.

## Pine 버전: v6 채택

원본 CEO 코드는 `//@version=5`였으나, 이 저장소의 지표 관행(v6 우세)에 맞춰 **v6로 포팅**했습니다. 쓰인 API(`ta.*`, `math.*`, `input.*`, `color.new`, `plot`, `hline`, `bgcolor`, `alertcondition`, `display.*`)는 v5·v6 문법이 같습니다.

## 지표 구조 — 3개 스토캐스틱

| 스토캐스틱 | 기본 (Length/K/D) | 역할 | 색 |
| --- | --- | --- | --- |
| **Slow** | 20 / 9 / 9 | **컨텍스트**(큰 추세·국면) | 파랑 `#1565C0` |
| **Mid** | 10 / 6 / 6 | **중간축**(정배열/역배열 서열의 가운데) | 청록 `#00897B` |
| **Fast** | 5 / 3 / 3 | **선행축**(가장 빠르게 반응) | 주황 `#FB8C00` |

각 스토캐스틱은 표준 정의로 계산합니다(`stoch_pair` 헬퍼):
```
raw_k = 100 × (close − 최저저가) / max(최고고가 − 최저저가, mintick)
k     = SMA(raw_k, smooth_k)
d     = SMA(k, smooth_d)
```
- `max(range, syminfo.mintick)`로 0으로 나누기를 방지합니다(횡보·갭 없는 구간 가드).

## 신호 로직

- **`stoch_bull_order` / `stoch_bear_order`** (정배열/역배열 서열 = 웨이브 배경): 세 스토캐스틱 **서열**로 판정. 기준선은 `Wave Background Basis`를 따릅니다.
  - **`D선`(기본)**: 정배열 = `fast_d > mid_d > slow_d`, 역배열 = `fast_d < mid_d < slow_d`. 매끄럽고 늦습니다.
  - **`K선`**: 정배열 = `fast_k > mid_k > slow_k`, 역배열 = 역순. 빠르고 민감합니다(이전 기본값).
  - 엄격 부등호라 "정확히" 순서대로 정렬된 상태만 참이며, 정배열=녹 / 역배열=적 배경(투명 80)으로 표시합니다.
- **`all_bull_aligned` / `all_bear_aligned`** (3중 시그널 정렬): Slow·Mid·Fast **각각** %K > 자기 %D(또는 셋 다 < 자기 %D). alert 조건입니다. *(각 스토캐스틱의 %K vs 자기 %D 비교이며, 스토캐스틱 간 서열인 `stoch_*_order`와는 다른 개념입니다. `Wave Background Basis`와 무관합니다.)*

## 플롯·배경·alert

- **라인 6개**: 각 스토캐스틱의 %K·%D. 색·투명도는 그대로입니다(%D 3개 불투명 0, %K는 Slow·Mid 0 / Fast 45). %K·%D는 같은 색이라 선 굵기로 구분합니다.
- **기본 표시 상태**:
  | plot title | 값 | 기본 | 굵기 |
  | --- | --- | --- | --- |
  | `Slow` | Slow %D | **켜짐**(`display.all`) | 2 |
  | `Mid` | Mid %D | **켜짐**(`display.all`) | 1 |
  | `Fast` | Fast %D | **켜짐**(`display.all`) | 1 |
  | `Slow %K` | Slow %K | 꺼짐(`display.none`) | 3 |
  | `Mid %K` | Mid %K | 꺼짐(`display.none`) | 2 |
  | `Fast %K` | Fast %K | 꺼짐(`display.none`) | 1 |
- **우측 프라이스 스케일 라벨**: 기본 상태에서 **`Slow` / `Mid` / `Fast` 세 개만**(각 %D 값) 나옵니다. 수평선(`hline`)과 배경(`bgcolor`)은 스케일 라벨을 만들지 않습니다.
- **%K를 켜면**: 설정 → 스타일 탭에서 `Slow %K` 등을 체크하면 해당 라인이 패널·상태줄·데이터 창·**스케일 라벨까지 전부** 표시됩니다(`display.none` 플롯은 켜질 때 전체 표시로 복원). 즉 %K를 켜면 라벨이 최대 6개가 됩니다. Pine은 plot당 기본 `display` 하나만 지정할 수 있어 "기본 숨김 + 켜면 라벨 없이 표시"는 코드로 만들 수 없습니다(한계). 라벨을 줄이려면 차트 프라이스 스케일 우클릭 → 라벨 설정에서 지표 라벨을 끄는 방식(지표 전체 단위)만 가능합니다.
- **`Wave Background Basis = K선`** 을 쓸 때는 %K 라인이 숨겨져 있으므로, 배경 근거를 눈으로 확인하려면 스타일 탭에서 %K를 켜세요.
- **웨이브 배경**: 정배열=녹 `#2E7D32`, 역배열=적 `#C62828`(투명 80).
- **수평선**: 과매수(80)·미드라인(50)·과매도(20).
- **alert 2종**: `Triple Stochastic Bull Alignment` / `Triple Stochastic Bear Alignment`(`all_*_aligned`).

## ⚠️ 단독 신호 아님 — 교차 검증 전제

이 지표는 **모멘텀·타이밍**을 봅니다. 방향의 최종 판단은 반드시 **이치모쿠(메인) + 다른 지표의 테이블 + 보조지표 정렬**로 교차 검증하세요(펀드 철학: 단일 신호 불신). 웨이브 배경·3중 정렬은 "지금 타이밍이 정렬됐나"를 보는 **확인용**입니다.

## 리페인팅 / 안전성

- 전 계산이 확정 `ta.*`(`highest`/`lowest`/`sma`)로 이뤄지며 **`request.security`·`lookahead` 없음**. 미래참조가 없습니다.
- 표시(`display`)·title 변경은 계산과 무관하며 신호·alert 로직에 영향이 없습니다.
- 라인·배경·alert는 형성 중인 실시간 봉에서 틱마다 갱신될 수 있습니다(스토캐스틱 지표의 정상 거동). 봉 마감 후 값은 확정됩니다.
- 별도 패널 지표라 가격 차트를 가리지 않습니다.

## 입력 옵션

### Fast Stochastic (5/3/3)
| 설정 | 기본값 |
| --- | --- |
| Fast Length | 5 |
| Smooth K | 3 |
| Smooth D | 3 |

### Mid Stochastic (10/6/6)
| 설정 | 기본값 |
| --- | --- |
| Mid Length | 10 |
| Smooth K | 6 |
| Smooth D | 6 |

### Slow Stochastic (20/9/9)
| 설정 | 기본값 |
| --- | --- |
| Slow Length | 20 |
| Smooth K | 9 |
| Smooth D | 9 |

### Wave Rules
| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| Oversold | 20 | 과매도 수평선 |
| Overbought | 80 | 과매수 수평선 |
| Trend Midline | 50 | 미드라인 수평선 |
| Wave Background Basis | **D선** | 웨이브 배경(정배열/역배열) 서열 기준선. `D선`=세 %D 서열(기본), `K선`=세 %K 서열(이전 기본값) |

> **기본값 변경 주의:** `Wave Background Basis` 기본값이 `K선` → `D선`으로 바뀌어, 기존 차트에 새로 추가하면 배경이 더 늦고 덜 자주 켜집니다. 이전 모습을 원하면 `K선`을 선택하세요. 3중 정렬 alert는 이 옵션과 무관합니다.

## 주의사항

- **임계값·기간은 전략 파라미터**입니다. 바꾸면 신호 성격이 달라지므로, 변경 시 백테스트·과최적화 리스크를 팀(본부장·알고리즘 수학자)과 먼저 검토합니다. 임의 변경 금지.
- 스토캐스틱은 강추세에서 극단 영역에 오래 머뭅니다(밴드워킹). 과매수/과매도를 곧바로 반전으로 읽지 말고, 최종 방향은 이치모쿠 정렬로 확인하세요.
- TradingView 실측(컴파일·차트 거동)에서 최종 확인이 필요합니다.

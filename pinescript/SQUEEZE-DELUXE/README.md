# Squeeze Momentum Deluxe (스퀴즈 모멘텀 디럭스)

트레이딩뷰용 Pine Script **외부 공개 보조 지표**를 펀드 저장소에 편입한 설명서입니다.

대상 스크립트:
- [`squeeze-momentum-deluxe.pine`](./squeeze-momentum-deluxe.pine)

> Pine Script **v5**(원본 버전 유지). 별도 패널(`overlay=false`)에 그려지는 **모멘텀·변동성 압축·방향 흐름 복합 오실레이터**입니다. 차트 표시명은 `[Ʌ] - Squeeze Deluxe`.

## 출처 · 라이선스

- 원작: **"Squeeze Momentum Deluxe"** © **EliCobra** (TradingView 공개 스크립트, CEO 제공 소스)
- 라이선스: **CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike 4.0 International) — https://creativecommons.org/licenses/by-nc-sa/4.0/
  - **저작자표시(BY)**: 원작자 `© EliCobra`와 라이선스 헤더를 지우거나 바꾸지 않습니다(코드 1~2행 유지).
  - **비영리(NC)**: 이 스크립트(및 변경본)를 판매·유료 배포·상업적 서비스의 일부로 제공할 수 없습니다. 펀드 내부 차트 보조 도구로만 사용하며, 외부 유료 제공·재판매는 금지입니다.
  - **동일조건변경허락(SA)**: 변경본을 배포할 경우 같은 CC BY-NC-SA 4.0으로 배포해야 하며, 변경 사실을 표시해야 합니다(아래 "원본 대비 변경 내역"이 그 표시입니다).
- 편입 원칙: **기능 변경 금지.** 계산식·신호·알림·색·입력 기본값·플롯 구성은 원본 그대로이며, 확정 버그 1건 수정과 스타일 탭 기본 표시값 2건만 바꿨습니다. 리팩토링·한글화·v6 마이그레이션은 하지 않았습니다.

## 이 지표는 단독 매매 신호가 아닙니다 (펀드 원칙)

Confluence Buy/Sell 삼각형·Trend Shift 원·Divergence 라벨은 모두 **정렬 확인용 참고 신호**입니다. 이 지표 하나로 진입하지 않습니다. 반드시 **이치모쿠(메인) + 우측 상단 테이블 + 다른 보조지표**가 같은 방향인지 교차 검증하고, 손익비(R:R)와 손절 위치가 확보된 경우에만 자리로 봅니다.

## 구성 요소

| 요소 | 표시 | 계산 · 의미 |
| --- | --- | --- |
| **Mom** (Squeeze Momentum 오실레이터) | 선. Mom > Signal이면 `#ffcfa6`(살구), 아니면 `#419fec`(파랑) | LazyBear식 스퀴즈 모멘텀 변형: `linreg((close − avg(돈치안 중간값, SMA(hl2))) / 돈치안 TR × 100, Length)`. 가격 범위로 정규화돼 대략 ±100 스케일 |
| **Signal** | 선(기본 숨김). Mom과의 사이 채움 `#ffd0a6`/`#4683b4`(투명 50) | `SMA(Mom, Signal)`. 채움은 Signal 선이 숨겨져도 보입니다 |
| **Flux** (Directional Flux) | 영역. 양수 `#169b5d`·음수 `#970529`(투명 70) | `RMA(상승폭)/ATR`·`RMA(하락폭)/ATR`로 만든 방향 비율 `(up−dn)/(up+dn)`을 `RMA(Length/2)` × 100. 양수=매수 흐름 우세 |
| **OverFlux** | 영역(끊김). 양수 `#11cf77`·음수 `#d11645`(투명 70) | Flux가 ±25를 넘은 초과분만(`Flux−25` / `Flux+25`). 방향 흐름 과열 구간 |
| **Squeeze** (3단계 컬럼) | `-1 ~ +1` 세로 막대, 압축 구간에만 표시 | 표준편차(close, Length) < ATR(Length) × k: **High** `#ff1100`(k=0.5, 가장 강한 압축) · **Normal** `#ff5e00`(k=0.75) · **Low** `#ffa600`(k=1.0) |
| **Trend Shift** (원 2개) | 원. 하락 전환 `#4683b4`(Signal 위치) · 상승 전환 `#ffd0a6`(Mom 위치) | Mom이 Signal을 하향/상향 교차한 봉(Squeeze Momentum 토글 켜짐일 때) |
| **Upper/Lower Gauge** (Confluence Gauge) | +70~+75 / −70~−75 띠 채움 | 상단: Flux>0 **그리고** Mom>0 → 진한 `#169b5d`(강), 둘 중 하나 → 투명 40(약), 아니면 중립 회색. 하단은 음수 조건·`#970529`. 게이지 경계선 플롯 4개는 기본 숨김(채움만 보임) |
| **Confluence Sell** | 상단 게이지 위(▼, `#d11645`, 85 위치) | Mom이 Signal 하향 교차 **그리고** Mom > +40 **그리고** Flux > 0 (과열 후 모멘텀 꺾임) |
| **Confluence Buy** | 하단 게이지 아래(▲, `#11cf77`, −90 위치) | Mom이 Signal 상향 교차 **그리고** Mom < −40 **그리고** Flux < 0 (침체 후 모멘텀 반등) |
| **Divergence 라인** | line 오브젝트(약세 `#d11645` / 강세 `#11cf77`) | 확정봉에서 Mom > +Sensitivity 구간의 하향 교차 지점을 피벗으로 저장 → 다음 같은 이벤트에서 **고가는 더 높은데 Signal은 더 낮으면** 약세 다이버전스(두 Signal 지점 연결). 강세는 −Sensitivity 이하·저가 더 낮음·Signal 더 높음 |
| **Divergence 라벨** | `𝐃▾` / `𝐃▴` 라벨(기본 숨김) | 다이버전스 확정 봉의 Signal ±3 위치 |
| **Mid-Line** | 0 점선 | 기준선 |

> Confluence Buy/Sell 삼각형은 해당 게이지가 `Showcase`로 표시될 때만 그려집니다(Sell=상단 게이지, Buy=하단 게이지). **알림은 Showcase 설정과 무관하게 발생**합니다(원본 동작).

## 입력 옵션 (원본 기본값 그대로)

### Directional Flux
| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| (토글) + Length | 켜짐 · `30` (7~50) | Flux/OverFlux 표시 여부 · 계산 길이(내부 평활은 Length/2) |
| Trend Bias | 꺼짐 | 켜면 Flux를 하이킨아시 변형 봉으로 계산(추세 편향 평활). 아래 버그 판정표 6번 참고 |
| Flux 색(상승/하락) | `#169b5d` / `#970529` | Flux 영역 색 |
| OverFlux 색(상승/하락) | `#11cf77` / `#d11645` | OverFlux 영역 색 |

### Squeeze Momentum
| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| (토글) + Length | 켜짐 · `20` (7~50) | Mom/Signal/Trend Shift 표시 및 Trend Shift 알림 여부 · 오실레이터 길이 겸 스퀴즈 판정 길이 |
| Signal | `3` (2~7) | Signal(SMA) 길이. 작을수록 빠르지만 조기 신호 증가 |
| Mom 색(상승/하락) | `#ffcfa6` / `#419fec` | Mom 선 색 |
| 채움·Trend Shift 색(상승/하락) | `#ffd0a6` / `#4683b4` | Mom–Signal 채움 및 Trend Shift 원 색 |

### Divergences
| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| Sensitivity | `25` (20~40) | 다이버전스 피벗으로 인정할 Mom 절대값 임계. 높을수록 탐지 감소 |
| Lines | 켜짐 | 다이버전스 라인 오브젝트 그리기 |
| Labels | 켜짐 | 다이버전스 라벨 플롯 값 생성(스타일 탭 기본 숨김이라 체크해야 보임) |
| 라인 색(강세/약세) | `#11cf77` / `#d11645` | 다이버전스 라인 색 |

### Gauges
| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| Showcase | `Both` (Both/Bull/Bear/None) | 표시할 Confluence Gauge(및 그 게이지에 붙는 Buy/Sell 삼각형) |
| 게이지 색(강세/약세) | `#169b5d` / `#970529` | 상단/하단 게이지 색(약한 정렬은 투명 40) |

## 스타일(모습) 탭 기본 표시 상태

| 켜짐 | 꺼짐 |
| --- | --- |
| Flux, OverFlux, Mom, Squeeze, Trend Shift(2개), Confluence Sell, Confluence Buy, Mid-Line, 라인(그래픽 오브젝트) | Signal, Lower Gauge(2개), Upper Gauge(2개), **Bearish Divergence, Bullish Divergence** |

- Signal·Gauge 4개는 원본부터 `display.none`. **Bearish/Bullish Divergence 라벨만 CEO 지정에 따라 `display = display.none`을 추가**했습니다.
- `display.none`은 표시만 끕니다. 다이버전스 **계산·알림(`alertcondition`/`alert()`)·라인 오브젝트는 그대로** 동작합니다. 라벨을 보려면 스타일 탭에서 체크하세요.
- 게이지 경계선은 숨김이지만 게이지 **채움(fill)** 은 보입니다(원본 설계).

## 알림 17종

`alertcondition`(알림 생성 창에서 개별 선택) 17종:

| # | 알림 제목 | 메시지 | 조건 |
| --- | --- | --- | --- |
| 1 | Confluence Sell | Sell Signal | Mom↓Signal 교차 & Mom > 40 & Flux > 0 |
| 2 | Confluence Buy | Buy  Signal | Mom↑Signal 교차 & Mom < −40 & Flux < 0 |
| 3 | Momentum Midline Crossover | Momentum Bullish | Mom 0 상향 돌파 |
| 4 | Momentum Midline Crossunder | Momentum Bearish | Mom 0 하향 이탈 |
| 5 | Flux Midline Crossover | Flux Bullish | Flux 0 상향 돌파 |
| 6 | Flux Midline Crossunder | Flux Bearish | Flux 0 하향 이탈 |
| 7 | Momentum Swing Crossover | Bullish Swing | Mom↑Signal 교차(Squeeze Momentum 토글 켜짐) |
| 8 | Momentum Swing Crossunder | Bearish Swing | Mom↓Signal 교차(토글 켜짐) |
| 9 | Strong Bullish Confluence | Strong Bull Gauge | 상단 게이지가 중립 → 강(진한색) |
| 10 | Strong Bearish Confluence | Strong Bear Gauge | 하단 게이지가 중립 → 강 (**버그 수정 대상**) |
| 11 | Weak Bullish Confluence | Weak   Bull Gauge | 상단 게이지가 중립 → 약(투명 40) |
| 12 | Weak Bearish Confluence | Weak   Bear Gauge | 하단 게이지가 중립 → 약 |
| 13 | High Squeeze | High   Squeeze | High 압축 진입 |
| 14 | Normal Squeeze | Normal Squeeze | Normal 압축 진입 |
| 15 | Low Squeeze | Low    Squeeze | Low 압축 진입 |
| 16 | Bearish Divergence | Bearish Divergence | 약세 다이버전스 확정 |
| 17 | Bullish Divergence | Bullish Divergence | 강세 다이버전스 확정 |

- 게이지 알림(9~12)은 **중립에서 벗어나는 순간만** 발동합니다. 약→강 승격, 강→약 강등은 알림이 없습니다(원본 설계).
- 추가로 `alert()` 호출(알림 조건 "Any alert() function call")이 **봉 마감 1회**(`alert.freq_once_per_bar_close`) 발동합니다. 단, 한 봉에 여러 조건이 겹치면 **우선순위상 첫 번째 메시지 하나만** 보냅니다: Sell → Buy → Momentum Bull/Bear → Flux Bull/Bear → Bearish/Bullish Swing → Strong Bull/Bear → Weak Bull/Bear → High/Normal/Low Squeeze → Bearish/Bullish Divergence. 개별 조건을 놓치지 않으려면 `alertcondition`을 개별로 거세요.

## 원본 대비 변경 내역

| # | 위치 | 원본 | 변경 | 사유 |
| --- | --- | --- | --- | --- |
| 1 | `alerts.new(...)` 12번째 인자(필드 `w`, Strong Bear Gauge) | `d.c == cng` | `d.c == cgn` | **버그 수정.** 하단 게이지 색은 게이지 색 입력 `cgn`으로 칠해지는데, 판정이 Flux 하락색 입력 `cng`와 비교. 기본값이 둘 다 `#970529`라 우연히 동작했을 뿐, 사용자가 게이지 하락색 또는 Flux 하락색 중 하나만 바꿔도 Strong Bearish Confluence 알림(alertcondition과 alert() 모두)이 영구 미발동. 대칭인 Strong Bull(`u.c == cgp`)·Weak Bear(`color.new(cgn, 40)`)와도 불일치. 기본값 사용 시 동작 변화 없음 |
| 2 | Bearish Divergence `plotshape` | 기본 표시 | `display = display.none` | CEO 지정 스타일 탭 기본값(표시만 변경) |
| 3 | Bullish Divergence `plotshape` | 기본 표시 | `display = display.none` | 동일 |

코드에는 `// [KJH fix]`, `// [KJH]` 주석으로 표시했습니다. 그 외 모든 줄은 원본과 바이트 단위로 동일합니다.

## 버그 검토 결과 (수정하지 않은 의심 항목)

기능 변경 금지 원칙에 따라, 의도된 설계로 볼 여지가 있거나 수정하면 지표 값이 바뀌는 항목은 손대지 않았습니다.

| 항목 | 판정 | 내용 |
| --- | --- | --- |
| Flux `tr`·`(up+dn)` 0 나눗셈 | 의심·미수정 | 가격 변동이 Length 동안 0인 극단 데이터에서만 발생. Pine에서 0 나눗셈은 런타임 에러가 아니라 `na` → 해당 봉 Flux 공백. 일반 심볼 영향 없음 |
| Mom `z.atr()` 0 나눗셈 | 의심·미수정 | 돈치안 범위가 0(Length 동안 완전 평탄)일 때만 `na`. 동일 |
| 사용자 정의 `stdev` 초기 구간 | 의심·미수정 | 초기 Length−1봉은 과거값을 `nz()`로 0 처리해 표준편차가 부풀려짐 → 차트 첫 ~Length봉 동안 Squeeze 미표시(워밍업). 표본 표준편차(n−1)로 `ta.stdev`(모집단)와 약간 다름 — 원작자 설계 |
| `ta.*` 일관 호출 | 정상 | 모든 `ta.*`는 메서드 최상위에서 매 봉 무조건 호출. `atr()`의 삼항 `len == 1 ? tr : ta.rma(...)`는 호출 지점마다 `len`이 고정(simple)이라 분기가 바뀌지 않음(컴파일 경고 가능성만 있음) |
| `ha()`의 `var` 사용 (Trend Bias) | 의심·미수정 | `var` 객체의 `c`를 먼저 바꾼 뒤 `x.src('oc2')[1]`·`x.o`를 참조해, 표준 하이킨아시(HA open = 직전 HA open·close 평균, HA high/low에 당봉 HA open 사용)와 1봉 어긋난 변형으로 계산될 가능성. 기본 꺼짐이고, 고치면 Flux 값이 바뀌는 **전략 변경**이라 미수정. TradingView에서 표준 HA와 값 비교 검증 필요 |
| `any()` 매핑 | 정상 | `a.x`(하향 교차)→`Bearish Swing`, `a.y`(상향 교차)→`Bullish Swing`, 나머지 필드-메시지 정합 |
| 게이지 `ta.change(u.c == colnt)` | 의도 동작·미수정 | 중립 여부 변화는 양방향이지만 `and u.c == 강/약색` 조건으로 실제로는 "중립 → 강/약" 진입만 발동. 승격/강등 무알림은 설계로 판단 |
| `alert()` 단일 메시지 | 의도 동작·미수정 | switch 우선순위로 봉당 1메시지(위 알림 절) |
| Showcase와 알림 | 의도 동작·미수정 | 게이지·Confluence 알림은 Showcase=None이어도 발생(표시만 게이팅) |
| 다이버전스 피벗 상태 공유 | 정상 | 강세/약세가 같은 피벗 변수를 쓰지만, 반대 종류 피벗과는 Signal 부호 조건이 성립할 수 없어 비교 실패 → 새 피벗으로 교체. 오탐 없음 |
| Squeeze 3단계 배열 | 정상 | `unshift` 후 `pop` 순서로 High=k 0.5, Normal=0.75, Low=1.0이 정확히 매핑 |

## 리페인팅 분석

- `request.security`·`lookahead`·음수 offset·미래 참조 **없음**. 모든 값은 현재 봉과 과거 봉으로만 계산됩니다. **봉 마감 후 과거 값은 바뀌지 않습니다.**
- **Divergence(라인·라벨·알림 16/17)**: 판정 블록이 `barstate.isconfirmed`로 게이트돼 확정봉에서만 발생 → 실시간 봉 중 깜빡임 없음, 과거·실시간 결과 동일. 라인은 과거 피벗 지점과 연결되지만 그려지는 시점은 확정 봉입니다(지연 확정).
- **Confluence Buy/Sell·Trend Shift·Squeeze·Gauge·0선 교차**: 실시간(미마감) 봉에서는 진행 중 가격에 따라 **나타났다 사라질 수 있습니다.** 봉 마감 시점 값으로 고정됩니다. `alertcondition` 알림은 **"Once Per Bar Close"** 빈도로 거는 것을 권장합니다.
- `alert()` 호출은 `alert.freq_once_per_bar_close`라 확정 봉 기준으로만 발송됩니다.

## 주의사항

- **매매 신호 단독 사용 금지** — 이치모쿠·테이블·보조지표 교차 검증(위 원칙).
- 입력 기본값(Length 20/30, Signal 3, Sensitivity 25, ±40 Confluence 임계)을 바꾸는 것은 **신호 민감도 변경(전략 변경)** 입니다. 팀(본부장·알고리즘 수학자) 검토 없이 임의 변경하지 않습니다.
- 라이선스상 **비영리 내부 사용만** 허용됩니다. 변경본 배포 시 CC BY-NC-SA 4.0 유지·원작자 표시 의무.
- 로컬 컴파일러가 없어 정적 검토만 했습니다. TradingView에서 컴파일·표시·알림 동작 최종 확인이 필요합니다.

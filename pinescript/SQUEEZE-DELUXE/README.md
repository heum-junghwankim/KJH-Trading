# Squeeze Momentum Deluxe (스퀴즈 모멘텀 디럭스)

트레이딩뷰용 Pine Script **외부 공개 보조 지표**를 펀드 저장소에 편입한 설명서입니다.

대상 스크립트:
- [`squeeze-momentum-deluxe.pine`](./squeeze-momentum-deluxe.pine)

> Pine Script **v5**(원본 버전 유지). 별도 패널(`overlay=false`)에 그려지는 **모멘텀·변동성 압축·방향 흐름 복합 오실레이터**입니다. 차트 표시명은 `[Ʌ] - Squeeze Deluxe`.

## 목차

1. [출처 · 라이선스](#출처--라이선스)
2. [이 지표는 단독 매매 신호가 아닙니다 (펀드 원칙)](#이-지표는-단독-매매-신호가-아닙니다-펀드-원칙)
3. [페인팅 요소별 상세](#페인팅-요소별-상세) — 요약표 + 요소 18개
4. [원작 설명 vs 코드 차이](#원작-설명-vs-코드-차이)
5. [입력 옵션](#입력-옵션-원본-기본값-그대로)
6. [스타일(모습) 탭 기본 표시 상태](#스타일모습-탭-기본-표시-상태)
7. [알림 17종](#알림-17종)
8. [원본 대비 변경 내역](#원본-대비-변경-내역)
9. [버그 검토 결과 (수정하지 않은 의심 항목)](#버그-검토-결과-수정하지-않은-의심-항목)
10. [리페인팅 분석](#리페인팅-분석)
11. [주의사항](#주의사항)

## 출처 · 라이선스

- 원작: **"Squeeze Momentum Deluxe"** © **EliCobra** (TradingView 공개 스크립트, CEO 제공 소스)
- 원작 설명 페이지: https://www.tradingview.com/script/iFZB4wBg-Squeeze-Momentum-Deluxe/ (영문. 이 문서의 "원작자 의도" 문구는 그 요지를 한국어로 옮긴 것입니다)
- 라이선스: **CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike 4.0 International) — https://creativecommons.org/licenses/by-nc-sa/4.0/
  - **저작자표시(BY)**: 원작자 `© EliCobra`와 라이선스 헤더를 지우거나 바꾸지 않습니다(코드 1~2행 유지).
  - **비영리(NC)**: 이 스크립트(및 변경본)를 판매·유료 배포·상업적 서비스의 일부로 제공할 수 없습니다. 펀드 내부 차트 보조 도구로만 사용하며, 외부 유료 제공·재판매는 금지입니다.
  - **동일조건변경허락(SA)**: 변경본을 배포할 경우 같은 CC BY-NC-SA 4.0으로 배포해야 하며, 변경 사실을 표시해야 합니다(아래 "원본 대비 변경 내역"이 그 표시입니다).
- 편입 원칙: **기능 변경 금지.** 계산식·신호·알림·색·입력 기본값·플롯 구성은 원본 그대로이며, 확정 버그 1건 수정과 스타일 탭 기본 표시값 2건만 바꿨습니다. 리팩토링·한글화·v6 마이그레이션은 하지 않았습니다.

## 이 지표는 단독 매매 신호가 아닙니다 (펀드 원칙)

Confluence Buy/Sell 삼각형·Trend Shift 원·Divergence 라벨은 모두 **정렬 확인용 참고 신호**입니다. 이 지표 하나로 진입하지 않습니다. 반드시 **이치모쿠(메인) + 우측 상단 테이블 + 다른 보조지표**가 같은 방향인지 교차 검증하고, 손익비(R:R)와 손절 위치가 확보된 경우에만 자리로 봅니다.

**교차 검증 시 주의 — 내부 신호는 서로 독립이 아닙니다.**

1. 정보원은 사실상 **Mom(+Signal)과 Flux 두 개뿐**입니다. Confluence ▼▲는 Mom 교차에 Mom 수준과 Flux 부호를 더한 조건이고, 게이지 채움도 같은 Mom·Flux 부호로 만듭니다. 그래서 ▼▲와 게이지가 함께 나와도 서로 다른 근거가 겹친 것이 아닙니다.
2. Trend Shift 원, Confluence, Divergence는 모두 **같은 Mom–Signal 교차**에서 나옵니다. Squeeze(stdev/ATR)만 독립적인 변동성 정보원입니다.
3. 따라서 이 지표는 내부 신호가 여러 개 겹쳐도 **"1표"로 취급**하고, 이치모쿠 메인과 테이블, 다른 보조지표와 정렬될 때만 근거로 씁니다.

## 페인팅 요소별 상세

- 기준: **코드 기준.** 원작 설명과 다른 부분은 각 요소에 `[원작 설명과 차이 → n]`으로 표시하고, 내용은 [원작 설명 vs 코드 차이](#원작-설명-vs-코드-차이) 절에 모았습니다.
- 아래 산식의 숫자는 원본 기본값(Squeeze Momentum Length `len=20`, Signal `sig=3`, Directional Flux Length `dfl=30`, Trend Bias `dfh=false`, Sensitivity `trs=25`, Showcase `gds='Both'`) 기준입니다. 입력 전체는 [입력 옵션](#입력-옵션-원본-기본값-그대로) 참고.
- 리페인팅은 3개 유형으로만 분류하고, 상세 설명은 [리페인팅 분석](#리페인팅-분석) 절 한 곳에 둡니다.
  - **없음** — 상수라 변하지 않음
  - **진행 봉** — 실시간(미마감) 봉에서만 값이 바뀌고 봉 마감 후 고정
  - **확정봉** — `barstate.isconfirmed` 게이트로 마감 봉에서만 생성

### 요약표

| # | 페인팅 요소 | 모양/색 | 기반 기술지표 | 한줄 의미 | 기본 표시 | 리페인팅 |
|---|---|---|---|---|---|---|
| 1 | Mid-Line | 점선 hline, 차트 전경색 70% 투명 | 상수 0 | 모든 오실레이터의 0 기준 | 표시 | 없음 |
| 2 | Flux | area, 녹 `#169b5d` / 적 `#970529` (70% 투명) | RMA 기반 상승폭/하락폭 방향성 비율 | 가격 변동성의 방향(추세 심리) | 표시 | 진행 봉 |
| 3 | OverFlux | areabr, 녹 `#11cf77` / 적 `#d11645` (70% 투명) | Flux의 ±25 초과분 | 한 방향으로의 극단 편향(소진 또는 지속) | 표시 | 진행 봉 |
| 4 | Mom | 선, `#ffcfa6` / `#419fec` | 돈치안 중간값·SMA(hl2) 평균 대비 종가 편차 ÷ 범위 → linreg | 정규화된 모멘텀 | 표시 | 진행 봉 |
| 5 | Signal | 선(숨김) | SMA(Mom, 3) | Mom의 신호선, 채움·교차용 | 숨김 | 진행 봉 |
| 6 | Mom–Signal 채움 | fill, `#ffd0a6` / `#4683b4` (50% 투명) | Mom vs Signal 대소 | 리본 방향 | 표시 | 진행 봉 |
| 7 | Squeeze 컬럼 | −1~+1 컬럼, `#ff1100` / `#ff5e00` / `#ffa600` | stdev(close) vs ATR × 0.5/0.75/1.0 | 변동성 수축 3단계 | 표시 | 진행 봉 |
| 8 | Trend Shift (Bearish Swing) | 원, `#4683b4`, 굵기 2 | Mom이 Signal 하향 교차 | 리본 하락 전환 | 표시 | 진행 봉 |
| 9 | Trend Shift (Bullish Swing) | 원, `#ffd0a6`, 굵기 2 | Mom이 Signal 상향 교차 | 리본 상승 전환 | 표시 | 진행 봉 |
| 10 | Upper Gauge 선 | plot 2개 (+70, +75) | 상수 | 상단 게이지 채움 경계 | 숨김 | 없음 |
| 11 | Upper Gauge 채움 | +70~+75 띠, `#169b5d` / 40% 투명 / 회색 | Flux>0, Mom>0 동시 여부 | 강세 합치 강도 | 표시 | 진행 봉 |
| 12 | Lower Gauge 선 | plot 2개 (−70, −75) | 상수 | 하단 게이지 채움 경계 | 숨김 | 없음 |
| 13 | Lower Gauge 채움 | −70~−75 띠, `#970529` / 40% 투명 / 회색 | Flux<0, Mom<0 동시 여부 | 약세 합치 강도 | 표시 | 진행 봉 |
| 14 | Confluence Sell ▼ | 역삼각형 tiny, `#d11645`, y=+85 | Mom 하향 교차 + Mom>+40 + Flux>0 | 과열권 평균회귀 매도 후보 | 표시 | 진행 봉 |
| 15 | Confluence Buy ▲ | 삼각형 tiny, `#11cf77`, y=−85 | Mom 상향 교차 + Mom<−40 + Flux<0 | 침체권 평균회귀 매수 후보 | 표시 | 진행 봉 |
| 16 | Bearish Divergence 라인 | line, `#d11645` | 고가 신고 vs Signal 하락 | 약세 다이버전스 | 표시 | 확정봉 |
| 17 | Bullish Divergence 라인 | line, `#11cf77` | 저가 신저 vs Signal 상승 | 강세 다이버전스 | 표시 | 확정봉 |
| 18 | Divergence 라벨 `𝐃▾` / `𝐃▴` | 라벨, 배경 회색, 글자 `#ff5e00` | 16·17과 같은 이벤트 | 다이버전스 발생 표시 | **숨김 (KJH 변경)** | 확정봉 |

### 1. Mid-Line (0선)

- **무엇을 그리나**: `hline(0)`, 점선(`hline.style_dashed`), 색 `chart.fg_color` 70% 투명.
- **기술지표·산식**: 상수 0. Mom·Flux·OverFlux·게이지가 모두 0을 중심으로 대칭.
- **발동/색 조건**: 항상 표시.
- **해석(원작자 의도)**: 별도 설명 없음. 0선 교차는 알림(Momentum/Flux Midline)의 기준.
- **리페인팅**: 없음.
- **관련 입력·알림**: 입력 없음 / 알림 3·4 `Momentum Midline Crossover/Crossunder`(Mom이 0 교차), 5·6 `Flux Midline Crossover/Crossunder`(Flux가 0 교차). 두 알림 모두 별도 마커는 그리지 않음.

### 2. Flux (영역)

- **무엇을 그리나**: `plot(v.o, style=plot.style_area)`. 0선부터 값까지 채운 영역. y = Flux 값(이론 범위 −100~+100).
- **기술지표·산식** (`method dfo`, Trend Bias 켜면 하이킨아시 변형 봉 기준):
  - `tr = RMA(TR, 30)`(ATR), `up = RMA(max(Δhigh, 0), 30) / tr`, `dn = RMA(max(−Δlow, 0), 30) / tr`
  - `v.o = RMA((up − dn) / (up + dn), 15) × 100` (15 = `dfl/2`)
  - 즉 상승 확장폭과 하락 확장폭의 비율(DX 계열 방향성 비율)을 다시 RMA로 평활한 값. `[원작 설명과 차이 → 1]`
- **발동/색 조건**: `v.o > 0` → `cps` `#169b5d` 70% 투명, 아니면 `cng` `#970529` 70% 투명. `dfb`(Flux 토글)가 꺼지면 숨김(게이지·알림 계산은 계속됨).
- **해석(원작자 의도)**: 배경의 "파도"로 추세 심리(상승/하락 우위)를 보여줌. Trend Bias는 Flux를 하이킨아시 봉으로 계산해 가격 추세 쪽으로 기울게 함(구현 의심 사항은 [의심 항목](#버그-검토-결과-수정하지-않은-의심-항목)의 `ha()` 항목).
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `Directional Flux` 그룹 토글 `dfb=true`, `Length dfl=30`, `Trend Bias dfh=false`, 색 `cps/cng` / 알림 5 `Flux Midline Crossover`(Flux Bullish), 6 `Flux Midline Crossunder`(Flux Bearish).

### 3. OverFlux (영역)

- **무엇을 그리나**: `plot(v.s, style=plot.style_areabr)`. 값이 `na`인 구간은 끊어지는 영역.
- **기술지표·산식**: Flux의 ±25 초과분.
  - `v.s = v.o − 25` (v.o > +25), `v.o + 25` (v.o < −25), 그 외 `na`.
- **발동/색 조건**: |Flux| > 25일 때만 표시. `v.s > 0` → `cpo` `#11cf77` 70% 투명, 아니면 `cno` `#d11645` 70% 투명. `dfb` 꺼지면 숨김.
- **해석(원작자 의도)**: 한 방향으로의 극단적 시장 편향. 소진(exhaustion) 또는 강한 지속(continuation)을 모두 뜻할 수 있음(방향 판단은 따로 필요).
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `dfb`, `dfl`, `dfh`, 색 `cpo/cno`(Flux 그룹 3번째 줄) / 알림 없음. 임계값 25는 하드코딩이라 입력으로 바꿀 수 없음.

### 4. Mom (모멘텀 선)

- **무엇을 그리나**: `plot(o.o, style=plot.style_line)`, 굵기 1. y = Mom 값(가격 범위로 정규화돼 대략 ±100 스케일).
- **기술지표·산식** (`method osc`):
  - `av = SMA(hl2, 20)`, 돈치안 봉 `z`: 고가 = `highest(20)`, 저가 = `lowest(20)`, 종가 = `close`
  - 기준선 = `avg(돈치안 중간값, av)`, 편차 = `close − 기준선`
  - 정규화: 편차 ÷ `z.atr()`(돈치안 봉의 1봉 TR. 돈치안 고저 폭과 같거나 그 이상) × 100
  - `o.o = linreg(정규화 편차, 20, 0)` — LazyBear 계열 Squeeze Momentum 산식을 범위로 정규화한 형태.
- **발동/색 조건**: `o.o > o.s` → `cup` `#ffcfa6`(살구), 아니면 `cdn` `#419fec`(파랑). `smb`(Squeeze Momentum 토글)가 꺼지면 숨김.
- **해석(원작자 의도)**: 가격과 일정 기간 극값 사이의 관계를 수치화. 정규화했기 때문에 시점·종목 간 비교가 가능.
- **리페인팅**: 진행 봉(linreg offset 0).
- **관련 입력·알림**: `Squeeze Momentum` 그룹 `smb=true`, `Length len=20`(스퀴즈 기간과 같은 값), 색 `cup/cdn` / 알림 3·4 `Momentum Midline Crossover/Crossunder`.

### 5. Signal (숨김 선)

- **무엇을 그리나**: `plot(o.s, display=display.none)`. 화면에 보이지 않고 채움(6)의 경계로만 쓰임. 채움은 Signal 선이 숨겨져도 보임.
- **기술지표·산식**: `o.s = SMA(o.o, 3)`.
- **발동/색 조건**: 항상 숨김. `smb` 꺼지면 `na`.
- **해석(원작자 의도)**: Signal 길이는 리본 폭을 조절. 값이 작을수록 반응은 빠르지만 조기 신호(premature positives)가 늘어남(입력 tooltip).
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `Signal sig=3`(2~7) / Mom과의 교차가 Swing(7·8)·Confluence(1·2)·Divergence(16·17) 알림의 트리거.

### 6. Mom–Signal 채움

- **무엇을 그리나**: `fill(Mom plot, Signal plot)` — Mom과 Signal 사이 리본.
- **기술지표·산식**: Mom(4)과 Signal(5)의 대소 비교.
- **발동/색 조건**: `o.o > o.s` → `cpf` `#ffd0a6` 50% 투명, 아니면 `cdf` `#4683b4` 50% 투명.
- **해석(원작자 의도)**: "신호선이 있는 리본"으로 방향을 보여줌.
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: 색 `cpf/cdf` / 알림 없음(교차 알림은 8·9 참고).

### 7. Squeeze 컬럼 (High / Normal / Low)

- **무엇을 그리나**: `plot(s.l ? 1 : na, style=plot.style_columns, histbase=-1)` → 0선을 가로지르는 y −1~+1의 얇은 컬럼. `display.pane`.
- **기술지표·산식** (`method sqz`):
  - `dev` = 종가의 표본 표준편차(20봉, 코드 내 자체 루프 계산), `atr` = `RMA(TR, 20)`
  - 임계값 `atr × 0.25 × i` (i = 2, 3, 4) → **0.5 / 0.75 / 1.0 × ATR**
  - `s.h = dev < 0.5·ATR`, `s.m = dev < 0.75·ATR`, `s.l = dev < 1.0·ATR` (High ⊂ Normal ⊂ Low) `[원작 설명과 차이 → 2]`
- **발동/색 조건**: 컬럼은 `s.l`(가장 느슨한 조건)일 때만 그려짐. 색은 우선순위대로 `[원작 설명과 차이 → 5]`
  - **High Squeeze** — `dev < 0.5·ATR` → `#ff1100`(빨강, 가장 강한 압축)
  - **Normal Squeeze** — `0.5·ATR ≤ dev < 0.75·ATR` → `#ff5e00`(주황)
  - **Low Squeeze** — `0.75·ATR ≤ dev < 1.0·ATR` → `#ffa600`(황주황)
- **해석(원작자 의도)**: ATR 임계값 3개로 스퀴즈(변동성 수축)를 3단계로 구분. 수축이 강할수록(High) 이후 확장 가능성이 큼을 보는 용도.
- **리페인팅**: 진행 봉. 차트 첫 ~20봉은 워밍업으로 미표시([의심 항목](#버그-검토-결과-수정하지-않은-의심-항목)의 `stdev` 항목).
- **관련 입력·알림**: `len=20`(Mom과 공유). 배수 0.25×i와 색은 하드코딩 / 알림 13~15 `High/Normal/Low Squeeze`(각 조건이 false→true로 바뀌는 봉에서 발동).

### 8. Trend Shift 원 — Bearish Swing

- **무엇을 그리나**: `plot(a.x ? o.s : na, style=plot.style_circles)`, 굵기 2, 색 `cdf` `#4683b4`. y = 그 봉의 **Signal** 값. title은 "Trend Shift".
- **기술지표·산식**: `a.x = crossunder(Mom, Signal) and smb`.
- **발동/색 조건**: Mom이 Signal을 하향 교차한 봉. 0선 위치·Flux와 관계없이 모든 교차에서 발동.
- **해석(원작자 의도)**: 원작 설명에 서술 없음 `[원작 설명과 차이 → 5]`. 알림명 "Bearish Swing" 기준으로 리본 하락 전환.
- **리페인팅**: 진행 봉(`barstate.isconfirmed` 조건 없음 → 실시간 봉에서 교차가 생겼다 사라질 수 있음).
- **관련 입력·알림**: `smb`, `len`, `sig` / 알림 8 `Momentum Swing Crossunder`(Bearish Swing).

### 9. Trend Shift 원 — Bullish Swing

- **무엇을 그리나**: `plot(a.y ? o.o : na, style=plot.style_circles)`, 굵기 2, 색 `cpf` `#ffd0a6`. y = 그 봉의 **Mom** 값.
- **기술지표·산식**: `a.y = crossover(Mom, Signal) and smb`.
- **발동/색 조건**: Mom이 Signal을 상향 교차한 봉.
- **해석(원작자 의도)**: 원작 설명에 서술 없음 `[원작 설명과 차이 → 5]`. 알림명 기준으로 리본 상승 전환.
- **리페인팅**: 진행 봉(8과 같음).
- **관련 입력·알림**: `smb`, `len`, `sig` / 알림 7 `Momentum Swing Crossover`(Bullish Swing).

### 10. Upper Gauge 선 (숨김)

- **무엇을 그리나**: `plot(+75)`, `plot(+70)` 2개, 모두 `display.none`. 채움(11)의 경계로만 쓰임.
- **기술지표·산식**: 상수 `gauge.new(+75, +70, ...)`.
- **발동/색 조건**: `u.p = gds == 'Both' or 'Bull'`일 때만 값이 생김(아니면 `na` → 채움과 Confluence Sell ▼도 사라짐).
- **해석(원작자 의도)**: 채움 경계용.
- **리페인팅**: 없음.
- **관련 입력·알림**: `Gauges` 그룹 `Showcase gds='Both'` / 알림 없음.

### 11. Upper Gauge 채움 (강세 합치)

- **무엇을 그리나**: `fill(+70, +75, u.c)` — 상단 띠.
- **기술지표·산식**: Flux(`v.o`)와 Mom(`o.o`)의 부호.
- **발동/색 조건**:
  - **강(Strong)**: `v.o > 0 and o.o > 0` → `cgp` `#169b5d`
  - **약(Weak)**: 둘 중 하나만 > 0 → `cgp` 40% 투명
  - **중립**: 둘 다 ≤ 0 → `colnt` `#787b8635`(회색)
- **해석(원작자 의도)**: 패널 위·아래에 놓여 Mom과 Flux 사이의 합치(confluence)를 측정. 반전 마커(Confluence ▼▲)와 함께 평균회귀 분석을 돕는 용도. 색별 의미는 원작 설명에 없음 `[원작 설명과 차이 → 5]`.
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `gds`, 색 `cgp` / 알림 9 `Strong Bullish Confluence`, 11 `Weak Bullish Confluence`. 알림은 "회색 여부가 바뀐 봉"(`ta.change(u.c == colnt)`)에서만 발동하므로 **중립 → 강/약** 진입만 울리고, 약→강 승격·강→약 강등은 울리지 않음.

### 12. Lower Gauge 선 (숨김)

- **무엇을 그리나**: `plot(−70)`, `plot(−75)` 2개, `display.none`. 두 plot 모두 title이 "Lower Gauge"(코드상 같은 이름).
- **기술지표·산식**: 상수 `gauge.new(−75, −70, ...)`.
- **발동/색 조건**: `d.p = gds == 'Both' or 'Bear'`일 때만(아니면 채움과 Confluence Buy ▲도 사라짐).
- **해석(원작자 의도)**: 채움 경계용.
- **리페인팅**: 없음.
- **관련 입력·알림**: `gds` / 알림 없음.

### 13. Lower Gauge 채움 (약세 합치)

- **무엇을 그리나**: `fill(−70, −75, d.c)` — 하단 띠.
- **기술지표·산식**: Flux·Mom 부호(11과 대칭).
- **발동/색 조건**:
  - **강**: `v.o < 0 and o.o < 0` → `cgn` `#970529`
  - **약**: 둘 중 하나만 < 0 → `cgn` 40% 투명
  - **중립**: 둘 다 ≥ 0 → 회색 `#787b8635`
- **해석(원작자 의도)**: 11과 같음(약세 쪽).
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `gds`, 색 `cgn` / 알림 10 `Strong Bearish Confluence`, 12 `Weak Bearish Confluence`(11과 같은 중립 → 강/약 진입 규칙). **KJH 수정**: Strong Bear 알림의 색 비교 대상을 원작의 Flux 색 `cng`에서 게이지 색 `cgn`으로 바로잡음([변경 내역](#원본-대비-변경-내역) 1번. 기본값에서는 동작 동일).

### 14. Confluence Sell ▼

- **무엇을 그리나**: `plotshape(shape.triangledown)`, tiny, 색 `colno` `#d11645`, 위치 `u.u + 10` = **y +85**(상단 게이지 위).
- **기술지표·산식**: Mom/Signal 교차 + Mom 수준 + Flux 부호.
- **발동/색 조건**: `a.s = crossunder(Mom, Signal) and Mom > +40 and Flux > 0`, 그리고 `u.p`(상단 게이지 표시 중)일 때만 그려짐. `smb` 토글과는 무관. **알림은 Showcase와 무관하게 발생**(표시만 게이팅).
- **해석(원작자 의도)**: 원작의 "반전 도리토스(Reversal doritos)". 과열권에서 모멘텀이 꺾이는 평균회귀 매도 후보.
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `gds`(Bull/Both일 때만 표시). 임계 ±40은 하드코딩 / 알림 1 `Confluence Sell`(Sell Signal).

### 15. Confluence Buy ▲

- **무엇을 그리나**: `plotshape(shape.triangleup)`, tiny, 색 `colpo` `#11cf77`, 위치 `d.l − 15` = **y −85**(하단 게이지 아래).
- **기술지표·산식**: 14와 대칭.
- **발동/색 조건**: `a.b = crossover(Mom, Signal) and Mom < −40 and Flux < 0`, 그리고 `d.p`(하단 게이지 표시 중)일 때만 그려짐. 알림은 Showcase와 무관.
- **해석(원작자 의도)**: 침체권에서 모멘텀이 돌아서는 평균회귀 매수 후보.
- **리페인팅**: 진행 봉.
- **관련 입력·알림**: `gds`(Bear/Both일 때만 표시) / 알림 2 `Confluence Buy`(Buy Signal).

### 16. Divergence 라인 — Bearish

- **무엇을 그리나**: `line.new(이전 피벗 bar, 이전 Signal → 현재 bar, 현재 Signal)`, 색 `cdd` `#d11645`. **Signal 값 위에** 그려짐(가격 차트가 아님).
- **기술지표·산식** (`method draw`):
  - 이벤트: `Mom > +25(trs)` 상태에서 `crossunder(Mom, Signal)`, **확정봉(`barstate.isconfirmed`)일 때만**.
  - 저장 피벗이 없으면 (고가, Signal, bar_index)를 저장.
  - 저장 피벗이 있으면: **현재 고가 > 저장 고가 이고 현재 Signal < 저장 Signal** → 라인을 그리고 초기화. 아니면 현재 값으로 피벗 교체.
  - 약세·강세 판정이 하나의 상태 변수(`var divergence d`)를 공유하므로, 반대 방향 이벤트가 오면 저장 피벗이 교체됨(오탐 없음 — [의심 항목](#버그-검토-결과-수정하지-않은-의심-항목) 참고). `[원작 설명과 차이 → 3]`
- **발동/색 조건**: 위 조건 충족 + `dbl`(Lines) 켜짐.
- **해석(원작자 의도)**: 잠재적 추세 반전 탐지. Sensitivity가 높을수록 탐지가 줄어듦.
- **리페인팅**: 확정봉. 라인은 과거 피벗 지점과 연결되지만 그려지는 시점은 확정 봉(지연 확정).
- **관련 입력·알림**: `Divergences` 그룹 `Sensitivity trs=25`(20~40), `Lines dbl=true`, 색 `cdd` / 알림 16 `Bearish Divergence`.

### 17. Divergence 라인 — Bullish

- **무엇을 그리나**: 16과 같은 방식의 line, 색 `cdu` `#11cf77`.
- **기술지표·산식**: `Mom < −25` 상태에서 `crossover(Mom, Signal)`, 확정봉. **현재 저가 < 저장 저가 이고 현재 Signal > 저장 Signal** → 라인. `[원작 설명과 차이 → 3]`
- **발동/색 조건**: 위 조건 + `dbl`.
- **해석(원작자 의도)**: 16과 대칭(상승 반전 후보).
- **리페인팅**: 확정봉.
- **관련 입력·알림**: `trs`, `dbl`, 색 `cdu` / 알림 17 `Bullish Divergence`.

### 18. Divergence 라벨 `𝐃▾` / `𝐃▴` (기본 숨김)

- **무엇을 그리나**: 약세 `shape.labeldown` `𝐃▾`(y = Signal + 3), 강세 `shape.labelup` `𝐃▴`(y = Signal − 3). 배경 `colnt` 회색, 글자 `colsm` `#ff5e00`.
- **기술지표·산식**: 16·17과 같은 이벤트(`p`). `a.e = p and Mom > +25`, `a.f = p and Mom < −25`.
- **발동/색 조건**: `dbs`(Labels) 켜짐 + 이벤트. 단, **KJH 변경으로 `display=display.none`** — 스타일 탭에서 켜야 보임. 계산과 알림은 그대로.
- **해석(원작자 의도)**: 라인과 같은 다이버전스 발생 위치 표시.
- **리페인팅**: 확정봉.
- **관련 입력·알림**: `Labels dbs=true` / 알림 16 `Bearish Divergence`, 17 `Bullish Divergence`.

## 원작 설명 vs 코드 차이

원작 설명 페이지의 서술과 실제 코드 동작이 다르거나, 원작 설명에 없는 내용을 코드에서 확인한 항목입니다. 이 문서는 **코드 기준**으로 서술합니다. 아래는 문서상 차이일 뿐이며 코드는 수정하지 않았습니다.

| # | 요소 | 원작 설명 | 코드 실제 동작 | 실무 영향 |
| --- | --- | --- | --- | --- |
| 1 | Flux (2) | "가격 변동성의 방향을 측정" | `/tr`(ATR 나눗셈)은 `(up−dn)/(up+dn)` 비율 안에서 상쇄되어 최종값에 영향이 없음. 상승폭/하락폭은 Wilder +DM/−DM처럼 "더 큰 쪽만 채택"하지 않고 각각 따로 누적 | ADX/DMI와 같은 값으로 읽으면 안 됨. 변동성 크기가 아니라 상승·하락 확장의 **상대 비율**만 반영 |
| 2 | Squeeze (7) | "BB가 KC 안에 들어가면 스퀴즈" | BB/KC 밴드를 직접 계산하지 않고 stdev(close, 20)를 ATR × 0.5/0.75/1.0과 바로 비교(개념상 같은 비율 비교) | 일반 BB(2σ)/KC(1.5 ATR) 설정의 스퀴즈와 발동 시점이 다를 수 있음 |
| 3 | Divergence (16·17) | "가격과 오실레이터 간 실시간 다이버전스" | 비교 대상은 Mom이 아니라 **Signal(SMA(Mom, 3))** 이고, 판정은 확정봉에서만 함 | "실시간"은 진행 봉 판정이 아니라 피벗 확인용 지연 봉 없이 **교차 봉에서 바로** 판정한다는 뜻으로 읽어야 함 |
| 4 | 다이버전스 피벗 상태 (16·17) | 서술 없음 | 약세·강세가 하나의 피벗 변수를 공유해 반대 방향 이벤트가 오면 피벗이 교체됨 | 두 같은 방향 이벤트 사이에 반대 방향 이벤트가 끼면 앞선 피벗과는 비교하지 않음(그 구간의 다이버전스는 그려지지 않음) |
| 5 | 색·마커 의미 (7·8·9·11·13) | Squeeze 3색, Trend Shift 원, 게이지 강/약/중립 색의 의미 서술 없음 | 이 문서의 색 조건은 코드에서 확인한 내용 | 해석은 코드 조건 기준으로만 함 |

## 입력 옵션 (원본 기본값 그대로)

### Directional Flux
| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| (토글) + Length | 켜짐 · `30` (7~50) | Flux/OverFlux 표시 여부 · 계산 길이(내부 평활은 Length/2) |
| Trend Bias | 꺼짐 | 켜면 Flux를 하이킨아시 변형 봉으로 계산(추세 편향 평활). 아래 의심 항목 표의 `ha()` 항목 참고 |
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
- 게이지·Confluence 알림은 Showcase=None이어도 발생합니다(Showcase는 표시만 게이팅).
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

이 절이 리페인팅 정보의 단일 기준입니다. 각 페인팅 요소의 "리페인팅" 항목은 아래 유형 이름만 표시합니다.

- **공통**: `request.security`·`lookahead`·음수 offset·미래 참조 **없음**. 모든 값은 현재 봉과 과거 봉으로만 계산됩니다. **봉 마감 후 과거 값은 바뀌지 않습니다.**

| 유형 | 해당 요소 (페인팅 #) | 해당 알림 (#) | 동작 |
| --- | --- | --- | --- |
| **없음** | Mid-Line(1), Upper/Lower Gauge 선(10·12) | — | 상수. 변하지 않음 |
| **진행 봉** | Flux(2), OverFlux(3), Mom(4), Signal(5), Mom–Signal 채움(6), Squeeze(7), Trend Shift(8·9), Gauge 채움(11·13), Confluence Sell/Buy(14·15) | 1~15 | 실시간(미마감) 봉에서는 진행 중 가격에 따라 값이 바뀌고, 교차·마커는 **나타났다 사라질 수 있습니다.** 봉 마감 시점 값으로 고정됩니다 |
| **확정봉** | Divergence 라인(16·17), Divergence 라벨(18) | 16·17 | 판정 블록이 `barstate.isconfirmed`로 게이트돼 확정봉에서만 발생 → 실시간 봉 중 깜빡임 없음, 과거·실시간 결과 동일. 라인은 과거 피벗 지점과 연결되지만 그려지는 시점은 확정 봉입니다(지연 확정) |

- `alertcondition` 알림은 **"Once Per Bar Close"** 빈도로 거는 것을 권장합니다(진행 봉 유형 알림 1~15의 오발송 방지).
- `alert()` 호출은 `alert.freq_once_per_bar_close`라 확정 봉 기준으로만 발송됩니다.

## 주의사항

- **매매 신호 단독 사용 금지** — 이치모쿠·테이블·보조지표 교차 검증(위 펀드 원칙). 이 지표 내부 신호는 여러 개가 겹쳐도 1표입니다.
- 입력 기본값(Length 20/30, Signal 3, Sensitivity 25, ±40 Confluence 임계)을 바꾸는 것은 **신호 민감도 변경(전략 변경)** 입니다. 팀(본부장·알고리즘 수학자) 검토 없이 임의 변경하지 않습니다.
- 라이선스상 **비영리 내부 사용만** 허용됩니다. 변경본 배포 시 CC BY-NC-SA 4.0 유지·원작자 표시 의무.
- 로컬 컴파일러가 없어 정적 검토만 했습니다. TradingView에서 컴파일·표시·알림 동작 최종 확인이 필요합니다.

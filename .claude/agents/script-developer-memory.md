# 스크립트 개발자 — 코드베이스 지식 메모리

> **목적:** 스크립트 개발자(Pine Script Engineer) 페르소나가 **세션 시작 시 참조**하는 로컬 지식 메모리.
> `pinescript/` 하위 전 스크립트의 역할·핵심 파라미터·신호 로직·UI·리페인팅/성능·컨벤션을 사실 중심으로 압축한다.
> **소설 금지 — 코드에서 확인된 사실만.** 수정 전에는 반드시 대상 `.pine` + 해당 폴더 `README.md`를 직접 다시 읽는다(이 메모리는 지도이지 원본이 아님).

## 🗂️ 역할: 저장소 관리자(Repository Owner)

- 나는 코드 작성뿐 아니라 **이 git 저장소의 관리 책임자**다 — 브랜치·커밋·푸시·이력·`.gitignore` 형상관리를 담당한다.
- **커밋 분리 원칙:** 펀드 코드 자산(`pinescript/**`)과 조직 설정(`.claude/**`·`CLAUDE.md`)은 관심사가 다르므로 커밋을 나눈다.
- **📄 코드↔문서 동기화(상시):** `.pine` 코드를 바꾸면 **관련 README(지표 폴더 README + 필요 시 루트 README)를 같은 브랜치·같은 작업에서 함께 갱신**한다. 코드만 바꾸고 문서를 방치하지 않는다. 기능/파라미터/테이블 행 변경은 반드시 문서 반영.
- **원격 규율:** 커밋·푸시·병합은 **본부장 지시(=CEO 승인)에 따라서만** 수행. 임의로 원격/기본 브랜치를 건드리지 않는다.
- 파일 이동/삭제는 `git mv`/`git rm`으로 히스토리 보존. 커밋 메시지 한국어 + 끝에 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

- **마지막 학습 커밋:** `6a3b9d8` (main, origin 동기화됨 — 재구조화 2커밋 ff 병합 + 조직 설정 커밋)
- **원격 이동 안내(2026-07-05 관측):** origin push 시 GitHub가 저장소 이동을 통지(`junghwan-kim-84/KJH-Trading` → `heum-junghwankim/KJH-Trading`). 아직 리다이렉트로 정상 동작하나, remote URL 갱신은 본부장/CEO 승인 후 별도 처리 권고.
- **학습 스크립트:** 활성 7개 `.pine` (SUPER-ICHIMOKU/VWAP/MACD/cRSI/OBV-ADX/CCI/VOLUME-PRESSURE) + 레거시 3개(`pinescript/_legacy/` 하위, 미사용). 각 폴더 `README.md` 유지, **`pinescript/README.md`(하위 가이드)는 삭제됨 → 루트 `README.md`가 안내서.**
- **학습일:** 2026-07-05
- **구조 정리 이력(2cf7b8b):** `ICHIMOKU/`→`SUPER-ICHIMOKU/` 리네이밍, `MA-RIBBON`·`비정상 가격 추적(캔들·보조)`을 `_legacy/`로 이동(미사용), `pinescript/README.md` 제거, `거래량 압력 추적`→`VOLUME-PRESSURE`.
- **⚠️ 메인 해석 축 = SUPER-ICHIMOKU(이치모쿠).** 과거 메모리의 "메인 축 = 비정상 캔들" 서술은 폐기됨(캔들 파일은 레거시). 코드 로직·파라미터·신호 사실은 코드 미변경이라 그대로 유효 — **경로/구조/메인축 서술만 정정됨.**

---

## 저장소 전역 코드 컨벤션 (관측된 규약)

- **버전 혼재 — 파일마다 다름(중요):** 새 파일 기준은 `//@version=6`이지만 실제로는 섞여 있다.
  - **v6:** SUPER-ICHIMOKU, VWAP, CCI, VOLUME-PRESSURE. (레거시: 비정상 가격 추적 캔들·보조)
  - **v5:** MACD, OBV-ADX. (레거시: MA-RIBBON)
  - **v4:** cRSI (`study()`·`iff()` 등 구 API — 수정 시 v4 문법 유지 주의)
  - **→ 파일 수정 시 그 파일의 버전을 먼저 확인.** 일괄 v6 가정 금지.
- **UI 언어:** 한국어 기본(`group`·`title`·테이블·알림). 단 **MACD와 (레거시) MA-RIBBON은 영어 UI**(그 파일 안에서는 영어 일관성 유지). CCI는 입력/그룹은 영어(`GRP`,`SIG`), 테이블 텍스트는 한국어 혼재.
- **색상:** 상수 또는 `input.color`로 상단 모아 선언, 투명도는 `color.new(base, transp)`.
- **입력 구조화:** `group`으로 섹션, 짝 토글+값은 `inline`, 종속 입력은 `active=`, 차트 안 어지럽힐 입력은 `display=display.none`, 설명은 `tooltip`.
- **헬퍼 함수:** 반복 로직은 상단 헬퍼로 추출 (`donchian(len)`, `f_scale`, `f_ltMa`, `ribbonMa`, `maFunc`, `formatPercentGap` 등).
- **상태 테이블:** 대부분 `var table ... = table.new(position.top_right, ...)` + `if barstate.islast`로 갱신(리페인팅·성능 안전 패턴).
- **철학:** 이치모쿠 = 메인(overlay), 나머지 = 교차 검증 보조. 단일 신호 불신·자본 보존.

---

## 스크립트별 지식

### 1. Advanced Ichimoku — **메인 해석 축 (overlay)**
**파일:** `pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine` (1072줄, v6)

- **역할:** 정통 이치모쿠 + 멀티스케일 신호·트리거 테이블·휩쏘 필터·이격도·스윕/청산·VWAP/장기추세 통합. **저장소의 핵심 자산이자 최복잡 파일.**
- **핵심 파라미터(전략값):** 컨버전=8, 베이스=22, 리딩스팬B=44, displacement=22 (구름 오프셋 = disp-1 = 21). 이격도 MA=SMA 20, 고정임계 ±10%, 통계구간 50·σ배수 1.5. 비정상캔들: cRSI Vibration 10·과매수70/과매도30·볼린저배수2.0·몸통비율0.3/바색0.15·ATR배수1.2/강한1.8·RSI이동제한15 (길이는 **베이스라인 22에 연동**). 스윕/청산: 룩백22·ATR22·배수3.0·청산버퍼0.4·스윙풀좌우5·최대간격1.0·트레일200. 장기추세: VWMA 100/200. 리본: 수축ATR배수0.8·확장봉수1. VWAP: Recent Bars 50·hlc3·Log Std·밴드1.0/2.0.
- **신호 로직:** 매수 = (래깅: `close > baseLine[disp-1]` 또는 상향크로스) AND (컨버전: `conv > base` 또는 골든크로스). 매도는 대칭. **멀티스케일** 0.5×/1×/2× (삼각형 크기 tiny/small/normal). **스케일 캐스케이드**: 4→8→16 컨버전 순서로만 표시, 반대신호 시 사다리 리셋(`buyStage`/`sellStage`). **같은 방향 재발화 차단**(`dir05/10/20`). **트리거 스킵**: 상위배수 트리거가 이미 충족되면 즉시 승격. **모멘텀 모드**: 비정상 캔들/반등 감시 진입 시 양방향 모두 한 단계 빠른 기간으로 시프트(정상 이격도 복귀 시 해제). 신호모드 확정(기본)/예측. 거래량가중(VWMA) 신호 별도(기본 OFF).
- **UI:** 우상단 22행 테이블(상승/하락 전환 0.5/1/2× 트리거가·리본추세·비정상매수매도·이격도·되돌림가·구름대·VWAP지지저항·VWAP상태·장기추세·장기지지저항·롱숏 스윕/청산·롱숏 손익비). 차트: 1× 라인/구름만, 신호 삼각형(모멘텀=청산선색), 리본 `+`표식(압축=보라·상승=파랑·하락=빨강), 비정상 바색+배경, 스윕(점선)·청산(직선) polyline+수평선. 손익비 우선순위 V(VWAP기준)→청산가→R(되돌림 -4%폴백).
- **리페인팅/성능:** VWAP 통합은 세션 누적 배열 방식(`var array<float>` + `time("D")`). `barstate.islast`로 테이블·라인·라벨·polyline 갱신. `f_trailLine`은 polyline을 매 last봉 delete/재생성. `request.security` 미사용. `max_bars_back` 미지정(displacement·룩백 길어 주의). 예측 모드·`ta.crossover`류 실시간 봉에서 값 변동 가능(확정봉 아니면 리페인트 성격). 플롯/라인/라벨 개수 상한 관리 필요(신호 삼각형 12종 + 리본 + VWAP 플롯 다수).
- **컨벤션:** 한국어 UI, `group` 다수(기본설정/표시/색상/신호모드/스윕청산/장기추세/이격도/AutoVWAP/비정상캔들/리본추세 등), 헬퍼 다수(`donchian`,`f_scale`,`f_scaleSignals`,`f_trigger`,`f_ltMa`,`ribbonMa`,`f_price`,`f_trailLine` 등). `alertcondition` 5종(매수1×/매도1×/압축/상승분출/하락분출).

### 2. Auto VWAP — 보조(기준 단가)
**파일:** `pinescript/VWAP/auto-vwap.pine` (248줄, v6)

- **역할:** VWAP 평균 체결 단가 + 확장 밴드. 밴드워킹(추세) vs 지지/저항(평균회귀) 구분.
- **핵심 파라미터:** `anchorMode`=Recent Bars(기본), `recentBars`=50, `recentTradingDays`=5, `src`=hlc3, `calcModeInput`=Log Standard Deviation, 밴드배수 1.0·2.0. (그룹 "VWAP Settings"/"Bands Settings")
- **신호 로직:** 밴드워킹 진입 = 수축/저변동 구간(`bwContracting or slopeFlat or ...`)에서 양봉이 상단 밴드2 종가돌파→`vwapWalk=1`, 음봉이 하단 밴드2 돌파→`-1`. 종료 = 밴드2가 반대로 꺾임. 지지/저항 = 밴드워킹 아님 + (수축 or 평탄) + nearLower/nearUpper. 포지션: 상단 밴드워킹/하단 지지=롱 유리(녹), 하단 밴드워킹/상단 저항=숏 유리(빨), 그 외 중립.
- **UI:** 메인 VWAP선(2px, 동적색), 밴드1(점선)·밴드2(파선), 밴드채움(transp 92), 수평선(미래20봉), 우상단 5행 테이블(Auto VWAP/위치/기울기/밴드폭/밴드상태). 밴드% 라벨 옵션(기본 OFF).
- **리페인팅/성능:** `var` 누적값(sessionStartPV 등), `barstate.islast`로 라인·라벨·테이블, `label.delete`로 누수방지, `request.security` 미사용. `array.get` 안전 접근. `cumulativeValue[recentBars]` 역산.
- **컨벤션:** 한국어 UI, `inline="band_1/2"`, `display=display.none` 다수, 헬퍼 `formatPercentGap`·`updateLineEndLabel`, 색상 상수(DEFAULT/UPPER/LOWER_BREAK_LINE_COLOR).

### 3. MACD Divergence Tracker — 보조(모멘텀 재개)
**파일:** `pinescript/MACD/macd-divergence-tracker.pine` (140줄, v5, **영어 UI**)

- **역할:** MACD 교차 + 히스토그램 triple-EMA 평활화 다이버전스(가격MA 기울기 vs 히스토그램 방향), ATR 노이즈 필터.
- **핵심 파라미터:** `fast_length`=9, `slow_length`=20, `signal_length`=7, sma_source/sma_signal=EMA. Divergence: `price_ma_length`=20, `hist_smoothing_length`=3, `divergence_confirm_bars`=2, `divergence_atr_length`=20, `divergence_atr_filter`=0.02. `res`(timeframe, 기본 "").
- **신호 로직:** `cross_UP`=`signal[1]>=macd[1] and signal<macd`(주의: 코드상 signal/macd 비교 방향), `cross_DN` 대칭. 필터: `cross_UP_A`=cross_UP and macd>0. Bullish divergence = price_ma 상승확정 & 이동>ATR×0.02 & hist 상승확정. Bearish는 대칭. 히스토그램 색상 상태머신(above/below × up/down + 다이버전스 강조색).
- **UI:** MACD선(추세색 옵션)·Signal선·히스토그램(columns)·0선, 교차 배경(옵션), 바색(옵션), 교차 원(기본 ON). 상태 테이블 없음.
- **리페인팅/성능:** **`request.security` 사용(`res` 타임프레임)** — 상위 TF 지정 시 미확정봉 리페인팅 가능성. 히스토그램 상태 `var`는 `hist==hist[1]`일 때 이전상태 유지(미묘한 리페인팅 소지). triple-EMA ~3봉 지연. 헬퍼 `is_rising_confirmed`/`is_falling_confirmed`.
- **컨벤션:** v5, 영어 UI, `group`("Show Plots?"/"Color Settings"/"Histogram Colors"/"Divergence"/"Alerts") + `inline` 다수, `alert()` 호출. 색상 상수 다수.

### 4. cRSI (Cyclic Smoothed RSI) — 보조(과열/과매도·다이버전스)
**파일:** `pinescript/cRSI/rsi-cyclic-smoothed.pine` (193줄, **v4 — 구 API 주의**)

- **역할:** 지배 사이클 기반 평활 RSI + **동적 밴드**(백분위 상/하위 10%). 고정 30/70 대신 현재 장세 기준 과매수/과매도. 밴드폭 = 변동성/사이클 진폭 대리.
- **핵심 파라미터:** `domcycle`=20(→cyclelen 10, cyclicmemory 40), `vibration`=10(코드상수), `leveling`=10.0(코드상수). Band Width Bg: `narrowBandThreshold`=20, `wideBandThreshold`=35, `bandBgOpacity`=35. 다이버전스 상수 `divLbL/R`=5, `divRangeMin`=5, `divRangeMax`=60.
- **신호 로직(우선순위):** ①수축돌파(narrowRecently 3봉 + 밴드 첫돌파)→`crsiBreak ±1` 지속. ②확장 다이버전스(wideBw + pivot + 가격LL/HH & osc 반대) → `crsiDiv ±1`, 돌파 후 복귀 시 해제. ③과매수/과매도 되돌림(atHigh/atLowCrsi). ④중립.
- **UI:** cRSI선(자홍#FF00FF), HighBand/LowBand(아쿠아), 30/70 점선, 밴드폭 배경(narrow=주황#D35400·wide=보라), 다이버전스 삼각형(offset=-divLbR, wideBw때만), 우상단 3행 테이블(cRSI/값+밴드폭상태/밴드위치).
- **리페인팅/성능:** `varip int crsiBreak`, `var int crsiDiv`. **동적밴드 100단계×40 루프 = O(4000)/봉** (선형탐색, 반응 약간 늦음). `bar_index < cyclicmemory` 초기구간 배경 제외. `valuewhen`/`barssince` lookahead 없음. **v4 문법(`study`,`iff`)** 유지 주의.
- **컨벤션:** v4, 한국어 UI, `group`="Band Width Background"만, 헬퍼 없음. 출처 명시: Lars von Thienen (2017), CC BY 4.0.

### 5. OBV-ADX Extreme Background — 보조(OBV 극단값 배경)
**파일:** `pinescript/OBV-ADX/obv-adx-extreme-background.pine` (93줄, v5)

- **역할:** OBV를 +DI/−DI/ADX 구조로 변환, DI Difference의 **Z-Score**로 낙폭과대/초과매수 극단 배경 표시(절대값 아닌 분포 대비).
- **핵심 파라미터:** `len`(DI)=20, `lensig`(ADX)=20(max50). Extreme: `extremeLookback`=55, `oversoldZThreshold`=1.2, `overboughtZThreshold`=1.2, `extremeAdxMin`=18.0, `requireDirectionalDi`=true, `obvEnergyLen`=14. Display: 배경투명도 72.
- **신호 로직:** 낙폭과대 = `diDiffZScore <= -1.2` and `adx >= 18` and (DI방향 −DI>+DI). 초과매수 대칭. 테이블 포지션: ADX<min=중립(휩쏘), ADX≥min + DI우위 + 에너지증가=롱/숏 유리(강화), 에너지감소=(약화).
- **UI:** 라인모드(+DI파랑/−DI주황/ADX빨강 + 크로스 원) 또는 히스토그램(diDiff+50). 배경: 낙폭과대=teal#00796b·초과매수=deeppink#880e4f(투명도72). 우상단 4행 테이블(OBV ADX/ADX/DI방향/추세과열).
- **리페인팅/성능:** `var table`, `barstate.islast`. `request.security` 미사용. lookback 55(Z-Score σ). 라인/히스토그램 토글로 렌더 절감.
- **컨벤션:** v5, 한국어 테이블, `group`("ADX / DI"/"Display"/"Extreme Background"), 헬퍼 없음. 약화 톤 상수 #6E8F72/#A57A7A.

### 6. CCI Extreme Cross Signals — 보조(극단 뒤 재진입 크로스)
**파일:** `pinescript/CCI/cci-extreme-cross-signals.pine` (110줄, v6)

- **역할:** CCI가 극단(과매도/과매수) 먼저 진입 후 신호선(CCI-MA) 재돌파할 때만 점 신호. 단순 크로스보다 강한 재진입에 초점.
- **핵심 파라미터:** `length`=20, `src`=hlc3, `maTypeInput`=SMA, `maLengthInput`=14, `bbMultInput`=2.0. Signals: `signalOffsetBarsInput`=0(max1), `bullExtremeInput`=−175.0, `bearExtremeInput`=175.0.
- **신호 로직:** `bullArmed` = 극단진입(`crossunder(cci,-175)`) 또는 유지, 골든크로스 시 해제. `goldenCrossFiltered` = `crossover(cci,MA)` and 직전 bullArmed. `deadCrossFiltered` 대칭. `cciPos` ±1 진입, 신호선 반대이탈 시 0. 테이블: 롱/숏 유리(추세 확인/둔화), 롱/숏 대기(과매도/과매수), 중립.
- **UI:** CCI선(파랑#2962FF), 상/중/하 hline + 배경fill, CCI-MA(노랑#FDD835), 볼린저(옵션), 극단 배경(과매도#0BDF72·과매수#FF3347 투명88), 골든/데드 크로스 원(offset 옵션), 우상단 3행 테이블(CCI Extreme/CCI값/극단상태).
- **리페인팅/성능:** `var bool bullArmed/bearArmed`, `var int cciPos`, `var table`. `barstate.islast`. `active=` 종속입력, `display.none`로 Smoothing 그룹 숨김. `request.security` 미사용.
- **컨벤션:** v6, 그룹은 영어(`GRP`="Smoothing"/`SIG`="Signals"), 테이블 텍스트 한국어. `tooltip`(BB), 헬퍼 `maFunc(source,length,maType)`.

### 7. Moving Average Ribbon — **레거시(미사용)**
**파일:** `pinescript/_legacy/MA-RIBBON/moving-average-ribbon.pine` (47줄, v5, **영어 plot 제목**)

- **⚠️ 레거시:** 이평선 리본 로직은 SUPER-ICHIMOKU에 통합됨. 독립 지표로는 미사용(`_legacy/`).
- **역할:** MA 20~50(7개) 리본 + 100/200 장기선. 정렬 구조로 추세/횡보 시각 판단. **순수 오버레이 — 신호·테이블 없음.**
- **핵심 파라미터:** `src`=close, `maType`=EMA, `show100`=true, `show200`=true. (그룹 없음)
- **신호 로직:** 명시적 신호 없음(해석용). MA100>MA200 → 초록 배경(#4CAF5033), 이하 → 빨강(#FF525233).
- **UI:** 리본 20~50 노랑→주황 그라데이션(투명50 내장), MA100=빨강·MA200=진빨강, 100/200 사이 fill(정배열 초록/역배열 빨강).
- **리페인팅/성능:** `request.security` 미사용, 최대 lookback 200. overlay=true. 헬퍼 `ma(length)`(9회 계산). 플롯 최대 9라인.
- **컨벤션:** v5, 입력 라벨만 한국어, plot 제목 영어. 그룹/inline/tooltip/active 미사용.

### 8. Volume Pressure Tracker — 보조(현재 봉 압력)
**파일:** `pinescript/VOLUME-PRESSURE/volume-pressure-tracker.pine` (74줄, v6)

- **역할:** 거래량을 종가 위치로 매수/매도 압력 선형 추정 + 비정상 거래량 + 평균선으로 추진력 판단.
- **핵심 파라미터:** Abnormal Volume: `length`=20, `multiplier`=1.0(→ 평균 대비 200% 기준). Average Lines: `avgLineLength`=20, `showAverageLines`=true. 색상 그룹(정상/비정상 매수매도).
- **신호 로직:** `buyVolume = volume*(close-low)/(high-low)`, sellVolume 대칭(high==low시 0). `abnormal = volume > sma(vol,20)*(1+1.0)`. 포지션: 평균선 상회+매수우세=롱 유리(녹), 상회+매도우세=숏 유리(빨), 하회=중립(회). 압력방향 셀(비정상=진함/일반=연함).
- **UI:** columns 플롯(매도색 배경 + 매수색 전면), 평균선(SMA 20 주황), 우상단 3행 테이블(거래량 압력/압력 방향/평균선). bgcolor·barcolor 미사용.
- **리페인팅/성능:** `ta.sma`, `var table`, `barstate.islast`. 현재봉 데이터만(lookahead 없음). `request.security` 미사용.
- **컨벤션:** v6, 한국어 UI, 3개 그룹(Volume Colors/Abnormal Volume/Average Lines), 헬퍼 없음, tooltip/active 미사용.

### 9. Abnormal Price Tracker (캔들) — **레거시(미사용)**
**파일:** `pinescript/_legacy/비정상 가격 추적 (캔들)/abnormal-price-tracker-candles.pine` (539줄, v6)

- **⚠️ 레거시:** `_legacy/` 이동됨. **더 이상 메인 축 아님** — 메인 해석 축은 SUPER-ICHIMOKU다. 아래 로직 지식은 참고용(코드는 미변경).
- **역할:** **3단계 진입 흐름** — 0단계 비정상 과매수/과매도 캔들(cRSI+볼린저 이탈) → 1단계 RSI 다이버전스 → 2단계 ATR 배경 진입/강화. Volume Pressure + Helper(MFI) 신호 통합.
- **핵심 파라미터(다수, 62개):** cRSI: `domCycle`=20·`vibration`=10·`leveling`=10.0·`absoluteOB`=70·`absoluteOS`=30. 비정상캔들: `bbLength`=20·`bbMultiplier`=2.0·`bbBodyBreakRatio`=0.3·`bbVisualBreakRatio`=0.15. 다이버전스: `rsiDivLength`=14·`lbR`=1·`lbL`=5·`rangeUpper`=36·`rangeLower`=5. 배경: `setupLookbackBars`=20·`candleSetupLookbackBars`=12·`atrLength`=20·`atrMultiplier`=0.8·`candleAtrMultiplier`=1.2·`strongBgAtrMultiplier`=1.4·`candleStrongBgAtrMultiplier`=1.8·`rsiMoveLimit`=15. VP통합·Helper통합 파라미터 다수(그룹 "거래량 압력 종합 신호"/"보조 종합 신호").
- **신호 로직:** 0단계 = `crsi>=70 & 몸통 상단밴드 30%초과`(약세) / `crsi<=30 & 하단밴드 30%초과`(강세), `barstate.isconfirmed`. 시각색은 15% 초과시만. 1단계 = pivot 기반 RSI 다이버전스(confirmed=확정, realtime=프리뷰 원마커 투명70). 2단계 = 신호 후 룩백 내 가격이동≥ATR×배수 & RSI이동≤제한 & cRSI필터 통과 → 배경 ON, 강한배경 = 둘 다 or 강한 ATR. Helper 약세/강세 위험점수(최대7) ≥2 & 반대 0 & MFI 필터.
- **UI:** 비정상 바색(과매수red/과매도aqua), 다이버전스 프리뷰 원(위/아래), 배경(강세 green/강한 blue·약세 orange/강한 red, 투명82). **테이블 없음.** `alertcondition` 12종(0/1/2단계 롱숏·강화).
- **리페인팅/성능:** `var float crsi`, `var` 트리거봉 인덱스 다수. `barstate.isconfirmed`(확정) + `barstate.isrealtime & not isconfirmed`(프리뷰). `useFastCRSIBands`=true → `ta.percentile_nearest_rank`(빠름) / false → 루프. pivot/valuewhen/barssince lookahead 없음. **`max_labels_count=500, max_boxes_count=500`**. 병목: Helper 점수·VP VAP 누적.
- **컨벤션:** v6, overlay=true, 한국어 UI, 8개 그룹, 헬퍼 `donchian`·`alphaFromAPT`·`withinLookback`·`_inRange`.

### 10. Abnormal Price Tracker (보조/Helper) — **레거시(미사용)**
**파일:** `pinescript/_legacy/비정상 가격 추적 (보조)/abnormal-price-tracker-helper.pine` (184줄, v6, overlay=false 패널)

- **⚠️ 레거시:** `_legacy/` 이동됨(캔들 파일과 함께 미사용). 아래는 참고용 지식.
- **역할:** RSI/MFI 이격(Gap) 기반 반전 위험 점수(추격 진입 필터). RSI 동적 밴드 narrow/wide로 변동성 압축/확장. cRSI 없이 표준 RSI만 사용(캔들 파일이 참조).
- **핵심 파라미터:** `rsiLength`=14·`mfiLength`=14. RSI밴드: `narrowBandWidthThreshold`=20·`wideBandWidthThreshold`=40. 반전위험: `gapThreshold`=14·`weakGapThreshold`=10·`strongGapThreshold`=18·`bullZone`=55·`bearZone`=45·`volumeAvgLength`=20·`volumeMultiplier`=1.1·`trendLength`=20·`priceStretchThreshold`=2.0·`useGapFade`=true·`gapFadeLookback`=2·`minRiskStrength`=2. 밴드 백분위 고정 10/90.
- **신호 로직:** `gap=abs(rsi-mfi)`. bearishGapBg = rsi>mfi & gap≥14. 약세 위험점수(최대7): gapBg+1, gapScore(0~2), priceExtendedUp+1, volumeOkay+1, zonePass+1, gapFade/turningDown+1, rsi/mfi하락+1. 강도 7→3·5→2·4→1. 최종: `barstate.isconfirmed & bearishGapBg & 양봉 & 강도≥2 & 반대0 & mfi>20`. 강세 대칭.
- **UI:** RSI선(핑크 2px)·MFI선(청록 2px)·동적밴드(db/ub 10/90분위)·밴드채움(narrow주황/wide보라 투명88)·MFI 과매수/과매도 fill·80/20 hline. 우상단 1×2 테이블("RSI 밴드"+밴드폭 숫자 narrow주황/wide보라). `alertcondition` 2종(Bearish/Bullish Reversal Risk).
- **리페인팅/성능:** `barstate.islast`(테이블)·`barstate.isconfirmed`(신호). `var table`. `percentile_nearest_rank`(빠름). 표준 지표만·복잡 루프 없음 — 경량. `request.security` 미사용.
- **컨벤션:** v6, overlay=false, 한국어 UI, 4개 그룹(기본/표시/RSI밴드/반전위험), 헬퍼 `formatPanelNumber`. 내부 상수(defaultLineWidth 등).

---

## 교차검증 아키텍처 요약

**루트 `README.md` 기준 현재 해석 흐름 (메인 축 = SUPER-ICHIMOKU / 이치모쿠):**
1. **SUPER-ICHIMOKU** = 메인 해석 축("자리"·국면·신호·구름/스윕/청산). 그 자체로 VWAP·장기추세·이격도·비정상 캔들·리본을 **한 인디케이터 안에 통합**한 종합 오버레이(테이블 22행).
2. **Auto VWAP** = 기준 단가(위/아래·밴드워킹 vs 지지저항)
3. **VOLUME-PRESSURE** = 현재 봉 실제 압력(같은 방향인가)
4. **CCI Extreme** = 극단 뒤 재진입 크로스
5. **MACD 다이버전스** = 모멘텀 재개
6. **OBV-ADX** = OBV 기준 낙폭과대/과매수 배경

즉 SUPER-ICHIMOKU 단일 차트만으로도 이치모쿠 + VWAP + 장기추세 + 비정상 + 리본 + 스윕/청산/손익비를 통합해 볼 수 있고, 나머지 보조지표(VWAP/VOLUME-PRESSURE/CCI/MACD/OBV-ADX)로 방향을 교차 확인한다.

**레거시(`_legacy/`, 미사용):** MA-RIBBON(→이치모쿠에 통합), 비정상 가격 추적(캔들·보조). 과거엔 "비정상 캔들 = 메인 축"이었으나 폐기됨. 새 작업의 참조 대상 아님.

**정렬 확인 원칙:** 한 방향으로 정렬(이치모쿠 삼각형 겹침 + 테이블 셀 색 일치 + 보조지표 같은 방향)될수록 신뢰↑. 하나라도 비거나 충돌하면 관망. "나쁜 진입을 피하는 것"이 우선.

---

## ⚠️ 경고 — 전략값 임의 변경 금지

아래는 **전략에 해당하는 값**이며 **임의로 바꾸면 전략 변경**이다. 백테스트·과최적화 리스크가 있으므로 변경 전 **본부장(및 알고리즘 수학자) 검토·승인 필수**:

- **기간(period):** 컨버전 8·베이스 22·리딩B 44·displacement 22, VWMA 100/200, RSI/MFI/CCI/DI 길이, cRSI domCycle 20, VWAP recentBars 50, 각종 룩백/setupLookback.
- **임계값(threshold):** 이격도 ±10%·σ1.5, cRSI OB70/OS30·narrow20/wide35, CCI 극단 ±175, OBV Z-Score ±1.2·ADX min 18, Gap 14/10/18·zone 55/45, ATR 배수(0.8/1.2/1.4/1.8/3.0 등), 볼린저 배수 2.0·몸통비율 0.3/0.15, 손익비 기준 1.0/1.5·되돌림 -4%.
- **신호 순서·게이트 로직:** 스케일 캐스케이드(4→8→16), 사다리 리셋, 모멘텀 모드 진입/해제 조건, 다이버전스 pivot 범위(5~60 / 5~36).

버그 수정·UI 개선·리팩토링은 이 값들을 **건드리지 않는 선에서만** 자유. 값 변경이 필요하면 먼저 에스컬레이션한다.

**수정 시 필수 체크:** 대상 파일 버전(v4/v5/v6) 확인 → `na`·타입(series/simple/const) → `max_bars_back`·플롯/라인/라벨/박스 상한 → 리페인팅(`request.security`·실시간봉·`var` 상태) → 로컬 컴파일러 없으므로 TradingView 최종 확인 필요 명시.

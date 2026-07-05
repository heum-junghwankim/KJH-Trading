#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
신호-상태 교차표 (프로그램/자동조회용) 생성기 — 이치모쿠 단독 10축 완전 열거
================================================================================
근거 코드: pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine (읽기만, 무수정)

이 스크립트는 이 저장소의 메인 지표(Advanced Ichimoku) **하나**가 출력하는 10개
상태축을 각 3상태로 정규화하고, 그 완전 열거(3^10 = 59,049행)를 결정론적으로
생성해 대용량 프로그램용 Markdown 표로 쓴다. 보조지표(cRSI/CCI/OBV-ADX/거래량)는
이번 표에서 제외한다(이치모쿠 단독).

■ 10축 · 3상태 정규화 (코드 근거)
  1. 추세(멀티스케일 통합)  = dir05/dir10/dir20 부호합 → 상승/하락/중립
  2. 리본 추세             = ribbonState(상승/하락/횡보·대기) → 상승/하락/횡보
  3. 이격도               = disparityState → 중립/되돌림주의/되돌림확실
  4. 구름대               = cloudPosText → 위/안/아래
  5. VWAP 기울기          = vwSlopeText(상승/하락/평탄(중심)) → 상승/하락/평탄
  6. VWAP 밴드폭          = vwBwStateText → 확장/수축/유지
  7. VWAP 밴드상태        = vwBandStateShort(밴드워킹/하단지지/상단저항/중앙) → 밴드워킹/지지/저항
  8. VWAP 지지/저항        = vwSrText(지지/저항/없음) → 지지/저항/없음
  9. 장기 추세            = ltStateBase+크로스 8종 → 상승/하락/중립
 10. 장기 지지/저항        = ltSrText 100선×200선 9종 → 지지우세/저항우세/혼조

■ 방향 판정 (앞 리뷰 규칙 그대로 — 방향 투표축 부호합 + 보정축 신뢰도 가감)
  방향 투표축(6): 추세 / 구름대 / 장기추세 / 장기지지저항 / VWAP지지저항 / 리본
    각 롱계열=+1, 숏계열=-1, 중립계열=0. 순합 vsum(-6..+6).
  판정: vsum >= +3 AND 반대표(음수) 0개 → "롱 정렬"
        vsum <= -3 AND 반대표(양수) 0개 → "숏 정렬"
        그 외 → "중립·혼조"
  신뢰도(보정축 4): 이격도 / VWAP밴드폭 / VWAP기울기 / VWAP밴드상태.
    기저 = |vsum| / 6 (0~1). 보정축으로 가감(±), 0~1 클램프.
    - 이격도:   중립 ×1.00 / 되돌림주의 ×0.85 / 되돌림확실 ×0.70 (되돌림=역풍 페널티)
    - VWAP기울기: 정렬 방향과 일치(+0.05) / 반대(-0.10) / 평탄(0)
    - VWAP밴드폭: 확장(+0.05) / 수축(-0.05) / 유지(0)   (추세 신뢰: 확장=지속, 수축=소멸)
    - VWAP밴드상태: 밴드워킹(+0.05) / 지지·저항(0)
    중립·혼조 행은 신뢰도 = 기저×이격도페널티만 (방향성 보정 무의미).

산출물: pinescript/신호-교차표-프로그램용.md
결정론적: 재실행 시 동일 결과. 코드(.pine)는 무수정.
"""

from itertools import product
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# 10축 정의 (각 3상태). 순서 = 표 열 순서. product는 첫 축이 가장 느리게 변한다.
# ---------------------------------------------------------------------------
TREND      = ["상승", "하락", "중립"]              # 1 추세(멀티스케일 통합)
RIBBON     = ["상승", "하락", "횡보"]              # 2 리본 추세
GAP        = ["중립", "되돌림주의", "되돌림확실"]    # 3 이격도
CLOUD      = ["위", "안", "아래"]                  # 4 구름대
VW_SLOPE   = ["상승", "하락", "평탄"]              # 5 VWAP 기울기
VW_BW      = ["확장", "수축", "유지"]              # 6 VWAP 밴드폭
VW_BAND    = ["밴드워킹", "지지", "저항"]           # 7 VWAP 밴드상태
VW_SR      = ["지지", "저항", "없음"]              # 8 VWAP 지지/저항
LT_TREND   = ["상승", "하락", "중립"]              # 9 장기 추세
LT_SR      = ["지지우세", "저항우세", "혼조"]        # 10 장기 지지/저항

AXES = [TREND, RIBBON, GAP, CLOUD, VW_SLOPE, VW_BW, VW_BAND, VW_SR, LT_TREND, LT_SR]
COLS = ["추세", "리본추세", "이격도", "구름대", "VWAP기울기", "VWAP밴드폭",
        "VWAP밴드상태", "VWAP지지저항", "장기추세", "장기지지저항"]

# 방향 판정 임계
VOTE_THRESHOLD = 3     # 순합 절댓값 이 이상 + 반대표 0개 → 정렬
GAP_PENALTY = {"중립": 1.00, "되돌림주의": 0.85, "되돌림확실": 0.70}


def trend_vote(v):   return 1 if v == "상승" else (-1 if v == "하락" else 0)
def ribbon_vote(v):  return 1 if v == "상승" else (-1 if v == "하락" else 0)      # 횡보=0
def cloud_vote(v):   return 1 if v == "위" else (-1 if v == "아래" else 0)        # 안=0
def lt_trend_vote(v):return 1 if v == "상승" else (-1 if v == "하락" else 0)
def lt_sr_vote(v):   return 1 if v == "지지우세" else (-1 if v == "저항우세" else 0)  # 혼조=0
def vw_sr_vote(v):   return 1 if v == "지지" else (-1 if v == "저항" else 0)        # 없음=0


def score(trend, ribbon, gap, cloud, vw_slope, vw_bw, vw_band, vw_sr, lt_trend, lt_sr):
    votes = [
        trend_vote(trend),
        cloud_vote(cloud),
        lt_trend_vote(lt_trend),
        lt_sr_vote(lt_sr),
        vw_sr_vote(vw_sr),
        ribbon_vote(ribbon),
    ]
    vsum = sum(votes)
    pos = sum(1 for x in votes if x > 0)
    neg = sum(1 for x in votes if x < 0)

    if vsum >= VOTE_THRESHOLD and neg == 0:
        direction = 1      # 롱 정렬
    elif vsum <= -VOTE_THRESHOLD and pos == 0:
        direction = -1     # 숏 정렬
    else:
        direction = 0      # 중립·혼조

    base = abs(vsum) / 6.0
    conf = base * GAP_PENALTY[gap]

    if direction != 0:
        # VWAP 기울기: 정렬 방향과 일치/반대
        slope_sign = 1 if vw_slope == "상승" else (-1 if vw_slope == "하락" else 0)
        if slope_sign == direction:
            conf += 0.05
        elif slope_sign == -direction:
            conf -= 0.10
        # VWAP 밴드폭: 확장=추세 지속(+), 수축=소멸(-)
        if vw_bw == "확장":
            conf += 0.05
        elif vw_bw == "수축":
            conf -= 0.05
        # VWAP 밴드상태: 밴드워킹=추세(+)
        if vw_band == "밴드워킹":
            conf += 0.05

    conf = max(0.0, min(1.0, conf))
    return vsum, pos, neg, direction, conf


def verdict_text(direction, conf, gap):
    if direction > 0:
        base = "강한 롱 정렬" if conf >= 0.8 else "롱 우세" if conf >= 0.5 else "롱 약세 정렬"
    elif direction < 0:
        base = "강한 숏 정렬" if conf >= 0.8 else "숏 우세" if conf >= 0.5 else "숏 약세 정렬"
    else:
        base = "중립·혼조"
    if gap == "되돌림확실":
        base += " · 과열, 되돌림 경계"
    elif gap == "되돌림주의":
        base += " · 되돌림 주의"
    return base


def build_rows():
    rows = []
    seq = 0
    for combo in product(*AXES):
        seq += 1
        (trend, ribbon, gap, cloud, vw_slope, vw_bw, vw_band, vw_sr, lt_trend, lt_sr) = combo
        vsum, pos, neg, direction, conf = score(*combo)
        v = verdict_text(direction, conf, gap)
        rows.append({
            "no": seq, "combo": combo, "conf": conf, "dir": direction, "verdict": v,
        })
    return rows


HEADER = """# 신호-교차표 (프로그램/자동조회용 · 대용량) — 이치모쿠 단독 10축 완전 열거

> **⚠ 프로그램/자동조회용 대용량 파일입니다.** 사람이 눈으로 훑는 용도가 아니라, 실차트
> 우측 상단 이치모쿠 테이블의 10개 상태값을 그대로 읽어 같은 조합 행을 **기계적으로 조회**하는
> 용도입니다. 사람용 요약은 별도 6축 축약표를 참조하세요.
>
> KJH-Trading Capital · 스크립트 개발자 산출 · 보조 참고 자료(미검증)
> 생성: `pinescript/tools/gen_cross_table_program.py` (재실행 시 동일 결과 — 결정론적)
> 근거 코드: `pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine` (읽기만, 무수정)

## 열 · 상태 범례 (10축, 각 3상태)

| 열 | 상태값 | 코드 근거(변수) |
|---|---|---|
| 추세 | 상승 / 하락 / 중립 | `dir05·dir10·dir20` 부호합 |
| 리본추세 | 상승 / 하락 / 횡보 | `ribbonState` (대기→횡보) |
| 이격도 | 중립 / 되돌림주의 / 되돌림확실 | `disparityState` |
| 구름대 | 위 / 안 / 아래 | `cloudPosText` |
| VWAP기울기 | 상승 / 하락 / 평탄 | `vwSlopeText` (평탄(중심)→평탄) |
| VWAP밴드폭 | 확장 / 수축 / 유지 | `vwBwStateText` |
| VWAP밴드상태 | 밴드워킹 / 지지 / 저항 | `vwBandStateShort` (상단/하단 밴드워킹→밴드워킹, 하단지지→지지, 상단저항→저항, 중앙(공방)→근접 쪽; ※ 축약 매핑 참조) |
| VWAP지지저항 | 지지 / 저항 / 없음 | `vwSrText` (VWAP 위=지지·아래=저항·미계산=없음) |
| 장기추세 | 상승 / 하락 / 중립 | `ltStateBase`+크로스 8종 → 방향 축약 |
| 장기지지저항 | 지지우세 / 저항우세 / 혼조 | `ltSrText` 100선×200선 9종 → 축약 |

### 3상태 축약 매핑 (다→3)

- **장기추세 (8종 → 3):** `골든 크로스·강한 상승·상승·약한 상승` → **상승** / `데드 크로스·강한 하락·하락·약한 하락` → **하락** / (확립 전 방향 미정) → **중립**. (강/약은 신뢰도 세분이라 방향은 상승/하락으로 통합. 코드상 `ltUp` 부호가 방향을 결정.)
- **장기지지저항 (100선×200선 9종 → 3):** 200선 상태를 우선(장기 기준). `200선 지지` 계열(둘 다 지지·100저항+200지지) → **지지우세** / `200선 저항` 계열(둘 다 저항·100지지+200저항) → **저항우세** / `200선 중립` → **혼조**. (코드 `ltM2St` 부호가 셀 배경색 기준이므로 200선을 대표로 축약.)
- **VWAP밴드상태 (4종 → 3):** `상단·하단 밴드워킹` → **밴드워킹** / `하단 지지` → **지지** / `상단 저항` → **저항** / `중앙(공방)`은 별도 3번째 상태가 없으므로 **근접 쪽(지지/저항)으로 문서상 편입하지 않고**, 본 표에서는 3상태(밴드워킹/지지/저항)만 열거한다. 실차트에서 `중앙(공방)`이 뜨면 방향 판정에서 이 축은 **중립(투표 0, 보정 0)** 으로 간주하고 가장 가까운 밴드 쪽 행을 참조한다(지지·저항 중 종가가 가까운 쪽). ※ 이 축은 방향 투표축이 아니라 신뢰도 보정축이므로 방향 결론에는 영향이 작다.
- **리본추세:** `대기`(초기)는 방향성 없음 → **횡보**로 편입.
- **VWAP기울기 `평탄(중심)`** → **평탄**(방향 0).

## 방향 판정 규칙 (앞 리뷰 규칙 그대로)

**방향 투표축 6개** (각 롱계열 +1 / 숏계열 -1 / 중립계열 0):
추세 · 구름대 · 장기추세 · 장기지지저항 · VWAP지지저항 · 리본추세.

```
vsum = 6개 투표 부호합 (-6..+6)
pos = 양수 표 개수, neg = 음수 표 개수
롱 정렬 : vsum >= +3  AND  neg == 0
숏 정렬 : vsum <= -3  AND  pos == 0
그 외   : 중립·혼조
```

**신뢰도(0~1)** — 보정축 4개(이격도·VWAP밴드폭·VWAP기울기·VWAP밴드상태)로 가감:
```
base = |vsum| / 6
conf = base × 이격도페널티(중립1.00 / 되돌림주의0.85 / 되돌림확실0.70)
  + VWAP기울기 정렬방향 일치 +0.05 / 반대 -0.10 / 평탄 0
  + VWAP밴드폭 확장 +0.05 / 수축 -0.05 / 유지 0
  + VWAP밴드상태 밴드워킹 +0.05 / 지지·저항 0
conf = clamp(0, 1)   (중립·혼조는 base×이격도페널티만)
```
등급: 신뢰도 ≥0.80 강한 정렬 / 0.50~0.80 우세 / <0.50 약세 정렬(방향은 있음).

## 리스크 (필독)

- **미검증 참조자료.** 이 표는 이치모쿠 10축의 상태 정렬을 규칙으로 요약한 것이지 진입 신호가 아니다. 신뢰도는 "축들이 얼마나 한 방향인가"의 일치도일 뿐 승률·기대수익이 아니다.
- **역추세·되돌림 행 주의.** 되돌림주의/확실, 방향과 반대인 VWAP기울기 등은 신뢰도로 감점되나, 최종 판단은 실차트·손익비(R:R)·시장 국면 확인 후 CEO/본부장이 내린다. 단일 신호 불신, 자본 보존 우선.

---

## 교차 상태표 (No 1..59049, 열거 순서 = 축 사전순)

"""


def render(rows):
    out = [HEADER]
    out.append("| No | " + " | ".join(COLS) + " | 방향 | 신뢰도 | 종합 해석 |")
    out.append("|---|" + "---|" * (len(COLS)) + "---|---|---|")
    dir_txt = {1: "롱", -1: "숏", 0: "중립"}
    for r in rows:
        cells = " | ".join(r["combo"])
        out.append(
            f"| {r['no']} | {cells} | {dir_txt[r['dir']]} | {r['conf']:.2f} | {r['verdict']} |"
        )
    out.append("")
    out.append(f"**총 {len(rows):,}행** (3^10 = 59,049 완전 열거 · No 1..{len(rows)} 순차).")
    out.append("")
    return "\n".join(out)


def main():
    rows = build_rows()
    assert len(rows) == 59049, f"행 수 오류: {len(rows)}"
    md = render(rows)
    out_path = Path(__file__).resolve().parent.parent / "신호-교차표-프로그램용.md"
    out_path.write_text(md, encoding="utf-8")
    dist = Counter("롱" if r["dir"] > 0 else "숏" if r["dir"] < 0 else "중립" for r in rows)
    print(f"생성 완료: {out_path}")
    print(f"총 행수: {len(rows)}")
    print(f"방향 분포: 롱={dist['롱']}  숏={dist['숏']}  중립={dist['중립']}")
    strong = sum(1 for r in rows if r["conf"] >= 0.8 and r["dir"] != 0)
    lean = sum(1 for r in rows if 0.5 <= r["conf"] < 0.8 and r["dir"] != 0)
    print(f"강한 정렬(≥0.80): {strong}  우세(0.50~0.80): {lean}")


if __name__ == "__main__":
    main()

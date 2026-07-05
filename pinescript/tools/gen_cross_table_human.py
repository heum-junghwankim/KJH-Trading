#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
신호-교차표 (사람 룩업용 · 슬림) 생성기 — 이치모쿠 단독 6축 완전 열거
================================================================================
근거 코드: pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine (읽기만, 무수정)

이 스크립트는 이 저장소의 메인 지표(Advanced Ichimoku) **하나**가 출력하는 상태 중
사람이 실차트에서 3초 안에 눈으로 읽는 **6축**을 정규화하고, 그 완전 열거
(3·3·3·5·3·3 = 1,215행)를 결정론적으로 생성해 사람 룩업용 슬림 Markdown 표로 쓴다.
프로그램/자동조회용은 별도 10축 대용량표(gen_cross_table_program.py)를 참조(무변경).

■ 6축 정규화 (코드 근거)
  1. 추세(멀티스케일) = dir05/dir10/dir20 부호합 → 상승/하락/중립
  2. 구름대          = cloudPosText → 위/안/아래
  3. 장기추세        = ltStateBase+크로스 8종 → 상승/하락/중립
  4. VWAP 상태(5값)  = vwSlopeText × vwBwStateText 조합 → 아래 5상태
  5. 리본추세        = ribbonState(상승/하락/횡보·대기) → 상승/하락/횡보
  6. 이격도          = disparityState → 중립/되돌림주의/되돌림확실
  ※ 종전 "VWAP 지지/저항" 축은 "VWAP 상태"로 교체, "장기 지지/저항" 축은 제거.

■ VWAP 상태 5값 · 코드 9조합 → 5상태 folding (코드 근거 · 반드시 문서화)
  코드는 두 텍스트를 조합한다:
    vwSlopeText (line 940): "상승" / "하락" / "평탄(중심)"      (기울기 성분)
    vwBwStateText(line 941): "확장" / "수축" / "유지"           (밴드폭 성분)
      - "확장" = vwBwExpanding (현재 밴드폭 > 5봉 전)
      - "수축" = vwBwContracting (현재 밴드폭 < 5봉 전)
      - "유지" = 둘 다 아님 (밴드폭 동일 = 확장이 아님 → 축소 계열로 접음)
  → 3×3 = 9조합. CEO 확정 5상태는 다음과 같고, 미열거 4조합을 아래처럼 접는다(folding):

    기울기\밴드폭 | 확장         | 수축         | 유지
    -------------|-------------|-------------|-------------
    상승         | 상승 확장    | 상승 축소    | 상승 축소 (유지→축소계열)
    평탄(중심)   | 평탄 수축*   | 평탄 수축    | 평탄 수축 (평탄은 CEO가 '평탄 수축' 하나만 열거)
    하락         | 하락 확장    | 하락 축소    | 하락 축소 (유지→축소계열)

    * folding 근거:
      (a) "유지"(밴드폭 불변) → **축소 계열**: 밴드가 벌어지지 않았으므로 추세 확장 신호가
          아니다. CEO가 "유지는 축소 계열로"를 예시로 지목 → 상승/하락/평탄 모두 유지=축소로 접음.
      (b) "평탄+확장/평탄+유지" → **평탄 수축**: CEO는 평탄 계열을 '평탄 수축' 하나만 열거했다.
          평탄(기울기 없음)은 방향성 미확정 국면이므로 밴드폭이 늘어도 방향 확장으로 못 본다.
          평탄의 모든 밴드폭 상태(확장/수축/유지)를 '평탄 수축'으로 단일 folding.
  결과: 실제 관측 5상태 = 상승 확장 / 상승 축소 / 평탄 수축 / 하락 확장 / 하락 축소.

■ 방향 판정 (프로그램용 표와 정합 · VWAP 이중카운트 회피)
  방향 투표축 5개: 추세 · 구름대 · 장기추세 · VWAP상태(기울기 성분) · 리본추세.
    각 롱계열=+1, 숏계열=-1, 중립계열=0. 순합 vsum(-5..+5).
    - VWAP상태의 방향은 **기울기**로만: 상승계열(상승확장·상승축소)=+1,
      하락계열(하락확장·하락축소)=-1, 평탄수축=0.
      → VWAP은 이 한 축으로만 방향에 반영 (밴드폭은 방향 투표에 넣지 않음 = 이중카운트 없음).
  판정: vsum >= +3 AND 반대표(음수) 0개 → "롱 정렬"
        vsum <= -3 AND 반대표(양수) 0개 → "숏 정렬"
        그 외 → "중립·혼조"
  신뢰도 conf = base(|vsum|/5) × 이격도페널티 + VWAP 밴드폭 보정.
    - 이격도 페널티: 중립 ×1.00 / 되돌림주의 ×0.85 / 되돌림확실 ×0.70.
    - VWAP 밴드폭 보정(신뢰도만, 방향 아님 — 종전 장기지지저항 보정과 동일 크기 승계):
        정렬(direction≠0)일 때만 적용.
        확장(상승확장·하락확장) = +0.05 (밴드 벌어짐 = 추세 신뢰↑, 종전 '일치 +0.05' 크기)
        축소(상승축소·하락축소·평탄수축) = -0.10 (밴드 수축 = 추세 신뢰↓, 종전 '역풍 -0.10' 크기)
      ※ 평탄수축은 방향 투표 0이라 direction 형성에 기여 못 하므로 실질 보정은
        상승/하락 계열에서만 발생. 크기는 기존 사람용에서 쓰던 값 그대로(신설 없음).
  판정 임계: 합≥+3 & 반대0=롱, ≤-3 & 반대0=숏, 그 외 중립·혼조.

산출물: pinescript/신호-교차표-사람용.md
결정론적: 재실행 시 동일 결과. 코드(.pine)는 무수정.
"""

from itertools import product
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# 6축 정의. 순서 = 표 열 순서. product는 첫 축이 가장 느리게 변한다.
#   행수 = 3·3·3·5·3·3 = 1,215
# ---------------------------------------------------------------------------
TREND     = ["상승", "하락", "중립"]                          # 1 추세(멀티스케일)
CLOUD     = ["위", "안", "아래"]                              # 2 구름대
LT_TREND  = ["상승", "하락", "중립"]                          # 3 장기추세
VWAP      = ["상승 확장", "상승 축소", "평탄 수축",
             "하락 확장", "하락 축소"]                        # 4 VWAP 상태(5값 folding)
RIBBON    = ["상승", "하락", "횡보"]                          # 5 리본추세
GAP       = ["중립", "되돌림주의", "되돌림확실"]                # 6 이격도

AXES = [TREND, CLOUD, LT_TREND, VWAP, RIBBON, GAP]
COLS = ["추세", "구름대", "장기추세", "VWAP 상태", "리본추세", "이격도"]

# 방향 판정 임계
VOTE_THRESHOLD = 3     # 순합 절댓값 이 이상 + 반대표 0개 → 정렬 (투표축 5개)
GAP_PENALTY = {"중립": 1.00, "되돌림주의": 0.85, "되돌림확실": 0.70}

# VWAP 밴드폭 신뢰도 보정 (종전 장기지지저항 보정 크기 승계: 일치 +0.05 / 역풍 -0.10)
VWAP_BW_ADJ = {
    "상승 확장": +0.05, "하락 확장": +0.05,   # 밴드 확장 = 추세 신뢰↑
    "상승 축소": -0.10, "하락 축소": -0.10,   # 밴드 수축 = 추세 신뢰↓
    "평탄 수축": -0.10,                        # 축소 계열
}


def trend_vote(v):    return 1 if v == "상승" else (-1 if v == "하락" else 0)
def cloud_vote(v):    return 1 if v == "위" else (-1 if v == "아래" else 0)     # 안=0
def lt_trend_vote(v): return 1 if v == "상승" else (-1 if v == "하락" else 0)
def ribbon_vote(v):   return 1 if v == "상승" else (-1 if v == "하락" else 0)    # 횡보=0
def vwap_vote(v):
    # VWAP 상태의 방향은 기울기 성분으로만 (밴드폭은 방향 투표 제외 = 이중카운트 없음)
    if v in ("상승 확장", "상승 축소"):
        return 1
    if v in ("하락 확장", "하락 축소"):
        return -1
    return 0   # 평탄 수축


def score(trend, cloud, lt_trend, vwap, ribbon, gap):
    # 방향 투표축 5개 (VWAP은 기울기 성분 한 축으로만 — 밴드폭은 방향에 미반영)
    votes = [
        trend_vote(trend),
        cloud_vote(cloud),
        lt_trend_vote(lt_trend),
        vwap_vote(vwap),
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

    base = abs(vsum) / 5.0
    conf = base * GAP_PENALTY[gap]

    if direction != 0:
        # VWAP 밴드폭 신뢰도 보정 (방향 아닌 신뢰도만 — 확장 +0.05 / 축소 -0.10)
        conf += VWAP_BW_ADJ[vwap]

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
    for combo in product(*AXES):
        vsum, pos, neg, direction, conf = score(*combo)
        rows.append({
            "combo": combo, "conf": conf, "dir": direction,
            "verdict": verdict_text(direction, conf, gap=combo[5]),
        })
    # 신뢰도 내림차순 정렬(강→약). 동률은 원래 열거 순서(안정 정렬)로 유지.
    rows.sort(key=lambda r: r["conf"], reverse=True)
    # 표시 순서대로 No 1..N 순차 부여
    for i, r in enumerate(rows, start=1):
        r["no"] = i
    return rows


HEADER = """# 신호-교차표 (사람 룩업용 · 슬림) — 이치모쿠 단독 6축

> **사람 룩업용.** 실차트 우측 상단 이치모쿠 테이블의 6개 상태값을 눈으로 읽고, 같은
> 조합 행의 **방향·신뢰도·해석**을 3초 안에 찾는 용도. 자동조회용 10축 대용량표는
> `pinescript/신호-교차표-프로그램용.md`.
>
> KJH-Trading Capital · 스크립트 개발자 산출 · 보조 참고 자료(미검증)
> 생성: `pinescript/tools/gen_cross_table_human.py` (재실행 시 동일 결과 — 결정론적)
> 근거 코드: `pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine` (읽기만, 무수정)

## 열 범례 (6축 · 차트 어디를 보나)

| 열 | 상태값 | 차트 위치 |
|---|---|---|
| 추세 | 상승 / 하락 / 중립 | 테이블 "상승/하락 전환(1×)" 행 + 신호 삼각형 (`dir05·10·20` 부호합) |
| 구름대 | 위 / 안 / 아래 | 테이블 "구름대" 행 (종가와 밀린 구름의 위치) |
| 장기추세 | 상승 / 하락 / 중립 | 테이블 "장기 추세" 행 (MA100 vs MA200) |
| VWAP 상태 | 상승 확장 / 상승 축소 / 평탄 수축 / 하락 확장 / 하락 축소 | 테이블 "VWAP" 행 (`vwSlopeText` 기울기 × `vwBwStateText` 밴드폭) |
| 리본추세 | 상승 / 하락 / 횡보 | 테이블 "이평 리본" 행 + 압축·분출 `+`표식 |
| 이격도 | 중립 / 되돌림주의 / 되돌림확실 | 테이블 "이격도" 행 괄호값 (방향 아님 — 되돌림 리스크) |

## VWAP 상태 범례 (5값 · 코드 9조합 folding)

- 코드는 **기울기**(`vwSlopeText`: 상승/하락/평탄중심)와 **밴드폭**(`vwBwStateText`: 확장/수축/유지)을 각각 낸다 → 3×3=9조합.
- 실차트에서 읽는 5값으로 접는다(folding): **상승 확장 / 상승 축소 / 평탄 수축 / 하락 확장 / 하락 축소**.
  - 밴드폭 **"유지"(불변)** → **축소 계열**로 접음(밴드가 벌어지지 않음 = 추세 확장 신호 아님).
  - 기울기 **"평탄"** → 밴드폭 확장/수축/유지 무관하게 **"평탄 수축"** 하나로 접음(방향 미확정 국면).
- 방향 = 기울기(상승계열 +1 / 하락계열 -1 / 평탄수축 0). 밴드폭(확장/축소)은 방향 아닌 **신뢰도 보정**.

## 방향 규칙 (4줄)

- **투표축 5개**(추세·구름대·장기추세·VWAP상태·리본): 롱계열 +1 / 숏계열 -1 / 중립 0. 부호합 = `vsum`(-5..+5). VWAP은 **기울기 성분**으로만 투표(밴드폭 제외 = 이중카운트 없음).
- **롱 정렬** = `vsum ≥ +3` 그리고 반대표 0개. **숏 정렬** = `vsum ≤ -3` 그리고 반대표 0개. 그 외 = 중립·혼조.
- **신뢰도** = |vsum|/5 × 이격도페널티(중립1.00·주의0.85·확실0.70) + VWAP 밴드폭 보정(확장 +0.05·축소 −0.10, 정렬 행에만). 등급: ≥0.80 강한 정렬 / 0.50~0.80 우세 / <0.50 약세.
- **VWAP 밴드폭은 방향 투표에 넣지 않음** — 기울기로 이미 방향에 반영했으므로 이중카운트 방지. 밴드폭은 확장=신뢰↑·축소=신뢰↓의 신뢰도 보정으로만 처리.

## 리스크 (2줄)

- **미검증 참조표.** 진입 신호가 아니라 6축 정렬 요약이다. 신뢰도는 "얼마나 한 방향인가"의 일치도일 뿐 승률·기대수익이 아니다.
- **되돌림·수축 행 주의.** 되돌림주의/확실, 밴드 축소(추세 신뢰↓)는 감점되나, 최종 판단은 실차트·손익비(R:R)·국면 확인 후 CEO/본부장이 내린다. 단일 신호 불신, 자본 보존 우선.

---

## 교차 상태표 (신뢰도 내림차순 · No는 표시순 순차)

"""


def render(rows):
    out = [HEADER]
    out.append("| No | " + " | ".join(COLS) + " | 방향 | 신뢰도 | 종합 해석 |")
    out.append("|---|" + "---|" * len(COLS) + "---|---|---|")
    dir_txt = {1: "롱", -1: "숏", 0: "중립"}
    for r in rows:
        cells = " | ".join(r["combo"])
        out.append(
            f"| {r['no']} | {cells} | {dir_txt[r['dir']]} | {r['conf']:.2f} | {r['verdict']} |"
        )
    out.append("")
    out.append(f"**총 {len(rows):,}행** (3·3·3·5·3·3 = 1,215 완전 열거 · No 1..{len(rows)} 순차, 신뢰도 내림차순).")
    out.append("")
    return "\n".join(out)


def main():
    rows = build_rows()
    assert len(rows) == 1215, f"행 수 오류: {len(rows)}"
    md = render(rows)
    out_path = Path(__file__).resolve().parent.parent / "신호-교차표-사람용.md"
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

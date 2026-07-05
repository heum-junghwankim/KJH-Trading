#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
신호-교차표 (사람 룩업용 · 슬림) 생성기 — 이치모쿠 단독 7축 완전 열거
================================================================================
근거 코드: pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine (읽기만, 무수정)

이 스크립트는 이 저장소의 메인 지표(Advanced Ichimoku) **하나**가 출력하는 상태 중
사람이 실차트에서 3초 안에 눈으로 읽는 **7축**을 각 3상태로 정규화하고, 그 완전
열거(3^7 = 2,187행)를 결정론적으로 생성해 사람 룩업용 슬림 Markdown 표로 쓴다.
프로그램/자동조회용은 별도 10축 대용량표(gen_cross_table_program.py)를 참조.

■ 7축 · 3상태 정규화 (코드 근거)
  1. 추세(멀티스케일)  = dir05/dir10/dir20 부호합 → 상승/하락/중립
  2. 구름대           = cloudPosText → 위/안/아래
  3. 장기추세         = ltStateBase+크로스 8종 → 상승/하락/중립
  4. VWAP지지저항     = vwSrText(위=지지·아래=저항·미계산=없음) → 지지/저항/없음
  5. 리본추세         = ribbonState(상승/하락/횡보·대기) → 상승/하락/횡보
  6. 이격도           = disparityState → 중립/되돌림주의/되돌림확실
  7. VWAP상태(모양)   = vwSlopeText(상승/하락/평탄(중심)) → 상승/하락/평탄  ← 신규 축

■ "모양" 축 확정 근거 (코드)
  advanced-ichimoku.pine 1184행 주석: "// VWAP 상태 = 모양값(기울기 | 밴드폭) | 상태값."
  1186행 렌더: vwSlopeText + " | " + vwBwStateText + " | " + vwBandStateShort
  → "VWAP 상태" 셀의 **첫 분절(모양값)의 기울기** = vwSlopeText(상승/하락/평탄(중심)).
  루트 README(55행)도 "모양"을 "기울기(상승/하락/평탄)"로 서술 → 일치. 3종 확정.

■ 방향 판정 (프로그램용 표와 정합 · VWAP 이중카운트 회피)
  방향 투표축 5개: 추세 · 구름대 · 장기추세 · VWAP지지저항 · 리본추세.
    각 롱계열=+1, 숏계열=-1, 중립계열=0. 순합 vsum(-5..+5).
  판정: vsum >= +3 AND 반대표(음수) 0개 → "롱 정렬"
        vsum <= -3 AND 반대표(양수) 0개 → "숏 정렬"
        그 외 → "중립·혼조"
  이격도 = 신뢰도 페널티(중립 ×1.00 / 되돌림주의 ×0.85 / 되돌림확실 ×0.70).
  VWAP상태(모양) = **방향 투표에 넣지 않는다**. VWAP지지저항이 이미 VWAP 방향표라,
    모양까지 투표하면 VWAP 이중카운트가 된다(프로그램용 A군에서 고친 실수 반복 방지).
    모양은 신뢰도 보정·표시로만 처리:
      - 정렬 방향과 같은 기울기(상승↔롱 / 하락↔숏) → +0.05 (신뢰 보조)
      - 정렬 방향과 반대 기울기 → -0.10 (역풍)
      - 평탄 → 0 (중립)
    중립·혼조 행은 base×이격도페널티만(방향성 보정 무의미).

산출물: pinescript/신호-교차표-사람용.md
결정론적: 재실행 시 동일 결과. 코드(.pine)는 무수정.
"""

from itertools import product
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# 7축 정의 (각 3상태). 순서 = 표 열 순서. product는 첫 축이 가장 느리게 변한다.
# ---------------------------------------------------------------------------
TREND     = ["상승", "하락", "중립"]              # 1 추세(멀티스케일)
CLOUD     = ["위", "안", "아래"]                  # 2 구름대
LT_TREND  = ["상승", "하락", "중립"]              # 3 장기추세
VW_SR     = ["지지", "저항", "없음"]              # 4 VWAP 지지/저항
RIBBON    = ["상승", "하락", "횡보"]              # 5 리본추세
GAP       = ["중립", "되돌림주의", "되돌림확실"]    # 6 이격도
VW_SHAPE  = ["상승", "하락", "평탄"]              # 7 VWAP 상태(모양=기울기)

AXES = [TREND, CLOUD, LT_TREND, VW_SR, RIBBON, GAP, VW_SHAPE]
COLS = ["추세", "구름대", "장기추세", "VWAP지지저항", "리본추세", "이격도", "VWAP상태(모양)"]

# 방향 판정 임계
VOTE_THRESHOLD = 3     # 순합 절댓값 이 이상 + 반대표 0개 → 정렬 (투표축 5개)
GAP_PENALTY = {"중립": 1.00, "되돌림주의": 0.85, "되돌림확실": 0.70}


def trend_vote(v):    return 1 if v == "상승" else (-1 if v == "하락" else 0)
def cloud_vote(v):    return 1 if v == "위" else (-1 if v == "아래" else 0)     # 안=0
def lt_trend_vote(v): return 1 if v == "상승" else (-1 if v == "하락" else 0)
def vw_sr_vote(v):    return 1 if v == "지지" else (-1 if v == "저항" else 0)    # 없음=0
def ribbon_vote(v):   return 1 if v == "상승" else (-1 if v == "하락" else 0)    # 횡보=0


def score(trend, cloud, lt_trend, vw_sr, ribbon, gap, vw_shape):
    # 방향 투표축 5개 (VWAP상태(모양)은 제외 — VWAP지지저항과의 이중카운트 회피)
    votes = [
        trend_vote(trend),
        cloud_vote(cloud),
        lt_trend_vote(lt_trend),
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

    base = abs(vsum) / 5.0
    conf = base * GAP_PENALTY[gap]

    if direction != 0:
        # VWAP 상태(모양=기울기): 정렬 방향과 일치(+0.05)/반대(-0.10)/평탄(0). 투표 아닌 보정만.
        shape_sign = 1 if vw_shape == "상승" else (-1 if vw_shape == "하락" else 0)
        if shape_sign == direction:
            conf += 0.05
        elif shape_sign == -direction:
            conf -= 0.10

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


HEADER = """# 신호-교차표 (사람 룩업용 · 슬림) — 이치모쿠 단독 7축

> **사람 룩업용.** 실차트 우측 상단 이치모쿠 테이블의 7개 상태값을 눈으로 읽고, 같은
> 조합 행의 **방향·신뢰도·해석**을 3초 안에 찾는 용도. 자동조회용 10축 대용량표는
> `pinescript/신호-교차표-프로그램용.md`.
>
> KJH-Trading Capital · 스크립트 개발자 산출 · 보조 참고 자료(미검증)
> 생성: `pinescript/tools/gen_cross_table_human.py` (재실행 시 동일 결과 — 결정론적)
> 근거 코드: `pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine` (읽기만, 무수정)

## 열 범례 (7축 · 차트 어디를 보나)

| 열 | 상태값 | 차트 위치 |
|---|---|---|
| 추세 | 상승 / 하락 / 중립 | 테이블 "상승/하락 전환(1×)" 행 + 신호 삼각형 (`dir05·10·20` 부호합) |
| 구름대 | 위 / 안 / 아래 | 테이블 "구름대" 행 (종가와 밀린 구름의 위치) |
| 장기추세 | 상승 / 하락 / 중립 | 테이블 "장기 추세" 행 (MA100 vs MA200) |
| VWAP지지저항 | 지지 / 저항 / 없음 | 테이블 "VWAP 지지/저항" 행 (VWAP 위=지지·아래=저항) |
| 리본추세 | 상승 / 하락 / 횡보 | 테이블 "이평 리본" 행 + 압축·분출 `+`표식 |
| 이격도 | 중립 / 되돌림주의 / 되돌림확실 | 테이블 "이격도" 행 괄호값 (방향 아님 — 되돌림 리스크) |
| VWAP상태(모양) | 상승 / 하락 / 평탄 | 테이블 "VWAP 상태" 행 **첫 분절(기울기)** = `vwSlopeText` |

## 방향 규칙 (4줄)

- **투표축 5개**(추세·구름대·장기추세·VWAP지지저항·리본): 롱계열 +1 / 숏계열 -1 / 중립 0. 부호합 = `vsum`(-5..+5).
- **롱 정렬** = `vsum ≥ +3` 그리고 반대표 0개. **숏 정렬** = `vsum ≤ -3` 그리고 반대표 0개. 그 외 = 중립·혼조.
- **신뢰도** = |vsum|/5 × 이격도페널티(중립1.00·주의0.85·확실0.70) + VWAP모양(정렬방향 일치 +0.05·반대 -0.10·평탄 0). 등급: ≥0.80 강한 정렬 / 0.50~0.80 우세 / <0.50 약세.
- **VWAP상태(모양)은 방향 투표에 넣지 않음** — VWAP지지저항이 이미 VWAP 방향표라 이중카운트 방지. 모양은 신뢰도 보정·표시로만(같은 기울기=신뢰 보조, 평탄=중립).

## 리스크 (2줄)

- **미검증 참조표.** 진입 신호가 아니라 7축 정렬 요약이다. 신뢰도는 "얼마나 한 방향인가"의 일치도일 뿐 승률·기대수익이 아니다.
- **되돌림·역풍 행 주의.** 되돌림주의/확실, 방향과 반대인 VWAP기울기는 감점되나, 최종 판단은 실차트·손익비(R:R)·국면 확인 후 CEO/본부장이 내린다. 단일 신호 불신, 자본 보존 우선.

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
    out.append(f"**총 {len(rows):,}행** (3^7 = 2,187 완전 열거 · No 1..{len(rows)} 순차, 신뢰도 내림차순).")
    out.append("")
    return "\n".join(out)


def main():
    rows = build_rows()
    assert len(rows) == 2187, f"행 수 오류: {len(rows)}"
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
신호-상태 교차표 (프로그램/자동조회용) 생성기 — 12축 완전 열거 · 7표 방향 판정
================================================================================
근거 코드(읽기만, 무수정):
  pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine   (메인: 이치모쿠 10축)
  pinescript/cRSI/rsi-cyclic-smoothed.pine           (보조: cRSI posVerdict)
  pinescript/OBV-ADX/obv-adx-extreme-background.pine  (보조: OBV-ADX posVerdict)

이 스크립트는 펀드 지표군이 출력하는 **12개 상태축**을 각 3상태로 정규화하고,
그 완전 열거(3^12 = 531,441행)를 결정론적으로 스트리밍 생성한 뒤,
**정렬행(방향≠중립·혼조)만 필터**해 프로그램용 CSV로 커밋한다. 완전열거 전체는
디스크에 쌓지 않고 필터만 스트림한다(대용량 방지). 필요 시 온디맨드 재생성.

※ CCI 축 제거 근거(수학자 지적): CCI(cci-extreme-cross-signals)의 posVerdict는
  cRSI와 마찬가지로 "가격의 극단 이탈"을 같은 정보원으로 측정 → 중복. 종전엔 둘을
  osc묶음(1표)으로 합쳤으나, 중복 축 자체를 제거해 cRSI 단독 1표로 단순화한다.
  (지표 파일 pinescript/CCI 는 유지 — 이 CSV의 축에서만 뺀다.)

■ 출력 형식: CSV(표만) — 헤더 1줄 + 정렬행. 산문·범례는 담지 않는다(사람용 설명은
  MD `신호-교차표.md`의 "프로그램용 CSV 안내" 섹션). UTF-8 · RFC 4180(csv 모듈).

■ 12 표시축 · 3상태 정규화 (코드 근거)
  이치모쿠(10):
    1. 추세(멀티스케일)  = dir05/dir10/dir20 부호합 → 상승/하락/중립
    2. 리본 추세         = ribbonState → 상승/하락/횡보(대기→횡보)
    3. 이격도            = disparityState → 중립/되돌림주의/되돌림확실
    4. 구름대            = cloudPosText → 위/안/아래
    5. VWAP 기울기       = vwSlopeText → 상승/하락/평탄(평탄(중심)→평탄)
    6. VWAP 밴드폭       = vwBwStateText → 확장/수축/유지
    7. VWAP 밴드상태     = vwBandStateShort → 밴드워킹/지지/저항
    8. VWAP 지지/저항     = vwSrText → 지지/저항/없음
    9. 장기 추세         = ltStateBase+크로스 8종 → 상승/하락/중립
   10. 장기 지지/저항     = ltSrText 100선×200선 9종 → 지지우세/저항우세/혼조
  보조(2):
   11. cRSI             = posVerdict → 롱/숏/중립
   12. OBV-ADX          = posVerdict → 롱/숏/중립

■ 방향 판정 — 이중계상 제거(장기 묶음 1건) → **7표** (수학자 리뷰 확정)
  · cRSI: CCI 제거로 오실레이터는 cRSI 단독 → cRSI가 방향에 직접 1표 투표.
      (종전 osc묶음 = sign(cRSI+CCI)는 제거.)
  · 장기 묶음: lt_vote = sign(장기추세_vote + 장기지지저항_vote).
      둘 다 VWMA100/200 소스 → 1표로 합산.
  · 최종 방향표 7개: 추세 · 구름대 · 리본추세 · VWAP지지저항 · OBV-ADX · cRSI · lt_vote.
      각 +1/−1/0. (VWAP은 지지저항으로만 투표 — 기울기·밴드폭·밴드상태는 신뢰도 보정.
       이격도는 신뢰도 페널티. A군 원칙 = 1계열 1표.)
  · 순합 vsum ∈ [−7, +7].
      vsum ≥ +4 AND 반대표(음수) 0개 → 롱 정렬
      vsum ≤ −4 AND 반대표(양수) 0개 → 숏 정렬
      그 외 → 중립·혼조
    (수학자 "절반 이상 + 반대표 0" 규칙. 7표 기준 ≥4. 임계 최종값은 백테스트 대상 — 잠정.)

■ 정렬도(alignment) — 확률·승률 아님. 지표 일치도.
  base = |vsum| / 7 (0~1). 보정축으로 가감 후 clamp(0,1).
    - 이격도:      중립 ×1.00 / 되돌림주의 ×0.85 / 되돌림확실 ×0.70 (되돌림=역풍 페널티)
    - VWAP 기울기: 정렬 방향과 일치 +0.05 / 반대 -0.10 / 평탄 0
    - VWAP 밴드폭: 확장 +0.05 / 수축 -0.05 / 유지 0
    - VWAP 밴드상태: 밴드워킹 +0.05 / 지지·저항 0

■ 컬럼(정직 표기):
  No · 12축 · 방향 · 정렬도 · 정렬표수 · 유효표수 · lt묶음 · 종합해석
  - `정렬도` = alignment(일치도). "확률·승률" 아님(용어 금지).
  - `정렬표수/유효표수` = 정렬 방향과 같은 부호 표 수 / 전체 방향표 수(=7).
  - `종합해석` = 정렬 강도 서술만("강한 롱 정렬" 등). 수익 뉘앙스 단어 지양.
  - (CCI 축 제거로 osc묶음 컬럼도 제거 — cRSI가 방향에 직접 반영되어 별도 묶음 없음.)

산출물(커밋): pinescript/신호-교차표-프로그램용.csv  (정렬행만)
비커밋: 완전열거는 디스크에 담지 않음 — 스트리밍 필터만. 코드(.pine)는 무수정.
"""

import csv
from itertools import product
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# 12 표시축 정의 (각 3상태). 순서 = 표 열 순서(컬럼 사양과 일치).
#   완전 열거 = 3^12 = 531,441
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
CRSI       = ["롱", "숏", "중립"]                  # 11 cRSI (posVerdict 정규화)
OBV_ADX    = ["롱", "숏", "중립"]                  # 12 OBV-ADX (posVerdict 정규화)

AXES = [TREND, RIBBON, GAP, CLOUD, VW_SLOPE, VW_BW, VW_BAND, VW_SR,
        LT_TREND, LT_SR, CRSI, OBV_ADX]
COLS = ["추세", "리본추세", "이격도", "구름대", "VWAP기울기", "VWAP밴드폭",
        "VWAP밴드상태", "VWAP지지저항", "장기추세", "장기지지저항",
        "cRSI", "OBV-ADX"]

# 방향 판정 임계 (7표 기준 · 잠정 — 백테스트 대상)
VOTE_THRESHOLD = 4     # 순합 절댓값 이 이상 + 반대표 0개 → 정렬 (7표 중 ≥4)
VOTE_TOTAL = 7         # 유효표수(방향표 개수)
GAP_PENALTY = {"중립": 1.00, "되돌림주의": 0.85, "되돌림확실": 0.70}


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def trend_vote(v):    return 1 if v == "상승" else (-1 if v == "하락" else 0)
def ribbon_vote(v):   return 1 if v == "상승" else (-1 if v == "하락" else 0)      # 횡보=0
def cloud_vote(v):    return 1 if v == "위" else (-1 if v == "아래" else 0)        # 안=0
def lt_trend_vote(v): return 1 if v == "상승" else (-1 if v == "하락" else 0)
def lt_sr_vote(v):    return 1 if v == "지지우세" else (-1 if v == "저항우세" else 0)  # 혼조=0
def vw_sr_vote(v):    return 1 if v == "지지" else (-1 if v == "저항" else 0)       # 없음=0
def lsn_vote(v):      return 1 if v == "롱" else (-1 if v == "숏" else 0)          # cRSI/OBV-ADX


def score(trend, ribbon, gap, cloud, vw_slope, vw_bw, vw_band, vw_sr,
          lt_trend, lt_sr, crsi, obv_adx):
    # --- 묶음(이중계상 제거) ---
    #  CCI 제거로 오실레이터는 cRSI 단독 → cRSI가 방향에 직접 투표(별도 묶음 없음).
    lt_vote  = sign(lt_trend_vote(lt_trend) + lt_sr_vote(lt_sr))  # 장기 묶음(VWMA100/200)

    # --- 최종 방향표 7개 ---
    votes = [
        trend_vote(trend),   # 추세
        cloud_vote(cloud),   # 구름대
        ribbon_vote(ribbon), # 리본추세
        vw_sr_vote(vw_sr),   # VWAP 지지저항
        lsn_vote(obv_adx),   # OBV-ADX
        lsn_vote(crsi),      # cRSI (단독 투표 — CCI 제거)
        lt_vote,             # 장기 묶음
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

    # 정렬표수 = 정렬 방향과 같은 부호의 표 수 / 유효표수 = VOTE_TOTAL(=7)
    aligned = pos if direction > 0 else (neg if direction < 0 else max(pos, neg))

    # --- 정렬도(alignment) — 승률·확률 아님 ---
    base = abs(vsum) / float(VOTE_TOTAL)
    align = base * GAP_PENALTY[gap]

    if direction != 0:
        slope_sign = 1 if vw_slope == "상승" else (-1 if vw_slope == "하락" else 0)
        if slope_sign == direction:
            align += 0.05
        elif slope_sign == -direction:
            align -= 0.10
        if vw_bw == "확장":
            align += 0.05
        elif vw_bw == "수축":
            align -= 0.05
        if vw_band == "밴드워킹":
            align += 0.05

    align = max(0.0, min(1.0, align))
    return vsum, pos, neg, direction, aligned, align, lt_vote


def verdict_text(direction, align, gap):
    # 정렬 강도 서술만 — 승률·수익 뉘앙스 단어 금지
    if direction > 0:
        base = "강한 롱 정렬" if align >= 0.8 else "롱 정렬(중)" if align >= 0.5 else "롱 정렬(약)"
    elif direction < 0:
        base = "강한 숏 정렬" if align >= 0.8 else "숏 정렬(중)" if align >= 0.5 else "숏 정렬(약)"
    else:
        base = "중립·혼조"
    if gap == "되돌림확실":
        base += " · 이격 과대, 되돌림 경계"
    elif gap == "되돌림주의":
        base += " · 되돌림 주의"
    return base


# CSV 컬럼 (정직 표기): No · 12축 · 방향 · 정렬도 · 정렬표수 · 유효표수 · lt묶음 · 종합해석
CSV_HEADER = ["No"] + COLS + [
    "방향", "정렬도", "정렬표수", "유효표수", "lt묶음", "종합해석"
]

DIR_TXT = {1: "롱", -1: "숏", 0: "중립"}
VOTE_TXT = {1: "롱", -1: "숏", 0: "중립"}


def build_aligned_rows():
    """완전 열거(3^12)를 스트림하며 정렬행(방향≠0)만 수집.
    메모리에 담는 것은 정렬행뿐 — 전체 531,441행을 리스트로 쌓지 않고,
    완전열거 파일도 만들지 않는다(스트리밍 필터)."""
    total = 0
    aligned_rows = []
    for combo in product(*AXES):
        total += 1
        gap = combo[2]   # 이격도(verdict_text에 필요) — 축 순서 고정
        vsum, pos, neg, direction, aligned, align, lt_v = score(*combo)
        if direction == 0:
            continue
        aligned_rows.append({
            "combo": combo,
            "dir": direction,
            "align": align,
            "aligned": aligned,
            "lt": lt_v,
            "verdict": verdict_text(direction, align, gap),
        })
    return total, aligned_rows


def sort_rows(rows):
    # 정렬 순서: 방향(롱→숏) → 정렬도 내림차순 → (안정) 열거순
    dir_rank = {1: 0, -1: 1}
    rows.sort(key=lambda r: (dir_rank[r["dir"]], -r["align"]))
    for i, r in enumerate(rows, start=1):
        r["no"] = i
    return rows


def write_csv(rows, out_path):
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        for r in rows:
            writer.writerow([
                r["no"], *r["combo"],
                DIR_TXT[r["dir"]],
                f"{r['align']:.2f}",
                r["aligned"],
                VOTE_TOTAL,
                VOTE_TXT[r["lt"]],
                r["verdict"],
            ])


def main():
    total, rows = build_aligned_rows()
    assert total == 531441, f"완전 열거 행 수 오류: {total}"
    rows = sort_rows(rows)

    out_path = Path(__file__).resolve().parent.parent / "pinescript" / "신호-교차표-프로그램용.csv"
    write_csv(rows, out_path)

    dist = Counter(DIR_TXT[r["dir"]] for r in rows)
    strong = sum(1 for r in rows if r["align"] >= 0.8)
    mid = sum(1 for r in rows if 0.5 <= r["align"] < 0.8)
    weak = sum(1 for r in rows if r["align"] < 0.5)
    size_mb = out_path.stat().st_size / (1024 * 1024)

    print(f"생성 완료: {out_path}")
    print(f"완전 열거(로컬 계산): {total:,}  (3^12)")
    print(f"커밋 대상 정렬행: {len(rows):,}  (방향≠중립·혼조만)")
    print(f"방향 분포: 롱={dist['롱']:,}  숏={dist['숏']:,}")
    print(f"정렬도 등급: 강한(≥0.80)={strong:,}  중(0.50~0.80)={mid:,}  약(<0.50)={weak:,}")
    print(f"CSV 용량: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()

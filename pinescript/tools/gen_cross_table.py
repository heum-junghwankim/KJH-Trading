#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
신호-상태 교차표 생성기 (KJH-Trading Capital)
================================================
7개 상태축의 완전 열거(3^7 = 2,187행) 교차곱 상태표를 Markdown으로 생성한다.

■ 알고리즘 수학자 리뷰 반영 (A군: 구조 개선, 신규 데이터 불필요) — 2026 개정
  - A-1 이치모쿠 이중카운트 수정: 표시 열은 방향·구름 둘 다 유지하되(트레이더가 실차트에서 읽음),
        **점수 계산에서는 이치모쿠를 순표(net) 1개로 통합**해 메인이 2배 가중되는 오류를 제거.
          ichi_net  = dir_vote(방향) + cloud_vote(구름)   (롱유리/위=+1, 숏유리/아래=-1, 중립/안=0)
          ichi_sign = sign(ichi_net)  ∈ {-1, 0, +1}
        방향 투표 소스 = 5개: ichi_sign, 거래량, cRSI, CCI, OBV-ADX (각 ±1/0). 이치모쿠는 5중 1표.
  - A-2 상충조합 자동 중립화 + 경계 표시: 방향=롱 & 구름=아래(또는 반대)면 ichi_net=0 → ichi_sign=0으로
        자동 중립화. 추가로 방향(전환신호)과 구름(추세)이 반대인 행에는 '역추세·전환 주의(구름 돌파
        확인)' 경계 표시를 종합해석에 붙인다. 이는 이치모쿠 정통 해석(구름=추세 필터 우선, 전환신호=
        진입 타이밍)상 **역추세·전환 초기 국면 → 저확신·구름 돌파로 확인 대기**임을 뜻하는 행동 지침
        표시이며, 방향 판정(구름 vs 전환 승자)은 미검증(B군 백테스트 대상).
  - A-3 연속 신뢰도 스코어(가중치 전부 1 → 현 규칙과 동치+연속화, 엣지 주장 아님):
          S = ichi_sign + vol + crsi + cci + obv           (방향 정렬 합, -5..+5)
          C = |S| / 5                                        (일치도 0~1)
          P = 이격도 페널티: 되돌림확실 ×0.7 / 되돌림주의 ×0.85 / 중립 ×1.0
          신뢰도 = C × P (0~1), 방향 = sign(S)
        등급: 신뢰도>=0.8 → 강한 정렬, 0.5~0.8 → 우세, <0.5 → 혼조·관망. (방향 부호로 롱/숏 라벨)
        표에 '신뢰도' 열 추가(0.00~1.00, 소수 2자리).

  ※ A군은 **논리 정합성 개선이지 엣지 증명이 아니다.** 가중치·국면·상태세분(B군)은 백테스트 검증
    전까지 미반영. 이 표는 여전히 미검증 참조자료다.

산출물: pinescript/신호-상태-교차표.md
이 스크립트는 재현성을 위해 tools/ 아래 보관한다. 코드(.pine)는 건드리지 않는다.
"""

from itertools import product
from pathlib import Path

# ---------------------------------------------------------------------------
# 축 정의 (각 3상태). 순서는 표의 열 순서와 동일.
# ---------------------------------------------------------------------------
ICHI_DIR   = ["롱유리", "숏유리", "중립"]        # 이치모쿠 방향 (1× 표시 신호 방향 dir10)
ICHI_CLOUD = ["위", "아래", "안"]                # 이치모쿠 구름 (cloudPosText)
ICHI_GAP   = ["중립", "되돌림주의", "되돌림확실"]  # 이치모쿠 이격도 (disparityState)
VOL        = ["롱유리", "숏유리", "중립"]        # 거래량 압력 (posText)
CRSI       = ["롱유리", "숏유리", "중립"]        # cRSI 종합 (posVerdict 8종 축약)
CCI        = ["롱유리", "숏유리", "중립"]        # CCI 종합 (posVerdict 7종 축약)
OBVADX     = ["롱유리", "숏유리", "중립"]        # OBV-ADX 종합 (posVerdict 5종 축약)

# 이격도 페널티 상수 (A-3, 수학자 제안 — 명시적 상수)
GAP_PENALTY = {
    "되돌림확실": 0.70,
    "되돌림주의": 0.85,
    "중립":       1.00,
}

# 등급 임계 (A-3)
STRONG_THRESHOLD = 0.80   # 신뢰도 >= 0.8 → 강한 정렬
LEAN_THRESHOLD   = 0.50   # 0.5 <= 신뢰도 < 0.8 → 우세


def vote(value: str) -> int:
    """방향계열 상태값을 표로 정규화. 롱유리=+1, 숏유리=-1, 그 외=0."""
    if value == "롱유리":
        return 1
    if value == "숏유리":
        return -1
    return 0


def cloud_vote(cloud: str) -> int:
    """구름: 위=롱(+1), 아래=숏(-1), 안=중립(0)."""
    if cloud == "위":
        return 1
    if cloud == "아래":
        return -1
    return 0


def sign(x: int) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def score_row(idir, cloud, gap, vol, crsi, cci, obvadx):
    """A군 반영 스코어링. 반환: dict(S, C, P, conf, direction, ichi_conflict).

    - 이치모쿠는 순표 1개(ichi_sign)로 통합 → 방향 투표 5소스.
    - 방향/구름 정면 충돌은 ichi_net=0 → ichi_sign=0으로 자동 상쇄(A-2).
    """
    dir_v = vote(idir)
    cloud_v = cloud_vote(cloud)
    ichi_net = dir_v + cloud_v          # -2..+2 (충돌이면 0)
    ichi_sign = sign(ichi_net)          # -1/0/+1 — 이치모쿠 순표(5중 1표)

    S = ichi_sign + vote(vol) + vote(crsi) + vote(cci) + vote(obvadx)   # -5..+5
    C = abs(S) / 5.0                    # 일치도 0~1
    P = GAP_PENALTY[gap]                # 이격도 페널티
    conf = C * P                        # 신뢰도 0~1
    direction = sign(S)                 # -1/0/+1

    # A-2: 방향·구름이 정면 충돌하는 행(순표에서 상쇄된 케이스)
    ichi_conflict = (idir == "롱유리" and cloud == "아래") or (idir == "숏유리" and cloud == "위")

    return {
        "ichi_sign": ichi_sign,
        "S": S,
        "C": C,
        "P": P,
        "conf": conf,
        "direction": direction,
        "ichi_conflict": ichi_conflict,
    }


def grade_label(conf: float, direction: int) -> str:
    """신뢰도 + 방향 부호 → 등급 라벨."""
    if conf >= STRONG_THRESHOLD:
        base = "강한 정렬"
    elif conf >= LEAN_THRESHOLD:
        base = "우세"
    else:
        return "혼조·관망"
    side = "롱" if direction > 0 else "숏" if direction < 0 else "중립"
    if base == "강한 정렬":
        return f"강한 {side} 정렬"
    return f"{side} 우세"


def build_rows():
    rows = []
    seq = 0
    for idir, cloud, gap, vol, crsi, cci, obvadx in product(
        ICHI_DIR, ICHI_CLOUD, ICHI_GAP, VOL, CRSI, CCI, OBVADX
    ):
        seq += 1
        sc = score_row(idir, cloud, gap, vol, crsi, cci, obvadx)
        verdict = grade_label(sc["conf"], sc["direction"])

        # 이격도 첨언 (신뢰도엔 P로 이미 반영됨 — 텍스트는 트레이더 경고용)
        if gap == "되돌림확실":
            verdict += " · 과열, 되돌림 경계"
        elif gap == "되돌림주의":
            verdict += " · 되돌림 주의"

        # A-2: 방향·구름 상충 → 역추세·전환 초기 국면 (확인 대기 경계 표시)
        if sc["ichi_conflict"]:
            verdict += " · 역추세·전환 주의(구름 돌파 확인)"

        rows.append({
            "seq": seq,
            "idir": idir,
            "cloud": cloud,
            "gap": gap,
            "vol": vol,
            "crsi": crsi,
            "cci": cci,
            "obvadx": obvadx,
            "S": sc["S"],
            "C": sc["C"],
            "P": sc["P"],
            "conf": sc["conf"],
            "direction": sc["direction"],
            "verdict": verdict,
        })
    return rows


def sort_key(row):
    """정렬: 신뢰도 내림차순(강→약). 동률이면 롱(방향+1) 우선, 그다음 원래 열거 순번(seq).
    No는 표시순으로 순차 부여(1..2187)."""
    return (-row["conf"], -row["direction"], row["seq"])


HEADER = """# 신호-상태 교차표 (완전 열거 3^7)

> KJH-Trading Capital · 스크립트 개발자 산출 · 보조 참고 자료
> 생성: `pinescript/tools/gen_cross_table.py` (재실행 시 동일 결과 — 결정론적)
> **알고리즘 수학자 리뷰 반영 (A군: 구조 개선, 신규 데이터 불필요)**

## 1. 목적 · 읽는 법

이 표는 이 저장소의 **메인 지표(이치모쿠)** 3개 상태축과 **보조지표 4종**(거래량 압력·cRSI·CCI·OBV-ADX)의
종합 상태를 **모든 경우의 수(3^7 = 2,187가지)** 로 완전 열거하고, 각 조합에 대해
**결정론적 규칙**으로 "신뢰도"(0~1) + "종합 해석" 한 줄을 붙인 참조표다.

- 왼쪽 7개 열(이치모쿠 방향/구름/이격도 + 거래량/cRSI/CCI/OBV-ADX)이 **현재 차트 상태**를 나타낸다.
- 실차트에서 각 지표 테이블(우측 상단)이 가리키는 값을 읽어 이 표에서 같은 조합의 행을 찾으면,
  펀드 규칙에 따른 **정렬 요약(신뢰도·해석)** 을 즉시 확인할 수 있다.
- `신뢰도`가 1.0에 가까울수록 5개 방향 소스가 한쪽으로 몰린("강한 롱/숏 정렬") 상태다.
- 표는 **신뢰도 내림차순**(강→약)으로 정렬되어 있으며, `No`는 표시 순서대로 1..2187 순차 부여한다.

## 2. 축 · 상태 정의와 보조지표 축약 매핑

### 2.1 이치모쿠 (메인, overlay) — 3축과 그 코드 근거

교차표의 이치모쿠 3열은 실차트 우측 상단 테이블·신호로 다음과 같이 **재현 가능하게** 매핑된다
(근거: `pinescript/SUPER-ICHIMOKU/advanced-ichimoku.pine`).

| 축 | 상태값 | 실차트 매핑 (코드 근거) |
|---|---|---|
| 이치모쿠 방향 | 롱유리 / 숏유리 / 중립 | **1× 스케일 표시 신호 방향** = 코드의 `dir10` 상태. 실차트에서 테이블 "상승 전환(1×)" 행이 **"상승 추세"** 로 잠겨 있거나(=`buyBlocked10`, `dir10==1`) 최근 1× 매수 삼각형이면 → **롱유리**. "하락 전환(1×)" 행이 **"하락 추세"**(=`sellBlocked10`, `dir10==-1`)거나 최근 1× 매도 삼각형이면 → **숏유리**. 아직 어느 방향 신호도 안 뜬 초기(`dir10==0`)면 → **중립**. (1×를 기준으로 삼는 이유: `alertcondition`이 `gBuy10`/`gSell10`을 쓰는 이 지표의 대표 신호축이기 때문.) |
| 이치모쿠 구름 | 위 / 아래 / 안 | 코드 `cloudPosText`. 종가가 (밀린) 구름 상단 위=**위**, 하단 아래=**아래**, 구름 안=**안**. 실차트 "구름대" 행. |
| 이치모쿠 이격도 | 중립 / 되돌림주의 / 되돌림확실 | 코드 `disparityState`. 실차트 "이격도" 행 괄호값. 방향이 아니라 **되돌림 리스크**를 나타냄(신뢰도 페널티로 반영). |

> **이치모쿠 방향은 새 신호 로직이 아니라 기존 코드 요소(`dir10`) 매핑 규칙**이다. 코드는 손대지 않았다.

### 2.2 보조지표 축약 매핑 (코드 원문 verdict → 방향계열 3상태)

보조지표의 실제 `.pine` 코드가 출력하는 상태 문구(posText / posVerdict)를 방향계열 3상태로 축약했다.

**거래량 압력** (`VOLUME-PRESSURE/volume-pressure-tracker.pine`, `posText` 3종 — 이미 방향계열):
| 원본 posText | 축약 |
|---|---|
| 롱 유리 | 롱유리 |
| 숏 유리 | 숏유리 |
| 중립 | 중립 |

**cRSI 종합** (`cRSI/rsi-cyclic-smoothed.pine`, `posVerdict` 8종 → 선두어 방향계열):
| 원본 posVerdict | 축약 |
|---|---|
| 롱 유리(상단돌파 지속) | 롱유리 |
| 롱 유리(상승 다이버전스) | 롱유리 |
| 롱 유리(과매도) | 롱유리 |
| 숏 유리(하단돌파 지속) | 숏유리 |
| 숏 유리(하락 다이버전스) | 숏유리 |
| 숏 유리(과매수) | 숏유리 |
| 중립(수축) | 중립 |
| 중립 | 중립 |

**CCI 종합** (`CCI/cci-extreme-cross-signals.pine`, `posVerdict` 7종 → 방향계열):
| 원본 posVerdict | 축약 | 비고 |
|---|---|---|
| 롱 유리(추세 확인) | 롱유리 | |
| 롱 유리(둔화) | 롱유리 | |
| 숏 유리(추세 확인) | 숏유리 | |
| 숏 유리(둔화) | 숏유리 | |
| 롱 대기(과매도) | 중립 | 방향 미확정 **대기(armed)** 상태 → 방향 투표 제외(과대계상 방지) |
| 숏 대기(과매수) | 중립 | 방향 미확정 **대기(armed)** 상태 → 방향 투표 제외 |
| 중립 | 중립 | |

**OBV-ADX 종합** (`OBV-ADX/obv-adx-extreme-background.pine`, `posVerdict` 5종 → 방향계열):
| 원본 posVerdict | 축약 |
|---|---|
| 롱 유리(강화) | 롱유리 |
| 롱 유리(약화) | 롱유리 |
| 숏 유리(강화) | 숏유리 |
| 숏 유리(약화) | 숏유리 |
| 중립(휩쏘) | 중립 |

## 3. 종합 해석 규칙 (전문 — 결정론적, A군 반영판)

### 3.1 이치모쿠 순표 통합 (A-1) — 이중카운트 제거

표에는 **방향·구름 두 열을 모두 표시**(트레이더가 실차트에서 각각 읽으므로)하되,
**점수 계산에서는 이치모쿠를 하나의 순표(net)로 합쳐** 메인 지표가 2배 가중되던 오류를 없앤다.

```
dir_vote   : 방향 롱유리=+1 / 숏유리=-1 / 중립=0
cloud_vote : 구름 위=+1 / 아래=-1 / 안=0
ichi_net   = dir_vote + cloud_vote           (-2..+2)
ichi_sign  = sign(ichi_net)  ∈ {-1, 0, +1}   ← 이치모쿠는 5중 "1표"
```

### 3.2 5소스 방향 투표 + 연속 신뢰도 스코어 (A-3)

방향 투표 **5소스**: `ichi_sign`, 거래량, cRSI, CCI, OBV-ADX (각 롱유리=+1 / 숏유리=-1 / 중립=0).

```
S      = ichi_sign + vol + crsi + cci + obv            (방향 정렬 합, -5..+5)
C      = |S| / 5                                        (일치도, 0~1)
P      = 이격도 페널티: 되돌림확실 ×0.70 / 되돌림주의 ×0.85 / 중립 ×1.00
신뢰도  = C × P                                          (0~1)
방향    = sign(S)                                        (-1=숏 / 0=중립 / +1=롱)
```

> 가중치는 **전부 1** 이다. 이는 기존 다수결 규칙을 **연속화**한 것일 뿐, 특정 지표에 엣지가 있다는
> 주장이 아니다(그 검증은 B군, 백테스트 필요).

### 3.3 등급 매핑

| 신뢰도 | 방향 부호 | 등급 |
|---|---|---|
| ≥ 0.80 | +1 / -1 | 강한 롱 정렬 / 강한 숏 정렬 |
| 0.50 ~ 0.80 | +1 / -1 | 롱 우세 / 숏 우세 |
| < 0.50 | 무관 | 혼조·관망 |

### 3.4 첨언 (A-2 포함)

- **이격도 첨언(경고 텍스트):** 되돌림확실 → " · 과열, 되돌림 경계", 되돌림주의 → " · 되돌림 주의".
  (신뢰도에는 이미 페널티 P로 정량 반영됨. 텍스트는 트레이더 시각 경고용.)
- **역추세·전환 주의(구름 돌파 확인)(A-2):** 방향(전환신호)=롱유리 & 구름=아래, 또는
  방향=숏유리 & 구름=위인 행 → 순표에서 `ichi_net=0 → ichi_sign=0`으로 **자동 중립화**
  (이중카운트·모순 동시 해소)되고, 해석 끝에 " · 역추세·전환 주의(구름 돌파 확인)" 경계 표시를
  붙인다(행은 유지). 이치모쿠 정통 해석상 **구름(추세)과 반대인 전환신호는 역추세·전환 초기
  국면 → 저확신**이며, 구름을 돌파해 추세가 바뀌었는지 **확인 대기**하라는 행동 지침이다.
  이는 방향 판정이 아니라 **확인 대기 경계 표시**이며, 상충 시 어느 쪽(구름 vs 전환)이 이기는지는
  **미검증 → 백테스트(B군) 대상**이다.

## 4. 리스크 고지 (강화)

**이 표는 상태 정렬을 규칙으로 요약한 보조 참고용이며, 단일 진입 신호가 아니다.**
**A군은 논리 정합성 개선이지 엣지 증명이 아니다.**
- 신뢰도 스코어는 "5개 소스가 얼마나 한 방향인가"의 **일치도**일 뿐, 승률·기대수익을 뜻하지 않는다.
- 가중치·시장 국면(추세/횡보/역추세)·상태 세분(B군)은 **백테스트 검증 전까지 미반영**이다.
- 3^7 완전 열거이므로 방향(전환신호)과 구름(추세)이 반대인 조합(예: 방향=롱유리인데 구름=아래)도
  포함된다. 그런 행은 "역추세·전환 주의(구름 돌파 확인)"로 표기하고 순표에서 자동 중립화되며,
  **구름 돌파로 추세 전환이 확인되기 전까지는** 진입 근거로 삼아서는 안 된다(저확신 역추세 국면).
- 이 표의 "강한 롱/숏 정렬"조차 **진입 신호가 아니라 정렬 확인**일 뿐이다.
  최종 판단은 반드시 **실차트 · 손익비(R:R) · 시장 국면 확인 후** CEO/본부장 판단으로 내린다.
- 펀드 철학: **단일 신호 불신, 자본 보존 우선.**

---

## 5. 교차 상태표

"""


def render(rows):
    out = [HEADER]
    out.append("| No | 이치모쿠 방향 | 이치모쿠 구름 | 이치모쿠 이격도 | 거래량 압력 | cRSI 종합 | CCI 종합 | OBV-ADX 종합 | 신뢰도 | 종합 해석 |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for no, r in enumerate(sorted(rows, key=sort_key), start=1):
        out.append(
            f"| {no} | {r['idir']} | {r['cloud']} | {r['gap']} | "
            f"{r['vol']} | {r['crsi']} | {r['cci']} | {r['obvadx']} | "
            f"{r['conf']:.2f} | {r['verdict']} |"
        )
    out.append("")
    out.append(f"**총 {len(rows):,}행** (3^7 = 2,187 완전 열거).")
    out.append("")
    return "\n".join(out)


def grade_distribution(rows):
    """등급 분포 집계(검증·보고용). verdict 선두 등급 문자열 기준."""
    from collections import Counter
    def base(v):
        for tag in ("강한 롱 정렬", "롱 우세", "강한 숏 정렬", "숏 우세", "혼조·관망"):
            if v.startswith(tag):
                return tag
        return "기타"
    return Counter(base(r["verdict"]) for r in rows)


def main():
    rows = build_rows()
    assert len(rows) == 2187, f"행 수 오류: {len(rows)}"
    md = render(rows)
    out_path = Path(__file__).resolve().parent.parent / "신호-상태-교차표.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"생성 완료: {out_path}")
    print(f"총 행수: {len(rows)}")
    dist = grade_distribution(rows)
    print("등급 분포:")
    for tag in ("강한 롱 정렬", "롱 우세", "강한 숏 정렬", "숏 우세", "혼조·관망"):
        print(f"  {tag}: {dist.get(tag, 0)}")
    conflict = sum(1 for r in rows if "역추세·전환 주의(구름 돌파 확인)" in r["verdict"])
    print(f"역추세·전환 주의(구름 돌파 확인) 행: {conflict}")


if __name__ == "__main__":
    main()

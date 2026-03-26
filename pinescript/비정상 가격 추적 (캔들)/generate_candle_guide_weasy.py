#!/usr/bin/env python3
"""비정상 가격 추적 (캔들) 초보자 시각 가이드 PDF — WeasyPrint HTML->PDF 버전"""

import os, base64
import weasyprint

BASE = os.path.dirname(__file__)
IMG_CHART = os.path.join(BASE, "img.png")
IMG_SM = "/tmp/smart-money-view.png"
IMG_TS = "/tmp/trade-strategy-example.png"
OUTPUT = os.path.join(BASE, "..", "..", "report", "비정상_가격_캔들_초보자_가이드.pdf")


def b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def build_html():
    chart_b64 = b64(IMG_CHART)
    sm_b64 = b64(IMG_SM)
    ts_b64 = b64(IMG_TS)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Apple SD Gothic Neo', 'Noto Sans CJK KR', sans-serif; color: #222; font-size: 10pt; line-height: 1.5; }}
h1 {{ font-size: 18pt; font-weight: 700; text-align: center; margin-bottom: 6px; }}
h2 {{ font-size: 14pt; font-weight: 700; text-align: center; margin-bottom: 4px; }}
h3 {{ font-size: 11pt; font-weight: 700; margin-bottom: 3px; }}
.center {{ text-align: center; }}
.small {{ font-size: 8pt; color: #777; }}
.tip {{ background: #fff8dc; border: 1px solid #e6c84a; border-radius: 6px; padding: 6px 10px; font-size: 9pt; font-weight: 700; color: #8a6d00; text-align: center; margin: 8px 0; }}

/* ── title page ── */
.title-page {{ page-break-after: always; background: #14191f; color: #fff; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 260mm; }}
.title-page h1 {{ color: #ffc83a; font-size: 28pt; margin-bottom: 10px; }}
.title-page .sub {{ color: #ccc; font-size: 14pt; }}
.title-page .sys {{ color: #888; font-size: 10pt; margin-top: 30px; }}
.title-candles {{ display: flex; gap: 12px; justify-content: center; margin-bottom: 40px; }}
.candle {{ display: flex; flex-direction: column; align-items: center; }}
.wick {{ width: 2px; background: #3c4150; }}
.body-bull {{ border-radius: 2px; }}
.body-bear {{ border-radius: 2px; }}

/* ── content pages ── */
.page {{ page-break-after: always; }}
.page:last-child {{ page-break-after: auto; }}

/* candle basics */
.candle-pair {{ display: flex; gap: 16px; justify-content: center; margin: 10px 0; }}
.candle-box {{ width: 45%; padding: 14px; border-radius: 8px; text-align: center; }}
.candle-box.bull {{ background: #f0faf0; }}
.candle-box.bear {{ background: #faf0f0; }}
.candle-svg {{ display: block; margin: 0 auto 6px; }}

/* abnormal candles */
.abnormal-pair {{ display: flex; gap: 12px; justify-content: center; margin: 10px 0; }}
.ab-box {{ width: 45%; padding: 10px; border-radius: 8px; text-align: center; }}
.ab-box.ob {{ background: #fff5e6; border: 1px solid #ffb46a; }}
.ab-box.os {{ background: #e6f8ff; border: 1px solid #6ac8e6; }}

/* 5 signals */
.signal-row {{ display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; }}
.signal-icon {{ width: 40px; flex-shrink: 0; text-align: center; }}
.signal-text {{ flex: 1; }}
.signal-text .title {{ font-weight: 700; font-size: 11pt; }}
.signal-text .desc {{ font-size: 9pt; color: #654; }}
.signal-num {{ width: 24px; height: 24px; border-radius: 50%; color: #fff; font-weight: 700; font-size: 9pt; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}

/* stage flow */
.stage-flow {{ display: flex; gap: 4px; justify-content: center; margin: 12px 0 6px; }}
.stage-box {{ border-radius: 6px; border: 2px solid; text-align: center; padding: 6px 4px; width: 18%; }}
.stage-box .num {{ display: inline-block; width: 22px; height: 22px; border-radius: 50%; color: #fff; font-weight: 700; font-size: 9pt; line-height: 22px; text-align: center; margin-bottom: 3px; }}
.stage-box .lbl {{ font-size: 8.5pt; font-weight: 700; }}
.zone-bar {{ display: flex; margin: 0 0 10px; }}
.zone-bar div {{ padding: 3px 8px; font-size: 8pt; font-weight: 700; border-radius: 4px; }}
.zone-watch {{ background: #ffe8e8; color: #a44; width: 36%; }}
.zone-enter {{ background: #e0ffe0; color: #070; width: 64%; }}

/* images */
.full-img {{ width: 100%; margin: 6px 0; border-radius: 4px; }}

/* rules page */
.rules-page {{ background: #14191f; color: #fff; padding: 40px 20px; min-height: 260mm; text-align: center; }}
.rules-page h2.dont {{ color: #ff5a5a; margin-bottom: 12px; }}
.rules-page h2.do {{ color: #64ff8c; margin: 24px 0 12px; }}
.rules-page .item {{ font-size: 11pt; margin: 6px 0; }}
.rules-page .item.bad {{ color: #ff9696; }}
.rules-page .item.good {{ color: #96ffb4; }}
.rules-page .quote {{ color: #ffc83a; font-size: 18pt; font-weight: 700; margin-top: 30px; }}
.rules-page .quote-sub {{ color: #aaa; font-size: 13pt; margin-top: 6px; }}
</style>
</head>
<body>

<!-- ====== PAGE 1: TITLE ====== -->
<div class="title-page">
  <div class="title-candles">
    <svg width="200" height="120" viewBox="0 0 200 120">
      <line x1="20" y1="10" x2="20" y2="30" stroke="#3c4150" stroke-width="2"/>
      <rect x="14" y="30" width="12" height="50" rx="2" fill="#00deff"/>
      <line x1="20" y1="80" x2="20" y2="100" stroke="#3c4150" stroke-width="2"/>
      <line x1="55" y1="5" x2="55" y2="25" stroke="#3c4150" stroke-width="2"/>
      <rect x="49" y="25" width="12" height="40" rx="2" fill="#00c8e6"/>
      <line x1="55" y1="65" x2="55" y2="85" stroke="#3c4150" stroke-width="2"/>
      <line x1="90" y1="30" x2="90" y2="50" stroke="#3c4150" stroke-width="2"/>
      <rect x="84" y="50" width="12" height="30" rx="2" fill="#ff8c3c"/>
      <line x1="90" y1="80" x2="90" y2="100" stroke="#3c4150" stroke-width="2"/>
      <line x1="130" y1="8" x2="130" y2="28" stroke="#3c4150" stroke-width="2"/>
      <rect x="124" y="28" width="12" height="45" rx="2" fill="#ffa050"/>
      <line x1="130" y1="73" x2="130" y2="93" stroke="#3c4150" stroke-width="2"/>
      <line x1="165" y1="15" x2="165" y2="35" stroke="#3c4150" stroke-width="2"/>
      <rect x="159" y="35" width="12" height="35" rx="2" fill="#00e6ff"/>
      <line x1="165" y1="70" x2="165" y2="95" stroke="#3c4150" stroke-width="2"/>
    </svg>
  </div>
  <h1>비정상 가격 추적 (캔들)</h1>
  <div class="sub">이미지로 배우는 시각 해석 가이드</div>
  <div class="sys">KJH-Trading System</div>
</div>

<!-- ====== PAGE 2: CANDLE BASICS ====== -->
<div class="page">
  <h1>캔들 차트, 이것만 알면 됩니다</h1>
  <div class="candle-pair">
    <div class="candle-box bull">
      <svg class="candle-svg" width="40" height="90" viewBox="0 0 40 90">
        <line x1="20" y1="5" x2="20" y2="20" stroke="#444" stroke-width="2"/>
        <rect x="10" y="20" width="20" height="45" rx="3" fill="#2ea050"/>
        <line x1="20" y1="65" x2="20" y2="85" stroke="#444" stroke-width="2"/>
      </svg>
      <div style="font-weight:700;color:#1e7a32;">양봉 (상승)</div>
      <div class="small">종가 &gt; 시가</div>
    </div>
    <div class="candle-box bear">
      <svg class="candle-svg" width="40" height="90" viewBox="0 0 40 90">
        <line x1="20" y1="5" x2="20" y2="20" stroke="#444" stroke-width="2"/>
        <rect x="10" y="20" width="20" height="45" rx="3" fill="#c83232"/>
        <line x1="20" y1="65" x2="20" y2="85" stroke="#444" stroke-width="2"/>
      </svg>
      <div style="font-weight:700;color:#b42828;">음봉 (하락)</div>
      <div class="small">종가 &lt; 시가</div>
    </div>
  </div>

  <h2>이 지표가 찾는 '비정상 캔들'</h2>
  <div class="abnormal-pair">
    <div class="ab-box ob">
      <svg width="50" height="70" viewBox="0 0 50 70">
        <line x1="5" y1="12" x2="45" y2="12" stroke="#c87830" stroke-width="1" stroke-dasharray="4,2"/>
        <text x="26" y="10" font-size="7" fill="#b06828" text-anchor="start">밴드 상단</text>
        <line x1="25" y1="5" x2="25" y2="18" stroke="#804028" stroke-width="2"/>
        <rect x="17" y="18" width="16" height="32" rx="2" fill="#ff8c3c"/>
        <line x1="25" y1="50" x2="25" y2="62" stroke="#804028" stroke-width="2"/>
      </svg>
      <div style="font-weight:700;color:#c86420;">주황 = 과매수 과열</div>
      <div class="small">위에서 과열 분출</div>
    </div>
    <div class="ab-box os">
      <svg width="50" height="70" viewBox="0 0 50 70">
        <line x1="25" y1="5" x2="25" y2="18" stroke="#1e6480" stroke-width="2"/>
        <rect x="17" y="18" width="16" height="32" rx="2" fill="#00dcff"/>
        <line x1="25" y1="50" x2="25" y2="62" stroke="#1e6480" stroke-width="2"/>
        <line x1="5" y1="55" x2="45" y2="55" stroke="#1e82b4" stroke-width="1" stroke-dasharray="4,2"/>
        <text x="26" y="53" font-size="7" fill="#1e6eaa" text-anchor="start">밴드 하단</text>
      </svg>
      <div style="font-weight:700;color:#1496c8;">하늘 = 과매도 투매</div>
      <div class="small">아래서 투매 분출</div>
    </div>
  </div>

  <div class="tip">비정상 캔들 = 감시 시작 신호 (진입 신호 아님!)</div>

  <h3 class="center">실제 차트에서 이렇게 보입니다</h3>
  {"<img class='full-img' src='data:image/png;base64," + chart_b64 + "'/>" if chart_b64 else ""}
</div>

<!-- ====== PAGE 3: 5 SIGNALS + STAGES ====== -->
<div class="page">
  <h1>차트에서 보이는 5가지 모양</h1>

  <div class="signal-row" style="background:#fff5e6;">
    <div class="signal-icon">
      <svg width="36" height="22"><rect x="2" y="3" width="10" height="16" rx="2" fill="#ff8c3c"/><rect x="18" y="3" width="10" height="16" rx="2" fill="#00dcff"/></svg>
    </div>
    <div class="signal-text"><span class="title">1. 비정상 캔들</span><br><span class="desc">자리 경고 -- 주황/하늘 색 캔들</span></div>
    <div class="signal-num" style="background:#ffc83a;">0</div>
  </div>

  <div class="signal-row" style="background:#e6f8fa;">
    <div class="signal-icon">
      <svg width="36" height="22"><polygon points="8,20 16,4 24,20" fill="#37919b"/><polygon points="26,4 34,20 18,20" fill="#aa6a2d" transform="translate(-6,0)"/></svg>
    </div>
    <div class="signal-text"><span class="title">2. 다이버전스</span><br><span class="desc">힘 약화 힌트 -- 청록/갈색 삼각형</span></div>
    <div class="signal-num" style="background:#37919b;">1</div>
  </div>

  <div class="signal-row" style="background:#ebfaeb;">
    <div class="signal-icon">
      <svg width="36" height="22"><rect x="1" y="4" width="7" height="14" rx="1" fill="#00b400"/><rect x="10" y="4" width="7" height="14" rx="1" fill="#0050c8"/><rect x="19" y="4" width="7" height="14" rx="1" fill="#ffa500"/><rect x="28" y="4" width="7" height="14" rx="1" fill="#dc2828"/></svg>
    </div>
    <div class="signal-text"><span class="title">3. ATR 배경</span><br><span class="desc">실제 움직임 확인 -- 녹/파/주/빨 배경색</span></div>
    <div class="signal-num" style="background:#50b450;">2</div>
  </div>

  <div class="signal-row" style="background:#f0f0ff;">
    <div class="signal-icon">
      <svg width="36" height="22"><circle cx="10" cy="11" r="7" fill="#005f00"/><circle cx="26" cy="11" r="7" fill="#960000"/></svg>
    </div>
    <div class="signal-text"><span class="title">4. 진입 후보</span><br><span class="desc">첫 진입 신호 -- 어두운 녹/빨 동그라미+박스</span></div>
    <div class="signal-num" style="background:#007800;">3</div>
  </div>

  <div class="signal-row" style="background:#faf0f2;">
    <div class="signal-icon">
      <svg width="36" height="22"><rect x="2" y="4" width="8" height="14" rx="1" fill="#00ff00"/><polygon points="22,2 28,11 22,20 16,11" fill="#00dc00"/><rect x="32" y="4" width="0" height="14" rx="1" fill="#ff0000"/></svg>
    </div>
    <div class="signal-text"><span class="title">5. 스윕 확인</span><br><span class="desc">최종 확인 -- 밝은 봉 + 다이아몬드</span></div>
    <div class="signal-num" style="background:#c83232;">4</div>
  </div>

  <h2 style="margin-top:14px;">신호가 쌓이는 순서</h2>
  <div class="stage-flow">
    <div class="stage-box" style="border-color:#ffc83a;background:#fff8e0;height:70px;align-self:flex-end;">
      <div class="num" style="background:#ffc83a;">0</div><br>
      <div class="lbl" style="color:#8a6d00;">자리<br>경고</div>
    </div>
    <div class="stage-box" style="border-color:#37919b;background:#e0f4f6;height:80px;align-self:flex-end;">
      <div class="num" style="background:#37919b;">1</div><br>
      <div class="lbl" style="color:#143c46;">힘 약화<br>힌트</div>
    </div>
    <div class="stage-box" style="border-color:#50b450;background:#e4f8e4;height:90px;align-self:flex-end;">
      <div class="num" style="background:#50b450;">2</div><br>
      <div class="lbl" style="color:#144614;">배경<br>점등</div>
    </div>
    <div class="stage-box" style="border-color:#008200;background:#c8f0c8;height:100px;align-self:flex-end;">
      <div class="num" style="background:#008200;">3</div><br>
      <div class="lbl" style="color:#fff;">진입<br>후보</div>
    </div>
    <div class="stage-box" style="border-color:#c83232;background:#f8d0d0;height:110px;align-self:flex-end;">
      <div class="num" style="background:#c83232;">4</div><br>
      <div class="lbl" style="color:#fff;">스윕<br>확인</div>
    </div>
  </div>
  <div class="zone-bar">
    <div class="zone-watch">감시만 하세요</div>
    <div class="zone-enter">진입 검토 가능</div>
  </div>
</div>

<!-- ====== PAGE 4: SMART MONEY ====== -->
<div class="page">
  <h1>세력 관점 해석</h1>
  {"<img class='full-img' src='data:image/png;base64," + sm_b64 + "'/>" if sm_b64 else ""}
</div>

<!-- ====== PAGE 5: STRATEGY ====== -->
<div class="page">
  <h1>실전 전략 예시 (롱 &amp; 숏)</h1>
  {"<img class='full-img' src='data:image/png;base64," + ts_b64 + "'/>" if ts_b64 else ""}
</div>

<!-- ====== PAGE 6: RULES ====== -->
<div class="rules-page">
  <h2 class="dont">하지 마세요</h2>
  <div class="item bad">X&nbsp;&nbsp;&nbsp;비정상 캔들 하나만 보고 진입</div>
  <div class="item bad">X&nbsp;&nbsp;&nbsp;다이버전스만 보고 역추세 베팅</div>
  <div class="item bad">X&nbsp;&nbsp;&nbsp;배경 없는 동그라미 맹신</div>
  <div class="item bad">X&nbsp;&nbsp;&nbsp;한 봉만 보고 방향 단정</div>

  <h2 class="do">꼭 하세요</h2>
  <div class="item good">O&nbsp;&nbsp;&nbsp;손절 가격을 먼저 정하기</div>
  <div class="item good">O&nbsp;&nbsp;&nbsp;0 &gt; 4단계 순서 지키기</div>
  <div class="item good">O&nbsp;&nbsp;&nbsp;배경 켜진 구간에서만 진입 검토</div>
  <div class="item good">O&nbsp;&nbsp;&nbsp;애매하면 관망</div>

  <div class="quote">가격이 진실이다.</div>
  <div class="quote-sub">나머지는 전부 노이즈.</div>
</div>

</body>
</html>"""


def main():
    html = build_html()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    weasyprint.HTML(string=html).write_pdf(OUTPUT)
    print(f"PDF 생성 완료: {OUTPUT}")


if __name__ == "__main__":
    main()

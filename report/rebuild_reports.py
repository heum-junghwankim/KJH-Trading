#!/usr/bin/env python3
"""기존 fpdf2 리포트를 WeasyPrint HTML->PDF로 재생성 (한글 폰트 정상화)"""

import os, base64
import weasyprint

REPORT_DIR = os.path.dirname(__file__)

def b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CSS = """
@page { size: A4; margin: 12mm 14mm 16mm 14mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Apple SD Gothic Neo', 'Noto Sans CJK KR', sans-serif; color: #ddd; font-size: 9pt; line-height: 1.55; }
.dark { background: #0d1420; color: #ddd; }
.page { page-break-after: always; background: #0d1420; padding: 10px 0; min-height: 265mm; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 20pt; color: #fff; text-align: center; margin: 6px 0; }
h2 { font-size: 13pt; color: #ffc83a; margin: 10px 0 4px; }
h3 { font-size: 11pt; color: #00e6c8; margin: 8px 0 3px; }
.subtitle { text-align: center; color: #aaa; font-size: 9pt; margin-bottom: 6px; }
.header-row { display: flex; gap: 12px; margin: 8px 0; }
.header-box { flex: 1; background: #16203a; border-radius: 8px; padding: 10px 14px; }
.header-box .label { color: #888; font-size: 8pt; }
.header-box .value { color: #00e6c8; font-size: 16pt; font-weight: 700; }
.header-box .change { font-size: 11pt; }
.change.up { color: #ff4444; }
.change.down { color: #4488ff; }
.ma-ribbon { background: #0a1830; border: 1px solid #1a3050; border-radius: 8px; padding: 8px 12px; margin: 6px 0; font-size: 8pt; }
.ma-ribbon .title { color: #ffc83a; font-weight: 700; font-size: 9pt; margin-bottom: 3px; }
.summary-bar { background: #006644; border-radius: 6px; padding: 8px 14px; margin: 8px 0; color: #fff; font-size: 9pt; font-weight: 700; text-align: center; }
.chart-img { width: 100%; border-radius: 6px; margin: 6px 0; }
.chart-note { font-size: 8pt; color: #888; margin: 4px 0; }
.stage-box { border: 1px solid; border-radius: 8px; padding: 10px 14px; margin: 8px 0; }
.stage-box.s1 { border-color: #00a0b4; }
.stage-box.s2 { border-color: #44bb44; }
.stage-box.s3 { border-color: #cc8800; }
.stage-box.s4 { border-color: #aa44aa; }
.stage-label { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 8pt; font-weight: 700; color: #fff; margin-bottom: 4px; }
.stage-label.s1 { background: #00a0b4; }
.stage-label.s2 { background: #44bb44; }
.stage-label.s3 { background: #cc8800; }
.stage-label.s4 { background: #aa44aa; }
.stage-title { font-size: 11pt; color: #fff; font-weight: 700; margin-bottom: 4px; }
.stage-sub { font-size: 8pt; color: #888; margin-bottom: 6px; }
.check { color: #00e6c8; }
.conclusion { background: #1a3020; border-radius: 4px; padding: 4px 10px; margin-top: 5px; font-size: 8.5pt; color: #88dd88; font-weight: 700; }
.entry-pair { display: flex; gap: 10px; margin: 8px 0; }
.entry-box { flex: 1; border: 1px solid; border-radius: 8px; padding: 10px; }
.entry-box.bull { border-color: #00a0b4; }
.entry-box.bear { border-color: #00a0b4; }
.entry-box .tag { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 7pt; font-weight: 700; color: #fff; }
.entry-box .tag.agg { background: #00a060; }
.entry-box .tag.con { background: #0080a0; }
.entry-box .price { color: #00e6c8; font-size: 14pt; font-weight: 700; margin: 3px 0; }
.entry-box .desc { font-size: 8pt; color: #aaa; }
.confirm-box { border: 1px solid #cc8800; border-radius: 8px; padding: 10px; margin: 8px 0; }
.confirm-box .num { color: #ffc83a; font-weight: 700; }
.target-pair { display: flex; gap: 10px; margin: 8px 0; }
.target-box { flex: 1; border: 1px solid #555; border-radius: 8px; padding: 10px; }
.target-box .label { font-size: 8pt; color: #888; }
.target-box .price { color: #00e6c8; font-size: 14pt; font-weight: 700; }
.target-box .desc { font-size: 8pt; color: #aaa; }
.stop-box { background: #3a1010; border: 1px solid #cc3333; border-radius: 8px; padding: 10px; margin: 8px 0; text-align: center; }
.stop-box .price { color: #ff4444; font-size: 16pt; font-weight: 700; }
.rr-table { width: 100%; border-collapse: collapse; margin: 6px 0; font-size: 8.5pt; }
.rr-table td { padding: 4px 8px; border-bottom: 1px solid #1a3050; }
.rr-table .rr { color: #ffc83a; font-weight: 700; }
.checklist-item { display: flex; align-items: flex-start; gap: 8px; padding: 8px 10px; margin: 4px 0; border-radius: 6px; }
.checklist-item:nth-child(odd) { background: #16203a; }
.checklist-item:nth-child(even) { background: #1a2540; }
.checklist-item .box { width: 14px; height: 14px; border: 2px solid #00a060; border-radius: 3px; flex-shrink: 0; margin-top: 2px; }
.checklist-item .text { flex: 1; }
.checklist-item .text .main { color: #00e6c8; font-weight: 700; font-size: 9pt; }
.checklist-item .text .warn { color: #888; font-size: 8pt; }
.dont-box { background: #3a1010; border: 1px solid #cc3333; border-radius: 8px; padding: 10px; margin: 8px 0; }
.dont-box .item { color: #ff8888; font-size: 9pt; margin: 3px 0; }
.final-box { background: #0a2040; border: 1px solid #2a80b0; border-radius: 8px; padding: 12px; margin: 10px 0; text-align: center; }
.final-box .main { color: #fff; font-size: 10pt; }
.footer { text-align: center; color: #555; font-size: 7pt; margin-top: 8px; border-top: 1px solid #1a3050; padding-top: 4px; }
.disclaimer { color: #666; font-size: 7pt; text-align: center; margin: 6px 0; }
.summary-teal { background: #0a3040; border: 1px solid #2a80b0; border-radius: 6px; padding: 8px; margin: 8px 0; text-align: center; color: #00e6c8; font-weight: 700; font-size: 9pt; }
"""

def footer(page, total):
    return f'<div class="footer">김프로 | KJH-Trading System | "가격이 진실이다. 나머지는 전부 노이즈." {page} / {total}</div>'


def build_hpsp(chart_b64):
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="dark">
<!-- PAGE 1 -->
<div class="page">
<h1>김프로의 차트 분석 리포트</h1>
<h2 style="text-align:center;color:#fff;font-size:18pt;">HPSP (에이치피에스피)</h2>
<div class="subtitle">KRX - 일봉 - 2026년 3월 26일 기준</div>
<div class="header-row">
  <div class="header-box"><div class="label">현재가</div><div class="value">46,850원</div></div>
  <div class="header-box"><div class="label">전일 대비</div><div class="change down">-2,900 (-5.83%)</div></div>
</div>
<div class="ma-ribbon">
  <div class="title">이동평균선 (MA Ribbon) -- 가격 위에 있으면 상승 흐름</div>
  SMA 50(파랑) ~38,000 &nbsp; SMA 100(노랑) ~34,000 &nbsp; SMA 200(주황) ~31,000 &nbsp; SMA 400(보라) ~29,000
</div>
<div class="summary-bar">"상승 추세(HH/HL) 유지 중. 모든 이평선 위. 눌림 매수 구간을 기다리는 국면."</div>
<h3 style="text-align:center;">차트 전체 화면</h3>
{"<img class='chart-img' src='data:image/png;base64," + chart_b64 + "'/>" if chart_b64 else ""}
<div class="chart-note">차트 보는 법: 맨 아래 cRSI+MFI(추격위험) / 중간 거래량(연두=비정상매수) / 메인 캔들+VWAP / 위 MA Ribbon</div>
{footer(1,4)}
</div>

<!-- PAGE 2 -->
<div class="page">
<h1>김프로의 4단계 분석</h1>
<div class="subtitle">KJH-Trading 시스템으로 HPSP 현재 상태를 진단합니다</div>

<div class="stage-box s1">
  <span class="stage-label s1">1단계</span>
  <div class="stage-title">추세 구조 -- 지금 방향이 위인가 아래인가?</div>
  <div class="stage-sub">사용 지표: 스윙 라벨(HH/HL) + 적응형 VWAP + 일목 기준선/구름 + SMA</div>
  <div class="check">- 스윙 구조: HH -> HL -> HH 반복 중 = 상승 추세 유지</div>
  <div class="check">- 가격 위치: 현재가는 적응형 VWAP와 일목 기준선 위</div>
  <div class="check">- MA 정렬: 가격 > SMA50 > SMA100 > SMA200 > SMA400 = 완전 강세</div>
  <div class="check">- 구름대: 가격이 일목 구름대 위 = 중기 지지 확인</div>
  <div class="conclusion">결론: 상승 추세 유지. 롱 우선 시나리오로 접근.</div>
</div>

<div class="stage-box s2">
  <span class="stage-label s2">2단계</span>
  <div class="stage-title">비정상 가격 감지 -- 지금 자리가 눌림인가?</div>
  <div class="stage-sub">사용 지표: cRSI + 볼린저 밴드 이탈 캔들 / RSI 다이버전스 / ATR 배경 / Strong L/S</div>
  <div class="check">- 오늘 봉: -5.83% 하락 음봉 = 눌림 시작 가능성</div>
  <div class="check">- cRSI: 현재 57 (중립) = 과매도 극단(30 이하)에 아직 미도달</div>
  <div class="check">- 비정상 캔들: cRSI 극단 + 볼린저 몸통 이탈 조건 미충족</div>
  <div class="check">- RSI 다이버전스: 아직 미확인 (더 눌려야 형성 가능)</div>
  <div class="check">- Strong Long 시그널: 미발생 = 진입 후보 대기 중</div>
  <div class="conclusion">결론: 눌림 초기 단계. 비정상 캔들이 나올 때까지 대기.</div>
</div>

<div class="stage-box s3">
  <span class="stage-label s3">3단계</span>
  <div class="stage-title">거래량 확인 -- 실제로 힘이 붙었는가?</div>
  <div class="stage-sub">사용 지표: 매수/매도 거래량 분리 + 비정상 거래량 표시 + 전체 거래량 평균선</div>
  <div class="check">- 현재 거래량: 특별한 비정상 거래량 없음 (매수/매도 평균 수준)</div>
  <div class="check">- 평균선 위치: 현재 거래량은 평균선 부근 = 아직 강한 실행은 아님</div>
  <div class="check">- 진입 시 확인할 것: 눌림 바닥에서 연두색(비정상 매수) 막대 출현 여부</div>
  <div class="conclusion">결론: 아직 매수 거래량 미확인. 비정상 매수 출현 시 진입 근거 강화.</div>
</div>

<div class="stage-box s4">
  <span class="stage-label s4">4단계</span>
  <div class="stage-title">추격 위험 -- 지금 들어가면 함정인가?</div>
  <div class="stage-sub">사용 지표: cRSI + MFI 동시 추적 / 괴리 배경 / Reversal Risk 라벨(H/L)</div>
  <div class="check">- cRSI: 57 / MFI: 56 = 둘 다 중립 영역, 극단 아님</div>
  <div class="check">- 괴리 배경: 뚜렷한 노란(과열) 또는 파란(과매도) 배경 없음</div>
  <div class="check">- Reversal Risk 라벨: Bearish H 없음 = 추격 위험 경고 없음</div>
  <div class="conclusion">결론: 추격 위험 낮음. 눌림 진입 시 함정 가능성 낮은 구간.</div>
</div>
{footer(2,4)}
</div>

<!-- PAGE 3 -->
<div class="page">
<h1>매매 전략</h1>
<div class="subtitle">어디서 사고, 어디서 팔고, 어디서 손절할까? -- 초보자용 눌림 매수 시나리오</div>

<h3>현재 상황 정리</h3>
<div style="margin:4px 0 8px;font-size:9pt;">
- 상승 추세(HH/HL) 유지 중이지만, 직전 고점 51,000원에서 -5.83% 하락 시작<br>
- 아직 비정상 캔들이나 강세 다이버전스가 나오지 않았으므로 "기다리는 구간"<br>
- 눌림이 충분히 진행된 후, 비정상 캔들 + 거래량 확인이 나오면 진입 준비
</div>

<h3>눌림 진입 구간</h3>
<div class="entry-pair">
  <div class="entry-box bull"><span class="tag agg">1차 진입 (공격적)</span><div class="price">44,000 ~ 45,000원</div><div class="desc">직전 고점~저점 50% 되돌림 구간</div></div>
  <div class="entry-box bear"><span class="tag con">2차 진입 (보수적)</span><div class="price">43,000 ~ 43,500원</div><div class="desc">직전 HL(43,050) + 피보나치 44% 구간</div></div>
</div>

<div class="confirm-box">
  <h3>진입 전 반드시 확인할 3가지</h3>
  <div><span class="num">1.</span> <b>비정상 캔들 출현</b> - cRSI가 30 이하로 내려가며 볼린저 밴드를 벗어나는 캔들이 나왔는가?</div>
  <div><span class="num">2.</span> <b>거래량 확인</b> - 눌림 바닥에서 연두색(비정상 매수) 거래량 막대가 터졌는가?</div>
  <div><span class="num">3.</span> <b>다음 봉 확인</b> - 비정상 캔들 다음 봉이 양봉으로 마감하며 저점을 지키는가?</div>
</div>

<h3>목표가 -- 어디까지 오르면 팔까?</h3>
<div class="target-pair">
  <div class="target-box"><div class="label">1차 목표 (보수적)</div><div class="price">51,000원</div><div class="desc">직전 고점(HH) 재시험 구간</div></div>
  <div class="target-box"><div class="label">2차 목표 (공격적)</div><div class="price">57,000원</div><div class="desc">피보나치 확장 100% 구간</div></div>
</div>

<div class="stop-box">
  <div style="font-size:9pt;color:#ff8888;">손절 기준</div>
  <div class="price">41,500원 이탈 시</div>
  <div style="font-size:8pt;color:#aaa;">이유: 직전 HL(43,050) 아래로 완전히 밀리면 HH/HL 상승 구조 깨짐 = 추세 전환 가능성</div>
</div>

<h3>리스크 / 리워드 비율 (R/R)</h3>
<table class="rr-table">
  <tr><td>2차 진입(43,500원) 기준</td><td></td><td></td></tr>
  <tr><td>1차 목표(51,000)</td><td>수익 +7,500 / 손실 -2,000</td><td class="rr">R/R = 1 : 3.75</td></tr>
  <tr><td>2차 목표(57,000)</td><td>수익 +13,500 / 손실 -2,000</td><td class="rr">R/R = 1 : 6.75</td></tr>
</table>

<div class="summary-teal">요약: 43,000~45,000원대 눌림에서 비정상 캔들 확인 후 롱 진입 | 목표 51,000~57,000 | 손절 41,500</div>
{footer(3,4)}
</div>

<!-- PAGE 4 -->
<div class="page">
<h1>실전 체크리스트</h1>
<div class="subtitle">진입 전에 이것만 확인하세요 -- 초보자가 빠지기 쉬운 실수 방지</div>

<h3>롱 진입 전 체크리스트</h3>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">추세 방향 확인</div><div>HH/HL 구조가 유지되고 있는가?</div><div class="warn">LH/LL로 바뀌면 추세 꺾임 = 진입 보류</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">이평선 위치 확인</div><div>가격이 SMA 50 위에 있는가?</div><div class="warn">SMA 50 아래면 단기 추세 약화 신호</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">비정상 캔들 출현</div><div>cRSI 극단 + 볼린저 이탈 캔들이 보이는가?</div><div class="warn">그냥 음봉이 아닌 '비정상'이어야 함</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">거래량 압력 확인</div><div>눌림 바닥에서 비정상 매수 거래량이 나왔는가?</div><div class="warn">거래량 없는 반등은 데드캣 바운스</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">추격 위험 체크</div><div>Bearish Reversal Risk 'H'가 없는가?</div><div class="warn">있으면 세력이 물량 던지는 중일 수 있음</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">다음 봉 확인</div><div>비정상 캔들 다음 봉이 저점을 지키는가?</div><div class="warn">한 봉만 보고 진입하지 않는다</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">손절 자리 설정</div><div>41,500원 아래에 손절 주문을 넣었는가?</div><div class="warn">손절 없는 진입은 도박이다</div></div></div>

<h3>절대 하지 말아야 할 것</h3>
<div class="dont-box">
  <div class="item">X "많이 빠졌으니까 싸다"는 이유만으로 매수하지 않는다 = 비정상 캔들 신호를 기다린다</div>
  <div class="item">X 손절 자리를 정하지 않고 진입하지 않는다 = 반드시 41,500원 이탈 시 손절</div>
  <div class="item">X 한 번에 전액 진입하지 않는다 = 1차/2차 구간으로 분할 매수</div>
  <div class="item">X SNS나 커뮤니티 의견만 보고 따라 사지 않는다 = 차트가 답이다</div>
</div>

<div class="final-box">
  <div class="main">HPSP는 상승 추세가 유지되는 가운데 눌림이 시작된 초기 단계입니다.<br>
  지금은 "기다리는 구간"이며, 43,000~45,000원대에서 비정상 캔들과 거래량 확인 시 롱 진입. 급할 필요 없습니다.</div>
</div>
<div class="disclaimer">본 자료는 매매를 권유하는 것이 아니며, 투자 판단과 책임은 본인에게 있습니다.<br>과거 차트 패턴이 미래 수익을 보장하지 않습니다. 반드시 본인의 리스크 허용 범위 내에서 매매하세요.</div>
{footer(4,4)}
</div>
</body></html>"""


def build_korea_carbon(chart_b64):
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="dark">
<!-- PAGE 1 -->
<div class="page">
<h1>김프로의 차트 분석 리포트</h1>
<h2 style="text-align:center;color:#fff;font-size:18pt;">한국카본 (017960)</h2>
<div class="subtitle">KRX - 일봉 - 2026년 3월 26일 기준 - 2024년 이후 추세 분석</div>
<div class="header-row">
  <div class="header-box"><div class="label">현재가</div><div class="value">43,150원</div></div>
  <div class="header-box"><div class="label">전일 대비</div><div class="change up">+1,300 (+3.11%)</div></div>
</div>
<div class="ma-ribbon">
  <div class="title">이동평균선 (MA Ribbon) -- 모든 이평선 위에서 급등 추세 진행 중</div>
  SMA 50 ~34,000 &nbsp; SMA 100 ~28,000 &nbsp; SMA 200 ~22,000 &nbsp; SMA 400 ~15,000
</div>
<div class="summary-bar">"2024년 9,000원대에서 43,000원대까지 약 380% 폭등. 추세 과열 구간 진입 가능성. 눌림 깊이에 주목."</div>
<div class="summary-bar" style="background:#884400;">"Bearish Reversal Risk H 반복 출현 = 고점 추격 금지. 조정 후 비정상 캔들 확인 시 재진입 대기."</div>
<h3 style="text-align:center;">차트 전체 화면 (2024년 이후 일봉)</h3>
{"<img class='chart-img' src='data:image/png;base64," + chart_b64 + "'/>" if chart_b64 else ""}
<div class="chart-note">핵심: 2024년 바닥 9,000원대 HH/HL 반복 상승 | 2025년 가속 20,000 돌파 | 최근 45,800 윗꼬리 | Bearish H 반복</div>
{footer(1,4)}
</div>

<!-- PAGE 2 -->
<div class="page">
<h1>김프로의 4단계 분석</h1>
<div class="subtitle">한국카본 현재 상태 진단 -- KJH-Trading 시스템</div>

<div class="stage-box s1">
  <span class="stage-label s1">1단계</span>
  <div class="stage-title">추세 구조 -- 방향이 위인가 아래인가?</div>
  <div class="stage-sub">사용 지표: 스윙 라벨(HH/HL) + 적응형 VWAP + 일목 기준선/구름 + SMA</div>
  <div class="check">- 스윙 구조: 2024년 이후 HH -> HL -> HH 패턴 반복 = 강한 상승 추세</div>
  <div class="check">- 최근 구조: HH(45,800) -> 현재 43,150 = 아직 HL 미확정, 조정 초기</div>
  <div class="check">- 가격 위치: 현재가가 모든 이평선(50/100/200/400) 위에 위치</div>
  <div class="check">- MA 정렬: 가격 > SMA50 > SMA100 > SMA200 > SMA400 = 완전 강세 정렬</div>
  <div class="check">- 일목 구름대: 가격이 구름대 크게 상회 = 중장기 지지 구조 확인</div>
  <div class="conclusion">결론: 매우 강한 상승 추세. 롱 우선이나 급등 후 과열 리스크 동반.</div>
</div>

<div class="stage-box s2">
  <span class="stage-label s2">2단계</span>
  <div class="stage-title">비정상 가격 감지 -- 폭등 후 변곡점 가능성은?</div>
  <div class="stage-sub">사용 지표: cRSI + 볼린저 밴드 이탈 / RSI 다이버전스 / ATR 배경 / Strong L/S</div>
  <div class="check">- 오늘 봉: +3.11% 양봉이나 윗꼬리 발생 (고 45,800 -> 종 43,150)</div>
  <div class="check">- 차트 상단: 빨간 ATR 배경이 최근 여러 차례 반복 = 비정상 급등 구간</div>
  <div class="check">- cRSI: 57 (중립) = 아직 극단 과매수에서 빠져나온 직후</div>
  <div class="check">- 비정상 캔들: 최근 고점 부근에서 주황색 비정상 과매수 캔들 다수 출현</div>
  <div class="check">- Strong Short 시그널: 아직 미발생이나, 고점 윗꼬리 반복 시 주의 필요</div>
  <div class="conclusion">결론: 급등 후 과열 신호 감지. 추격 매수 금지. 눌림 대기.</div>
</div>

<div class="stage-box s3">
  <span class="stage-label s3">3단계</span>
  <div class="stage-title">거래량 확인 -- 실제로 힘이 붙었는가?</div>
  <div class="stage-sub">사용 지표: 매수/매도 거래량 분리 + 비정상 거래량 + 전체 거래량 평균선</div>
  <div class="check">- 최근 거래량: 상승 과정에서 거래량 동반 = 실제 매수 유입 확인</div>
  <div class="check">- 비정상 거래량: 급등 구간에서 비정상 매수 거래량 다수 출현 (확인 완료)</div>
  <div class="check">- 주의점: 고점 부근에서 비정상 매도 거래량이 나오면 세력 분산 시작 신호</div>
  <div class="check">- 현재: 870K 수준 = 최근 평균 대비 높은 편, 고점 경합 구간</div>
  <div class="conclusion">결론: 거래량은 살아있으나, 고점 매도 압력 감시 필요.</div>
</div>

<div class="stage-box s4">
  <span class="stage-label s4">4단계</span>
  <div class="stage-title">추격 위험 -- 지금 들어가면 함정인가?</div>
  <div class="stage-sub">사용 지표: cRSI + MFI 동시 추적 / 괴리 배경 / Reversal Risk 라벨(H/L)</div>
  <div class="check">- cRSI: 57 / MFI: 48 = cRSI가 MFI보다 높음 = 가격이 자금 흐름 앞선 상태</div>
  <div class="check">- Bearish Reversal Risk: 과거 고점마다 붉은색 'H' 반복 출현 (핵심 경고)</div>
  <div class="check">- 해석: 급등할 때마다 '가격은 올라가는데 내부 에너지가 약해지는' 패턴</div>
  <div class="check">- 현재 구간: 직전 고점(45,800) 터치 후 되밀림 = 추격 매수 최악의 타이밍</div>
  <div class="conclusion" style="background:#3a2010;color:#ffaa44;">결론: Bearish H 반복 = 고점 추격 금지. 눌림 후 Bullish H 대기.</div>
</div>
{footer(2,4)}
</div>

<!-- PAGE 3 -->
<div class="page">
<h1>매매 전략</h1>
<div class="subtitle">한국카본 -- 급등 후 눌림 매수 시나리오 (초보자용)</div>

<h3>현재 상황 정리</h3>
<div style="margin:4px 0 8px;font-size:9pt;">
- 2024년 9,000원대에서 2026년 3월 43,000원대까지 약 380% 상승<br>
- 모든 이평선(50/100/200/400) 위에서 완전 강세 정렬 유지 중<br>
- 오늘 고점 45,800원 터치 후 윗꼬리 발생 = 고점 매도 압력 감지<br>
- Bearish Reversal Risk H 반복 = 지금은 추격이 아니라 기다리는 구간
</div>

<h3>눌림 진입 구간</h3>
<div class="entry-pair">
  <div class="entry-box bull"><span class="tag agg">1차 진입 (공격적)</span><div class="price">38,000 ~ 40,000원</div><div class="desc">SMA 50 부근 + 직전 HL 지지 테스트 구간</div></div>
  <div class="entry-box bear"><span class="tag con">2차 진입 (보수적)</span><div class="price">34,000 ~ 35,000원</div><div class="desc">SMA 50 하단 + 피보나치 44% 되돌림</div></div>
</div>

<div class="confirm-box">
  <h3>진입 전 반드시 확인할 3가지</h3>
  <div><span class="num">1.</span> <b>비정상 캔들 출현</b> - cRSI 30 이하 + 볼린저 밴드 이탈 캔들이 나왔는가?</div>
  <div><span class="num">2.</span> <b>거래량 확인</b> - 눌림 바닥에서 연두색(비정상 매수) 거래량 막대 출현?</div>
  <div><span class="num">3.</span> <b>Bullish H 확인</b> - 보조 지표에서 파란 'H' (Bullish Reversal Risk)가 나왔는가?</div>
</div>

<h3>목표가 -- 어디까지 오르면 팔까?</h3>
<div class="target-pair">
  <div class="target-box"><div class="label">1차 목표 (보수적)</div><div class="price">45,800원</div><div class="desc">직전 고점(HH) 재시험</div></div>
  <div class="target-box"><div class="label">2차 목표 (공격적)</div><div class="price">55,000 ~ 57,000원</div><div class="desc">피보나치 확장 100% 구간</div></div>
</div>

<div class="stop-box">
  <div style="font-size:9pt;color:#ff8888;">손절 기준</div>
  <div class="price">32,500원 이탈 시</div>
  <div style="font-size:8pt;color:#aaa;">이유: SMA 100(~28,000) 상회하는 마지막 HL 구간 하단 이탈 = 상승 구조 훼손</div>
</div>

<h3>리스크 / 리워드 비율 (R/R)</h3>
<table class="rr-table">
  <tr><td>1차 진입(39,000원) 기준</td><td></td><td></td></tr>
  <tr><td>1차 목표(45,800)</td><td>수익 +6,800 / 손실 -6,500</td><td class="rr">R/R = 1 : 1.05</td></tr>
  <tr><td>2차 목표(55,000)</td><td>수익 +16,000 / 손실 -6,500</td><td class="rr">R/R = 1 : 2.46</td></tr>
</table>

<div class="confirm-box" style="border-color:#cc3333;">
  <h3 style="color:#ff4444;">무효화 기준 -- 이 조건이 나오면 롱 시나리오 전면 취소</h3>
  <div>- 스윙 라벨이 LH -> LL로 전환되고 SMA 50 아래로 안착하면 추세 꺾임</div>
  <div>- 직전 HL(약 30,000원대) 하향 이탈 + 약세 정렬 전환 시 매수 금지</div>
  <div>- 이 경우 기존 보유분 전량 청산, 신규 진입 중단</div>
</div>
{footer(3,4)}
</div>

<!-- PAGE 4 -->
<div class="page">
<h1>실전 체크리스트 + 한국카본 특별 주의사항</h1>
<div class="subtitle">380% 급등 종목은 일반 종목과 다른 접근이 필요합니다</div>

<h3>롱 진입 전 체크리스트</h3>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">추세 방향 확인</div><div>HH/HL 구조가 유지되고 있는가?</div><div class="warn">LH/LL 전환 시 진입 보류</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">이평선 위치</div><div>가격이 SMA 50(~34,000) 위인가?</div><div class="warn">SMA 50 아래면 단기 추세 약화</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">비정상 캔들 출현</div><div>cRSI 극단 + 볼린저 이탈 캔들이 나왔는가?</div><div class="warn">그냥 음봉이 아닌 '비정상'이어야 함</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">거래량 확인</div><div>바닥에서 비정상 매수 거래량이 나왔는가?</div><div class="warn">거래량 없는 반등은 함정</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">Bearish H 소멸</div><div>Bearish Reversal Risk H가 해소되었는가?</div><div class="warn">H 유지 중이면 추격 금지</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">Bullish H 출현</div><div>Bullish Reversal Risk H가 새로 나왔는가?</div><div class="warn">세력 흡수 시작 신호</div></div></div>
<div class="checklist-item"><div class="box"></div><div class="text"><div class="main">손절 설정</div><div>32,500원 이탈 시 손절 주문을 넣었는가?</div><div class="warn">손절 없는 진입은 도박이다</div></div></div>

<h3 style="color:#ff4444;">380% 급등 종목 특별 주의사항</h3>
<div class="dont-box">
  <div class="item">X 급등주는 빠질 때도 빠르다 = 일반 종목보다 손절 기준을 철저히 지킨다</div>
  <div class="item">X "2024년 9,000원이었으니 아직 싸다"는 착각 = 지금 기준으로만 판단한다</div>
  <div class="item">X 윗꼬리가 반복되면 세력이 물량을 던지는 중일 수 있다 = 양봉에 속지 않는다</div>
  <div class="item">X 한 번에 전액 진입하지 않는다 = 반드시 1차/2차 분할 매수</div>
  <div class="item">X Bearish H가 떠 있는 동안에는 절대 신규 매수하지 않는다</div>
</div>

<div class="final-box">
  <div class="main">한국카본은 2024년 이후 380% 급등한 강세 종목이지만, 현재 고점 부근에서 Bearish H가 반복 출현 중입니다.<br>
  지금은 "고점 추격 금지" 구간이며, 38,000~40,000원대 눌림에서 비정상 캔들과 Bullish H 확인 시 롱 재진입.</div>
</div>
<div class="disclaimer">본 자료는 매매를 권유하는 것이 아니며, 투자 판단과 책임은 본인에게 있습니다.<br>과거 차트 패턴이 미래 수익을 보장하지 않습니다. 반드시 본인의 리스크 허용 범위 내에서 매매하세요.</div>
{footer(4,4)}
</div>
</body></html>"""


def main():
    # HPSP
    hpsp_chart = b64("/tmp/HPSP_매매전략_김프로_260326/p1_img0.png")
    html = build_hpsp(hpsp_chart)
    out = os.path.join(REPORT_DIR, "HPSP_매매전략_김프로_260326.pdf")
    weasyprint.HTML(string=html).write_pdf(out)
    print(f"HPSP 생성 완료: {out}")

    # 한국카본
    kc_chart = b64("/tmp/한국카본_매매전략_김프로_200326/p1_img0.png")
    html = build_korea_carbon(kc_chart)
    out = os.path.join(REPORT_DIR, "한국카본_매매전략_김프로_200326.pdf")
    weasyprint.HTML(string=html).write_pdf(out)
    print(f"한국카본 생성 완료: {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""비정상 가격 추적 (캔들) 초보자 시각 가이드 PDF — 이미지 중심 버전 v2"""

from fpdf import FPDF
import os

FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
BASE = os.path.dirname(__file__)
IMG_CHART = os.path.join(BASE, "pinescript", "비정상 가격 추적 (캔들)", "img.png")
IMG_SM = "/tmp/smart-money-view.png"
IMG_TS = "/tmp/trade-strategy-example.png"
OUTPUT = os.path.join(BASE, "비정상_가격_캔들_초보자_가이드.pdf")


class V(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("K", "", FONT)
        self.add_font("K", "B", FONT)
        self.set_auto_page_break(auto=False)

    # ── drawing primitives ──
    def _tri(self, x1, y1, x2, y2, x3, y3, r, g, b):
        s = f"q {r/255:.3f} {g/255:.3f} {b/255:.3f} rg "
        s += f"{x1*self.k:.2f} {(self.h-y1)*self.k:.2f} m "
        s += f"{x2*self.k:.2f} {(self.h-y2)*self.k:.2f} l "
        s += f"{x3*self.k:.2f} {(self.h-y3)*self.k:.2f} l f Q"
        self._out(s)

    def _quad(self, x1, y1, x2, y2, x3, y3, x4, y4, r, g, b):
        s = f"q {r/255:.3f} {g/255:.3f} {b/255:.3f} rg "
        s += f"{x1*self.k:.2f} {(self.h-y1)*self.k:.2f} m "
        s += f"{x2*self.k:.2f} {(self.h-y2)*self.k:.2f} l "
        s += f"{x3*self.k:.2f} {(self.h-y3)*self.k:.2f} l "
        s += f"{x4*self.k:.2f} {(self.h-y4)*self.k:.2f} l f Q"
        self._out(s)

    def _circle(self, x, y, r, color):
        self.set_fill_color(*color)
        self.ellipse(x - r, y - r, r * 2, r * 2, "F")

    def _diamond(self, x, y, s, color):
        hs = s / 2
        self._quad(x, y + hs, x + hs, y, x + s, y + hs, x + hs, y + s, *color)

    def _arrow_up(self, x, y, s, c):
        self._tri(x, y + s * 0.8, x + s, y + s * 0.8, x + s / 2, y, *c)

    def _arrow_down(self, x, y, s, c):
        self._tri(x, y, x + s, y, x + s / 2, y + s * 0.8, *c)

    def _bg_rect(self, x, y, w, h, color, alpha=40):
        r, g, b = color
        a = alpha / 100
        self.set_fill_color(int(r*(1-a)+255*a), int(g*(1-a)+255*a), int(b*(1-a)+255*a))
        self.rect(x, y, w, h, "F")

    def _txt(self, x, y, text, sz=9, bold=False, color=(40, 40, 40)):
        self.set_text_color(*color)
        self.set_font("K", "B" if bold else "", sz)
        self.set_xy(x, y)
        self.cell(0, 5, text)

    def _ctxt(self, y, text, sz=11, bold=False, color=(40, 40, 40)):
        self.set_text_color(*color)
        self.set_font("K", "B" if bold else "", sz)
        self.set_y(y)
        self.cell(0, 6, text, align="C", new_x="LMARGIN", new_y="NEXT")

    # ── PAGE 1: Title ──
    def p_title(self):
        self.add_page()
        self.set_fill_color(20, 25, 35)
        self.rect(0, 0, 210, 297, "F")

        # decorative candles
        for cx, cy, bh, col in [(30, 95, 40, (0, 255, 255)), (50, 80, 30, (0, 200, 230)),
                                 (70, 110, 25, (255, 140, 60)), (140, 85, 35, (255, 160, 80)),
                                 (160, 100, 28, (0, 230, 255)), (180, 75, 45, (0, 200, 200))]:
            self.set_draw_color(60, 65, 75)
            self.set_line_width(0.4)
            self.line(cx + 5, cy - 12, cx + 5, cy)
            self.line(cx + 5, cy + bh, cx + 5, cy + bh + 10)
            self.set_fill_color(*col)
            self.rect(cx, cy, 10, bh, "F")

        self.set_y(160)
        self.set_text_color(255, 200, 60)
        self.set_font("K", "B", 28)
        self.cell(0, 14, "비정상 가격 추적 (캔들)", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self.set_text_color(200, 200, 200)
        self.set_font("K", "", 14)
        self.cell(0, 8, "이미지로 배우는 시각 해석 가이드", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(24)
        self.set_text_color(120, 120, 120)
        self.set_font("K", "", 10)
        self.cell(0, 6, "KJH-Trading System", align="C", new_x="LMARGIN", new_y="NEXT")

    # ── PAGE 2: 캔들 기초 + 비정상 캔들 ──
    def p_candle_basics(self):
        self.add_page()
        self._ctxt(10, "캔들 차트, 이것만 알면 됩니다", 18, True, (30, 30, 30))

        # 양봉
        bx, by = 25, 36
        self.set_fill_color(240, 250, 240)
        self.rect(bx, by, 75, 72, "F")
        cx, cy = bx + 28, by + 14
        self.set_draw_color(60, 60, 60)
        self.set_line_width(0.5)
        self.line(cx + 8, cy - 10, cx + 8, cy)
        self.line(cx + 8, cy + 32, cx + 8, cy + 42)
        self.set_fill_color(46, 160, 80)
        self.rect(cx, cy, 16, 32, "F")
        self._txt(bx + 8, by + 56, "양봉 (상승)", 10, True, (30, 120, 50))
        self._txt(bx + 8, by + 63, "종가 > 시가", 8, False, (80, 80, 80))

        # 음봉
        bx2 = 115
        self.set_fill_color(250, 240, 240)
        self.rect(bx2, by, 75, 72, "F")
        cx2 = bx2 + 28
        self.set_draw_color(60, 60, 60)
        self.line(cx2 + 8, cy - 10, cx2 + 8, cy)
        self.line(cx2 + 8, cy + 32, cx2 + 8, cy + 42)
        self.set_fill_color(200, 50, 50)
        self.rect(cx2, cy, 16, 32, "F")
        self._txt(bx2 + 8, by + 56, "음봉 (하락)", 10, True, (180, 40, 40))
        self._txt(bx2 + 8, by + 63, "종가 < 시가", 8, False, (80, 80, 80))

        # 비정상 캔들
        ny = 118
        self._ctxt(ny, "이 지표가 찾는 '비정상 캔들'", 13, True, (50, 50, 50))
        ny += 16

        # 과매수
        ox = 20
        self.set_fill_color(255, 245, 230)
        self.set_draw_color(255, 180, 100)
        self.set_line_width(0.5)
        self.rect(ox, ny, 82, 55, "DF")
        self.set_draw_color(100, 70, 40)
        self.set_line_width(0.4)
        self.line(ox + 21, ny + 6, ox + 21, ny + 12)
        self.line(ox + 21, ny + 38, ox + 21, ny + 44)
        self.set_fill_color(255, 140, 60)
        self.rect(ox + 15, ny + 12, 12, 26, "F")
        self.set_draw_color(200, 100, 30)
        self.set_line_width(0.3)
        self.set_dash_pattern(dash=2, gap=1)
        self.line(ox + 5, ny + 10, ox + 77, ny + 10)
        self.set_dash_pattern()
        self._txt(ox + 40, ny + 6, "밴드 상단", 7, False, (180, 100, 30))
        self._txt(ox + 5, ny + 44, "주황 = 과매수 과열", 7, True, (200, 100, 30))

        # 과매도
        ox2 = 112
        self.set_fill_color(230, 248, 255)
        self.set_draw_color(100, 200, 230)
        self.set_line_width(0.5)
        self.rect(ox2, ny, 82, 55, "DF")
        self.set_draw_color(30, 100, 130)
        self.set_line_width(0.4)
        self.line(ox2 + 21, ny + 6, ox2 + 21, ny + 12)
        self.line(ox2 + 21, ny + 38, ox2 + 21, ny + 44)
        self.set_fill_color(0, 220, 255)
        self.rect(ox2 + 15, ny + 12, 12, 26, "F")
        self.set_draw_color(30, 150, 200)
        self.set_line_width(0.3)
        self.set_dash_pattern(dash=2, gap=1)
        self.line(ox2 + 5, ny + 40, ox2 + 77, ny + 40)
        self.set_dash_pattern()
        self._txt(ox2 + 40, ny + 37, "밴드 하단", 7, False, (30, 130, 180))
        self._txt(ox2 + 5, ny + 44, "하늘 = 과매도 투매", 7, True, (30, 150, 200))

        # 핵심 메시지
        ny2 = ny + 62
        self.set_fill_color(255, 248, 220)
        self.set_draw_color(230, 200, 100)
        self.set_line_width(0.4)
        self.rect(15, ny2, 180, 14, "DF")
        self._ctxt(ny2 + 3, "비정상 캔들 = 감시 시작 신호 (진입 신호 아님!)", 9, True, (140, 90, 0))

        # 실제 차트
        ny3 = ny2 + 20
        self._ctxt(ny3, "실제 차트에서 이렇게 보입니다", 11, True, (50, 50, 50))
        if os.path.exists(IMG_CHART):
            self.image(IMG_CHART, x=15, y=ny3 + 10, w=180)

    # ── PAGE 3: 5가지 신호 + 단계 ──
    def p_signals_and_stages(self):
        self.add_page()
        self._ctxt(8, "차트에서 보이는 5가지 모양", 16, True, (30, 30, 30))

        y = 24
        signals = [
            ("① 비정상 캔들", "자리 경고", "candle", (255, 245, 230), (255, 200, 60)),
            ("② 다이버전스", "힘 약화 힌트", "triangle", (230, 248, 250), (55, 145, 155)),
            ("③ ATR 배경", "실제 움직임 확인", "background", (235, 250, 240), (80, 180, 80)),
            ("④ 진입 후보", "첫 진입 신호", "entry", (240, 245, 255), (0, 120, 0)),
            ("⑤ 스윕 확인", "최종 확인", "sweep", (250, 240, 245), (200, 50, 50)),
        ]

        for i, (title, sub, dtype, bg, scol) in enumerate(signals):
            self.set_fill_color(*bg)
            self.rect(15, y, 180, 28, "F")

            vx, vy = 22, y + 6
            if dtype == "candle":
                self.set_draw_color(80, 80, 80)
                self.set_line_width(0.3)
                self.line(vx + 4, vy, vx + 4, vy + 3)
                self.line(vx + 4, vy + 13, vx + 4, vy + 16)
                self.set_fill_color(255, 140, 60)
                self.rect(vx, vy + 3, 8, 10, "F")
                self.line(vx + 16, vy, vx + 16, vy + 3)
                self.line(vx + 16, vy + 13, vx + 16, vy + 16)
                self.set_fill_color(0, 220, 255)
                self.rect(vx + 12, vy + 3, 8, 10, "F")
            elif dtype == "triangle":
                self._arrow_up(vx, vy + 1, 10, (55, 145, 155))
                self._arrow_down(vx + 14, vy + 1, 10, (170, 105, 45))
            elif dtype == "background":
                for j, c in enumerate([(0, 180, 0), (0, 80, 200), (255, 165, 0), (220, 40, 40)]):
                    self._bg_rect(vx + j * 7, vy, 6, 14, c, 30)
            elif dtype == "entry":
                self._circle(vx + 6, vy + 7, 5, (0, 95, 0))
                self._circle(vx + 20, vy + 7, 5, (150, 0, 0))
            elif dtype == "sweep":
                self.set_fill_color(0, 255, 0)
                self.rect(vx, vy + 1, 6, 12, "F")
                self._diamond(vx + 10, vy + 1, 10, (0, 220, 0))
                self.set_fill_color(255, 0, 0)
                self.rect(vx + 24, vy + 1, 6, 12, "F")

            self._txt(52, y + 4, title, 11, True, (30, 30, 30))
            self._txt(52, y + 14, sub, 9, False, (100, 60, 20))
            self._circle(185, y + 14, 6, scol)
            self._txt(182, y + 11, str(i), 8, True, (255, 255, 255))
            y += 32

        # 단계 흐름도
        y += 2
        self._ctxt(y, "신호가 쌓이는 순서", 13, True, (30, 30, 30))
        y += 14

        colors = [(255, 200, 60), (55, 145, 155), (80, 180, 80), (0, 130, 0), (200, 50, 50)]
        txt_colors = [(100, 70, 0), (20, 60, 70), (20, 70, 20), (255, 255, 255), (255, 255, 255)]
        labels = ["자리\n경고", "힘 약화\n힌트", "배경\n점등", "진입\n후보", "스윕\n확인"]

        bx = 15
        sw = 34
        for i in range(5):
            x = bx + i * (sw + 2)
            yt = y + (4 - i) * 5
            h = 34 + i * 5
            self._bg_rect(x, yt, sw, h, colors[i], 55 - i * 8)
            self.set_draw_color(*colors[i])
            self.set_line_width(0.8)
            self.rect(x, yt, sw, h, "D")
            self._circle(x + sw / 2, yt + 8, 6, colors[i])
            self._txt(x + sw / 2 - 3, yt + 5, str(i), 9, True, (255, 255, 255))
            parts = labels[i].split("\n")
            for j, p in enumerate(parts):
                self._txt(x + 3, yt + 18 + j * 9, p, 8, True, txt_colors[i])

        # zone labels
        zy = y + 58
        self.set_fill_color(255, 235, 235)
        self.rect(bx, zy, sw * 2 + 2, 12, "F")
        self._txt(bx + 4, zy + 2, "감시만 하세요", 7, True, (180, 80, 80))

        self.set_fill_color(230, 255, 230)
        self.rect(bx + sw * 2 + 4, zy, sw * 3 + 4, 12, "F")
        self._txt(bx + sw * 2 + 8, zy + 2, "진입 검토 가능", 7, True, (0, 120, 0))

    # ── PAGE 4: 세력 관점 ──
    def p_smart_money(self):
        self.add_page()
        self._ctxt(8, "세력 관점 해석", 16, True, (30, 30, 30))
        if os.path.exists(IMG_SM):
            self.image(IMG_SM, x=5, y=20, w=200)

    # ── PAGE 5: 실전 전략 ──
    def p_strategy(self):
        self.add_page()
        self._ctxt(8, "실전 전략 예시 (롱 & 숏)", 16, True, (30, 30, 30))
        if os.path.exists(IMG_TS):
            self.image(IMG_TS, x=5, y=20, w=200)

    # ── PAGE 6: 치트시트 (컴팩트) ──
    def p_cheatsheet(self):
        self.add_page()
        self._ctxt(8, "색상 & 도형 치트시트", 16, True, (30, 30, 30))

        y = 24

        def section(title, color):
            nonlocal y
            self._txt(15, y, title, 10, True, color)
            y += 10

        def row(draw_fn, label, desc):
            nonlocal y
            draw_fn(22, y + 1)
            self._txt(46, y, label, 9, True, (30, 30, 30))
            self._txt(46, y + 6, desc, 7, False, (100, 100, 100))
            y += 14

        section("캔들 색상", (80, 60, 40))
        row(lambda x, yy: [self.set_fill_color(255, 140, 60), self.rect(x, yy, 18, 10, "F")],
            "주황", "과매수 + 밴드 초과 (위쪽 과열)")
        row(lambda x, yy: [self.set_fill_color(0, 220, 255), self.rect(x, yy, 18, 10, "F")],
            "하늘", "과매도 + 밴드 초과 (아래쪽 투매)")
        y += 2

        section("삼각형 (다이버전스)", (40, 80, 90))
        row(lambda x, yy: self._arrow_up(x, yy, 10, (55, 145, 155)),
            "청록 삼각형", "강세 다이버전스 (하락 힘 약화)")
        row(lambda x, yy: self._arrow_down(x, yy, 10, (170, 105, 45)),
            "갈색 삼각형", "약세 다이버전스 (상승 힘 약화)")
        y += 2

        section("배경색 (ATR 후속 이동)", (40, 100, 40))
        for col, lbl, desc in [((0, 180, 0), "녹색", "강세 이동"), ((0, 80, 200), "파란", "강한 강세"),
                                ((255, 165, 0), "주황", "약세 이동"), ((220, 40, 40), "빨강", "강한 약세")]:
            row(lambda x, yy, c=col: self._bg_rect(x, yy, 18, 10, c, 30), lbl, desc)
        y += 2

        section("동그라미 (진입 후보)", (0, 80, 0))
        row(lambda x, yy: self._circle(x + 5, yy + 5, 5, (0, 95, 0)),
            "어두운 녹색", "롱 진입 후보")
        row(lambda x, yy: self._circle(x + 5, yy + 5, 5, (150, 0, 0)),
            "어두운 빨강", "숏 진입 후보")
        y += 2

        section("스윕 확인 (최강 신호)", (150, 30, 30))
        row(lambda x, yy: [self.set_fill_color(0, 255, 0), self.rect(x, yy, 7, 10, "F"),
                            self._diamond(x + 10, yy, 9, (0, 220, 0))],
            "밝은 초록 봉 + 다이아몬드", "롱 스윕 확인")
        row(lambda x, yy: [self.set_fill_color(255, 0, 0), self.rect(x, yy, 7, 10, "F"),
                            self._diamond(x + 10, yy, 9, (220, 0, 0))],
            "밝은 빨강 봉 + 다이아몬드", "숏 스윕 확인")

    # ── PAGE 7: 핵심 원칙 ──
    def p_rules(self):
        self.add_page()
        self.set_fill_color(20, 25, 35)
        self.rect(0, 0, 210, 297, "F")

        y = 45
        self.set_text_color(255, 90, 90)
        self.set_font("K", "B", 16)
        self.set_y(y)
        self.cell(0, 10, "하지 마세요", align="C", new_x="LMARGIN", new_y="NEXT")
        y += 20
        for d in ["비정상 캔들 하나만 보고 진입", "다이버전스만 보고 역추세 베팅",
                   "배경 없는 동그라미 맹신", "한 봉만 보고 방향 단정"]:
            self.set_text_color(255, 150, 150)
            self.set_font("K", "", 11)
            self.set_y(y)
            self.cell(0, 7, f"X   {d}", align="C", new_x="LMARGIN", new_y="NEXT")
            y += 13

        y += 16
        self.set_text_color(100, 255, 140)
        self.set_font("K", "B", 16)
        self.set_y(y)
        self.cell(0, 10, "꼭 하세요", align="C", new_x="LMARGIN", new_y="NEXT")
        y += 20
        for d in ["손절 가격을 먼저 정하기", "0 > 4단계 순서 지키기",
                   "배경 켜진 구간에서만 진입 검토", "애매하면 관망"]:
            self.set_text_color(150, 255, 180)
            self.set_font("K", "", 11)
            self.set_y(y)
            self.cell(0, 7, f"O   {d}", align="C", new_x="LMARGIN", new_y="NEXT")
            y += 13

        y += 22
        self.set_text_color(255, 200, 60)
        self.set_font("K", "B", 18)
        self.set_y(y)
        self.cell(0, 12, "가격이 진실이다.", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(160, 160, 160)
        self.set_font("K", "", 13)
        self.cell(0, 10, "나머지는 전부 노이즈.", align="C", new_x="LMARGIN", new_y="NEXT")

    def build(self):
        self.p_title()           # 1
        self.p_candle_basics()   # 2
        self.p_signals_and_stages()  # 3
        self.p_smart_money()     # 4
        self.p_strategy()        # 5
        self.p_rules()           # 6


def main():
    pdf = V()
    pdf.build()
    pdf.output(OUTPUT)
    print(f"PDF 생성 완료: {OUTPUT}")
    print(f"총 {pdf.pages_count}페이지")


if __name__ == "__main__":
    main()

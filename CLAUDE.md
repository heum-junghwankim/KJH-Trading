# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KJH-Trading is a collection of TradingView Pine Script (v6) indicators for crypto/futures trading analysis. The project is written in Korean with English code identifiers. All indicators are designed to be used together on TradingView charts.

## Repository Structure

- `pinescript/` — All Pine Script indicators, each in its own Korean-named subdirectory with a README and `.pine` file
  - **추세 추적** (`trend-tracker.pine`) — Overlay indicator: adaptive VWAP, swing HH/HL/LH/LL labels, Ichimoku cloud, MA, alignment background
  - **비정상 가격 추적 (캔들)** (`abnormal-price-tracker-candles.pine`) — Overlay indicator: cRSI extreme + Bollinger Band breach candle coloring, RSI divergence, ATR background, smart volume signals
  - **거래량 압력 추적** (`volume-pressure-tracker.pine`) — Separate pane: buy/sell volume split, abnormal volume highlighting, total volume average line
  - **볼륨 델타** (`volume-delta.pine`) — Overlay summary: session/fixed-bar delta with buy/sell ratios and price change
  - **비정상 가격 추적 (보조)** (`abnormal-price-tracker-helper.pine`) — Separate pane: cRSI vs MFI gap, bearish/bullish reversal risk labels

## Key Concepts

The 4 indicators form a layered analysis system read in order: **Trend → Candle position → Volume pressure → Reversal risk**. Each indicator answers a specific question:
1. Trend direction (HH/HL = bullish, LH/LL = bearish)
2. Entry candidate quality (abnormal candles, divergences, ATR zones)
3. Volume confirmation (buy vs sell pressure alignment)
4. Chase risk (cRSI-MFI divergence, H/L reversal risk labels)

## Language & Conventions

- README documentation is in Korean
- Pine Script code uses English identifiers with Korean input labels/tooltips
- All scripts use Pine Script v6 (`//@version=6`)
- Indicator inputs use Korean `title` strings for TradingView UI display
- License: CC BY-NC-SA 4.0 (trend-tracker is based on Zeiierman's work)

## Working with Pine Script

- Pine Script files are not compiled/tested locally — they are copied to TradingView's Pine Editor
- There is no build system, linter, or test framework
- Changes are validated by loading the script in TradingView and visually confirming indicator behavior

## Trading Analysis Reports

- 분석 리포트 작성 시 반드시 `report/principle.md`를 먼저 읽고 따른다
- 리포트는 `report/{YYMMDD}/` 디렉토리에 저장한다
- 차트 스크린샷은 `report/{YYMMDD}/imgs/`에 종목명으로 저장한다
- PDF 파일명: `{종목}_매매전략_김프로_{YYMMDD}.pdf`
- PDF 생성은 WeasyPrint (HTML -> PDF) 방식만 사용한다 (fpdf2 등 금지)

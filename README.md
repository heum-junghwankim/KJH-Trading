# KJH-Trading

AI 트레이딩 분석과 Pine Script 지표 문서를 함께 정리하는 저장소입니다.

## 문서 바로가기

- [PineScript 트레이딩 가이드](./pinescript/README.md)
- [Auto VWAP](./pinescript/VWAP/README.md)
- [비정상 가격 추적 (캔들)](./pinescript/%EB%B9%84%EC%A0%95%EC%83%81%20%EA%B0%80%EA%B2%A9%20%EC%B6%94%EC%A0%81%20(%EC%BA%94%EB%93%A4)/README.md)
- [거래량 압력 추적](./pinescript/%EA%B1%B0%EB%9E%98%EB%9F%89%20%EC%95%95%EB%A0%A5%20%EC%B6%94%EC%A0%81/README.md)
- [MACD 다이버전스 추적](./pinescript/MACD/README.md)
- [비정상 가격 추적 (보조)](./pinescript/%EB%B9%84%EC%A0%95%EC%83%81%20%EA%B0%80%EA%B2%A9%20%EC%B6%94%EC%A0%81%20(%EB%B3%B4%EC%A1%B0)/README.md)

## 주요 폴더

- [`pinescript`](./pinescript/README.md): 트레이딩뷰에서 사용하는 지표와 설명서 모음

## 현재 포함된 대표 지표

- [`Auto VWAP`](./pinescript/VWAP/README.md): 현재 세션 또는 최근 거래일 기준 평균 체결 단가와 확장 밴드를 보는 기준선 오버레이
- [`비정상 가격 추적 (캔들)`](./pinescript/%EB%B9%84%EC%A0%95%EC%83%81%20%EA%B0%80%EA%B2%A9%20%EC%B6%94%EC%A0%81%20(%EC%BA%94%EB%93%A4)/README.md): 비정상 캔들, 다이버전스, ATR 배경을 봉 마감 기준으로 함께 보는 메인 오버레이
- [`거래량 압력 추적`](./pinescript/%EA%B1%B0%EB%9E%98%EB%9F%89%20%EC%95%95%EB%A0%A5%20%EC%B6%94%EC%A0%81/README.md): 매수/매도 거래량 압력과 비정상 거래량 확인
- [`MACD 다이버전스 추적`](./pinescript/MACD/README.md): 내부 모멘텀 재가속과 다이버전스 확인
- [`비정상 가격 추적 (보조)`](./pinescript/%EB%B9%84%EC%A0%95%EC%83%81%20%EA%B0%80%EA%B2%A9%20%EC%B6%94%EC%A0%81%20(%EB%B3%B4%EC%A1%B0)/README.md): cRSI와 MFI 기반 반전 위험 필터

## 사용하는 방법

1. 먼저 [PineScript 트레이딩 가이드](./pinescript/README.md)에서 전체 흐름을 봅니다.
2. 필요하면 각 지표별 README로 들어가 설정과 해석 방법을 확인합니다. `Auto VWAP`은 평균 단가 기준을, `비정상 가격 추적 (캔들)`은 자리와 ATR 감시 흐름을, 거래량/MACD/보조 지표는 후속 확인을 담당합니다.
3. 트레이딩뷰 `Pine Editor`에 `.pine` 파일을 붙여넣어 차트에 적용합니다.

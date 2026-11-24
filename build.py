#!/usr/bin/env python3
"""평수별 가전 적정용량 & 해외직구 관부가세 계산기 (0520goeus/life-fee-calc) — 고단가(20만~150만원) 가전·직구 구매전환 30페이지."""
from __future__ import annotations

import html
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST)

SITE_NAME = "가전용량·직구관세 계산기"
SITE_URL = "https://0520goeus.github.io/life-fee-calc"
INDEXNOW_KEY = "f19c8372a60448e9b312d840a19c5521"
GOOGLE_FILE = "google873809343766a3b6.html"
ADSENSE_CLIENT = "ca-pub-8749404731911210"
COUPANG_TRACKING = "AF9170267"
COUPANG_WIDGET_ID = 1049499

DISCLOSURE = "이 페이지는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
COUPANG_BOX = (
    '<section class="card shop">'
    f'<p class="disc">{DISCLOSURE}</p>'
    '<h3>🚀 관부가세·배송대행 걱정 없는 로켓배송 인기 가전·직구 특가</h3>'
    '<script src="https://ads-partners.coupang.com/g.js"></script>'
    f'<script>new PartnersCoupang.G({{"id":{COUPANG_WIDGET_ID},"template":"carousel",'
    f'"trackingCode":"{COUPANG_TRACKING}","width":"100%","height":"145","tsource":""}});</script>'
    "</section>"
)


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def won(n) -> str:
    return f"{int(round(n)):,}원"


CSS = """
:root{--bg:#0b1120;--card:#151f38;--line:#283659;--ink:#f1f5f9;--sub:#94a3b8;--accent:#38d9a9;--warn:#ffb703;--blue:#3b82f6}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 -apple-system,"Apple SD Gothic Neo",sans-serif}
header{background:#070b14;border-bottom:1px solid var(--line);padding:16px 20px}
.wrap{max-width:940px;margin:0 auto;padding:0 18px}
header .wrap{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
header a{color:var(--sub);text-decoration:none;font-size:14px;font-weight:600}
header .brand{color:#fff;font-size:19px;font-weight:800}
nav{display:flex;gap:14px;flex-wrap:wrap}
main{padding:28px 0 60px;display:grid;gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px}
h1{font-size:27px;line-height:1.35;margin:0 0 10px}h2{font-size:20px;margin:0 0 12px}h3{font-size:17px;margin:0 0 8px}
.sub{color:var(--sub);margin:0 0 14px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:11px}
.tile{display:grid;gap:4px;padding:14px 16px;border:1px solid var(--line);border-radius:12px;background:#0e1629;color:var(--ink);text-decoration:none}
.tile:hover{border-color:var(--accent)}
.tile b{font-size:15.5px}.tile small{color:var(--sub)}
.res-box{background:#0e1629;border:2px solid var(--accent);border-radius:14px;padding:20px;display:grid;gap:8px}
.big{font-size:34px;font-weight:800;color:var(--accent)}
input,select{width:100%;padding:11px 13px;border:1px solid var(--line);border-radius:10px;background:#0b1120;color:#fff;font:inherit;font-size:15px}
label{display:grid;gap:5px;font-size:13.5px;color:var(--sub);margin-bottom:10px}
table{width:100%;border-collapse:collapse;font-size:14.5px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:right}
th:first-child,td:first-child{text-align:left}
thead th{background:#0e1629;color:var(--sub);font-size:13px}
.faq{background:#0e1629;padding:14px 16px;border-left:4px solid var(--accent);border-radius:8px;margin:10px 0}
.shop .disc{font-size:12.5px;color:var(--sub);margin:0 0 8px}
footer{border-top:1px solid var(--line);padding:24px 0 44px;color:var(--sub);font-size:13.5px}
footer a{color:var(--accent);text-decoration:none}
"""


def write_page(rel: str, title: str, desc: str, body: str, faqs: list[tuple[str, str]] | None = None) -> str:
    canon = f"{SITE_URL}/" if rel == "index.html" else f"{SITE_URL}/{rel}"
    ld = ""
    if faqs:
        obj = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
        }
        ld = f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'
    page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<link rel="stylesheet" href="{SITE_URL}/style.css">
{ld}
<meta name="google-site-verification" content="E0MKLI_9g0wTNR9pjNKmxb_QGiA51AIK93dV9qBKumg"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8749404731911210" crossorigin="anonymous"></script><script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"평수별 가전용량 & 해외직구 관부가세 계산기","url":"https://0520goeus.github.io/life-fee-calc/"}}</script>
</head>
<body>
<header><div class="wrap">
  <a class="brand" href="{SITE_URL}/">🏠 {SITE_NAME}</a>
  <nav>
    <a href="{SITE_URL}/#pyeong">평수별 가전 용량</a>
    <a href="{SITE_URL}/#customs">해외직구 관부가세</a>
    <a href="https://0520goeus.github.io/vs-pick/">가성비 VS 사전</a>
    <a href="https://0520goeus.github.io/elec-calc/">전기세 얼마</a>
    <a href="https://0520goeus.github.io/price-note/">해뎐 가격노트</a>
  </nav>
</div></header>
<main class="wrap">{body}<div style="margin:20px auto;max-width:960px;padding:16px 20px;border-radius:14px;background:linear-gradient(135deg,#0f172a,#0f766e);color:#fff;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;"><div><div style="font-weight:800;font-size:16px;">2026 직장인·1인셀러 무매크로 자동계산 엑셀 3종 올인원 번들</div><div style="font-size:13px;opacity:.9;margin-top:2px;">1인셀러 마진·ROAS + 내집마련 매물10개 비교 + 월급 가계부·순자산 대시보드 (즉시 다운로드)</div></div><a href="https://scopekit-studio.lemonsqueezy.com/checkout/buy/ba4f11c6-8609-49c0-a947-39bead163d74" target="_blank" rel="noopener" style="background:#facc15;color:#0f172a;padding:10px 18px;border-radius:10px;font-weight:800;font-size:14px;text-decoration:none;white-space:nowrap;">3종 번들 즉시 다운로드 →</a></div>
</main>
<footer><div class="wrap">
  <p>패밀리 사이트: <a href="https://0520goeus.github.io/price-note/">해뎐 가격노트</a> · <a href="https://0520goeus.github.io/elec-calc/">전기세 얼마</a> · <a href="https://0520goeus.github.io/life-money-lab/">생활비 물가 연구소</a> · <a href="https://0520goeus.github.io/vs-pick/">가성비 VS 비교 사전</a> · <a href="https://0520goeus.github.io/money-calc-kr/">실수령액 계산기</a> · <a href="https://0520goeus.github.io/seller-margin-calc/">셀러 마진 계산기</a> · <a href="https://lifefixnote-kr.blogspot.com/">생활해결 노트</a></p>
</div><div style="margin:14px auto 8px;max-width:960px;display:flex;flex-wrap:wrap;gap:6px;justify-content:center;font-size:12px;"><a href="https://0520goeus.github.io/house-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">부동산·대출·복비</a><a href="https://0520goeus.github.io/car-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">자동차세·유지비</a><a href="https://0520goeus.github.io/money-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">실수령액·금융</a><a href="https://0520goeus.github.io/benefit-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">2026 지원금</a><a href="https://0520goeus.github.io/life-fee-calc/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">평수가전·직구관세</a><a href="https://0520goeus.github.io/elec-calc/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">전기세 계산기</a><a href="https://0520goeus.github.io/vs-pick/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">가성비 VS 124종</a><a href="https://0520goeus.github.io/price-note/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">588 생필품 시세</a><a href="https://0520goeus.github.io/seller-margin-calc/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">셀러마진·엑셀</a><a href="https://0520goeus.github.io/kr-trend-brief/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">실시간 트렌드</a></div>
</footer>
</body></html>"""
    out = DIST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return canon


# 16 Pyeong (평수) tiers for high-ticket appliance sizing (원룸 5평 ~ 대형 48평)
PYEONG_LIST = [
    (5, "원룸·오피스텔"),
    (7, "분리형 원룸"),
    (10, "투룸·소형 빌라"),
    (12, "투룸·오피스텔"),
    (15, "소형 아파트·쓰리룸"),
    (18, "18평형 아파트 (전용 49㎡)"),
    (21, "21평형 아파트"),
    (24, "24~25평형 아파트 (전용 59㎡)"),
    (28, "28평형 아파트"),
    (30, "30평형 아파트"),
    (32, "32~34평형 국민평형 (전용 84㎡)"),
    (36, "36평형 아파트"),
    (40, "40평형 아파트"),
    (45, "45평형 대형 아파트"),
    (50, "50평형 대형 아파트"),
]

# 14 Overseas Direct-Purchase (해외직구) Customs Duty categories
CUSTOMS_ITEMS = [
    ("nutrients", "영양제·비타민 (6병 이하)", 150, 0.08, 0.10, "개인 자가사용 목적 6병 이하까지 면세 한도($150) 적용. 초과 시 관세 8% + 부가세 10% 부과"),
    ("electronics", "가전·전자기기 (청소기·커피머신)", 150, 0.08, 0.10, "1인 1대 전파인증 면제. $150 초과 시 관세 8% + 부가세 10%가 전액에 부과되어 국내 로켓배송과 가격 비교 필수"),
    ("laptop-tablet", "노트북·태블릿·컴퓨터 부품", 150, 0.00, 0.10, "IT 협정 무관세(관세 0%) 품목이나, 면세 한도 초과 시 부가세 10%는 전체 과세가격에 부과"),
    ("clothes", "의류·패션 잡화", 200, 0.13, 0.10, "미국발 목록통관 시 $200까지 면세(타 국가 $150). 한도 초과 시 관세 13% + 부가세 10%"),
    ("shoes", "운동화·신발", 200, 0.13, 0.10, "미국발 $200 / 외 국가 $150 면세. 초과 시 관세 13% + 부가세 10% (총 약 24.3% 세금)"),
    ("perfume", "향수 (60ml~100ml)", 150, 0.065, 0.10, "자가사용 면세 용량 한도 내 $150 이하 면세. 초과 시 관세·개별소비세·부가세 부과"),
    ("cosmetics", "화장품·스킨케어", 150, 0.065, 0.10, "기능성·일반 화장품 $150 이하 면세. 초과 시 관세 6.5% + 부가세 10%"),
    ("golf", "골프채·스포츠 용품", 150, 0.08, 0.10, "관세 8% + 부가세 10% (총 약 18.8%). 고가 클럽은 관부가세 합산 시 국내 정식수입품이 더 저렴한 경우가 많음"),
    ("watch", "손목시계·스마트워치", 150, 0.08, 0.10, "고가 시계는 개별소비세 대상 여부 확인 필수. 일반 시계는 관세 8% + 부가세 10%"),
    ("bag", "가방·백팩·지갑", 150, 0.08, 0.10, "일반 가방 관세 8% + 부가세 10% (총 약 18.8%)"),
    ("audio", "헤드폰·이어폰·스피커", 150, 0.08, 0.10, "블루투스 기기 1인 1대 전파인증 면제, $150 초과 시 관세 8% + 부가세 10%"),
    ("kitchen", "주방용품·냄비·식기", 150, 0.08, 0.10, "식약처 식품검역 유의. $150 초과 시 관세 8% + 부가세 10%"),
    ("camping", "캠핑용품·텐트·침낭", 150, 0.08, 0.10, "부피무게 배송비와 관부가세(18.8%)를 합산하면 쿠팡 로켓배송 국내 재고와 반드시 비교 필요"),
    ("food", "가공식품·커피 캡슐·간식", 150, 0.08, 0.10, "식품류는 목록통관 배제(일반통관 $150 한도). 초과 시 관세 8% + 부가세 10%"),
]


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "style.css").write_text(CSS, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / GOOGLE_FILE).write_text(f"google-site-verification: {GOOGLE_FILE}", encoding="utf-8")
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (DIST / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")

    urls: list[str] = []
    pyeong_tiles: list[str] = []
    customs_tiles: list[str] = []

    # 1. Build 15 Pyeong Appliance Sizing Pages
    for py, label in PYEONG_LIST:
        sqm = round(py * 3.305785, 1)
        # Real Korean appliance sizing rules:
        # Air Purifier: 1.3 ~ 1.5x room area in sqm (living room or whole house)
        ap_sqm = round(sqm * 0.65, 1) if py >= 20 else round(sqm * 1.2, 1)
        # Air Conditioner:リビング = ~py // 2 for apartment 2-in-1 or py for single room
        ac_py = max(6, int(round(py * 0.55))) if py >= 18 else py
        ac_watts = ac_py * 110
        # Dehumidifier: daily liters = ~0.6L per pyeong (living area)
        dehum_l = max(7, min(24, int(round(py * 0.55))))
        # TV size: viewing distance based on pyeong
        tv_inch = 43 if py <= 8 else 55 if py <= 16 else 65 if py <= 26 else 75 if py <= 36 else 85
        # Heater / Humidifier
        hum_ml = max(200, min(800, py * 20))

        rel = f"pyeong/{py}pyeong.html"
        title = f"{py}평({sqm}㎡) 가전 적정 용량 계산표 | 에어컨·공기청정기·제습기·TV 인치 추천"
        desc = f"{py}평({label}, 약 {sqm}㎡) 집의 에어컨 적정 평수({ac_py}평형), 공기청정기 권장 면적({ap_sqm}㎡), 제습기 일일 제습량({dehum_l}L), TV 권장 크기({tv_inch}인치) 계산표."
        faqs = [
            (
                f"{py}평({sqm}㎡) 집에는 공기청정기를 몇 ㎡(몇 평형)로 사야 하나요?",
                f"공기청정기는 실사용 공간의 1.2~1.5배 용량이 정석입니다. {py}평({label}) 기준 거실·메인 공간용으로 최소 {ap_sqm}㎡ 이상(전체 커버 시 {round(sqm*1.2,1)}㎡) 제품을 권장합니다.",
            ),
            (
                f"{py}평 집 에어컨과 제습기 적정 용량은 얼마인가요?",
                f"에어컨은 {ac_py}평형(냉방면적 약 {round(ac_py*3.3,1)}㎡), 제습기는 일일 제습량 {dehum_l}L 이상 제품이 습도 관리와 전기요금 효율이 가장 좋습니다.",
            ),
        ]
        body = f"""
        <section class="card">
          <h1>{py}평({sqm}㎡ · {esc(label)}) 가전제품 적정 용량·크기 기준표</h1>
          <p class="sub">집 크기에 비해 용량이 너무 작으면 모터·압축기가 쉬지 않고 돌아 전기세 폭탄이 나오고, 너무 크면 초기 구매 비용이 낭비됩니다. {py}평({sqm}㎡) 공간에 딱 맞는 가전 스펙 기준선입니다.</p>
          <div class="res-box">
            <div>{py}평 ({sqm}㎡) 핵심 권장 가전 스펙</div>
            <div class="big">에어컨 {ac_py}평형 · 공청기 {ap_sqm}㎡ · 제습기 {dehum_l}L · TV {tv_inch}인치</div>
            <div class="sub">실제 평수({py}평 = {sqm}㎡)와 천장고(2.3~2.4m 표준)를 반영한 권장 규격입니다.</div>
          </div>
        </section>
        {COUPANG_BOX}
        <section class="card">
          <h2>{py}평({sqm}㎡) 가전별 상세 권장 규격 및 구매 체크리스트</h2>
          <table>
            <thead><tr><th>가전 품목</th><th>권장 용량·규격</th><th>선택 이유 및 전기세 절약 팁</th></tr></thead>
            <tbody>
              <tr><td><strong>에어컨</strong></td><td><strong>{ac_py}평형 ({round(ac_py*3.3,1)}㎡)</strong></td><td>인버터 정격 {ac_watts:,}W급 · 목표 온도 도달 후 저전력 유지</td></tr>
              <tr><td><strong>공기청정기</strong></td><td><strong>사용면적 {ap_sqm}㎡ 이상</strong></td><td>실평수 대비 1.2~1.3배 용량이어야 약풍(저소음·저전력)으로 순환 가능</td></tr>
              <tr><td><strong>제습기</strong></td><td><strong>일일 제습량 {dehum_l}L</strong></td><td>물통 용량 최소 {max(2.5, round(dehum_l*0.25,1))}L 이상 · 에너지효율 1등급 권장</td></tr>
              <tr><td><strong>TV·모니터</strong></td><td><strong>{tv_inch}인치 ({int(tv_inch*2.54)}cm)</strong></td><td>시청거리 약 {round(tv_inch*0.038, 1)}m 기준 몰입감 최적 크기</td></tr>
              <tr><td><strong>가습기</strong></td><td><strong>시간당 {hum_ml}ml 이상</strong></td><td>겨울철 실내 습도 45~55% 유지 기준</td></tr>
            </tbody>
          </table>
          <p class="sub" style="margin-top:14px">👉 각 가전의 한 달 전기요금이 궁금하다면: <a href="https://0520goeus.github.io/elec-calc/" style="color:var(--accent)">전기세 얼마 (24종 가전 누진제 계산기)</a> · <a href="https://0520goeus.github.io/vs-pick/" style="color:var(--accent)">가전 1:1 유지비 비교 사전</a></p>
        </section>
        <section class="card">
          <h2>자주 묻는 질문</h2>
          {"".join(f'<div class="faq"><strong>Q. {esc(q)}</strong><p class="sub" style="margin:6px 0 0">A. {esc(a)}</p></div>' for q, a in faqs)}
        </section>
        """
        urls.append(write_page(rel, title, desc, body, faqs))
        pyeong_tiles.append(
            f'<a class="tile" href="{SITE_URL}/{rel}"><b>{py}평 ({sqm}㎡) 가전 용량</b>'
            f'<small>에어컨 {ac_py}평 · 공청기 {ap_sqm}㎡ · 제습기 {dehum_l}L →</small></a>'
        )

    # 2. Build 14 Overseas Customs Duty (해외직구 관부가세) Calculator Pages
    for slug, name, free_usd, duty_rate, vat_rate, note in CUSTOMS_ITEMS:
        ex_usd = 250
        fx = 1400
        krw_base = ex_usd * fx
        duty_krw = int(krw_base * duty_rate)
        vat_krw = int((krw_base + duty_krw) * vat_rate)
        total_tax = duty_krw + vat_krw
        eff_pct = round(total_tax / krw_base * 100, 1)

        rel = f"customs/{slug}.html"
        title = f"{name} 해외직구 관부가세 계산기 | 면세한도 ${free_usd}·세율 {eff_pct}% 자동 계산"
        desc = f"{name} 해외직구 시 면세 한도(${free_usd}) 초과 여부와 관세({duty_rate*100:g}%)·부가세({vat_rate*100:g}%) 합산 예상 세금, 국내 로켓배송 손익분기 가격을 즉시 계산합니다."
        faqs = [
            (
                f"{name} 해외직구 면세 한도는 몇 달러인가요?",
                f"기본 면세 한도는 미화 ${free_usd} 이하입니다. 한도를 1달러라도 초과하면 초과분이 아니라 '물품 가격 + 과세운임 전체 금액'에 대해 약 {eff_pct}%의 관부가세가 부과됩니다.",
            ),
            (
                f"${ex_usd}짜리 {name}을(를) 직구하면 관부가세가 얼마나 나오나요?",
                f"환율 1,400원 기준 물품가 {won(krw_base)}에 대해 관세 약 {won(duty_krw)} + 부가세 약 {won(vat_krw)} = 총 {won(total_tax)}의 세금이 추가되어 총 구매비용이 {won(krw_base + total_tax)}이 됩니다.",
            ),
        ]
        body = f"""
        <section class="card">
          <h1>{esc(name)} 해외직구 관부가세 실시간 계산기</h1>
          <p class="sub">{esc(note)}</p>
          <div class="grid2">
            <div>
              <label>직구 결제 금액 (USD 달러) <input id="usd" type="number" value="{ex_usd}" oninput="calcC()"></label>
              <label>적용 환율 (원/USD) <input id="fx" type="number" value="{fx}" oninput="calcC()"></label>
              <label>현지 배송비/과세운임 (원) <input id="ship" type="number" value="15000" oninput="calcC()"></label>
            </div>
            <div class="res-box">
              <div id="cStatus">관부가세 부과 대상 (${free_usd} 초과)</div>
              <div class="big" id="cTax">{won(total_tax)}</div>
              <div id="cTotal" class="sub">물품+운임+세금 총 실제 비용: {won(krw_base + total_tax + 15000)}</div>
              <div style="font-size:13.5px;color:var(--warn)">💡 국내 로켓배송 가격이 위 '총 실제 비용'과 비슷하거나 더 싸다면 관세·파손 위험 없는 국내 구매가 이득입니다.</div>
            </div>
          </div>
        </section>
        {COUPANG_BOX}
        <section class="card">
          <h2>금액대별 {esc(name)} 예상 관부가세 표 (환율 1,400원 기준)</h2>
          <table>
            <thead><tr><th>직구 물품가 (USD)</th><th>원화 환산</th><th>관세 ({duty_rate*100:g}%)</th><th>부가세 ({vat_rate*100:g}%)</th><th>총 세금 합계</th><th>실제 총비용</th></tr></thead>
            <tbody>
              {"".join(
                  f"<tr><td>${u}</td><td>{won(u*fx)}</td>"
                  + ("<td colspan='3' style='color:var(--accent);text-align:center;font-weight:700'>면세 한도 이내 (세금 0원)</td>" if u <= free_usd else f"<td>{won(u*fx*duty_rate)}</td><td>{won(u*fx*(1+duty_rate)*vat_rate)}</td><td style='color:var(--warn);font-weight:700'>+{won(u*fx*duty_rate + u*fx*(1+duty_rate)*vat_rate)}</td>")
                  + f"<td><strong>{won(u*fx if u<=free_usd else u*fx*(1+duty_rate)*(1+vat_rate))}</strong></td></tr>"
                  for u in (100, 150, 180, 200, 250, 300, 400, 500)
              )}
            </tbody>
          </table>
        </section>
        <section class="card">
          <h2>자주 묻는 질문</h2>
          {"".join(f'<div class="faq"><strong>Q. {esc(q)}</strong><p class="sub" style="margin:6px 0 0">A. {esc(a)}</p></div>' for q, a in faqs)}
        </section>
        <script>
        function calcC(){{
          const u = parseFloat(document.getElementById('usd').value)||0;
          const fx = parseFloat(document.getElementById('fx').value)||1400;
          const sh = parseFloat(document.getElementById('ship').value)||0;
          const base = u * fx + sh;
          if(u <= {free_usd}){{
            document.getElementById('cStatus').textContent = '✅ 면세 한도 이내 (${free_usd} 이하)';
            document.getElementById('cTax').textContent = '0원 (면세)';
            document.getElementById('cTotal').textContent = '총 실제 비용: ' + Math.round(base).toLocaleString('ko-KR') + '원';
          }} else {{
            const d = Math.round(base * {duty_rate});
            const v = Math.round((base + d) * {vat_rate});
            const t = d + v;
            document.getElementById('cStatus').textContent = '⚠️ 관부가세 부과 (${free_usd} 초과 · 실효세율 {eff_pct}%)';
            document.getElementById('cTax').textContent = '+' + t.toLocaleString('ko-KR') + '원';
            document.getElementById('cTotal').textContent = '물품+운임+세금 총 실제 비용: ' + Math.round(base + t).toLocaleString('ko-KR') + '원';
          }}
        }}
        calcC();
        </script>
        """
        urls.append(write_page(rel, title, desc, body, faqs))
        customs_tiles.append(
            f'<a class="tile" href="{SITE_URL}/{rel}"><b>{esc(name)}</b>'
            f'<small>면세 ${free_usd} · 초과 시 세금 +{eff_pct}% →</small></a>'
        )

    # Homepage
    home_body = f"""
    <section class="card">
      <h1>평수별 가전 적정 용량 & 해외직구 관부가세 계산기</h1>
      <p class="sub">에어컨·공기청정기·제습기·TV 구매 전 우리 집 평수(5평~50평)에 딱 맞는 적정 용량과, 해외직구 전 반드시 확인해야 할 품목별 관부가세 손익분기점을 즉시 계산합니다.</p>
    </section>
    {COUPANG_BOX}
    <section class="card" id="pyeong">
      <h2>🏠 우리 집 평수별 가전 적정 용량 계산표 (5평 원룸 ~ 50평 아파트)</h2>
      <div class="grid">{"".join(pyeong_tiles)}</div>
    </section>
    <section class="card" id="customs">
      <h2>✈️ 해외직구 품목별 관부가세 vs 국내 로켓배송 손익분기 계산기</h2>
      <div class="grid">{"".join(customs_tiles)}</div>
    </section>
    """
    urls.insert(0, write_page(
        "index.html",
        f"{SITE_NAME} | 평수별 에어컨·공기청정기·제습기 용량 & 해외직구 관부가세 계산",
        "5평 원룸부터 50평 아파트까지 평수별 가전 적정 용량 계산표와 14개 품목별 해외직구 관부가세 실시간 계산기.",
        home_body,
    ))

    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc><lastmod>{NOW.strftime('%Y-%m-%d')}</lastmod></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"가전용량·직구관세 계산기 빌드 완료: 총 {len(urls)}페이지")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Normalize the supported static locale matrix without rewriting page copy."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
LANGUAGES = (
    ("en", "English"),
    ("zh", "中文"),
    ("es", "Español"),
    ("ko", "한국어"),
    ("ja", "日本語"),
    ("pt", "Português"),
    ("pl", "Polski"),
)
CORE_PAGES = (
    "index.html",
    "about.html",
    "parameters.html",
    "contact.html",
    "compatibility.html",
    "roi.html",
    "payment.html",
    "privacy.html",
    "404.html",
)
SWITCHER_PAGES = {
    "index.html",
    "about.html",
    "parameters.html",
    "contact.html",
    "compatibility.html",
    "roi.html",
    "payment.html",
    "privacy.html",
}
PRETTY_PAGES = {"about.html", "parameters.html", "contact.html"}

GENERIC_PRODUCT_TERMS = {
    "en": "gas mixing equipment",
    "zh": "混合气体设备",
    "es": "equipo de mezcla de gases",
    "ko": "가스 혼합 장비",
    "ja": "ガス混合装置",
    "pt": "equipamento de mistura de gases",
    "pl": "urządzenie do mieszania gazów",
}

LOCALIZED_PRODUCT_BRANDS = {
    "en": ("EUCHIO Mixed Gas", "EUCHIO gas mixing equipment"),
    "zh": ("EUCHIO混合气体设备", "EUCHIO混合气"),
    "es": ("EUCHIO Mixed Gas", "EUCHIO Gas Mixto", "Dispositivo de Gas Mixto EUCHIO"),
    "ko": ("EUCHIO Mixed Gas", "EUCHIO 혼합가스 장비", "EUCHIO 혼합가스 장치", "EUCHIO 혼합 가스 장치", "EUCHIO 혼합 가스"),
    "ja": ("EUCHIO Mixed Gas", "EUCHIO混合ガス装置", "EUCHIO 混合ガス装置"),
    "pt": ("EUCHIO Mixed Gas", "EUCHIO Gás Misto", "dispositivo EUCHIO", "Dispositivo de Gás Misto EUCHIO"),
    "pl": ("EUCHIO Mixed Gas", "EUCHIO Mieszanka gazowa", "Urządzenia do Mieszania Gazów EUCHIO"),
}

LOCALIZED_CONTACT_COPY = {
    "zh": {
        "联系供应团队获取混合气体设备报价和参数。兼容所有主流激光品牌（HANS、DNE、PENTA、LEAD、HSG、BODOR）。全球发货。":
            "联系中国供应团队，提交激光功率、材料、厚度、供气、压力和流量要求，以便进行兼容性评估和报价。",
        "获取混合气体设备报价。兼容所有主流激光品牌。全球发货。":
            "提交机器、材料、厚度和供气条件，获取应用评估、集成沟通和报价。",
    },
    "ja": {
        "ガス混合装置混合ガス装置の見積もりと価格をお問い合わせください。すべての主要レーザーブランド（HANS、DNE、PENTA、LEAD、HSG、BODOR）と互換性があります。世界各国へ出荷可能。":
            "レーザー出力、材料、板厚、ガス供給、圧力、流量を共有し、ガス混合装置の適合性評価と見積もりをご依頼ください。",
        "ガス混合装置混合ガス切断装置の見積もりを依頼してください。すべての主要レーザーブランドと互換性があります。世界各国へ出荷可能。":
            "機械、材料、板厚、ガス供給条件に基づく用途評価、統合相談、見積もりをご依頼ください。",
    },
    "pl": {
        "Skontaktuj się z urządzenie do mieszania gazów w sprawie wyceny urządzenia do mieszania gazów. Kompatybilne ze wszystkimi głównymi markami laserów (HANS, DNE, PENTA, LEAD, HSG, BODOR). Wysyłka globalna.":
            "Prześlij moc lasera, materiał, grubość, zasilanie gazem, ciśnienie i przepływ, aby otrzymać ocenę kompatybilności i wycenę.",
        "Poproś o wycenę urządzenia do cięcia laserowego z mieszaniem gazów urządzenie do mieszania gazów. Kompatybilne ze wszystkimi głównymi markami laserów. Wysyłka globalna.":
            "Poproś o ocenę zastosowania, konsultację integracyjną i wycenę na podstawie warunków maszyny i zasilania gazem.",
    },
}

ABOUT_MISSING_CARDS = {
    "ko": {
        "what": (
            ("지속적인 애프터서비스", "SAGEMRO는 당사가 공급한 장비에 대해 유지보수, 수리 및 운영 지원을 제공합니다."),
            ("책임 있는 조달", "제조 파트너를 신중하게 선정하고 각 제품의 성능과 한계를 솔직하게 안내합니다."),
        ),
        "why": (
            ("24시간당 2kWh", "전력 소모가 매우 낮고 필터, 오일 또는 마모되는 운동 부품을 교체할 필요가 없습니다."),
            ("고객의 레이저 장비와 호환", "HAN'S, DNE, PENTA, LEAD, HSG, BODOR 등 표준 보조 가스 인터페이스를 사용하는 주요 장비와 호환됩니다."),
        ),
    },
    "pt": {
        "what": (
            ("Suporte pós-venda", "A SAGEMRO fornece manutenção, reparo e suporte operacional contínuos para os equipamentos que fornecemos."),
            ("Fornecimento responsável", "Selecionamos cuidadosamente os parceiros de fabricação e comunicamos com clareza o desempenho e os limites de cada produto."),
        ),
        "why": (
            ("Apenas 2 kWh por 24 horas", "Baixíssimo consumo de energia, sem troca de filtros ou óleo e sem peças móveis sujeitas a desgaste."),
            ("Compatível com sua máquina", "Compatível com HAN'S, DNE, PENTA, LEAD, HSG, BODOR e outras máquinas com interface padrão de gás auxiliar."),
        ),
    },
    "pl": {
        "what": (
            ("Wsparcie posprzedażowe", "SAGEMRO zapewnia bieżącą konserwację, naprawy i wsparcie eksploatacyjne dla dostarczanych urządzeń."),
            ("Odpowiedzialne zaopatrzenie", "Starannie wybieramy partnerów produkcyjnych i jasno przedstawiamy możliwości oraz ograniczenia każdego produktu."),
        ),
        "why": (
            ("Tylko 2 kWh na 24 godziny", "Bardzo niskie zużycie energii, bez wymiany filtrów lub oleju i bez zużywających się części ruchomych."),
            ("Kompatybilność z maszyną", "Współpracuje z HAN'S, DNE, PENTA, LEAD, HSG, BODOR oraz innymi maszynami ze standardowym przyłączem gazu pomocniczego."),
        ),
    },
    "it": {
        "what": (
            ("Assistenza post-vendita", "SAGEMRO fornisce manutenzione, riparazione e supporto operativo continuativi per le apparecchiature fornite."),
            ("Approvvigionamento responsabile", "Selezioniamo con cura i partner produttivi e comunichiamo chiaramente prestazioni e limiti di ogni prodotto."),
        ),
        "why": (
            ("Solo 2 kWh ogni 24 ore", "Consumo energetico molto basso, nessuna sostituzione di filtri o olio e nessuna parte mobile soggetta a usura."),
            ("Compatibile con la vostra macchina", "Compatibile con HAN'S, DNE, PENTA, LEAD, HSG, BODOR e altre macchine con interfaccia standard per gas ausiliario."),
        ),
    },
    "nl": {
        "what": (
            ("Ondersteuning na verkoop", "SAGEMRO biedt doorlopend onderhoud, reparatie en operationele ondersteuning voor de door ons geleverde apparatuur."),
            ("Verantwoorde inkoop", "We selecteren productiepartners zorgvuldig en communiceren duidelijk over de prestaties en beperkingen van elk product."),
        ),
        "why": (
            ("Slechts 2 kWh per 24 uur", "Zeer laag energieverbruik, geen filter- of olievervanging en geen bewegende slijtdelen."),
            ("Compatibel met uw machine", "Compatibel met HAN'S, DNE, PENTA, LEAD, HSG, BODOR en andere machines met een standaardaansluiting voor hulpgas."),
        ),
    },
}

RELATED_LABELS = {
    "zh": ("相关链接", "EUCHIO — 整机设备", "SAGEMRO — 零部件与服务", "DHgate 店铺"),
    "es": ("Enlaces relacionados", "EUCHIO — Máquinas completas", "SAGEMRO — Repuestos y servicio", "Tienda DHgate"),
    "ko": ("관련 링크", "EUCHIO — 완성 장비", "SAGEMRO — 부품 및 서비스", "DHgate 스토어"),
    "ja": ("関連リンク", "EUCHIO — 完成機", "SAGEMRO — 部品・サービス", "DHgate ストア"),
    "pt": ("Links relacionados", "EUCHIO — Máquinas completas", "SAGEMRO — Peças e serviço", "Loja DHgate"),
    "pl": ("Powiązane linki", "EUCHIO — Kompletne maszyny", "SAGEMRO — Części i serwis", "Sklep DHgate"),
}

READING_LABELS = {
    "zh": ("深入了解", "相关英文文章", "通过英文资料进一步了解辅助气体技术和切割优化。"),
    "es": ("MÁS INFORMACIÓN", "Artículos relacionados en inglés", "Consulte recursos en inglés sobre gases auxiliares y optimización del corte."),
    "ko": ("더 알아보기", "관련 영문 자료", "보조 가스 기술과 절단 최적화에 대한 영문 자료를 확인하세요."),
    "pt": ("SAIBA MAIS", "Artigos relacionados em inglês", "Consulte recursos em inglês sobre gases auxiliares e otimização de corte."),
    "pl": ("DOWIEDZ SIĘ WIĘCEJ", "Powiązane artykuły w języku angielskim", "Zobacz angielskie materiały o gazach pomocniczych i optymalizacji cięcia."),
}

CONTACT_LABELS = {
    "zh": {
        "website": ("公司网站", "https://www.company.com"),
        "buyer": ("采购方类型 *", ("请选择...", "激光切割终端用户", "自有激光切割的工厂", "激光系统集成商", "项目方 / 采购团队", "其他")),
        "material": ("主要材料", ("请选择材料...", "碳钢", "不锈钢", "铝", "多种材料")),
        "thickness": ("厚度范围", "例如：6-20 mm"),
        "gas": ("当前辅助气体", ("请选择...", "氧气", "氮气", "压缩空气", "已使用混合气", "不确定")),
        "problem": ("主要问题", ("请选择...", "毛刺 / 二次去毛刺", "切割速度慢", "氮气成本高", "切边质量不稳定", "需要提高班次产量")),
    },
    "ko": {
        "website": ("회사 웹사이트", "https://www.company.com"),
        "buyer": ("구매자 유형 *", ("선택하세요...", "최종 사용자 / 레이저 절단 업체", "자체 레이저 절단 공장", "레이저 시스템 인티그레이터", "프로젝트 소유자 / 구매 팀", "기타")),
        "material": ("주요 소재", ("소재를 선택하세요...", "탄소강", "스테인리스강", "알루미늄", "복합 소재")),
        "thickness": ("두께 범위", "예: 6-20 mm"),
        "gas": ("현재 보조 가스", ("선택하세요...", "산소", "질소", "압축 공기", "이미 혼합가스 사용", "확실하지 않음")),
        "problem": ("주요 문제", ("선택하세요...", "버 / 2차 디버링", "느린 절단 속도", "높은 질소 비용", "불안정한 에지 품질", "근무조당 생산량 확대 필요")),
    },
    "ja": {
        "website": ("会社ウェブサイト", "https://www.company.com"),
        "buyer": ("購入者の種類 *", ("選択してください...", "エンドユーザー / レーザー加工会社", "自社内にレーザー加工設備を持つ工場", "レーザーシステムインテグレーター", "プロジェクト所有者 / 調達チーム", "その他")),
        "material": ("主な材料", ("材料を選択...", "炭素鋼", "ステンレス鋼", "アルミニウム", "複数材料")),
        "thickness": ("板厚範囲", "例: 6-20 mm"),
        "gas": ("現在のアシストガス", ("選択してください...", "酸素", "窒素", "圧縮空気", "混合ガスを使用中", "不明")),
        "problem": ("主な課題", ("選択してください...", "バリ / 二次バリ取り", "切断速度が遅い", "窒素コストが高い", "エッジ品質が不安定", "1シフト当たりの生産量を増やしたい")),
    },
    "pl": {
        "website": ("Strona internetowa firmy", "https://www.company.com"),
        "buyer": ("Typ kupującego *", ("Wybierz...", "Użytkownik końcowy / zakład cięcia laserowego", "Fabryka z własnym cięciem laserowym", "Integrator systemów laserowych", "Właściciel projektu / zespół zakupowy", "Inny")),
        "material": ("Główny materiał", ("Wybierz materiał...", "Stal węglowa", "Stal nierdzewna", "Aluminium", "Różne materiały")),
        "thickness": ("Zakres grubości", "np. 6-20 mm"),
        "gas": ("Obecny gaz pomocniczy", ("Wybierz...", "Tlen", "Azot", "Sprężone powietrze", "Już używany gaz mieszany", "Nie wiem")),
        "problem": ("Główny problem", ("Wybierz...", "Zadziory / dodatkowe gratowanie", "Niska prędkość cięcia", "Wysoki koszt azotu", "Niestabilna jakość krawędzi", "Potrzeba większej wydajności na zmianę")),
    },
}

INTERFACE_TRANSLATIONS = {
    "zh": {
        "Best for ≤2mm carbon steel": "最适合 ≤2mm 碳钢",
        "Best for ≤6mm carbon steel": "最适合 ≤6mm 碳钢",
        "Project owner / purchasing team": "项目负责人 / 采购团队",
        "Industrial equipment solutions and service for sheet metal processing": "钣金加工工业设备解决方案与服务",
        "Jinan, Shandong Province, China": "中国山东省济南市",
        "— maintenance, repair, spare parts, technical support": "— 维护、维修、备件与技术支持",
        "下一个区域合作机会正在开放。": "请发送您的切割工况。",
        "重点市场区域合作伙伴名额开放申请。发一集装箱，建立您的市场。": "请提供激光功率、材料厚度和供气方案。我们将在报价前确认混合气是否适用。",
        "成为合作伙伴 →": "申请评估 →",
    },
    "es": {
        "Best for ≤2mm carbon steel": "Ideal para acero al carbono de ≤2 mm",
        "Best for ≤6mm carbon steel": "Ideal para acero al carbono de ≤6 mm",
        "Industrial equipment solutions and service for sheet metal processing": "Soluciones y servicios de equipos industriales para el procesamiento de chapa metálica",
        "Jinan, Shandong Province, China": "Jinan, provincia de Shandong, China",
        "— maintenance, repair, spare parts, technical support": "— mantenimiento, reparación, repuestos y soporte técnico",
        "El Siguiente Territorio Sigue Abierto.": "Envíenos su escenario de corte.",
        "Asociaciones de distribuidor exclusivo disponibles en regiones selectas. Envíe un contenedor, construya su mercado.": "Comparta la potencia del láser, el espesor del material y el plan de suministro de gas. Comprobaremos si el gas mezclado es viable antes de cotizar.",
        "Convertirse en Socio →": "Solicitar evaluación →",
    },
    "ko": {
        "Best for ≤2mm carbon steel": "≤2mm 탄소강에 적합",
        "Best for ≤6mm carbon steel": "≤6mm 탄소강에 적합",
        "Project owner / purchasing team": "프로젝트 책임자 / 구매 팀",
        "다음 시장은 아직 열려 있습니다.": "절단 조건을 보내주세요.",
        "선정 지역 독점 유통사 파트너십 공개. 컨테이너 한 대로 시장 구축.": "레이저 출력, 소재 두께 및 가스 공급 계획을 알려주시면 견적 전에 혼합가스 적용 가능성을 확인합니다.",
        "파트너 신청 →": "적용 평가 요청 →",
    },
    "ja": {
        "Best for ≤2mm carbon steel": "2mm以下の炭素鋼に最適",
        "Best for ≤6mm carbon steel": "6mm以下の炭素鋼に最適",
        "Project owner / purchasing team": "プロジェクト責任者 / 調達チーム",
        "Industrial equipment solutions and service for sheet metal processing": "板金加工向け産業機器ソリューションとサービス",
        "Jinan, Shandong Province, China": "中国山東省済南市",
        "— maintenance, repair, spare parts, technical support": "— 保守、修理、スペアパーツ、技術サポート",
        "次の市場はまだ開いています。": "切断条件をお送りください。",
        "厳選された地域での独占流通パートナーシップ募集。コンテナ1台で市場構築。": "レーザー出力、材料の板厚、ガス供給計画を共有してください。見積前に混合ガスが実用的か確認します。",
        "パートナーになる →": "適用評価を依頼 →",
    },
    "pt": {
        "Best for ≤2mm carbon steel": "Ideal para aço carbono de até 2 mm",
        "Best for ≤6mm carbon steel": "Ideal para aço carbono de até 6 mm",
        "O Próximo Território Ainda Está Aberto.": "Envie-nos o seu cenário de corte.",
        "Parcerias de distribuidor exclusivo disponíveis em regiões selecionadas. Envie um contêiner, construa seu mercado.": "Informe a potência do laser, a espessura do material e o plano de fornecimento de gás. Verificaremos se o gás misto é viável antes da cotação.",
        "Tornar-se Parceiro →": "Solicitar avaliação →",
    },
    "pl": {
        "Project owner / purchasing team": "Właściciel projektu / zespół zakupowy",
        "Następne terytorium jest wciąż otwarte.": "Prześlij parametry procesu cięcia.",
        "Dostępne są ekskluzywne partnerstwa dystrybucyjne w wybranych regionach. Wyślij jeden kontener, zbuduj swój rynek.": "Podaj moc lasera, grubość materiału i plan zasilania gazem. Przed wyceną sprawdzimy, czy gaz mieszany jest praktycznym rozwiązaniem.",
        "Zostań partnerem →": "Poproś o ocenę →",
        "Szukasz dystrybutora?": "Dla projektów użytkowników końcowych",
        "Request Assessment →": "Poproś o ocenę →",
    },
}


def page_path(lang, filename):
    return PUBLIC / filename if lang == "en" else PUBLIC / lang / filename


def page_url(lang, filename):
    prefix = "" if lang == "en" else f"/{lang}"
    if filename == "index.html":
        return f"{prefix}/"
    if filename in PRETTY_PAGES:
        return f"{prefix}/{filename.removesuffix('.html')}"
    return f"{prefix}/{filename}"


def hreflang_block(filename, newline):
    lines = [
        f'  <link rel="alternate" hreflang="{lang}" href="https://gasmixtech.com{page_url(lang, filename)}">'
        for lang, _ in LANGUAGES
    ]
    lines.append(
        f'  <link rel="alternate" hreflang="x-default" href="https://gasmixtech.com{page_url("en", filename)}">'
    )
    return newline.join(lines) + newline


def normalize_hreflangs(content, filename):
    if filename in {"privacy.html", "404.html"}:
        return re.sub(
            r'(?:^[ \t]*<link rel="alternate" hreflang="[^"]+"[^>]*>\r?\n)+',
            "",
            content,
            flags=re.MULTILINE,
        )

    newline = "\r\n" if "\r\n" in content else "\n"
    block = hreflang_block(filename, newline)
    pattern = re.compile(
        r'(?:^[ \t]*<link rel="alternate" hreflang="[^"]+"[^>]*>\r?\n)+',
        re.MULTILINE,
    )
    if pattern.search(content):
        return pattern.sub(block, content, count=1)

    canonical = re.compile(r'(^[ \t]*<link rel="canonical"[^>]*>\r?\n)', re.MULTILINE)
    return canonical.sub(rf"\g<1>{block}", content, count=1)


def normalize_site_branding(content, lang):
    """Use GasMixTech as the site label and generic terms for the product category."""
    generic = GENERIC_PRODUCT_TERMS[lang]
    content = re.sub(
        r"EUCHIO Gas Mixing Technology",
        "GasMixTech — Laser Cutting Gas Mixers",
        content,
        flags=re.IGNORECASE,
    )
    for brand in LOCALIZED_PRODUCT_BRANDS[lang]:
        content = re.sub(re.escape(brand), generic, content, flags=re.IGNORECASE)
    for old, new in LOCALIZED_CONTACT_COPY.get(lang, {}).items():
        content = content.replace(old, new)
    content = re.sub(r"EUCHIO gas mixing equipment", generic, content, flags=re.IGNORECASE)
    if lang == "zh":
        content = content.replace("联系EUCHIO获取混合气体设备", "联系供应团队获取混合气体设备")
        content = content.replace('"name": "联系EUCHIO"', '"name": "联系供应团队"')
        content = content.replace('alt="EUCHIO标志"', 'alt="济南钰峭机械有限公司"')
    content = re.sub(
        r'(<span class="logo-brand">)\s*EUCHIO\s*(</span>)',
        r"\1GasMixTech\2",
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'(<img\b[^>]*\balt=")EUCHIO("[^>]*>)',
        r"\1Jinan Euchio Machinery Co., Ltd.\2",
        content,
        flags=re.IGNORECASE,
    )
    return content


def normalize_polish_homepage_claims(content, lang, filename):
    if (lang, filename) != ("pl", "index.html"):
        return content

    replacements = {
        'content="Urządzenie do mieszania gazów urządzenie do mieszania gazów do maszyn do cięcia laserowego 3KW-60KW. 3x szybsze cięcie, zero zadziorów, ultra-niskie zużycie prądu. Technologia proporcji N2/O2 do cięcia stali węglowej."':
            'content="Informacje o urządzeniach do mieszania azotu i tlenu do cięcia laserowego: kompatybilność, wymagania zasilania gazem, parametry referencyjne i ocena zastosowania."',
        '<title>Urządzenie do mieszania gazów urządzenie do mieszania gazów | 3× szybsze cięcie laserowe</title>':
            '<title>Mieszalnik gazów do cięcia laserowego | Dostawca z Chin</title>',
        'content="Urządzenie do mieszania gazów urządzenie do mieszania gazów | 3× szybsze cięcie laserowe"':
            'content="Mieszalnik gazów do cięcia laserowego | Dostawca z Chin"',
        'content="Urządzenie do mieszania gazów do maszyn do cięcia laserowego 3KW-60KW. 3× szybsze cięcie, zero zadziorów, ultra-niskie zużycie prądu. Technologia proporcji N2/O2."':
            'content="Informacje o mieszaniu azotu i tlenu do cięcia laserowego, w tym kompatybilność, wymagania zasilania gazem i parametry referencyjne."',
        'konfiguracja jeden-do-dwóch, ': '',
        '<div class="hero-badge"><span>13 lat</span> w branży cięcia laserowego metali</div>':
            '<div class="hero-badge"><span>Ocena zastosowania</span> dla laserów włóknowych</div>',
        '<h1>Tnij <span class="accent">3× szybciej</span><br>technologią mieszanki gazowej</h1>':
            '<h1>Mieszalnik gazów do cięcia laserowego</h1>',
        '<p class="hero-subtitle">Urządzenie do mieszania gazów urządzenie do mieszania gazów zapewnia cięcie mikro-tlenowe dla laserów wysokiej mocy (3KW–60KW). Zero zadziorów, mniejsze zużycie gazu i znacznie wyższe prędkości cięcia.</p>':
            '<p class="hero-subtitle">Urządzenie miesza azot i tlen jako kontrolowany gaz pomocniczy. Przed doborem należy sprawdzić moc lasera, materiał, grubość, ciśnienie, przepływ oraz warunki zasilania gazem.</p>',
        '<div class="hero-stat-value">3×</div><div class="hero-stat-label">Szybciej niż O₂</div>':
            '<div class="hero-stat-value">Maszyna</div><div class="hero-stat-label">Ocena kompatybilności</div>',
        '<div class="hero-stat-value">0</div><div class="hero-stat-label">Zadziorów na powierzchni</div>':
            '<div class="hero-stat-value">Gaz</div><div class="hero-stat-label">Ocena ciśnienia i przepływu</div>',
        '<div class="hero-stat-value">2 kWh</div><div class="hero-stat-label">Zużycie prądu / 24h</div>':
            '<div class="hero-stat-value">Proces</div><div class="hero-stat-label">Parametry referencyjne</div>',
        '<p class="price-hint">Inwestycja od <strong>~$18 000</strong> &middot; Typowy zwrot: <strong>6–12 miesięcy</strong> &middot; Jedno urządzenie obsługuje do trzech laserów</p>':
            '<p class="price-hint">Zakres dostawy, konfiguracja i cena są potwierdzane po ocenie warunków zastosowania.</p>',
        '<span class="trust-item"><span class="trust-icon">&#10003;</span> 1,000+ Instalacji</span>':
            '<span class="trust-item"><span class="trust-icon">&#10003;</span> Ocena kompatybilności</span>',
        '<span class="trust-item"><span class="trust-icon">&#10003;</span> Certyfikat CE</span>':
            '<span class="trust-item"><span class="trust-icon">&#10003;</span> Wymagania techniczne</span>',
        '<span class="trust-item"><span class="trust-icon">&#10003;</span> 12-miesięczna gwarancja</span>':
            '<span class="trust-item"><span class="trust-icon">&#10003;</span> Parametry referencyjne</span>',
        '<span class="trust-item"><span class="trust-icon">&#10003;</span> Dostawa 2-4 tygodnie</span>':
            '<span class="trust-item"><span class="trust-icon">&#10003;</span> Koordynacja dostawy</span>',
        'Jedno urządzenie obsługuje dwie maszyny laserowe jednocześnie (konfiguracja Jeden-do-Dwóch).':
            'Wspólne zasilanie kilku maszyn wymaga sprawdzenia łącznego przepływu, spadków ciśnienia, tras rurociągów i sterowania.',
        'Nasze urządzenie do mieszania azotu i tlenu wykorzystuje <strong>technologię cięcia mikro-tlenowego</strong> do wytwarzania precyzyjnie skalibrowanej mieszanki gazowej N₂/O₂ — eliminując zadziory na stali węglowej przy 3× szybszym cięciu niż tradycyjne cięcie tlenem. Zaprojektowane dla laserów wysokiej mocy od 3kW do 60kW.':
            'Urządzenie miesza azot i tlen w kontrolowanej proporcji do zastosowań z gazem pomocniczym. Zakres mocy, materiału i grubości należy potwierdzić razem z ciśnieniem, przepływem, dyszą i kryteriami jakości.',
        'Wysoka prędkość cięcia + zero zadziorów. Po instalacji dostosuj proporcję między N₂ 95% a O₂ 5% dla różnych grubości blach. Wbudowany program analizuje wskaźnik wykorzystania i rejestruje wymagania dotyczące czystości gazu.':
            'Prędkość i stan krawędzi zależą od maszyny, materiału, grubości, dyszy, ciśnienia i proporcji gazu. Parametry należy potwierdzić próbami cięcia.',
        'Współpracuje ze wszystkimi głównymi markami: HAN\'S, DNE, PENTA, LEAD, HSG i innymi. Kompatybilne z BODOR, JIATAI, HG LASER, XUNLEI i innymi globalnymi markami.':
            'Kompatybilność zależy od przyłącza gazu pomocniczego, wymaganego ciśnienia i przepływu oraz sterowania. Każdy model maszyny wymaga osobnej oceny.',
        'Wyeliminuj zadziory przy cięciu laserowym stali węglowej przy praktycznie zerowym koszcie energii elektrycznej. Nasz bezobsługowy system zasilania gazem jest kompatybilny z laserami Han\'s, DNE, PENTA, LEAD, HSG, BODOR i innymi głównymi markami.':
            'Porównaj gaz mieszany z tlenem, azotem i sprężonym powietrzem na podstawie prędkości, stanu krawędzi, zużycia gazu, prac wykończeniowych i lokalnych kosztów eksploatacji.',
        '<div class="advantage-card fade-in"><h3>3× szybsze cięcie</h3><p>Zwiększ prędkość cięcia laserowego do 3 razy w porównaniu z cięciem tlenem. Przykład: stal węglowa 8mm z prędkością 16m/min mieszanką gazową vs tylko 2–3m/min O₂.</p></div>':
            '<div class="advantage-card fade-in"><h3>Ocena przepustowości</h3><p>Porównuj prędkość na podstawie zarejestrowanych warunków procesu. Wynik dla innej maszyny lub materiału wymaga prób cięcia.</p></div>',
        '<div class="advantage-card fade-in"><h3>Eliminacja zadziorów</h3><p>W przeciwieństwie do cięcia azotem, które powoduje zadziory na blachach ≥8mm (12kW) lub ≥10mm (20kW), cięcie mieszanką gazową daje czyste, pozbawione zadziorów powierzchnie na stali węglowej — bez wtórnego szlifowania.</p></div>':
            '<div class="advantage-card fade-in"><h3>Stan krawędzi</h3><p>Oceń zadziory, utlenienie i potrzebę dalszej obróbki według uzgodnionych kryteriów odbioru dla konkretnego detalu.</p></div>',
        '<div class="advantage-card fade-in"><h3>Ultra niski koszt energii</h3><p>Tylko 2 kWh na 24 godziny — praktycznie zerowy koszt energii elektrycznej. Urządzenie do mieszania gazów zaprojektowano z myślą o prędkości i jakości, a nie oszczędności gazu. Zużycie gazu może być podobne lub wyższe w zależności od zastosowania.</p></div>':
            '<div class="advantage-card fade-in"><h3>Koszt eksploatacji</h3><p>Porównaj zużycie gazu i energii razem z czasem cyklu, poprawkami, pracą operatora, konserwacją i lokalnymi cenami mediów.</p></div>',
        '<div class="advantage-card fade-in"><h3>Bezobsługowe</h3><p>Zużycie energii: tylko 2 kWh / 24 godziny. W przeciwieństwie do sprężarek powietrza wymagających wymiany filtrów/oleju co 3.000 godzin, nasze przemysłowe urządzenia gazowe są bezobsługowe.</p></div>':
            '<div class="advantage-card fade-in"><h3>Wymagania serwisowe</h3><p>Zakres przeglądów i obsługi należy potwierdzić w dostarczonej instrukcji i specyfikacji dla wybranej konfiguracji.</p></div>',
        '<div class="advantage-card fade-in"><h3>Konfiguracja Jeden-do-Dwóch</h3><p>Jedyny producent ze stabilnym urządzeniem do mieszania gazów jeden-do-dwóch. Jedna przemysłowa stacja mieszania zasila dwie maszyny laserowe o różnych poziomach mocy jednocześnie.</p></div>':
            '<div class="advantage-card fade-in"><h3>Możliwa konfiguracja jeden-do-trzech</h3><p>Wspólne zasilanie maksymalnie trzech laserów może być ocenione po potwierdzeniu jednoczesnego zapotrzebowania na przepływ, ciśnienia i układu rurociągów.</p></div>',
        '<div class="advantage-card fade-in"><h3>Ochrona soczewek</h3><p>Sprężarki powietrza ryzykują zanieczyszczenie olejem/wodą, które może spalić soczewki głowicy laserowej (strata 5.000–50.000 USD). Nasze czyste źródło ciekłego gazu zapewnia 100% bezpieczeństwo układu optycznego.</p></div>':
            '<div class="advantage-card fade-in"><h3>Jakość zasilania gazem</h3><p>Ryzyko dla układu optycznego zależy od jakości, czystości i filtracji zasilania gazem. Wymagania należy potwierdzić dla konkretnej instalacji.</p></div>',
        '<p class="pain-row-solution">100% bezpieczne — czyste źródło ciekłego gazu</p><p class="pain-row-cost">Zero ryzyka optycznego</p>':
            '<p class="pain-row-solution">Określone źródła azotu i tlenu</p><p class="pain-row-cost">Jakość zasilania wymaga weryfikacji</p>',
        'Konfiguracja z podwójną mocą, jedno urządzenie zasila dwa — bez kompromisów w prędkości':
            'Przykład konfiguracji wielomaszynowej; wydajność wymaga oceny łącznego zapotrzebowania',
        '<tr><td>Prędkość cięcia</td><td class="comparison-win">3× szybsze (np. 16m/min @ 8mm SW)</td><td>2–3m/min @ 8mm SW</td><td>Podobna do mieszanki</td><td>30% wolniejsze niż mieszanka</td></tr>':
            '<tr><td>Prędkość cięcia</td><td class="comparison-win">Zależna od procesu; wymaga prób</td><td>Wartość odniesienia dla danej maszyny</td><td>Zależna od procesu</td><td>Zależna od sprężarki i procesu</td></tr>',
        '<tr><td>Powierzchnia cięcia</td><td class="comparison-win">Gładka, bez zadziorów</td><td>Utleniona, szorstkie krawędzie</td><td>Możliwe zadziory na grubych blachach</td><td>Zanieczyszczona, szorstka</td></tr>':
            '<tr><td>Powierzchnia cięcia</td><td class="comparison-win">Potwierdzić według kryteriów odbioru</td><td>Możliwe utlenienie</td><td>Zależna od grubości i parametrów</td><td>Zależna od jakości powietrza i parametrów</td></tr>',
        '<tr><td>Zużycie gazu</td><td>1/3 mniej niż N₂</td><td>Podobne całkowite</td><td>Wysokie</td><td>Bardzo wysokie (sprężarka)</td></tr>':
            '<tr><td>Zużycie gazu</td><td>Zmierzyć dla konkretnego zadania</td><td>Zmierzyć dla konkretnego zadania</td><td>Zmierzyć dla konkretnego zadania</td><td>Uwzględnić wydajność sprężarki</td></tr>',
        '<tr><td>Koszt energii</td><td class="comparison-win">2 kWh/24h</td><td>Wysoki</td><td>Wysoki</td><td>Bardzo wysoki (sprężarka)</td></tr>':
            '<tr><td>Koszt energii</td><td class="comparison-win">Potwierdzić dane dostarczonej konfiguracji</td><td>Zależny od instalacji</td><td>Zależny od instalacji</td><td>Uwzględnić sprężarkę i osuszanie</td></tr>',
        'Zobacz, ile więcej możesz wyprodukować — i zarobić — przechodząc z O₂ na mieszankę gazową urządzenie do mieszania gazów. Na podstawie rzeczywistych danych dotyczących prędkości cięcia od użytkowników na całym świecie.':
            'Porównaj scenariusz gazu mieszanego z obecnym procesem za pomocą własnych danych. Wyniki są szacunkowe i wymagają potwierdzenia próbami oraz lokalnymi kosztami.',
        'Większość użytkowników wybiera sprężarkę powietrza ze względu na niski koszt początkowy, ale trzy ukryte koszty pożerają Twój zysk.':
            'Przy porównaniu sprężonego powietrza uwzględnij konserwację, stan krawędzi, poprawki, jakość powietrza i ryzyko przestojów.',
        '<p class="pain-row-solution">2 kWh/24h — prawie bezobsługowe</p><p class="pain-row-cost">~73 USD/rok za prąd</p>':
            '<p class="pain-row-solution">Potwierdź moc i wymagania serwisowe</p><p class="pain-row-cost">Oblicz według lokalnych stawek</p>',
        '<p class="pain-row-solution">Srebrno-biała powierzchnia, zero zadziorów</p><p class="pain-row-cost">Gotowe do natychmiastowej dostawy</p>':
            '<p class="pain-row-solution">Docelowy stan krawędzi wymaga prób</p><p class="pain-row-cost">Ocena zależy od kryteriów odbioru</p>',
        '<div class="summary-text"><h4>EUCHIO Mieszanka gazowa: Prawdziwa oszczędność</h4><p>Powietrze wydaje się darmowe, ale Twój prawdziwy koszt to konserwacja, poprawki i wymiana soczewek. Mieszanka gazowa kosztuje mniej w dłuższej perspektywie — i zapewnia doskonałą jakość.</p></div>':
            '<div class="summary-text"><h4>Oceń całkowity koszt eksploatacji</h4><p>Porównaj zużycie gazu, czas cyklu, poprawki, robociznę, wykorzystanie maszyny i konserwację na podstawie własnych danych.</p></div>',
        '<div class="section-header fade-in"><span class="section-label">Dane techniczne</span><h2>Parametry cięcia według mocy</h2><p>Optymalny zakres grubości cięcia stali węglowej dla każdego poziomu mocy lasera. Mieszanka gazowa zapewnia stałe, szybkie cięcie we wszystkich grubościach.</p></div>':
            '<div class="section-header fade-in"><span class="section-label">Dane techniczne</span><h2>Parametry cięcia według mocy</h2><p>Wartości referencyjne wymagają potwierdzenia dla maszyny, materiału, dyszy, ciśnienia, proporcji gazu i kryteriów jakości.</p></div>',
        '<div class="section-header fade-in"><span class="section-label">Rzeczywiste rezultaty</span><h2>Próbki cięcia i filmy testowe</h2><p>Rzeczywiste nagrania cięcia od użytkowników końcowych z całego świata. Bez upiększeń — prawdziwe dane, prawdziwa wydajność.</p></div>':
            '<div class="section-header fade-in"><span class="section-label">Przykłady zarejestrowane</span><h2>Próbki cięcia i filmy testowe</h2><p>Materiały referencyjne do rozmowy technicznej. Wyniki zależą od pełnych warunków procesu i kryteriów odbioru.</p></div>',
        'Grube blachy, zero zadziorów. 10–14 m/min na 10mm, wcześniej osiągalne tylko z O₂':
            'Zarejestrowany przykład grubej blachy; przed porównaniem potwierdź pełne warunki procesu',
        'Aluminium cienkie jak papier, zero przepaleń. Mieszanka gazowa umożliwia to, czego N₂ nie może':
            'Zarejestrowany przykład cienkiego aluminium; wynik należy ocenić według kryteriów odbioru',
        'Od nadmorskich megafabryk po warsztaty w głębi lądu, technologia mieszanki gazowej zasila teraz wycinarki laserowe na wielu kontynentach — a zasięg rośnie z każdym kwartałem.':
            'Obsługujemy rozmowy techniczne i koordynację projektów eksportowych z Chin. Zakres dostawy jest ustalany indywidualnie.',
        'Urządzenie do mieszania gazów precyzyjnie miesza ciekły azot (N₂) i ciekły tlen (O₂) w skalibrowaną mieszankę gazową N₂/O₂ (zazwyczaj 95%/5%). Ta mieszanka mikro-tlenowa jest używana jako gaz pomocniczy w cięciu laserowym wysokiej mocy, zapewniając 3× szybsze cięcie stali węglowej w porównaniu z czystym tlenem, przy całkowitej eliminacji zadziorów.':
            'Urządzenie miesza azot i tlen w kontrolowanej proporcji do wybranych procesów cięcia laserowego. Wynik zależy od maszyny, materiału, grubości, dyszy, ciśnienia, przepływu i ustawień procesu.',
        'Tak. Urządzenie do mieszania gazów urządzenie do mieszania gazów współpracuje ze wszystkimi głównymi markami laserów, w tym HAN\'S, DNE, PENTA, LEAD, HSG, BODOR, JIATAI, HG LASER i XUNLEI. Obsługuje maszyny od 3kW do 60kW. Jeśli Twoja maszyna używa standardowych przyłączy gazu pomocniczego, jest kompatybilna.':
            'Kompatybilność wymaga sprawdzenia modelu maszyny, przyłącza gazu pomocniczego, ciśnienia, przepływu, materiału i zakresu grubości. Prześlij te dane przed wyceną.',
        'Zakres cięcia zależy od mocy lasera: 12kW obsługuje stal węglową do 16mm, 20kW do 25mm, 30kW do 30mm, a 60kW do 40mm. Urządzenie tnie również stal nierdzewną i aluminium z doskonałymi rezultatami.':
            'Zakres grubości zależy od mocy lasera, materiału, dyszy, ciśnienia, przepływu, proporcji gazu i wymagań dotyczących krawędzi. Tabele na stronie mają charakter referencyjny.',
        'Urządzenie do mieszania gazów zaprojektowano z myślą o prędkości i jakości cięcia. Zużywa tylko 2 kWh na 24 godziny — praktycznie zerowy koszt energii. Kluczową wartością są krawędzie bez zadziorów i 3× szybsza prędkość, a nie oszczędność gazu. Zużycie gazu może być podobne lub wyższe w zależności od zastosowania.':
            'Oszczędność należy obliczać na podstawie zużycia gazu, czasu cyklu, poprawek, robocizny, wykorzystania i lokalnych kosztów. Zużycie gazu może być podobne lub wyższe zależnie od zastosowania.',
        'Nie. W przeciwieństwie do sprężarek powietrza, które wymagają wymiany filtrów/oleju co 500–3.000 godzin, urządzenie do mieszania gazów EUCHIO jest bezobsługowe. Wykorzystuje czyste źródła ciekłego gazu bez ruchomych części, które ulegają zużyciu. Zużycie energii wynosi tylko 2 kWh/24h.':
            'Wymagania konserwacyjne zależą od dostarczonej konfiguracji i warunków pracy. Należy stosować harmonogram oraz wymagania jakości gazu określone w instrukcji.',
        'Cięcie powietrzem powoduje utlenione, szorstkie krawędzie i ryzykuje zanieczyszczenie olejem/wodą, które może spalić drogie soczewki głowicy laserowej (5.000–50.000 USD). Mieszanka gazowa zapewnia gładkie, pozbawione zadziorów, srebrno-białe powierzchnie cięcia przy zerowym ryzyku zanieczyszczenia — prędkość cięcia jest o 30% wyższa niż powietrzem.':
            'Porównanie z powietrzem powinno uwzględniać jakość i filtrację powietrza, stan krawędzi, poprawki, przepustowość oraz ryzyko dla układu optycznego w konkretnej instalacji.',
        'Instalacja jest prosta i zazwyczaj kończy się w ciągu jednego dnia. Urządzenie podłącza się do istniejącego źródła ciekłego gazu i maszyny laserowej. Zapewniamy szczegółowe instrukcje instalacji i zdalne wsparcie techniczne dla wszystkich klientów.':
            'Czas i zakres instalacji zależą od źródeł gazu, rurociągów, interfejsu maszyny i prac odbiorowych. Instrukcje i zakres zdalnego wsparcia są potwierdzane w ofercie.',
        'Podłącz jedno urządzenie do swojej maszyny laserowej i zacznij ciąć 3× szybciej już dziś. Dostępne dla maszyn 6KW–60KW.':
            'Prześlij moc lasera, materiał, zakres grubości, obecny gaz i wymagania produkcyjne do wstępnej oceny zastosowania.',
        '<div class="section-header fade-in"><span class="section-label">SIEĆ GLOBALNA</span><h2>Tam gdzie tną lasery wysokiej mocy.<br><span class="gp-accent">Nasz gaz płynie.</span></h2><p>Obsługujemy rozmowy techniczne i koordynację projektów eksportowych z Chin. Zakres dostawy jest ustalany indywidualnie.</p></div>':
            '<div class="section-header fade-in"><span class="section-label">WSPARCIE EKSPORTOWE</span><h2>Wsparcie projektów mieszania gazów z Chin</h2><p>Koordynujemy ocenę zastosowania, pytania integracyjne, wycenę, dostawę i komunikację posprzedażową dla zagranicznych nabywców.</p></div>',
        'Cięcie ultra-grube z prędkością 3,5 m/min. Tam gdzie N₂ nie daje rady, mieszanka gazowa zwycięża':
            'Zarejestrowany przykład grubej blachy; wynik wymaga oceny pełnych warunków procesu i kryteriów odbioru',
        'Gładkie krawędzie aluminium, bez utlenienia. Szybsze niż powietrze, czystsze niż N₂':
            'Zarejestrowany przykład aluminium; stan krawędzi należy ocenić według wymagań części',
        'Precyzyjne cięcie aluminium z mikro-tlenem — prędkość i jakość w jednym przejściu':
            'Zarejestrowany przykład aluminium; parametry i wynik wymagają walidacji dla konkretnego zadania',
        '<div class="presence-stats fade-in"><div class="presence-stat"><div class="stat-num" data-target="20" data-suffix="+">0</div><div class="stat-label">Krajów w przygotowaniu</div></div><div class="presence-stat featured"><div class="stat-num" data-target="4" data-suffix="">0</div><div class="stat-label">Kontynenty wdrożone</div></div><div class="presence-stat"><div class="stat-num" data-target="60" data-prefix="3–" data-suffix="kW">0</div><div class="stat-label">Obsługiwany zakres mocy</div></div><div class="presence-stat"><div class="stat-num static-num">24/7</div><div class="stat-label">Wytrzymałość produkcyjna</div></div></div>':
            '<div class="presence-stats fade-in"><div class="presence-stat"><div class="stat-num static-num">Projekt</div><div class="stat-label">Ocena zastosowania</div></div><div class="presence-stat featured"><div class="stat-num static-num">Eksport</div><div class="stat-label">Koordynacja projektu</div></div><div class="presence-stat"><div class="stat-num static-num">Weryfikacja</div><div class="stat-label">Ocena techniczna</div></div><div class="presence-stat"><div class="stat-num static-num">Zdalnie</div><div class="stat-label">Komunikacja wsparcia</div></div></div>',
        '<summary class="faq-question">Czy jedno urządzenie może obsługiwać dwie maszyny laserowe?</summary><div class="faq-answer"><p>Tak. urządzenie do mieszania gazów jest jedynym producentem oferującym stabilną konfigurację Jeden-do-Dwóch. Jedna stacja mieszania może jednocześnie zasilać dwie maszyny laserowe o różnych poziomach mocy (np. jedną 12kW i jedną 20kW).</p>':
            '<summary class="faq-question">Czy jedno urządzenie może obsługiwać kilka maszyn laserowych?</summary><div class="faq-answer"><p>Możliwa jest ocena konfiguracji maksymalnie jeden-do-trzech. Wymaga to potwierdzenia łącznego i jednoczesnego przepływu, ciśnienia, rurociągów, sterowania oraz interfejsu każdej maszyny.</p>',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    content = re.sub(
        r'(<div class="result-badge euchio-badge"[^>]*>.*?</svg>)EUCHIO(</div>)',
        r'\1MIESZALNIK GAZÓW\2',
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )

    content = re.sub(
        r'<h3>EUCHIO</h3>',
        '<h3>Urządzenie do mieszania gazów</h3>',
        content,
        flags=re.IGNORECASE,
    )
    return content


def normalize_canonical(content, lang, filename):
    if filename == "404.html":
        return content
    canonical = f'https://gasmixtech.com{page_url(lang, filename)}'
    return re.sub(
        r'<link rel="canonical" href="[^"]+">',
        f'<link rel="canonical" href="{canonical}">',
        content,
        count=1,
    )


def language_switcher(lang, filename, indent, newline):
    current = lang.upper()
    inner = indent + "  "
    option_indent = inner + "  "
    options = []
    for code, label in LANGUAGES:
        active = " active" if code == lang else ""
        options.append(
            f'{option_indent}<a href="{page_url(code, filename)}" class="lang-option{active}" data-lang="{code}">{label}</a>'
        )
    return newline.join(
        [
            f'{indent}<div class="lang-switch" id="langSwitch">',
            f'{inner}<button class="lang-btn" id="langBtn" type="button">',
            f'{option_indent}<span class="lang-current">{current}</span>',
            f'{option_indent}<span class="lang-sep">|</span>',
            f'{option_indent}<span class="lang-arrow">▼</span>',
            f'{inner}</button>',
            f'{inner}<div class="lang-dropdown" id="langDropdown">',
            *options,
            f'{inner}</div>',
            f'{indent}</div>',
        ]
    )


def normalize_switcher(content, lang, filename):
    if filename not in SWITCHER_PAGES:
        return content
    newline = "\r\n" if "\r\n" in content else "\n"
    pattern = re.compile(
        r'(?P<indent>^[ \t]*)<div class="lang-switch" id="langSwitch">.*?</div>\s*</div>',
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(content)
    if match:
        replacement = language_switcher(lang, filename, match.group("indent"), newline)
        return content[: match.start()] + replacement + content[match.end() :]

    nav_end = re.search(r'(?P<indent>^[ \t]*)</nav>', content, re.MULTILINE)
    if nav_end is None:
        raise ValueError(f"Navigation not found for {lang}/{filename}")
    indent = nav_end.group("indent") + "  "
    replacement = language_switcher(lang, filename, indent, newline) + newline
    return content[: nav_end.start()] + replacement + content[nav_end.start() :]


def normalize_local_assets(content):
    asset = r'(?:styles(?:\.min)?\.css|script(?:\.min)?\.js|favicon\.svg|images/)'
    content = re.sub(
        rf'(?P<prefix>(?:href|src|srcset|poster)=")\.*?/(?P<asset>{asset})',
        r'\g<prefix>../\g<asset>',
        content,
    )
    content = re.sub(
        rf'(?P<prefix>(?:href|src|srcset|poster)=")/(?P<asset>{asset})',
        r'\g<prefix>../\g<asset>',
        content,
    )
    content = re.sub(
        r'https://gasmixtech\.com/[a-z]{2}/images/',
        'https://gasmixtech.com/images/',
        content,
    )
    return content


def normalize_blog_links(content):
    return re.sub(r'href="/[a-z]{2}/blog(?:/)?"', 'href="/blog/"', content)


def normalize_schema_identity(content):
    """Remove unsupported commerce schema and keep the site/company entities stable."""
    pattern = re.compile(
        r'(?P<open><script\b[^>]*type="application/ld\+json"[^>]*>)'
        r'(?P<body>.*?)'
        r'(?P<close></script>)',
        re.DOTALL | re.IGNORECASE,
    )

    def normalize(match):
        body = match.group("body")
        if re.search(r'"@type"\s*:\s*"(?:Product|Offer|Review|AggregateRating|FAQPage|HowTo)"', body):
            return ""
        if re.search(r'"@type"\s*:\s*"Organization"', body):
            body = re.sub(
                r'("@type"\s*:\s*"Organization"\s*,\s*"name"\s*:\s*)"[^"]+"',
                r'\1"Jinan Euchio Machinery Co., Ltd."',
                body,
                count=1,
            )
        if re.search(r'"@type"\s*:\s*"WebSite"', body):
            body = re.sub(
                r'("@type"\s*:\s*"WebSite"\s*,\s*"name"\s*:\s*)"[^"]+"',
                r'\1"GasMixTech"',
                body,
                count=1,
            )
        return match.group("open") + body + match.group("close")

    content = pattern.sub(normalize, content)
    return re.sub(r'^[ \t]+$', '', content, flags=re.MULTILINE)


def advantage_card(title, description):
    return (
        '<div class="advantage-card fade-in">'
        f"<h3>{title}</h3><p>{description}</p></div>"
    )


def repair_about_cards(content, lang):
    translations = ABOUT_MISSING_CARDS.get(lang)
    if translations is None:
        return content

    for section_id in ("what-we-do", "why-euchio"):
        pattern = re.compile(
            rf'(?P<open><section[^>]*id="{section_id}"[^>]*>.*?<div class="advantage-grid"[^>]*>)'
            r'(?P<cards>.*?)'
            r'(?P<close></div></div></section>)',
            re.DOTALL,
        )
        match = pattern.search(content)
        if match is None:
            raise ValueError(f"{lang}/about.html: {section_id} grid not found")
        cards = re.findall(r'<div class="advantage-card fade-in">.*?</div>', match.group("cards"), re.DOTALL)
        if len(cards) == 6:
            continue
        if len(cards) != 4:
            raise ValueError(f"{lang}/about.html: expected 4 or 6 cards in {section_id}, got {len(cards)}")

        added = [advantage_card(*card) for card in translations["what" if section_id == "what-we-do" else "why"]]
        ordered = cards + added if section_id == "what-we-do" else cards[:3] + added + cards[3:]
        replacement = match.group("open") + "".join(ordered) + match.group("close")
        content = content[: match.start()] + replacement + content[match.end() :]
    return content


def repair_polish_homepage(content):
    content = re.sub(
        r'\s*<!-- Case Studies -->.*?(?=\s*<!-- CTA Section -->)',
        "\n\n",
        content,
        count=1,
        flags=re.DOTALL,
    )
    if '<span class="params-power">3KW</span>' in content:
        return content

    cards = """
        <div class="params-card fade-in"><h3><span class="params-power">3KW</span> Maszyna laserowa</h3><table class="params-table"><tr><th>Grubość</th><th>Prędkość gazu mieszanego</th></tr><tr><td>1mm</td><td>28–35 m/min</td></tr><tr><td>2mm</td><td>16–20 m/min</td></tr></table><p class="params-note">Najlepsza dla stali węglowej ≤2mm</p></div>
        <div class="params-card fade-in"><h3><span class="params-power">6KW</span> Maszyna laserowa</h3><table class="params-table"><tr><th>Grubość</th><th>Prędkość gazu mieszanego</th></tr><tr><td>1mm</td><td>35–45 m/min</td></tr><tr><td>2mm</td><td>20–25 m/min</td></tr><tr><td>3mm</td><td>12–14 m/min</td></tr><tr><td>4mm</td><td>8–10 m/min</td></tr><tr><td>5mm</td><td>6–7 m/min</td></tr><tr><td>6mm</td><td>5–6 m/min</td></tr></table><p class="params-note">Najlepsza dla stali węglowej ≤6mm</p></div>
"""
    return content.replace('<div class="params-grid">', '<div class="params-grid">' + cards, 1)


def repair_parameters_reading(content, lang):
    if 'class="blog-post-card' in content:
        return content
    english = (PUBLIC / "parameters.html").read_text(encoding="utf-8")
    match = re.search(
        r'\s*<!-- Further Reading -->\s*(<section class="section section-alt".*?</section>)',
        english,
        re.DOTALL,
    )
    if match is None:
        raise ValueError("English parameters Further Reading section not found")
    section = match.group(1)
    label, title, description = READING_LABELS[lang]
    section = section.replace("LEARN MORE", label, 1)
    section = section.replace("Related Articles", title, 1)
    section = section.replace(
        "Deepen your understanding of assist gas technology and cutting optimization.",
        description,
        1,
    )
    marker = "  <!-- Footer -->"
    if marker not in content:
        raise ValueError(f"{lang}/parameters.html: footer marker not found")
    return content.replace(marker, f"\n\n  <!-- Further Reading -->\n  {section}\n\n{marker}", 1)


def select_options(values, option_values):
    return "".join(f'<option value="{value}">{label}</option>' for value, label in zip(option_values, values))


def repair_contact_fields(content, lang):
    if 'name="website"' in content:
        return content
    labels = CONTACT_LABELS[lang]
    buyer_values = ("", "end_user", "factory", "integrator", "project_owner", "other")
    material_values = ("", "carbon_steel", "stainless_steel", "aluminum", "mixed")
    gas_values = ("", "oxygen", "nitrogen", "air", "mixed", "unknown")
    problem_values = ("", "burr", "slow_speed", "gas_cost", "edge_quality", "capacity")
    first = f"""
            <div class="form-group">
              <label for="website">{labels['website'][0]}</label>
              <input type="url" id="website" name="website" placeholder="{labels['website'][1]}">
            </div>

            <div class="form-group">
              <label for="buyer_type">{labels['buyer'][0]}</label>
              <select id="buyer_type" name="buyer_type" required>{select_options(labels['buyer'][1], buyer_values)}</select>
            </div>

"""
    inquiry = re.search(r'(?P<start>[ \t]*<div class="form-group">\s*<label for="inquiry">)', content)
    if inquiry is None:
        raise ValueError(f"{lang}/contact.html: inquiry field not found")
    content = content[: inquiry.start()] + first + content[inquiry.start() :]

    second = f"""
            <div class="form-row">
              <div class="form-group"><label for="material">{labels['material'][0]}</label><select id="material" name="material">{select_options(labels['material'][1], material_values)}</select></div>
              <div class="form-group"><label for="thickness">{labels['thickness'][0]}</label><input type="text" id="thickness" name="thickness" placeholder="{labels['thickness'][1]}"></div>
            </div>

            <div class="form-row">
              <div class="form-group"><label for="current_gas">{labels['gas'][0]}</label><select id="current_gas" name="current_gas">{select_options(labels['gas'][1], gas_values)}</select></div>
              <div class="form-group"><label for="main_problem">{labels['problem'][0]}</label><select id="main_problem" name="main_problem">{select_options(labels['problem'][1], problem_values)}</select></div>
            </div>

"""
    message = re.search(r'(?P<start>[ \t]*<div class="form-group">\s*<label for="message">)', content)
    if message is None:
        raise ValueError(f"{lang}/contact.html: message field not found")
    return content[: message.start()] + second + content[message.start() :]


def repair_footer_group(content, lang):
    footer = re.search(r'<footer class="footer">.*?</footer>', content, re.DOTALL)
    if footer is None or footer.group(0).count('class="footer-links"') >= 3:
        return content
    labels = RELATED_LABELS[lang]
    group = f"""
        <div>
          <h4 class="footer-subtitle">{labels[0]}</h4>
          <ul class="footer-links">
            <li><a href="https://www.euchio.com" target="_blank" rel="noopener">{labels[1]}</a></li>
            <li><a href="https://www.sagemro.com" target="_blank" rel="noopener">{labels[2]}</a></li>
            <li><a href="https://www.dhgate.com/store/22325464" target="_blank" rel="noopener">{labels[3]}</a></li>
          </ul>
        </div>"""
    repaired = re.sub(
        r'(</div>)(\s*<div class="footer-bottom">)',
        rf'\1{group}\2',
        footer.group(0),
        count=1,
    )
    if repaired == footer.group(0):
        raise ValueError(f"{lang}: footer insertion point not found")
    return content[: footer.start()] + repaired + content[footer.end() :]


def repair_visible_structure(content, lang, filename):
    if lang == "pl" and filename == "index.html":
        content = repair_polish_homepage(content)
    if filename == "about.html":
        content = repair_about_cards(content, lang)
    if filename == "parameters.html" and lang in READING_LABELS:
        content = repair_parameters_reading(content, lang)
    if filename == "contact.html" and lang in CONTACT_LABELS:
        content = repair_contact_fields(content, lang)
    if lang in RELATED_LABELS and filename in {"index.html", "parameters.html", "contact.html"}:
        content = repair_footer_group(content, lang)
    return content


def repair_interface_translations(content, lang):
    for english, localized in INTERFACE_TRANSLATIONS.get(lang, {}).items():
        content = content.replace(english, localized)
    return content


def repair_polish_contact_encoding(content, lang, filename):
    if (lang, filename) != ("pl", "contact.html"):
        return content

    mojibake_marker = re.compile(r"[\u3400-\u9fff\ue000-\uf8ff]")

    def reverse_token(match):
        token = match.group(0)
        if mojibake_marker.search(token) is None:
            return token
        try:
            return token.encode("gb18030").decode("utf-8")
        except UnicodeError:
            return token

    content = re.sub(r"\S+", reverse_token, content)
    return content.replace("鈫?/button>", "→</button>")


def normalize_core_page(path, lang, filename):
    content = path.read_text(encoding="utf-8")
    original = content
    content = normalize_canonical(content, lang, filename)
    content = normalize_hreflangs(content, filename)
    content = normalize_switcher(content, lang, filename)
    content = normalize_blog_links(content)
    content = normalize_schema_identity(content)
    content = normalize_site_branding(content, lang)
    content = normalize_polish_homepage_claims(content, lang, filename)
    if lang != "en":
        content = repair_polish_contact_encoding(content, lang, filename)
        content = repair_interface_translations(content, lang)
        content = normalize_local_assets(content)
        content = repair_visible_structure(content, lang, filename)
    if content != original:
        path.write_text(content, encoding="utf-8", newline="")


def normalize_english_content_page(path):
    content = path.read_text(encoding="utf-8")
    original = content
    content = re.sub(
        r'(?:^[ \t]*<link rel="alternate" hreflang="[^"]+"[^>]*>\r?\n)+',
        "",
        content,
        flags=re.MULTILINE,
    )
    content = normalize_blog_links(content)
    content = normalize_site_branding(content, "en")
    if 'class="lang-switch"' in content:
        content = normalize_switcher(content, "en", "index.html")
    if content != original:
        path.write_text(content, encoding="utf-8", newline="")


def main():
    for lang, _ in LANGUAGES:
        for filename in CORE_PAGES:
            normalize_core_page(page_path(lang, filename), lang, filename)

    template = PUBLIC / "_template.html"
    normalize_core_page(template, "en", "index.html")

    for folder in (PUBLIC / "blog", PUBLIC / "case-studies"):
        for path in folder.glob("*.html"):
            normalize_english_content_page(path)


if __name__ == "__main__":
    main()

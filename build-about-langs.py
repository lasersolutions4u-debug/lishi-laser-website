#!/usr/bin/env python3
"""
Generate multilingual about.html pages from English source.
Applies structural changes (paths, canonical, hreflang, nav) and full content translations.
"""
import os, re, json
from about_locales import COPY as COMPACT_COPY, render_main

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
SOURCE = os.path.join(BASE, 'about.html')

LANGS = ['zh', 'es', 'ko', 'ja', 'pt', 'tr', 'pl', 'it', 'de', 'fr', 'nl', 'ru', 'vi', 'th']

ABOUT_IMAGE_ALTS = {
    'zh': ['混合气体设备在中国佛山40kW激光切割客户工厂的应用', '配备混合气体设备和绿色储气罐的40kW激光切割客户工厂', '配备混合气体设备的60kW超高功率激光切割客户工厂', '配备混合气体设备的20kW大族激光客户工厂'],
    'es': ['Dispositivo de gas mixto en una fábrica cliente de corte láser de 40kW en Foshan', 'Fábrica cliente de corte láser de 40kW con dispositivo de gas mixto y tanques verdes', 'Fábrica cliente de corte láser de 60kW con dispositivo de gas mixto', 'Fábrica cliente con láser HAN\'S de 20kW y dispositivo de gas mixto'],
    'ja': ['中国佛山の40kWレーザー切断顧客工場に導入された混合ガス装置', '混合ガス装置と緑色ガスタンクを備えた40kWレーザー切断顧客工場', '混合ガス装置を備えた60kW超高出力レーザー顧客工場', '混合ガス装置を備えた20kW HAN\'Sレーザー顧客工場'],
    'de': ['Mischgasgerät in einer 40kW-Laserschneidfabrik eines Kunden in Foshan', '40kW-Laserschneidfabrik eines Kunden mit Mischgasgerät und grünen Gastanks', '60kW-Hochleistungs-Laserschneidfabrik eines Kunden mit Mischgasgerät', 'Kundenfabrik mit 20kW-HAN\'S-Laser und Mischgasgerät'],
    'fr': ['Dispositif de gaz mixte dans une usine cliente de découpe laser 40kW à Foshan', 'Usine cliente de découpe laser 40kW avec dispositif de gaz mixte et réservoirs verts', 'Usine cliente de découpe laser 60kW avec dispositif de gaz mixte', 'Usine cliente équipée d\'un laser HAN\'S 20kW et d\'un dispositif de gaz mixte'],
    'ru': ['Устройство смешанного газа на заводе клиента с лазером 40 кВт в Фошане', 'Завод клиента с лазером 40 кВт, устройством смешанного газа и зелёными резервуарами', 'Завод клиента с лазером 60 кВт и устройством смешанного газа', 'Завод клиента с лазером HAN\'S 20 кВт и устройством смешанного газа'],
}

ENGLISH_ABOUT_IMAGE_ALTS = [
    'Gas mixing device deployed at a 40kW laser cutting factory in Foshan, China',
    '40kW laser cutting factory with mixed gas device — Hymson laser machine with green gas storage tanks',
    '60kW laser cutting factory with mixed gas device — ultra-high-power laser installation',
    "20kW Han's laser factory with mixed gas device",
]

# Language code display in the switcher button
LANG_CODE_DISPLAY = {
    'zh': '中文', 'es': 'ES', 'ko': 'KO', 'ja': 'JA', 'pt': 'PT',
    'tr': 'TR', 'pl': 'PL', 'it': 'IT', 'de': 'DE', 'fr': 'FR',
    'nl': 'NL', 'ru': 'RU', 'vi': 'VI', 'th': 'TH',
}

# Nav and UI translations (kept from original, plus new keys)
UI_TRANSLATIONS = {
    'zh': {
        'About': '关于我们', 'Home': '首页', 'How It Works': '工作原理', 'Parameters': '参数',
        'Samples': '样品', 'Blog': '博客', 'Contact': '联系', 'Get Assessment': '获取评估',
        'About Us': '关于我们', 'Advantages': '优势',
        'Cutting Samples': '切割样品', 'FAQ': '常见问题',
        'Get a Quote →': '获取报价 →', 'View Parameters': '查看参数',
    },
    'es': {
        'About': 'Acerca de', 'Home': 'Inicio', 'How It Works': 'Cómo Funciona', 'Parameters': 'Parámetros',
        'Samples': 'Muestras', 'Blog': 'Blog', 'Contact': 'Contacto', 'Get Assessment': 'Solicitar Evaluación',
        'About Us': 'Sobre Nosotros', 'Advantages': 'Ventajas',
        'Cutting Samples': 'Muestras de Corte', 'FAQ': 'Preguntas Frecuentes',
        'Get a Quote →': 'Solicitar Cotización →', 'View Parameters': 'Ver Parámetros',
    },
    'ko': {
        'About': '소개', 'Home': '홈', 'How It Works': '작동 원리', 'Parameters': '매개변수',
        'Samples': '샘플', 'Blog': '블로그', 'Contact': '문의', 'Get Assessment': '평가 받기',
        'About Us': '회사 소개', 'Advantages': '장점',
        'Cutting Samples': '절단 샘플', 'FAQ': '자주 묻는 질문',
        'Get a Quote →': '견적 요청 →', 'View Parameters': '매개변수 보기',
    },
    'ja': {
        'About': '会社概要', 'Home': 'ホーム', 'How It Works': '原理', 'Parameters': 'パラメータ',
        'Samples': 'サンプル', 'Blog': 'ブログ', 'Contact': 'お問い合わせ', 'Get Assessment': '評価依頼',
        'About Us': '会社概要', 'Advantages': 'メリット',
        'Cutting Samples': '切断サンプル', 'FAQ': 'よくある質問',
        'Get a Quote →': '見積もり依頼 →', 'View Parameters': 'パラメータを見る',
    },
    'pt': {
        'About': 'Sobre', 'Home': 'Início', 'How It Works': 'Como Funciona', 'Parameters': 'Parâmetros',
        'Samples': 'Amostras', 'Blog': 'Blog', 'Contact': 'Contato', 'Get Assessment': 'Solicitar Avaliação',
        'About Us': 'Sobre Nós', 'Advantages': 'Vantagens',
        'Cutting Samples': 'Amostras de Corte', 'FAQ': 'Perguntas Frequentes',
        'Get a Quote →': 'Solicitar Orçamento →', 'View Parameters': 'Ver Parâmetros',
    },
    'tr': {
        'About': 'Hakkımızda', 'Home': 'Ana Sayfa', 'How It Works': 'Çalışma Prensibi', 'Parameters': 'Parametreler',
        'Samples': 'Numuneler', 'Blog': 'Blog', 'Contact': 'İletişim', 'Get Assessment': 'Değerlendirme İste',
        'About Us': 'Hakkımızda', 'Advantages': 'Avantajlar',
        'Cutting Samples': 'Kesim Numuneleri', 'FAQ': 'SSS',
        'Get a Quote →': 'Teklif Al →', 'View Parameters': 'Parametreleri Gör',
    },
    'pl': {
        'About': 'O nas', 'Home': 'Strona główna', 'How It Works': 'Zasada działania', 'Parameters': 'Parametry',
        'Samples': 'Próbki', 'Blog': 'Blog', 'Contact': 'Kontakt', 'Get Assessment': 'Poproś o ocenę',
        'About Us': 'O nas', 'Advantages': 'Zalety',
        'Cutting Samples': 'Próbki cięcia', 'FAQ': 'FAQ',
        'Get a Quote →': 'Poproś o wycenę →', 'View Parameters': 'Zobacz parametry',
    },
    'it': {
        'About': 'Chi siamo', 'Home': 'Home', 'How It Works': 'Principio', 'Parameters': 'Parametri',
        'Samples': 'Campioni', 'Blog': 'Blog', 'Contact': 'Contatto', 'Get Assessment': 'Richiedi valutazione',
        'About Us': 'Chi siamo', 'Advantages': 'Vantaggi',
        'Cutting Samples': 'Campioni di taglio', 'FAQ': 'FAQ',
        'Get a Quote →': 'Richiedi preventivo →', 'View Parameters': 'Vedi parametri',
    },
    'de': {
        'About': 'Über uns', 'Home': 'Startseite', 'How It Works': 'Funktionsweise', 'Parameters': 'Parameter',
        'Samples': 'Proben', 'Blog': 'Blog', 'Contact': 'Kontakt', 'Get Assessment': 'Bewertung anfordern',
        'About Us': 'Über uns', 'Advantages': 'Vorteile',
        'Cutting Samples': 'Schnittproben', 'FAQ': 'FAQ',
        'Get a Quote →': 'Angebot anfordern →', 'View Parameters': 'Parameter ansehen',
    },
    'fr': {
        'About': 'À propos', 'Home': 'Accueil', 'How It Works': 'Principe', 'Parameters': 'Paramètres',
        'Samples': 'Échantillons', 'Blog': 'Blog', 'Contact': 'Contact', 'Get Assessment': 'Demander une évaluation',
        'About Us': 'À propos de nous', 'Advantages': 'Avantages',
        'Cutting Samples': 'Échantillons de coupe', 'FAQ': 'FAQ',
        'Get a Quote →': 'Demander un devis →', 'View Parameters': 'Voir les paramètres',
    },
    'nl': {
        'About': 'Over ons', 'Home': 'Home', 'How It Works': 'Werking', 'Parameters': 'Parameters',
        'Samples': 'Monsters', 'Blog': 'Blog', 'Contact': 'Contact', 'Get Assessment': 'Beoordeling aanvragen',
        'About Us': 'Over ons', 'Advantages': 'Voordelen',
        'Cutting Samples': 'Snijmonsters', 'FAQ': 'FAQ',
        'Get a Quote →': 'Offerte aanvragen →', 'View Parameters': 'Parameters bekijken',
    },
    'ru': {
        'About': 'О нас', 'Home': 'Главная', 'How It Works': 'Принцип работы', 'Parameters': 'Параметры',
        'Samples': 'Образцы', 'Blog': 'Блог', 'Contact': 'Контакт', 'Get Assessment': 'Запросить оценку',
        'About Us': 'О нас', 'Advantages': 'Преимущества',
        'Cutting Samples': 'Образцы реза', 'FAQ': 'Часто задаваемые вопросы',
        'Get a Quote →': 'Запросить расчёт →', 'View Parameters': 'Смотреть параметры',
    },
    'vi': {
        'About': 'Giới thiệu', 'Home': 'Trang chủ', 'How It Works': 'Nguyên lý', 'Parameters': 'Thông số',
        'Samples': 'Mẫu', 'Blog': 'Blog', 'Contact': 'Liên hệ', 'Get Assessment': 'Yêu cầu đánh giá',
        'About Us': 'Giới thiệu', 'Advantages': 'Ưu điểm',
        'Cutting Samples': 'Mẫu cắt', 'FAQ': 'Câu hỏi thường gặp',
        'Get a Quote →': 'Nhận báo giá →', 'View Parameters': 'Xem thông số',
    },
    'th': {
        'About': 'เกี่ยวกับ', 'Home': 'หน้าแรก', 'How It Works': 'หลักการ', 'Parameters': 'พารามิเตอร์',
        'Samples': 'ตัวอย่าง', 'Blog': 'บล็อก', 'Contact': 'ติดต่อ', 'Get Assessment': 'ขอประเมิน',
        'About Us': 'เกี่ยวกับเรา', 'Advantages': 'ข้อดี',
        'Cutting Samples': 'ตัวอย่างการตัด', 'FAQ': 'คำถามที่พบบ่อย',
        'Get a Quote →': 'ขอใบเสนอราคา →', 'View Parameters': 'ดูพารามิเตอร์',
    },
}

# Full body content translations for each language
# Keys map to specific text blocks in about.html
BODY_TRANSLATIONS = {
    'zh': {
        'page_title': '关于我们 | Euchio Machinery — 钣金设备与服务',
        'meta_description': '关于 Euchio Machinery — 一家专注于钣金加工设备的中国机械贸易与服务公司。运营 EUCHIO（整机）和 SAGEMRO（MRO零部件及服务）品牌，服务海外工业客户。',
        'hero_badge': '<span>钣金设备</span>与服务',
        'hero_h1': '为钣金加工企业<br>提供<span class="accent">实用的设备方案</span>',
        'hero_subtitle': '济南钰峭机械有限公司是一家专注于钣金加工设备的中国机械贸易与服务公司。我们运营两个品牌 — <strong>EUCHIO</strong>（整机）和 <strong>SAGEMRO</strong>（MRO零部件及服务）— 以清晰的沟通、负责任的采购和长期的支持服务海外工业客户。',
        'btn_contact_us': '联系我们',
        'label_company': '我们的公司',
        'h2_who_we_are': '我们是谁',
        'wwa_p1': '济南钰峭机械有限公司是一家专注于钣金加工设备及相关工业解决方案的中国机械贸易与服务公司。我们与中国的制造商合作，将他们的设备与海外工业客户对接。',
        'wwa_p2': '公司运营两个品牌：<strong>EUCHIO</strong> — 可在自有品牌下供应的整机设备；<strong>SAGEMRO</strong> — MRO产品和服务，包括维护、维修、备件和外围设备。不允许贴牌的产品，或来自不允许品牌重塑的制造商的产品，通过 SAGEMRO 或我们的在线商店提供。',
        'wwa_p3': '我们的目标很明确：为海外工业客户提供实用、匹配的设备和服务方案，以清晰的沟通和长期的支持。我们专注于诚实面对我们能做什么和不能做什么 — 如果产品不合适，我们会直说。',
        'tl1_title': '产品开发',
        'tl1_desc': '发现激光切割客户中反复出现的辅助气体问题。开发了覆盖 3kW 至 60kW 光纤激光器的混合气体调节装置。首批设备已在客户现场部署测试。',
        'tl2_title': '现场验证',
        'tl2_desc': '上线 gasmixtech.com 记录设备功能并分享现场测试结果。已收集 12kW、20kW、30kW、40kW 和 60kW 客户部署的验证切割数据。',
        'tl3_title': '全球拓展',
        'tl3_desc': '多语言网站上线（15种语言）。持续从新客户现场添加验证数据。通过敦煌网在线商店和直接联系支持销售。',
        'label_brands': '我们的品牌',
        'h2_brands': '两个品牌，一个使命',
        'brands_subtitle': '我们运营两个品牌，覆盖不同的设备和服务需求 — 清晰分开，让客户始终知道自己得到的是什么。',
        'euchio_title': 'EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— 整机设备</span>',
        'euchio_desc': 'EUCHIO 是我们的自有品牌整机品牌，包括激光切割机、剪板机、切管机、折弯机和其他钣金加工设备。适用于在自有品牌下供应整机设备的场景。',
        'sagemro_title': 'SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— MRO零部件及服务</span>',
        'sagemro_desc': 'SAGEMRO 专注于MRO相关产品和服务 — 维护、维修、运行支持、备件、易损件、设备升级、改造方案和外围设备，适用于激光切割、焊接、折弯和其他金属加工应用。不适合贴牌的产品也通过 SAGEMRO 提供。',
        'gas_fit_q': '<strong style="color: var(--color-text);">混合气体装置属于哪个品牌？</strong>',
        'gas_fit_a': '混合气体装置是专有产品，不接受贴牌。它在 SAGEMRO 品牌下供应。售后服务、维护和技术支持请访问 <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a>。',
        'label_what_we_do': '我们的业务',
        'h2_what_we_do': '设备、零部件与服务 — 做到位',
        'card1_title': '整机设备',
        'card1_desc': '通过 EUCHIO 品牌，我们在自有品牌下供应激光切割机、折弯机、切管机和剪板机 — 面向需要交钥匙设备方案的客户。',
        'card2_title': 'MRO零部件及服务',
        'card2_desc': '通过 SAGEMRO，我们提供备件、易损件、设备升级、改造方案和外围设备，适用于激光切割、焊接、折弯和其他金属加工应用。',
        'card3_title': '混气技术',
        'card3_desc': '我们的专有氮氧混合气体装置（3kW–60kW）在 SAGEMRO 品牌下供应。一台设备可同时供应最多三台激光切割机，切割速度提升3倍，无毛刺，氮气消耗减少33%。',
        'card4_title': '技术咨询',
        'card4_desc': '在推荐方案之前，我们评估您的激光功率、材料厚度和气体供应配置。如果混合气体不适合您的应用，我们会告诉您。',
        'card5_title': '售后支持',
        'card5_desc': 'SAGEMRO 为我们供应的所有设备提供持续的维护、维修和运行支持。长期支持不是附加服务 — 它是我们工作方式的一部分。',
        'card6_title': '负责任采购',
        'card6_desc': '我们谨慎选择制造合作伙伴，并诚实沟通每个产品能做什么和不能做什么。不夸大参数，不做虚假承诺。',
        'label_deployments': '实际部署',
        'h2_deployments': '不是产品图册照片。是真实客户工厂。',
        'deployments_subtitle': '这些是来自客户生产现场的真实照片 — 20kW、40kW 和 60kW 激光设备使用混合气体运行。',
        'dep40_title': '<span class="params-power">40kW</span> 部署',
        'dep40_desc': '中国佛山 — 海目星 40kW 光纤激光器配混合气体。切割碳钢至35mm。右侧可见绿色液态气体储罐。',
        'dep60_title': '<span class="params-power">60kW</span> 部署',
        'dep60_desc': '中国佛山 — 60kW 光纤激光器用混合气体切割厚碳钢（30–50mm）。无毛刺边缘，无需切割后打磨。',
        'dep20_title': '<span class="params-power">20kW</span> 部署',
        'dep20_desc': '大族激光 20kW 设备配混合气体 — 切割碳钢至25mm，速度比纯氧快2.5–7倍。',
        'want_more': '想看更多？观看来自真实客户工厂的切割视频：',
        'btn_view_samples': '查看切割样品 →',
        'label_global': '真实生产验证',
        'deployment_metric': '中国国内安装量',
        'h2_global': '经过真实工厂使用验证',
        'global_note': '中国国内已有超过1,000台EUCHIO混气装置安装在激光切割工厂。真实生产环境中的长期使用验证了设备运行稳定、性能可靠。',
        'label_why': '为什么选择我们',
        'h2_why': '诚实面对我们是什么 — 以及不是什么',
        'why1_title': '不合适我们会告诉你',
        'why1_desc': '在报价之前，我们检查混合气体是否适合您的激光功率、材料和气体供应。如果不适合，我们会直说。我们宁愿失去一笔生意，也不愿发出错误的方案。',
        'why2_title': '真实数据，不是营销数字',
        'why2_desc': '我们的参数表区分已验证的现场数据和估算参考值。我们标注哪些是测试的、哪些是推算的 — 让您可以用诚实的数字做决策。',
        'why3_title': '一台设备，三台机器',
        'why3_desc': '一拖三配置让一台混合气体站同时供应最多三台不同功率的激光切割机。更少设备，更少复杂度，更低成本。',
        'why4_title': '24小时仅2度电',
        'why4_desc': '接近零电费。无滤芯更换，无机油更换，无磨损运动部件。设备在后台静默运行，同时您的激光器切割得更快。',
        'why5_title': '兼容您的机器',
        'why5_desc': '大族、DNE、PENTA、LEAD、HSG、BODOR、KIMLA、MESSER — 如果您的机器使用标准辅助气体接口，就兼容。我们会在您购买前确认。',
        'why6_title': '通过 SAGEMRO 提供长期支持',
        'why6_desc': '售后服务、维护指导、备件和技术支持由 <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> — 我们专门的MRO和服务平台处理。购买后您不是独自面对。',
        'label_details': '公司',
        'h2_details': '法律与联系信息',
        'th_detail': '项目',
        'th_info': '信息',
        'td_company': '公司名称',
        'td_location': '所在地',
        'td_business': '业务',
        'td_brands': '品牌',
        'td_product': '本站产品',
        'td_after_sales': '售后服务',
        'td_email': '邮箱',
        'td_phone': '电话/微信',
        'td_whatsapp': 'WhatsApp',
        'td_linkedin': '领英',
        'td_website': '网站',
        'cta_h2': '准备好升级您的激光切割了吗？',
        'cta_p': '告诉我们您的激光配置 — 功率、材料、厚度 — 我们会评估混合气体是否适合您。',
        'footer_product': '产品',
        'footer_related': '相关链接',
        'footer_euchio': 'EUCHIO — 整机设备',
        'footer_sagemro': 'SAGEMRO — 零部件及服务',
        'footer_dhgate': '敦煌网店铺',
        'footer_contact_h': '联系',
        'footer_whatsapp_mx': 'WhatsApp（墨西哥）',
        'footer_whatsapp_th': 'WhatsApp（泰国）',
    },
    'es': {
        'page_title': 'Sobre Nosotros | Euchio Machinery — Equipos de Chapa y Servicio',
        'meta_description': 'Sobre Euchio Machinery — una empresa china de comercio y servicio de maquinaria enfocada en equipos de procesamiento de chapa. Opera las marcas EUCHIO (máquinas completas) y SAGEMRO (repuestos y servicio MRO) para clientes industriales en el extranjero.',
        'hero_badge': '<span>Equipos de Chapa</span> y Servicio',
        'hero_h1': 'Soluciones Prácticas de Equipos<br>para <span class="accent">Fabricantes de Chapa</span>',
        'hero_subtitle': 'Jinan Euchio Machinery Co., Ltd. es una empresa china de comercio y servicio de maquinaria enfocada en equipos de procesamiento de chapa. Operamos dos marcas — <strong>EUCHIO</strong> para máquinas completas y <strong>SAGEMRO</strong> para repuestos y servicio MRO — para servir a clientes industriales en el extranjero con comunicación clara, aprovisionamiento responsable y soporte a largo plazo.',
        'btn_contact_us': 'Contáctenos',
        'label_company': 'Nuestra Empresa',
        'h2_who_we_are': 'Quiénes Somos',
        'wwa_p1': 'Jinan Euchio Machinery Co., Ltd. es una empresa china de comercio y servicio de maquinaria enfocada en equipos de procesamiento de chapa y soluciones industriales relacionadas. Trabajamos con fabricantes en China y conectamos sus equipos con clientes industriales en el extranjero.',
        'wwa_p2': 'La empresa opera dos marcas: <strong>EUCHIO</strong> para máquinas completas que pueden suministrarse bajo nuestra propia identidad de marca, y <strong>SAGEMRO</strong> para productos y servicios MRO — incluyendo mantenimiento, reparación, repuestos y equipos periféricos. Los productos que no pueden ser renombrados, o que provienen de fabricantes que no permiten el etiquetado privado, se ofrecen bajo SAGEMRO o a través de nuestra tienda en línea.',
        'wwa_p3': 'Nuestro objetivo es claro: proporcionar soluciones prácticas de equipos y servicio para clientes industriales en el extranjero, con comunicación clara y soporte a largo plazo. Nos enfocamos en ser honestos sobre lo que podemos y no podemos hacer — si un producto no es el adecuado, lo diremos.',
        'tl1_title': 'Desarrollo de Producto',
        'tl1_desc': 'Identificamos problemas recurrentes de gas auxiliar entre nuestros clientes de corte láser. Desarrollamos un dispositivo de regulación de gas mixto que cubre láseres de fibra de 3kW a 60kW. Las primeras unidades se desplegaron en sitios de clientes para pruebas de campo.',
        'tl2_title': 'Verificación de Campo',
        'tl2_desc': 'Lanzamos gasmixtech.com para documentar lo que hace el dispositivo y compartir resultados de pruebas de campo. Datos de corte verificados recopilados de despliegues de clientes de 12kW, 20kW, 30kW, 40kW y 60kW.',
        'tl3_title': 'Alcance Global',
        'tl3_desc': 'Sitio web multilingüe lanzado (15 idiomas). Continuamos agregando datos verificados de nuevos sitios de clientes. Ventas respaldadas por la tienda en línea DHgate y contacto directo.',
        'label_brands': 'Nuestras Marcas',
        'h2_brands': 'Dos Marcas, Una Misión',
        'brands_subtitle': 'Operamos dos marcas para cubrir diferentes necesidades de equipos y servicios — claramente separadas para que los clientes siempre sepan lo que están obteniendo.',
        'euchio_title': 'EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Máquinas Completas</span>',
        'euchio_desc': 'EUCHIO es nuestra marca para máquinas completas de etiqueta privada, incluyendo máquinas de corte láser, cizallas, cortadoras de tubos, prensas plegadoras y otros equipos de fabricación de chapa. Se utiliza cuando las máquinas completas se suministran bajo nuestra propia identidad de marca.',
        'sagemro_title': 'SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Repuestos y Servicio MRO</span>',
        'sagemro_desc': 'SAGEMRO se enfoca en productos y servicios relacionados con MRO — mantenimiento, reparación, soporte de operación, repuestos, piezas de desgaste, actualizaciones de equipos, soluciones de retrofit y equipos periféricos para corte láser, soldadura, plegado y otras aplicaciones de trabajo de metales.',
        'gas_fit_q': '<strong style="color: var(--color-text);">¿Dónde encaja el dispositivo de gas mixto?</strong>',
        'gas_fit_a': 'El dispositivo de gas mixto es un producto propio que no se ofrece para etiquetado privado. Se suministra bajo la marca SAGEMRO. Para servicio postventa, mantenimiento y soporte técnico, visite <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a>.',
        'label_what_we_do': 'Lo Que Hacemos',
        'h2_what_we_do': 'Equipos, Repuestos y Servicio — Bien Hecho',
        'card1_title': 'Máquinas Completas',
        'card1_desc': 'A través de la marca EUCHIO, suministramos máquinas de corte láser, prensas plegadoras, cortadoras de tubos y cizallas bajo nuestra propia identidad de marca — para clientes que necesitan soluciones de equipos llave en mano.',
        'card2_title': 'Repuestos y Servicio MRO',
        'card2_desc': 'A través de SAGEMRO, proporcionamos repuestos, piezas de desgaste, actualizaciones de equipos, soluciones de retrofit y equipos periféricos para corte láser, soldadura, plegado y otras aplicaciones de trabajo de metales.',
        'card3_title': 'Tecnología de Gas Mixto',
        'card3_desc': 'Nuestros dispositivos propietarios de mezcla de gas nitrógeno-oxígeno para corte láser (3kW–60kW) se ofrecen bajo la marca SAGEMRO. Un dispositivo puede suministrar hasta tres máquinas láser simultáneamente, cortando 3x más rápido sin rebabas y con 33% menos consumo de nitrógeno.',
        'card4_title': 'Consultoría Técnica',
        'card4_desc': 'Evaluamos su potencia láser, espesor de material y configuración de gas antes de recomendar una solución. Si el gas mixto no es adecuado para su aplicación, se lo diremos.',
        'card5_title': 'Soporte Postventa',
        'card5_desc': 'SAGEMRO proporciona mantenimiento continuo, reparación y soporte de operación para todos los equipos que suministramos. El soporte a largo plazo no es un complemento — está integrado en nuestra forma de trabajar.',
        'card6_title': 'Aprovisionamiento Responsable',
        'card6_desc': 'Seleccionamos cuidadosamente a nuestros socios fabricantes y comunicamos honestamente lo que cada producto puede y no puede hacer. Sin especificaciones infladas, sin promesas falsas.',
        'label_deployments': 'Despliegues Reales',
        'h2_deployments': 'No Son Fotos de Catálogo. Son Fábricas Reales de Clientes.',
        'deployments_subtitle': 'Estas son fotos reales de pisos de producción de clientes — instalaciones láser de 20kW, 40kW y 60kW funcionando con gas mixto.',
        'dep40_title': 'Despliegue <span class="params-power">40kW</span>',
        'dep40_desc': 'Foshan, China — Láser de fibra Hymson 40kW con gas mixto. Corte de acero al carbono hasta 35mm. Tanques de almacenamiento de gas líquido verde visibles a la derecha.',
        'dep60_title': 'Despliegue <span class="params-power">60kW</span>',
        'dep60_desc': 'Foshan, China — Láser de fibra 60kW cortando acero al carbono grueso (30–50mm) con gas mixto. Bordes sin rebabas, sin necesidad de rectificado post-corte.',
        'dep20_title': 'Despliegue <span class="params-power">20kW</span>',
        'dep20_desc': 'Máquina Han\'s Laser 20kW con gas mixto — corte de acero al carbono hasta 25mm a velocidades 2.5–7x más rápidas que el oxígeno puro.',
        'want_more': '¿Quiere ver más? Vea videos de corte de fábricas reales de clientes:',
        'btn_view_samples': 'Ver Muestras de Corte →',
        'label_global': 'PROBADO EN PRODUCCIÓN',
        'deployment_metric': 'Unidades instaladas en China',
        'h2_global': 'Validado en fábricas reales',
        'global_note': 'Más de 1.000 dispositivos de mezcla de gases EUCHIO están instalados en fábricas de corte láser en China. El uso continuo en entornos de producción reales ha demostrado un funcionamiento estable y fiable.',
        'label_why': 'Por Qué Elegirnos',
        'h2_why': 'Honestos Sobre Lo Que Somos — y Lo Que No',
        'why1_title': 'Le Decimos Si No Funciona',
        'why1_desc': 'Antes de cotizar, verificamos si el gas mixto tiene sentido para su potencia láser, material y suministro de gas. Si no es así, lo decimos. Preferimos perder una venta que enviar la solución equivocada.',
        'why2_title': 'Datos Reales, No Números de Marketing',
        'why2_desc': 'Nuestras tablas de parámetros distinguen entre datos de campo verificados y valores de referencia estimados. Etiquetamos lo que está probado y lo que está extrapolado — para que pueda tomar decisiones con números honestos.',
        'why3_title': 'Un Dispositivo, Tres Máquinas',
        'why3_desc': 'La configuración uno-a-tres permite que una sola estación de mezcla de gas suministre hasta tres máquinas láser de diferentes niveles de potencia. Menos dispositivos, menos complejidad, menor costo.',
        'why4_title': '2 kWh por 24 Horas',
        'why4_desc': 'Costo de electricidad casi nulo. Sin filtros, sin cambios de aceite, sin piezas móviles que se desgasten. El dispositivo funciona silenciosamente mientras su láser corta más rápido.',
        'why5_title': 'Compatible Con Su Máquina',
        'why5_desc': 'HAN\'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER — si su máquina usa conexiones de gas auxiliar estándar, es compatible. Lo confirmaremos antes de que compre.',
        'why6_title': 'Soporte a Largo Plazo a Través de SAGEMRO',
        'why6_desc': 'El servicio postventa, la guía de mantenimiento, los repuestos y el soporte técnico se gestionan a través de <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> — nuestra plataforma dedicada de MRO y servicio. No está solo después de la compra.',
        'label_details': 'Empresa',
        'h2_details': 'Detalles Legales y de Contacto',
        'th_detail': 'Detalle',
        'th_info': 'Información',
        'td_company': 'Nombre de la Empresa',
        'td_location': 'Ubicación',
        'td_business': 'Negocio',
        'td_brands': 'Marcas',
        'td_product': 'Producto en este sitio',
        'td_after_sales': 'Servicio Postventa',
        'td_email': 'Correo',
        'td_phone': 'Teléfono/WeChat',
        'td_whatsapp': 'WhatsApp',
        'td_linkedin': 'LinkedIn',
        'td_website': 'Sitio Web',
        'cta_h2': '¿Listo para Mejorar Su Corte Láser?',
        'cta_p': 'Cuéntenos sobre su configuración láser — potencia, material, espesor — y evaluaremos si el gas mixto tiene sentido para usted.',
        'footer_product': 'Producto',
        'footer_related': 'Enlaces Relacionados',
        'footer_euchio': 'EUCHIO — Máquinas Completas',
        'footer_sagemro': 'SAGEMRO — Repuestos y Servicio',
        'footer_dhgate': 'Tienda DHgate',
        'footer_contact_h': 'Contacto',
        'footer_whatsapp_mx': 'WhatsApp (México)',
        'footer_whatsapp_th': 'WhatsApp (Tailandia)',
    },
    'de': {
        'page_title': 'Über Uns | Euchio Machinery — Blechbearbeitungsgeräte & Service',
        'meta_description': 'Über Euchio Machinery — ein chinesisches Maschinenhandels- und Serviceunternehmen für Blechbearbeitungsgeräte. Betreibt die Marken EUCHIO (komplette Maschinen) und SAGEMRO (MRO-Teile und Service) für industrielle Kunden im Ausland.',
        'hero_badge': '<span>Blechgeräte</span> & Service',
        'hero_h1': 'Praktische Gerätelösungen<br>für <span class="accent">Blechbearbeiter</span>',
        'hero_subtitle': 'Jinan Euchio Machinery Co., Ltd. ist ein chinesisches Maschinenhandels- und Serviceunternehmen für Blechbearbeitungsgeräte. Wir betreiben zwei Marken — <strong>EUCHIO</strong> für komplette Maschinen und <strong>SAGEMRO</strong> für MRO-Teile und Service — um ausländische Industriekunden mit klarer Kommunikation, verantwortungsvoller Beschaffung und langfristigem Support zu bedienen.',
        'btn_contact_us': 'Kontaktieren Sie uns',
        'label_company': 'Unser Unternehmen',
        'h2_who_we_are': 'Wer wir sind',
        'wwa_p1': 'Jinan Euchio Machinery Co., Ltd. ist ein chinesisches Maschinenhandels- und Serviceunternehmen für Blechbearbeitungsgeräte und verwandte Industrielösungen. Wir arbeiten mit Herstellern in China und verbinden deren Geräte mit ausländischen Industriekunden.',
        'wwa_p2': 'Das Unternehmen betreibt zwei Marken: <strong>EUCHIO</strong> für komplette Maschinen, die unter unserer eigenen Markenidentität geliefert werden können, und <strong>SAGEMRO</strong> für MRO-Produkte und Dienstleistungen — einschließlich Wartung, Reparatur, Ersatzteile und Peripheriegeräte. Produkte, die nicht umgebrandet werden können, oder von Herstellern stammen, die kein Private Labeling erlauben, werden unter SAGEMRO oder über unseren Online-Shop angeboten.',
        'wwa_p3': 'Unser Ziel ist unkompliziert: praktische, passende Geräte- und Servicelösungen für ausländische Industriekunden mit klarer Kommunikation und langfristigem Support. Wir konzentrieren uns darauf, ehrlich darüber zu sein, was wir können und was nicht — wenn ein Produkt nicht passt, sagen wir es.',
        'tl1_title': 'Produktentwicklung',
        'tl1_desc': 'Wiederkehrende Hilfsgasprobleme bei Laserschneidekunden identifiziert. Ein Gasmischreguliergerät für 3kW bis 60kW Faserlaser entwickelt. Erste Geräte bei Kunden vor Ort zur Feldtestung installiert.',
        'tl2_title': 'Feldverifikation',
        'tl2_desc': 'gasmixtech.com gestartet, um zu dokumentieren, was das Gerät tut und Feldtestergebnisse zu teilen. Verifizierte Schneiddaten von 12kW-, 20kW-, 30kW-, 40kW- und 60kW-Kundeneinsätzen gesammelt.',
        'tl3_title': 'Globale Reichweite',
        'tl3_desc': 'Mehrsprachige Website gestartet (15 Sprachen). Weiterhin verifizierte Daten von neuen Kundenstandorten hinzugefügt. Vertrieb über DHgate-Online-Shop und direkten Kontakt.',
        'label_brands': 'Unsere Marken',
        'h2_brands': 'Zwei Marken, eine Mission',
        'brands_subtitle': 'Wir betreiben zwei Marken, um unterschiedliche Geräte- und Servicebedürfnisse abzudecken — klar getrennt, damit Kunden immer wissen, was sie bekommen.',
        'euchio_title': 'EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Komplette Maschinen</span>',
        'euchio_desc': 'EUCHIO ist unsere Marke für Private-Label-Kompletmaschinen, einschließlich Laserschneidmaschinen, Tafelscheren, Rohrschneidmaschinen, Abkantpressen und andere Blechbearbeitungsgeräte. Wird verwendet, wenn komplette Maschinen unter unserer eigenen Markenidentität geliefert werden.',
        'sagemro_title': 'SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— MRO-Teile & Service</span>',
        'sagemro_desc': 'SAGEMRO konzentriert sich auf MRO-bezogene Produkte und Dienstleistungen — Wartung, Reparatur, Betriebsunterstützung, Ersatzteile, Verschleißteile, Geräte-Upgrades, Retrofit-Lösungen und Peripheriegeräte für Laserschneiden, Schweißen, Biegen und andere Metallbearbeitungsanwendungen.',
        'gas_fit_q': '<strong style="color: var(--color-text);">Wo passt das Gasmischgerät hin?</strong>',
        'gas_fit_a': 'Das Gasmischgerät ist ein proprietäres Produkt, das nicht für Private Labeling angeboten wird. Es wird unter der Marke SAGEMRO geliefert. Für Kundendienst, Wartung und technischen Support besuchen Sie <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a>.',
        'label_what_we_do': 'Was wir tun',
        'h2_what_we_do': 'Geräte, Teile und Service — Richtig gemacht',
        'card1_title': 'Komplette Maschinen',
        'card1_desc': 'Über die Marke EUCHIO liefern wir Laserschneidmaschinen, Abkantpressen, Rohrschneider und Tafelscheren unter unserer eigenen Markenidentität — für Kunden, die schlüsselfertige Gerätelösungen benötigen.',
        'card2_title': 'MRO-Teile & Service',
        'card2_desc': 'Über SAGEMRO bieten wir Ersatzteile, Verschleißteile, Geräte-Upgrades, Retrofit-Lösungen und Peripheriegeräte für Laserschneiden, Schweißen, Biegen und andere Metallbearbeitungsanwendungen.',
        'card3_title': 'Gasmischtechnologie',
        'card3_desc': 'Unsere proprietären Stickstoff-Sauerstoff-Gasmischgeräte für Laserschneiden (3kW–60kW) werden unter der Marke SAGEMRO angeboten. Ein Gerät kann gleichzeitig bis zu drei Lasermaschinen versorgen, schneidet 3x schneller ohne Grat und mit 33% weniger Stickstoffverbrauch.',
        'card4_title': 'Technische Beratung',
        'card4_desc': 'Wir bewerten Ihre Laserleistung, Materialstärke und Gasversorgung, bevor wir eine Lösung empfehlen. Wenn Gasgemisch nicht für Ihre Anwendung geeignet ist, sagen wir es.',
        'card5_title': 'Kundendienst',
        'card5_desc': 'SAGEMRO bietet fortlaufende Wartung, Reparatur und Betriebsunterstützung für alle von uns gelieferten Geräte. Langfristiger Support ist kein Add-on — er ist in unsere Arbeitsweise integriert.',
        'card6_title': 'Verantwortungsvolle Beschaffung',
        'card6_desc': 'Wir wählen unsere Fertigungspartner sorgfältig aus und kommunizieren ehrlich, was jedes Produkt kann und was nicht. Keine übertriebenen Specs, keine falschen Versprechen.',
        'label_deployments': 'Reale Einsätze',
        'h2_deployments': 'Keine Katalogfotos. Echte Kundenfabriken.',
        'deployments_subtitle': 'Dies sind echte Fotos von Kundenproduktionsflächen — 20kW-, 40kW- und 60kW-Laseranlagen, die mit Gasgemisch laufen.',
        'dep40_title': '<span class="params-power">40kW</span>-Einsatz',
        'dep40_desc': 'Foshan, China — Hymson 40kW Faserlaser mit Gasgemisch. Schneidet Kohlenstoffstahl bis 35mm. Grüne Flüssiggasspeichertanks rechts sichtbar.',
        'dep60_title': '<span class="params-power">60kW</span>-Einsatz',
        'dep60_desc': 'Foshan, China — 60kW Faserlaser schneidet dicken Kohlenstoffstahl (30–50mm) mit Gasgemisch. Gratfreie Kanten, kein Nachschleifen erforderlich.',
        'dep20_title': '<span class="params-power">20kW</span>-Einsatz',
        'dep20_desc': 'Han\'s Laser 20kW Maschine mit Gasgemisch — schneidet Kohlenstoffstahl bis 25mm mit 2,5–7x höherer Geschwindigkeit als reinem Sauerstoff.',
        'want_more': 'Mehr sehen? Schneidevideos aus echten Kundenfabriken ansehen:',
        'btn_view_samples': 'Schnittproben ansehen →',
        'label_global': 'IN DER PRODUKTION BEWÄHRT',
        'deployment_metric': 'In China installierte Geräte',
        'h2_global': 'Im realen Fabrikeinsatz bewährt',
        'global_note': 'Mehr als 1.000 EUCHIO-Mischgasgeräte sind in Laserschneidbetrieben in China installiert. Der kontinuierliche Einsatz in realen Produktionsumgebungen bestätigt einen stabilen und zuverlässigen Betrieb.',
        'label_why': 'Warum wir',
        'h2_why': 'Ehrlich darüber, was wir sind — und was nicht',
        'why1_title': 'Wir sagen Ihnen, wenn es nicht funktioniert',
        'why1_desc': 'Vor dem Angebot prüfen wir, ob Gasgemisch für Ihre Laserleistung, Ihr Material und Ihre Gasversorgung sinnvoll ist. Wenn nicht, sagen wir es. Wir verlieren lieber einen Verkauf, als die falsche Lösung zu liefern.',
        'why2_title': 'Echte Daten, keine Marketingzahlen',
        'why2_desc': 'Unsere Parametertabellen unterscheiden zwischen verifizierten Felddaten und geschätzten Referenzwerten. Wir kennzeichnen, was getestet und was extrapoliert ist — damit Sie mit ehrlichen Zahlen entscheiden können.',
        'why3_title': 'Ein Gerät, drei Maschinen',
        'why3_desc': 'Die Eins-zu-Drei-Konfiguration ermöglicht es einer einzigen Gasmischstation, bis zu drei Lasermaschinen unterschiedlicher Leistung zu versorgen. Weniger Geräte, weniger Komplexität, niedrigere Kosten.',
        'why4_title': '2 kWh pro 24 Stunden',
        'why4_desc': 'Fast keine Stromkosten. Kein Filterwechsel, kein Ölwechsel, keine Verschleißteile. Das Gerät läuft leise im Hintergrund, während Ihr Laser schneller schneidet.',
        'why5_title': 'Kompatibel mit Ihrer Maschine',
        'why5_desc': 'HAN\'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER — wenn Ihre Maschine Standard-Hilfsgasanschlüsse verwendet, ist sie kompatibel. Wir bestätigen es vor dem Kauf.',
        'why6_title': 'Langfristiger Support durch SAGEMRO',
        'why6_desc': 'Kundendienst, Wartungsleitung, Ersatzteile und technischer Support werden über <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> abgewickelt — unserer dedizierten MRO- und Serviceplattform. Sie sind nach dem Kauf nicht allein.',
        'label_details': 'Unternehmen',
        'h2_details': 'Rechtliche Details & Kontakt',
        'th_detail': 'Detail',
        'th_info': 'Information',
        'td_company': 'Firmenname',
        'td_location': 'Standort',
        'td_business': 'Geschäft',
        'td_brands': 'Marken',
        'td_product': 'Produkt auf dieser Website',
        'td_after_sales': 'Kundendienst & Service',
        'td_email': 'E-Mail',
        'td_phone': 'Telefon/WeChat',
        'td_whatsapp': 'WhatsApp',
        'td_linkedin': 'LinkedIn',
        'td_website': 'Website',
        'cta_h2': 'Bereit, Ihr Laserschneiden zu verbessern?',
        'cta_p': 'Erzählen Sie uns von Ihrer Laserausstattung — Leistung, Material, Stärke — und wir bewerten, ob Gasgemisch für Sie sinnvoll ist.',
        'footer_product': 'Produkt',
        'footer_related': 'Verwandte Links',
        'footer_euchio': 'EUCHIO — Komplette Maschinen',
        'footer_sagemro': 'SAGEMRO — Teile & Service',
        'footer_dhgate': 'DHgate Shop',
        'footer_contact_h': 'Kontakt',
        'footer_whatsapp_mx': 'WhatsApp (Mexiko)',
        'footer_whatsapp_th': 'WhatsApp (Thailand)',
    },
    'fr': {
        'page_title': 'À Propos | Euchio Machinery — Équipements de Tôle & Service',
        'meta_description': 'À propos d\'Euchio Machinery — une entreprise chinoise de commerce et de service de machines spécialisée dans les équipements de traitement de tôle. Opère les marques EUCHIO (machines complètes) et SAGEMRO (pièces et service MRO) pour les clients industriels étrangers.',
        'hero_badge': '<span>Équipements de Tôle</span> & Service',
        'hero_h1': 'Solutions d\'Équipements Pratiques<br>pour <span class="accent">Fabricants de Tôle</span>',
        'hero_subtitle': 'Jinan Euchio Machinery Co., Ltd. est une entreprise chinoise de commerce et de service de machines spécialisée dans les équipements de traitement de tôle. Nous opérons deux marques — <strong>EUCHIO</strong> pour les machines complètes et <strong>SAGEMRO</strong> pour les pièces et services MRO — pour servir les clients industriels étrangers avec une communication claire, un approvisionnement responsable et un support à long terme.',
        'btn_contact_us': 'Contactez-nous',
        'label_company': 'Notre Entreprise',
        'h2_who_we_are': 'Qui Nous Sommes',
        'wwa_p1': 'Jinan Euchio Machinery Co., Ltd. est une entreprise chinoise de commerce et de service de machines spécialisée dans les équipements de traitement de tôle et les solutions industrielles associées. Nous travaillons avec des fabricants en Chine et connectons leurs équipements avec des clients industriels étrangers.',
        'wwa_p2': 'L\'entreprise opère deux marques : <strong>EUCHIO</strong> pour les machines complètes pouvant être fournies sous notre propre identité de marque, et <strong>SAGEMRO</strong> pour les produits et services MRO — incluant maintenance, réparation, pièces de rechange et équipements périphériques. Les produits qui ne peuvent pas être rebaptisés, ou provenant de fabricants n\'autorisant pas le marquage privé, sont proposés sous SAGEMRO ou via notre boutique en ligne.',
        'wwa_p3': 'Notre objectif est simple : fournir des solutions d\'équipements et de services pratiques et adaptées aux clients industriels étrangers, avec une communication claire et un support à long terme. Nous nous concentrons sur l\'honnêteté quant à ce que nous pouvons et ne pouvons pas faire — si un produit n\'est pas adapté, nous le dirons.',
        'tl1_title': 'Développement de Produit',
        'tl1_desc': 'Identification de problèmes récurrents de gaz auxiliaires parmi nos clients de découpe laser. Développement d\'un dispositif de régulation de gaz mixte couvrant les lasers fibrés de 3kW à 60kW. Premières unités déployées sur sites clients pour tests terrain.',
        'tl2_title': 'Vérification Terrain',
        'tl2_desc': 'Lancement de gasmixtech.com pour documenter la fonction du dispositif et partager les résultats de tests terrain. Données de découpe vérifiées collectées auprès de déploiements clients de 12kW, 20kW, 30kW, 40kW et 60kW.',
        'tl3_title': 'Portée Mondiale',
        'tl3_desc': 'Site web multilingue lancé (15 langues). Ajout continu de données vérifiées de nouveaux sites clients. Ventes soutenues via la boutique en ligne DHgate et contact direct.',
        'label_brands': 'Nos Marques',
        'h2_brands': 'Deux Marques, Une Mission',
        'brands_subtitle': 'Nous opérons deux marques pour couvrir différents besoins d\'équipements et de services — clairement séparées pour que les clients sachent toujours ce qu\'ils obtiennent.',
        'euchio_title': 'EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Machines Complètes</span>',
        'euchio_desc': 'EUCHIO est notre marque de machines complètes en marque privée, incluant les machines de découpe laser, cisailles, coupe-tubes, presses plieuses et autres équipements de fabrication de tôle. Utilisée lorsque des machines complètes sont fournies sous notre propre identité de marque.',
        'sagemro_title': 'SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Pièces & Service MRO</span>',
        'sagemro_desc': 'SAGEMRO se concentre sur les produits et services liés au MRO — maintenance, réparation, support d\'exploitation, pièces de rechange, pièces d\'usure, mises à niveau d\'équipements, solutions de retrofit et équipements périphériques pour la découpe laser, le soudage, le pliage et autres applications de travail des métaux.',
        'gas_fit_q': '<strong style="color: var(--color-text);">Où se situe le dispositif de gaz mixte ?</strong>',
        'gas_fit_a': 'Le dispositif de gaz mixte est un produit propriétaire qui n\'est pas proposé en marquage privé. Il est fourni sous la marque SAGEMRO. Pour le service après-vente, la maintenance et le support technique, visitez <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a>.',
        'label_what_we_do': 'Ce Que Nous Faisons',
        'h2_what_we_do': 'Équipements, Pièces et Service — Bien Fait',
        'card1_title': 'Machines Complètes',
        'card1_desc': 'Via la marque EUCHIO, nous fournissons des machines de découpe laser, presses plieuses, coupe-tubes et cisailles sous notre propre identité de marque — pour les clients nécessitant des solutions d\'équipements clés en main.',
        'card2_title': 'Pièces & Service MRO',
        'card2_desc': 'Via SAGEMRO, nous fournissons des pièces de rechange, pièces d\'usure, mises à niveau d\'équipements, solutions de retrofit et équipements périphériques pour la découpe laser, le soudage, le pliage et autres applications de travail des métaux.',
        'card3_title': 'Technologie de Gaz Mixte',
        'card3_desc': 'Nos dispositifs propriétaires de mélange de gaz azote-oxygène pour la découpe laser (3kW–60kW) sont proposés sous la marque SAGEMRO. Un dispositif peut alimenter jusqu\'à trois machines laser simultanément, découpant 3x plus vite sans bavure et avec 33% de moins de consommation d\'azote.',
        'card4_title': 'Conseil Technique',
        'card4_desc': 'Nous évaluons votre puissance laser, l\'épaisseur du matériau et votre configuration d\'alimentation en gaz avant de recommander une solution. Si le gaz mixte n\'est pas adapté à votre application, nous le dirons.',
        'card5_title': 'Support Après-Vente',
        'card5_desc': 'SAGEMRO fournit une maintenance continue, des réparations et un support d\'exploitation pour tous les équipements que nous fournissons. Le support à long terme n\'est pas un supplément — il est intégré à notre façon de travailler.',
        'card6_title': 'Approvisionnement Responsable',
        'card6_desc': 'Nous sélectionnons soigneusement nos partenaires de fabrication et communiquons honnêtement sur ce que chaque produit peut et ne peut pas faire. Pas de spécifications gonflées, pas de fausses promesses.',
        'label_deployments': 'Déploiements Réels',
        'h2_deployments': 'Pas des Photos de Catalogue. De Vraies Usines Clients.',
        'deployments_subtitle': 'Ce sont de vraies photos d\'ateliers de production clients — installations laser 20kW, 40kW et 60kW fonctionnant au gaz mixte.',
        'dep40_title': 'Déploiement <span class="params-power">40kW</span>',
        'dep40_desc': 'Foshan, Chine — Laser fibré Hymson 40kW avec gaz mixte. Découpe d\'acier au carbone jusqu\'à 35mm. Réservoirs de stockage de gaz liquide vert visibles à droite.',
        'dep60_title': 'Déploiement <span class="params-power">60kW</span>',
        'dep60_desc': 'Foshan, Chine — Laser fibré 60kW découpant de l\'acier au carbone épais (30–50mm) avec gaz mixte. Bords sans bavure, aucun meulage post-découpe requis.',
        'dep20_title': 'Déploiement <span class="params-power">20kW</span>',
        'dep20_desc': 'Machine Han\'s Laser 20kW avec gaz mixte — découpe d\'acier au carbone jusqu\'à 25mm à des vitesses 2,5–7x plus rapides que l\'oxygène pur.',
        'want_more': 'Vous voulez voir plus ? Regardez des vidéos de découpe de vraies usines clientes :',
        'btn_view_samples': 'Voir les Échantillons de Coupe →',
        'label_global': 'ÉPROUVÉ EN PRODUCTION',
        'deployment_metric': 'Unités installées en Chine',
        'h2_global': 'Validé dans de véritables usines',
        'global_note': 'Plus de 1 000 dispositifs de mélange de gaz EUCHIO sont installés dans des usines de découpe laser en Chine. Leur utilisation continue en production réelle a confirmé un fonctionnement stable et fiable.',
        'label_why': 'Pourquoi Nous Choisir',
        'h2_why': 'Honnêtes sur Ce Que Nous Sommes — et Ce Que Nous Ne Sommes Pas',
        'why1_title': 'Nous Vous Disons Si Ça Ne Marche Pas',
        'why1_desc': 'Avant de deviser, nous vérifions si le gaz mixte a du sens pour votre puissance laser, votre matériau et votre alimentation en gaz. Si ce n\'est pas le cas, nous le disons. Nous préférons perdre une vente que d\'envoyer la mauvaise solution.',
        'why2_title': 'Données Réelles, Pas des Chiffres Marketing',
        'why2_desc': 'Nos tableaux de paramètres distinguent les données de terrain vérifiées des valeurs de référence estimées. Nous étiquetons ce qui est testé et ce qui est extrapolé — pour que vous puissiez décider avec des chiffres honnêtes.',
        'why3_title': 'Un Dispositif, Trois Machines',
        'why3_desc': 'La configuration un-pour-trois permet à une seule station de mélange de gaz d\'alimenter jusqu\'à trois machines laser de différents niveaux de puissance. Moins de dispositifs, moins de complexité, coût plus bas.',
        'why4_title': '2 kWh par 24 Heures',
        'why4_desc': 'Coût d\'électricité presque nul. Pas de filtres, pas de vidange, pas de pièces mobiles qui s\'usent. Le dispositif fonctionne silencieusement pendant que votre laser coupe plus vite.',
        'why5_title': 'Compatible avec Votre Machine',
        'why5_desc': 'HAN\'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER — si votre machine utilise des connexions de gaz auxiliaire standard, elle est compatible. Nous confirmerons avant que vous achetiez.',
        'why6_title': 'Support à Long Terme via SAGEMRO',
        'why6_desc': 'Le service après-vente, l\'assistance à la maintenance, les pièces de rechange et le support technique sont gérés via <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> — notre plateforme dédiée MRO et service. Vous n\'êtes pas seul après l\'achat.',
        'label_details': 'Entreprise',
        'h2_details': 'Détails Légaux et de Contact',
        'th_detail': 'Détail',
        'th_info': 'Information',
        'td_company': 'Nom de l\'Entreprise',
        'td_location': 'Emplacement',
        'td_business': 'Activité',
        'td_brands': 'Marques',
        'td_product': 'Produit sur ce site',
        'td_after_sales': 'Service Après-Vente',
        'td_email': 'E-mail',
        'td_phone': 'Téléphone/WeChat',
        'td_whatsapp': 'WhatsApp',
        'td_linkedin': 'LinkedIn',
        'td_website': 'Site Web',
        'cta_h2': 'Prêt à Améliorer Votre Découpe Laser ?',
        'cta_p': 'Parlez-nous de votre configuration laser — puissance, matériau, épaisseur — et nous évaluerons si le gaz mixte a du sens pour vous.',
        'footer_product': 'Produit',
        'footer_related': 'Liens Connexes',
        'footer_euchio': 'EUCHIO — Machines Complètes',
        'footer_sagemro': 'SAGEMRO — Pièces & Service',
        'footer_dhgate': 'Boutique DHgate',
        'footer_contact_h': 'Contact',
        'footer_whatsapp_mx': 'WhatsApp (Mexique)',
        'footer_whatsapp_th': 'WhatsApp (Thaïlande)',
    },
    'ja': {
        'page_title': '会社概要 | Euchio Machinery — 板金設備・サービス',
        'meta_description': 'Euchio Machinery について — 板金加工設備に特化した中国の機械貿易・サービス企業。海外の産業顧客向けに EUCHIO（完成機）および SAGEMRO（MRO部品・サービス）ブランドを運営。',
        'hero_badge': '<span>板金設備</span>・サービス',
        'hero_h1': '板金加工業者のための<br><span class="accent">実用的な設備ソリューション</span>',
        'hero_subtitle': '济南钰峭機械有限公司は、板金加工設備に特化した中国の機械貿易・サービス企業です。EUCHIO（完成機）と SAGEMRO（MRO部品・サービス）の2つのブランドを運営し、明確なコミュニケーション、責任ある調達、長期的なサポートで海外の産業顧客にサービスを提供します。',
        'btn_contact_us': 'お問い合わせ',
        'label_company': '会社概要',
        'h2_who_we_are': '私たちについて',
        'wwa_p1': '济南钰峭機械有限公司は、板金加工設備および関連する産業ソリューションに特化した中国の機械貿易・サービス企業です。中国のメーカーと協力し、その設備を海外の産業顧客と結びつけます。',
        'wwa_p2': '当社は2つのブランドを運営しています：<strong>EUCHIO</strong> — 自社ブランドで供給できる完成機、<strong>SAGEMRO</strong> — 保守、修理、スペアパーツ、周辺機器を含むMRO製品・サービス。再ブランド化できない製品、またはプライベートラベルを許可しないメーカーの製品は、SAGEMROまたはオンラインストアを通じて提供されます。',
        'wwa_p3': '私たちの目標は明確です：明確なコミュニケーションと長期的なサポートにより、海外の産業顧客に実用的で適合した設備・サービスソリューションを提供すること。できることとできないことについて正直に努めます — 製品が合わない場合は、そう言います。',
        'tl1_title': '製品開発',
        'tl1_desc': 'レーザー切断顧客間で繰り返し発生する補助ガス問題を特定。3kW〜60kWファイバーレーザーをカバーする混合ガス調整装置を開発。最初のユニットを顧客サイトに配置し、フィールドテストを実施。',
        'tl2_title': 'フィールド検証',
        'tl2_desc': 'gasmixtech.comを立ち上げ、装置の機能を文書化し、フィールドテスト結果を共有。12kW、20kW、30kW、40kW、60kWの顧客デプロイメントから検証された切断データを収集。',
        'tl3_title': 'グローバル展開',
        'tl3_desc': '多言語ウェブサイトを立ち上げ（15言語）。新規顧客サイトから検証データの追加を継続。DHgateオンラインストアと直接連絡による販売支援。',
        'label_brands': '私たちのブランド',
        'h2_brands': '2つのブランド、1つの使命',
        'brands_subtitle': '異なる設備・サービスニーズをカバーするため、2つのブランドを運営しています — 常にお客様が何を得ているか分かるよう、明確に分離しています。',
        'euchio_title': 'EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— 完成機</span>',
        'euchio_desc': 'EUCHIOは、レーザー切断機、シャー、パイプ切断機、ベンダー、その他の板金加工設備を含むプライベートラベル完成機のブランドです。完成機が自社ブランドで供給される場合に使用されます。',
        'sagemro_title': 'SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— MRO部品・サービス</span>',
        'sagemro_desc': 'SAGEMROは、レーザー切断、溶接、曲げ、その他の金属加工アプリケーション向けの保守、修理、運用サポート、スペアパーツ、消耗品、設備アップグレード、レトロフィットソリューション、周辺機器を含むMRO関連製品・サービスに注力しています。',
        'gas_fit_q': '<strong style="color: var(--color-text);">混合ガス装置はどのブランドに属しますか？</strong>',
        'gas_fit_a': '混合ガス装置はプライベートラベル非対応の独自製品です。SAGEMROブランドで供給されます。アフターサービス、メンテナンス、技術サポートは <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a> をご覧ください。',
        'label_what_we_do': '事業内容',
        'h2_what_we_do': '設備、部品、サービス — 正しく',
        'card1_title': '完成機',
        'card1_desc': 'EUCHIOブランドを通じて、自社ブランドでレーザー切断機、ベンダー、パイプ切断機、シャーを供給します — ターンキー設備ソリューションが必要な顧客向け。',
        'card2_title': 'MRO部品・サービス',
        'card2_desc': 'SAGEMROを通じて、レーザー切断、溶接、曲げ、その他の金属加工アプリケーション向けのスペアパーツ、消耗品、設備アップグレード、レトロフィットソリューション、周辺機器を提供します。',
        'card3_title': '混合ガス技術',
        'card3_desc': 'レーザー切断用（3kW〜60kW）の独自の窒素・酸素混合ガス装置は SAGEMRO ブランドで提供されます。1台の装置で最大3台のレーザー機を同時に供給でき、バリなしで3倍速く切断し、窒素消費量を33%削減します。',
        'card4_title': '技術コンサルティング',
        'card4_desc': 'ソリューションを推奨する前に、レーザー出力、材料厚さ、ガス供給設定を評価します。混合ガスがお客様の用途に適さない場合は、お伝えします。',
        'card5_title': 'アフターサポート',
        'card5_desc': 'SAGEMRO は、当社が供給するすべての設備に対して継続的な保守、修理、運用サポートを提供します。長期的なサポートは追加オプションではなく — 私たちの働き方に組み込まれています。',
        'card6_title': '責任ある調達',
        'card6_desc': '製造パートナーを慎重に選択し、各製品の可能なことと不可能なことを正直に伝えます。誇大スペックなし、偽りの約束なし。',
        'label_deployments': '実際の導入',
        'h2_deployments': 'カタログ写真ではありません。実際の顧客工場です。',
        'deployments_subtitle': 'これらは顧客の生産現場からの実際の写真です — 混合ガスで稼働する20kW、40kW、60kWのレーザー設備。',
        'dep40_title': '<span class="params-power">40kW</span> 導入',
        'dep40_desc': '中国仏山 — 海目星 40kW ファイバーレーザーと混合ガス。炭素鋼を35mmまで切断。右側に緑色の液化ガス貯蔵タンクが見えます。',
        'dep60_title': '<span class="params-power">60kW</span> 導入',
        'dep60_desc': '中国仏山 — 60kW ファイバーレーザーが混合ガスで厚板炭素鋼（30〜50mm）を切断。バリフリーエッジ、切断後の研磨不要。',
        'dep20_title': '<span class="params-power">20kW</span> 導入',
        'dep20_desc': 'ハンズレーザー 20kW 機と混合ガス — 炭素鋼を25mmまで純酸素より2.5〜7倍速く切断。',
        'want_more': 'もっと見たいですか？実際の顧客工場からの切断動画をご覧ください：',
        'btn_view_samples': '切断サンプルを見る →',
        'label_global': '生産現場で実証済み',
        'deployment_metric': '中国国内の設置台数',
        'h2_global': '実際の工場稼働で実証',
        'global_note': '中国のレーザー切断工場に1,000台を超えるEUCHIO混合ガス装置が設置されています。実際の生産環境での継続使用により、安定した信頼性の高い稼働が確認されています。',
        'label_why': '選ばれる理由',
        'h2_why': '私たちが何であるか — そして何でないか — に正直',
        'why1_title': '合わない場合はお伝えします',
        'why1_desc': '見積もり前に、レーザー出力、材料、ガス供給に対して混合ガスが適切か確認します。不適切な場合はお伝えします。間違ったソリューションを出荷するより、売上を失うことを選びます。',
        'why2_title': '実データ、マーケティング数字ではない',
        'why2_desc': 'パラメータ表は、検証されたフィールドデータと推定参照値を区別します。テスト済みのものと推定のものを明記し — 正直な数字で意思決定できます。',
        'why3_title': '1台の装置、3台の機械',
        'why3_desc': '1対3構成により、1つのガス混合ステーションで異なる出力レベルの最大3台のレーザー機を供給できます。装置が少なく、複雑さが減り、コストが下がります。',
        'why4_title': '24時間で2 kWh',
        'why4_desc': 'ほぼゼロの電気コスト。フィルター不要、オイル交換不要、摩耗する可動部なし。装置は静かに稼働し、レーザーはより速く切断します。',
        'why5_title': 'お使いの機械と互換',
        'why5_desc': 'HAN\'S、DNE、PENTA、LEAD、HSG、BODOR、KIMLA、MESSER — 標準的な補助ガス接続を使用する機械なら互換性があります。購入前に確認します。',
        'why6_title': 'SAGEMRO による長期サポート',
        'why6_desc': 'アフターサービス、メンテナンスガイダンス、スペアパーツ、技術サポートは <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> — 専用のMRO・サービスプラットフォームで処理されます。購入後も一人ではありません。',
        'label_details': '会社',
        'h2_details': '法人情報・連絡先',
        'th_detail': '項目',
        'th_info': '情報',
        'td_company': '会社名',
        'td_location': '所在地',
        'td_business': '事業',
        'td_brands': 'ブランド',
        'td_product': '本サイトの製品',
        'td_after_sales': 'アフターサービス',
        'td_email': 'メール',
        'td_phone': '電話/WeChat',
        'td_whatsapp': 'WhatsApp',
        'td_linkedin': 'LinkedIn',
        'td_website': 'ウェブサイト',
        'cta_h2': 'レーザー切断をアップグレードする準備はできましたか？',
        'cta_p': 'レーザー設定をお聞かせください — 出力、材料、厚さ — 混合ガスが適切か評価します。',
        'footer_product': '製品',
        'footer_related': '関連リンク',
        'footer_euchio': 'EUCHIO — 完成機',
        'footer_sagemro': 'SAGEMRO — 部品・サービス',
        'footer_dhgate': 'DHgate ストア',
        'footer_contact_h': '連絡先',
        'footer_whatsapp_mx': 'WhatsApp（メキシコ）',
        'footer_whatsapp_th': 'WhatsApp（タイ）',
    },
    'ru': {
        'page_title': 'О нас | Euchio Machinery — Листовое оборудование и сервис',
        'meta_description': 'О Euchio Machinery — китайская торгово-сервисная машиностроительная компания, специализирующаяся на оборудовании для обработки листового металла. Управляет брендами EUCHIO (готовые станки) и SAGEMRO (запчасти и сервис MRO) для зарубежных промышленных клиентов.',
        'hero_badge': '<span>Листовое оборудование</span> и сервис',
        'hero_h1': 'Практичные решения по оборудованию<br>для <span class="accent">производителей листового металла</span>',
        'hero_subtitle': 'Jinan Euchio Machinery Co., Ltd. — китайская торгово-сервисная машиностроительная компания, специализирующаяся на оборудовании для обработки листового металла. Мы управляем двумя брендами — <strong>EUCHIO</strong> для готовых станков и <strong>SAGEMRO</strong> для запчастей и сервиса MRO — для обслуживания зарубежных промышленных клиентов с чёткой коммуникацией, ответственными закупками и долгосрочной поддержкой.',
        'btn_contact_us': 'Связаться с нами',
        'label_company': 'Наша компания',
        'h2_who_we_are': 'Кто мы',
        'wwa_p1': 'Jinan Euchio Machinery Co., Ltd. — китайская торгово-сервисная машиностроительная компания, специализирующаяся на оборудовании для обработки листового металла и смежных промышленных решениях. Мы работаем с производителями в Китае и связываем их оборудование с зарубежными промышленными клиентами.',
        'wwa_p2': 'Компания управляет двумя брендами: <strong>EUCHIO</strong> — готовые станки, поставляемые под собственным брендом, и <strong>SAGEMRO</strong> — продукция и услуги MRO, включая техобслуживание, ремонт, запчасти и периферийное оборудование. Продукция, не подлежащая ребрендингу, или от производителей, не допускающих частную маркировку, предлагается под SAGEMRO или через наш интернет-магазин.',
        'wwa_p3': 'Наша цель проста: предоставлять практичные, подходящие решения по оборудованию и сервису для зарубежных промышленных клиентов с чёткой коммуникацией и долгосрочной поддержкой. Мы честны в том, что можем и не можем сделать — если продукт не подходит, мы так и скажем.',
        'tl1_title': 'Разработка продукта',
        'tl1_desc': 'Выявлены повторяющиеся проблемы со вспомогательным газом у клиентов лазерной резки. Разработано устройство регулирования смешанного газа для волоконных лазеров мощностью от 3кВт до 60кВт. Первые образцы развёрнуты на площадках клиентов для полевых испытаний.',
        'tl2_title': 'Полевая верификация',
        'tl2_desc': 'Запущен gasmixtech.com для документирования функций устройства и обмена результатами полевых испытаний. Собраны проверенные данные резки от клиентских развёртываний 12кВт, 20кВт, 30кВт, 40кВт и 60кВт.',
        'tl3_title': 'Глобальный охват',
        'tl3_desc': 'Запущен многоязычный сайт (15 языков). Продолжаем добавлять проверенные данные с новых клиентских площадок. Продажи поддерживаются через интернет-магазин DHgate и прямой контакт.',
        'label_brands': 'Наши бренды',
        'h2_brands': 'Два бренда, одна миссия',
        'brands_subtitle': 'Мы управляем двумя брендами для покрытия различных потребностей в оборудовании и сервисе — чётко разделённых, чтобы клиенты всегда знали, что получают.',
        'euchio_title': 'EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Готовые станки</span>',
        'euchio_desc': 'EUCHIO — наш бренд готовых станков частной марки, включая лазерные раскройные машины, листовые ножницы, труборезы, листогибы и другое оборудование для обработки листового металла. Используется, когда готовые станки поставляются под нашим брендом.',
        'sagemro_title': 'SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Запчасти и сервис MRO</span>',
        'sagemro_desc': 'SAGEMRO специализируется на продукции и услугах MRO — техобслуживание, ремонт, эксплуатационная поддержка, запчасти, изнашиваемые детали, модернизация оборудования, ретрофит-решения и периферийное оборудование для лазерной резки, сварки, гибки и других металлообрабатывающих применений.',
        'gas_fit_q': '<strong style="color: var(--color-text);">К какому бренду относится газосмесительное устройство?</strong>',
        'gas_fit_a': 'Газосмесительное устройство — проприетарный продукт, не предлагаемый для частной маркировки. Оно поставляется под брендом SAGEMRO. Для послепродажного обслуживания, техобслуживания и технической поддержки посетите <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a>.',
        'label_what_we_do': 'Чем мы занимаемся',
        'h2_what_we_do': 'Оборудование, запчасти и сервис — качественно',
        'card1_title': 'Готовые станки',
        'card1_desc': 'Через бренд EUCHIO мы поставляем лазерные раскройные машины, листогибы, труборезы и ножницы под собственным брендом — для клиентов, нуждающихся в готовых оборудовательных решениях.',
        'card2_title': 'Запчасти и сервис MRO',
        'card2_desc': 'Через SAGEMRO мы предоставляем запчасти, изнашиваемые детали, модернизацию оборудования, ретрофит-решения и периферийное оборудование для лазерной резки, сварки, гибки и других металлообрабатывающих применений.',
        'card3_title': 'Технология смешанного газа',
        'card3_desc': 'Наши проприетарные газосмесительные устройства азот-кислород для лазерной резки (3кВт–60кВт) предлагаются под брендом SAGEMRO. Одно устройство может одновременно питать до трёх лазерных машин, резая в 3 раза быстрее без заусенцев и с на 33% меньшим потреблением азота.',
        'card4_title': 'Технический консалтинг',
        'card4_desc': 'Перед рекомендацией решения мы оцениваем мощность вашего лазера, толщину материала и настройку газоснабжения. Если смешанный газ не подходит для вашего применения, мы скажем.',
        'card5_title': 'Послепродажная поддержка',
        'card5_desc': 'SAGEMRO обеспечивает постоянное техобслуживание, ремонт и эксплуатационную поддержку всего поставляемого нами оборудования. Долгосрочная поддержка — это не дополнение, а часть нашей работы.',
        'card6_title': 'Ответственные закупки',
        'card6_desc': 'Мы тщательно отбираем производственных партнёров и честно сообщаем, что каждый продукт может и не может делать. Без завышенных характеристик, без ложных обещаний.',
        'label_deployments': 'Реальные внедрения',
        'h2_deployments': 'Не каталог. Реальные фабрики клиентов.',
        'deployments_subtitle': 'Это реальные фотографии с производственных площадок клиентов — лазерные установки 20кВт, 40кВт и 60кВт, работающие на смешанном газе.',
        'dep40_title': 'Внедрение <span class="params-power">40кВт</span>',
        'dep40_desc': 'Фошань, Китай — волоконный лазер Hymson 40кВт со смешанным газом. Резка углеродистой стали до 35мм. Справа видны зелёные резервуары для хранения жидкого газа.',
        'dep60_title': 'Внедрение <span class="params-power">60кВт</span>',
        'dep60_desc': 'Фошань, Китай — волоконный лазер 60кВт режет толстую углеродистую сталь (30–50мм) смешанным газом. Края без заусенцев, дополнительная шлифовка не требуется.',
        'dep20_title': 'Внедрение <span class="params-power">20кВт</span>',
        'dep20_desc': 'Машина Han\'s Laser 20кВт со смешанным газом — резка углеродистой стали до 25мм со скоростью в 2,5–7 раз выше чистого кислорода.',
        'want_more': 'Хотите увидеть больше? Смотрите видео резки с реальных фабрик клиентов:',
        'btn_view_samples': 'Образцы резы →',
        'label_global': 'ПРОВЕРЕНО В ПРОИЗВОДСТВЕ',
        'deployment_metric': 'Установлено в Китае',
        'h2_global': 'Проверено в реальных производственных условиях',
        'global_note': 'Более 1 000 устройств смешанного газа EUCHIO установлены на предприятиях лазерной резки в Китае. Непрерывная эксплуатация в реальных производственных условиях подтвердила стабильную и надёжную работу.',
        'label_why': 'Почему мы',
        'h2_why': 'Честны о том, что мы — и чем не являемся',
        'why1_title': 'Мы скажем, если не сработает',
        'why1_desc': 'Перед расчётом мы проверяем, имеет ли смысл смешанный газ для вашей мощности лазера, материала и газоснабжения. Если нет — говорим прямо. Мы лучше потеряем сделку, чем отправим неправильное решение.',
        'why2_title': 'Реальные данные, не маркетинговые цифры',
        'why2_desc': 'Наши таблицы параметров различают проверенные полевые данные и оценочные эталонные значения. Мы маркируем протестированное и экстраполированное — чтобы вы могли принимать решения с честными цифрами.',
        'why3_title': 'Одно устройство, три машины',
        'why3_desc': 'Конфигурация «один-к-трём» позволяет одной газосмесительной станции питать до трёх лазерных машин разной мощности. Меньше устройств, меньше сложности, ниже стоимость.',
        'why4_title': '2 кВт·ч за 24 часа',
        'why4_desc': 'Почти нулевые затраты на электричество. Без фильтров, без замены масла, без изнашиваемых деталей. Устройство работает бесшумно, пока ваш лазер режет быстрее.',
        'why5_title': 'Совместимо с вашей машиной',
        'why5_desc': 'HAN\'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER — если ваша машина использует стандартные соединения вспомогательного газа, она совместима. Мы подтвердим перед покупкой.',
        'why6_title': 'Долгосрочная поддержка через SAGEMRO',
        'why6_desc': 'Послепродажное обслуживание, руководство по ТО, запчасти и техподдержка осуществляются через <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> — нашу специализированную платформу MRO и сервиса. Вы не одиноки после покупки.',
        'label_details': 'Компания',
        'h2_details': 'Юридические данные и контакты',
        'th_detail': 'Параметр',
        'th_info': 'Информация',
        'td_company': 'Название компании',
        'td_location': 'Местонахождение',
        'td_business': 'Деятельность',
        'td_brands': 'Бренды',
        'td_product': 'Продукт на этом сайте',
        'td_after_sales': 'Послепродажный сервис',
        'td_email': 'Email',
        'td_phone': 'Телефон/WeChat',
        'td_whatsapp': 'WhatsApp',
        'td_linkedin': 'LinkedIn',
        'td_website': 'Сайт',
        'cta_h2': 'Готовы улучшить лазерную резку?',
        'cta_p': 'Расскажите о вашей лазерной установке — мощность, материал, толщина — и мы оценим, подходит ли вам смешанный газ.',
        'footer_product': 'Продукт',
        'footer_related': 'Связанные ссылки',
        'footer_euchio': 'EUCHIO — Готовые станки',
        'footer_sagemro': 'SAGEMRO — Запчасти и сервис',
        'footer_dhgate': 'Магазин DHgate',
        'footer_contact_h': 'Контакт',
        'footer_whatsapp_mx': 'WhatsApp (Мексика)',
        'footer_whatsapp_th': 'WhatsApp (Таиланд)',
    },
}

# For languages not yet fully translated, use English as fallback (empty dict)
# They will still get nav + UI translation + structural fixes + lang-current fix
# Body content stays in English until translations are added


def apply_structural(content, lang):
    """Apply structural changes for subdirectory language page."""
    p = lang

    # Asset paths
    content = content.replace('href="./styles.min.css', 'href="../styles.min.css')
    content = content.replace('src="./script.min.js"', 'src="../script.min.js"')
    content = content.replace('href="./favicon.svg"', 'href="../favicon.svg"')
    content = content.replace('src="/script.min.js"', 'src="../script.min.js"')

    # Image paths (src and srcset)
    content = content.replace('src="./images/', 'src="../images/')
    content = content.replace('src="/images/', 'src="../images/')
    content = content.replace('srcset="./images/', 'srcset="../images/')
    content = content.replace('srcset="/images/', 'srcset="../images/')

    # HTML lang
    content = content.replace('<html lang="en">', f'<html lang="{lang}">')

    # Canonical
    content = content.replace(
        '<link rel="canonical" href="https://gasmixtech.com/about.html">',
        f'<link rel="canonical" href="https://gasmixtech.com/{p}/about.html">')
    content = content.replace(
        '<link rel="canonical" href="https://gasmixtech.com/about">',
        f'<link rel="canonical" href="https://gasmixtech.com/{p}/about">')

    # OG:url
    content = content.replace(
        '<meta property="og:url" content="https://gasmixtech.com/about.html">',
        f'<meta property="og:url" content="https://gasmixtech.com/{p}/about.html">')
    content = content.replace(
        '<meta property="og:url" content="https://gasmixtech.com/about">',
        f'<meta property="og:url" content="https://gasmixtech.com/{p}/about">')

    # Nav: logo links
    content = content.replace('href="/" class="logo"', f'href="/{p}/" class="logo"')

    # Nav: Home link
    content = content.replace('<a href="/">Home</a>', f'<a href="/{p}/">Home</a>')

    # Nav: About link (both active and non-active)
    content = content.replace('<a href="/about.html" class="active">About</a>', f'<a href="/{p}/about.html" class="active">About</a>')
    content = content.replace('<a href="/about.html">About</a>', f'<a href="/{p}/about.html">About</a>')
    content = content.replace('<a href="/about" class="active">About</a>', f'<a href="/{p}/about" class="active">About</a>')
    content = content.replace('<a href="/about">About</a>', f'<a href="/{p}/about">About</a>')

    # Nav: section anchors
    for sec in ['#principle', '#advantages', '#samples', '#reference', '#faq', '#parameters']:
        content = content.replace(f'<a href="/{sec}"', f'<a href="/{p}/{sec}"')

    # Nav: parameters.html link
    content = content.replace('href="/parameters.html"', f'href="/{p}/parameters.html"')
    content = content.replace('href="/parameters"', f'href="/{p}/parameters"')

    # Nav: contact CTA
    content = content.replace(
        'href="/contact.html" class="nav-cta',
        f'href="/{p}/contact.html" class="nav-cta')
    content = content.replace(
        'href="/contact" class="nav-cta',
        f'href="/{p}/contact" class="nav-cta')

    # Contact Us button (hero + CTA section)
    content = content.replace('href="/contact.html" class="btn btn-secondary">Contact Us', f'href="/{p}/contact.html" class="btn btn-secondary">Contact Us')
    content = content.replace('href="/contact" class="btn btn-secondary">Contact Us', f'href="/{p}/contact" class="btn btn-secondary">Contact Us')

    # Footer links
    content = content.replace('href="/about.html">About Us', f'href="/{p}/about.html">About Us')
    content = content.replace('href="/about">About Us', f'href="/{p}/about">About Us')
    for sec in ['#principle', '#advantages', '#parameters', '#samples', '#faq']:
        content = content.replace(f'href="/{sec}"', f'href="/{p}/{sec}"')
    content = content.replace('href="/parameters.html"', f'href="/{p}/parameters.html"')

    # View Cutting Samples link
    content = content.replace('href="/#samples"', f'href="/{p}/#samples"')

    # Privacy link
    content = content.replace('href="/privacy.html"', f'href="/{p}/privacy.html"')

    # Language dropdown: update active state
    content = content.replace(
        f'<a href="/about.html" class="lang-option active" data-lang="en">English</a>',
        '<a href="/about.html" class="lang-option" data-lang="en">English</a>')
    content = content.replace(
        '<a href="/about" class="lang-option active" data-lang="en">English</a>',
        '<a href="/about" class="lang-option" data-lang="en">English</a>')
    content = content.replace(
        f'<a href="/{p}/about.html" class="lang-option" data-lang="{p}">',
        f'<a href="/{p}/about.html" class="lang-option active" data-lang="{p}">')
    content = content.replace(
        f'<a href="/{p}/about" class="lang-option" data-lang="{p}">',
        f'<a href="/{p}/about" class="lang-option active" data-lang="{p}">')

    # Update lang-current display
    old_current = '<span class="lang-current">EN</span>'
    new_current = f'<span class="lang-current">{LANG_CODE_DISPLAY.get(p, p.upper())}</span>'
    content = content.replace(old_current, new_current)

    # Breadcrumb JSON-LD
    content = content.replace(
        '"item": "https://gasmixtech.com/about.html"',
        f'"item": "https://gasmixtech.com/{p}/about.html"')
    content = content.replace(
        '"item": "https://gasmixtech.com/about"',
        f'"item": "https://gasmixtech.com/{p}/about"')

    content = content.replace(f'https://gasmixtech.com/{p}/about.html', f'https://gasmixtech.com/{p}/about')
    content = content.replace('https://gasmixtech.com/about.html', 'https://gasmixtech.com/about')
    content = content.replace(f'/{p}/about.html', f'/{p}/about')
    content = content.replace('/about.html', '/about')

    # Footer logo link
    content = content.replace('href="/" class="logo"', f'href="/{p}/" class="logo"')

    if lang in ABOUT_IMAGE_ALTS:
        for english_alt, localized_alt in zip(ENGLISH_ABOUT_IMAGE_ALTS, ABOUT_IMAGE_ALTS[lang]):
            content = content.replace(f'alt="{english_alt}"', f'alt="{localized_alt}"')

    return content


def apply_translations(content, lang):
    """Apply UI and body translations."""
    tr = UI_TRANSLATIONS.get(lang, {})

    # Nav items
    content = re.sub(r'>(About)<', f'>{tr.get("About", "About")}<', content)
    content = content.replace(f'>{tr.get("About", "About")} Us</a>', f'>{tr.get("About Us", "About Us")}</a>')
    content = content.replace('>Home</a>', f'>{tr.get("Home", "Home")}</a>')
    content = content.replace('>How It Works</a>', f'>{tr.get("How It Works", "How It Works")}</a>')
    content = content.replace('>Parameters</a>', f'>{tr.get("Parameters", "Parameters")}</a>')
    content = content.replace('>Samples</a>', f'>{tr.get("Samples", "Samples")}</a>')
    content = content.replace('>Cutting Samples</a>', f'>{tr.get("Cutting Samples", "Cutting Samples")}</a>')
    content = content.replace('>Blog</a>', f'>{tr.get("Blog", "Blog")}</a>')
    content = content.replace('>Contact</a>', f'>{tr.get("Contact", "Contact")}</a>')
    content = content.replace('>Advantages</a>', f'>{tr.get("Advantages", "Advantages")}</a>')
    content = content.replace('>FAQ</a>', f'>{tr.get("FAQ", "FAQ")}</a>')

    if lang in COMPACT_COPY:
        compact = COMPACT_COPY[lang]
        content = content.replace(
            'About Us | Euchio Machinery — Sheet Metal Equipment & Service',
            compact['title'])
        content = content.replace(
            'About Euchio Machinery — a China-based machinery trading and service company focused on sheet metal processing equipment. Operating EUCHIO (complete machines) and SAGEMRO (MRO parts and service) brands for overseas industrial customers.',
            compact['description'])
        content = re.sub(
            r'<main id="main">.*?</main>',
            lambda _: render_main(lang, tr),
            content,
            flags=re.DOTALL)
        content = content.replace(
            'Jinan Euchio Machinery Co., Ltd. — machinery trading and service for sheet metal processing equipment. Operating EUCHIO (complete machines) and SAGEMRO (MRO parts & service) brands for overseas industrial customers.',
            compact['footer_intro'])
        return content

    # CTA buttons in nav
    content = content.replace('>Get a Quote →', f'>{tr.get("Get a Quote →", "Get a Quote →")}')

    # Footer
    content = content.replace('>About Us</a>', f'>{tr.get("About Us", "About Us")}</a>')
    content = content.replace('>About Us</li>', f'>{tr.get("About Us", "About Us")}</li>')

    # Body translations
    bt = BODY_TRANSLATIONS.get(lang, {})

    # Apply body translations via direct string replacement
    replacements = [
        # Meta
        ('About Us | Euchio Machinery — Sheet Metal Equipment & Service', bt.get('page_title', 'About Us | Euchio Machinery — Sheet Metal Equipment & Service')),
        ('About Euchio Machinery — a China-based machinery trading and service company focused on sheet metal processing equipment. Operating EUCHIO (complete machines) and SAGEMRO (MRO parts and service) brands for overseas industrial customers.', bt.get('meta_description', 'About Euchio Machinery — a China-based machinery trading and service company focused on sheet metal processing equipment. Operating EUCHIO (complete machines) and SAGEMRO (MRO parts and service) brands for overseas industrial customers.')),

        # Hero
        ('<span>Sheet Metal Equipment</span> & Service', bt.get('hero_badge', '<span>Sheet Metal Equipment</span> & Service')),
        ('Practical Equipment Solutions<br>for <span class="accent">Sheet Metal Fabricators</span>', bt.get('hero_h1', 'Practical Equipment Solutions<br>for <span class="accent">Sheet Metal Fabricators</span>')),
        ('Jinan Euchio Machinery Co., Ltd. is a China-based machinery trading and service company focused on sheet metal processing equipment. We operate two brands — <strong>EUCHIO</strong> for complete machines and <strong>SAGEMRO</strong> for MRO parts and service — to serve overseas industrial customers with clear communication, responsible sourcing, and long-term support.', bt.get('hero_subtitle', '')),
        ('Contact Us', bt.get('btn_contact_us', 'Contact Us')),

        # Who We Are
        ('>Our Company<', f'>{bt.get("label_company", "Our Company")}<'),
        ('>Who We Are<', f'>{bt.get("h2_who_we_are", "Who We Are")}<'),
        ('Jinan Euchio Machinery Co., Ltd. is a China-based machinery trading and service company focused on sheet metal processing equipment and related industrial solutions. We work with manufacturers in China and connect their equipment with overseas industrial customers.', bt.get('wwa_p1', '')),
        ('The company operates two brands: <strong>EUCHIO</strong> for complete machines that can be supplied under our own brand identity, and <strong>SAGEMRO</strong> for MRO products and services — including maintenance, repair, spare parts, and peripheral equipment. Products that cannot be rebranded, or that come from manufacturers who do not allow private labeling, are offered under SAGEMRO or through our online store.', bt.get('wwa_p2', '')),
        ('Our goal is straightforward: provide practical, well-matched equipment and service solutions for overseas industrial customers, with clear communication and long-term support. We focus on being honest about what we can and cannot do — if a product isn\'t the right fit, we\'ll say so.', bt.get('wwa_p3', '')),

        # Timeline
        ('>Product Development<', f'>{bt.get("tl1_title", "Product Development")}<'),
        ('Identified recurring auxiliary gas problems among laser cutting customers. Developed a mixed gas regulation device covering 3kW to 60kW fiber lasers. First units deployed at customer sites for field testing.', bt.get('tl1_desc', '')),
        ('>Field Verification<', f'>{bt.get("tl2_title", "Field Verification")}<'),
        ('Launched gasmixtech.com to document what the device does and share field-test results. Verified cutting data collected from 12kW, 20kW, 30kW, 40kW, and 60kW customer deployments.', bt.get('tl2_desc', '')),
        ('>Global Reach<', f'>{bt.get("tl3_title", "Global Reach")}<'),
        ('Multi-language website launched (15 languages). Continuing to add verified data from new customer sites. Sales supported through DHgate online store and direct contact.', bt.get('tl3_desc', '')),

        # Two Brands
        ('>Our Brands<', f'>{bt.get("label_brands", "Our Brands")}<'),
        ('>Two Brands, One Mission<', f'>{bt.get("h2_brands", "Two Brands, One Mission")}<'),
        ('We operate two brands to cover different equipment and service needs — clearly separated so customers always know what they\'re getting.', bt.get('brands_subtitle', '')),
        ('EUCHIO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— Complete Machines</span>', bt.get('euchio_title', '')),
        ('EUCHIO is our brand for private-label complete machines, including laser cutting machines, sheet shearing machines, tube cutting machines, press brakes, and other sheet metal fabrication equipment. It is used when complete machines are supplied under our own brand identity.', bt.get('euchio_desc', '')),
        ('SAGEMRO <span style="font-size: 0.8rem; font-weight: 400; color: var(--color-text-muted);">— MRO Parts & Service</span>', bt.get('sagemro_title', '')),
        ('SAGEMRO focuses on MRO-related products and services — maintenance, repair, operation support, spare parts, wearing parts, equipment upgrades, retrofit solutions, and peripheral equipment for laser cutting, welding, bending, and other metalworking applications. Products not suitable for private labeling are also offered under SAGEMRO.', bt.get('sagemro_desc', '')),
        ('<strong style="color: var(--color-text);">Where does the gas mixing device fit?</strong>', bt.get('gas_fit_q', '')),
        ('The mixed gas device is a proprietary product that is not offered for private labeling. It is supplied under the SAGEMRO brand. For after-sales service, maintenance, and technical support, visit <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">sagemro.com</a>.', bt.get('gas_fit_a', '')),

        # What We Do
        ('>What We Do<', f'>{bt.get("label_what_we_do", "What We Do")}<'),
        ('>Equipment, Parts, and Service — Done Right<', f'>{bt.get("h2_what_we_do", "Equipment, Parts, and Service — Done Right")}<'),
        ('>Complete Machines</h3>', f'>{bt.get("card1_title", "Complete Machines")}</h3>'),
        ('Through the EUCHIO brand, we supply laser cutting machines, press brakes, tube cutters, and shearing machines under our own brand identity — for customers who need turnkey equipment solutions.', bt.get('card1_desc', '')),
        ('>MRO Parts & Service</h3>', f'>{bt.get("card2_title", "MRO Parts & Service")}</h3>'),
        ('Through SAGEMRO, we provide spare parts, wearing parts, equipment upgrades, retrofit solutions, and peripheral equipment for laser cutting, welding, bending, and other metalworking applications.', bt.get('card2_desc', '')),
        ('>Gas Mixing Technology</h3>', f'>{bt.get("card3_title", "Gas Mixing Technology")}</h3>'),
        ('Our proprietary nitrogen-oxygen gas mixing devices for laser cutting (3kW–60kW) are offered under the SAGEMRO brand. One device can supply up to three laser machines simultaneously, cutting 3x faster with zero burrs and 33% less nitrogen consumption.', bt.get('card3_desc', '')),
        ('>Technical Consulting</h3>', f'>{bt.get("card4_title", "Technical Consulting")}</h3>'),
        ('We assess your laser power, material thickness, and gas supply setup before recommending a solution. If mixed gas isn\'t right for your application, we\'ll tell you.', bt.get('card4_desc', '')),
        ('>After-Sales Support</h3>', f'>{bt.get("card5_title", "After-Sales Support")}</h3>'),
        ('SAGEMRO provides ongoing maintenance, repair, and operation support for all equipment we supply. Long-term support is not an add-on — it\'s built into how we work.', bt.get('card5_desc', '')),
        ('>Responsible Sourcing</h3>', f'>{bt.get("card6_title", "Responsible Sourcing")}</h3>'),
        ('We select manufacturing partners carefully and communicate honestly about what each product can and cannot do. No inflated specs, no false promises.', bt.get('card6_desc', '')),

        # Deployments
        ('>Real-World Deployments<', f'>{bt.get("label_deployments", "Real-World Deployments")}<'),
        ('>Not Catalog Photos. Real Customer Factories.<', f'>{bt.get("h2_deployments", "Not Catalog Photos. Real Customer Factories.")}<'),
        ('These are actual photos from customer production floors — 20kW, 40kW, and 60kW laser installations running with mixed gas.', bt.get('deployments_subtitle', '')),
        ('<span class="params-power">40kW</span> Deployment', bt.get('dep40_title', '<span class="params-power">40kW</span> Deployment')),
        ('Foshan, China — Hymson 40kW fiber laser with mixed gas. Cutting carbon steel up to 35mm. Green liquid gas storage tanks visible on the right.', bt.get('dep40_desc', '')),
        ('<span class="params-power">60kW</span> Deployment', bt.get('dep60_title', '<span class="params-power">60kW</span> Deployment')),
        ('Foshan, China — 60kW fiber laser cutting thick carbon steel (30–50mm) with mixed gas. Burr-free edges, zero post-cut grinding required.', bt.get('dep60_desc', '')),
        ('<span class="params-power">20kW</span> Deployment', bt.get('dep20_title', '<span class="params-power">20kW</span> Deployment')),
        ('Han\'s Laser 20kW machine with mixed gas — cutting carbon steel up to 25mm at speeds 2.5–7x faster than pure oxygen.', bt.get('dep20_desc', '')),
        ('Want to see more? Watch cutting videos from real customer factories:', bt.get('want_more', '')),
        ('>View Cutting Samples →', f'>{bt.get("btn_view_samples", "View Cutting Samples →")}'),

        # Deployment Proof
        ('>PROVEN IN PRODUCTION<', f'>{bt.get("label_global", "PROVEN IN PRODUCTION")}<'),
        ('>Units Installed Across China<', f'>{bt.get("deployment_metric", "Units Installed Across China")}<'),
        ('>Proven by Real Factory Use<', f'>{bt.get("h2_global", "Proven by Real Factory Use")}<'),
        ('More than 1,000 EUCHIO gas mixing devices are installed at laser cutting factories across China. Continuous use in real production environments has validated stable, reliable operation.', bt.get('global_note', '')),

        # Why Choose Us
        ('>Why Choose Us<', f'>{bt.get("label_why", "Why Choose Us")}<'),
        ('>Honest About What We Are — and Aren\'t<', f'>{bt.get("h2_why", "Honest About What We Are — and Aren\'t")}<'),
        ('>We Tell You If It Won\'t Work</h3>', f'>{bt.get("why1_title", "We Tell You If It Won\'t Work")}</h3>'),
        ('Before quoting, we check whether mixed gas makes sense for your laser power, material, and gas supply. If it doesn\'t, we\'ll say so. We\'d rather lose a sale than ship the wrong solution.', bt.get('why1_desc', '')),
        ('>Real Data, Not Marketing Numbers</h3>', f'>{bt.get("why2_title", "Real Data, Not Marketing Numbers")}</h3>'),
        ('Our parameter tables distinguish between verified field data and estimated reference values. We label what\'s tested and what\'s extrapolated — so you can make decisions with honest numbers.', bt.get('why2_desc', '')),
        ('>One Device, Three Machines</h3>', f'>{bt.get("why3_title", "One Device, Three Machines")}</h3>'),
        ('The one-to-three configuration lets a single gas mixing station supply up to three laser machines of different power levels. Fewer devices, less complexity, lower cost.', bt.get('why3_desc', '')),
        ('>2 kWh per 24 Hours</h3>', f'>{bt.get("why4_title", "2 kWh per 24 Hours")}</h3>'),
        ('Near-zero electricity cost. No filters, no oil changes, no moving parts that wear out. The device runs silently in the background while your laser cuts faster.', bt.get('why4_desc', '')),
        ('>Compatible With Your Machine</h3>', f'>{bt.get("why5_title", "Compatible With Your Machine")}</h3>'),
        ('HAN\'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER — if your machine uses standard auxiliary gas connections, it\'s compatible. We\'ll confirm before you buy.', bt.get('why5_desc', '')),
        ('>Long-Term Support Through SAGEMRO</h3>', f'>{bt.get("why6_title", "Long-Term Support Through SAGEMRO")}</h3>'),
        ('After-sales service, maintenance guidance, spare parts, and technical support are handled through <a href="https://www.sagemro.com" target="_blank" rel="noopener" style="color: var(--color-accent);">SAGEMRO</a> — our dedicated MRO and service platform. You\'re not on your own after purchase.', bt.get('why6_desc', '')),

        # Company Details
        ('>Company<', f'>{bt.get("label_details", "Company")}<'),
        ('>Legal & Contact Details<', f'>{bt.get("h2_details", "Legal & Contact Details")}<'),
        ('>Detail</th>', f'>{bt.get("th_detail", "Detail")}</th>'),
        ('>Information</th>', f'>{bt.get("th_info", "Information")}</th>'),
        ('>Company Name</td>', f'>{bt.get("td_company", "Company Name")}</td>'),
        ('>Location</td>', f'>{bt.get("td_location", "Location")}</td>'),
        ('>Business</td>', f'>{bt.get("td_business", "Business")}</td>'),
        ('>Brands</td>', f'>{bt.get("td_brands", "Brands")}</td>'),
        ('>Product on this site</td>', f'>{bt.get("td_product", "Product on this site")}</td>'),
        ('>After-Sales & Service</td>', f'>{bt.get("td_after_sales", "After-Sales & Service")}</td>'),
        ('>Email</td>', f'>{bt.get("td_email", "Email")}</td>'),
        ('>Phone / WeChat</td>', f'>{bt.get("td_phone", "Phone / WeChat")}</td>'),
        ('>WhatsApp</td>', f'>{bt.get("td_whatsapp", "WhatsApp")}</td>'),
        ('>LinkedIn</td>', f'>{bt.get("td_linkedin", "LinkedIn")}</td>'),
        ('>Website</td>', f'>{bt.get("td_website", "Website")}</td>'),

        # CTA Section
        ('>Ready to Upgrade Your Laser Cutting?<', f'>{bt.get("cta_h2", "Ready to Upgrade Your Laser Cutting?")}<'),
        ('Tell us about your laser setup — power, material, thickness — and we\'ll assess whether mixed gas makes sense for you.', bt.get('cta_p', '')),

        # Footer
        ('>Product</h4>', f'>{bt.get("footer_product", "Product")}</h4>'),
        ('>Related Links</h4>', f'>{bt.get("footer_related", "Related Links")}</h4>'),
        ('>EUCHIO — Complete Machines</a>', f'>{bt.get("footer_euchio", "EUCHIO — Complete Machines")}</a>'),
        ('>SAGEMRO — Parts & Service</a>', f'>{bt.get("footer_sagemro", "SAGEMRO — Parts & Service")}</a>'),
        ('>DHgate Store</a>', f'>{bt.get("footer_dhgate", "DHgate Store")}</a>'),
        ('>Contact</h4>', f'>{bt.get("footer_contact_h", "Contact")}</h4>'),
        ('>WhatsApp (Mexico)</a>', f'>{bt.get("footer_whatsapp_mx", "WhatsApp (Mexico)")}</a>'),
        ('>WhatsApp (Thailand)</a>', f'>{bt.get("footer_whatsapp_th", "WhatsApp (Thailand)")}</a>'),
    ]

    for old, new in replacements:
        if new and old != new:
            content = content.replace(old, new)

    return content


def main():
    with open(SOURCE, 'r', encoding='utf-8') as f:
        source_content = f.read()

    for lang in LANGS:
        content = source_content
        content = apply_structural(content, lang)
        content = apply_translations(content, lang)

        out_dir = os.path.join(BASE, lang)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'about.html')

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Generated: {lang}/about.html")

    print(f"\nDone! Generated {len(LANGS)} language versions.")


if __name__ == '__main__':
    main()

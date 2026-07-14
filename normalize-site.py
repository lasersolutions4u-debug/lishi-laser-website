#!/usr/bin/env python3
import re
from pathlib import Path


PUBLIC = Path(__file__).resolve().parent / 'public'
LANGS = ['en', 'es', 'zh', 'ko', 'ja', 'pt', 'tr', 'pl', 'it', 'de', 'fr', 'nl', 'ru', 'vi', 'th']

ABOUT_LABELS = {
    'en': 'About',
    'es': 'Acerca de',
    'zh': '关于我们',
    'ko': '소개',
    'ja': '会社概要',
    'pt': 'Sobre',
    'tr': 'Hakkımızda',
    'pl': 'O nas',
    'it': 'Chi siamo',
    'de': 'Über uns',
    'fr': 'À propos',
    'nl': 'Over ons',
    'ru': 'О нас',
    'vi': 'Giới thiệu',
    'th': 'เกี่ยวกับ',
}

TITLES = {
    'en': {'parameters': '20kW Laser Cutting Parameters | Mixed Gas vs O₂ Speed Data', 'contact': 'Get Cutting Gas Assessment | EUCHIO Mixed Gas Device'},
    'es': {'parameters': 'Parámetros de Corte Láser 20kW | Gas Mixto vs O₂', 'contact': 'Contacto | Cotización del Dispositivo de Gas Mixto EUCHIO'},
    'zh': {'parameters': '20kW激光切割参数 | 混合气与氧气速度数据', 'contact': '联系我们 | EUCHIO混合气体设备'},
    'ko': {'parameters': '20kW 레이저 절단 파라미터 | 혼합가스와 O₂ 속도 데이터', 'contact': '문의하기 | EUCHIO 혼합가스 장치 견적'},
    'ja': {'parameters': '20kWレーザー切断パラメータ | 混合ガスとO₂の速度データ', 'contact': 'お問い合わせ | EUCHIO 混合ガス装置 見積もり'},
    'pt': {'parameters': 'Parâmetros de Corte a Laser 20kW | Gás Misto vs O₂', 'contact': 'Contato | Cotação do Dispositivo de Gás Misto EUCHIO'},
    'tr': {'parameters': '20kW Lazer Kesim Parametreleri | Karışık Gaz ve O₂', 'contact': 'İletişim | EUCHIO Karışık Gaz Cihazı Teklifi'},
    'pl': {'parameters': 'Parametry Cięcia Laserowego 20kW | Gaz Mieszany i O₂', 'contact': 'Kontakt | Wycena Urządzenia do Mieszania Gazów EUCHIO'},
    'it': {'parameters': 'Parametri di Taglio Laser 20kW | Gas Misto vs O₂', 'contact': 'Contatti | Preventivo Dispositivo a Gas Misto EUCHIO'},
    'de': {'parameters': '20kW Laserschneidparameter | Mischgas vs O₂', 'contact': 'Kontakt | Angebot für EUCHIO Mischgasgerät'},
    'fr': {'parameters': 'Paramètres de Découpe Laser 20kW | Gaz Mixte vs O₂', 'contact': 'Contact | Devis Dispositif à Gaz Mixte EUCHIO'},
    'nl': {'parameters': '20kW Lasersnijparameters | Menggas vs O₂', 'contact': 'Contact | Offerte voor EUCHIO Menggasapparaat'},
    'ru': {'parameters': 'Параметры лазерной резки 20 кВт | Смешанный газ и O₂', 'contact': 'Контакты | Предложение на устройство смешанного газа EUCHIO'},
    'vi': {'parameters': 'Thông số Cắt Laser 20kW | Khí Hỗn hợp và O₂', 'contact': 'Liên hệ | Báo giá Thiết bị Khí Hỗn hợp EUCHIO'},
    'th': {'parameters': 'พารามิเตอร์ตัดเลเซอร์ 20kW | ก๊าซผสมและ O₂', 'contact': 'ติดต่อ | ใบเสนอราคาอุปกรณ์ก๊าซผสม EUCHIO'},
}

H1_TITLES = {
    'ja': {
        'parameters': '20kWレーザー切断パラメータとガス速度データ',
    },
}

QUESTIONS = {
    'es': ('¿Un dispositivo puede suministrar gas a tres máquinas láser simultáneamente?', 'Sí. La configuración estable uno a tres permite suministrar gas simultáneamente a un máximo de tres máquinas láser de diferentes potencias.'),
    'zh': ('一台混合气设备能否同时为三台激光机供气？', '可以。稳定的一拖三配置可同时为最多三台不同功率的激光机供气。'),
    'ko': ('혼합가스 장치 한 대로 최대 세 대의 레이저 장비에 동시에 공급할 수 있나요?', '예. 안정적인 1대 3 구성으로 출력이 서로 다른 최대 세 대의 레이저 장비에 동시에 공급할 수 있습니다.'),
    'ja': ('1台の混合ガス装置で最大3台のレーザー機に同時供給できますか？', 'はい。安定した1対3構成により、出力の異なる最大3台のレーザー機へ同時に供給できます。'),
    'pt': ('Um dispositivo pode fornecer gás para até três máquinas laser simultaneamente?', 'Sim. A configuração estável um para três permite fornecer gás simultaneamente para até três máquinas laser de diferentes potências.'),
    'tr': ('Bir karışık gaz cihazı aynı anda üç lazer makinesine kadar gaz sağlayabilir mi?', 'Evet. Kararlı bire üç yapı, farklı güçlerde üç lazer makinesine kadar aynı anda gaz sağlar.'),
    'pl': ('Czy jedno urządzenie może jednocześnie zasilać do trzech maszyn laserowych?', 'Tak. Stabilna konfiguracja jeden do trzech zasila jednocześnie do trzech maszyn laserowych o różnej mocy.'),
}


def language_for(path):
    rel = path.relative_to(PUBLIC)
    return rel.parts[0] if rel.parts[0] in LANGS[1:] else 'en'


def normalize_urls(content):
    content = re.sub(
        r'https://gasmixtech\.com/([a-z]{2})//+(about|contact|parameters)\.html',
        r'https://gasmixtech.com/\1/\2',
        content)
    content = re.sub(
        r'(https://gasmixtech\.com(?:/[a-z]{2})?/(?:about|contact|parameters))\.html',
        r'\1',
        content)
    content = re.sub(
        r'href="(/(?:[a-z]{2}/)?(?:about|contact|parameters))\.html"',
        r'href="\1"',
        content)
    return content


def normalize_header_nav(content, lang):
    def reorder(match):
        body = match.group('body')
        lines = body.splitlines(keepends=True)
        newline = '\r\n' if '\r\n' in body else '\n'

        def href_for(line):
            anchor = re.search(r'<a\b[^>]*\bhref="([^"]+)"', line)
            return anchor.group(1) if anchor else ''

        parameter_lines = [line for line in lines if 'parameters' in href_for(line)]
        contact_lines = [line for line in lines if 'contact' in href_for(line)]
        if len(parameter_lines) != 1 or len(contact_lines) != 1:
            return match.group(0)

        about_lines = [line for line in lines if 'about' in href_for(line)]
        if about_lines:
            about_anchor = about_lines[0].strip()
        else:
            about_href = '/about' if lang == 'en' else f'/{lang}/about'
            about_anchor = f'<a href="{about_href}">{ABOUT_LABELS[lang]}</a>'

        lines = [line for line in lines if 'about' not in href_for(line)]
        contact_index = next(i for i, line in enumerate(lines) if 'contact' in href_for(line))
        indent = re.match(r'\s*', lines[contact_index]).group(0).replace('\r', '').replace('\n', '')
        lines.insert(contact_index, f'{indent}{about_anchor}{newline}')
        return f'{match.group("open")}{"".join(lines)}{match.group("close")}'

    return re.sub(
        r'(?P<open><nav class="nav"[^>]*>)(?P<body>.*?)(?P<close></nav>)',
        reorder,
        content,
        count=1,
        flags=re.DOTALL)


def normalize_page(path):
    content = path.read_text(encoding='utf-8')
    original = content
    lang = language_for(path)
    page_type = path.stem

    content = normalize_urls(content)

    if lang != 'en':
        content = content.replace('href="/about"', f'href="/{lang}/about"')
        content = content.replace('href="./about"', f'href="/{lang}/about"')

    content = normalize_header_nav(content, lang)

    if page_type in ('parameters', 'contact'):
        title = TITLES[lang][page_type]
        content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, count=1, flags=re.DOTALL)
        if '<h1' not in content:
            content = re.sub(r'<h2([^>]*)>', r'<h1\1>', content, count=1)
            content = content.replace('</h2>', '</h1>', 1)
        if lang in H1_TITLES and page_type in H1_TITLES[lang]:
            content = re.sub(
                r'(<h1[^>]*>).*?(</h1>)',
                rf'\g<1>{H1_TITLES[lang][page_type]}\g<2>',
                content,
                count=1,
                flags=re.DOTALL)

    content = content.replace('One-to-Two', 'One-to-Three')
    content = content.replace('one-to-two', 'one-to-three')
    content = content.replace('One‑to‑Two', 'One‑to‑Three')
    content = content.replace('one‑to‑two', 'one‑to‑three')
    content = content.replace('two laser cutting machines', 'up to three laser cutting machines')
    content = content.replace('two laser machines', 'up to three laser machines')

    if lang in QUESTIONS:
        question, answer = QUESTIONS[lang]
        content = re.sub(
            r'("name": ")[^"]*(?:two|dos|两台|2台|두 대|trzech|iki|dois)[^"]*(")',
            rf'\g<1>{question}\g<2>',
            content,
            flags=re.IGNORECASE)
        content = re.sub(
            r'("text": ")[^"]*one-to-three[^"]*(")',
            rf'\g<1>{answer}\g<2>',
            content,
            flags=re.IGNORECASE)

    if lang == 'ko':
        content = content.replace(
            'Yes. The EUCHIO Mixed Gas supports a stable configuration. 하나의 혼합 스테이션은 서로 다른 파워 레벨의 두 대의 레이저 머신(예: 12KW 1대 및 20KW 1대)에 안정적인 가스 혼합 비율로 동시에 공급할 수 있습니다.',
            '예. EUCHIO Mixed Gas는 안정적인 1대 3 구성을 지원하며, 하나의 혼합 스테이션이 출력이 서로 다른 최대 세 대의 레이저 장비에 동시에 가스를 공급할 수 있습니다.')

    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

    if content != original:
        path.write_text(content, encoding='utf-8', newline='')


def main():
    for path in PUBLIC.rglob('*.html'):
        normalize_page(path)


if __name__ == '__main__':
    main()

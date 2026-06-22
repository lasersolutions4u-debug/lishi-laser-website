#!/usr/bin/env node
/**
 * build-privacy.js — Generate translated privacy policy pages for all 15 languages.
 * Reads privacy.html as structural template, replaces content with translations.
 * Usage: node build-privacy.js
 */

const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = __dirname;
const LANG_DIRS = ['zh','es','ko','ja','pt','tr','pl','it','de','fr','nl','ru','vi','th'];

// ─── Translations ────────────────────────────────────────────────────

const T = {
  en: {
    metaDesc: 'Privacy Policy for EUCHIO Mixed Gas — how we collect, use, and protect your personal data.',
    title: 'Privacy Policy | EUCHIO Mixed Gas',
    pageTitle: 'Privacy Policy',
    lastUpdated: 'Last updated: May 25, 2026',
    nav: { home:'Home', howItWorks:'How It Works', advantages:'Advantages', parameters:'Parameters', samples:'Cutting Samples', references:'References', blog:'Blog', contact:'Contact' },
    s1t: '1. Who We Are',
    s1p: 'EUCHIO Mixed Gas is a mixed gas cutting technology series operated by Jinan Euchio Machinery Co., Ltd. Our website is <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. What Data We Collect',
    s2p: 'We collect the following information when you use our website:',
    s2l1: '<strong>Contact form submissions</strong> — name, email address, phone number, company name, and any message content you choose to provide. This data is processed via Web3Forms and sent directly to us by email.',
    s2l2: '<strong>Analytics data</strong> — we use Google Analytics 4 (GA4) to understand how visitors use our site. This includes pages visited, time on site, geographic region (country/city level), device type, and referral source. GA4 does not collect your IP address in full.',
    s2l3: '<strong>Server logs</strong> — our hosting provider (Cloudflare) automatically collects basic access logs including anonymized IP addresses, browser type, and timestamps for security and performance monitoring.',
    s3t: '3. How We Use Your Data',
    s3p: 'We use the collected data for these purposes only:',
    s3l1: 'Responding to your inquiries submitted via our contact form',
    s3l2: 'Understanding website traffic and improving our content (analytics)',
    s3l3: 'Ensuring website security and preventing abuse',
    s3noshare: 'We do not sell, rent, or share your personal data with third parties for their marketing purposes.',
    s4t: '4. Cookies',
    s4p1: 'Google Analytics uses first-party cookies to distinguish users. These cookies do not store personally identifiable information. You can disable cookies in your browser settings, or opt out of Google Analytics entirely using the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics Opt-out Browser Add-on</a>.',
    s4p2: 'Our website does not use advertising cookies, tracking pixels, or third-party marketing cookies.',
    s5t: '5. Legal Basis (GDPR)',
    s5p: 'For visitors from the European Economic Area (EEA), we process your data on the following legal bases:',
    s5l1: '<strong>Legitimate interest</strong> — analytics data to improve our website and services.',
    s5l2: '<strong>Consent</strong> — contact form data, which you voluntarily provide when submitting an inquiry.',
    s6t: '6. Data Retention',
    s6p: 'Contact form inquiries are retained in our email system for the duration of the business relationship plus 2 years. Google Analytics data is retained for 14 months. Cloudflare logs are retained for 24 hours.',
    s7t: '7. Your Rights',
    s7p: 'You have the right to:',
    s7l1: 'Request access to the personal data we hold about you',
    s7l2: 'Request correction or deletion of your data',
    s7l3: 'Withdraw consent at any time (for contact form data)',
    s7l4: 'Object to analytics data processing',
    s7contact: 'To exercise any of these rights, contact us at <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Third-Party Services',
    s8p: 'We use the following third-party services that may process your data:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, USA) — website analytics. Google is certified under the EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., USA) — website hosting and security. Cloudflare is certified under the EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — contact form delivery. Form submissions are sent directly to our email.',
    s9t: '9. Contact',
    s9p: 'If you have questions about this privacy policy or wish to exercise your data rights, contact us:',
    s9email: 'Email',
    s9phone: 'Phone',
    s9addr: 'Address: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, China',
    footerTagline: 'Gas Mixing Technology',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Product',
    footerHow: 'How It Works',
    footerAdv: 'Advantages',
    footerParams: 'Parameters',
    footerSamples: 'Cutting Samples',
    footerBlog: 'Blog',
    footerContact: 'Contact',
    footerWA_MX: 'WhatsApp (Mexico)',
    footerWA_TH: 'WhatsApp (Thailand)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. All rights reserved.',
    footerPrivacy: 'Privacy Policy',
    footerLinkedIn: 'LinkedIn'
  },

  zh: {
    metaDesc: 'EUCHIO隐私政策 — 我们如何收集、使用和保护您的个人数据。',
    title: '隐私政策 | EUCHIO Mixed Gas',
    pageTitle: '隐私政策',
    lastUpdated: '最后更新：2026年5月25日',
    nav: { home:'首页', howItWorks:'工作原理', advantages:'优势特点', parameters:'参数数据', samples:'切割案例', references:'客户案例', blog:'Blog', contact:'联系我们' },
    s1t: '1. 我们是谁',
    s1p: 'EUCHIO Mixed Gas 是由济南钰峭机械有限公司（Jinan Euchio Machinery Co., Ltd.）运营的混合气体切割技术系列。我们的网站是 <a href="https://gasmixtech.com">gasmixtech.com</a>。',
    s2t: '2. 我们收集哪些数据',
    s2p: '当您使用我们的网站时，我们会收集以下信息：',
    s2l1: '<strong>联系表单提交</strong> — 姓名、邮箱地址、电话号码、公司名称以及您选择提供的任何消息内容。这些数据通过 Web3Forms 处理并直接发送到我们的邮箱。',
    s2l2: '<strong>分析数据</strong> — 我们使用 Google Analytics 4（GA4）来了解访客如何使用我们的网站。包括访问的页面、停留时间、地理区域（国家/城市级别）、设备类型和引荐来源。GA4 不会收集您的完整 IP 地址。',
    s2l3: '<strong>服务器日志</strong> — 我们的托管服务商（Cloudflare）会自动收集基本访问日志，包括匿名化 IP 地址、浏览器类型和时间戳，用于安全和性能监控。',
    s3t: '3. 我们如何使用您的数据',
    s3p: '我们仅将收集的数据用于以下目的：',
    s3l1: '回复您通过联系表单提交的咨询',
    s3l2: '了解网站流量并改进我们的内容（分析）',
    s3l3: '确保网站安全并防止滥用',
    s3noshare: '我们不会将您的个人数据出售、出租或分享给第三方用于其营销目的。',
    s4t: '4. Cookie',
    s4p1: 'Google Analytics 使用第一方 Cookie 来区分用户。这些 Cookie 不存储个人身份信息。您可以在浏览器设置中禁用 Cookie，或使用 <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics 选择退出浏览器插件</a> 完全退出 Google Analytics。',
    s4p2: '我们的网站不使用广告 Cookie、追踪像素或第三方营销 Cookie。',
    s5t: '5. 法律依据（GDPR）',
    s5p: '对于来自欧洲经济区（EEA）的访客，我们基于以下法律依据处理您的数据：',
    s5l1: '<strong>合法利益</strong> — 用于改进我们网站和服务的分析数据。',
    s5l2: '<strong>同意</strong> — 联系表单数据，您在提交咨询时自愿提供。',
    s6t: '6. 数据保留',
    s6p: '联系表单咨询在我们的邮件系统中保留至业务关系结束加 2 年。Google Analytics 数据保留 14 个月。Cloudflare 日志保留 24 小时。',
    s7t: '7. 您的权利',
    s7p: '您拥有以下权利：',
    s7l1: '请求访问我们持有的关于您的个人数据',
    s7l2: '请求更正或删除您的数据',
    s7l3: '随时撤回同意（针对联系表单数据）',
    s7l4: '反对分析数据处理',
    s7contact: '如需行使上述任何权利，请通过 <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a> 联系我们。',
    s8t: '8. 第三方服务',
    s8p: '我们使用以下可能处理您数据的第三方服务：',
    s8l1: '<strong>Google Analytics</strong>（Google LLC，美国）— 网站分析。Google 已获得 EU-US 数据隐私框架认证。',
    s8l2: '<strong>Cloudflare</strong>（Cloudflare, Inc.，美国）— 网站托管与安全。Cloudflare 已获得 EU-US 数据隐私框架认证。',
    s8l3: '<strong>Web3Forms</strong> — 联系表单投递。表单提交内容直接发送到我们的邮箱。',
    s9t: '9. 联系我们',
    s9p: '如果您对本隐私政策有任何疑问，或希望行使您的数据权利，请联系我们：',
    s9email: '邮箱',
    s9phone: '电话',
    s9addr: '地址：济南钰峭机械有限公司，中国山东济南',
    footerTagline: '混合气体技术',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: '产品',
    footerHow: '工作原理',
    footerAdv: '优势特点',
    footerParams: '参数数据',
    footerSamples: '切割案例',
    footerBlog: 'Blog',
    footerContact: '联系我们',
    footerWA_MX: 'WhatsApp（墨西哥）',
    footerWA_TH: 'WhatsApp（泰国）',
    footerCopy: '© 2026 济南钰峭机械有限公司 版权所有',
    footerPrivacy: '隐私政策',
    footerLinkedIn: 'LinkedIn'
  },

  es: {
    metaDesc: 'Política de Privacidad de EUCHIO Mixed Gas — cómo recopilamos, usamos y protegemos sus datos personales.',
    title: 'Política de Privacidad | EUCHIO Mixed Gas',
    pageTitle: 'Política de Privacidad',
    lastUpdated: 'Última actualización: 25 de mayo de 2026',
    nav: { home:'Inicio', howItWorks:'Cómo Funciona', advantages:'Ventajas', parameters:'Parámetros', samples:'Muestras', references:'Referencias', blog:'Blog', contact:'Contacto' },
    s1t: '1. Quiénes Somos',
    s1p: 'EUCHIO Mixed Gas es una serie de tecnología de corte con gas mixto operada por Jinan Euchio Machinery Co., Ltd. Nuestro sitio web es <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Qué Datos Recopilamos',
    s2p: 'Recopilamos la siguiente información cuando utiliza nuestro sitio web:',
    s2l1: '<strong>Envíos de formulario de contacto</strong> — nombre, dirección de correo electrónico, número de teléfono, nombre de la empresa y cualquier contenido de mensaje que elija proporcionar. Estos datos se procesan a través de Web3Forms y se nos envían directamente por correo electrónico.',
    s2l2: '<strong>Datos analíticos</strong> — utilizamos Google Analytics 4 (GA4) para comprender cómo los visitantes usan nuestro sitio. Esto incluye páginas visitadas, tiempo en el sitio, región geográfica (nivel país/ciudad), tipo de dispositivo y fuente de referencia. GA4 no recopila su dirección IP completa.',
    s2l3: '<strong>Registros del servidor</strong> — nuestro proveedor de alojamiento (Cloudflare) recopila automáticamente registros básicos de acceso, incluidas direcciones IP anonimizadas, tipo de navegador y marcas de tiempo para monitoreo de seguridad y rendimiento.',
    s3t: '3. Cómo Usamos Sus Datos',
    s3p: 'Usamos los datos recopilados solo para estos fines:',
    s3l1: 'Responder a sus consultas enviadas a través de nuestro formulario de contacto',
    s3l2: 'Comprender el tráfico del sitio web y mejorar nuestro contenido (analítica)',
    s3l3: 'Garantizar la seguridad del sitio web y prevenir abusos',
    s3noshare: 'No vendemos, alquilamos ni compartimos sus datos personales con terceros para sus fines de marketing.',
    s4t: '4. Cookies',
    s4p1: 'Google Analytics utiliza cookies propias para distinguir a los usuarios. Estas cookies no almacenan información de identificación personal. Puede desactivar las cookies en la configuración de su navegador u optar por no participar en Google Analytics utilizando el <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Complemento de inhabilitación de Google Analytics</a>.',
    s4p2: 'Nuestro sitio web no utiliza cookies publicitarias, píxeles de seguimiento ni cookies de marketing de terceros.',
    s5t: '5. Base Legal (GDPR)',
    s5p: 'Para los visitantes del Espacio Económico Europeo (EEE), procesamos sus datos sobre las siguientes bases legales:',
    s5l1: '<strong>Interés legítimo</strong> — datos analíticos para mejorar nuestro sitio web y servicios.',
    s5l2: '<strong>Consentimiento</strong> — datos del formulario de contacto, que usted proporciona voluntariamente al enviar una consulta.',
    s6t: '6. Retención de Datos',
    s6p: 'Las consultas del formulario de contacto se conservan en nuestro sistema de correo electrónico durante la duración de la relación comercial más 2 años. Los datos de Google Analytics se conservan durante 14 meses. Los registros de Cloudflare se conservan durante 24 horas.',
    s7t: '7. Sus Derechos',
    s7p: 'Usted tiene derecho a:',
    s7l1: 'Solicitar acceso a los datos personales que tenemos sobre usted',
    s7l2: 'Solicitar la corrección o eliminación de sus datos',
    s7l3: 'Retirar el consentimiento en cualquier momento (para datos del formulario de contacto)',
    s7l4: 'Oponerse al procesamiento de datos analíticos',
    s7contact: 'Para ejercer cualquiera de estos derechos, contáctenos en <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Servicios de Terceros',
    s8p: 'Utilizamos los siguientes servicios de terceros que pueden procesar sus datos:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, EE. UU.) — analítica web. Google está certificado bajo el Marco de Privacidad de Datos UE-EE. UU.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., EE. UU.) — alojamiento y seguridad web. Cloudflare está certificado bajo el Marco de Privacidad de Datos UE-EE. UU.',
    s8l3: '<strong>Web3Forms</strong> — entrega de formularios de contacto. Los envíos de formularios se envían directamente a nuestro correo electrónico.',
    s9t: '9. Contacto',
    s9p: 'Si tiene preguntas sobre esta política de privacidad o desea ejercer sus derechos de datos, contáctenos:',
    s9email: 'Correo electrónico',
    s9phone: 'Teléfono',
    s9addr: 'Dirección: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, China',
    footerTagline: 'Tecnología de Gas Mixto',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Producto',
    footerHow: 'Cómo Funciona',
    footerAdv: 'Ventajas',
    footerParams: 'Parámetros',
    footerSamples: 'Muestras de Corte',
    footerBlog: 'Blog',
    footerContact: 'Contacto',
    footerWA_MX: 'WhatsApp (México)',
    footerWA_TH: 'WhatsApp (Tailandia)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Todos los derechos reservados.',
    footerPrivacy: 'Política de Privacidad',
    footerLinkedIn: 'LinkedIn'
  },

  ko: {
    metaDesc: 'EUCHIO Mixed Gas 개인정보처리방침 — 당사가 귀하의 개인 데이터를 수집, 사용 및 보호하는 방법.',
    title: '개인정보처리방침 | EUCHIO Mixed Gas',
    pageTitle: '개인정보처리방침',
    lastUpdated: '최종 업데이트: 2026년 5월 25일',
    nav: { home:'홈', howItWorks:'작동 원리', advantages:'장점', parameters:'사양', samples:'절단 샘플', references:'참조', blog:'블로그', contact:'문의' },
    s1t: '1. 당사 소개',
    s1p: 'EUCHIO Mixed Gas는 Jinan Euchio Machinery Co., Ltd.가 운영하는 혼합 가스 절단 기술 시리즈입니다. 당사 웹사이트는 <a href="https://gasmixtech.com">gasmixtech.com</a>입니다.',
    s2t: '2. 수집하는 데이터',
    s2p: '귀하가 당사 웹사이트를 이용할 때 다음 정보를 수집합니다:',
    s2l1: '<strong>문의 양식 제출</strong> — 이름, 이메일 주소, 전화번호, 회사명 및 귀하가 제공하기로 선택한 메시지 내용. 이 데이터는 Web3Forms를 통해 처리되며 이메일로 당사에 직접 전송됩니다.',
    s2l2: '<strong>분석 데이터</strong> — Google Analytics 4(GA4)를 사용하여 방문자의 사이트 이용 방식을 이해합니다. 여기에는 방문 페이지, 사이트 체류 시간, 지리적 지역(국가/도시 수준), 기기 유형 및 추천 소스가 포함됩니다. GA4는 전체 IP 주소를 수집하지 않습니다.',
    s2l3: '<strong>서버 로그</strong> — 호스팅 제공업체(Cloudflare)가 보안 및 성능 모니터링을 위해 익명화된 IP 주소, 브라우저 유형 및 타임스탬프를 포함한 기본 액세스 로그를 자동으로 수집합니다.',
    s3t: '3. 데이터 사용 방법',
    s3p: '수집된 데이터는 다음 목적으로만 사용됩니다:',
    s3l1: '문의 양식을 통해 제출된 귀하의 문의에 응답',
    s3l2: '웹사이트 트래픽 이해 및 콘텐츠 개선 (분석)',
    s3l3: '웹사이트 보안 보장 및 남용 방지',
    s3noshare: '당사는 귀하의 개인 데이터를 제3자의 마케팅 목적으로 판매, 임대 또는 공유하지 않습니다.',
    s4t: '4. 쿠키',
    s4p1: 'Google Analytics는 사용자를 구별하기 위해 자사 쿠키를 사용합니다. 이 쿠키는 개인 식별 정보를 저장하지 않습니다. 브라우저 설정에서 쿠키를 비활성화하거나 <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics 선택 해제 브라우저 추가 기능</a>을 사용하여 Google Analytics를 완전히 선택 해제할 수 있습니다.',
    s4p2: '당사 웹사이트는 광고 쿠키, 추적 픽셀 또는 제3자 마케팅 쿠키를 사용하지 않습니다.',
    s5t: '5. 법적 근거 (GDPR)',
    s5p: '유럽 경제 지역(EEA) 방문자의 경우, 당사는 다음 법적 근거에 따라 귀하의 데이터를 처리합니다:',
    s5l1: '<strong>정당한 이익</strong> — 웹사이트 및 서비스 개선을 위한 분석 데이터.',
    s5l2: '<strong>동의</strong> — 문의 제출 시 귀하가 자발적으로 제공하는 문의 양식 데이터.',
    s6t: '6. 데이터 보관',
    s6p: '문의 양식 문의는 비즈니스 관계 기간 + 2년 동안 이메일 시스템에 보관됩니다. Google Analytics 데이터는 14개월간 보관됩니다. Cloudflare 로그는 24시간 동안 보관됩니다.',
    s7t: '7. 귀하의 권리',
    s7p: '귀하는 다음과 같은 권리가 있습니다:',
    s7l1: '당사가 보유한 귀하의 개인 데이터에 대한 액세스 요청',
    s7l2: '데이터의 정정 또는 삭제 요청',
    s7l3: '언제든지 동의 철회 (문의 양식 데이터의 경우)',
    s7l4: '분석 데이터 처리에 대한 이의 제기',
    s7contact: '이러한 권리를 행사하려면 <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>으로 문의하십시오.',
    s8t: '8. 제3자 서비스',
    s8p: '당사는 귀하의 데이터를 처리할 수 있는 다음 제3자 서비스를 사용합니다:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, 미국) — 웹사이트 분석. Google은 EU-US 데이터 프라이버시 프레임워크에 따라 인증되었습니다.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., 미국) — 웹사이트 호스팅 및 보안. Cloudflare는 EU-US 데이터 프라이버시 프레임워크에 따라 인증되었습니다.',
    s8l3: '<strong>Web3Forms</strong> — 문의 양식 전달. 양식 제출은 당사 이메일로 직접 전송됩니다.',
    s9t: '9. 연락처',
    s9p: '본 개인정보처리방침에 대해 질문이 있거나 데이터 권리를 행사하려면 당사에 문의하십시오:',
    s9email: '이메일',
    s9phone: '전화',
    s9addr: '주소: Jinan Euchio Machinery Co., Ltd., 중국 산둥성 지난시',
    footerTagline: '가스 혼합 기술',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: '제품',
    footerHow: '작동 원리',
    footerAdv: '장점',
    footerParams: '사양',
    footerSamples: '절단 샘플',
    footerBlog: '블로그',
    footerContact: '문의',
    footerWA_MX: 'WhatsApp (멕시코)',
    footerWA_TH: 'WhatsApp (태국)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. All rights reserved.',
    footerPrivacy: '개인정보처리방침',
    footerLinkedIn: 'LinkedIn'
  },

  ja: {
    metaDesc: 'EUCHIO Mixed Gas プライバシーポリシー — 個人データの収集、使用、保護について。',
    title: 'プライバシーポリシー | EUCHIO Mixed Gas',
    pageTitle: 'プライバシーポリシー',
    lastUpdated: '最終更新：2026年5月25日',
    nav: { home:'ホーム', howItWorks:'仕組み', advantages:'利点', parameters:'仕様', samples:'切断サンプル', references:'導入事例', blog:'ブログ', contact:'お問い合わせ' },
    s1t: '1. 運営者情報',
    s1p: 'EUCHIO Mixed GasはJinan Euchio Machinery Co., Ltd.が運営する混合ガス切断技術シリーズです。当社のウェブサイトは <a href="https://gasmixtech.com">gasmixtech.com</a> です。',
    s2t: '2. 収集するデータ',
    s2p: '当社は、お客様が当社ウェブサイトを利用する際に以下の情報を収集します：',
    s2l1: '<strong>お問い合わせフォームの送信</strong> — 氏名、メールアドレス、電話番号、会社名、およびお客様が提供を選択したメッセージ内容。このデータはWeb3Formsを通じて処理され、メールで直接当社に送信されます。',
    s2l2: '<strong>分析データ</strong> — Google Analytics 4（GA4）を使用して、訪問者のサイト利用状況を把握しています。これには、訪問ページ、サイト滞在時間、地理的地域（国/都市レベル）、デバイスタイプ、参照元が含まれます。GA4は完全なIPアドレスを収集しません。',
    s2l3: '<strong>サーバーログ</strong> — ホスティングプロバイダー（Cloudflare）が、セキュリティとパフォーマンス監視のため、匿名化されたIPアドレス、ブラウザタイプ、タイムスタンプを含む基本的なアクセスログを自動的に収集します。',
    s3t: '3. データの利用目的',
    s3p: '収集したデータは以下の目的にのみ使用します：',
    s3l1: 'お問い合わせフォームから送信されたお問い合わせへの対応',
    s3l2: 'ウェブサイトのトラフィック把握とコンテンツ改善（分析）',
    s3l3: 'ウェブサイトのセキュリティ確保と不正利用防止',
    s3noshare: '当社は、お客様の個人データを第三者のマーケティング目的で販売、貸与、共有することはありません。',
    s4t: '4. Cookie',
    s4p1: 'Google Analyticsはユーザーを区別するためにファーストパーティCookieを使用します。これらのCookieは個人を特定できる情報を保存しません。ブラウザ設定でCookieを無効にするか、<a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analyticsオプトアウトブラウザアドオン</a>を使用してGoogle Analyticsを完全にオプトアウトできます。',
    s4p2: '当社のウェブサイトは、広告Cookie、トラッキングピクセル、または第三者のマーケティングCookieを使用していません。',
    s5t: '5. 法的根拠（GDPR）',
    s5p: '欧州経済領域（EEA）からの訪問者について、当社は以下の法的根拠に基づいてデータを処理します：',
    s5l1: '<strong>正当な利益</strong> — ウェブサイトとサービスを改善するための分析データ。',
    s5l2: '<strong>同意</strong> — お問い合わせフォームのデータ。お客様がお問い合わせを送信する際に自発的に提供するものです。',
    s6t: '6. データ保持期間',
    s6p: 'お問い合わせフォームの内容は、ビジネス関係の期間＋2年間、メールシステムに保持されます。Google Analyticsデータは14か月間保持されます。Cloudflareログは24時間保持されます。',
    s7t: '7. お客様の権利',
    s7p: 'お客様には以下の権利があります：',
    s7l1: '当社が保持するお客様の個人データへのアクセスを要求する',
    s7l2: 'データの訂正または削除を要求する',
    s7l3: 'いつでも同意を撤回する（お問い合わせフォームデータについて）',
    s7l4: '分析データ処理に異議を唱える',
    s7contact: 'これらの権利を行使するには、<a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a> までご連絡ください。',
    s8t: '8. 第三者サービス',
    s8p: '当社は、お客様のデータを処理する可能性のある以下の第三者サービスを利用しています：',
    s8l1: '<strong>Google Analytics</strong>（Google LLC、米国）— ウェブサイト分析。GoogleはEU-USデータプライバシーフレームワークの認証を受けています。',
    s8l2: '<strong>Cloudflare</strong>（Cloudflare, Inc.、米国）— ウェブサイトのホスティングとセキュリティ。CloudflareはEU-USデータプライバシーフレームワークの認証を受けています。',
    s8l3: '<strong>Web3Forms</strong> — お問い合わせフォームの配信。フォーム送信内容は直接当社のメールに送信されます。',
    s9t: '9. お問い合わせ',
    s9p: '本プライバシーポリシーに関するご質問やデータ権利の行使をご希望の場合は、当社までご連絡ください：',
    s9email: 'メール',
    s9phone: '電話',
    s9addr: '住所：Jinan Euchio Machinery Co., Ltd., 中国山東省済南市',
    footerTagline: 'ガス混合技術',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: '製品',
    footerHow: '仕組み',
    footerAdv: '利点',
    footerParams: '仕様',
    footerSamples: '切断サンプル',
    footerBlog: 'ブログ',
    footerContact: 'お問い合わせ',
    footerWA_MX: 'WhatsApp（メキシコ）',
    footerWA_TH: 'WhatsApp（タイ）',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. All rights reserved.',
    footerPrivacy: 'プライバシーポリシー',
    footerLinkedIn: 'LinkedIn'
  },

  pt: {
    metaDesc: 'Política de Privacidade da EUCHIO Mixed Gas — como coletamos, usamos e protegemos seus dados pessoais.',
    title: 'Política de Privacidade | EUCHIO Mixed Gas',
    pageTitle: 'Política de Privacidade',
    lastUpdated: 'Última atualização: 25 de maio de 2026',
    nav: { home:'Início', howItWorks:'Como Funciona', advantages:'Vantagens', parameters:'Parâmetros', samples:'Amostras', references:'Referências', blog:'Blog', contact:'Contato' },
    s1t: '1. Quem Somos',
    s1p: 'EUCHIO Mixed Gas é uma série de tecnologia de corte com gás misto operada pela Jinan Euchio Machinery Co., Ltd. Nosso site é <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Quais Dados Coletamos',
    s2p: 'Coletamos as seguintes informações quando você usa nosso site:',
    s2l1: '<strong>Envios do formulário de contato</strong> — nome, endereço de e-mail, número de telefone, nome da empresa e qualquer conteúdo de mensagem que você optar por fornecer. Esses dados são processados via Web3Forms e enviados diretamente para nós por e-mail.',
    s2l2: '<strong>Dados analíticos</strong> — usamos o Google Analytics 4 (GA4) para entender como os visitantes usam nosso site. Isso inclui páginas visitadas, tempo no site, região geográfica (nível país/cidade), tipo de dispositivo e fonte de referência. O GA4 não coleta seu endereço IP completo.',
    s2l3: '<strong>Logs do servidor</strong> — nosso provedor de hospedagem (Cloudflare) coleta automaticamente logs básicos de acesso, incluindo endereços IP anonimizados, tipo de navegador e registros de data/hora para monitoramento de segurança e desempenho.',
    s3t: '3. Como Usamos Seus Dados',
    s3p: 'Usamos os dados coletados apenas para estas finalidades:',
    s3l1: 'Responder às suas consultas enviadas através do nosso formulário de contato',
    s3l2: 'Compreender o tráfego do site e melhorar nosso conteúdo (analítica)',
    s3l3: 'Garantir a segurança do site e prevenir abusos',
    s3noshare: 'Não vendemos, alugamos ou compartilhamos seus dados pessoais com terceiros para fins de marketing.',
    s4t: '4. Cookies',
    s4p1: 'O Google Analytics usa cookies próprios para distinguir os usuários. Esses cookies não armazenam informações de identificação pessoal. Você pode desativar os cookies nas configurações do seu navegador ou optar por não participar do Google Analytics usando o <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Complemento de Desativação do Google Analytics</a>.',
    s4p2: 'Nosso site não usa cookies de publicidade, pixels de rastreamento ou cookies de marketing de terceiros.',
    s5t: '5. Base Legal (GDPR)',
    s5p: 'Para visitantes do Espaço Econômico Europeu (EEE), processamos seus dados nas seguintes bases legais:',
    s5l1: '<strong>Interesse legítimo</strong> — dados analíticos para melhorar nosso site e serviços.',
    s5l2: '<strong>Consentimento</strong> — dados do formulário de contato, que você fornece voluntariamente ao enviar uma consulta.',
    s6t: '6. Retenção de Dados',
    s6p: 'As consultas do formulário de contato são mantidas em nosso sistema de e-mail durante a relação comercial mais 2 anos. Os dados do Google Analytics são mantidos por 14 meses. Os logs do Cloudflare são mantidos por 24 horas.',
    s7t: '7. Seus Direitos',
    s7p: 'Você tem o direito de:',
    s7l1: 'Solicitar acesso aos dados pessoais que mantemos sobre você',
    s7l2: 'Solicitar a correção ou exclusão dos seus dados',
    s7l3: 'Retirar o consentimento a qualquer momento (para dados do formulário de contato)',
    s7l4: 'Opor-se ao processamento de dados analíticos',
    s7contact: 'Para exercer qualquer um desses direitos, entre em contato conosco em <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Serviços de Terceiros',
    s8p: 'Usamos os seguintes serviços de terceiros que podem processar seus dados:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, EUA) — analítica do site. O Google é certificado sob o EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., EUA) — hospedagem e segurança do site. A Cloudflare é certificada sob o EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — entrega do formulário de contato. Os envios do formulário são enviados diretamente para nosso e-mail.',
    s9t: '9. Contato',
    s9p: 'Se você tiver dúvidas sobre esta política de privacidade ou desejar exercer seus direitos de dados, entre em contato conosco:',
    s9email: 'E-mail',
    s9phone: 'Telefone',
    s9addr: 'Endereço: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, China',
    footerTagline: 'Tecnologia de Mistura de Gases',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Produto',
    footerHow: 'Como Funciona',
    footerAdv: 'Vantagens',
    footerParams: 'Parâmetros',
    footerSamples: 'Amostras de Corte',
    footerBlog: 'Blog',
    footerContact: 'Contato',
    footerWA_MX: 'WhatsApp (México)',
    footerWA_TH: 'WhatsApp (Tailândia)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Todos os direitos reservados.',
    footerPrivacy: 'Política de Privacidade',
    footerLinkedIn: 'LinkedIn'
  },

  de: {
    metaDesc: 'Datenschutzerklärung von EUCHIO Mixed Gas — wie wir Ihre personenbezogenen Daten erfassen, verwenden und schützen.',
    title: 'Datenschutzerklärung | EUCHIO Mixed Gas',
    pageTitle: 'Datenschutzerklärung',
    lastUpdated: 'Zuletzt aktualisiert: 25. Mai 2026',
    nav: { home:'Startseite', howItWorks:'Funktionsweise', advantages:'Vorteile', parameters:'Parameter', samples:'Schnittmuster', references:'Referenzen', blog:'Blog', contact:'Kontakt' },
    s1t: '1. Wer Wir Sind',
    s1p: 'EUCHIO Mixed Gas ist eine von Jinan Euchio Machinery Co., Ltd. betriebene Mischgas-Schneidtechnologie-Serie. Unsere Website ist <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Welche Daten Wir Erfassen',
    s2p: 'Wir erfassen die folgenden Informationen, wenn Sie unsere Website nutzen:',
    s2l1: '<strong>Kontaktformular-Übermittlungen</strong> — Name, E-Mail-Adresse, Telefonnummer, Firmenname und alle Nachrichteninhalte, die Sie uns mitteilen möchten. Diese Daten werden über Web3Forms verarbeitet und direkt per E-Mail an uns gesendet.',
    s2l2: '<strong>Analysedaten</strong> — wir verwenden Google Analytics 4 (GA4), um zu verstehen, wie Besucher unsere Website nutzen. Dies umfasst besuchte Seiten, Verweildauer, geografische Region (Land/Stadt), Gerätetyp und Verweisquelle. GA4 erfasst Ihre vollständige IP-Adresse nicht.',
    s2l3: '<strong>Server-Logs</strong> — unser Hosting-Anbieter (Cloudflare) erfasst automatisch grundlegende Zugriffsprotokolle, einschließlich anonymisierter IP-Adressen, Browsertyp und Zeitstempel für Sicherheits- und Leistungsüberwachung.',
    s3t: '3. Wie Wir Ihre Daten Verwenden',
    s3p: 'Wir verwenden die erfassten Daten ausschließlich für folgende Zwecke:',
    s3l1: 'Beantwortung Ihrer Anfragen, die über unser Kontaktformular eingehen',
    s3l2: 'Verständnis des Website-Traffics und Verbesserung unserer Inhalte (Analyse)',
    s3l3: 'Gewährleistung der Website-Sicherheit und Verhinderung von Missbrauch',
    s3noshare: 'Wir verkaufen, vermieten oder teilen Ihre personenbezogenen Daten nicht mit Dritten für deren Marketingzwecke.',
    s4t: '4. Cookies',
    s4p1: 'Google Analytics verwendet Erstanbieter-Cookies zur Unterscheidung der Nutzer. Diese Cookies speichern keine personenbezogenen Daten. Sie können Cookies in Ihren Browsereinstellungen deaktivieren oder Google Analytics vollständig mit dem <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics Opt-out Browser-Add-on</a> deaktivieren.',
    s4p2: 'Unsere Website verwendet keine Werbe-Cookies, Tracking-Pixel oder Marketing-Cookies von Drittanbietern.',
    s5t: '5. Rechtsgrundlage (DSGVO)',
    s5p: 'Für Besucher aus dem Europäischen Wirtschaftsraum (EWR) verarbeiten wir Ihre Daten auf folgenden Rechtsgrundlagen:',
    s5l1: '<strong>Berechtigtes Interesse</strong> — Analysedaten zur Verbesserung unserer Website und Dienste.',
    s5l2: '<strong>Einwilligung</strong> — Kontaktformulardaten, die Sie bei der Übermittlung einer Anfrage freiwillig angeben.',
    s6t: '6. Datenspeicherung',
    s6p: 'Kontaktformular-Anfragen werden für die Dauer der Geschäftsbeziehung plus 2 Jahre in unserem E-Mail-System gespeichert. Google Analytics-Daten werden 14 Monate gespeichert. Cloudflare-Protokolle werden 24 Stunden gespeichert.',
    s7t: '7. Ihre Rechte',
    s7p: 'Sie haben das Recht auf:',
    s7l1: 'Auskunft über die von uns gespeicherten personenbezogenen Daten',
    s7l2: 'Berichtigung oder Löschung Ihrer Daten',
    s7l3: 'Jederzeitigen Widerruf der Einwilligung (für Kontaktformulardaten)',
    s7l4: 'Widerspruch gegen die Verarbeitung von Analysedaten',
    s7contact: 'Um diese Rechte auszuüben, kontaktieren Sie uns unter <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Drittanbieter-Dienste',
    s8p: 'Wir nutzen folgende Drittanbieter-Dienste, die Ihre Daten verarbeiten können:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, USA) — Website-Analyse. Google ist nach dem EU-US Data Privacy Framework zertifiziert.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., USA) — Website-Hosting und Sicherheit. Cloudflare ist nach dem EU-US Data Privacy Framework zertifiziert.',
    s8l3: '<strong>Web3Forms</strong> — Kontaktformular-Zustellung. Formularübermittlungen werden direkt an unsere E-Mail gesendet.',
    s9t: '9. Kontakt',
    s9p: 'Wenn Sie Fragen zu dieser Datenschutzerklärung haben oder Ihre Datenschutzrechte ausüben möchten, kontaktieren Sie uns:',
    s9email: 'E-Mail',
    s9phone: 'Telefon',
    s9addr: 'Adresse: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, China',
    footerTagline: 'Mischgastechnologie',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Produkt',
    footerHow: 'Funktionsweise',
    footerAdv: 'Vorteile',
    footerParams: 'Parameter',
    footerSamples: 'Schnittmuster',
    footerBlog: 'Blog',
    footerContact: 'Kontakt',
    footerWA_MX: 'WhatsApp (Mexiko)',
    footerWA_TH: 'WhatsApp (Thailand)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Alle Rechte vorbehalten.',
    footerPrivacy: 'Datenschutzerklärung',
    footerLinkedIn: 'LinkedIn'
  },

  fr: {
    metaDesc: 'Politique de confidentialité de EUCHIO Mixed Gas — comment nous collectons, utilisons et protégeons vos données personnelles.',
    title: 'Politique de Confidentialité | EUCHIO Mixed Gas',
    pageTitle: 'Politique de Confidentialité',
    lastUpdated: 'Dernière mise à jour : 25 mai 2026',
    nav: { home:'Accueil', howItWorks:'Fonctionnement', advantages:'Avantages', parameters:'Paramètres', samples:'Échantillons', references:'Références', blog:'Blog', contact:'Contact' },
    s1t: '1. Qui Nous Sommes',
    s1p: 'EUCHIO Mixed Gas est une série de technologie de coupe au gaz mixte exploitée par Jinan Euchio Machinery Co., Ltd. Notre site Web est <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Quelles Données Nous Collectons',
    s2p: 'Nous collectons les informations suivantes lorsque vous utilisez notre site Web :',
    s2l1: '<strong>Soumissions du formulaire de contact</strong> — nom, adresse e-mail, numéro de téléphone, nom de l\'entreprise et tout contenu de message que vous choisissez de fournir. Ces données sont traitées via Web3Forms et nous sont envoyées directement par e-mail.',
    s2l2: '<strong>Données analytiques</strong> — nous utilisons Google Analytics 4 (GA4) pour comprendre comment les visiteurs utilisent notre site. Cela inclut les pages visitées, le temps passé sur le site, la région géographique (niveau pays/ville), le type d\'appareil et la source de référence. GA4 ne collecte pas votre adresse IP complète.',
    s2l3: '<strong>Journaux du serveur</strong> — notre hébergeur (Cloudflare) collecte automatiquement des journaux d\'accès de base, y compris les adresses IP anonymisées, le type de navigateur et les horodatages pour la surveillance de la sécurité et des performances.',
    s3t: '3. Comment Nous Utilisons Vos Données',
    s3p: 'Nous utilisons les données collectées uniquement à ces fins :',
    s3l1: 'Répondre à vos demandes soumises via notre formulaire de contact',
    s3l2: 'Comprendre le trafic du site Web et améliorer notre contenu (analyse)',
    s3l3: 'Assurer la sécurité du site Web et prévenir les abus',
    s3noshare: 'Nous ne vendons, ne louons ni ne partageons vos données personnelles avec des tiers à des fins de marketing.',
    s4t: '4. Cookies',
    s4p1: 'Google Analytics utilise des cookies propriétaires pour distinguer les utilisateurs. Ces cookies ne stockent pas d\'informations personnellement identifiables. Vous pouvez désactiver les cookies dans les paramètres de votre navigateur ou désactiver complètement Google Analytics en utilisant le <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Module complémentaire de désactivation de Google Analytics</a>.',
    s4p2: 'Notre site Web n\'utilise pas de cookies publicitaires, de pixels de suivi ou de cookies marketing tiers.',
    s5t: '5. Base Légale (RGPD)',
    s5p: 'Pour les visiteurs de l\'Espace Économique Européen (EEE), nous traitons vos données sur les bases légales suivantes :',
    s5l1: '<strong>Intérêt légitime</strong> — données analytiques pour améliorer notre site Web et nos services.',
    s5l2: '<strong>Consentement</strong> — données du formulaire de contact, que vous fournissez volontairement lors de l\'envoi d\'une demande.',
    s6t: '6. Conservation des Données',
    s6p: 'Les demandes du formulaire de contact sont conservées dans notre système de messagerie pendant la durée de la relation commerciale plus 2 ans. Les données Google Analytics sont conservées pendant 14 mois. Les journaux Cloudflare sont conservés pendant 24 heures.',
    s7t: '7. Vos Droits',
    s7p: 'Vous avez le droit de :',
    s7l1: 'Demander l\'accès aux données personnelles que nous détenons à votre sujet',
    s7l2: 'Demander la correction ou la suppression de vos données',
    s7l3: 'Retirer votre consentement à tout moment (pour les données du formulaire de contact)',
    s7l4: 'Vous opposer au traitement des données analytiques',
    s7contact: 'Pour exercer l\'un de ces droits, contactez-nous à <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Services Tiers',
    s8p: 'Nous utilisons les services tiers suivants qui peuvent traiter vos données :',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, États-Unis) — analyse du site Web. Google est certifié en vertu du EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., États-Unis) — hébergement et sécurité du site Web. Cloudflare est certifié en vertu du EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — livraison du formulaire de contact. Les soumissions de formulaire sont envoyées directement à notre e-mail.',
    s9t: '9. Contact',
    s9p: 'Si vous avez des questions sur cette politique de confidentialité ou souhaitez exercer vos droits en matière de données, contactez-nous :',
    s9email: 'E-mail',
    s9phone: 'Téléphone',
    s9addr: 'Adresse : Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, Chine',
    footerTagline: 'Technologie de Gaz Mixte',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Produit',
    footerHow: 'Fonctionnement',
    footerAdv: 'Avantages',
    footerParams: 'Paramètres',
    footerSamples: 'Échantillons',
    footerBlog: 'Blog',
    footerContact: 'Contact',
    footerWA_MX: 'WhatsApp (Mexique)',
    footerWA_TH: 'WhatsApp (Thaïlande)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Tous droits réservés.',
    footerPrivacy: 'Politique de Confidentialité',
    footerLinkedIn: 'LinkedIn'
  },

  it: {
    metaDesc: 'Informativa sulla Privacy di EUCHIO Mixed Gas — come raccogliamo, utilizziamo e proteggiamo i tuoi dati personali.',
    title: 'Informativa sulla Privacy | EUCHIO Mixed Gas',
    pageTitle: 'Informativa sulla Privacy',
    lastUpdated: 'Ultimo aggiornamento: 25 maggio 2026',
    nav: { home:'Home', howItWorks:'Come Funziona', advantages:'Vantaggi', parameters:'Parametri', samples:'Campioni', references:'Referenze', blog:'Blog', contact:'Contatti' },
    s1t: '1. Chi Siamo',
    s1p: 'EUCHIO Mixed Gas è una serie di tecnologia di taglio a gas misto gestita da Jinan Euchio Machinery Co., Ltd. Il nostro sito Web è <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Quali Dati Raccogliamo',
    s2p: 'Raccogliamo le seguenti informazioni quando utilizzi il nostro sito Web:',
    s2l1: '<strong>Invii del modulo di contatto</strong> — nome, indirizzo e-mail, numero di telefono, nome dell\'azienda e qualsiasi contenuto del messaggio che scegli di fornire. Questi dati vengono elaborati tramite Web3Forms e inviati direttamente a noi via e-mail.',
    s2l2: '<strong>Dati analitici</strong> — utilizziamo Google Analytics 4 (GA4) per capire come i visitatori usano il nostro sito. Ciò include pagine visitate, tempo sul sito, area geografica (livello paese/città), tipo di dispositivo e fonte di riferimento. GA4 non raccoglie il tuo indirizzo IP completo.',
    s2l3: '<strong>Log del server</strong> — il nostro provider di hosting (Cloudflare) raccoglie automaticamente i log di accesso di base, inclusi indirizzi IP anonimizzati, tipo di browser e timestamp per il monitoraggio della sicurezza e delle prestazioni.',
    s3t: '3. Come Utilizziamo i Tuoi Dati',
    s3p: 'Utilizziamo i dati raccolti solo per questi scopi:',
    s3l1: 'Rispondere alle tue richieste inviate tramite il nostro modulo di contatto',
    s3l2: 'Comprendere il traffico del sito Web e migliorare i nostri contenuti (analisi)',
    s3l3: 'Garantire la sicurezza del sito Web e prevenire abusi',
    s3noshare: 'Non vendiamo, affittiamo o condividiamo i tuoi dati personali con terze parti per le loro finalità di marketing.',
    s4t: '4. Cookie',
    s4p1: 'Google Analytics utilizza cookie di prima parte per distinguere gli utenti. Questi cookie non memorizzano informazioni di identificazione personale. Puoi disabilitare i cookie nelle impostazioni del browser o disattivare completamente Google Analytics utilizzando il <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Componente aggiuntivo per la disattivazione di Google Analytics</a>.',
    s4p2: 'Il nostro sito Web non utilizza cookie pubblicitari, pixel di tracciamento o cookie di marketing di terze parti.',
    s5t: '5. Base Giuridica (GDPR)',
    s5p: 'Per i visitatori dello Spazio Economico Europeo (SEE), trattiamo i tuoi dati sulle seguenti basi giuridiche:',
    s5l1: '<strong>Legittimo interesse</strong> — dati analitici per migliorare il nostro sito Web e i nostri servizi.',
    s5l2: '<strong>Consenso</strong> — dati del modulo di contatto, che fornisci volontariamente quando invii una richiesta.',
    s6t: '6. Conservazione dei Dati',
    s6p: 'Le richieste del modulo di contatto vengono conservate nel nostro sistema di posta elettronica per la durata del rapporto commerciale più 2 anni. I dati di Google Analytics vengono conservati per 14 mesi. I log di Cloudflare vengono conservati per 24 ore.',
    s7t: '7. I Tuoi Diritti',
    s7p: 'Hai il diritto di:',
    s7l1: 'Richiedere l\'accesso ai dati personali che deteniamo su di te',
    s7l2: 'Richiedere la correzione o la cancellazione dei tuoi dati',
    s7l3: 'Revocare il consenso in qualsiasi momento (per i dati del modulo di contatto)',
    s7l4: 'Opporti al trattamento dei dati analitici',
    s7contact: 'Per esercitare uno qualsiasi di questi diritti, contattaci a <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Servizi di Terze Parti',
    s8p: 'Utilizziamo i seguenti servizi di terze parti che possono trattare i tuoi dati:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, USA) — analisi del sito Web. Google è certificato ai sensi dell\'EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., USA) — hosting e sicurezza del sito Web. Cloudflare è certificato ai sensi dell\'EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — consegna del modulo di contatto. Gli invii del modulo vengono inviati direttamente alla nostra e-mail.',
    s9t: '9. Contatti',
    s9p: 'Se hai domande su questa informativa sulla privacy o desideri esercitare i tuoi diritti sui dati, contattaci:',
    s9email: 'E-mail',
    s9phone: 'Telefono',
    s9addr: 'Indirizzo: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, Cina',
    footerTagline: 'Tecnologia del Gas Misto',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Prodotto',
    footerHow: 'Come Funziona',
    footerAdv: 'Vantaggi',
    footerParams: 'Parametri',
    footerSamples: 'Campioni di Taglio',
    footerBlog: 'Blog',
    footerContact: 'Contatti',
    footerWA_MX: 'WhatsApp (Messico)',
    footerWA_TH: 'WhatsApp (Thailandia)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Tutti i diritti riservati.',
    footerPrivacy: 'Informativa sulla Privacy',
    footerLinkedIn: 'LinkedIn'
  },

  nl: {
    metaDesc: 'Privacybeleid van EUCHIO Mixed Gas — hoe wij uw persoonlijke gegevens verzamelen, gebruiken en beschermen.',
    title: 'Privacybeleid | EUCHIO Mixed Gas',
    pageTitle: 'Privacybeleid',
    lastUpdated: 'Laatst bijgewerkt: 25 mei 2026',
    nav: { home:'Home', howItWorks:'Hoe Het Werkt', advantages:'Voordelen', parameters:'Parameters', samples:'Snijmonsters', references:'Referenties', blog:'Blog', contact:'Contact' },
    s1t: '1. Wie Wij Zijn',
    s1p: 'EUCHIO Mixed Gas is een menggas-snijtechnologieserie die wordt beheerd door Jinan Euchio Machinery Co., Ltd. Onze website is <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Welke Gegevens Wij Verzamelen',
    s2p: 'Wij verzamelen de volgende informatie wanneer u onze website gebruikt:',
    s2l1: '<strong>Inzendingen via contactformulier</strong> — naam, e-mailadres, telefoonnummer, bedrijfsnaam en eventuele berichtinhoud die u kiest te verstrekken. Deze gegevens worden verwerkt via Web3Forms en rechtstreeks per e-mail naar ons verzonden.',
    s2l2: '<strong>Analysegegevens</strong> — wij gebruiken Google Analytics 4 (GA4) om te begrijpen hoe bezoekers onze site gebruiken. Dit omvat bezochte pagina\'s, tijd op de site, geografische regio (land/stad), apparaattype en verwijzingsbron. GA4 verzamelt uw volledige IP-adres niet.',
    s2l3: '<strong>Serverlogs</strong> — onze hostingprovider (Cloudflare) verzamelt automatisch basis-toegangslogs, inclusief geanonimiseerde IP-adressen, browsertype en tijdstempels voor veiligheids- en prestatiebewaking.',
    s3t: '3. Hoe Wij Uw Gegevens Gebruiken',
    s3p: 'Wij gebruiken de verzamelde gegevens uitsluitend voor deze doeleinden:',
    s3l1: 'Beantwoorden van uw vragen ingediend via ons contactformulier',
    s3l2: 'Begrijpen van websiteverkeer en verbeteren van onze inhoud (analyse)',
    s3l3: 'Waarborgen van websitebeveiliging en voorkomen van misbruik',
    s3noshare: 'Wij verkopen, verhuren of delen uw persoonlijke gegevens niet met derden voor hun marketingdoeleinden.',
    s4t: '4. Cookies',
    s4p1: 'Google Analytics gebruikt first-party cookies om gebruikers te onderscheiden. Deze cookies slaan geen persoonlijk identificeerbare informatie op. U kunt cookies uitschakelen in uw browserinstellingen of Google Analytics volledig uitschakelen met de <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics Opt-out Browser Add-on</a>.',
    s4p2: 'Onze website gebruikt geen advertentiecookies, trackingpixels of marketingcookies van derden.',
    s5t: '5. Rechtsgrondslag (AVG/GDPR)',
    s5p: 'Voor bezoekers uit de Europese Economische Ruimte (EER) verwerken wij uw gegevens op de volgende rechtsgrondslagen:',
    s5l1: '<strong>Gerechtvaardigd belang</strong> — analysegegevens om onze website en diensten te verbeteren.',
    s5l2: '<strong>Toestemming</strong> — contactformuliergegevens, die u vrijwillig verstrekt bij het indienen van een vraag.',
    s6t: '6. Bewaartermijnen',
    s6p: 'Contactformuliervragen worden bewaard in ons e-mailsysteem voor de duur van de zakelijke relatie plus 2 jaar. Google Analytics-gegevens worden 14 maanden bewaard. Cloudflare-logs worden 24 uur bewaard.',
    s7t: '7. Uw Rechten',
    s7p: 'U heeft het recht om:',
    s7l1: 'Toegang te vragen tot de persoonlijke gegevens die wij over u bewaren',
    s7l2: 'Correctie of verwijdering van uw gegevens te vragen',
    s7l3: 'Uw toestemming op elk moment in te trekken (voor contactformuliergegevens)',
    s7l4: 'Bezwaar te maken tegen de verwerking van analysegegevens',
    s7contact: 'Om deze rechten uit te oefenen, neem contact met ons op via <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Diensten van Derden',
    s8p: 'Wij maken gebruik van de volgende diensten van derden die uw gegevens kunnen verwerken:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, VS) — website-analyse. Google is gecertificeerd onder het EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., VS) — websitehosting en beveiliging. Cloudflare is gecertificeerd onder het EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — bezorging van contactformulieren. Formulierinzendingen worden rechtstreeks naar onze e-mail verzonden.',
    s9t: '9. Contact',
    s9p: 'Als u vragen heeft over dit privacybeleid of uw gegevensrechten wilt uitoefenen, neem dan contact met ons op:',
    s9email: 'E-mail',
    s9phone: 'Telefoon',
    s9addr: 'Adres: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, China',
    footerTagline: 'Menggastechnologie',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Product',
    footerHow: 'Hoe Het Werkt',
    footerAdv: 'Voordelen',
    footerParams: 'Parameters',
    footerSamples: 'Snijmonsters',
    footerBlog: 'Blog',
    footerContact: 'Contact',
    footerWA_MX: 'WhatsApp (Mexico)',
    footerWA_TH: 'WhatsApp (Thailand)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Alle rechten voorbehouden.',
    footerPrivacy: 'Privacybeleid',
    footerLinkedIn: 'LinkedIn'
  },

  pl: {
    metaDesc: 'Polityka Prywatności EUCHIO Mixed Gas — jak zbieramy, wykorzystujemy i chronimy Twoje dane osobowe.',
    title: 'Polityka Prywatności | EUCHIO Mixed Gas',
    pageTitle: 'Polityka Prywatności',
    lastUpdated: 'Ostatnia aktualizacja: 25 maja 2026',
    nav: { home:'Strona Główna', howItWorks:'Jak To Działa', advantages:'Zalety', parameters:'Parametry', samples:'Próbki Cięcia', references:'Referencje', blog:'Blog', contact:'Kontakt' },
    s1t: '1. Kim Jesteśmy',
    s1p: 'EUCHIO Mixed Gas to seria technologii cięcia gazem mieszanym obsługiwana przez Jinan Euchio Machinery Co., Ltd. Nasza strona internetowa to <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Jakie Dane Zbieramy',
    s2p: 'Zbieramy następujące informacje podczas korzystania z naszej strony:',
    s2l1: '<strong>Zgłoszenia z formularza kontaktowego</strong> — imię i nazwisko, adres e-mail, numer telefonu, nazwa firmy oraz wszelkie treści wiadomości, które zdecydujesz się podać. Dane te są przetwarzane przez Web3Forms i wysyłane bezpośrednio do nas e-mailem.',
    s2l2: '<strong>Dane analityczne</strong> — używamy Google Analytics 4 (GA4), aby zrozumieć, w jaki sposób odwiedzający korzystają z naszej strony. Obejmuje to odwiedzane strony, czas spędzony na stronie, region geograficzny (kraj/miasto), typ urządzenia i źródło odesłania. GA4 nie zbiera pełnego adresu IP.',
    s2l3: '<strong>Logi serwera</strong> — nasz dostawca hostingu (Cloudflare) automatycznie zbiera podstawowe logi dostępu, w tym zanonimizowane adresy IP, typ przeglądarki i znaczniki czasu w celu monitorowania bezpieczeństwa i wydajności.',
    s3t: '3. Jak Wykorzystujemy Twoje Dane',
    s3p: 'Wykorzystujemy zebrane dane wyłącznie w następujących celach:',
    s3l1: 'Odpowiadanie na zapytania przesłane za pośrednictwem naszego formularza kontaktowego',
    s3l2: 'Zrozumienie ruchu na stronie i ulepszanie naszych treści (analityka)',
    s3l3: 'Zapewnienie bezpieczeństwa strony i zapobieganie nadużyciom',
    s3noshare: 'Nie sprzedajemy, nie wynajmujemy ani nie udostępniamy Twoich danych osobowych stronom trzecim do ich celów marketingowych.',
    s4t: '4. Pliki Cookie',
    s4p1: 'Google Analytics wykorzystuje własne pliki cookie do rozróżniania użytkowników. Te pliki cookie nie przechowują danych osobowych. Możesz wyłączyć pliki cookie w ustawieniach przeglądarki lub całkowicie zrezygnować z Google Analytics za pomocą <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Dodatku do przeglądarki wyłączającego Google Analytics</a>.',
    s4p2: 'Nasza strona nie wykorzystuje reklamowych plików cookie, pikseli śledzących ani marketingowych plików cookie stron trzecich.',
    s5t: '5. Podstawa Prawna (RODO)',
    s5p: 'Dla odwiedzających z Europejskiego Obszaru Gospodarczego (EOG) przetwarzamy Twoje dane na następujących podstawach prawnych:',
    s5l1: '<strong>Uzasadniony interes</strong> — dane analityczne w celu ulepszania naszej strony i usług.',
    s5l2: '<strong>Zgoda</strong> — dane z formularza kontaktowego, które podajesz dobrowolnie podczas wysyłania zapytania.',
    s6t: '6. Przechowywanie Danych',
    s6p: 'Zapytania z formularza kontaktowego są przechowywane w naszym systemie pocztowym przez okres trwania relacji biznesowej plus 2 lata. Dane Google Analytics są przechowywane przez 14 miesięcy. Logi Cloudflare są przechowywane przez 24 godziny.',
    s7t: '7. Twoje Prawa',
    s7p: 'Masz prawo do:',
    s7l1: 'Dostępu do swoich danych osobowych, które przechowujemy',
    s7l2: 'Sprostowania lub usunięcia swoich danych',
    s7l3: 'Wycofania zgody w dowolnym momencie (w przypadku danych z formularza kontaktowego)',
    s7l4: 'Sprzeciwu wobec przetwarzania danych analitycznych',
    s7contact: 'Aby skorzystać z tych praw, skontaktuj się z nami pod adresem <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Usługi Stron Trzecich',
    s8p: 'Korzystamy z następujących usług stron trzecich, które mogą przetwarzać Twoje dane:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, USA) — analityka strony. Google posiada certyfikat EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., USA) — hosting i bezpieczeństwo strony. Cloudflare posiada certyfikat EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — dostarczanie formularza kontaktowego. Zgłoszenia z formularza są wysyłane bezpośrednio na nasz e-mail.',
    s9t: '9. Kontakt',
    s9p: 'Jeśli masz pytania dotyczące niniejszej polityki prywatności lub chcesz skorzystać ze swoich praw dotyczących danych, skontaktuj się z nami:',
    s9email: 'E-mail',
    s9phone: 'Telefon',
    s9addr: 'Adres: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, Chiny',
    footerTagline: 'Technologia Gazu Mieszanego',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Produkt',
    footerHow: 'Jak To Działa',
    footerAdv: 'Zalety',
    footerParams: 'Parametry',
    footerSamples: 'Próbki Cięcia',
    footerBlog: 'Blog',
    footerContact: 'Kontakt',
    footerWA_MX: 'WhatsApp (Meksyk)',
    footerWA_TH: 'WhatsApp (Tajlandia)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Wszelkie prawa zastrzeżone.',
    footerPrivacy: 'Polityka Prywatności',
    footerLinkedIn: 'LinkedIn'
  },

  ru: {
    metaDesc: 'Политика конфиденциальности EUCHIO Mixed Gas — как мы собираем, используем и защищаем ваши персональные данные.',
    title: 'Политика Конфиденциальности | EUCHIO Mixed Gas',
    pageTitle: 'Политика Конфиденциальности',
    lastUpdated: 'Последнее обновление: 25 мая 2026 г.',
    nav: { home:'Главная', howItWorks:'Как Это Работает', advantages:'Преимущества', parameters:'Параметры', samples:'Образцы Резки', references:'Клиенты', blog:'Блог', contact:'Контакты' },
    s1t: '1. Кто Мы',
    s1p: 'EUCHIO Mixed Gas — серия технологий резки смешанным газом, управляемая Jinan Euchio Machinery Co., Ltd. Наш веб-сайт: <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Какие Данные Мы Собираем',
    s2p: 'Мы собираем следующую информацию при использовании вами нашего веб-сайта:',
    s2l1: '<strong>Отправки контактной формы</strong> — имя, адрес электронной почты, номер телефона, название компании и любое содержание сообщения, которое вы решите предоставить. Эти данные обрабатываются через Web3Forms и отправляются непосредственно нам по электронной почте.',
    s2l2: '<strong>Аналитические данные</strong> — мы используем Google Analytics 4 (GA4) для понимания того, как посетители используют наш сайт. Сюда входят посещенные страницы, время на сайте, географический регион (страна/город), тип устройства и источник перехода. GA4 не собирает ваш полный IP-адрес.',
    s2l3: '<strong>Серверные логи</strong> — наш хостинг-провайдер (Cloudflare) автоматически собирает базовые журналы доступа, включая анонимизированные IP-адреса, тип браузера и временные метки для мониторинга безопасности и производительности.',
    s3t: '3. Как Мы Используем Ваши Данные',
    s3p: 'Мы используем собранные данные только для следующих целей:',
    s3l1: 'Ответы на ваши запросы, отправленные через нашу контактную форму',
    s3l2: 'Понимание трафика веб-сайта и улучшение нашего контента (аналитика)',
    s3l3: 'Обеспечение безопасности веб-сайта и предотвращение злоупотреблений',
    s3noshare: 'Мы не продаем, не сдаем в аренду и не передаем ваши персональные данные третьим лицам для их маркетинговых целей.',
    s4t: '4. Файлы Cookie',
    s4p1: 'Google Analytics использует собственные файлы cookie для различения пользователей. Эти файлы cookie не хранят личную информацию. Вы можете отключить файлы cookie в настройках браузера или полностью отказаться от Google Analytics с помощью <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Надстройки для отказа от Google Analytics</a>.',
    s4p2: 'Наш веб-сайт не использует рекламные файлы cookie, отслеживающие пиксели или маркетинговые файлы cookie третьих лиц.',
    s5t: '5. Правовое Основание (GDPR)',
    s5p: 'Для посетителей из Европейской экономической зоны (ЕЭЗ) мы обрабатываем ваши данные на следующих правовых основаниях:',
    s5l1: '<strong>Законный интерес</strong> — аналитические данные для улучшения нашего веб-сайта и услуг.',
    s5l2: '<strong>Согласие</strong> — данные контактной формы, которые вы добровольно предоставляете при отправке запроса.',
    s6t: '6. Хранение Данных',
    s6p: 'Запросы через контактную форму хранятся в нашей почтовой системе в течение срока деловых отношений плюс 2 года. Данные Google Analytics хранятся 14 месяцев. Журналы Cloudflare хранятся 24 часа.',
    s7t: '7. Ваши Права',
    s7p: 'Вы имеете право:',
    s7l1: 'Запросить доступ к вашим персональным данным, которые мы храним',
    s7l2: 'Потребовать исправления или удаления ваших данных',
    s7l3: 'Отозвать согласие в любое время (для данных контактной формы)',
    s7l4: 'Возражать против обработки аналитических данных',
    s7contact: 'Для осуществления этих прав свяжитесь с нами по адресу <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Сторонние Сервисы',
    s8p: 'Мы используем следующие сторонние сервисы, которые могут обрабатывать ваши данные:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, США) — веб-аналитика. Google сертифицирован в соответствии с EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., США) — хостинг и безопасность веб-сайта. Cloudflare сертифицирован в соответствии с EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — доставка контактной формы. Отправки формы направляются непосредственно на нашу электронную почту.',
    s9t: '9. Контакты',
    s9p: 'Если у вас есть вопросы о данной политике конфиденциальности или вы хотите воспользоваться своими правами на данные, свяжитесь с нами:',
    s9email: 'Эл. почта',
    s9phone: 'Телефон',
    s9addr: 'Адрес: Jinan Euchio Machinery Co., Ltd., Цзинань, Шаньдун, Китай',
    footerTagline: 'Технология Смешанных Газов',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Продукт',
    footerHow: 'Как Это Работает',
    footerAdv: 'Преимущества',
    footerParams: 'Параметры',
    footerSamples: 'Образцы Резки',
    footerBlog: 'Блог',
    footerContact: 'Контакты',
    footerWA_MX: 'WhatsApp (Мексика)',
    footerWA_TH: 'WhatsApp (Таиланд)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Все права защищены.',
    footerPrivacy: 'Политика Конфиденциальности',
    footerLinkedIn: 'LinkedIn'
  },

  tr: {
    metaDesc: 'EUCHIO Mixed Gas Gizlilik Politikası — kişisel verilerinizi nasıl topladığımız, kullandığımız ve koruduğumuz.',
    title: 'Gizlilik Politikası | EUCHIO Mixed Gas',
    pageTitle: 'Gizlilik Politikası',
    lastUpdated: 'Son güncelleme: 25 Mayıs 2026',
    nav: { home:'Ana Sayfa', howItWorks:'Nasıl Çalışır', advantages:'Avantajlar', parameters:'Parametreler', samples:'Kesim Örnekleri', references:'Referanslar', blog:'Blog', contact:'İletişim' },
    s1t: '1. Biz Kimiz',
    s1p: 'EUCHIO Mixed Gas is a mixed gas cutting technology series operated by Jinan Euchio Machinery Co., Ltd. Our website is <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Hangi Verileri Topluyoruz',
    s2p: 'Web sitemizi kullandığınızda aşağıdaki bilgileri topluyoruz:',
    s2l1: '<strong>İletişim formu gönderimleri</strong> — ad, e-posta adresi, telefon numarası, şirket adı ve sağlamayı seçtiğiniz mesaj içeriği. Bu veriler Web3Forms aracılığıyla işlenir ve doğrudan bize e-posta ile gönderilir.',
    s2l2: '<strong>Analitik verileri</strong> — ziyaretçilerin sitemizi nasıl kullandığını anlamak için Google Analytics 4 (GA4) kullanıyoruz. Buna ziyaret edilen sayfalar, sitede geçirilen süre, coğrafi bölge (ülke/şehir düzeyi), cihaz türü ve yönlendirme kaynağı dahildir. GA4 tam IP adresinizi toplamaz.',
    s2l3: '<strong>Sunucu günlükleri</strong> — barındırma sağlayıcımız (Cloudflare), güvenlik ve performans izleme için anonimleştirilmiş IP adresleri, tarayıcı türü ve zaman damgaları dahil olmak üzere temel erişim günlüklerini otomatik olarak toplar.',
    s3t: '3. Verilerinizi Nasıl Kullanıyoruz',
    s3p: 'Toplanan verileri yalnızca şu amaçlarla kullanıyoruz:',
    s3l1: 'İletişim formumuz aracılığıyla gönderilen sorularınızı yanıtlamak',
    s3l2: 'Web sitesi trafiğini anlamak ve içeriğimizi geliştirmek (analitik)',
    s3l3: 'Web sitesi güvenliğini sağlamak ve kötüye kullanımı önlemek',
    s3noshare: 'Kişisel verilerinizi, kendi pazarlama amaçları için üçüncü taraflara satmıyor, kiralamıyor veya paylaşmıyoruz.',
    s4t: '4. Çerezler',
    s4p1: 'Google Analytics, kullanıcıları ayırt etmek için birinci taraf çerezleri kullanır. Bu çerezler kişisel olarak tanımlanabilir bilgiler saklamaz. Tarayıcı ayarlarınızdan çerezleri devre dışı bırakabilir veya <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics Devre Dışı Bırakma Tarayıcı Eklentisi</a>\'ni kullanarak Google Analytics\'ten tamamen çıkabilirsiniz.',
    s4p2: 'Web sitemiz reklam çerezleri, izleme pikselleri veya üçüncü taraf pazarlama çerezleri kullanmaz.',
    s5t: '5. Yasal Dayanak (GDPR)',
    s5p: 'Avrupa Ekonomik Alanı (AEA) ziyaretçileri için verilerinizi aşağıdaki yasal dayanaklara göre işliyoruz:',
    s5l1: '<strong>Meşru menfaat</strong> — web sitemizi ve hizmetlerimizi geliştirmek için analitik verileri.',
    s5l2: '<strong>Onay</strong> — bir soru gönderirken gönüllü olarak sağladığınız iletişim formu verileri.',
    s6t: '6. Veri Saklama',
    s6p: 'İletişim formu soruları, iş ilişkisi süresince artı 2 yıl boyunca e-posta sistemimizde saklanır. Google Analytics verileri 14 ay süreyle saklanır. Cloudflare günlükleri 24 saat süreyle saklanır.',
    s7t: '7. Haklarınız',
    s7p: 'Aşağıdaki haklara sahipsiniz:',
    s7l1: 'Hakkınızda tuttuğumuz kişisel verilere erişim talep etme',
    s7l2: 'Verilerinizin düzeltilmesini veya silinmesini talep etme',
    s7l3: 'İstediğiniz zaman onayınızı geri çekme (iletişim formu verileri için)',
    s7l4: 'Analitik veri işlemeye itiraz etme',
    s7contact: 'Bu haklardan herhangi birini kullanmak için <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a> adresinden bizimle iletişime geçin.',
    s8t: '8. Üçüncü Taraf Hizmetleri',
    s8p: 'Verilerinizi işleyebilecek aşağıdaki üçüncü taraf hizmetlerini kullanıyoruz:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, ABD) — web sitesi analitiği. Google, EU-US Data Privacy Framework kapsamında sertifikalıdır.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., ABD) — web sitesi barındırma ve güvenliği. Cloudflare, EU-US Data Privacy Framework kapsamında sertifikalıdır.',
    s8l3: '<strong>Web3Forms</strong> — iletişim formu iletimi. Form gönderimleri doğrudan e-postamıza gönderilir.',
    s9t: '9. İletişim',
    s9p: 'Bu gizlilik politikası hakkında sorularınız varsa veya veri haklarınızı kullanmak istiyorsanız, bizimle iletişime geçin:',
    s9email: 'E-posta',
    s9phone: 'Telefon',
    s9addr: 'Adres: Jinan Euchio Machinery Co., Ltd., Jinan, Shandong, Çin',
    footerTagline: 'Karma Gaz Teknolojisi',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Ürün',
    footerHow: 'Nasıl Çalışır',
    footerAdv: 'Avantajlar',
    footerParams: 'Parametreler',
    footerSamples: 'Kesim Örnekleri',
    footerBlog: 'Blog',
    footerContact: 'İletişim',
    footerWA_MX: 'WhatsApp (Meksika)',
    footerWA_TH: 'WhatsApp (Tayland)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Tüm hakları saklıdır.',
    footerPrivacy: 'Gizlilik Politikası',
    footerLinkedIn: 'LinkedIn'
  },

  vi: {
    metaDesc: 'Chính Sách Bảo Mật của EUCHIO Mixed Gas — cách chúng tôi thu thập, sử dụng và bảo vệ dữ liệu cá nhân của bạn.',
    title: 'Chính Sách Bảo Mật | EUCHIO Mixed Gas',
    pageTitle: 'Chính Sách Bảo Mật',
    lastUpdated: 'Cập nhật lần cuối: 25 tháng 5 năm 2026',
    nav: { home:'Trang Chủ', howItWorks:'Cơ Chế Hoạt Động', advantages:'Ưu Điểm', parameters:'Thông Số', samples:'Mẫu Cắt', references:'Khách Hàng', blog:'Blog', contact:'Liên Hệ' },
    s1t: '1. Chúng Tôi Là Ai',
    s1p: 'EUCHIO Mixed Gas is a mixed gas cutting technology series operated by Jinan Euchio Machinery Co., Ltd. Our website is <a href="https://gasmixtech.com">gasmixtech.com</a>.',
    s2t: '2. Dữ Liệu Chúng Tôi Thu Thập',
    s2p: 'Chúng tôi thu thập các thông tin sau khi bạn sử dụng trang web của chúng tôi:',
    s2l1: '<strong>Gửi biểu mẫu liên hệ</strong> — tên, địa chỉ email, số điện thoại, tên công ty và bất kỳ nội dung tin nhắn nào bạn chọn cung cấp. Dữ liệu này được xử lý qua Web3Forms và gửi trực tiếp cho chúng tôi qua email.',
    s2l2: '<strong>Dữ liệu phân tích</strong> — chúng tôi sử dụng Google Analytics 4 (GA4) để hiểu cách khách truy cập sử dụng trang web. Bao gồm các trang đã truy cập, thời gian trên trang, khu vực địa lý (cấp quốc gia/thành phố), loại thiết bị và nguồn giới thiệu. GA4 không thu thập địa chỉ IP đầy đủ của bạn.',
    s2l3: '<strong>Nhật ký máy chủ</strong> — nhà cung cấp dịch vụ lưu trữ của chúng tôi (Cloudflare) tự động thu thập nhật ký truy cập cơ bản bao gồm địa chỉ IP ẩn danh, loại trình duyệt và dấu thời gian để giám sát bảo mật và hiệu suất.',
    s3t: '3. Cách Chúng Tôi Sử Dụng Dữ Liệu',
    s3p: 'Chúng tôi chỉ sử dụng dữ liệu thu thập được cho các mục đích sau:',
    s3l1: 'Trả lời các yêu cầu của bạn được gửi qua biểu mẫu liên hệ',
    s3l2: 'Hiểu lưu lượng truy cập trang web và cải thiện nội dung (phân tích)',
    s3l3: 'Đảm bảo an ninh trang web và ngăn chặn lạm dụng',
    s3noshare: 'Chúng tôi không bán, cho thuê hoặc chia sẻ dữ liệu cá nhân của bạn với bên thứ ba cho mục đích tiếp thị của họ.',
    s4t: '4. Cookie',
    s4p1: 'Google Analytics sử dụng cookie bên thứ nhất để phân biệt người dùng. Các cookie này không lưu trữ thông tin nhận dạng cá nhân. Bạn có thể tắt cookie trong cài đặt trình duyệt hoặc từ chối hoàn toàn Google Analytics bằng <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Tiện ích Từ chối Google Analytics</a>.',
    s4p2: 'Trang web của chúng tôi không sử dụng cookie quảng cáo, pixel theo dõi hoặc cookie tiếp thị của bên thứ ba.',
    s5t: '5. Cơ Sở Pháp Lý (GDPR)',
    s5p: 'Đối với khách truy cập từ Khu vực Kinh tế Châu Âu (EEA), chúng tôi xử lý dữ liệu của bạn trên các cơ sở pháp lý sau:',
    s5l1: '<strong>Lợi ích hợp pháp</strong> — dữ liệu phân tích để cải thiện trang web và dịch vụ của chúng tôi.',
    s5l2: '<strong>Sự đồng ý</strong> — dữ liệu biểu mẫu liên hệ, được bạn tự nguyện cung cấp khi gửi yêu cầu.',
    s6t: '6. Lưu Trữ Dữ Liệu',
    s6p: 'Các yêu cầu qua biểu mẫu liên hệ được lưu trong hệ thống email của chúng tôi trong thời gian quan hệ kinh doanh cộng thêm 2 năm. Dữ liệu Google Analytics được lưu trữ trong 14 tháng. Nhật ký Cloudflare được lưu trữ trong 24 giờ.',
    s7t: '7. Quyền Của Bạn',
    s7p: 'Bạn có quyền:',
    s7l1: 'Yêu cầu truy cập dữ liệu cá nhân chúng tôi lưu giữ về bạn',
    s7l2: 'Yêu cầu chỉnh sửa hoặc xóa dữ liệu của bạn',
    s7l3: 'Rút lại sự đồng ý bất cứ lúc nào (đối với dữ liệu biểu mẫu liên hệ)',
    s7l4: 'Phản đối việc xử lý dữ liệu phân tích',
    s7contact: 'Để thực hiện bất kỳ quyền nào trong số này, hãy liên hệ với chúng tôi tại <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>.',
    s8t: '8. Dịch Vụ Bên Thứ Ba',
    s8p: 'Chúng tôi sử dụng các dịch vụ bên thứ ba sau có thể xử lý dữ liệu của bạn:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, Hoa Kỳ) — phân tích trang web. Google được chứng nhận theo EU-US Data Privacy Framework.',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., Hoa Kỳ) — lưu trữ và bảo mật trang web. Cloudflare được chứng nhận theo EU-US Data Privacy Framework.',
    s8l3: '<strong>Web3Forms</strong> — gửi biểu mẫu liên hệ. Các gửi biểu mẫu được gửi trực tiếp đến email của chúng tôi.',
    s9t: '9. Liên Hệ',
    s9p: 'Nếu bạn có câu hỏi về chính sách bảo mật này hoặc muốn thực hiện quyền dữ liệu của mình, hãy liên hệ với chúng tôi:',
    s9email: 'Email',
    s9phone: 'Điện thoại',
    s9addr: 'Địa chỉ: Jinan Euchio Machinery Co., Ltd., Tế Nam, Sơn Đông, Trung Quốc',
    footerTagline: 'Công Nghệ Khí Hỗn Hợp',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'Sản Phẩm',
    footerHow: 'Cơ Chế Hoạt Động',
    footerAdv: 'Ưu Điểm',
    footerParams: 'Thông Số',
    footerSamples: 'Mẫu Cắt',
    footerBlog: 'Blog',
    footerContact: 'Liên Hệ',
    footerWA_MX: 'WhatsApp (Mexico)',
    footerWA_TH: 'WhatsApp (Thái Lan)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. Bảo lưu mọi quyền.',
    footerPrivacy: 'Chính Sách Bảo Mật',
    footerLinkedIn: 'LinkedIn'
  },

  th: {
    metaDesc: 'นโยบายความเป็นส่วนตัวของ EUCHIO Mixed Gas — วิธีที่เราเก็บรวบรวม ใช้ และปกป้องข้อมูลส่วนบุคคลของคุณ',
    title: 'นโยบายความเป็นส่วนตัว | EUCHIO Mixed Gas',
    pageTitle: 'นโยบายความเป็นส่วนตัว',
    lastUpdated: 'อัปเดตล่าสุด: 25 พฤษภาคม 2026',
    nav: { home:'หน้าแรก', howItWorks:'วิธีการทำงาน', advantages:'ข้อดี', parameters:'พารามิเตอร์', samples:'ตัวอย่างการตัด', references:'ลูกค้าอ้างอิง', blog:'บล็อก', contact:'ติดต่อ' },
    s1t: '1. เราเป็นใคร',
    s1p: 'EUCHIO Mixed Gas เป็นซีรีส์เทคโนโลยีตัดด้วยแก๊สผสมที่ดำเนินงานโดย Jinan Euchio Machinery Co., Ltd. เว็บไซต์ของเราคือ <a href="https://gasmixtech.com">gasmixtech.com</a>',
    s2t: '2. ข้อมูลที่เราเก็บรวบรวม',
    s2p: 'เราเก็บรวบรวมข้อมูลต่อไปนี้เมื่อคุณใช้เว็บไซต์ของเรา:',
    s2l1: '<strong>การส่งแบบฟอร์มติดต่อ</strong> — ชื่อ ที่อยู่อีเมล หมายเลขโทรศัพท์ ชื่อบริษัท และเนื้อหาข้อความใดๆ ที่คุณเลือกให้ ข้อมูลนี้ถูกประมวลผลผ่าน Web3Forms และส่งตรงถึงเราทางอีเมล',
    s2l2: '<strong>ข้อมูลการวิเคราะห์</strong> — เราใช้ Google Analytics 4 (GA4) เพื่อทำความเข้าใจว่าผู้เยี่ยมชมใช้เว็บไซต์ของเราอย่างไร ซึ่งรวมถึงหน้าที่เข้าชม เวลาบนเว็บไซต์ ภูมิภาคทางภูมิศาสตร์ (ระดับประเทศ/เมือง) ประเภทอุปกรณ์ และแหล่งที่มาของการอ้างอิง GA4 ไม่ได้เก็บที่อยู่ IP เต็มรูปแบบของคุณ',
    s2l3: '<strong>บันทึกเซิร์ฟเวอร์</strong> — ผู้ให้บริการโฮสติ้งของเรา (Cloudflare) เก็บรวบรวมบันทึกการเข้าถึงพื้นฐานโดยอัตโนมัติ รวมถึงที่อยู่ IP ที่ไม่ระบุตัวตน ประเภทเบราว์เซอร์ และเวลาสำหรับการตรวจสอบความปลอดภัยและประสิทธิภาพ',
    s3t: '3. เราใช้ข้อมูลของคุณอย่างไร',
    s3p: 'เราใช้ข้อมูลที่เก็บรวบรวมเพื่อวัตถุประสงค์เหล่านี้เท่านั้น:',
    s3l1: 'ตอบกลับคำถามของคุณที่ส่งผ่านแบบฟอร์มติดต่อของเรา',
    s3l2: 'ทำความเข้าใจปริมาณการเข้าชมเว็บไซต์และปรับปรุงเนื้อหาของเรา (การวิเคราะห์)',
    s3l3: 'รับประกันความปลอดภัยของเว็บไซต์และป้องกันการละเมิด',
    s3noshare: 'เราไม่ขาย ให้เช่า หรือแบ่งปันข้อมูลส่วนบุคคลของคุณกับบุคคลที่สามเพื่อวัตถุประสงค์ทางการตลาดของพวกเขา',
    s4t: '4. คุกกี้',
    s4p1: 'Google Analytics ใช้คุกกี้ของบุคคลที่หนึ่งเพื่อแยกแยะผู้ใช้ คุกกี้เหล่านี้ไม่เก็บข้อมูลที่สามารถระบุตัวบุคคลได้ คุณสามารถปิดการใช้งานคุกกี้ในการตั้งค่าเบราว์เซอร์ของคุณ หรือเลือกไม่ใช้ Google Analytics ทั้งหมดโดยใช้ <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">ส่วนเสริมเบราว์เซอร์สำหรับการยกเลิก Google Analytics</a>',
    s4p2: 'เว็บไซต์ของเราไม่ใช้คุกกี้โฆษณา พิกเซลติดตาม หรือคุกกี้การตลาดของบุคคลที่สาม',
    s5t: '5. พื้นฐานทางกฎหมาย (GDPR)',
    s5p: 'สำหรับผู้เยี่ยมชมจากเขตเศรษฐกิจยุโรป (EEA) เราประมวลผลข้อมูลของคุณตามพื้นฐานทางกฎหมายต่อไปนี้:',
    s5l1: '<strong>ผลประโยชน์ที่ชอบด้วยกฎหมาย</strong> — ข้อมูลการวิเคราะห์เพื่อปรับปรุงเว็บไซต์และบริการของเรา',
    s5l2: '<strong>ความยินยอม</strong> — ข้อมูลแบบฟอร์มติดต่อ ซึ่งคุณให้โดยสมัครใจเมื่อส่งคำถาม',
    s6t: '6. การเก็บรักษาข้อมูล',
    s6p: 'คำถามผ่านแบบฟอร์มติดต่อถูกเก็บไว้ในระบบอีเมลของเราตลอดระยะเวลาความสัมพันธ์ทางธุรกิจบวก 2 ปี ข้อมูล Google Analytics ถูกเก็บไว้ 14 เดือน บันทึก Cloudflare ถูกเก็บไว้ 24 ชั่วโมง',
    s7t: '7. สิทธิของคุณ',
    s7p: 'คุณมีสิทธิ์ที่จะ:',
    s7l1: 'ขอเข้าถึงข้อมูลส่วนบุคคลที่เราเก็บเกี่ยวกับคุณ',
    s7l2: 'ขอแก้ไขหรือลบข้อมูลของคุณ',
    s7l3: 'ถอนความยินยอมได้ตลอดเวลา (สำหรับข้อมูลแบบฟอร์มติดต่อ)',
    s7l4: 'คัดค้านการประมวลผลข้อมูลการวิเคราะห์',
    s7contact: 'เพื่อใช้สิทธิ์เหล่านี้ โปรดติดต่อเราที่ <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a>',
    s8t: '8. บริการของบุคคลที่สาม',
    s8p: 'เราใช้บริการของบุคคลที่สามต่อไปนี้ซึ่งอาจประมวลผลข้อมูลของคุณ:',
    s8l1: '<strong>Google Analytics</strong> (Google LLC, สหรัฐอเมริกา) — การวิเคราะห์เว็บไซต์ Google ได้รับการรับรองภายใต้ EU-US Data Privacy Framework',
    s8l2: '<strong>Cloudflare</strong> (Cloudflare, Inc., สหรัฐอเมริกา) — โฮสติ้งและความปลอดภัยของเว็บไซต์ Cloudflare ได้รับการรับรองภายใต้ EU-US Data Privacy Framework',
    s8l3: '<strong>Web3Forms</strong> — การส่งแบบฟอร์มติดต่อ การส่งแบบฟอร์มถูกส่งตรงไปยังอีเมลของเรา',
    s9t: '9. ติดต่อ',
    s9p: 'หากคุณมีคำถามเกี่ยวกับนโยบายความเป็นส่วนตัวนี้หรือต้องการใช้สิทธิ์ข้อมูลของคุณ โปรดติดต่อเรา:',
    s9email: 'อีเมล',
    s9phone: 'โทรศัพท์',
    s9addr: 'ที่อยู่: Jinan Euchio Machinery Co., Ltd., จี่หนาน, ซานตง, จีน',
    footerTagline: 'เทคโนโลยีแก๊สผสม',
    footerAuth: 'EUCHIO Gas Mixing Technology',
    footerProduct: 'ผลิตภัณฑ์',
    footerHow: 'วิธีการทำงาน',
    footerAdv: 'ข้อดี',
    footerParams: 'พารามิเตอร์',
    footerSamples: 'ตัวอย่างการตัด',
    footerBlog: 'บล็อก',
    footerContact: 'ติดต่อ',
    footerWA_MX: 'WhatsApp (เม็กซิโก)',
    footerWA_TH: 'WhatsApp (ไทย)',
    footerCopy: '© 2026 Jinan Euchio Machinery Co., Ltd. สงวนลิขสิทธิ์',
    footerPrivacy: 'นโยบายความเป็นส่วนตัว',
    footerLinkedIn: 'LinkedIn'
  }
};

// ─── All 15 language codes ─────────────────────────────────────────────
const ALL_LANGS = ['en','zh','es','ko','ja','pt','de','fr','it','nl','pl','ru','tr','vi','th'];

// ─── Build HTML for one language ───────────────────────────────────────
function buildPrivacyHtml(lang) {
  const t = T[lang];
  const isEn = lang === 'en';
  const prefix = isEn ? '' : `/${lang}`;
  const canonical = `https://gasmixtech.com${prefix}/privacy.html`;

  // Build hreflang tags
  let hreflangs = '';
  for (const l of ALL_LANGS) {
    const lprefix = l === 'en' ? '' : `/${l}`;
    hreflangs += `  <link rel="alternate" hreflang="${l}" href="https://gasmixtech.com${lprefix}/privacy.html">\n`;
  }
  hreflangs += `  <link rel="alternate" hreflang="x-default" href="https://gasmixtech.com/privacy.html">`;

  const nav = t.nav;
  const assetPrefix = isEn ? '/' : '/';
  // In subdirectory, links to root assets need / prefix
  // Nav links: on privacy page (root-level for EN, subdir for others)
  const homeHref = isEn ? '/' : `/${lang}/`;
  const navHow = isEn ? '/#principle' : `/${lang}/#principle`;
  const navAdv = isEn ? '/#advantages' : `/${lang}/#advantages`;
  const navParams = isEn ? '/parameters.html' : `/${lang}/parameters.html`;
  const navSamples = isEn ? '/#samples' : `/${lang}/#samples`;
  const navRefs = isEn ? '/#reference' : `/${lang}/#reference`;
  const navBlog = '/blog/';
  const navContact = isEn ? '/contact.html' : `/${lang}/contact.html`;
  const privacyHref = isEn ? '/privacy.html' : `/${lang}/privacy.html`;

  // Footer links
  const footerHomeHref = isEn ? '/' : `/${lang}/`;
  const footerHowHref = isEn ? '/#principle' : `/${lang}/#principle`;
  const footerAdvHref = isEn ? '/#advantages' : `/${lang}/#advantages`;
  const footerParamsHref = isEn ? '/parameters.html' : `/${lang}/parameters.html`;
  const footerSamplesHref = isEn ? '/#samples' : `/${lang}/#samples`;
  const footerBlogHref = '/blog/';

  // For subdirectory pages, asset paths use / prefix (absolute from root)
  const cssPath = '/styles.min.css';
  const jsPath = '/script.min.js';
  const faviconPath = '/favicon.svg';
  const logoPath = '/images/lishi-logo.png';

  return `<!DOCTYPE html>
<html lang="${lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="${t.metaDesc}">
  <meta name="robots" content="noindex, follow">
  <title>${t.title}</title>
  <link rel="canonical" href="${canonical}">
${hreflangs}
  <link rel="icon" type="image/svg+xml" href="${faviconPath}">
  <link rel="stylesheet" href="${cssPath}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    .policy-section {
      padding: 120px 0 80px;
    }
    .policy-content {
      max-width: 780px;
      margin: 0 auto;
    }
    .policy-content h1 {
      font-size: 2rem;
      margin-bottom: 8px;
      color: var(--color-text);
    }
    .policy-content .last-updated {
      color: var(--color-text-dim);
      font-size: 0.9rem;
      margin-bottom: 40px;
    }
    .policy-content h2 {
      font-size: 1.2rem;
      margin-top: 36px;
      margin-bottom: 12px;
      color: var(--color-primary);
    }
    .policy-content p, .policy-content li {
      font-size: 0.95rem;
      line-height: 1.7;
      color: var(--color-text-muted);
      margin-bottom: 12px;
    }
    .policy-content ul {
      padding-left: 20px;
      margin-bottom: 16px;
    }
    .policy-content a {
      color: var(--color-primary);
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header class="header">
    <div class="container header-inner">
      <a href="${homeHref}" class="logo">
        <img src="${logoPath}" alt="EUCHIO">
        <div class="logo-text">
          <span class="logo-brand">EUCHIO</span>
          <span class="logo-tagline">${t.footerTagline}</span>
        </div>
      </a>
      <nav class="nav" id="nav" role="navigation" aria-label="Main navigation">
        <a href="${homeHref}">${nav.home}</a>
        <a href="${navHow}">${nav.howItWorks}</a>
        <a href="${navAdv}">${nav.advantages}</a>
        <a href="${navParams}">${nav.parameters}</a>
        <a href="${navSamples}">${nav.samples}</a>
        <a href="${navRefs}">${nav.references}</a>
        <a href="${navBlog}">${nav.blog}</a>
        <a href="${navContact}" class="nav-cta">${nav.contact}</a>
      </nav>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Toggle menu">&#9776;</button>
    </div>
  </header>

  <section class="policy-section">
    <div class="container">
      <div class="policy-content">
        <h1>${t.pageTitle}</h1>
        <p class="last-updated">${t.lastUpdated}</p>

        <h2>${t.s1t}</h2>
        <p>${t.s1p}</p>

        <h2>${t.s2t}</h2>
        <p>${t.s2p}</p>
        <ul>
          <li>${t.s2l1}</li>
          <li>${t.s2l2}</li>
          <li>${t.s2l3}</li>
        </ul>

        <h2>${t.s3t}</h2>
        <p>${t.s3p}</p>
        <ul>
          <li>${t.s3l1}</li>
          <li>${t.s3l2}</li>
          <li>${t.s3l3}</li>
        </ul>
        <p>${t.s3noshare}</p>

        <h2>${t.s4t}</h2>
        <p>${t.s4p1}</p>
        <p>${t.s4p2}</p>

        <h2>${t.s5t}</h2>
        <p>${t.s5p}</p>
        <ul>
          <li>${t.s5l1}</li>
          <li>${t.s5l2}</li>
        </ul>

        <h2>${t.s6t}</h2>
        <p>${t.s6p}</p>

        <h2>${t.s7t}</h2>
        <p>${t.s7p}</p>
        <ul>
          <li>${t.s7l1}</li>
          <li>${t.s7l2}</li>
          <li>${t.s7l3}</li>
          <li>${t.s7l4}</li>
        </ul>
        <p>${t.s7contact}</p>

        <h2>${t.s8t}</h2>
        <p>${t.s8p}</p>
        <ul>
          <li>${t.s8l1}</li>
          <li>${t.s8l2}</li>
          <li>${t.s8l3}</li>
        </ul>

        <h2>${t.s9t}</h2>
        <p>${t.s9p}</p>
        <p>
          ${t.s9email}: <a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a><br>
          ${t.s9phone}: +86 186 1558 4520<br>
          ${t.s9addr}
        </p>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="${footerHomeHref}" class="logo">
            <img src="${logoPath}" alt="EUCHIO">
            <div class="logo-text">
              <span class="logo-brand">EUCHIO</span>
              <span class="logo-tagline">${t.footerTagline}</span>
            </div>
          </a>
          <div class="footer-auth">
            <div class="footer-auth-line">${t.footerAuth}</div>
          </div>
        </div>
        <div>
          <h4>${t.footerProduct}</h4>
          <ul class="footer-links">
            <li><a href="${footerHowHref}">${t.footerHow}</a></li>
            <li><a href="${footerAdvHref}">${t.footerAdv}</a></li>
            <li><a href="${footerParamsHref}">${t.footerParams}</a></li>
            <li><a href="${footerSamplesHref}">${t.footerSamples}</a></li>
            <li><a href="${footerBlogHref}">${t.footerBlog}</a></li>
          </ul>
        </div>
        <div>
          <h4>${t.footerContact}</h4>
          <ul class="footer-links">
            <li><a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a></li>
            <li><a href="tel:+8618615584520">+86 186 1558 4520</a></li>
            <li><a href="https://wa.me/525572080065" target="_blank">${t.footerWA_MX}</a></li>
            <li><a href="https://wa.me/66961135966" target="_blank">${t.footerWA_TH}</a></li>
            <li><a href="https://www.linkedin.com/company/euchio" target="_blank">${t.footerLinkedIn}</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>${t.footerCopy}</span>
        <span><a href="${privacyHref}">${t.footerPrivacy}</a></span>
      </div>
    </div>
  </footer>

  <script src="${jsPath}"></script>
</body>
</html>
`;
}

// ─── Main ──────────────────────────────────────────────────────────────

console.log('Building privacy policy pages...\n');

// English (root)
const enHtml = buildPrivacyHtml('en');
fs.writeFileSync(path.join(PUBLIC_DIR, 'privacy.html'), enHtml, 'utf-8');
console.log('  privacy.html (en - root)');

let built = 1;

// All other languages
for (const lang of LANG_DIRS) {
  if (!T[lang]) {
    console.warn(`  skip: ${lang} - no translations`);
    continue;
  }
  const html = buildPrivacyHtml(lang);
  const outDir = path.join(PUBLIC_DIR, lang);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'privacy.html'), html, 'utf-8');
  built++;
  console.log(`  ${lang}/privacy.html`);
}

console.log(`\nDone — ${built} privacy policy pages built.`);

#!/usr/bin/env python3
"""
Build language versions from English source.
Step 1: Apply structural changes (paths, URLs, hreflang, dropdown)
Step 2: Translate English content to target language
"""
import os, re, sys

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

# Language metadata
LANGS = {
    'it': {'name': 'Italiano', 'html_lang': 'it', 'dir': 'ltr'},
    'de': {'name': 'Deutsch', 'html_lang': 'de', 'dir': 'ltr'},
    'fr': {'name': 'Français', 'html_lang': 'fr', 'dir': 'ltr'},
    'nl': {'name': 'Nederlands', 'html_lang': 'nl', 'dir': 'ltr'},
    'ru': {'name': 'Русский', 'html_lang': 'ru', 'dir': 'ltr'},
    'vi': {'name': 'Tiếng Việt', 'html_lang': 'vi', 'dir': 'ltr'},
    'th': {'name': 'ไทย', 'html_lang': 'th', 'dir': 'ltr'},
}

def apply_structural(content, lang, page_type):
    """Apply all structural changes for subdirectory language page."""
    info = LANGS[lang]
    p = lang  # short alias

    # ── Phase 1: Asset paths (./ → ../) ──
    content = content.replace('href="./styles.css"', 'href="../styles.css"')
    content = content.replace('src="./script.js"', 'src="../script.js"')
    content = content.replace('href="./favicon.svg"', 'href="../favicon.svg"')

    # ── Phase 2: Image paths ──
    content = content.replace('src="/images/', 'src="../images/')
    content = content.replace('src="./images/', 'src="../images/')

    # ── Phase 3: OG image + JSON-LD logo URLs ──
    content = content.replace(
        'content="https://gasmixtech.com/images/',
        f'content="https://gasmixtech.com/{p}/images/')
    content = content.replace(
        '"logo": "https://gasmixtech.com/images/',
        f'"logo": "https://gasmixtech.com/{p}/images/')

    # ── Phase 4: <html lang> ──
    content = content.replace('<html lang="en">', f'<html lang="{info["html_lang"]}">')

    # ── Phase 5: Canonical + OG:url (tag-specific patterns) ──
    if page_type == 'index':
        content = content.replace(
            '<link rel="canonical" href="https://gasmixtech.com/">',
            f'<link rel="canonical" href="https://gasmixtech.com/{p}/">')
        content = content.replace(
            '<meta property="og:url" content="https://gasmixtech.com/">',
            f'<meta property="og:url" content="https://gasmixtech.com/{p}/">')
    elif page_type == 'contact':
        content = content.replace(
            '<link rel="canonical" href="https://gasmixtech.com/contact.html">',
            f'<link rel="canonical" href="https://gasmixtech.com/{p}/contact.html">')
        content = content.replace(
            '<meta property="og:url" content="https://gasmixtech.com/contact.html">',
            f'<meta property="og:url" content="https://gasmixtech.com/{p}/contact.html">')
        content = content.replace(
            'value="https://gasmixtech.com/contact.html',
            f'value="https://gasmixtech.com/{p}/contact.html')
    elif page_type == 'parameters':
        content = content.replace(
            '<link rel="canonical" href="https://gasmixtech.com/parameters.html">',
            f'<link rel="canonical" href="https://gasmixtech.com/{p}/parameters.html">')
        content = content.replace(
            '<meta property="og:url" content="https://gasmixtech.com/parameters.html">',
            f'<meta property="og:url" content="https://gasmixtech.com/{p}/parameters.html">')

    # ── Phase 6: Hreflang ──
    # Replace en hreflang → new_lang + en (net +1 entry).
    # x-default stays untouched (always points to root).
    if page_type == 'index':
        content = content.replace(
            '<link rel="alternate" hreflang="en" href="https://gasmixtech.com/">',
            f'<link rel="alternate" hreflang="{p}" href="https://gasmixtech.com/{p}/">\n'
            '  <link rel="alternate" hreflang="en" href="https://gasmixtech.com/">')
    elif page_type == 'contact':
        content = content.replace(
            '<link rel="alternate" hreflang="en" href="https://gasmixtech.com/contact.html">',
            f'<link rel="alternate" hreflang="{p}" href="https://gasmixtech.com/{p}/contact.html">\n'
            '  <link rel="alternate" hreflang="en" href="https://gasmixtech.com/contact.html">')
    elif page_type == 'parameters':
        content = content.replace(
            '<link rel="alternate" hreflang="en" href="https://gasmixtech.com/parameters.html">',
            f'<link rel="alternate" hreflang="{p}" href="https://gasmixtech.com/{p}/parameters.html">\n'
            '  <link rel="alternate" hreflang="en" href="https://gasmixtech.com/parameters.html">')

    # ── Phase 7: Nav links (match with HTML context to avoid lang-dropdown) ──
    # Logo (in header and footer) — contains class="logo"
    content = content.replace('href="/" class="logo"', f'href="/{p}/" class="logo"')

    # Nav: "Home" link on contact/parameters pages (NOT index, which uses #home)
    if page_type != 'index':
        content = content.replace('<a href="/">Home</a>', f'<a href="/{p}/">Home</a>')

    # Nav: section anchors on contact/parameters pages
    for sec in ['#principle', '#advantages', '#samples', '#reference', '#faq']:
        content = content.replace(f'<a href="/{sec}">', f'<a href="/{p}/{sec}">')

    # Nav: blog link
    content = content.replace('<a href="/blog/">Blog</a>', f'<a href="/{p}/blog/">Blog</a>')

    # Nav: contact CTA (NOT dropdown)
    content = content.replace(
        'href="/contact.html" class="nav-cta',
        f'href="/{p}/contact.html" class="nav-cta')
    # Also match active nav-cta on contact page itself
    content = content.replace(
        'href="/contact.html" class="active nav-cta',
        f'href="/{p}/contact.html" class="active nav-cta')

    # Nav: parameters link on contact page
    content = content.replace(
        '<a href="/parameters.html">Parameters</a>',
        f'<a href="/{p}/parameters.html">Parameters</a>')

    # ── Phase 8: Content CTAs (match btn classes to avoid dropdown) ──
    content = content.replace(
        'href="/contact.html" class="btn',
        f'href="/{p}/contact.html" class="btn')
    content = content.replace(
        'href="/parameters.html" class="btn',
        f'href="/{p}/parameters.html" class="btn')
    # "Back to Home" link
    content = content.replace(
        'href="/" class="btn btn-primary">Back to',
        f'href="/{p}/" class="btn btn-primary">Back to')

    # ── Phase 9: Lang dropdown ──
    # Remove active from English option
    content = content.replace(
        'class="lang-option active" data-lang="en">English',
        'class="lang-option" data-lang="en">English')
    content = content.replace(
        'class="lang-option active" data-lang="en">Eng</a>',
        'class="lang-option" data-lang="en">Eng</a>')

    # Add new language option after pl (which is the last one in every dropdown)
    # For index page: no page suffix
    # For contact/params: add page-specific URL
    if page_type == 'index':
        new_option = f'<a href="/{p}/" class="lang-option active" data-lang="{p}">{info["name"]}</a>'
        marker = '<a href="/pl/" class="lang-option" data-lang="pl">Polski</a>'
    elif page_type == 'contact':
        new_option = f'<a href="/{p}/contact.html" class="lang-option active" data-lang="{p}">{info["name"]}</a>'
        marker = '<a href="/pl/contact.html" class="lang-option" data-lang="pl">Polski</a>'
    elif page_type == 'parameters':
        new_option = f'<a href="/{p}/parameters.html" class="lang-option active" data-lang="{p}">{info["name"]}</a>'
        marker = '<a href="/pl/parameters.html" class="lang-option" data-lang="pl">Polski</a>'

    content = content.replace(marker, f'{marker}\n            {new_option}')

    return content


def translate(content, translations):
    """Apply English→target translations (longest-first to avoid substring conflicts)."""
    for eng, tgt in sorted(translations.items(), key=lambda x: -len(x[0])):
        if eng in content:
            content = content.replace(eng, tgt)
    return content


# ================================================================
# COMPLETE TRANSLATION MAPS
# ================================================================

# ---- ITALIAN ----
IT = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "Dispositivo a gas misto LISHI LASER per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di gas in meno. Tecnologia a rapporto N2/O2 per taglio acciaio al carbonio.",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Dispositivo a Gas Misto | Taglio Laser 3× Più Veloce",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Dispositivo a gas misto per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di gas in meno. Tecnologia a rapporto N2/O2.",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "miscelatore gas taglio laser, dispositivo miscelazione azoto ossigeno, taglio laser micro ossigeno, taglio laser acciaio carbonio, laser alta potenza 12kW 60kW, gas misto vs compressore aria, eliminazione bave taglio laser, riduzione consumo azoto, miscelatore gas Han's, apparecchiatura gas laser industriale, configurazione gas uno-a-due, ottimizzazione gas assistito",
    "LISHI LASER Mixed Gas Device": "LISHI LASER Dispositivo a Gas Misto",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Prezzi e preventivi dispositivo a gas misto LISHI LASER. Compatibile con tutti i principali marchi laser (HANS, DNE, PENTA, LEAD, HSG, BODOR). Spedizione globale disponibile.",
    "Request a quote for LISHI LASER mixed gas cutting equipment. Compatible with all major laser brands. Global shipping available.":
     "Richiedi un preventivo per apparecchiatura da taglio a gas misto LISHI LASER. Compatibile con tutti i principali marchi laser. Spedizione globale disponibile.",
    "LISHI LASER Contact | Get Mixed Gas Device Quote":
     "LISHI LASER Contatto | Richiedi Preventivo Dispositivo Gas Misto",
    "laser cutting gas equipment quote, mixed gas device distributor, laser cutting equipment manufacturer, HANS laser compatible gas":
     "preventivo apparecchiatura gas taglio laser, distributore dispositivo gas misto, produttore apparecchiatura taglio laser, gas compatibile laser HANS",
    "LISHI LASER Contact": "LISHI LASER Contatto",

    # Nav + UI
    "Skip to content": "Vai al contenuto",
    "Home": "Home",
    "Advantages": "Vantaggi",
    "Samples": "Campioni",
    "Customers": "Clienti",
    "Blog": "Blog",
    "Contact": "Contatto",
    "Gas Mixing Technology": "Tecnologia Miscelazione Gas",
    "Menu toggle": "Menu",
    "How It Works": "Come Funziona",
    "Parameters": "Parametri",

    # Hero
    'Cut <span class="accent">3× Faster</span><br>with Mixed Gas Technology':
     'Taglia <span class="accent">3× Più Veloce</span><br>con la Tecnologia a Gas Misto',
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "Soluzione gas misto N₂/O₂ per macchine da taglio laser 12KW-60KW",
    "3× Faster than O₂": "3× Più Veloce dell'O₂",
    "Zero Burrs": "Zero Bave",
    "33% Less N₂": "33% Meno N₂",
    "13 Years in Laser Metal Cutting": "13 Anni nel Taglio Laser dei Metalli",
    "LISHI LASER Mixed Gas Device delivers micro-oxygen cutting for high-power laser machines (12KW–60KW). No burrs, less gas consumption, and dramatically faster processing.":
     "Il Dispositivo a Gas Misto LISHI LASER offre taglio a micro-ossigeno per macchine laser ad alta potenza (12KW–60KW). Nessuna bava, minor consumo di gas e lavorazione notevolmente più veloce.",
    "Get Quote →": "Richiedi Preventivo →",
    "View Parameters": "Visualizza Parametri",

    # Principle
    "What is a Mixed Gas Device?": "Cos'è un Dispositivo a Gas Misto?",
    "Our nitrogen oxygen mixing device uses": "Il nostro dispositivo di miscelazione azoto-ossigeno utilizza",
    "to produce precisely calibrated N₂/O₂ mixed gas — eliminating burrs on carbon steel while delivering 3× faster cutting speed versus traditional oxygen cutting. Supports high-power laser machines from 12kW to 60kW.":
     "per produrre gas misto N₂/O₂ precisamente calibrato — eliminando le bave sull'acciaio al carbonio e offrendo una velocità di taglio 3× superiore rispetto al taglio a ossigeno tradizionale. Supporta macchine laser ad alta potenza da 12kW a 60kW.",
    "Micro-oxygen laser cutting technology": "Tecnologia di taglio laser a micro-ossigeno",
    "Liquid N₂ + Liquid O₂": "N₂ Liquido + O₂ Liquido",
    "Raw materials stored in tanks, pressure 20–25 bar": "Materie prime stoccate in serbatoi, pressione 20–25 bar",
    "Vaporizer": "Vaporizzatore",
    "Converts liquid gases to gas form": "Converte i gas liquidi in forma gassosa",
    "Mixed Gas Device": "Dispositivo a Gas Misto",
    "Stable pressure + proportional mixing → N₂ 95% / O₂ 5%": "Pressione stabile + miscelazione proporzionale → N₂ 95% / O₂ 5%",
    "To Laser Machine": "Alla Macchina Laser",
    "Output: 12–16 bar, flow rate up to 200m³/h": "Uscita: 12–16 bar, portata fino a 200m³/h",
    "Input: N₂ + O₂ at 20–25 bar. Output: N₂ purity ~95%, pressure 12–16 bar, max flow 200m³/h. Compact gas tank (capacity >3m³).":
     "Ingresso: N₂ + O₂ a 20–25 bar. Uscita: purezza N₂ ~95%, pressione 12–16 bar, portata max 200m³/h. Serbatoio gas compatto (capacità >3m³).",
    "Device Dimensions": "Dimensioni Dispositivo",
    "800mm × 350mm × 1100mm, weight 90kg. One device simultaneously supports two laser machines (One-to-Two configuration).":
     "800mm × 350mm × 1100mm, peso 90kg. Un dispositivo supporta simultaneamente due macchine laser (configurazione Uno-a-Due).",
    "High cutting speed + zero burrs. After installation, simply adjust the N₂ 95% to O₂ 5% ratio for different sheet thicknesses. The built-in program makes operation intuitive.":
     "Alta velocità di taglio + zero bave. Dopo l'installazione, regola semplicemente il rapporto N₂ 95% / O₂ 5% per diversi spessori lamiera. Il programma integrato rende il funzionamento intuitivo.",
    "Broad Compatibility": "Ampia Compatibilità",
    "Works with all major brands: HAN'S, DNE, PENTA, LEAD, HSG and more. Compatible with BODOR, KIMLA, MESSER and other global brands.":
     "Funziona con tutti i principali marchi: HAN'S, DNE, PENTA, LEAD, HSG e altri. Compatibile con BODOR, KIMLA, MESSER e altri marchi globali.",

    # Advantages
    "Why Mixed Gas Instead of O₂, N₂ or Air?": "Perché Gas Misto invece di O₂, N₂ o Aria?",
    "Eliminate burrs in carbon steel laser cutting while cutting nitrogen consumption by 33%. Our maintenance-free gas delivery system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Elimina le bave nel taglio laser dell'acciaio al carbonio riducendo il consumo di azoto del 33%. Il nostro sistema di alimentazione gas esente da manutenzione è compatibile con HAN'S, DNE, PENTA, LEAD, HSG, BODOR e tutti gli altri principali marchi.",
    "Competitive Advantage": "Vantaggio Competitivo",
    "3× Faster Cutting": "Taglio 3× Più Veloce",
    "Boost laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Aumenta la velocità di taglio laser fino a 3× rispetto al taglio a ossigeno. Esempio: acciaio al carbonio 8mm a 16m/min con gas misto, solo 2–3m/min con O₂.",
    "Eliminate Burrs": "Elimina le Bave",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cutting edges requiring no secondary grinding.":
     "L'ambiente a micro-ossigeno controllato garantisce una combustione completa. Risultato: bordi di taglio lisci e senza bave che non richiedono molatura secondaria.",
    "Cut Gas Costs": "Riduci i Costi del Gas",
    "Reduce nitrogen consumption by 33–50% versus pure N₂ cutting. Cost comparison: mixed gas costs significantly less than air compressors when factoring in maintenance-free operation.":
     "Riduci il consumo di azoto del 33–50% rispetto al taglio con N₂ puro. Confronto costi: il gas misto costa significativamente meno dei compressori d'aria considerando il funzionamento esente da manutenzione.",
    "Maintenance-Free": "Esente da Manutenzione",
    "Power consumption: only 2 kWh per 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Consumo energetico: solo 2 kWh ogni 24 ore. A differenza dei compressori d'aria che richiedono cambio filtri/olio ogni 3.000 ore, la nostra apparecchiatura gas laser industriale è esente da manutenzione.",
    "One-to-Two Laser Setup": "Configurazione Uno-a-Due",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines at different power levels simultaneously — no switching required.":
     "L'unico produttore con apparecchiatura a gas misto uno-a-due stabile. Una stazione di miscelazione gas industriale alimenta due macchine laser a diversi livelli di potenza simultaneamente — senza necessità di commutazione.",
    "Lens Protection": "Protezione Lenti",
    "Air compressors carry oil/water contamination risk that can burn laser head lenses ($5,000–50,000 loss). Our pure liquid gas source keeps your optical system pristine.":
     "I compressori d'aria comportano rischi di contaminazione olio/acqua che possono bruciare le lenti della testa laser (perdita di $5.000–50.000). La nostra fonte di gas liquido puro mantiene il sistema ottico impeccabile.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air": "Confronto Prestazioni: Gas Misto vs O₂ vs N₂ vs Aria",
    "Factor": "Fattore",
    "Mixed Gas": "Gas Misto",
    "O₂ (Oxygen)": "O₂ (Ossigeno)",
    "N₂ (Nitrogen)": "N₂ (Azoto)",
    "Air": "Aria",
    "Cutting Speed": "Velocità di Taglio",
    "3× faster (e.g. 16m/min @ 8mm CS)": "3× più veloce (es. 16m/min @ 8mm AC)",
    "30% slower than mixed gas": "30% più lento del gas misto",
    "Burrs possible on thick sheets": "Bave possibili su lamiere spesse",
    "Cut Surface": "Superficie di Taglio",
    "Smooth, burr-free": "Liscia, senza bave",
    "Oxidized, rough edges": "Ossidata, bordi ruvidi",
    "Contaminated, rough": "Contaminata, ruvida",
    "Gas Consumption": "Consumo Gas",
    "1/3 less than N₂": "1/3 in meno di N₂",
    "Similar total": "Totale simile",
    "High": "Alto",
    "Very high (compressor)": "Molto alto (compressore)",
    "Power Cost": "Costo Energetico",
    "2 kWh/24h": "2 kWh/24h",
    "Small Hole Piercing": "Perforazione Piccoli Fori",
    "Excellent — clean & fast": "Eccellente — pulito e veloce",
    "Some burr during piercing": "Qualche bava durante perforazione",
    "Best for small holes": "Migliore per piccoli fori",
    "Equipment Protection": "Protezione Attrezzatura",
    "No pipeline contamination": "Nessuna contaminazione tubazioni",
    "Oil/water risk": "Rischio olio/acqua",

    # ROI
    "ROI Calculator": "Calcolatore ROI",
    "Calculator": "Calcolatore",
    "Calculate Your Laser Cutting Gas Cost Savings": "Calcola il Risparmio sui Costi del Gas da Taglio Laser",
    "See how much you could save with LISHI LASER mixed gas technology. Cut nitrogen consumption, eliminate burrs on carbon steel, and boost throughput.":
     "Scopri quanto puoi risparmiare con la tecnologia a gas misto LISHI LASER. Riduci il consumo di azoto, elimina le bave sull'acciaio al carbonio e aumenta la produttività.",
    "Machine Power": "Potenza Macchina",
    "Material Thickness": "Spessore Materiale",
    "Daily Work Hours": "Ore Lavorative Giornaliere",
    "Actual Cutting Time (Beam On %)": "Tempo di Taglio Effettivo (Raggio Attivo %)",
    "Typical shops run 40–70% — remaining time is loading, piercing, idle.": "Le officine tipiche operano al 40–70% — il tempo restante è carico, perforazione, inattività.",
    "Profit Per Meter (USD/m)": "Profitto al Metro (USD/m)",
    "Your selling price minus material cost (USD)": "Il tuo prezzo di vendita meno il costo del materiale (USD)",
    "Monthly N₂ Cost (USD)": "Costo Mensile N₂ (USD)",
    "Your current monthly nitrogen spend (USD)": "La tua spesa mensile attuale in azoto (USD)",
    "Estimated Annual Profit Increase (USD)": "Aumento Stimato del Profitto Annuo (USD)",
    "in nitrogen savings": "in risparmio di azoto",
    "Theoretical ceiling based on your inputs. Real results depend on job mix, nesting efficiency and machine uptime.":
     "Tetto teorico basato sui tuoi input. I risultati reali dipendono dal mix di lavoro, efficienza di nesting e disponibilità macchina.",
    "Want the full parameter table for your specific machine?": "Vuoi la tabella completa dei parametri per la tua macchina specifica?",
    "Get detailed cutting data tailored to your 12KW–60KW laser setup.": "Ottieni dati di taglio dettagliati su misura per il tuo setup laser 12KW–60KW.",
    "Get Free Parameters →": "Ottieni Parametri Gratuiti →",
    "Or contact us directly:": "O contattaci direttamente:",

    # Air vs Mixed
    "Why Air Compressors Cost More": "Perché i Compressori d'Aria Costano di Più",
    "Air Looks Free. It Isn't.": "L'Aria Sembra Gratis. Non Lo È.",
    "Most users pick an air compressor for the low upfront cost — but three hidden costs eat your margin.":
     "La maggior parte degli utenti sceglie un compressore d'aria per il basso costo iniziale — ma tre costi nascosti erodono il margine.",
    "HIGH MAINTENANCE COST": "COSTO DI MANUTENZIONE ELEVATO",
    "Filter replacement every 500-1000 hours": "Sostituzione filtri ogni 500-1000 ore",
    "Oil changes and system flushing": "Cambio olio e lavaggio sistema",
    "Unexpected repair downtime": "Fermi macchina imprevisti per riparazioni",
    "2 kWh/24h — near zero maintenance": "2 kWh/24h — manutenzione quasi zero",
    "~$73/year electricity": "~$73/anno di elettricità",
    "POOR CUT QUALITY": "SCARSA QUALITÀ DI TAGLIO",
    "Dark oxidation layer on cut surface": "Strato di ossidazione scura sulla superficie di taglio",
    "Burrs and slag requiring rework": "Bave e scorie che richiedono rilavorazione",
    "Extra grinding/polishing labor": "Lavoro extra di molatura/lucidatura",
    "Cannot deliver premium jobs": "Impossibile consegnare lavori premium",
    "Silver-white surface, zero burrs": "Superficie bianco-argento, zero bave",
    "Ready to ship immediately": "Pronto per la spedizione immediata",
    "LENS CONTAMINATION RISK": "RISCHIO CONTAMINAZIONE LENTI",
    "Oil/water in compressed air": "Olio/acqua nell'aria compressa",
    "Burns the laser head protection lens": "Brucia la lente di protezione della testa laser",
    "Lens replacement: $200–500 each time": "Sostituzione lente: $200–500 ogni volta",
    "Unplanned production stop": "Fermo produzione non pianificato",
    "100% safe — pure liquid gas source": "100% sicuro — fonte di gas liquido puro",
    "Zero optical risk": "Zero rischio ottico",
    "LISHI Mixed Gas: The Real Cost Saver": "LISHI Gas Misto: Il Vero Riduttore di Costi",
    "While air looks free, your real cost is in maintenance, rework, and lens replacements. Mixed gas costs less long-term — and delivers superior quality.":
     "Anche se l'aria sembra gratis, il costo reale è in manutenzione, rilavorazioni e sostituzioni lenti. Il gas misto costa meno a lungo termine — e offre qualità superiore.",

    # Parameters by Power
    "Cutting Parameters by Power": "Parametri di Taglio per Potenza",
    "Optimal carbon steel cutting thickness range for each laser power level. Mixed gas delivers consistent high-speed cutting across all thicknesses.":
     "Gamma di spessore ottimale per taglio acciaio al carbonio per ogni livello di potenza laser. Il gas misto offre taglio ad alta velocità costante su tutti gli spessori.",
    "Mixed Gas Speed": "Velocità Gas Misto",
    "Best for ≤16mm carbon steel": "Ideale per acciaio al carbonio ≤16mm",
    "Best for ≤25mm carbon steel": "Ideale per acciaio al carbonio ≤25mm",
    "Contact for details": "Contattaci per dettagli",
    "Best for ≤30mm carbon steel": "Ideale per acciaio al carbonio ≤30mm",
    "Higher powers (40KW, 60KW) available. Contact us for detailed parameters.": "Potenze superiori (40KW, 60KW) disponibili. Contattaci per parametri dettagliati.",
    "View All Parameters →": "Visualizza Tutti i Parametri →",

    # Samples
    "Real Results": "Risultati Reali",
    "Cutting Samples & Test Videos": "Campioni di Taglio e Video di Test",
    "Real cutting footage from end users worldwide. No retouching — real data, real performance.":
     "Filmati di taglio reali da utilizzatori finali in tutto il mondo. Nessun ritocco — dati reali, prestazioni reali.",
    "12kW & 30kW · Professional Metal Fab": "12kW e 30kW · Fabbrica Metalmeccanica Professionale",
    "Dual-power setup, one device feeds two machines — 33% less gas, no speed compromise": "Configurazione doppia potenza, un dispositivo alimenta due macchine — 33% di gas in meno, nessun compromesso sulla velocità",
    "Mixed gas for high-power lasers": "Gas misto per laser ad alta potenza",
    "30kW · 10–30mm Carbon Steel": "30kW · 10–30mm Acciaio al Carbonio",
    "Thick sheets, zero burrs. 10–14 m/min on 10mm, previously only possible with O₂": "Lamiere spesse, zero bave. 10–14 m/min su 10mm, prima possibile solo con O₂",
    "High-power mixed gas cutting": "Taglio a gas misto ad alta potenza",
    "60kW · 30–40mm Carbon Steel": "60kW · 30–40mm Acciaio al Carbonio",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas dominates": "Taglio ultra-spesso a 3,5 m/min. Dove N₂ fatica, il gas misto domina",
    "Ultra-high-power mixed gas": "Gas misto ad altissima potenza",
    "12kW · 3mm Aluminum": "12kW · 3mm Alluminio",
    "Smooth aluminum edges, zero oxidation. Faster than air, cleaner than N₂": "Bordi in alluminio lisci, zero ossidazione. Più veloce dell'aria, più pulito di N₂",
    "Aluminum mixed gas cutting": "Taglio alluminio a gas misto",
    "12kW · 2mm Aluminum": "12kW · 2mm Alluminio",
    "Precision aluminum with micro-oxygen — speed and quality in a single pass": "Alluminio di precisione con micro-ossigeno — velocità e qualità in un singolo passaggio",
    "Thin aluminum mixed gas": "Gas misto per alluminio sottile",
    "12kW · 1mm Aluminum": "12kW · 1mm Alluminio",
    "Paper-thin aluminum, zero burn. Mixed gas enables what N₂ can't achieve": "Alluminio sottile come carta, zero bruciature. Il gas misto permette ciò che N₂ non può ottenere",
    "Precision thin aluminum cutting": "Taglio di precisione alluminio sottile",
    "Watch Video": "Guarda Video",

    # Global
    "GLOBAL NETWORK": "RETE GLOBALE",
    "Where High-Power Lasers Cut.<br>Our Gas Flows.": "Dove i Laser ad Alta Potenza Tagliano.<br>Il Nostro Gas Scorre.",
    "From mega-factories on the coast to workshops deep inland, mixed gas technology now powers laser cutters across four continents — and the footprint is expanding every quarter.":
     "Dalle mega-fabbriche sulla costa alle officine nell'entroterra, la tecnologia a gas misto ora alimenta macchine da taglio laser in quattro continenti — e la presenza si espande ogni trimestre.",
    "Countries Stocked": "Paesi Riforniti",
    "Continents Deployed": "Continenti Operativi",
    "Power Range Served": "Gamma di Potenza Servita",
    "Manufacturing Durability": "Durabilità di Produzione",
    "The Next Territory is Still Open.": "Il Prossimo Territorio è Ancora Disponibile.",
    "Exclusive distributor partnerships available in select regions. Ship a container, build your market.":
     "Partenariati di distribuzione esclusivi disponibili in regioni selezionate. Spedisci un container, costruisci il tuo mercato.",

    # FAQ
    "Frequently Asked Questions": "Domande Frequenti",
    "What is a mixed gas device and how does it work?": "Cos'è un dispositivo a gas misto e come funziona?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Un dispositivo a gas misto converte azoto liquido (N₂) e ossigeno liquido (O₂) in una miscela di gas N₂/O₂ precisamente calibrata (tipicamente 95%/5%). Questa miscela micro-ossigeno viene utilizzata come gas ausiliario nel taglio laser ad alta potenza, offrendo velocità di taglio 3× superiori sull'acciaio al carbonio rispetto all'ossigeno puro, eliminando completamente le bave.",
    "Is it compatible with my laser machine?": "È compatibile con la mia macchina laser?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Sì. Il Dispositivo a Gas Misto LISHI LASER funziona con tutti i principali marchi laser, inclusi HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA e MESSER. Supporta macchine da 12kW a 60kW. Se la tua macchina utilizza connessioni standard per gas ausiliario, è compatibile.",
    "What thicknesses can it cut?": "Quali spessori può tagliare?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "La gamma di taglio dipende dalla potenza del laser: 12kW gestisce fino a 16mm, 20kW fino a 25mm, 30kW fino a 30mm e 60kW fino a 40mm di acciaio al carbonio. Taglia anche acciaio inossidabile e alluminio. Tabelle dettagliate dei parametri sono disponibili nella nostra pagina parametri.",
    "How much gas does it save?": "Quanto gas fa risparmiare?",
    "Mixed gas reduces nitrogen consumption by 33–50% compared to pure N₂ cutting. Additionally, the device consumes only 2 kWh per 24 hours — essentially maintenance-free. The optimized mixing ratio means you get more cutting per unit of gas.":
     "Il gas misto riduce il consumo di azoto del 33–50% rispetto al taglio con N₂ puro. Inoltre, il dispositivo consuma solo 2 kWh ogni 24 ore — essenzialmente esente da manutenzione. Il rapporto di miscelazione ottimizzato significa più taglio per unità di gas.",
    "Does it require regular maintenance?": "Richiede manutenzione regolare?",
    "No. Unlike air compressors that need filter/oil changes every 500–3,000 hours, the LISHI Mixed Gas Device is maintenance-free. There are no moving parts to wear out, no filters to replace, and no oil to change.":
     "No. A differenza dei compressori d'aria che necessitano cambio filtri/olio ogni 500–3.000 ore, il Dispositivo a Gas Misto LISHI è esente da manutenzione. Non ci sono parti mobili da usurare, nessun filtro da sostituire e nessun olio da cambiare.",
    "Can one device supply two lasers?": "Un dispositivo può alimentare due laser?",
    "Yes. LISHI LASER is the only manufacturer offering a stable One-to-Two configuration. One mixing station feeds two laser machines at different power levels (e.g., 12kW + 20kW) simultaneously — no switching, no pressure drops.":
     "Sì. LISHI LASER è l'unico produttore che offre una configurazione Uno-a-Due stabile. Una stazione di miscelazione alimenta due macchine laser a diversi livelli di potenza (es. 12kW + 20kW) simultaneamente — nessuna commutazione, nessuna caduta di pressione.",
    "How is mixed gas different from air cutting?": "In cosa il gas misto è diverso dal taglio ad aria?",
    "Air cutting produces oxidized, rough edges and carries oil/water contamination risk that can burn expensive laser head lenses ($5,000–50,000). Mixed gas from pure liquid source delivers smooth, bright, burr-free edges — and protects your optics.":
     "Il taglio ad aria produce bordi ossidati e ruvidi e comporta rischi di contaminazione olio/acqua che possono bruciare costose lenti della testa laser ($5.000–50.000). Il gas misto da fonte liquida pura offre bordi lisci, luminosi e senza bave — e protegge l'ottica.",
    "How long does installation take?": "Quanto tempo richiede l'installazione?",
    "Installation is straightforward and typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "L'installazione è semplice e tipicamente completata entro un giorno. Il dispositivo si collega alla tua fornitura di gas liquido esistente e alla macchina laser. Forniamo guida dettagliata all'installazione per tutti i clienti.",

    # CTA
    "Ready to Boost Your Cutting Speed?": "Pronto ad Aumentare la Tua Velocità di Taglio?",
    "Connect one device to your laser machine and start cutting 3× faster today. Available for 6KW–60KW machines.":
     "Collega un dispositivo alla tua macchina laser e inizia a tagliare 3× più velocemente oggi. Disponibile per macchine 6KW–60KW.",
    "Contact Us →": "Contattaci →",
    "Get Free Consultation": "Consulenza Gratuita",

    # Footer
    "Brand-Authorized Overseas Market Operations Agent:": "Agente Autorizzato per le Operazioni sul Mercato Estero:",
    "© 2025 Jinan Euchio Machinery Co., Ltd. All rights reserved.": "© 2025 Jinan Euchio Machinery Co., Ltd. Tutti i diritti riservati.",
    "Product": "Prodotto",
    "Cutting Samples": "Campioni di Taglio",

    # Contact page
    "Get in Touch": "Contattaci",
    "Contact Us": "Contattaci",
    "Ready to boost your cutting speed? Send your laser machine details and we'll provide custom parameters and pricing.":
     "Pronto ad aumentare la tua velocità di taglio? Invia i dettagli della tua macchina laser e ti forniremo parametri e prezzi personalizzati.",
    "Email": "Email",
    "Reply within 24 hours": "Risposta entro 24 ore",
    "Phone / WeChat": "Telefono / WeChat",
    "WeChat: same number": "WeChat: stesso numero",
    "Company": "Azienda",
    "Product Brand": "Marchio Prodotto",
    "Mixed Gas Device — 13 years in laser cutting industry": "Dispositivo a Gas Misto — 13 anni nel settore del taglio laser",
    "Looking for a distributor?": "Cerchi un distributore?",
    "We are actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "Stiamo espandendo attivamente la nostra rete globale di agenti. Territori esclusivi disponibili per distributori qualificati.",
    "Agency Application →": "Richiesta Agenzia →",
    "Send Us a Message": "Inviaci un Messaggio",
    "Full Name *": "Nome e Cognome *",
    "John Doe": "Mario Rossi",
    "ABC Laser Co.": "ABC Laser S.r.l.",
    "john@company.com": "mario@azienda.it",
    "+1 555 123 4567": "+39 333 123 4567",
    "Country": "Paese",
    "e.g. USA, Germany, Brazil": "es. Italia, Germania, Francia",
    "Inquiry Type": "Tipo di Richiesta",
    "Select...": "Seleziona...",
    "Pricing & Quote": "Prezzi e Preventivo",
    "Technical Parameters": "Parametri Tecnici",
    "Distributor / Agency": "Distributore / Agenzia",
    "OEM / Customization": "OEM / Personalizzazione",
    "Other": "Altro",
    "Laser Machine Power": "Potenza Macchina Laser",
    "Select laser power...": "Seleziona potenza laser...",
    "Other / Multiple": "Altro / Multiplo",
    "Laser Machine Brand": "Marca Macchina Laser",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "es. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "Messaggio *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "Descrivi le tue esigenze di taglio — tipo materiale, spessore, configurazione gas attuale, ecc.",
    "Send Message →": "Invia Messaggio →",
    "Or reach us directly via": "O contattaci direttamente via",
    "for faster response.": "per una risposta più rapida.",
    "Your Message Has Been Sent!": "Messaggio Inviato con Successo!",
    "Thank you for your inquiry. We will respond within 24 hours.": "Grazie per la tua richiesta. Ti risponderemo entro 24 ore.",
    "Back to Home": "Torna alla Home",

    # Parameters page
    "Cutting Parameters": "Parametri di Taglio",
    "Detailed cutting parameters for different laser powers. All tests performed on real customer machines. Results verified by our engineering team.":
     "Parametri di taglio dettagliati per diverse potenze laser. Tutti i test eseguiti su macchine reali dei clienti. Risultati verificati dal nostro team di ingegneri.",
    "Thickness": "Spessore",
    "Speed Improvement": "Miglioramento Velocità",
    "Test Location": "Luogo Test",
    "Notes": "Note",
    "Mixed Gas Optimization": "Ottimizzazione Gas Misto",
    "Gas Consumption Comparison": "Confronto Consumo Gas",
    "Pure Nitrogen": "Azoto Puro",
    "Mixed gas": "Gas Misto",
    "Savings": "Risparmio",
    "per hour": "all'ora",
    "per day": "al giorno",
    "per month": "al mese",
    "per year": "all'anno",
    "Download Parameters": "Scarica Parametri",
    "Get Technical Support": "Supporto Tecnico",
    "How do I read the cutting parameters table?": "Come leggere la tabella dei parametri di taglio?",
    "The table shows cutting speed in meters per minute (m/min), mixed gas pressure in bar, and nozzle diameter in mm. Higher speeds mean better productivity. The speed improvement percentage shows the gain versus pure oxygen cutting.":
     "La tabella mostra la velocità di taglio in metri al minuto (m/min), la pressione del gas misto in bar e il diametro dell'ugello in mm. Velocità più alte significano migliore produttività. La percentuale di miglioramento velocità mostra il guadagno rispetto al taglio a ossigeno puro.",
    "Why does speed improvement decrease at very thick materials?": "Perché il miglioramento della velocità diminuisce su materiali molto spessi?",
    "At extreme thicknesses (30mm+), the limiting factor shifts from gas chemistry to laser power penetration. The mixed gas still provides benefits in edge quality and eliminates burrs, but the raw speed difference versus oxygen narrows because both processes are dominated by the laser beam's physical ability to penetrate the material.":
     "A spessori estremi (30mm+), il fattore limitante passa dalla chimica del gas alla potenza di penetrazione del laser. Il gas misto offre comunque benefici in qualità del bordo ed elimina le bave, ma la differenza di velocità rispetto all'ossigeno si riduce perché entrambi i processi sono dominati dalla capacità fisica del raggio laser di penetrare il materiale.",

    # Nav labels (short form)
    "Principle": "Principio",
    "Clients": "Clienti",

    # Hero (exact source text)
    "The LISHI LASER Mixed Gas Device delivers micro-oxygen cutting for high-power laser machines (12KW–60KW). No burrs, less gas consumption, and significantly faster cutting speeds.":
     "Il Dispositivo a Gas Misto LISHI LASER offre taglio a micro-ossigeno per macchine laser ad alta potenza (12KW–60KW). Nessuna bava, minor consumo di gas e velocità di taglio notevolmente superiori.",
    "Faster than O₂": "Più veloce dell'O₂",
    "Burrs on cut surface": "Nessuna bava sulla superficie",
    "Less gas than N₂": "Meno gas dell'N₂",
    "in Laser Metal Cutting Industry": "nel Settore del Taglio Laser dei Metalli",

    # Advantages heading
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "Perché Scegliere Gas Misto invece di O₂, N₂ o Aria?",
    "Reduce nitrogen consumption by 33% while eliminating burrs on laser cutting carbon steel. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and other major brands.":
     "Riduci il consumo di azoto del 33% eliminando le bave nel taglio laser dell'acciaio al carbonio. Il nostro sistema di alimentazione gas esente da manutenzione è compatibile con HAN'S, DNE, PENTA, LEAD, HSG, BODOR e altri principali marchi.",

    # Advantage cards — exact source text
    "Increase laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas vs only 2–3m/min with O₂.":
     "Aumenta la velocità di taglio laser fino a 3× rispetto al taglio a ossigeno. Esempio: acciaio al carbonio 8mm a 16m/min con gas misto vs solo 2–3m/min con O₂.",
    "Unlike nitrogen cutting which produces burrs on plates ≥8mm (12kW) or ≥10mm (20kW), mixed gas cutting produces clean, burr-free surfaces on carbon steel — no secondary grinding needed.":
     "A differenza del taglio ad azoto che produce bave su lamiere ≥8mm (12kW) o ≥10mm (20kW), il taglio a gas misto produce superfici pulite e senza bave su acciaio al carbonio — nessuna molatura secondaria necessaria.",
    "Reduce Gas Costs": "Riduci i Costi del Gas",
    "Reduce nitrogen consumption by 33–50% compared to pure N₂ cutting. Cost comparison: mixed gas saves significantly vs air compressor when factoring in maintenance-free operation.":
     "Riduci il consumo di azoto del 33–50% rispetto al taglio con N₂ puro. Confronto costi: il gas misto fa risparmiare significativamente rispetto al compressore d'aria considerando il funzionamento esente da manutenzione.",
    "Power consumption: only 2 kWh / 24 hours. Unlike air compressors requiring filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Consumo energetico: solo 2 kWh / 24 ore. A differenza dei compressori d'aria che richiedono cambio filtri/olio ogni 3.000 ore, la nostra apparecchiatura gas laser industriale è esente da manutenzione.",
    "One-to-Two Laser Setup": "Configurazione Uno-a-Due",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines of different power levels simultaneously.":
     "L'unico produttore con apparecchiatura a gas misto uno-a-due stabile. Una stazione di miscelazione gas industriale alimenta due macchine laser di diversi livelli di potenza simultaneamente.",
    "Lens Protection": "Protezione Lenti",
    "Air compressors risk oil/water contamination burning laser head lenses ($5,000–$50,000 loss). Our pure liquid gas source keeps your optical system 100% safe — pure liquid gas source":
     "I compressori d'aria rischiano la contaminazione olio/acqua che brucia le lenti della testa laser (perdita di $5.000–$50.000). La nostra fonte di gas liquido puro mantiene il sistema ottico 100% sicuro.",

    # Principle section — device diagram labels
    "Converts liquid gases to gaseous form": "Converte i gas liquidi in forma gassosa",
    "Laser Cutting Machine": "Macchina da Taglio Laser",
    "Cutting Effect": "Effetto di Taglio",
    "High cutting speed + zero burrs. After installation, adjust ratio between N₂ 95% and O₂ 5% for different board thicknesses. Built-in program analyzes usage ratio and records gas purity requirements.":
     "Alta velocità di taglio + zero bave. Dopo l'installazione, regola il rapporto tra N₂ 95% e O₂ 5% per diversi spessori lamiera. Il programma integrato analizza il rapporto di utilizzo e registra i requisiti di purezza del gas.",
    "Works with all major brands: HAN'S, DNE, PENTA, LEAD, HSG, and more. Compatible with BODOR, KIMLA, MESSER, and other global brands.":
     "Funziona con tutti i principali marchi: HAN'S, DNE, PENTA, LEAD, HSG e altri. Compatibile con BODOR, KIMLA, MESSER e altri marchi globali.",
    "Wide Compatibility": "Ampia Compatibilità",

    # Air vs Mixed Gas section
    "Air Seems Free. The Reality Is Not.": "L'Aria Sembra Gratis. La Realtà Non Lo È.",
    "HIGH MAINTENANCE COST": "COSTO DI MANUTENZIONE ELEVATO",
    "Most users choose air compressor for low upfront cost, but three hidden costs eat into your profit.":
     "La maggior parte degli utenti sceglie il compressore d'aria per il basso costo iniziale, ma tre costi nascosti erodono il profitto.",
    "High Maintenance Cost": "Costo di Manutenzione Elevato",
    "Filter replacement every 500-1000 hours": "Sostituzione filtri ogni 500-1000 ore",
    "Oil change and system flush": "Cambio olio e lavaggio sistema",
    "Unexpected downtime for repairs": "Fermi macchina imprevisti per riparazioni",
    "2 kWh/24h electricity — basically maintenance-free": "2 kWh/24h di elettricità — praticamente esente da manutenzione",
    "~$73/year in electricity": "~$73/anno di elettricità",
    "POOR CUT QUALITY": "SCARSA QUALITÀ DI TAGLIO",
    "Poor Cut Quality": "Scarsa Qualità di Taglio",
    "Dark oxidation layer on cut surface": "Strato di ossidazione scura sulla superficie di taglio",
    "Burrs and dross requiring rework": "Bave e scorie che richiedono rilavorazione",
    "Extra grinding/polishing labor": "Lavoro extra di molatura/lucidatura",
    "Cannot deliver premium jobs": "Impossibile consegnare lavori premium",
    "Silver-white surface, zero burrs": "Superficie bianco-argento, zero bave",
    "Ready for immediate delivery": "Pronto per la consegna immediata",
    "LENS CONTAMINATION RISK": "RISCHIO CONTAMINAZIONE LENTI",
    "Lens Contamination": "Contaminazione Lenti",
    "Lens Contamination Risk": "Rischio Contaminazione Lenti",
    "Oil/water in compressed air": "Olio/acqua nell'aria compressa",
    "Burns laser head protection lens": "Brucia la lente di protezione della testa laser",
    "Lens replacement: $200–500 each time": "Sostituzione lente: $200–500 ogni volta",
    "Unplanned production stop": "Fermo produzione non pianificato",
    "100% safe — pure liquid gas source": "100% sicuro — fonte di gas liquido puro",
    "Zero optical risk": "Zero rischio ottico",
    "LISHI Mixed Gas: The True Cost Saver": "LISHI Gas Misto: Il Vero Riduttore di Costi",
    "While air seems free, your real cost is in maintenance, rework, and lens replacement. Mixed gas costs less in the long run — and delivers superior quality.":
     "Anche se l'aria sembra gratis, il costo reale è in manutenzione, rilavorazioni e sostituzione lenti. Il gas misto costa meno a lungo termine — e offre qualità superiore.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air": "Confronto Prestazioni: Gas Misto vs O₂ vs N₂ vs Aria",
    "3× Faster": "3× Più Veloce",
    "3× faster (e.g. 16m/min @ 8mm CS)": "3× più veloce (es. 16m/min @ 8mm AC)",
    "30% slower than mixed gas": "30% più lento del gas misto",
    "May have burrs on thick plates": "Possibili bave su lamiere spesse",
    "Similar to mixed gas": "Simile al gas misto",
    "Smooth, no burrs": "Liscio, senza bave",
    "Some burrs during pierce": "Qualche bava durante la perforazione",
    "Best for small holes": "Migliore per piccoli fori",
    "Less than 1/3 of N₂": "Meno di 1/3 dell'N₂",
    "No pipeline contamination": "Nessuna contaminazione tubazioni",
    "Oil/water risk from compressor": "Rischio olio/acqua dal compressore",

    # Global section
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Filmati di taglio reali da utilizzatori finali in tutto il mondo. Nessun abbellimento — dati reali, prestazioni reali.",
    "Our Gas Flows.": "Il Nostro Gas Scorre.",
    "From coastal megafactories to inland workshops, mixed gas technology now powers laser cutters on four continents — and the footprint is expanding every quarter.":
     "Dalle megafabbriche costiere alle officine interne, la tecnologia a gas misto ora alimenta macchine da taglio laser in quattro continenti — e la presenza si espande ogni trimestre.",
    "The Next Territory Is Still Open.": "Il Prossimo Territorio è Ancora Disponibile.",
    "Exclusive distributor partnerships available in select regions. Ship one container, build your market.":
     "Partenariati di distribuzione esclusivi disponibili in regioni selezionate. Spedisci un container, costruisci il tuo mercato.",

    # Hero CTA / Buttons
    "Get detailed cutting data tailored to your 12KW–60KW laser setup.":
     "Ottieni dati di taglio dettagliati su misura per il tuo setup laser 12KW–60KW.",
    "Connect one device to your laser machine and start cutting 3× faster today. Available for 6KW–60KW machines.":
     "Collega un dispositivo alla tua macchina laser e inizia a tagliare 3× più velocemente oggi. Disponibile per macchine 6KW–60KW.",
    "Ready to Increase Your Cutting Speed?": "Pronto ad Aumentare la Tua Velocità di Taglio?",
    "Calculate Your Laser Cutting Gas Cost Savings": "Calcola il Risparmio sui Costi del Gas da Taglio Laser",

    # Samples
    "Dual power setup, one machine feeds two — 33% less gas, zero compromise on speed":
     "Configurazione doppia potenza, una macchina alimenta due — 33% di gas in meno, nessun compromesso sulla velocità",
    "Thick plates, no burrs. 10–14 m/min on 10mm, previously only achievable with O₂":
     "Lamiere spesse, zero bave. 10–14 m/min su 10mm, prima possibile solo con O₂",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas delivers":
     "Taglio ultra-spesso a 3,5 m/min. Dove l'N₂ fatica, il gas misto eccelle",
    "Smooth aluminum edges, no oxidation. Faster than air, cleaner than N₂":
     "Bordi in alluminio lisci, zero ossidazione. Più veloce dell'aria, più pulito dell'N₂",
    "Precision aluminum cutting with micro-oxygen — speed and quality in one pass":
     "Taglio alluminio di precisione con micro-ossigeno — velocità e qualità in un singolo passaggio",
    "Paper-thin aluminum, zero burn-through. Mixed gas enables what N₂ cannot":
     "Alluminio sottile come carta, zero bruciature. Il gas misto permette ciò che l'N₂ non può",

    # FAQ — exact source text
    "What is a mixed gas device and how does it work?":
     "Cos'è un dispositivo a gas misto e come funziona?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Un dispositivo a gas misto converte azoto liquido (N₂) e ossigeno liquido (O₂) in una miscela di gas N₂/O₂ precisamente calibrata (tipicamente 95%/5%). Questa miscela micro-ossigeno è utilizzata come gas ausiliario nel taglio laser ad alta potenza, offrendo velocità di taglio 3× superiori sull'acciaio al carbonio rispetto all'ossigeno puro, eliminando completamente le bave.",
    "Is it compatible with my laser machine?":
     "È compatibile con la mia macchina laser?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands, including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Sì. Il Dispositivo a Gas Misto LISHI LASER funziona con tutti i principali marchi laser, inclusi HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA e MESSER. Supporta macchine da 12kW a 60kW. Se la tua macchina utilizza connessioni standard per gas ausiliario, è compatibile.",
    "What thicknesses can it cut?":
     "Quali spessori può tagliare?",
    "What thickness can it cut?":
     "Quali spessori può tagliare?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "La gamma di taglio dipende dalla potenza del laser: 12kW gestisce fino a 16mm, 20kW fino a 25mm, 30kW fino a 30mm e 60kW fino a 40mm di acciaio al carbonio. Taglia anche acciaio inossidabile e alluminio. Tabelle dettagliate dei parametri di taglio sono disponibili nella nostra pagina parametri qui sotto.",
    "How much can I save on gas costs?":
     "Quanto posso risparmiare sui costi del gas?",
    "Mixed gas reduces nitrogen consumption by approximately 33–50% compared to pure N₂ cutting. Additionally, the device consumes only 2 kWh per 24 hours — essentially maintenance-free. The optimized mixing ratio means more cutting per unit of gas.":
     "Il gas misto riduce il consumo di azoto di circa il 33–50% rispetto al taglio con N₂ puro. Inoltre, il dispositivo consuma solo 2 kWh ogni 24 ore — essenzialmente esente da manutenzione. Il rapporto di miscelazione ottimizzato significa più taglio per unità di gas.",
    "Does the device require regular maintenance?":
     "Il dispositivo richiede manutenzione regolare?",
    "No. Unlike air compressors that need filter/oil changes every 500–3,000 hours, the LISHI Mixed Gas Device is maintenance-free. There are no moving parts to wear out, no filters to replace, and no oil to change.":
     "No. A differenza dei compressori d'aria che necessitano cambio filtri/olio ogni 500–3.000 ore, il Dispositivo a Gas Misto LISHI è esente da manutenzione. Non ci sono parti mobili da usurare, nessun filtro da sostituire e nessun olio da cambiare.",
    "Can one device serve two laser machines?":
     "Un dispositivo può servire due macchine laser?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station feeds two laser machines at different power levels (e.g., 12kW + 20kW) simultaneously — no switching, no pressure drops.":
     "Sì. LISHI LASER è l'unico produttore che offre una configurazione uno-a-due stabile. Una stazione di miscelazione alimenta due macchine laser a diversi livelli di potenza (es. 12kW + 20kW) simultaneamente — nessuna commutazione, nessuna caduta di pressione.",
    "How is mixed gas different from air cutting?":
     "In cosa il gas misto è diverso dal taglio ad aria?",
    "Air cutting produces oxidized, rough edges and carries oil/water contamination risk that can burn expensive laser head lenses ($5,000–$50,000). Mixed gas from pure liquid source delivers smooth, bright, burr-free edges — and protects your optics.":
     "Il taglio ad aria produce bordi ossidati e ruvidi e comporta rischi di contaminazione olio/acqua che possono bruciare costose lenti della testa laser ($5.000–$50.000). Il gas misto da fonte liquida pura offre bordi lisci, luminosi e senza bave — e protegge l'ottica.",
    "How long does installation take?":
     "Quanto tempo richiede l'installazione?",
    "Installation is straightforward — typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "L'installazione è semplice — tipicamente completata entro un giorno. Il dispositivo si collega alla tua fornitura di gas liquido esistente e alla macchina laser. Forniamo guida dettagliata all'installazione per tutti i clienti.",

    # ROI
    "Actual Cutting Time (Beam-On %)": "Tempo di Taglio Effettivo (Raggio Attivo %)",
    "Typical shops run 40–70% — the rest is loading, piercing, idle.":
     "Le officine tipiche operano al 40–70% — il resto è carico, perforazione, inattività.",
    "Monthly N₂ Cost (USD)": "Costo Mensile N₂ (USD)",
    "Your current monthly nitrogen expense (USD)": "La tua spesa mensile attuale in azoto (USD)",
    "Your selling price minus material cost (USD)": "Il tuo prezzo di vendita meno il costo del materiale (USD)",
    "Theoretical upper bound based on your inputs. Real-world results depend on job mix, nesting efficiency, and machine uptime.":
     "Limite superiore teorico basato sui tuoi input. I risultati reali dipendono dal mix di lavoro, efficienza di nesting e disponibilità macchina.",
    "USD/year in nitrogen savings": "USD/anno in risparmio di azoto",
    "Want the full parameter table for your specific machine?":
     "Vuoi la tabella completa dei parametri per la tua macchina specifica?",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER Dispositivo a Gas Misto"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER Contatto"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "Produzione Industriale > Apparecchiatura Taglio Laser"',

    # Misc
    "in Laser Metal Cutting Industry": "nel Settore del Taglio Laser dei Metalli",
    "Laser Machine": "Macchina Laser",
    "micro-oxygen laser cutting technology": "tecnologia di taglio laser a micro-ossigeno",
}

# ---- GERMAN ----
DE = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "LISHI LASER Mischgasgerät für 12KW-60KW Laserschneidmaschinen. 3× schnellere Schnittgeschwindigkeit, keine Grate, 33% weniger Gasverbrauch. N2/O2-Verhältnistechnologie für Kohlenstoffstahlschneiden.",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Mischgasgerät | 3× Schnelleres Laserschneiden",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Mischgasgerät für 12KW-60KW Laserschneidmaschinen. 3× schnellere Schnittgeschwindigkeit, keine Grate, 33% weniger Gasverbrauch. N2/O2-Verhältnistechnologie.",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "Laserschneiden Gasmischer, Stickstoff-Sauerstoff-Mischgerät, Mikro-Sauerstoff-Laserschneiden, Kohlenstoffstahl-Laserschneiden, Hochleistungslaser 12kW 60kW, Mischgas vs Luftkompressor, Laserschneidgrate beseitigen, Stickstoffverbrauch reduzieren, Han's Laser Gasmischer, industrielle Lasergasausrüstung, Eins-zu-Zwei-Lasergaskonfiguration, Schutzgasoptimierung",
    "LISHI LASER Mixed Gas Device": "LISHI LASER Mischgasgerät",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "LISHI LASER Mischgasgerät Preise und Angebote. Kompatibel mit allen großen Lasermarken (HANS, DNE, PENTA, LEAD, HSG, BODOR). Weltweiter Versand verfügbar.",
    "Request a quote for LISHI LASER mixed gas cutting equipment. Compatible with all major laser brands. Global shipping available.":
     "Fordern Sie ein Angebot für LISHI LASER Mischgas-Schneidausrüstung an. Kompatibel mit allen großen Lasermarken. Weltweiter Versand verfügbar.",
    "LISHI LASER Contact | Get Mixed Gas Device Quote":
     "LISHI LASER Kontakt | Mischgasgerät Angebot Erhalten",
    "laser cutting gas equipment quote, mixed gas device distributor, laser cutting equipment manufacturer, HANS laser compatible gas":
     "Laserschneidgasanlage Angebot, Mischgasgerät Vertriebspartner, Laserschneidausrüstung Hersteller, HANS Laser kompatibles Gas",
    "LISHI LASER Contact": "LISHI LASER Kontakt",

    # Nav + UI
    "Skip to content": "Zum Inhalt springen",
    "Home": "Startseite",
    "Advantages": "Vorteile",
    "Samples": "Proben",
    "Customers": "Kunden",
    "Blog": "Blog",
    "Contact": "Kontakt",
    "Gas Mixing Technology": "Gasmischtechnologie",
    "Menu toggle": "Menü",
    "How It Works": "Funktionsweise",
    "Parameters": "Parameter",
    "Principle": "Prinzip",
    "Clients": "Kunden",

    # Hero
    'Cut <span class="accent">3× Faster</span><br>with Mixed Gas Technology':
     'Schneiden Sie <span class="accent">3× Schneller</span><br>mit Mischgastechnologie',
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "N₂/O₂ Mischgaslösung für 12KW-60KW Laserschneidmaschinen",
    "3× Faster than O₂": "3× Schneller als O₂",
    "Zero Burrs": "Keine Grate",
    "33% Less N₂": "33% Weniger N₂",
    "13 Years in Laser Metal Cutting": "13 Jahre im Laser-Metallschneiden",
    "The LISHI LASER Mixed Gas Device delivers micro-oxygen cutting for high-power laser machines (12KW–60KW). No burrs, less gas consumption, and significantly faster cutting speeds.":
     "Das LISHI LASER Mischgasgerät ermöglicht Mikro-Sauerstoff-Schneiden für Hochleistungslasermaschinen (12KW–60KW). Keine Grate, weniger Gasverbrauch und deutlich höhere Schnittgeschwindigkeiten.",
    "Get Quote →": "Angebot Erhalten →",
    "View Parameters": "Parameter Anzeigen",
    "Faster than O₂": "Schneller als O₂",
    "Burrs on cut surface": "Keine Grate an der Schnittfläche",
    "Less gas than N₂": "Weniger Gas als N₂",
    "in Laser Metal Cutting Industry": "in der Laser-Metallschneidbranche",

    # Principle
    "What is a Mixed Gas Device?": "Was ist ein Mischgasgerät?",
    "Our nitrogen oxygen mixing device uses": "Unser Stickstoff-Sauerstoff-Mischgerät verwendet",
    "to produce precisely calibrated N₂/O₂ mixed gas — eliminating burrs on carbon steel while delivering 3× faster cutting speed versus traditional oxygen cutting. Supports high-power laser machines from 12kW to 60kW.":
     "um präzise kalibriertes N₂/O₂-Mischgas zu erzeugen — beseitigt Grate auf Kohlenstoffstahl und liefert 3× schnellere Schnittgeschwindigkeit gegenüber herkömmlichem Sauerstoffschneiden. Unterstützt Hochleistungslaser von 12kW bis 60kW.",
    "Micro-oxygen laser cutting technology": "Mikro-Sauerstoff-Laserschneidtechnologie",
    "Liquid N₂ + Liquid O₂": "Flüssig-N₂ + Flüssig-O₂",
    "Raw materials stored in tanks, pressure 20–25 bar": "Rohstoffe in Tanks gelagert, Druck 20–25 bar",
    "Vaporizer": "Verdampfer",
    "Converts liquid gases to gas form": "Wandelt Flüssiggase in Gasform um",
    "Mixed Gas Device": "Mischgasgerät",
    "Stable pressure + proportional mixing → N₂ 95% / O₂ 5%": "Stabiler Druck + proportionale Mischung → N₂ 95% / O₂ 5%",
    "To Laser Machine": "Zur Lasermaschine",
    "Output: 12–16 bar, flow rate up to 200m³/h": "Ausgang: 12–16 bar, Durchflussrate bis 200m³/h",
    "Input: N₂ + O₂ at 20–25 bar. Output: N₂ purity ~95%, pressure 12–16 bar, max flow 200m³/h. Compact gas tank (capacity >3m³).":
     "Eingang: N₂ + O₂ bei 20–25 bar. Ausgang: N₂-Reinheit ~95%, Druck 12–16 bar, max. Durchfluss 200m³/h. Kompakter Gastank (Kapazität >3m³).",
    "Device Dimensions": "Geräteabmessungen",
    "800mm × 350mm × 1100mm, weight 90kg. One device simultaneously supports two laser machines (One-to-Two configuration).":
     "800mm × 350mm × 1100mm, Gewicht 90kg. Ein Gerät versorgt gleichzeitig zwei Lasermaschinen (Eins-zu-Zwei-Konfiguration).",
    "High cutting speed + zero burrs. After installation, simply adjust the N₂ 95% to O₂ 5% ratio for different sheet thicknesses. The built-in program makes operation intuitive.":
     "Hohe Schnittgeschwindigkeit + keine Grate. Nach der Installation einfach das N₂ 95% zu O₂ 5% Verhältnis für verschiedene Blechdicken anpassen. Das eingebaute Programm macht die Bedienung intuitiv.",
    "Wide Compatibility": "Breite Kompatibilität",
    "Broad Compatibility": "Breite Kompatibilität",
    "Works with all major brands: HAN'S, DNE, PENTA, LEAD, HSG and more. Compatible with BODOR, KIMLA, MESSER and other global brands.":
     "Funktioniert mit allen großen Marken: HAN'S, DNE, PENTA, LEAD, HSG und mehr. Kompatibel mit BODOR, KIMLA, MESSER und anderen globalen Marken.",
    "Converts liquid gases to gaseous form": "Wandelt Flüssiggase in Gasform um",
    "Laser Cutting Machine": "Laserschneidmaschine",
    "Laser Machine": "Lasermaschine",
    "Cutting Effect": "Schneideffekt",

    # Advantages
    "Why Mixed Gas Instead of O₂, N₂ or Air?": "Warum Mischgas statt O₂, N₂ oder Luft?",
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "Warum Mischgas statt O₂, N₂ oder Luft wählen?",
    "Eliminate burrs in carbon steel laser cutting while cutting nitrogen consumption by 33%. Our maintenance-free gas delivery system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Beseitigen Sie Grate beim Laserschneiden von Kohlenstoffstahl und reduzieren Sie den Stickstoffverbrauch um 33%. Unser wartungsfreies Gasversorgungssystem ist mit HAN'S, DNE, PENTA, LEAD, HSG, BODOR und allen anderen großen Marken kompatibel.",
    "Reduce nitrogen consumption by 33% while eliminating burrs on laser cutting carbon steel. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and other major brands.":
     "Reduzieren Sie den Stickstoffverbrauch um 33% und beseitigen Sie Grate beim Laserschneiden von Kohlenstoffstahl. Unser wartungsfreies Gasversorgungssystem ist mit HAN'S, DNE, PENTA, LEAD, HSG, BODOR und anderen großen Marken kompatibel.",
    "Competitive Advantage": "Wettbewerbsvorteil",
    "3× Faster Cutting": "3× Schnelleres Schneiden",
    "Boost laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Steigern Sie die Laserschneidgeschwindigkeit um das 3-fache im Vergleich zum Sauerstoffschneiden. Beispiel: 8mm Kohlenstoffstahl mit 16m/min mit Mischgas, nur 2–3m/min mit O₂.",
    "Increase laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas vs only 2–3m/min with O₂.":
     "Steigern Sie die Laserschneidgeschwindigkeit um das 3-fache im Vergleich zum Sauerstoffschneiden. Beispiel: 8mm Kohlenstoffstahl mit 16m/min mit Mischgas vs. nur 2–3m/min mit O₂.",
    "Eliminate Burrs": "Grate Beseitigen",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cutting edges requiring no secondary grinding.":
     "Kontrollierte Mikro-Sauerstoffumgebung gewährleistet vollständige Verbrennung. Ergebnis: glatte, gratfreie Schnittkanten ohne Nachschleifen.",
    "Unlike nitrogen cutting which produces burrs on plates ≥8mm (12kW) or ≥10mm (20kW), mixed gas cutting produces clean, burr-free surfaces on carbon steel — no secondary grinding needed.":
     "Anders als beim Stickstoffschneiden, das bei Blechen ≥8mm (12kW) oder ≥10mm (20kW) Grate erzeugt, liefert das Mischgasschneiden saubere, gratfreie Oberflächen auf Kohlenstoffstahl — kein Nachschleifen nötig.",
    "Cut Gas Costs": "Gaskosten Senken",
    "Reduce nitrogen consumption by 33–50% versus pure N₂ cutting. Cost comparison: mixed gas costs significantly less than air compressors when factoring in maintenance-free operation.":
     "Reduzieren Sie den Stickstoffverbrauch um 33–50% gegenüber reinem N₂-Schneiden. Kostenvergleich: Mischgas ist deutlich günstiger als Luftkompressoren unter Berücksichtigung des wartungsfreien Betriebs.",
    "Reduce Gas Costs": "Gaskosten Senken",
    "Reduce nitrogen consumption by 33–50% compared to pure N₂ cutting. Cost comparison: mixed gas saves significantly vs air compressor when factoring in maintenance-free operation.":
     "Reduzieren Sie den Stickstoffverbrauch um 33–50% im Vergleich zu reinem N₂-Schneiden. Kostenvergleich: Mischgas spart erheblich gegenüber Luftkompressor bei Berücksichtigung des wartungsfreien Betriebs.",
    "Maintenance-Free": "Wartungsfrei",
    "Power consumption: only 2 kWh per 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Stromverbrauch: nur 2 kWh pro 24 Stunden. Anders als Luftkompressoren, die alle 3.000 Stunden Filter-/Ölwechsel benötigen, ist unsere industrielle Lasergasausrüstung wartungsfrei.",
    "Power consumption: only 2 kWh / 24 hours. Unlike air compressors requiring filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Stromverbrauch: nur 2 kWh / 24 Stunden. Anders als Luftkompressoren, die alle 3.000 Stunden Filter-/Ölwechsel benötigen, ist unsere industrielle Lasergasausrüstung wartungsfrei.",
    "One-to-Two Laser Setup": "Eins-zu-Zwei-Laserkonfiguration",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines at different power levels simultaneously — no switching required.":
     "Der einzige Hersteller mit stabiler Eins-zu-Zwei-Mischgasausrüstung. Eine industrielle Gasmischstation versorgt zwei Lasermaschinen mit unterschiedlichen Leistungsstufen gleichzeitig — keine Umschaltung nötig.",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines of different power levels simultaneously.":
     "Der einzige Hersteller mit stabiler Eins-zu-Zwei-Mischgasausrüstung. Eine industrielle Gasmischstation versorgt zwei Lasermaschinen unterschiedlicher Leistungsstufen gleichzeitig.",
    "Lens Protection": "Linsenschutz",
    "Air compressors carry oil/water contamination risk that can burn laser head lenses ($5,000–50,000 loss). Our pure liquid gas source keeps your optical system pristine.":
     "Luftkompressoren bergen das Risiko von Öl-/Wasserverschmutzung, die Laserkopflinsen zerstören kann ($5.000–50.000 Verlust). Unsere reine Flüssiggasquelle hält Ihr optisches System makellos.",
    "Air compressors risk oil/water contamination burning laser head lenses ($5,000–$50,000 loss). Our pure liquid gas source keeps your optical system 100% safe — pure liquid gas source":
     "Luftkompressoren riskieren Öl-/Wasserverschmutzung, die Laserkopflinsen zerstört ($5.000–$50.000 Verlust). Unsere reine Flüssiggasquelle hält Ihr optisches System 100% sicher.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air": "Leistungsvergleich: Mischgas vs. O₂ vs. N₂ vs. Luft",
    "Factor": "Faktor",
    "Mixed Gas": "Mischgas",
    "O₂ (Oxygen)": "O₂ (Sauerstoff)",
    "N₂ (Nitrogen)": "N₂ (Stickstoff)",
    "Air": "Luft",
    "Cutting Speed": "Schnittgeschwindigkeit",
    "3× faster (e.g. 16m/min @ 8mm CS)": "3× schneller (z.B. 16m/min @ 8mm KS)",
    "30% slower than mixed gas": "30% langsamer als Mischgas",
    "May have burrs on thick plates": "Kann Grate auf dicken Blechen haben",
    "3× Faster": "3× Schneller",
    "Similar to mixed gas": "Ähnlich wie Mischgas",
    "Cut Surface": "Schnittfläche",
    "Smooth, burr-free": "Glatt, gratfrei",
    "Smooth, no burrs": "Glatt, keine Grate",
    "Oxidized, rough edges": "Oxidiert, raue Kanten",
    "Contaminated, rough": "Verschmutzt, rau",
    "Gas Consumption": "Gasverbrauch",
    "1/3 less than N₂": "1/3 weniger als N₂",
    "Less than 1/3 of N₂": "Weniger als 1/3 von N₂",
    "Similar total": "Ähnliche Gesamtmenge",
    "High": "Hoch",
    "Very high (compressor)": "Sehr hoch (Kompressor)",
    "Power Cost": "Stromkosten",
    "2 kWh/24h": "2 kWh/24h",
    "Small Hole Piercing": "Kleinloch-Perforation",
    "Excellent — clean & fast": "Ausgezeichnet — sauber & schnell",
    "Some burr during piercing": "Etwas Grat beim Perforieren",
    "Some burrs during pierce": "Etwas Grat beim Perforieren",
    "Best for small holes": "Am besten für kleine Löcher",
    "Equipment Protection": "Geräteschutz",
    "No pipeline contamination": "Keine Rohrleitungsverschmutzung",
    "Oil/water risk": "Öl-/Wasserrisiko",
    "Oil/water risk from compressor": "Öl-/Wasserrisiko vom Kompressor",

    # ROI
    "ROI Calculator": "ROI-Rechner",
    "Calculator": "Rechner",
    "Calculate Your Laser Cutting Gas Cost Savings": "Berechnen Sie Ihre Laserschneid-Gaskosteneinsparungen",
    "See how much you could save with LISHI LASER mixed gas technology. Cut nitrogen consumption, eliminate burrs on carbon steel, and boost throughput.":
     "Sehen Sie, wie viel Sie mit LISHI LASER Mischgastechnologie sparen können. Reduzieren Sie den Stickstoffverbrauch, beseitigen Sie Grate auf Kohlenstoffstahl und steigern Sie den Durchsatz.",
    "Machine Power": "Maschinenleistung",
    "Material Thickness": "Materialdicke",
    "Daily Work Hours": "Tägliche Arbeitsstunden",
    "Actual Cutting Time (Beam On %)": "Tatsächliche Schneidzeit (Strahl-An-%)",
    "Typical shops run 40–70% — remaining time is loading, piercing, idle.": "Typische Betriebe arbeiten mit 40–70% — die restliche Zeit ist Laden, Perforieren, Leerlauf.",
    "Profit Per Meter (USD/m)": "Gewinn pro Meter (USD/m)",
    "Your selling price minus material cost (USD)": "Ihr Verkaufspreis abzüglich Materialkosten (USD)",
    "Monthly N₂ Cost (USD)": "Monatliche N₂-Kosten (USD)",
    "Your current monthly nitrogen spend (USD)": "Ihre aktuellen monatlichen Stickstoffkosten (USD)",
    "Estimated Annual Profit Increase (USD)": "Geschätzte jährliche Gewinnsteigerung (USD)",
    "in nitrogen savings": "an Stickstoffeinsparungen",
    "Theoretical ceiling based on your inputs. Real results depend on job mix, nesting efficiency and machine uptime.":
     "Theoretische Obergrenze basierend auf Ihren Eingaben. Reale Ergebnisse hängen vom Auftragsmix, der Verschachtelungseffizienz und der Maschinenverfügbarkeit ab.",
    "Want the full parameter table for your specific machine?": "Möchten Sie die vollständige Parametertabelle für Ihre spezifische Maschine?",
    "Get detailed cutting data tailored to your 12KW–60KW laser setup.": "Erhalten Sie detaillierte Schneiddaten, abgestimmt auf Ihre 12KW–60KW Laserkonfiguration.",
    "Get Free Parameters →": "Kostenlose Parameter Erhalten →",
    "Or contact us directly:": "Oder kontaktieren Sie uns direkt:",
    "Actual Cutting Time (Beam-On %)": "Tatsächliche Schneidzeit (Strahl-An-%)",
    "Typical shops run 40–70% — the rest is loading, piercing, idle.": "Typische Betriebe arbeiten mit 40–70% — der Rest ist Laden, Perforieren, Leerlauf.",
    "Your selling price minus material cost (USD)": "Ihr Verkaufspreis abzüglich Materialkosten (USD)",
    "Your current monthly nitrogen expense (USD)": "Ihre aktuellen monatlichen Stickstoffkosten (USD)",
    "Theoretical upper bound based on your inputs. Real-world results depend on job mix, nesting efficiency, and machine uptime.":
     "Theoretische Obergrenze basierend auf Ihren Eingaben. Praktische Ergebnisse hängen vom Auftragsmix, der Verschachtelungseffizienz und der Maschinenverfügbarkeit ab.",
    "USD/year in nitrogen savings": "USD/Jahr an Stickstoffeinsparungen",

    # Air vs Mixed
    "Why Air Compressors Cost More": "Warum Luftkompressoren Mehr Kosten",
    "Air Looks Free. It Isn't.": "Luft Sieht Kostenlos Aus. Ist Sie Nicht.",
    "Most users pick an air compressor for the low upfront cost — but three hidden costs eat your margin.":
     "Die meisten Anwender wählen einen Luftkompressor wegen der niedrigen Anschaffungskosten — aber drei versteckte Kosten schmälern Ihre Marge.",
    "HIGH MAINTENANCE COST": "HOHE WARTUNGSKOSTEN",
    "High Maintenance Cost": "Hohe Wartungskosten",
    "Filter replacement every 500-1000 hours": "Filterwechsel alle 500-1000 Stunden",
    "Oil changes and system flushing": "Ölwechsel und Systemspülung",
    "Oil change and system flush": "Ölwechsel und Systemspülung",
    "Unexpected repair downtime": "Unerwartete Reparaturausfallzeiten",
    "Unexpected downtime for repairs": "Unerwartete Ausfallzeiten für Reparaturen",
    "2 kWh/24h — near zero maintenance": "2 kWh/24h — nahezu keine Wartung",
    "2 kWh/24h electricity — basically maintenance-free": "2 kWh/24h Strom — praktisch wartungsfrei",
    "~$73/year electricity": "~$73/Jahr Strom",
    "~$73/year in electricity": "~$73/Jahr an Strom",
    "POOR CUT QUALITY": "SCHLECHTE SCHNITTQUALITÄT",
    "Poor Cut Quality": "Schlechte Schnittqualität",
    "Dark oxidation layer on cut surface": "Dunkle Oxidationsschicht auf der Schnittfläche",
    "Burrs and slag requiring rework": "Grate und Schlacke, die Nacharbeit erfordern",
    "Burrs and dross requiring rework": "Grate und Schlacke, die Nacharbeit erfordern",
    "Extra grinding/polishing labor": "Zusätzlicher Schleif-/Polieraufwand",
    "Cannot deliver premium jobs": "Kann keine Premium-Aufträge liefern",
    "Silver-white surface, zero burrs": "Silberweiße Oberfläche, keine Grate",
    "Ready to ship immediately": "Sofort versandfertig",
    "Ready for immediate delivery": "Sofort lieferbereit",
    "LENS CONTAMINATION RISK": "LINSENVERSCHMUTZUNGSRISIKO",
    "Lens Contamination Risk": "Linsenverschmutzungsrisiko",
    "Lens Contamination": "Linsenverschmutzung",
    "Oil/water in compressed air": "Öl/Wasser in der Druckluft",
    "Burns the laser head protection lens": "Zerstört die Laserkopf-Schutzlinse",
    "Burns laser head protection lens": "Zerstört die Laserkopf-Schutzlinse",
    "Lens replacement: $200–500 each time": "Linsenwechsel: $200–500 jedes Mal",
    "Unplanned production stop": "Ungeplanter Produktionsstopp",
    "100% safe — pure liquid gas source": "100% sicher — reine Flüssiggasquelle",
    "Zero optical risk": "Kein optisches Risiko",
    "LISHI Mixed Gas: The Real Cost Saver": "LISHI Mischgas: Der Echte Kostensparer",
    "LISHI Mixed Gas: The True Cost Saver": "LISHI Mischgas: Der Wahre Kostensparer",
    "While air looks free, your real cost is in maintenance, rework, and lens replacements. Mixed gas costs less long-term — and delivers superior quality.":
     "Während Luft kostenlos erscheint, liegen Ihre wahren Kosten in Wartung, Nacharbeit und Linsenwechseln. Mischgas kostet langfristig weniger — und liefert überlegene Qualität.",
    "While air seems free, your real cost is in maintenance, rework, and lens replacement. Mixed gas costs less in the long run — and delivers superior quality.":
     "Während Luft kostenlos erscheint, liegen Ihre wahren Kosten in Wartung, Nacharbeit und Linsenwechsel. Mischgas kostet langfristig weniger — und liefert überlegene Qualität.",
    "Air Seems Free. The Reality Is Not.": "Luft Scheint Kostenlos. Die Realität Ist Es Nicht.",
    "Most users choose air compressor for low upfront cost, but three hidden costs eat into your profit.":
     "Die meisten Anwender wählen einen Luftkompressor wegen der niedrigen Anschaffungskosten, aber drei versteckte Kosten schmälern Ihren Gewinn.",

    # Parameters by Power
    "Cutting Parameters by Power": "Schneidparameter nach Leistung",
    "Optimal carbon steel cutting thickness range for each laser power level. Mixed gas delivers consistent high-speed cutting across all thicknesses.":
     "Optimale Kohlenstoffstahl-Schneiddickenbereich für jede Laserleistungsstufe. Mischgas liefert konsistentes Hochgeschwindigkeitsschneiden über alle Dicken.",
    "Mixed Gas Speed": "Mischgas-Geschwindigkeit",
    "Best for ≤16mm carbon steel": "Optimal für ≤16mm Kohlenstoffstahl",
    "Best for ≤25mm carbon steel": "Optimal für ≤25mm Kohlenstoffstahl",
    "Contact for details": "Kontakt für Details",
    "Best for ≤30mm carbon steel": "Optimal für ≤30mm Kohlenstoffstahl",
    "Higher powers (40KW, 60KW) available. Contact us for detailed parameters.": "Höhere Leistungen (40KW, 60KW) verfügbar. Kontaktieren Sie uns für detaillierte Parameter.",
    "View All Parameters →": "Alle Parameter Anzeigen →",

    # Samples
    "Real Results": "Echte Ergebnisse",
    "Cutting Samples & Test Videos": "Schnittproben & Testvideos",
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Echte Schneidaufnahmen von Endanwendern weltweit. Keine Beschönigung — echte Daten, echte Leistung.",
    "12kW & 30kW · Professional Metal Fab": "12kW & 30kW · Professionelle Metallfertigung",
    "Dual-power setup, one device feeds two machines — 33% less gas, no speed compromise": "Doppelleistungs-Setup, ein Gerät versorgt zwei Maschinen — 33% weniger Gas, kein Geschwindigkeitskompromiss",
    "Mixed gas for high-power lasers": "Mischgas für Hochleistungslaser",
    "30kW · 10–30mm Carbon Steel": "30kW · 10–30mm Kohlenstoffstahl",
    "Thick sheets, zero burrs. 10–14 m/min on 10mm, previously only possible with O₂": "Dicke Bleche, keine Grate. 10–14 m/min bei 10mm, zuvor nur mit O₂ möglich",
    "High-power mixed gas cutting": "Hochleistungs-Mischgasschneiden",
    "60kW · 30–40mm Carbon Steel": "60kW · 30–40mm Kohlenstoffstahl",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas dominates": "Ultradickes Schneiden mit 3,5 m/min. Wo N₂ kämpft, dominiert Mischgas",
    "Ultra-high-power mixed gas": "Ultrahochleistungs-Mischgas",
    "12kW · 3mm Aluminum": "12kW · 3mm Aluminium",
    "Smooth aluminum edges, zero oxidation. Faster than air, cleaner than N₂": "Glatte Aluminiumkanten, keine Oxidation. Schneller als Luft, sauberer als N₂",
    "Aluminum mixed gas cutting": "Aluminium-Mischgasschneiden",
    "12kW · 2mm Aluminum": "12kW · 2mm Aluminium",
    "Precision aluminum with micro-oxygen — speed and quality in a single pass": "Präzisionsaluminium mit Mikro-Sauerstoff — Geschwindigkeit und Qualität in einem Durchgang",
    "Thin aluminum mixed gas": "Dünnaluminium-Mischgas",
    "12kW · 1mm Aluminum": "12kW · 1mm Aluminium",
    "Paper-thin aluminum, zero burn. Mixed gas enables what N₂ can't achieve": "Papierdünnes Aluminium, kein Durchbrennen. Mischgas ermöglicht, was N₂ nicht erreichen kann",
    "Precision thin aluminum cutting": "Präzisions-Dünnaluminiumschneiden",
    "Watch Video": "Video Ansehen",
    "Dual power setup, one machine feeds two — 33% less gas, zero compromise on speed":
     "Doppelleistungs-Setup, eine Maschine versorgt zwei — 33% weniger Gas, kein Kompromiss bei der Geschwindigkeit",
    "Thick plates, no burrs. 10–14 m/min on 10mm, previously only achievable with O₂":
     "Dicke Bleche, keine Grate. 10–14 m/min bei 10mm, zuvor nur mit O₂ erreichbar",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas delivers":
     "Ultradickes Schneiden mit 3,5 m/min. Wo N₂ kämpft, liefert Mischgas",
    "Smooth aluminum edges, no oxidation. Faster than air, cleaner than N₂":
     "Glatte Aluminiumkanten, keine Oxidation. Schneller als Luft, sauberer als N₂",
    "Precision aluminum cutting with micro-oxygen — speed and quality in one pass":
     "Präzisionsaluminiumschneiden mit Mikro-Sauerstoff — Geschwindigkeit und Qualität in einem Durchgang",
    "Paper-thin aluminum, zero burn-through. Mixed gas enables what N₂ cannot":
     "Papierdünnes Aluminium, kein Durchbrennen. Mischgas ermöglicht, was N₂ nicht kann",

    # Global
    "GLOBAL NETWORK": "GLOBALES NETZWERK",
    "Where High-Power Lasers Cut.<br>Our Gas Flows.": "Wo Hochleistungslaser Schneiden.<br>Unser Gas Fließt.",
    "From mega-factories on the coast to workshops deep inland, mixed gas technology now powers laser cutters across four continents — and the footprint is expanding every quarter.":
     "Von Megafabriken an der Küste bis zu Werkstätten tief im Landesinneren — Mischgastechnologie treibt heute Laserschneider auf vier Kontinenten an — und die Präsenz wächst jedes Quartal.",
    "Countries Stocked": "Belieferte Länder",
    "Continents Deployed": "Eingesetzte Kontinente",
    "Power Range Served": "Abgedeckter Leistungsbereich",
    "Manufacturing Durability": "Fertigungsbeständigkeit",
    "The Next Territory is Still Open.": "Das Nächste Gebiet Ist Noch Frei.",
    "Exclusive distributor partnerships available in select regions. Ship a container, build your market.":
     "Exklusive Vertriebspartnerschaften in ausgewählten Regionen verfügbar. Verschiffen Sie einen Container, bauen Sie Ihren Markt auf.",
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Echte Schneidaufnahmen von Endanwendern weltweit. Keine Beschönigung — echte Daten, echte Leistung.",
    "Our Gas Flows.": "Unser Gas Fließt.",
    "From coastal megafactories to inland workshops, mixed gas technology now powers laser cutters on four continents — and the footprint is expanding every quarter.":
     "Von Küsten-Megafabriken bis zu Werkstätten im Landesinneren treibt Mischgastechnologie heute Laserschneider auf vier Kontinenten an — und die Präsenz wächst jedes Quartal.",
    "The Next Territory Is Still Open.": "Das Nächste Gebiet Ist Noch Frei.",
    "Exclusive distributor partnerships available in select regions. Ship one container, build your market.":
     "Exklusive Vertriebspartnerschaften in ausgewählten Regionen verfügbar. Verschiffen Sie einen Container, bauen Sie Ihren Markt auf.",

    # FAQ
    "Frequently Asked Questions": "Häufig Gestellte Fragen",
    "What is a mixed gas device and how does it work?": "Was ist ein Mischgasgerät und wie funktioniert es?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Ein Mischgasgerät wandelt flüssigen Stickstoff (N₂) und flüssigen Sauerstoff (O₂) in eine präzise kalibrierte N₂/O₂-Gasmischung um (typischerweise 95%/5%). Diese Mikro-Sauerstoffmischung wird als Schutzgas beim Hochleistungslaserschneiden verwendet und liefert 3× höhere Schnittgeschwindigkeiten bei Kohlenstoffstahl im Vergleich zu reinem Sauerstoff, während Grate vollständig beseitigt werden.",
    "Is it compatible with my laser machine?": "Ist es mit meiner Lasermaschine kompatibel?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Ja. Das LISHI LASER Mischgasgerät funktioniert mit allen großen Lasermarken, einschließlich HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA und MESSER. Es unterstützt Maschinen von 12kW bis 60kW. Wenn Ihre Maschine Standard-Schutzgasanschlüsse verwendet, ist sie kompatibel.",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands, including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Ja. Das LISHI LASER Mischgasgerät funktioniert mit allen großen Lasermarken, einschließlich HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA und MESSER. Es unterstützt Maschinen von 12kW bis 60kW. Wenn Ihre Maschine Standard-Schutzgasanschlüsse verwendet, ist sie kompatibel.",
    "What thickness can it cut?": "Welche Dicken kann es schneiden?",
    "What thicknesses can it cut?": "Welche Dicken kann es schneiden?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "Der Schneidbereich hängt von Ihrer Laserleistung ab: 12kW bewältigt bis zu 16mm, 20kW bis zu 25mm, 30kW bis zu 30mm und 60kW bis zu 40mm Kohlenstoffstahl. Es schneidet auch Edelstahl und Aluminium. Detaillierte Schneidparametertabellen finden Sie auf unserer Parameterseite unten.",
    "How much can I save on gas costs?": "Wie viel kann ich bei den Gaskosten sparen?",
    "Mixed gas reduces nitrogen consumption by approximately 33–50% compared to pure N₂ cutting. Additionally, the device consumes only 2 kWh per 24 hours — essentially maintenance-free. The optimized mixing ratio means more cutting per unit of gas.":
     "Mischgas reduziert den Stickstoffverbrauch um etwa 33–50% im Vergleich zu reinem N₂-Schneiden. Zusätzlich verbraucht das Gerät nur 2 kWh pro 24 Stunden — praktisch wartungsfrei. Das optimierte Mischungsverhältnis bedeutet mehr Schneidleistung pro Gaseinheit.",
    "How much gas does it save?": "Wie viel Gas spart es?",
    "Does the device require regular maintenance?": "Erfordert das Gerät regelmäßige Wartung?",
    "No. Unlike air compressors that need filter/oil changes every 500–3,000 hours, the LISHI Mixed Gas Device is maintenance-free. There are no moving parts to wear out, no filters to replace, and no oil to change.":
     "Nein. Anders als Luftkompressoren, die alle 500–3.000 Stunden Filter-/Ölwechsel benötigen, ist das LISHI Mischgasgerät wartungsfrei. Es gibt keine beweglichen Teile, die verschleißen, keine Filter zum Wechseln und kein Öl zum Austauschen.",
    "Does it require regular maintenance?": "Erfordert es regelmäßige Wartung?",
    "Can one device serve two laser machines?": "Kann ein Gerät zwei Lasermaschinen versorgen?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station feeds two laser machines at different power levels (e.g., 12kW + 20kW) simultaneously — no switching, no pressure drops.":
     "Ja. LISHI LASER ist der einzige Hersteller, der eine stabile Eins-zu-Zwei-Konfiguration anbietet. Eine Mischstation versorgt zwei Lasermaschinen mit unterschiedlichen Leistungsstufen (z.B. 12kW + 20kW) gleichzeitig — keine Umschaltung, keine Druckabfälle.",
    "Can one device supply two lasers?": "Kann ein Gerät zwei Laser versorgen?",
    "How is mixed gas different from air cutting?": "Wie unterscheidet sich Mischgas vom Luftschneiden?",
    "Air cutting produces oxidized, rough edges and carries oil/water contamination risk that can burn expensive laser head lenses ($5,000–50,000). Mixed gas from pure liquid source delivers smooth, bright, burr-free edges — and protects your optics.":
     "Luftschneiden erzeugt oxidierte, raue Kanten und birgt das Risiko von Öl-/Wasserverschmutzung, die teure Laserkopflinsen zerstören kann ($5.000–50.000). Mischgas aus reiner Flüssigquelle liefert glatte, helle, gratfreie Kanten — und schützt Ihre Optik.",
    "How long does installation take?": "Wie lange dauert die Installation?",
    "Installation is straightforward and typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "Die Installation ist einfach und in der Regel innerhalb eines Tages abgeschlossen. Das Gerät wird an Ihre bestehende Flüssiggasversorgung und Lasermaschine angeschlossen. Wir bieten detaillierte Installationsanleitungen für alle Kunden.",
    "Installation is straightforward — typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "Die Installation ist einfach — in der Regel innerhalb eines Tages abgeschlossen. Das Gerät wird an Ihre bestehende Flüssiggasversorgung und Lasermaschine angeschlossen. Wir bieten detaillierte Installationsanleitungen für alle Kunden.",

    # CTA
    "Ready to Boost Your Cutting Speed?": "Bereit, Ihre Schnittgeschwindigkeit zu Steigern?",
    "Ready to Increase Your Cutting Speed?": "Bereit, Ihre Schnittgeschwindigkeit zu Erhöhen?",
    "Connect one device to your laser machine and start cutting 3× faster today. Available for 6KW–60KW machines.":
     "Schließen Sie ein Gerät an Ihre Lasermaschine an und beginnen Sie noch heute 3× schneller zu schneiden. Verfügbar für Maschinen von 6KW–60KW.",
    "Contact Us →": "Kontaktieren Sie Uns →",
    "Get Free Consultation": "Kostenlose Beratung",

    # Footer
    "Brand-Authorized Overseas Market Operations Agent:": "Markenautorisierter Übersee-Marktbetriebsagent:",
    "© 2025 Jinan Euchio Machinery Co., Ltd. All rights reserved.": "© 2025 Jinan Euchio Machinery Co., Ltd. Alle Rechte vorbehalten.",
    "Product": "Produkt",
    "Cutting Samples": "Schnittproben",

    # Contact page
    "Get in Touch": "Kontaktieren Sie Uns",
    "Contact Us": "Kontaktieren Sie Uns",
    "Ready to boost your cutting speed? Send your laser machine details and we'll provide custom parameters and pricing.":
     "Bereit, Ihre Schnittgeschwindigkeit zu steigern? Senden Sie uns die Details Ihrer Lasermaschine und wir erstellen individuelle Parameter und Preise.",
    "Email": "E-Mail",
    "Reply within 24 hours": "Antwort innerhalb von 24 Stunden",
    "Phone / WeChat": "Telefon / WeChat",
    "WeChat: same number": "WeChat: gleiche Nummer",
    "Company": "Unternehmen",
    "Product Brand": "Produktmarke",
    "Mixed Gas Device — 13 years in laser cutting industry": "Mischgasgerät — 13 Jahre in der Laserschneidbranche",
    "Looking for a distributor?": "Suchen Sie einen Vertriebspartner?",
    "We are actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "Wir erweitern aktiv unser globales Vertriebsnetz. Exklusive Gebiete verfügbar für qualifizierte Vertriebspartner.",
    "Agency Application →": "Vertriebspartnerantrag →",
    "Send Us a Message": "Senden Sie Uns eine Nachricht",
    "Full Name *": "Vollständiger Name *",
    "John Doe": "Max Mustermann",
    "ABC Laser Co.": "ABC Laser GmbH",
    "john@company.com": "max@unternehmen.de",
    "Phone / WhatsApp": "Telefon / WhatsApp",
    "+1 555 123 4567": "+49 170 123 4567",
    "Country": "Land",
    "e.g. USA, Germany, Brazil": "z.B. Deutschland, Österreich, Schweiz",
    "Inquiry Type": "Anfragetyp",
    "Select...": "Auswählen...",
    "Pricing & Quote": "Preise & Angebot",
    "Technical Parameters": "Technische Parameter",
    "Distributor / Agency": "Vertriebspartner / Agentur",
    "OEM / Customization": "OEM / Anpassung",
    "Other": "Sonstiges",
    "Laser Machine Power": "Lasermaschinenleistung",
    "Select laser power...": "Laserleistung auswählen...",
    "Other / Multiple": "Sonstige / Mehrere",
    "Laser Machine Brand": "Lasermaschinenmarke",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "z.B. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "Nachricht *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "Beschreiben Sie Ihre Schneidanforderungen — Materialtyp, Dicke, aktuelle Gaskonfiguration, etc.",
    "Send Message →": "Nachricht Senden →",
    "Or reach us directly via": "Oder erreichen Sie uns direkt per",
    "for faster response.": "für eine schnellere Antwort.",
    "Your Message Has Been Sent!": "Ihre Nachricht Wurde Gesendet!",
    "Thank you for your inquiry. We will respond within 24 hours.": "Vielen Dank für Ihre Anfrage. Wir werden innerhalb von 24 Stunden antworten.",
    "Back to Home": "Zurück zur Startseite",

    # Parameters page
    "Cutting Parameters": "Schneidparameter",
    "Detailed cutting parameters for different laser powers. All tests performed on real customer machines. Results verified by our engineering team.":
     "Detaillierte Schneidparameter für verschiedene Laserleistungen. Alle Tests wurden auf echten Kundenmaschinen durchgeführt. Ergebnisse von unserem Ingenieurteam verifiziert.",
    "Thickness": "Dicke",
    "Speed Improvement": "Geschwindigkeitsverbesserung",
    "Test Location": "Teststandort",
    "Notes": "Anmerkungen",
    "Mixed Gas Optimization": "Mischgasoptimierung",
    "Gas Consumption Comparison": "Gasverbrauchsvergleich",
    "Pure Nitrogen": "Reiner Stickstoff",
    "Mixed gas": "Mischgas",
    "Savings": "Einsparungen",
    "per hour": "pro Stunde",
    "per day": "pro Tag",
    "per month": "pro Monat",
    "per year": "pro Jahr",
    "Download Parameters": "Parameter Herunterladen",
    "Get Technical Support": "Technischen Support Erhalten",
    "How do I read the cutting parameters table?": "Wie lese ich die Schneidparametertabelle?",
    "The table shows cutting speed in meters per minute (m/min), mixed gas pressure in bar, and nozzle diameter in mm. Higher speeds mean better productivity. The speed improvement percentage shows the gain versus pure oxygen cutting.":
     "Die Tabelle zeigt die Schnittgeschwindigkeit in Metern pro Minute (m/min), den Mischgasdruck in bar und den Düsendurchmesser in mm. Höhere Geschwindigkeiten bedeuten bessere Produktivität. Der Geschwindigkeitsverbesserungsprozentsatz zeigt den Gewinn gegenüber reinem Sauerstoffschneiden.",
    "Why does speed improvement decrease at very thick materials?": "Warum nimmt die Geschwindigkeitsverbesserung bei sehr dicken Materialien ab?",
    "At extreme thicknesses (30mm+), the limiting factor shifts from gas chemistry to laser power penetration. The mixed gas still provides benefits in edge quality and eliminates burrs, but the raw speed difference versus oxygen narrows because both processes are dominated by the laser beam's physical ability to penetrate the material.":
     "Bei extremen Dicken (30mm+) verschiebt sich der limitierende Faktor von der Gaschemie zur Laserleistungsdurchdringung. Das Mischgas bietet weiterhin Vorteile bei der Kantenqualität und beseitigt Grate, aber der reine Geschwindigkeitsunterschied zu Sauerstoff verringert sich, da beide Prozesse von der physikalischen Fähigkeit des Laserstrahls dominiert werden, das Material zu durchdringen.",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER Mischgasgerät"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER Kontakt"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "Industrielle Fertigung > Laserschneidausrüstung"',

    # Misc
    "in Laser Metal Cutting Industry": "in der Laser-Metallschneidbranche",
    "Laser Machine": "Lasermaschine",
    "micro-oxygen laser cutting technology": "Mikro-Sauerstoff-Laserschneidtechnologie",
}

# ---- FRENCH ----
FR = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "Dispositif à gaz mixte LISHI LASER pour machines de découpe laser 12KW-60KW. Découpe 3× plus rapide, zéro bavure, 33% de gaz en moins. Technologie à ratio N2/O2 pour la découpe d'acier carbone.",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Dispositif à Gaz Mixte | Découpe Laser 3× Plus Rapide",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Dispositif à gaz mixte pour machines de découpe laser 12KW-60KW. Découpe 3× plus rapide, zéro bavure, 33% de gaz en moins. Technologie à ratio N2/O2.",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "mélangeur gaz découpe laser, dispositif mélange azote oxygène, découpe laser micro oxygène, découpe laser acier carbone, laser haute puissance 12kW 60kW, gaz mixte vs compresseur air, éliminer bavures découpe laser, réduire consommation azote, mélangeur gaz laser Han's, équipement gaz laser industriel, configuration gaz laser un-pour-deux, optimisation gaz auxiliaire",
    "LISHI LASER Mixed Gas Device": "LISHI LASER Dispositif à Gaz Mixte",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Tarifs et devis dispositif à gaz mixte LISHI LASER. Compatible avec toutes les grandes marques laser (HANS, DNE, PENTA, LEAD, HSG, BODOR). Livraison mondiale disponible.",
    "Request a quote for LISHI LASER mixed gas cutting equipment. Compatible with all major laser brands. Global shipping available.":
     "Demandez un devis pour équipement de découpe à gaz mixte LISHI LASER. Compatible avec toutes les grandes marques laser. Livraison mondiale disponible.",
    "LISHI LASER Contact | Get Mixed Gas Device Quote":
     "LISHI LASER Contact | Devis Dispositif Gaz Mixte",
    "laser cutting gas equipment quote, mixed gas device distributor, laser cutting equipment manufacturer, HANS laser compatible gas":
     "devis équipement gaz découpe laser, distributeur dispositif gaz mixte, fabricant équipement découpe laser, gaz compatible laser HANS",
    "LISHI LASER Contact": "LISHI LASER Contact",

    # Nav + UI
    "Skip to content": "Aller au contenu",
    "Home": "Accueil",
    "Advantages": "Avantages",
    "Samples": "Échantillons",
    "Customers": "Clients",
    "Blog": "Blog",
    "Contact": "Contact",
    "Gas Mixing Technology": "Technologie de Mélange de Gaz",
    "Menu toggle": "Menu",
    "How It Works": "Fonctionnement",
    "Parameters": "Paramètres",
    "Principle": "Principe",
    "Clients": "Clients",

    # Hero
    'Cut <span class="accent">3× Faster</span><br>with Mixed Gas Technology':
     'Coupez <span class="accent">3× Plus Vite</span><br>avec la Technologie à Gaz Mixte',
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "Solution gaz mixte N₂/O₂ pour machines de découpe laser 12KW-60KW",
    "3× Faster than O₂": "3× Plus Rapide que l'O₂",
    "Zero Burrs": "Zéro Bavure",
    "33% Less N₂": "33% de N₂ en Moins",
    "13 Years in Laser Metal Cutting": "13 Ans dans la Découpe Laser des Métaux",
    "The LISHI LASER Mixed Gas Device delivers micro-oxygen cutting for high-power laser machines (12KW–60KW). No burrs, less gas consumption, and significantly faster cutting speeds.":
     "Le Dispositif à Gaz Mixte LISHI LASER offre une découpe micro-oxygène pour machines laser haute puissance (12KW–60KW). Aucune bavure, moins de gaz et des vitesses de découpe nettement supérieures.",
    "Get Quote →": "Obtenir un Devis →",
    "View Parameters": "Voir les Paramètres",
    "Faster than O₂": "Plus Rapide que l'O₂",
    "Burrs on cut surface": "Bavures sur surface de coupe",
    "Less gas than N₂": "Moins de gaz que le N₂",
    "in Laser Metal Cutting Industry": "dans l'Industrie de la Découpe Laser des Métaux",

    # Principle
    "What is a Mixed Gas Device?": "Qu'est-ce qu'un Dispositif à Gaz Mixte ?",
    "Our nitrogen oxygen mixing device uses": "Notre dispositif de mélange azote-oxygène utilise",
    "to produce precisely calibrated N₂/O₂ mixed gas — eliminating burrs on carbon steel while delivering 3× faster cutting speed versus traditional oxygen cutting. Supports high-power laser machines from 12kW to 60kW.":
     "pour produire un gaz mixte N₂/O₂ précisément calibré — éliminant les bavures sur l'acier carbone tout en offrant une vitesse de découpe 3× supérieure à la découpe oxygène traditionnelle. Prend en charge les machines laser de 12kW à 60kW.",
    "Micro-oxygen laser cutting technology": "Technologie de découpe laser micro-oxygène",
    "Liquid N₂ + Liquid O₂": "N₂ Liquide + O₂ Liquide",
    "Raw materials stored in tanks, pressure 20–25 bar": "Matières premières stockées en réservoirs, pression 20–25 bar",
    "Vaporizer": "Vaporisateur",
    "Converts liquid gases to gas form": "Convertit les gaz liquides en forme gazeuse",
    "Mixed Gas Device": "Dispositif à Gaz Mixte",
    "Stable pressure + proportional mixing → N₂ 95% / O₂ 5%": "Pression stable + mélange proportionnel → N₂ 95% / O₂ 5%",
    "To Laser Machine": "Vers la Machine Laser",
    "Output: 12–16 bar, flow rate up to 200m³/h": "Sortie : 12–16 bar, débit jusqu'à 200m³/h",
    "Input: N₂ + O₂ at 20–25 bar. Output: N₂ purity ~95%, pressure 12–16 bar, max flow 200m³/h. Compact gas tank (capacity >3m³).":
     "Entrée : N₂ + O₂ à 20–25 bar. Sortie : pureté N₂ ~95%, pression 12–16 bar, débit max 200m³/h. Réservoir gaz compact (capacité >3m³).",
    "Device Dimensions": "Dimensions du Dispositif",
    "800mm × 350mm × 1100mm, weight 90kg. One device simultaneously supports two laser machines (One-to-Two configuration).":
     "800mm × 350mm × 1100mm, poids 90kg. Un dispositif prend en charge simultanément deux machines laser (configuration Un-pour-Deux).",
    "High cutting speed + zero burrs. After installation, simply adjust the N₂ 95% to O₂ 5% ratio for different sheet thicknesses. The built-in program makes operation intuitive.":
     "Vitesse de coupe élevée + zéro bavure. Après installation, ajustez simplement le ratio N₂ 95% / O₂ 5% pour différentes épaisseurs de tôle. Le programme intégré rend l'opération intuitive.",
    "Wide Compatibility": "Large Compatibilité",
    "Broad Compatibility": "Large Compatibilité",
    "Works with all major brands: HAN'S, DNE, PENTA, LEAD, HSG and more. Compatible with BODOR, KIMLA, MESSER and other global brands.":
     "Fonctionne avec toutes les grandes marques : HAN'S, DNE, PENTA, LEAD, HSG et plus. Compatible avec BODOR, KIMLA, MESSER et autres marques mondiales.",
    "Converts liquid gases to gaseous form": "Convertit les gaz liquides en forme gazeuse",
    "Laser Cutting Machine": "Machine de Découpe Laser",
    "Laser Machine": "Machine Laser",
    "Cutting Effect": "Effet de Coupe",
    "micro-oxygen laser cutting technology": "technologie de découpe laser micro-oxygène",

    # Advantages
    "Why Mixed Gas Instead of O₂, N₂ or Air?": "Pourquoi le Gaz Mixte Plutôt que O₂, N₂ ou Air ?",
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "Pourquoi Choisir le Gaz Mixte Plutôt que O₂, N₂ ou Air ?",
    "Eliminate burrs in carbon steel laser cutting while cutting nitrogen consumption by 33%. Our maintenance-free gas delivery system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Éliminez les bavures dans la découpe laser d'acier carbone tout en réduisant la consommation d'azote de 33%. Notre système de distribution de gaz sans maintenance est compatible avec HAN'S, DNE, PENTA, LEAD, HSG, BODOR et toutes les autres grandes marques.",
    "Reduce nitrogen consumption by 33% while eliminating burrs on laser cutting carbon steel. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and other major brands.":
     "Réduisez la consommation d'azote de 33% tout en éliminant les bavures sur la découpe laser d'acier carbone. Notre système d'alimentation en gaz sans maintenance est compatible avec HAN'S, DNE, PENTA, LEAD, HSG, BODOR et autres grandes marques.",
    "Competitive Advantage": "Avantage Concurrentiel",
    "3× Faster Cutting": "Découpe 3× Plus Rapide",
    "Boost laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Augmentez la vitesse de découpe laser jusqu'à 3× par rapport à la découpe oxygène. Exemple : acier carbone 8mm à 16m/min avec gaz mixte, seulement 2–3m/min avec O₂.",
    "Increase laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas vs only 2–3m/min with O₂.":
     "Augmentez la vitesse de découpe laser jusqu'à 3× par rapport à la découpe oxygène. Exemple : acier carbone 8mm à 16m/min avec gaz mixte vs seulement 2–3m/min avec O₂.",
    "Eliminate Burrs": "Éliminer les Bavures",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cutting edges requiring no secondary grinding.":
     "L'environnement micro-oxygène contrôlé assure une combustion complète. Résultat : bords de coupe lisses et sans bavures ne nécessitant aucun meulage secondaire.",
    "Unlike nitrogen cutting which produces burrs on plates ≥8mm (12kW) or ≥10mm (20kW), mixed gas cutting produces clean, burr-free surfaces on carbon steel — no secondary grinding needed.":
     "Contrairement à la découpe azote qui produit des bavures sur tôles ≥8mm (12kW) ou ≥10mm (20kW), la découpe au gaz mixte produit des surfaces propres et sans bavures sur acier carbone — aucun meulage secondaire nécessaire.",
    "Cut Gas Costs": "Réduire les Coûts de Gaz",
    "Reduce nitrogen consumption by 33–50% versus pure N₂ cutting. Cost comparison: mixed gas costs significantly less than air compressors when factoring in maintenance-free operation.":
     "Réduisez la consommation d'azote de 33–50% par rapport à la découpe N₂ pur. Comparaison des coûts : le gaz mixte coûte nettement moins cher que les compresseurs d'air en tenant compte du fonctionnement sans maintenance.",
    "Reduce Gas Costs": "Réduire les Coûts de Gaz",
    "Reduce nitrogen consumption by 33–50% compared to pure N₂ cutting. Cost comparison: mixed gas saves significantly vs air compressor when factoring in maintenance-free operation.":
     "Réduisez la consommation d'azote de 33–50% par rapport à la découpe N₂ pur. Comparaison des coûts : le gaz mixte économise considérablement vs compresseur d'air en tenant compte du fonctionnement sans maintenance.",
    "Maintenance-Free": "Sans Maintenance",
    "Power consumption: only 2 kWh per 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Consommation électrique : seulement 2 kWh par 24 heures. Contrairement aux compresseurs d'air nécessitant des changements de filtre/huile toutes les 3.000 heures, notre équipement gaz laser industriel est sans maintenance.",
    "Power consumption: only 2 kWh / 24 hours. Unlike air compressors requiring filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Consommation électrique : seulement 2 kWh / 24 heures. Contrairement aux compresseurs d'air nécessitant des changements de filtre/huile toutes les 3.000 heures, notre équipement gaz laser industriel est sans maintenance.",
    "One-to-Two Laser Setup": "Configuration Un-pour-Deux",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines at different power levels simultaneously — no switching required.":
     "Le seul fabricant avec un équipement gaz mixte un-pour-deux stable. Une station de mélange de gaz industrielle alimente deux machines laser à différents niveaux de puissance simultanément — aucune commutation nécessaire.",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines of different power levels simultaneously.":
     "Le seul fabricant avec un équipement gaz mixte un-pour-deux stable. Une station de mélange de gaz industrielle alimente deux machines laser de différents niveaux de puissance simultanément.",
    "Lens Protection": "Protection des Lentilles",
    "Air compressors carry oil/water contamination risk that can burn laser head lenses ($5,000–50,000 loss). Our pure liquid gas source keeps your optical system pristine.":
     "Les compresseurs d'air présentent un risque de contamination huile/eau qui peut brûler les lentilles de tête laser (perte de 5.000–50.000$). Notre source de gaz liquide pur maintient votre système optique impeccable.",
    "Air compressors risk oil/water contamination burning laser head lenses ($5,000–$50,000 loss). Our pure liquid gas source keeps your optical system 100% safe — pure liquid gas source":
     "Les compresseurs d'air risquent la contamination huile/eau brûlant les lentilles de tête laser (perte de 5.000$–50.000$). Notre source de gaz liquide pur maintient votre système optique 100% sûr.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air": "Comparaison de Performance : Gaz Mixte vs O₂ vs N₂ vs Air",
    "Factor": "Facteur",
    "Mixed Gas": "Gaz Mixte",
    "O₂ (Oxygen)": "O₂ (Oxygène)",
    "N₂ (Nitrogen)": "N₂ (Azote)",
    "Air": "Air",
    "Cutting Speed": "Vitesse de Découpe",
    "3× faster (e.g. 16m/min @ 8mm CS)": "3× plus rapide (ex. 16m/min @ 8mm AC)",
    "30% slower than mixed gas": "30% plus lent que le gaz mixte",
    "May have burrs on thick plates": "Possibilité de bavures sur tôles épaisses",
    "3× Faster": "3× Plus Rapide",
    "Similar to mixed gas": "Similaire au gaz mixte",
    "Cut Surface": "Surface de Coupe",
    "Smooth, burr-free": "Lisse, sans bavure",
    "Smooth, no burrs": "Lisse, sans bavures",
    "Oxidized, rough edges": "Oxydée, bords rugueux",
    "Contaminated, rough": "Contaminée, rugueuse",
    "Gas Consumption": "Consommation de Gaz",
    "1/3 less than N₂": "1/3 de moins que N₂",
    "Less than 1/3 of N₂": "Moins d'1/3 du N₂",
    "Similar total": "Total similaire",
    "High": "Élevé",
    "Very high (compressor)": "Très élevé (compresseur)",
    "Power Cost": "Coût Énergétique",
    "2 kWh/24h": "2 kWh/24h",
    "Small Hole Piercing": "Perçage Petits Trous",
    "Excellent — clean & fast": "Excellent — propre et rapide",
    "Some burr during piercing": "Quelques bavures lors du perçage",
    "Some burrs during pierce": "Quelques bavures lors du perçage",
    "Best for small holes": "Idéal pour petits trous",
    "Equipment Protection": "Protection de l'Équipement",
    "No pipeline contamination": "Aucune contamination des conduites",
    "Oil/water risk": "Risque huile/eau",
    "Oil/water risk from compressor": "Risque huile/eau du compresseur",

    # ROI
    "ROI Calculator": "Calculateur ROI",
    "Calculator": "Calculateur",
    "Calculate Your Laser Cutting Gas Cost Savings": "Calculez vos Économies de Coûts de Gaz de Découpe Laser",
    "See how much you could save with LISHI LASER mixed gas technology. Cut nitrogen consumption, eliminate burrs on carbon steel, and boost throughput.":
     "Voyez combien vous pourriez économiser avec la technologie à gaz mixte LISHI LASER. Réduisez la consommation d'azote, éliminez les bavures sur acier carbone et augmentez le débit.",
    "Machine Power": "Puissance Machine",
    "Material Thickness": "Épaisseur Matériau",
    "Daily Work Hours": "Heures de Travail Quotidiennes",
    "Actual Cutting Time (Beam On %)": "Temps de Découpe Réel (% Faisceau Actif)",
    "Typical shops run 40–70% — remaining time is loading, piercing, idle.": "Les ateliers typiques fonctionnent à 40–70% — le reste est chargement, perçage, inactivité.",
    "Profit Per Meter (USD/m)": "Profit par Mètre (USD/m)",
    "Your selling price minus material cost (USD)": "Votre prix de vente moins le coût matériel (USD)",
    "Monthly N₂ Cost (USD)": "Coût Mensuel N₂ (USD)",
    "Your current monthly nitrogen spend (USD)": "Vos dépenses mensuelles actuelles en azote (USD)",
    "Estimated Annual Profit Increase (USD)": "Augmentation Estimée du Profit Annuel (USD)",
    "in nitrogen savings": "en économies d'azote",
    "Theoretical ceiling based on your inputs. Real results depend on job mix, nesting efficiency and machine uptime.":
     "Plafond théorique basé sur vos saisies. Les résultats réels dépendent du mix de travaux, de l'efficacité d'imbrication et de la disponibilité machine.",
    "Want the full parameter table for your specific machine?": "Voulez-vous le tableau complet des paramètres pour votre machine spécifique ?",
    "Get detailed cutting data tailored to your 12KW–60KW laser setup.": "Obtenez des données de découpe détaillées adaptées à votre configuration laser 12KW–60KW.",
    "Get Free Parameters →": "Obtenir Paramètres Gratuits →",
    "Or contact us directly:": "Ou contactez-nous directement :",
    "Actual Cutting Time (Beam-On %)": "Temps de Découpe Réel (% Faisceau Actif)",
    "Typical shops run 40–70% — the rest is loading, piercing, idle.": "Les ateliers typiques fonctionnent à 40–70% — le reste est chargement, perçage, inactivité.",
    "Your selling price minus material cost (USD)": "Votre prix de vente moins le coût matériel (USD)",
    "Your current monthly nitrogen expense (USD)": "Vos dépenses mensuelles actuelles en azote (USD)",
    "Theoretical upper bound based on your inputs. Real-world results depend on job mix, nesting efficiency, and machine uptime.":
     "Limite supérieure théorique basée sur vos saisies. Les résultats réels dépendent du mix de travaux, de l'efficacité d'imbrication et de la disponibilité machine.",
    "USD/year in nitrogen savings": "USD/an en économies d'azote",

    # Air vs Mixed
    "Why Air Compressors Cost More": "Pourquoi les Compresseurs d'Air Coûtent Plus Cher",
    "Air Looks Free. It Isn't.": "L'Air Semble Gratuit. Il Ne L'est Pas.",
    "Most users pick an air compressor for the low upfront cost — but three hidden costs eat your margin.":
     "La plupart des utilisateurs choisissent un compresseur d'air pour son faible coût initial — mais trois coûts cachés grignotent votre marge.",
    "HIGH MAINTENANCE COST": "COÛT DE MAINTENANCE ÉLEVÉ",
    "High Maintenance Cost": "Coût de Maintenance Élevé",
    "Filter replacement every 500-1000 hours": "Remplacement filtre toutes les 500-1000 heures",
    "Oil changes and system flushing": "Vidanges d'huile et rinçage système",
    "Oil change and system flush": "Vidange d'huile et rinçage système",
    "Unexpected repair downtime": "Temps d'arrêt imprévu pour réparations",
    "Unexpected downtime for repairs": "Temps d'arrêt imprévu pour réparations",
    "2 kWh/24h — near zero maintenance": "2 kWh/24h — presque zéro maintenance",
    "2 kWh/24h electricity — basically maintenance-free": "2 kWh/24h d'électricité — pratiquement sans maintenance",
    "~$73/year electricity": "~$73/an d'électricité",
    "~$73/year in electricity": "~$73/an d'électricité",
    "POOR CUT QUALITY": "MAUVAISE QUALITÉ DE COUPE",
    "Poor Cut Quality": "Mauvaise Qualité de Coupe",
    "Dark oxidation layer on cut surface": "Couche d'oxydation foncée sur surface de coupe",
    "Burrs and slag requiring rework": "Bavures et scories nécessitant reprise",
    "Burrs and dross requiring rework": "Bavures et scories nécessitant reprise",
    "Extra grinding/polishing labor": "Travail supplémentaire de meulage/polissage",
    "Cannot deliver premium jobs": "Impossible de livrer des travaux premium",
    "Silver-white surface, zero burrs": "Surface blanc argenté, zéro bavure",
    "Ready to ship immediately": "Prêt à expédier immédiatement",
    "Ready for immediate delivery": "Prêt pour livraison immédiate",
    "LENS CONTAMINATION RISK": "RISQUE DE CONTAMINATION DES LENTILLES",
    "Lens Contamination Risk": "Risque de Contamination des Lentilles",
    "Lens Contamination": "Contamination des Lentilles",
    "Oil/water in compressed air": "Huile/eau dans l'air comprimé",
    "Burns the laser head protection lens": "Brûle la lentille de protection de tête laser",
    "Burns laser head protection lens": "Brûle la lentille de protection de tête laser",
    "Lens replacement: $200–500 each time": "Remplacement lentille : 200–500$ à chaque fois",
    "Unplanned production stop": "Arrêt de production non planifié",
    "100% safe — pure liquid gas source": "100% sûr — source de gaz liquide pur",
    "Zero optical risk": "Zéro risque optique",
    "LISHI Mixed Gas: The Real Cost Saver": "LISHI Gaz Mixte : Le Vrai Réducteur de Coûts",
    "LISHI Mixed Gas: The True Cost Saver": "LISHI Gaz Mixte : Le Véritable Économiseur de Coûts",
    "While air looks free, your real cost is in maintenance, rework, and lens replacements. Mixed gas costs less long-term — and delivers superior quality.":
     "Alors que l'air semble gratuit, votre coût réel est dans la maintenance, les reprises et les remplacements de lentilles. Le gaz mixte coûte moins cher à long terme — et offre une qualité supérieure.",
    "While air seems free, your real cost is in maintenance, rework, and lens replacement. Mixed gas costs less in the long run — and delivers superior quality.":
     "Alors que l'air semble gratuit, votre coût réel est dans la maintenance, les reprises et le remplacement de lentilles. Le gaz mixte coûte moins cher à long terme — et offre une qualité supérieure.",
    "Air Seems Free. The Reality Is Not.": "L'Air Semble Gratuit. La Réalité Ne L'est Pas.",
    "Most users choose air compressor for low upfront cost, but three hidden costs eat into your profit.":
     "La plupart des utilisateurs choisissent le compresseur d'air pour son faible coût initial, mais trois coûts cachés grignotent votre profit.",

    # Parameters by Power
    "Cutting Parameters by Power": "Paramètres de Découpe par Puissance",
    "Optimal carbon steel cutting thickness range for each laser power level. Mixed gas delivers consistent high-speed cutting across all thicknesses.":
     "Plage d'épaisseur de coupe optimale pour acier carbone pour chaque niveau de puissance laser. Le gaz mixte offre une découpe haute vitesse constante sur toutes les épaisseurs.",
    "Mixed Gas Speed": "Vitesse Gaz Mixte",
    "Best for ≤16mm carbon steel": "Idéal pour acier carbone ≤16mm",
    "Best for ≤25mm carbon steel": "Idéal pour acier carbone ≤25mm",
    "Contact for details": "Contact pour détails",
    "Best for ≤30mm carbon steel": "Idéal pour acier carbone ≤30mm",
    "Higher powers (40KW, 60KW) available. Contact us for detailed parameters.": "Puissances supérieures (40KW, 60KW) disponibles. Contactez-nous pour paramètres détaillés.",
    "View All Parameters →": "Voir Tous les Paramètres →",

    # Samples
    "Real Results": "Résultats Réels",
    "Cutting Samples & Test Videos": "Échantillons de Découpe et Vidéos de Test",
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Vidéos de découpe réelles d'utilisateurs finaux dans le monde entier. Aucun embellissement — données réelles, performance réelle.",
    "12kW & 30kW · Professional Metal Fab": "12kW & 30kW · Atelier Métallurgique Professionnel",
    "Dual-power setup, one device feeds two machines — 33% less gas, no speed compromise": "Configuration double puissance, un dispositif alimente deux machines — 33% de gaz en moins, aucun compromis de vitesse",
    "Mixed gas for high-power lasers": "Gaz mixte pour lasers haute puissance",
    "30kW · 10–30mm Carbon Steel": "30kW · 10–30mm Acier Carbone",
    "Thick sheets, zero burrs. 10–14 m/min on 10mm, previously only possible with O₂": "Tôles épaisses, zéro bavure. 10–14 m/min sur 10mm, auparavant possible seulement avec O₂",
    "High-power mixed gas cutting": "Découpe gaz mixte haute puissance",
    "60kW · 30–40mm Carbon Steel": "60kW · 30–40mm Acier Carbone",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas dominates": "Découpe ultra-épaisse à 3,5 m/min. Là où le N₂ peine, le gaz mixte domine",
    "Ultra-high-power mixed gas": "Gaz mixte ultra-haute puissance",
    "12kW · 3mm Aluminum": "12kW · 3mm Aluminium",
    "Smooth aluminum edges, zero oxidation. Faster than air, cleaner than N₂": "Bords aluminium lisses, zéro oxydation. Plus rapide que l'air, plus propre que le N₂",
    "Aluminum mixed gas cutting": "Découpe aluminium gaz mixte",
    "12kW · 2mm Aluminum": "12kW · 2mm Aluminium",
    "Precision aluminum with micro-oxygen — speed and quality in a single pass": "Aluminium de précision avec micro-oxygène — vitesse et qualité en un seul passage",
    "Thin aluminum mixed gas": "Gaz mixte aluminium fin",
    "12kW · 1mm Aluminum": "12kW · 1mm Aluminium",
    "Paper-thin aluminum, zero burn. Mixed gas enables what N₂ can't achieve": "Aluminium fin comme du papier, zéro brûlure. Le gaz mixte permet ce que le N₂ ne peut atteindre",
    "Precision thin aluminum cutting": "Découpe de précision aluminium fin",
    "Watch Video": "Voir Vidéo",
    "Dual power setup, one machine feeds two — 33% less gas, zero compromise on speed":
     "Configuration double puissance, une machine alimente deux — 33% de gaz en moins, aucun compromis de vitesse",
    "Thick plates, no burrs. 10–14 m/min on 10mm, previously only achievable with O₂":
     "Tôles épaisses, aucune bavure. 10–14 m/min sur 10mm, auparavant réalisable seulement avec O₂",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas delivers":
     "Découpe ultra-épaisse à 3,5 m/min. Là où le N₂ peine, le gaz mixte livre",
    "Smooth aluminum edges, no oxidation. Faster than air, cleaner than N₂":
     "Bords aluminium lisses, aucune oxydation. Plus rapide que l'air, plus propre que le N₂",
    "Precision aluminum cutting with micro-oxygen — speed and quality in one pass":
     "Découpe aluminium de précision avec micro-oxygène — vitesse et qualité en un seul passage",
    "Paper-thin aluminum, zero burn-through. Mixed gas enables what N₂ cannot":
     "Aluminium fin comme du papier, zéro perçage. Le gaz mixte permet ce que le N₂ ne peut pas",

    # Global
    "GLOBAL NETWORK": "RÉSEAU MONDIAL",
    "Where High-Power Lasers Cut.<br>Our Gas Flows.": "Là Où les Lasers Haute Puissance Coupent.<br>Notre Gaz Coule.",
    "From mega-factories on the coast to workshops deep inland, mixed gas technology now powers laser cutters across four continents — and the footprint is expanding every quarter.":
     "Des méga-usines côtières aux ateliers de l'intérieur, la technologie à gaz mixte alimente désormais les découpeuses laser sur quatre continents — et l'empreinte s'étend chaque trimestre.",
    "Countries Stocked": "Pays Approvisionnés",
    "Continents Deployed": "Continents Déployés",
    "Power Range Served": "Gamme de Puissance Desservie",
    "Manufacturing Durability": "Durabilité de Fabrication",
    "The Next Territory is Still Open.": "Le Prochain Territoire est Encore Ouvert.",
    "Exclusive distributor partnerships available in select regions. Ship a container, build your market.":
     "Partenariats de distribution exclusifs disponibles dans certaines régions. Expédiez un conteneur, construisez votre marché.",
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Vidéos de découpe réelles d'utilisateurs finaux dans le monde entier. Aucun embellissement — données réelles, performance réelle.",
    "Our Gas Flows.": "Notre Gaz Coule.",
    "From coastal megafactories to inland workshops, mixed gas technology now powers laser cutters on four continents — and the footprint is expanding every quarter.":
     "Des méga-usines côtières aux ateliers de l'intérieur, la technologie à gaz mixte alimente désormais les découpeuses laser sur quatre continents — et l'empreinte s'étend chaque trimestre.",
    "The Next Territory Is Still Open.": "Le Prochain Territoire est Encore Ouvert.",
    "Exclusive distributor partnerships available in select regions. Ship one container, build your market.":
     "Partenariats de distribution exclusifs disponibles dans certaines régions. Expédiez un conteneur, construisez votre marché.",

    # FAQ
    "Frequently Asked Questions": "Questions Fréquemment Posées",
    "What is a mixed gas device and how does it work?": "Qu'est-ce qu'un dispositif à gaz mixte et comment fonctionne-t-il ?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Un dispositif à gaz mixte convertit l'azote liquide (N₂) et l'oxygène liquide (O₂) en un mélange gazeux N₂/O₂ précisément calibré (typiquement 95%/5%). Ce mélange micro-oxygène est utilisé comme gaz auxiliaire dans la découpe laser haute puissance, offrant des vitesses de découpe 3× supérieures sur acier carbone par rapport à l'oxygène pur tout en éliminant complètement les bavures.",
    "Is it compatible with my laser machine?": "Est-il compatible avec ma machine laser ?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Oui. Le Dispositif à Gaz Mixte LISHI LASER fonctionne avec toutes les grandes marques laser, y compris HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA et MESSER. Il prend en charge les machines de 12kW à 60kW. Si votre machine utilise des connexions gaz auxiliaire standard, elle est compatible.",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands, including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Oui. Le Dispositif à Gaz Mixte LISHI LASER fonctionne avec toutes les grandes marques laser, y compris HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA et MESSER. Il prend en charge les machines de 12kW à 60kW. Si votre machine utilise des connexions gaz auxiliaire standard, elle est compatible.",
    "What thickness can it cut?": "Quelles épaisseurs peut-il couper ?",
    "What thicknesses can it cut?": "Quelles épaisseurs peut-il couper ?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "La plage de découpe dépend de votre puissance laser : 12kW gère jusqu'à 16mm, 20kW jusqu'à 25mm, 30kW jusqu'à 30mm et 60kW jusqu'à 40mm d'acier carbone. Il coupe également l'acier inoxydable et l'aluminium. Des tableaux détaillés de paramètres de découpe sont disponibles sur notre page paramètres ci-dessous.",
    "How much can I save on gas costs?": "Combien puis-je économiser sur les coûts de gaz ?",
    "Mixed gas reduces nitrogen consumption by approximately 33–50% compared to pure N₂ cutting. Additionally, the device consumes only 2 kWh per 24 hours — essentially maintenance-free. The optimized mixing ratio means more cutting per unit of gas.":
     "Le gaz mixte réduit la consommation d'azote d'environ 33–50% par rapport à la découpe N₂ pur. De plus, le dispositif ne consomme que 2 kWh par 24 heures — essentiellement sans maintenance. Le ratio de mélange optimisé signifie plus de découpe par unité de gaz.",
    "How much gas does it save?": "Combien de gaz économise-t-il ?",
    "Does the device require regular maintenance?": "Le dispositif nécessite-t-il une maintenance régulière ?",
    "No. Unlike air compressors that need filter/oil changes every 500–3,000 hours, the LISHI Mixed Gas Device is maintenance-free. There are no moving parts to wear out, no filters to replace, and no oil to change.":
     "Non. Contrairement aux compresseurs d'air nécessitant des changements de filtre/huile toutes les 500–3.000 heures, le Dispositif à Gaz Mixte LISHI est sans maintenance. Aucune pièce mobile à user, aucun filtre à remplacer, aucune huile à changer.",
    "Does it require regular maintenance?": "Nécessite-t-il une maintenance régulière ?",
    "Can one device serve two laser machines?": "Un dispositif peut-il servir deux machines laser ?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station feeds two laser machines at different power levels (e.g., 12kW + 20kW) simultaneously — no switching, no pressure drops.":
     "Oui. LISHI LASER est le seul fabricant offrant une configuration un-pour-deux stable. Une station de mélange alimente deux machines laser à différents niveaux de puissance (ex. 12kW + 20kW) simultanément — aucune commutation, aucune chute de pression.",
    "Can one device supply two lasers?": "Un dispositif peut-il alimenter deux lasers ?",
    "How is mixed gas different from air cutting?": "En quoi le gaz mixte diffère-t-il de la découpe à air ?",
    "Air cutting produces oxidized, rough edges and carries oil/water contamination risk that can burn expensive laser head lenses ($5,000–50,000). Mixed gas from pure liquid source delivers smooth, bright, burr-free edges — and protects your optics.":
     "La découpe à air produit des bords oxydés et rugueux et présente un risque de contamination huile/eau pouvant brûler les lentilles coûteuses de tête laser (5.000–50.000$). Le gaz mixte de source liquide pure offre des bords lisses, brillants et sans bavures — et protège votre optique.",
    "How long does installation take?": "Combien de temps prend l'installation ?",
    "Installation is straightforward and typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "L'installation est simple et généralement terminée en une journée. Le dispositif se connecte à votre alimentation en gaz liquide existante et à votre machine laser. Nous fournissons des conseils d'installation détaillés pour tous les clients.",
    "Installation is straightforward — typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "L'installation est simple — généralement terminée en une journée. Le dispositif se connecte à votre alimentation en gaz liquide existante et à votre machine laser. Nous fournissons des conseils d'installation détaillés pour tous les clients.",

    # CTA
    "Ready to Boost Your Cutting Speed?": "Prêt à Augmenter Votre Vitesse de Découpe ?",
    "Ready to Increase Your Cutting Speed?": "Prêt à Augmenter Votre Vitesse de Découpe ?",
    "Connect one device to your laser machine and start cutting 3× faster today. Available for 6KW–60KW machines.":
     "Connectez un dispositif à votre machine laser et commencez à couper 3× plus vite aujourd'hui. Disponible pour machines 6KW–60KW.",
    "Contact Us →": "Contactez-Nous →",
    "Get Free Consultation": "Consultation Gratuite",

    # Footer
    "Brand-Authorized Overseas Market Operations Agent:": "Agent Autorisé des Opérations sur le Marché International :",
    "© 2025 Jinan Euchio Machinery Co., Ltd. All rights reserved.": "© 2025 Jinan Euchio Machinery Co., Ltd. Tous droits réservés.",
    "Product": "Produit",
    "Cutting Samples": "Échantillons de Découpe",

    # Contact page
    "Get in Touch": "Contactez-Nous",
    "Contact Us": "Contactez-Nous",
    "Ready to boost your cutting speed? Send your laser machine details and we'll provide custom parameters and pricing.":
     "Prêt à augmenter votre vitesse de découpe ? Envoyez les détails de votre machine laser et nous vous fournirons des paramètres et tarifs personnalisés.",
    "Email": "E-mail",
    "Reply within 24 hours": "Réponse sous 24 heures",
    "Phone / WeChat": "Téléphone / WeChat",
    "WeChat: same number": "WeChat : même numéro",
    "Company": "Entreprise",
    "Product Brand": "Marque du Produit",
    "Mixed Gas Device — 13 years in laser cutting industry": "Dispositif à Gaz Mixte — 13 ans dans l'industrie de la découpe laser",
    "Looking for a distributor?": "Vous cherchez un distributeur ?",
    "We are actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "Nous élargissons activement notre réseau mondial d'agents. Territoires exclusifs disponibles pour distributeurs qualifiés.",
    "Agency Application →": "Demande d'Agence →",
    "Send Us a Message": "Envoyez-Nous un Message",
    "Full Name *": "Nom Complet *",
    "John Doe": "Jean Dupont",
    "ABC Laser Co.": "ABC Laser SARL",
    "john@company.com": "jean@entreprise.fr",
    "Phone / WhatsApp": "Téléphone / WhatsApp",
    "+1 555 123 4567": "+33 6 12 34 56 78",
    "Country": "Pays",
    "e.g. USA, Germany, Brazil": "ex. France, Belgique, Suisse",
    "Inquiry Type": "Type de Demande",
    "Select...": "Sélectionner...",
    "Pricing & Quote": "Tarifs et Devis",
    "Technical Parameters": "Paramètres Techniques",
    "Distributor / Agency": "Distributeur / Agence",
    "OEM / Customization": "OEM / Personnalisation",
    "Other": "Autre",
    "Laser Machine Power": "Puissance Machine Laser",
    "Select laser power...": "Sélectionner puissance laser...",
    "Other / Multiple": "Autre / Multiple",
    "Laser Machine Brand": "Marque Machine Laser",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "ex. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "Message *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "Décrivez vos besoins de découpe — type de matériau, épaisseur, configuration gaz actuelle, etc.",
    "Send Message →": "Envoyer Message →",
    "Or reach us directly via": "Ou contactez-nous directement par",
    "for faster response.": "pour une réponse plus rapide.",
    "Your Message Has Been Sent!": "Votre Message a Été Envoyé !",
    "Thank you for your inquiry. We will respond within 24 hours.": "Merci pour votre demande. Nous répondrons dans les 24 heures.",
    "Back to Home": "Retour à l'Accueil",

    # Parameters page
    "Cutting Parameters": "Paramètres de Découpe",
    "Detailed cutting parameters for different laser powers. All tests performed on real customer machines. Results verified by our engineering team.":
     "Paramètres de découpe détaillés pour différentes puissances laser. Tous les tests effectués sur de vraies machines clients. Résultats vérifiés par notre équipe d'ingénieurs.",
    "Thickness": "Épaisseur",
    "Speed Improvement": "Amélioration Vitesse",
    "Test Location": "Lieu du Test",
    "Notes": "Notes",
    "Mixed Gas Optimization": "Optimisation Gaz Mixte",
    "Gas Consumption Comparison": "Comparaison Consommation Gaz",
    "Pure Nitrogen": "Azote Pur",
    "Mixed gas": "Gaz mixte",
    "Savings": "Économies",
    "per hour": "par heure",
    "per day": "par jour",
    "per month": "par mois",
    "per year": "par an",
    "Download Parameters": "Télécharger Paramètres",
    "Get Technical Support": "Support Technique",
    "How do I read the cutting parameters table?": "Comment lire le tableau des paramètres de découpe ?",
    "The table shows cutting speed in meters per minute (m/min), mixed gas pressure in bar, and nozzle diameter in mm. Higher speeds mean better productivity. The speed improvement percentage shows the gain versus pure oxygen cutting.":
     "Le tableau montre la vitesse de découpe en mètres par minute (m/min), la pression du gaz mixte en bar et le diamètre de buse en mm. Des vitesses plus élevées signifient une meilleure productivité. Le pourcentage d'amélioration de vitesse montre le gain par rapport à la découpe oxygène pur.",
    "Why does speed improvement decrease at very thick materials?": "Pourquoi l'amélioration de vitesse diminue-t-elle sur des matériaux très épais ?",
    "At extreme thicknesses (30mm+), the limiting factor shifts from gas chemistry to laser power penetration. The mixed gas still provides benefits in edge quality and eliminates burrs, but the raw speed difference versus oxygen narrows because both processes are dominated by the laser beam's physical ability to penetrate the material.":
     "À des épaisseurs extrêmes (30mm+), le facteur limitant passe de la chimie du gaz à la puissance de pénétration laser. Le gaz mixte offre toujours des avantages en qualité de bord et élimine les bavures, mais la différence de vitesse brute par rapport à l'oxygène se réduit car les deux processus sont dominés par la capacité physique du faisceau laser à pénétrer le matériau.",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER Dispositif à Gaz Mixte"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER Contact"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "Fabrication Industrielle > Équipement de Découpe Laser"',

    # Misc
    "in Laser Metal Cutting Industry": "dans l'Industrie de la Découpe Laser des Métaux",
    "Laser Machine": "Machine Laser",
    "micro-oxygen laser cutting technology": "technologie de découpe laser micro-oxygène",
}

# ---- DUTCH ----
NL = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "LISHI LASER Menggasapparaat voor 12KW-60KW lasersnijmachines. 3× snellere snijsnelheid, geen bramen, 33% minder gasverbruik. N2/O2-verhoudingstechnologie voor koolstofstaalsnijden.",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Menggasapparaat | 3× Sneller Lasersnijden",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Menggasapparaat voor 12KW-60KW lasersnijmachines. 3× snellere snijsnelheid, geen bramen, 33% minder gasverbruik. N2/O2-verhoudingstechnologie.",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "lasersnijden gasmenger, stikstof zuurstof mengapparaat, micro zuurstof lasersnijden, koolstofstaal lasersnijden, hoogvermogen laser 12kW 60kW, menggas vs luchtcompressor, lasersnijbramen verwijderen, stikstofverbruik verminderen, Han's laser gasmenger, industriële lasergasapparatuur, een-op-twee lasergasconfiguratie, snijgasoptimalisatie",
    "LISHI LASER Mixed Gas Device": "LISHI LASER Menggasapparaat",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "LISHI LASER menggasapparaat prijzen en offertes. Compatibel met alle grote lasermerken (HANS, DNE, PENTA, LEAD, HSG, BODOR). Wereldwijde verzending beschikbaar.",
    "Request a quote for LISHI LASER mixed gas cutting equipment. Compatible with all major laser brands. Global shipping available.":
     "Vraag een offerte aan voor LISHI LASER menggas snijapparatuur. Compatibel met alle grote lasermerken. Wereldwijde verzending beschikbaar.",
    "LISHI LASER Contact | Get Mixed Gas Device Quote":
     "LISHI LASER Contact | Menggasapparaat Offerte Aanvragen",
    "laser cutting gas equipment quote, mixed gas device distributor, laser cutting equipment manufacturer, HANS laser compatible gas":
     "lasersnijgasapparatuur offerte, menggasapparaat distributeur, lasersnijapparatuur fabrikant, HANS laser compatibel gas",
    "LISHI LASER Contact": "LISHI LASER Contact",

    # Nav + UI
    "Skip to content": "Naar inhoud",
    "Home": "Home",
    "Advantages": "Voordelen",
    "Samples": "Stalen",
    "Customers": "Klanten",
    "Blog": "Blog",
    "Contact": "Contact",
    "Gas Mixing Technology": "Gasmengtechnologie",
    "Menu toggle": "Menu",
    "How It Works": "Werking",
    "Parameters": "Parameters",
    "Principle": "Principe",
    "Clients": "Klanten",

    # Hero
    'Cut <span class="accent">3× Faster</span><br>with Mixed Gas Technology':
     'Snij <span class="accent">3× Sneller</span><br>met Menggastechnologie',
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "N₂/O₂ menggasoplossing voor 12KW-60KW lasersnijmachines",
    "3× Faster than O₂": "3× Sneller dan O₂",
    "Zero Burrs": "Geen Bramen",
    "33% Less N₂": "33% Minder N₂",
    "13 Years in Laser Metal Cutting": "13 Jaar in Laser Metaalsnijden",
    "The LISHI LASER Mixed Gas Device delivers micro-oxygen cutting for high-power laser machines (12KW–60KW). No burrs, less gas consumption, and significantly faster cutting speeds.":
     "Het LISHI LASER Menggasapparaat levert micro-zuurstofsnijden voor hoogvermogen lasermachines (12KW–60KW). Geen bramen, minder gasverbruik en aanzienlijk hogere snijsnelheden.",
    "Get Quote →": "Offerte Aanvragen →",
    "View Parameters": "Parameters Bekijken",
    "Faster than O₂": "Sneller dan O₂",
    "Burrs on cut surface": "Bramen op snijoppervlak",
    "Less gas than N₂": "Minder gas dan N₂",
    "in Laser Metal Cutting Industry": "in de Laser Metaalsnij-industrie",

    # Principle
    "What is a Mixed Gas Device?": "Wat is een Menggasapparaat?",
    "Our nitrogen oxygen mixing device uses": "Ons stikstof-zuurstof mengapparaat gebruikt",
    "to produce precisely calibrated N₂/O₂ mixed gas — eliminating burrs on carbon steel while delivering 3× faster cutting speed versus traditional oxygen cutting. Supports high-power laser machines from 12kW to 60kW.":
     "om nauwkeurig gekalibreerd N₂/O₂-menggas te produceren — elimineert bramen op koolstofstaal en levert 3× hogere snijsnelheid vergeleken met traditioneel zuurstofsnijden. Ondersteunt hoogvermogen lasers van 12kW tot 60kW.",
    "Micro-oxygen laser cutting technology": "Micro-zuurstof lasersnijtechnologie",
    "Liquid N₂ + Liquid O₂": "Vloeibaar N₂ + Vloeibaar O₂",
    "Raw materials stored in tanks, pressure 20–25 bar": "Grondstoffen opgeslagen in tanks, druk 20–25 bar",
    "Vaporizer": "Verdamper",
    "Converts liquid gases to gas form": "Zet vloeibare gassen om in gasvorm",
    "Mixed Gas Device": "Menggasapparaat",
    "Stable pressure + proportional mixing → N₂ 95% / O₂ 5%": "Stabiele druk + proportionele menging → N₂ 95% / O₂ 5%",
    "To Laser Machine": "Naar Lasermachine",
    "Output: 12–16 bar, flow rate up to 200m³/h": "Uitgang: 12–16 bar, debiet tot 200m³/u",
    "Input: N₂ + O₂ at 20–25 bar. Output: N₂ purity ~95%, pressure 12–16 bar, max flow 200m³/h. Compact gas tank (capacity >3m³).":
     "Ingang: N₂ + O₂ bij 20–25 bar. Uitgang: N₂-zuiverheid ~95%, druk 12–16 bar, max debiet 200m³/u. Compacte gastank (capaciteit >3m³).",
    "Device Dimensions": "Apparaatafmetingen",
    "800mm × 350mm × 1100mm, weight 90kg. One device simultaneously supports two laser machines (One-to-Two configuration).":
     "800mm × 350mm × 1100mm, gewicht 90kg. Eén apparaat ondersteunt gelijktijdig twee lasermachines (Een-op-Twee-configuratie).",
    "High cutting speed + zero burrs. After installation, simply adjust the N₂ 95% to O₂ 5% ratio for different sheet thicknesses. The built-in program makes operation intuitive.":
     "Hoge snijsnelheid + geen bramen. Pas na installatie eenvoudig de N₂ 95% tot O₂ 5% verhouding aan voor verschillende plaatdiktes. Het ingebouwde programma maakt bediening intuïtief.",
    "Wide Compatibility": "Brede Compatibiliteit",
    "Broad Compatibility": "Brede Compatibiliteit",
    "Works with all major brands: HAN'S, DNE, PENTA, LEAD, HSG and more. Compatible with BODOR, KIMLA, MESSER and other global brands.":
     "Werkt met alle grote merken: HAN'S, DNE, PENTA, LEAD, HSG en meer. Compatibel met BODOR, KIMLA, MESSER en andere wereldwijde merken.",
    "Converts liquid gases to gaseous form": "Zet vloeibare gassen om in gasvorm",
    "Laser Cutting Machine": "Lasersnijmachine",
    "Laser Machine": "Lasermachine",
    "Cutting Effect": "Snij-effect",
    "micro-oxygen laser cutting technology": "micro-zuurstof lasersnijtechnologie",

    # Advantages
    "Why Mixed Gas Instead of O₂, N₂ or Air?": "Waarom Menggas in Plaats van O₂, N₂ of Lucht?",
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "Waarom Kiezen voor Menggas in Plaats van O₂, N₂ of Lucht?",
    "Eliminate burrs in carbon steel laser cutting while cutting nitrogen consumption by 33%. Our maintenance-free gas delivery system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Elimineer bramen bij lasersnijden van koolstofstaal en verlaag het stikstofverbruik met 33%. Ons onderhoudsvrije gastoevoersysteem is compatibel met HAN'S, DNE, PENTA, LEAD, HSG, BODOR en alle andere grote merken.",
    "Reduce nitrogen consumption by 33% while eliminating burrs on laser cutting carbon steel. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and other major brands.":
     "Verlaag het stikstofverbruik met 33% terwijl u bramen bij lasersnijden van koolstofstaal elimineert. Ons onderhoudsvrije gastoevoersysteem is compatibel met HAN'S, DNE, PENTA, LEAD, HSG, BODOR en andere grote merken.",
    "Competitive Advantage": "Concurrentievoordeel",
    "3× Faster Cutting": "3× Sneller Snijden",
    "Boost laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Verhoog de lasersnijsnelheid tot 3× in vergelijking met zuurstofsnijden. Voorbeeld: 8mm koolstofstaal op 16m/min met menggas, slechts 2–3m/min met O₂.",
    "Increase laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas vs only 2–3m/min with O₂.":
     "Verhoog de lasersnijsnelheid tot 3× in vergelijking met zuurstofsnijden. Voorbeeld: 8mm koolstofstaal op 16m/min met menggas vs slechts 2–3m/min met O₂.",
    "Eliminate Burrs": "Elimineer Bramen",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cutting edges requiring no secondary grinding.":
     "Gecontroleerde micro-zuurstofomgeving zorgt voor volledige verbranding. Resultaat: gladde, braamvrije snijkanten die geen secundair slijpen vereisen.",
    "Unlike nitrogen cutting which produces burrs on plates ≥8mm (12kW) or ≥10mm (20kW), mixed gas cutting produces clean, burr-free surfaces on carbon steel — no secondary grinding needed.":
     "In tegenstelling tot stikstofsnijden dat bramen produceert op platen ≥8mm (12kW) of ≥10mm (20kW), produceert menggassnijden schone, braamvrije oppervlakken op koolstofstaal — geen secundair slijpen nodig.",
    "Cut Gas Costs": "Verlaag Gaskosten",
    "Reduce nitrogen consumption by 33–50% versus pure N₂ cutting. Cost comparison: mixed gas costs significantly less than air compressors when factoring in maintenance-free operation.":
     "Verlaag het stikstofverbruik met 33–50% ten opzichte van puur N₂-snijden. Kostenvergelijking: menggas kost aanzienlijk minder dan luchtcompressoren rekening houdend met onderhoudsvrij bedrijf.",
    "Reduce Gas Costs": "Verlaag Gaskosten",
    "Reduce nitrogen consumption by 33–50% compared to pure N₂ cutting. Cost comparison: mixed gas saves significantly vs air compressor when factoring in maintenance-free operation.":
     "Verlaag het stikstofverbruik met 33–50% in vergelijking met puur N₂-snijden. Kostenvergelijking: menggas bespaart aanzienlijk vs luchtcompressor rekening houdend met onderhoudsvrij bedrijf.",
    "Maintenance-Free": "Onderhoudsvrij",
    "Power consumption: only 2 kWh per 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Stroomverbruik: slechts 2 kWh per 24 uur. In tegenstelling tot luchtcompressoren die elke 3.000 uur filter-/olieverversing nodig hebben, is onze industriële lasergasapparatuur onderhoudsvrij.",
    "Power consumption: only 2 kWh / 24 hours. Unlike air compressors requiring filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Stroomverbruik: slechts 2 kWh / 24 uur. In tegenstelling tot luchtcompressoren die elke 3.000 uur filter-/olieverversing nodig hebben, is onze industriële lasergasapparatuur onderhoudsvrij.",
    "One-to-Two Laser Setup": "Een-op-Twee Laserconfiguratie",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines at different power levels simultaneously — no switching required.":
     "De enige fabrikant met stabiele een-op-twee menggasapparatuur. Eén industrieel gasmengstation voedt twee lasermachines op verschillende vermogensniveaus gelijktijdig — geen omschakeling nodig.",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines of different power levels simultaneously.":
     "De enige fabrikant met stabiele een-op-twee menggasapparatuur. Eén industrieel gasmengstation voedt twee lasermachines van verschillende vermogensniveaus gelijktijdig.",
    "Lens Protection": "Lensbescherming",
    "Air compressors carry oil/water contamination risk that can burn laser head lenses ($5,000–50,000 loss). Our pure liquid gas source keeps your optical system pristine.":
     "Luchtcompressoren brengen risico op olie-/waterverontreiniging die laserkoplenzen kan verbranden ($5.000–50.000 verlies). Onze zuivere vloeibare gasbron houdt uw optisch systeem onberispelijk.",
    "Air compressors risk oil/water contamination burning laser head lenses ($5,000–$50,000 loss). Our pure liquid gas source keeps your optical system 100% safe — pure liquid gas source":
     "Luchtcompressoren riskeren olie-/waterverontreiniging die laserkoplenzen verbrandt ($5.000–$50.000 verlies). Onze zuivere vloeibare gasbron houdt uw optisch systeem 100% veilig.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air": "Prestatievergelijking: Menggas vs O₂ vs N₂ vs Lucht",
    "Factor": "Factor",
    "Mixed Gas": "Menggas",
    "O₂ (Oxygen)": "O₂ (Zuurstof)",
    "N₂ (Nitrogen)": "N₂ (Stikstof)",
    "Air": "Lucht",
    "Cutting Speed": "Snijsnelheid",
    "3× faster (e.g. 16m/min @ 8mm CS)": "3× sneller (bijv. 16m/min @ 8mm KS)",
    "30% slower than mixed gas": "30% langzamer dan menggas",
    "May have burrs on thick plates": "Kan bramen hebben op dikke platen",
    "3× Faster": "3× Sneller",
    "Similar to mixed gas": "Vergelijkbaar met menggas",
    "Cut Surface": "Snijoppervlak",
    "Smooth, burr-free": "Glad, braamvrij",
    "Smooth, no burrs": "Glad, geen bramen",
    "Oxidized, rough edges": "Geoxideerd, ruwe randen",
    "Contaminated, rough": "Verontreinigd, ruw",
    "Gas Consumption": "Gasverbruik",
    "1/3 less than N₂": "1/3 minder dan N₂",
    "Less than 1/3 of N₂": "Minder dan 1/3 van N₂",
    "Similar total": "Vergelijkbaar totaal",
    "High": "Hoog",
    "Very high (compressor)": "Zeer hoog (compressor)",
    "Power Cost": "Stroomkosten",
    "2 kWh/24h": "2 kWh/24u",
    "Small Hole Piercing": "Gaatjes Perforeren",
    "Excellent — clean & fast": "Uitstekend — schoon & snel",
    "Some burr during piercing": "Enige braam tijdens perforeren",
    "Some burrs during pierce": "Enige bramen tijdens perforeren",
    "Best for small holes": "Beste voor kleine gaten",
    "Equipment Protection": "Apparatuurbescherming",
    "No pipeline contamination": "Geen leidingverontreiniging",
    "Oil/water risk": "Olie-/waterrisico",
    "Oil/water risk from compressor": "Olie-/waterrisico van compressor",

    # ROI
    "ROI Calculator": "ROI-Calculator",
    "Calculator": "Calculator",
    "Calculate Your Laser Cutting Gas Cost Savings": "Bereken Uw Lasersnijden Gaskostenbesparing",
    "See how much you could save with LISHI LASER mixed gas technology. Cut nitrogen consumption, eliminate burrs on carbon steel, and boost throughput.":
     "Zie hoeveel u kunt besparen met LISHI LASER menggastechnologie. Verlaag stikstofverbruik, elimineer bramen op koolstofstaal en verhoog de doorvoer.",
    "Machine Power": "Machinevermogen",
    "Material Thickness": "Materiaaldikte",
    "Daily Work Hours": "Dagelijkse Werkuren",
    "Actual Cutting Time (Beam On %)": "Werkelijke Snijtijd (Straal Aan %)",
    "Typical shops run 40–70% — remaining time is loading, piercing, idle.": "Typische werkplaatsen draaien 40–70% — resterende tijd is laden, perforeren, inactief.",
    "Profit Per Meter (USD/m)": "Winst Per Meter (USD/m)",
    "Your selling price minus material cost (USD)": "Uw verkoopprijs minus materiaalkosten (USD)",
    "Monthly N₂ Cost (USD)": "Maandelijkse N₂-Kosten (USD)",
    "Your current monthly nitrogen spend (USD)": "Uw huidige maandelijkse stikstofuitgaven (USD)",
    "Estimated Annual Profit Increase (USD)": "Geschatte Jaarlijkse Winststijging (USD)",
    "in nitrogen savings": "aan stikstofbesparingen",
    "Theoretical ceiling based on your inputs. Real results depend on job mix, nesting efficiency and machine uptime.":
     "Theoretisch plafond gebaseerd op uw invoer. Echte resultaten zijn afhankelijk van werkmix, nesting-efficiëntie en machinebeschikbaarheid.",
    "Want the full parameter table for your specific machine?": "Wilt u de volledige parametertabel voor uw specifieke machine?",
    "Get detailed cutting data tailored to your 12KW–60KW laser setup.": "Ontvang gedetailleerde snijgegevens afgestemd op uw 12KW–60KW laserconfiguratie.",
    "Get Free Parameters →": "Ontvang Gratis Parameters →",
    "Or contact us directly:": "Of neem direct contact op:",
    "Actual Cutting Time (Beam-On %)": "Werkelijke Snijtijd (Straal-Aan %)",
    "Typical shops run 40–70% — the rest is loading, piercing, idle.": "Typische werkplaatsen draaien 40–70% — de rest is laden, perforeren, inactief.",
    "Your selling price minus material cost (USD)": "Uw verkoopprijs minus materiaalkosten (USD)",
    "Your current monthly nitrogen expense (USD)": "Uw huidige maandelijkse stikstofuitgaven (USD)",
    "Theoretical upper bound based on your inputs. Real-world results depend on job mix, nesting efficiency, and machine uptime.":
     "Theoretische bovengrens gebaseerd op uw invoer. Praktijkresultaten zijn afhankelijk van werkmix, nesting-efficiëntie en machinebeschikbaarheid.",
    "USD/year in nitrogen savings": "USD/jaar aan stikstofbesparingen",

    # Air vs Mixed
    "Why Air Compressors Cost More": "Waarom Luchtcompressoren Meer Kosten",
    "Air Looks Free. It Isn't.": "Lucht Lijkt Gratis. Dat Is Het Niet.",
    "Most users pick an air compressor for the low upfront cost — but three hidden costs eat your margin.":
     "De meeste gebruikers kiezen een luchtcompressor vanwege de lage aanschafkosten — maar drie verborgen kosten vreten aan uw marge.",
    "HIGH MAINTENANCE COST": "HOGE ONDERHOUDSKOSTEN",
    "High Maintenance Cost": "Hoge Onderhoudskosten",
    "Filter replacement every 500-1000 hours": "Filtervervanging elke 500-1000 uur",
    "Oil changes and system flushing": "Olieverversing en systeemspoeling",
    "Oil change and system flush": "Olieverversing en systeemspoeling",
    "Unexpected repair downtime": "Onverwachte reparatiestilstand",
    "Unexpected downtime for repairs": "Onverwachte stilstand voor reparaties",
    "2 kWh/24h — near zero maintenance": "2 kWh/24u — bijna geen onderhoud",
    "2 kWh/24h electricity — basically maintenance-free": "2 kWh/24u elektriciteit — vrijwel onderhoudsvrij",
    "~$73/year electricity": "~$73/jaar elektriciteit",
    "~$73/year in electricity": "~$73/jaar aan elektriciteit",
    "POOR CUT QUALITY": "SLECHTE SNIJKWALITEIT",
    "Poor Cut Quality": "Slechte Snijkwaliteit",
    "Dark oxidation layer on cut surface": "Donkere oxidatielaag op snijoppervlak",
    "Burrs and slag requiring rework": "Bramen en slak die nabewerking vereisen",
    "Burrs and dross requiring rework": "Bramen en slak die nabewerking vereisen",
    "Extra grinding/polishing labor": "Extra slijp-/polijstwerk",
    "Cannot deliver premium jobs": "Kan geen premium opdrachten leveren",
    "Silver-white surface, zero burrs": "Zilverwit oppervlak, geen bramen",
    "Ready to ship immediately": "Klaar voor onmiddellijke verzending",
    "Ready for immediate delivery": "Klaar voor directe levering",
    "LENS CONTAMINATION RISK": "LENSVERONTREINIGINGSRISICO",
    "Lens Contamination Risk": "Lensverontreinigingsrisico",
    "Lens Contamination": "Lensverontreiniging",
    "Oil/water in compressed air": "Olie/water in perslucht",
    "Burns the laser head protection lens": "Verbrandt de laserkop-beschermlens",
    "Burns laser head protection lens": "Verbrandt laserkop-beschermlens",
    "Lens replacement: $200–500 each time": "Lensvervanging: $200–500 elke keer",
    "Unplanned production stop": "Ongeplande productiestop",
    "100% safe — pure liquid gas source": "100% veilig — zuivere vloeibare gasbron",
    "Zero optical risk": "Geen optisch risico",
    "LISHI Mixed Gas: The Real Cost Saver": "LISHI Menggas: De Echte Kostenbespaarder",
    "LISHI Mixed Gas: The True Cost Saver": "LISHI Menggas: De Ware Kostenbespaarder",
    "While air looks free, your real cost is in maintenance, rework, and lens replacements. Mixed gas costs less long-term — and delivers superior quality.":
     "Hoewel lucht gratis lijkt, zitten uw echte kosten in onderhoud, nabewerking en lensvervangingen. Menggas kost op lange termijn minder — en levert superieure kwaliteit.",
    "While air seems free, your real cost is in maintenance, rework, and lens replacement. Mixed gas costs less in the long run — and delivers superior quality.":
     "Hoewel lucht gratis lijkt, zitten uw echte kosten in onderhoud, nabewerking en lensvervanging. Menggas kost op lange termijn minder — en levert superieure kwaliteit.",
    "Air Seems Free. The Reality Is Not.": "Lucht Lijkt Gratis. De Realiteit Is Het Niet.",
    "Most users choose air compressor for low upfront cost, but three hidden costs eat into your profit.":
     "De meeste gebruikers kiezen een luchtcompressor vanwege de lage aanschafkosten, maar drie verborgen kosten vreten aan uw winst.",

    # Parameters by Power
    "Cutting Parameters by Power": "Snijparameters per Vermogen",
    "Optimal carbon steel cutting thickness range for each laser power level. Mixed gas delivers consistent high-speed cutting across all thicknesses.":
     "Optimaal koolstofstaal snijdiktebereik voor elk laservermogensniveau. Menggas levert consistent hogesnelheidssnijden over alle diktes.",
    "Mixed Gas Speed": "Menggas Snelheid",
    "Best for ≤16mm carbon steel": "Beste voor ≤16mm koolstofstaal",
    "Best for ≤25mm carbon steel": "Beste voor ≤25mm koolstofstaal",
    "Contact for details": "Contact voor details",
    "Best for ≤30mm carbon steel": "Beste voor ≤30mm koolstofstaal",
    "Higher powers (40KW, 60KW) available. Contact us for detailed parameters.": "Hogere vermogens (40KW, 60KW) beschikbaar. Neem contact op voor gedetailleerde parameters.",
    "View All Parameters →": "Bekijk Alle Parameters →",

    # Samples
    "Real Results": "Echte Resultaten",
    "Cutting Samples & Test Videos": "Snijstalen & Testvideo's",
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Echte snijbeelden van eindgebruikers wereldwijd. Geen verfraaiing — echte data, echte prestaties.",
    "12kW & 30kW · Professional Metal Fab": "12kW & 30kW · Professionele Metaalwerkplaats",
    "Dual-power setup, one device feeds two machines — 33% less gas, no speed compromise": "Dubbelvermogen-opstelling, één apparaat voedt twee machines — 33% minder gas, geen snelheidscompromis",
    "Mixed gas for high-power lasers": "Menggas voor hoogvermogen lasers",
    "30kW · 10–30mm Carbon Steel": "30kW · 10–30mm Koolstofstaal",
    "Thick sheets, zero burrs. 10–14 m/min on 10mm, previously only possible with O₂": "Dikke platen, geen bramen. 10–14 m/min op 10mm, voorheen alleen mogelijk met O₂",
    "High-power mixed gas cutting": "Hoogvermogen menggassnijden",
    "60kW · 30–40mm Carbon Steel": "60kW · 30–40mm Koolstofstaal",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas dominates": "Ultradik snijden op 3,5 m/min. Waar N₂ worstelt, domineert menggas",
    "Ultra-high-power mixed gas": "Ultrahoogvermogen menggas",
    "12kW · 3mm Aluminum": "12kW · 3mm Aluminium",
    "Smooth aluminum edges, zero oxidation. Faster than air, cleaner than N₂": "Gladde aluminium randen, geen oxidatie. Sneller dan lucht, schoner dan N₂",
    "Aluminum mixed gas cutting": "Aluminium menggassnijden",
    "12kW · 2mm Aluminum": "12kW · 2mm Aluminium",
    "Precision aluminum with micro-oxygen — speed and quality in a single pass": "Precisie aluminium met micro-zuurstof — snelheid en kwaliteit in één doorgang",
    "Thin aluminum mixed gas": "Dun aluminium menggas",
    "12kW · 1mm Aluminum": "12kW · 1mm Aluminium",
    "Paper-thin aluminum, zero burn. Mixed gas enables what N₂ can't achieve": "Papierdun aluminium, geen doorbranding. Menggas maakt mogelijk wat N₂ niet kan bereiken",
    "Precision thin aluminum cutting": "Precisie dun aluminium snijden",
    "Watch Video": "Bekijk Video",
    "Dual power setup, one machine feeds two — 33% less gas, zero compromise on speed":
     "Dubbelvermogen-opstelling, één machine voedt twee — 33% minder gas, geen compromis in snelheid",
    "Thick plates, no burrs. 10–14 m/min on 10mm, previously only achievable with O₂":
     "Dikke platen, geen bramen. 10–14 m/min op 10mm, voorheen alleen bereikbaar met O₂",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas delivers":
     "Ultradik snijden op 3,5 m/min. Waar N₂ worstelt, levert menggas",
    "Smooth aluminum edges, no oxidation. Faster than air, cleaner than N₂":
     "Gladde aluminium randen, geen oxidatie. Sneller dan lucht, schoner dan N₂",
    "Precision aluminum cutting with micro-oxygen — speed and quality in one pass":
     "Precisie aluminium snijden met micro-zuurstof — snelheid en kwaliteit in één doorgang",
    "Paper-thin aluminum, zero burn-through. Mixed gas enables what N₂ cannot":
     "Papierdun aluminium, geen doorbranding. Menggas maakt mogelijk wat N₂ niet kan",

    # Global
    "GLOBAL NETWORK": "WERELDWIJD NETWERK",
    "Where High-Power Lasers Cut.<br>Our Gas Flows.": "Waar Hoogvermogen Lasers Snijden.<br>Ons Gas Stroomt.",
    "From mega-factories on the coast to workshops deep inland, mixed gas technology now powers laser cutters across four continents — and the footprint is expanding every quarter.":
     "Van megafabrieken aan de kust tot werkplaatsen diep in het binnenland, menggastechnologie drijft nu lasersnijders aan op vier continenten — en de voetafdruk breidt elk kwartaal uit.",
    "Countries Stocked": "Landen Bevoorraad",
    "Continents Deployed": "Continenten Ingezet",
    "Power Range Served": "Vermogensbereik Bediend",
    "Manufacturing Durability": "Productieduurzaamheid",
    "The Next Territory is Still Open.": "Het Volgende Territorium Is Nog Open.",
    "Exclusive distributor partnerships available in select regions. Ship a container, build your market.":
     "Exclusieve distributeurpartnerschappen beschikbaar in geselecteerde regio's. Verscheep een container, bouw uw markt op.",
    "Actual cutting footage from end users worldwide. No embellishment — real data, real performance.":
     "Echte snijbeelden van eindgebruikers wereldwijd. Geen verfraaiing — echte data, echte prestaties.",
    "Our Gas Flows.": "Ons Gas Stroomt.",
    "From coastal megafactories to inland workshops, mixed gas technology now powers laser cutters on four continents — and the footprint is expanding every quarter.":
     "Van kustmegafabrieken tot werkplaatsen in het binnenland, menggastechnologie drijft nu lasersnijders aan op vier continenten — en de voetafdruk breidt elk kwartaal uit.",
    "The Next Territory Is Still Open.": "Het Volgende Territorium Is Nog Open.",
    "Exclusive distributor partnerships available in select regions. Ship one container, build your market.":
     "Exclusieve distributeurpartnerschappen beschikbaar in geselecteerde regio's. Verscheep één container, bouw uw markt op.",

    # FAQ
    "Frequently Asked Questions": "Veelgestelde Vragen",
    "What is a mixed gas device and how does it work?": "Wat is een menggasapparaat en hoe werkt het?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Een menggasapparaat zet vloeibare stikstof (N₂) en vloeibare zuurstof (O₂) om in een nauwkeurig gekalibreerd N₂/O₂-gasmengsel (meestal 95%/5%). Dit micro-zuurstofmengsel wordt gebruikt als snijgas bij hoogvermogen lasersnijden en levert 3× hogere snijsnelheden op koolstofstaal in vergelijking met zuivere zuurstof, terwijl bramen volledig worden geëlimineerd.",
    "Is it compatible with my laser machine?": "Is het compatibel met mijn lasermachine?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Ja. Het LISHI LASER Menggasapparaat werkt met alle grote lasermerken, waaronder HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA en MESSER. Het ondersteunt machines van 12kW tot 60kW. Als uw machine standaard snijgasaansluitingen gebruikt, is het compatibel.",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands, including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Ja. Het LISHI LASER Menggasapparaat werkt met alle grote lasermerken, waaronder HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA en MESSER. Het ondersteunt machines van 12kW tot 60kW. Als uw machine standaard snijgasaansluitingen gebruikt, is het compatibel.",
    "What thickness can it cut?": "Welke diktes kan het snijden?",
    "What thicknesses can it cut?": "Welke diktes kan het snijden?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "Het snijbereik hangt af van uw laservermogen: 12kW verwerkt tot 16mm, 20kW tot 25mm, 30kW tot 30mm en 60kW tot 40mm koolstofstaal. Het snijdt ook roestvrij staal en aluminium. Gedetailleerde snijparametertabellen zijn beschikbaar op onze parameterspagina hieronder.",
    "How much can I save on gas costs?": "Hoeveel kan ik besparen op gaskosten?",
    "Mixed gas reduces nitrogen consumption by approximately 33–50% compared to pure N₂ cutting. Additionally, the device consumes only 2 kWh per 24 hours — essentially maintenance-free. The optimized mixing ratio means more cutting per unit of gas.":
     "Menggas vermindert het stikstofverbruik met ongeveer 33–50% in vergelijking met puur N₂-snijden. Bovendien verbruikt het apparaat slechts 2 kWh per 24 uur — vrijwel onderhoudsvrij. De geoptimaliseerde mengverhouding betekent meer snijwerk per eenheid gas.",
    "How much gas does it save?": "Hoeveel gas bespaart het?",
    "Does the device require regular maintenance?": "Heeft het apparaat regelmatig onderhoud nodig?",
    "No. Unlike air compressors that need filter/oil changes every 500–3,000 hours, the LISHI Mixed Gas Device is maintenance-free. There are no moving parts to wear out, no filters to replace, and no oil to change.":
     "Nee. In tegenstelling tot luchtcompressoren die elke 500–3.000 uur filter-/olieverversing nodig hebben, is het LISHI Menggasapparaat onderhoudsvrij. Er zijn geen bewegende delen die slijten, geen filters te vervangen en geen olie te verversen.",
    "Does it require regular maintenance?": "Heeft het regelmatig onderhoud nodig?",
    "Can one device serve two laser machines?": "Kan één apparaat twee lasermachines bedienen?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station feeds two laser machines at different power levels (e.g., 12kW + 20kW) simultaneously — no switching, no pressure drops.":
     "Ja. LISHI LASER is de enige fabrikant die een stabiele een-op-twee-configuratie aanbiedt. Eén mengstation voedt twee lasermachines op verschillende vermogensniveaus (bijv. 12kW + 20kW) gelijktijdig — geen omschakeling, geen drukverlies.",
    "Can one device supply two lasers?": "Kan één apparaat twee lasers voeden?",
    "How is mixed gas different from air cutting?": "Hoe verschilt menggas van luchtsnijden?",
    "Air cutting produces oxidized, rough edges and carries oil/water contamination risk that can burn expensive laser head lenses ($5,000–50,000). Mixed gas from pure liquid source delivers smooth, bright, burr-free edges — and protects your optics.":
     "Luchtsnijden produceert geoxideerde, ruwe randen en brengt risico op olie-/waterverontreiniging die dure laserkoplenzen kan verbranden ($5.000–50.000). Menggas uit zuivere vloeibare bron levert gladde, heldere, braamvrije randen — en beschermt uw optiek.",
    "How long does installation take?": "Hoe lang duurt de installatie?",
    "Installation is straightforward and typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "Installatie is eenvoudig en meestal binnen één dag voltooid. Het apparaat wordt aangesloten op uw bestaande vloeibare gastoevoer en lasermachine. Wij bieden gedetailleerde installatie-instructies voor alle klanten.",
    "Installation is straightforward — typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "Installatie is eenvoudig — meestal binnen één dag voltooid. Het apparaat wordt aangesloten op uw bestaande vloeibare gastoevoer en lasermachine. Wij bieden gedetailleerde installatie-instructies voor alle klanten.",

    # CTA
    "Ready to Boost Your Cutting Speed?": "Klaar om Uw Snijsnelheid te Verhogen?",
    "Ready to Increase Your Cutting Speed?": "Klaar om Uw Snijsnelheid te Verhogen?",
    "Connect one device to your laser machine and start cutting 3× faster today. Available for 6KW–60KW machines.":
     "Sluit één apparaat aan op uw lasermachine en begin vandaag nog 3× sneller te snijden. Beschikbaar voor machines van 6KW–60KW.",
    "Contact Us →": "Neem Contact Op →",
    "Get Free Consultation": "Gratis Consultatie",

    # Footer
    "Brand-Authorized Overseas Market Operations Agent:": "Merk-Erkende Buitenlandse Marktoperatieagent:",
    "© 2025 Jinan Euchio Machinery Co., Ltd. All rights reserved.": "© 2025 Jinan Euchio Machinery Co., Ltd. Alle rechten voorbehouden.",
    "Product": "Product",
    "Cutting Samples": "Snijstalen",

    # Contact page
    "Get in Touch": "Neem Contact Op",
    "Contact Us": "Neem Contact Op",
    "Ready to boost your cutting speed? Send your laser machine details and we'll provide custom parameters and pricing.":
     "Klaar om uw snijsnelheid te verhogen? Stuur de details van uw lasermachine en wij bieden aangepaste parameters en prijzen.",
    "Email": "E-mail",
    "Reply within 24 hours": "Antwoord binnen 24 uur",
    "Phone / WeChat": "Telefoon / WeChat",
    "WeChat: same number": "WeChat: zelfde nummer",
    "Company": "Bedrijf",
    "Product Brand": "Productmerk",
    "Mixed Gas Device — 13 years in laser cutting industry": "Menggasapparaat — 13 jaar in de lasersnij-industrie",
    "Looking for a distributor?": "Op zoek naar een distributeur?",
    "We are actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "We breiden ons wereldwijde agentennetwerk actief uit. Exclusieve territoria beschikbaar voor gekwalificeerde distributeurs.",
    "Agency Application →": "Agentschapsaanvraag →",
    "Send Us a Message": "Stuur Ons een Bericht",
    "Full Name *": "Volledige Naam *",
    "John Doe": "Jan de Vries",
    "ABC Laser Co.": "ABC Laser B.V.",
    "john@company.com": "jan@bedrijf.nl",
    "Phone / WhatsApp": "Telefoon / WhatsApp",
    "+1 555 123 4567": "+31 6 12 34 56 78",
    "Country": "Land",
    "e.g. USA, Germany, Brazil": "bijv. Nederland, België, Duitsland",
    "Inquiry Type": "Type Aanvraag",
    "Select...": "Selecteer...",
    "Pricing & Quote": "Prijzen & Offerte",
    "Technical Parameters": "Technische Parameters",
    "Distributor / Agency": "Distributeur / Agentschap",
    "OEM / Customization": "OEM / Maatwerk",
    "Other": "Anders",
    "Laser Machine Power": "Lasermachine Vermogen",
    "Select laser power...": "Selecteer laservermogen...",
    "Other / Multiple": "Anders / Meerdere",
    "Laser Machine Brand": "Lasermachinemerk",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "bijv. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "Bericht *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "Beschrijf uw snijbehoeften — materiaalsoort, dikte, huidige gasconfiguratie, etc.",
    "Send Message →": "Bericht Versturen →",
    "Or reach us directly via": "Of bereik ons direct via",
    "for faster response.": "voor een snellere reactie.",
    "Your Message Has Been Sent!": "Uw Bericht Is Verzonden!",
    "Thank you for your inquiry. We will respond within 24 hours.": "Bedankt voor uw aanvraag. Wij reageren binnen 24 uur.",
    "Back to Home": "Terug naar Home",

    # Parameters page
    "Cutting Parameters": "Snijparameters",
    "Detailed cutting parameters for different laser powers. All tests performed on real customer machines. Results verified by our engineering team.":
     "Gedetailleerde snijparameters voor verschillende laservermogens. Alle tests uitgevoerd op echte klantmachines. Resultaten geverifieerd door ons engineeringteam.",
    "Thickness": "Dikte",
    "Speed Improvement": "Snelheidsverbetering",
    "Test Location": "Testlocatie",
    "Notes": "Notities",
    "Mixed Gas Optimization": "Menggas Optimalisatie",
    "Gas Consumption Comparison": "Gasverbruik Vergelijking",
    "Pure Nitrogen": "Zuivere Stikstof",
    "Mixed gas": "Menggas",
    "Savings": "Besparingen",
    "per hour": "per uur",
    "per day": "per dag",
    "per month": "per maand",
    "per year": "per jaar",
    "Download Parameters": "Parameters Downloaden",
    "Get Technical Support": "Technische Ondersteuning",
    "How do I read the cutting parameters table?": "Hoe lees ik de snijparameterstabel?",
    "The table shows cutting speed in meters per minute (m/min), mixed gas pressure in bar, and nozzle diameter in mm. Higher speeds mean better productivity. The speed improvement percentage shows the gain versus pure oxygen cutting.":
     "De tabel toont snijsnelheid in meters per minuut (m/min), menggasdruk in bar en mondstukdiameter in mm. Hogere snelheden betekenen betere productiviteit. Het snelheidsverbeteringspercentage toont de winst ten opzichte van zuiver zuurstofsnijden.",
    "Why does speed improvement decrease at very thick materials?": "Waarom neemt de snelheidsverbetering af bij zeer dikke materialen?",
    "At extreme thicknesses (30mm+), the limiting factor shifts from gas chemistry to laser power penetration. The mixed gas still provides benefits in edge quality and eliminates burrs, but the raw speed difference versus oxygen narrows because both processes are dominated by the laser beam's physical ability to penetrate the material.":
     "Bij extreme diktes (30mm+) verschuift de beperkende factor van gaschemie naar laservermogenpenetratie. Het menggas biedt nog steeds voordelen in randkwaliteit en elimineert bramen, maar het ruwe snelheidsverschil met zuurstof wordt kleiner omdat beide processen worden gedomineerd door het fysieke vermogen van de laserstraal om het materiaal te doordringen.",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER Menggasapparaat"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER Contact"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "Industriële Productie > Lasersnijapparatuur"',

    # Contact page specific
    "Contact LISHI LASER for mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Neem contact op met LISHI LASER voor menggasapparaat prijzen en offertes. Compatibel met alle grote lasermerken (HANS, DNE, PENTA, LEAD, HSG, BODOR). Wereldwijde verzending beschikbaar.",
    "Contact LISHI LASER | Get Mixed Gas Device Quote":
     "Neem Contact Op Met LISHI LASER | Offerte Menggasapparaat Aanvragen",
    "Ready to increase your cutting speed? Send us your laser machine details and we'll provide customized parameters and pricing.":
     "Klaar om uw snijsnelheid te verhogen? Stuur ons de gegevens van uw lasermachine en wij bieden aangepaste parameters en prijzen.",
    "We're actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "We breiden ons wereldwijde agentnetwerk actief uit. Exclusieve gebieden beschikbaar voor gekwalificeerde distributeurs.",
    "Looking for a Distributor?": "Op zoek naar een Distributeur?",
    "Apply for Agency →": "Vraag Agentschap Aan →",
    "Message Sent Successfully!": "Bericht Succesvol Verzonden!",
    "Thank you for your inquiry. We'll respond within 24 hours.":
     "Bedankt voor uw aanvraag. Wij reageren binnen 24 uur.",
    "Or contact us directly via": "Of neem direct contact met ons op via",
    "Select one...": "Selecteer...",
    "Distributor / Agent": "Distributeur / Agent",
    "Response within 24 hours": "Reactie binnen 24 uur",
    "Get In Touch": "Neem Contact Op",
    "Brand Licensed Overseas Market Operation Agent:":
     "Merk Gelicentieerde Buitenlandse Markt Operatie Agent:",

    # Parameters page specific
    "Carbon steel cutting speed parameters: 12kW to 60kW. Compare mixed gas vs oxygen cutting speeds. Data from real end user tests.":
     "Snijparameters voor koolstofstaal: 12kW tot 60kW. Vergelijk menggas vs zuurstof snijsnelheden. Gegevens uit echte eindgebruikerstests.",
    "20kW laser cutting parameters for 8mm carbon steel. Mixed gas vs oxygen cutting speed data for 12kW to 60kW lasers. Industrial gas mixing optimization guide with real end user data.":
     "20kW lasersnijparameters voor 8mm koolstofstaal. Menggas vs zuurstof snijsnelheid gegevens voor 12kW tot 60kW lasers. Industriële gasmengoptimalisatiegids met echte eindgebruikersgegevens.",
    "Laser Cutting Parameters by Power | Mixed Gas vs O2 Speed Data":
     "Lasersnijparameters per Vermogen | Menggas vs O2 Snelheid Gegevens",
    "Laser Cutting Parameters | LISHI LASER Mixed Gas Device":
     "Lasersnijparameters | LISHI LASER Menggasapparaat",
    "20kW Laser Cutting Parameters | Mixed Gas vs O2 Speed Data":
     "20kW Lasersnijparameters | Menggas vs O2 Snelheid Gegevens",
    "20kW Laser Cutting Parameters & Gas Speed Data":
     "20kW Lasersnijparameters & Gas Snelheid Gegevens",
    "Need detailed parameters for your specific laser machine and use case?":
     "Gedetailleerde parameters nodig voor uw specifieke lasermachine en toepassing?",
    "Contact Us for Custom Parameters →": "Neem Contact Op voor Aangepaste Parameters →",
    "Work Hours per Day": "Werkuren per Dag",
    "Actual Cutting Time (Beam-On %)": "Werkelijke Snijtijd (Straal-Aan %)",
    "Mixed Gas (N₂/O₂)": "Menggas (N₂/O₂)",
    "Competitive Edge": "Concurrentievoordeel",
    "Get a Quote": "Offerte Aanvragen",
    "Watch Video": "Bekijk Video",
    "Video demonstration of mixed gas device": "Videodemonstratie van menggasapparaat",
    "Mixed gas device cutting carbon steel": "Menggasapparaat snijdt koolstofstaal",
    "Mixed Gas Device": "Menggasapparaat",

    # Misc
    "in Laser Metal Cutting Industry": "in de Laser Metaalsnij-industrie",
    "Laser Machine": "Lasermachine",
    "micro-oxygen laser cutting technology": "micro-zuurstof lasersnijtechnologie",
}

RU = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "LISHI LASER Устройство смешанного газа для станков лазерной резки 12-60 кВт. Скорость резки в 3 раза выше, без заусенцев, расход газа на 33% меньше. Технология соотношения N2/O2 для резки углеродистой стали.",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Устройство смешанного газа | Лазерная резка в 3× быстрее",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Устройство смешанного газа для станков лазерной резки 12-60 кВт. Скорость резки в 3× выше, без заусенцев, расход газа на 33% меньше. Технология соотношения N2/O2.",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "смеситель газа лазерной резки, устройство смешивания азота и кислорода, микрокислородная лазерная резка, лазерная резка углеродистой стали, мощный лазер 12кВт 60кВт, смешанный газ против воздушного компрессора, устранение заусенцев лазерной резки, снижение расхода азота, смеситель газа Han's laser, промышленное газовое оборудование, подключение одного устройства к двум станкам, оптимизация вспомогательного газа",
    "LISHI LASER Mixed Gas Device": "LISHI LASER Устройство смешанного газа",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Цены и предложения на устройство смешанного газа LISHI LASER. Совместимо со всеми основными брендами лазеров (HANS, DNE, PENTA, LEAD, HSG, BODOR). Доступна международная доставка.",

    "Mixed gas device for carbon steel laser cutting — 3× faster than oxygen, zero burrs, 33% nitrogen savings":
     "Устройство смешанного газа для лазерной резки углеродистой стали — в 3× быстрее кислорода, без заусенцев, экономия азота 33%",
    "Get LISHI LASER mixed gas cutting parameters and pricing. Compatible with HANS, DNE, PENTA, LEAD, HSG, BODOR. Global shipping.":
     "Получите параметры резки и цены на смешанный газ LISHI LASER. Совместимо с HANS, DNE, PENTA, LEAD, HSG, BODOR. Международная доставка.",
    "LISHI LASER Mixed Gas Device | Industrial Laser Cutting Gas Mixer":
     "LISHI LASER Устройство смешанного газа | Промышленный смеситель газа для лазерной резки",

    # Hero
    "Cut <span class=\"accent\">3× Faster</span><br>with Mixed Gas Technology":
     "Режьте <span class=\"accent\">в 3× Быстрее</span><br>с Технологией Смешанного Газа",
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "Решение на смешанном газе N₂/O₂ для станков лазерной резки 12-60 кВт",
    "3× Faster Than O₂": "В 3× Быстрее, чем O₂",
    "Zero Burrs": "Без Заусенцев",
    "33% Less Nitrogen": "На 33% Меньше Азота",

    # Nav
    "Home": "Главная",
    "Principle": "Принцип",
    "Advantages": "Преимущества",
    "Parameters": "Параметры",
    "Samples": "Образцы",
    "Clients": "Клиенты",
    "Contact": "Контакты",
    "FAQ": "Вопросы",
    "Primary navigation": "Основная навигация",

    # Principle
    "What is a Mixed Gas Device?": "Что такое устройство смешанного газа?",
    "The mixed gas device combines high-purity liquid nitrogen (N₂) and liquid oxygen (O₂) through precision IGBT-controlled mixing technology.":
     "Устройство смешанного газа объединяет жидкий азот высокой чистоты (N₂) и жидкий кислород (O₂) с помощью прецизионной технологии смешивания с IGBT-управлением.",
    "The result is an auxiliary gas that is 3 times faster than pure oxygen for carbon steel cutting, and far more economical than pure nitrogen.":
     "В результате получается вспомогательный газ, который в 3 раза быстрее чистого кислорода для резки углеродистой стали и значительно экономичнее чистого азота.",

    # Advantages
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "Почему смешанный газ вместо O₂, N₂ или воздуха?",
    "Eliminate burrs in carbon steel laser cutting while reducing nitrogen consumption by 33%. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Устраните заусенцы при лазерной резке углеродистой стали, снижая расход азота на 33%. Наша необслуживаемая система подачи газа совместима с HAN'S, DNE, PENTA, LEAD, HSG, BODOR и другими ведущими брендами.",

    "3× Faster Cutting": "Резка в 3× Быстрее",
    "Increase laser cutting speed up to 3 times compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Увеличьте скорость лазерной резки до 3 раз по сравнению с кислородной резкой. Пример: углеродистая сталь 8 мм — 16 м/мин со смешанным газом, всего 2–3 м/мин с O₂.",
    "Eliminate Burrs": "Устранение Заусенцев",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cut edges requiring no additional sanding.":
     "Контролируемая микрокислородная среда обеспечивает полное сгорание. Результат: гладкие края без заусенцев, не требующие дополнительной шлифовки.",
    "Lower Gas Costs": "Снижение Затрат на Газ",
    "Optimized N₂/O₂ mixing ratio reduces nitrogen usage by approximately one third compared to pure nitrogen.":
     "Оптимизированное соотношение смешивания N₂/O₂ снижает расход азота примерно на треть по сравнению с чистым азотом.",
    "Maintenance-Free": "Без Обслуживания",
    "Power consumption: only 2 kWh in 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Энергопотребление: всего 2 кВт·ч за 24 часа. В отличие от воздушных компрессоров, требующих замены фильтров/масла каждые 3000 часов, наше промышленное газовое оборудование не требует обслуживания.",
    "One-to-Two Laser Setup": "Подключение к Двум Станкам",
    "A single mixed gas device can simultaneously supply two laser cutting machines, cutting equipment costs in half.":
     "Одно устройство смешанного газа может одновременно питать два станка лазерной резки, сокращая затраты на оборудование вдвое.",
    "Lens Protection": "Защита Линз",
    "Unlike air compressors that introduce oil vapor and particulates, our closed-loop gas system delivers clean, dry gas that protects your laser optics.":
     "В отличие от воздушных компрессоров, вносящих пары масла и частицы, наша замкнутая газовая система подает чистый, сухой газ, защищающий лазерную оптику.",
    "Wide Compatibility": "Широкая Совместимость",
    "Compatible with all major laser brands: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. Supports from 12kW to 60kW.":
     "Совместимо со всеми основными брендами: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA и MESSER. Поддерживает от 12 до 60 кВт.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air":
     "Сравнение производительности: смешанный газ против O₂ против N₂ против воздуха",
    "Pure Oxygen (O₂)": "Чистый кислород (O₂)",
    "Pure Nitrogen (N₂)": "Чистый азот (N₂)",
    "Air (Compressor)": "Воздух (Компрессор)",
    "Mixed Gas (N₂/O₂)": "Смешанный газ (N₂/O₂)",
    "Burred edges": "Края с заусенцами",
    "Perfectly smooth": "Идеально гладкие",
    "Low quality": "Низкое качество",
    "Very high": "Очень высокий",
    "Low (~33% savings)": "Низкий (~33% экономии)",
    "Frequent cleaning required": "Требуется частая очистка",
    "Minimal": "Минимальное",
    "Compressor maintenance": "Обслуживание компрессора",

    # ROI
    "Calculate Your Laser Cutting Gas Cost Savings": "Рассчитайте экономию затрат на газ для лазерной резки",
    "Machine Power": "Мощность станка",
    "Material Thickness": "Толщина материала",
    "Daily Work Hours": "Часов работы в день",
    "Gas Cost (/m³)": "Стоимость газа (/м³)",
    "Calculate": "Рассчитать",
    "Estimated Annual Savings": "Расчетная годовая экономия",
    "Investment Payback Period": "Срок окупаемости инвестиций",
    "months": "месяцев",
    "Estimated Annual Profit Increase (USD)": "Расчетное годовое увеличение прибыли (USD)",
    "Get Free Parameters →": "Получить параметры бесплатно →",
    "ROI Calculator": "Калькулятор окупаемости",
    "Calculator": "Калькулятор",

    # Air vs Mixed
    "Air Seems Free. The Reality Is Not.": "Воздух кажется бесплатным. На деле — нет.",
    "Why Air Costs More": "Почему воздух обходится дороже",
    "High Maintenance Cost": "Высокие затраты на обслуживание",
    "Air compressor systems require regular filter changes, oil changes, and dryer maintenance. Annual maintenance costs typically range from $2,000 to $5,000.":
     "Системы воздушных компрессоров требуют регулярной замены фильтров, масла и обслуживания осушителя. Годовые затраты на обслуживание обычно составляют от $2 000 до $5 000.",
    "Poor Cut Quality": "Низкое качество резки",
    "Air cutting cannot control oxidation, resulting in burrs and discoloration on cut edges.":
     "Резка воздухом не может контролировать окисление, что приводит к заусенцам и изменению цвета на краях реза.",
    "Lens Contamination": "Загрязнение линз",
    "Oil vapor and particulates from the compressor contaminate laser optics, reducing lens life.":
     "Пары масла и частицы из компрессора загрязняют лазерную оптику, сокращая срок службы линз.",
    "Energy Consumption": "Энергопотребление",
    "Air compressors typically consume 15–30kW per hour. The mixed gas device consumes only 2kWh/24h.":
     "Воздушные компрессоры обычно потребляют 15–30 кВт в час. Устройство смешанного газа потребляет всего 2 кВт·ч за 24 часа.",
    "Noise": "Шум",
    "Air compressors produce 75–85dB of noise. The mixed gas device operates silently.":
     "Воздушные компрессоры создают шум 75–85 дБ. Устройство смешанного газа работает бесшумно.",

    # Parameters section
    "Cutting Parameters by Power": "Параметры резки по мощности",
    "View All Parameters →": "Смотреть все параметры →",
    "Detailed Parameters →": "Подробные параметры →",

    # Samples
    "Cutting Samples and Test Videos": "Образцы резки и видео испытаний",
    "Real customer cutting results, tested across different materials and power levels.":
     "Реальные результаты резки клиентов, протестированные на разных материалах и уровнях мощности.",
    "Watch Video": "Смотреть видео",
    "Cutting Video": "Видео резки",
    "Before / After": "До / После",

    # Global
    "GLOBAL NETWORK": "ГЛОБАЛЬНАЯ СЕТЬ",
    "50+ Countries": "50+ Стран",
    "500+ Systems Installed": "500+ Установленных Систем",
    "30+ Distributors": "30+ Дистрибьюторов",
    "Global After-Sales Support": "Глобальная послепродажная поддержка",
    "Asia": "Азия",
    "Europe": "Европа",
    "Americas": "Америка",
    "Africa": "Африка",
    "Oceania": "Океания",

    # FAQ
    "Frequently Asked Questions": "Часто задаваемые вопросы",

    # CTA
    "Ready to Increase Your Cutting Speed?": "Готовы увеличить скорость резки?",
    "Contact us now for a customized solution and pricing.":
     "Свяжитесь с нами сейчас для индивидуального решения и расчета стоимости.",
    "Contact Us Now": "Связаться с нами",
    "Get Free Consultation": "Получить бесплатную консультацию",
    "Get a Quote": "Получить предложение",
    "How It Works →": "Как это работает →",

    # Footer
    "Brand Licensed Overseas Market Operation Agent:":
     "Лицензированный агент по зарубежным рыночным операциям:",
    "All rights reserved.": "Все права защищены.",
    "Gas Mixing Technology": "Технология смешивания газов",
    "Product": "Продукт",
    "How It Works": "Как это работает",
    "Cutting Samples": "Образцы резки",

    # Contact page
    "Get In Touch": "Свяжитесь с нами",
    "Contact Us": "Свяжитесь с нами",
    "Ready to increase your cutting speed? Send us your laser machine details and we'll provide customized parameters and pricing.":
     "Готовы увеличить скорость резки? Отправьте нам данные о вашем лазерном станке, и мы предоставим индивидуальные параметры и цены.",
    "Email": "Эл. почта",
    "Response within 24 hours": "Ответ в течение 24 часов",
    "Phone / WeChat": "Телефон / WeChat",
    "WeChat: same number": "WeChat: тот же номер",
    "WhatsApp": "WhatsApp",
    "Company": "Компания",
    "Product Brand": "Бренд продукта",
    "Mixed Gas Device — 13 Years in Laser Cutting Industry": "Устройство смешанного газа — 13 лет в отрасли лазерной резки",
    "Looking for a Distributor?": "Ищете дистрибьютора?",
    "We're actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "Мы активно расширяем нашу глобальную агентскую сеть. Эксклюзивные территории доступны для квалифицированных дистрибьюторов.",
    "Apply for Agency →": "Подать заявку на агентство →",
    "Send Us a Message": "Отправьте нам сообщение",
    "Full Name *": "Полное имя *",
    "John Smith": "Иван Петров",
    "ABC Laser Ltd.": "ООО ЛазерТех",
    "john@company.com": "ivan@kompaniya.ru",
    "Phone / WhatsApp": "Телефон / WhatsApp",
    "+1 234 567 8900": "+7 999 123 4567",
    "Country": "Страна",
    "e.g. Mexico, Thailand, India": "напр. Россия, Германия, Польша",
    "Inquiry Type": "Тип запроса",
    "Select one...": "Выберите...",
    "Pricing & Quote": "Цены и предложение",
    "Technical Parameters": "Технические параметры",
    "Distributor / Agent": "Дистрибьютор / Агент",
    "OEM / Customization": "OEM / Индивидуальная настройка",
    "Other": "Другое",
    "Laser Machine Power": "Мощность лазерного станка",
    "Select laser power...": "Выберите мощность лазера...",
    "Other / Multiple": "Другое / Несколько",
    "Laser Machine Brand": "Бренд лазерного станка",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "напр. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "Сообщение *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "Опишите ваши потребности в резке — тип материала, толщина, текущая газовая установка и т.д.",
    "Send Message →": "Отправить сообщение →",
    "Or contact us directly via": "Или свяжитесь с нами напрямую через",
    "Message Sent Successfully!": "Сообщение успешно отправлено!",
    "Thank you for your inquiry. We'll respond within 24 hours.":
     "Спасибо за ваш запрос. Мы ответим в течение 24 часов.",
    "Back to Home": "На главную",

    # Parameters page
    "Cutting Parameters": "Параметры резки",
    "Below are detailed cutting parameters for different laser powers. All tests performed on real customer machines.":
     "Ниже приведены подробные параметры резки для различных мощностей лазера. Все испытания проведены на реальных станках клиентов.",
    "Thickness": "Толщина",
    "Mixed Gas Speed": "Скорость смешанного газа",
    "Speed Increase": "Увеличение скорости",
    "Test Location": "Место испытания",
    "Notes": "Примечания",
    "Mixed Gas Optimization": "Оптимизация смешанного газа",
    "Gas Consumption Comparison": "Сравнение расхода газа",
    "Pure Nitrogen": "Чистый азот",
    "Mixed Gas": "Смешанный газ",
    "Savings": "Экономия",
    "per hour": "в час",
    "per day": "в день",
    "per month": "в месяц",
    "per year": "в год",
    "Download Parameters": "Скачать параметры",
    "Get Technical Support": "Получить техподдержку",
    "View Parameters": "Смотреть параметры",

    # Contact page meta
    "Contact LISHI LASER for mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Свяжитесь с LISHI LASER для получения цен и предложений на устройство смешанного газа. Совместимо со всеми основными брендами лазеров (HANS, DNE, PENTA, LEAD, HSG, BODOR). Доступна международная доставка.",
    "Contact LISHI LASER | Get Mixed Gas Device Quote":
     "Свяжитесь с LISHI LASER | Получите предложение на устройство смешанного газа",

    # Parameters page meta
    "Carbon steel cutting speed parameters: 12kW to 60kW. Compare mixed gas vs oxygen cutting speeds. Data from real end user tests.":
     "Параметры скорости резки углеродистой стали: от 12 до 60 кВт. Сравнение скорости резки смешанным газом и кислородом. Данные реальных испытаний.",
    "20kW laser cutting parameters for 8mm carbon steel. Mixed gas vs oxygen cutting speed data for 12kW to 60kW lasers. Industrial gas mixing optimization guide with real end user data.":
     "Параметры лазерной резки 20 кВт для углеродистой стали 8 мм. Данные о скорости резки смешанным газом и кислородом для лазеров от 12 до 60 кВт. Руководство по оптимизации промышленного смешивания газов с реальными данными.",
    "Laser Cutting Parameters by Power | Mixed Gas vs O2 Speed Data":
     "Параметры лазерной резки по мощности | Сравнение скорости смешанного газа и O2",
    "Laser Cutting Parameters | LISHI LASER Mixed Gas Device":
     "Параметры лазерной резки | LISHI LASER Устройство смешанного газа",
    "20kW Laser Cutting Parameters | Mixed Gas vs O2 Speed Data":
     "Параметры лазерной резки 20 кВт | Сравнение скорости смешанного газа и O2",
    "20kW Laser Cutting Parameters & Gas Speed Data":
     "Параметры лазерной резки 20 кВт и данные о скорости газа",
    "Need detailed parameters for your specific laser machine and use case?":
     "Нужны подробные параметры для вашего конкретного лазерного станка и применения?",
    "Contact Us for Custom Parameters →": "Свяжитесь с нами для индивидуальных параметров →",

    # Additional UI labels
    "Work Hours per Day": "Часов работы в день",
    "Actual Cutting Time (Beam-On %)": "Фактическое время резки (Луч-Вкл %)",
    "Competitive Edge": "Конкурентное преимущество",
    "Watch Video": "Смотреть видео",
    "Video demonstration of mixed gas device": "Видеодемонстрация устройства смешанного газа",
    "Mixed gas device cutting carbon steel": "Устройство смешанного газа режет углеродистую сталь",
    "Mixed Gas Device": "Устройство смешанного газа",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER Устройство смешанного газа"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER Контакты"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "Промышленное производство > Оборудование для лазерной резки"',

    # FAQ content
    "What is a mixed gas device and how does it work?":
     "Что такое устройство смешанного газа и как оно работает?",
    "The mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen mixture is used as an auxiliary gas in high-power laser cutting, delivering 3× faster cutting speed compared to pure oxygen on carbon steel while completely eliminating burrs.":
     "Устройство смешанного газа преобразует жидкий азот (N₂) и жидкий кислород (O₂) в точно калиброванную газовую смесь N₂/O₂ (обычно 95%/5%). Эта микрокислородная смесь используется в качестве вспомогательного газа при мощной лазерной резке, обеспечивая скорость резки в 3 раза выше по сравнению с чистым кислородом на углеродистой стали и полностью устраняя заусенцы.",
    "Is it compatible with my laser machine?":
     "Совместимо ли с моим лазерным станком?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it's compatible.":
     "Да. Устройство смешанного газа LISHI LASER работает со всеми основными брендами лазеров, включая HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA и MESSER. Поддерживает станки от 12 до 60 кВт. Если ваш станок использует стандартные подключения вспомогательного газа, он совместим.",
    "What thicknesses can it cut?": "Какие толщины можно резать?",
    "The mixed gas device can cut carbon steel, stainless steel and aluminum from 1mm to 30mm. Cutting thickness depends on your laser power. Detailed cutting parameter tables are available on our parameters page below.":
     "Устройство смешанного газа может резать углеродистую сталь, нержавеющую сталь и алюминий от 1 до 30 мм. Толщина резки зависит от мощности вашего лазера. Подробные таблицы параметров резки доступны на нашей странице параметров.",
    "Mixed gas is primarily used for carbon steel cutting where it delivers the best speed and quality. It also works well for stainless steel and aluminum, though the speed advantage is less pronounced for non-ferrous metals.":
     "Смешанный газ в основном используется для резки углеродистой стали, где он обеспечивает наилучшую скорость и качество. Он также хорошо работает с нержавеющей сталью и алюминием, хотя преимущество в скорости менее выражено для цветных металлов.",
    "How much faster is mixed gas compared to pure oxygen cutting?":
     "Насколько быстрее смешанный газ по сравнению с чисто кислородной резкой?",
    "Mixed gas cutting is 2.5× to 7× faster than pure oxygen cutting depending on material thickness. For example: 6mm carbon steel — mixed gas 18m/min vs oxygen 3m/min (6× faster); 12mm carbon steel — mixed gas 8m/min vs oxygen 1.5m/min (5.3× faster).":
     "Резка смешанным газом в 2,5–7 раз быстрее, чем резка чистым кислородом, в зависимости от толщины материала. Например: углеродистая сталь 6 мм — смешанный газ 18 м/мин против кислорода 3 м/мин (в 6 раз быстрее); 12 мм — смешанный газ 8 м/мин против кислорода 1,5 м/мин (в 5,3 раза быстрее).",
    "How much nitrogen can be saved by using mixed gas instead of pure N₂?":
     "Сколько азота можно сэкономить, используя смешанный газ вместо чистого N₂?",
    "Mixed gas reduces nitrogen consumption by 33–50% compared to pure N₂ cutting. The small percentage of oxygen (5%) allows the oxidation reaction to contribute cutting energy, meaning you need less total gas flow for the same cut.":
     "Смешанный газ снижает расход азота на 33–50% по сравнению с резкой чистым N₂. Небольшой процент кислорода (5%) позволяет реакции окисления вносить энергию резки, что означает меньший общий расход газа для того же реза.",
    "Does mixed gas really eliminate burrs?": "Действительно ли смешанный газ устраняет заусенцы?",
    "Yes. The controlled micro-oxygen content in the nitrogen/oxygen mixture enables complete combustion without the excessive oxidation that occurs with pure oxygen or air cutting. Result: clean, burr-free edges requiring no additional sanding or grinding.":
     "Да. Контролируемое содержание микрокислорода в азотно-кислородной смеси обеспечивает полное сгорание без чрезмерного окисления, возникающего при резке чистым кислородом или воздухом. Результат: чистые края без заусенцев, не требующие дополнительной шлифовки.",
    "Is it difficult to install and maintain?": "Сложно ли устанавливать и обслуживать?",
    "Installation is simple — a compact unit that connects to your existing laser machine. Maintenance is minimal: only 2kWh/24h power consumption and a basic annual check. No moving parts, so no wear or frequent service needed.":
     "Установка проста — компактный блок, подключаемый к вашему существующему лазерному станку. Обслуживание минимально: всего 2 кВт·ч/24 ч энергопотребления и базовая ежегодная проверка. Нет движущихся частей, поэтому нет износа или необходимости в частом обслуживании.",
    "Can one mixed gas device supply two laser machines simultaneously?":
     "Может ли одно устройство подавать газ на два лазерных станка одновременно?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station can simultaneously supply two laser cutting machines with independent flow control, effectively halving your equipment cost per machine.":
     "Да. LISHI LASER — единственный производитель, предлагающий стабильную конфигурацию «один к двум». Одна смесительная станция может одновременно питать два станка лазерной резки с независимым контролем потока, эффективно сокращая затраты на оборудование вдвое.",
    "What are the input gas pressure requirements?": "Каковы требования к входному давлению газа?",
    "The LISHI LASER Mixed Gas Device has an input pressure requirement of 20–25 bar from liquid N₂ and O₂ storage tanks, with an output pressure range of 15–30 bar adjustable for different laser machines and cutting applications.":
     "Устройство смешанного газа LISHI LASER требует входного давления 20–25 бар от резервуаров жидкого N₂ и O₂, с диапазоном выходного давления 15–30 бар, регулируемым для различных лазерных станков и применений резки.",
    "Is it guaranteed?": "Есть ли гарантия?",
    "Yes, all LISHI LASER Mixed Gas Devices are covered by a 1-year warranty from the date of purchase. Extended warranty options are available through our global after-sales support network.":
     "Да, все устройства смешанного газа LISHI LASER покрываются гарантией 1 год с даты покупки. Варианты расширенной гарантии доступны через нашу глобальную сеть послепродажной поддержки.",
    "What laser power levels are supported by the LISHI LASER Mixed Gas Device?":
     "Какие уровни мощности лазера поддерживает устройство смешанного газа LISHI LASER?",
    "The device supports laser machines from 12KW to 60KW. 12KW handles up to 16mm carbon steel, 20KW up to 25mm, 30KW up to 30mm. Contact us for parameters specific to your power level.":
     "Устройство поддерживает лазерные станки от 12 до 60 кВт. 12 кВт режет углеродистую сталь до 16 мм, 20 кВт до 25 мм, 30 кВт до 30 мм. Свяжитесь с нами для получения параметров для вашего уровня мощности.",

    # Misc
    "in Laser Metal Cutting Industry": "в отрасли лазерной резки металла",
    "Laser Machine": "Лазерный станок",
    "micro-oxygen laser cutting technology": "микрокислородная технология лазерной резки",
}

VI = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "Thiết bị Khí Hỗn hợp LISHI LASER cho máy cắt laser 12KW-60KW. Tốc độ cắt nhanh gấp 3 lần, không ba via, tiêu thụ khí ít hơn 33%. Công nghệ tỷ lệ N2/O2 cho cắt thép carbon.",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Thiết bị Khí Hỗn hợp | Cắt Laser Nhanh Gấp 3×",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Thiết bị khí hỗn hợp cho máy cắt laser 12KW-60KW. Tốc độ cắt nhanh gấp 3×, không ba via, tiêu thụ khí ít hơn 33%. Công nghệ tỷ lệ N2/O2.",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "máy trộn khí cắt laser, thiết bị trộn nitơ oxy, cắt laser vi oxy, cắt laser thép carbon, laser công suất cao 12kW 60kW, khí hỗn hợp so với máy nén khí, loại bỏ ba via cắt laser, giảm tiêu thụ nitơ, máy trộn khí laser Han's, thiết bị khí laser công nghiệp, cấu hình khí một-đến-hai, tối ưu hóa khí phụ trợ",
    "LISHI LASER Mixed Gas Device": "Thiết bị Khí Hỗn hợp LISHI LASER",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Giá và báo giá thiết bị khí hỗn hợp LISHI LASER. Tương thích với tất cả các thương hiệu laser lớn (HANS, DNE, PENTA, LEAD, HSG, BODOR). Vận chuyển toàn cầu.",

    "Mixed gas device for carbon steel laser cutting — 3× faster than oxygen, zero burrs, 33% nitrogen savings":
     "Thiết bị khí hỗn hợp cho cắt laser thép carbon — nhanh gấp 3× so với oxy, không ba via, tiết kiệm nitơ 33%",
    "Get LISHI LASER mixed gas cutting parameters and pricing. Compatible with HANS, DNE, PENTA, LEAD, HSG, BODOR. Global shipping.":
     "Nhận thông số cắt và giá thiết bị khí hỗn hợp LISHI LASER. Tương thích với HANS, DNE, PENTA, LEAD, HSG, BODOR. Vận chuyển toàn cầu.",
    "LISHI LASER Mixed Gas Device | Industrial Laser Cutting Gas Mixer":
     "LISHI LASER Thiết bị Khí Hỗn hợp | Máy Trộn Khí Cắt Laser Công nghiệp",

    # Hero
    "Cut <span class=\"accent\">3× Faster</span><br>with Mixed Gas Technology":
     "Cắt <span class=\"accent\">Nhanh Gấp 3×</span><br>với Công nghệ Khí Hỗn hợp",
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "Giải pháp khí hỗn hợp N₂/O₂ cho máy cắt laser 12KW-60KW",
    "3× Faster Than O₂": "Nhanh Gấp 3× So với O₂",
    "Zero Burrs": "Không Ba Via",
    "33% Less Nitrogen": "Ít Hơn 33% Nitơ",

    # Nav
    "Home": "Trang chủ",
    "Principle": "Nguyên lý",
    "Advantages": "Ưu điểm",
    "Parameters": "Thông số",
    "Samples": "Mẫu",
    "Clients": "Khách hàng",
    "Contact": "Liên hệ",
    "FAQ": "Hỏi đáp",
    "Primary navigation": "Điều hướng chính",

    # Principle
    "What is a Mixed Gas Device?": "Thiết bị Khí Hỗn hợp là gì?",
    "The mixed gas device combines high-purity liquid nitrogen (N₂) and liquid oxygen (O₂) through precision IGBT-controlled mixing technology.":
     "Thiết bị khí hỗn hợp kết hợp nitơ lỏng (N₂) và oxy lỏng (O₂) độ tinh khiết cao thông qua công nghệ trộn điều khiển IGBT chính xác.",
    "The result is an auxiliary gas that is 3 times faster than pure oxygen for carbon steel cutting, and far more economical than pure nitrogen.":
     "Kết quả là khí phụ trợ nhanh gấp 3 lần so với oxy tinh khiết để cắt thép carbon, và tiết kiệm hơn nhiều so với nitơ tinh khiết.",

    # Advantages
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "Tại sao chọn Khí Hỗn hợp thay vì O₂, N₂ hoặc Không khí?",
    "Eliminate burrs in carbon steel laser cutting while reducing nitrogen consumption by 33%. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Loại bỏ ba via trong cắt laser thép carbon đồng thời giảm tiêu thụ nitơ 33%. Hệ thống cung cấp khí không cần bảo trì của chúng tôi tương thích với HAN'S, DNE, PENTA, LEAD, HSG, BODOR và tất cả các thương hiệu lớn khác.",

    "3× Faster Cutting": "Cắt Nhanh Gấp 3×",
    "Increase laser cutting speed up to 3 times compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Tăng tốc độ cắt laser lên đến 3 lần so với cắt oxy. Ví dụ: thép carbon 8mm ở 16m/phút với khí hỗn hợp, chỉ 2–3m/phút với O₂.",
    "Eliminate Burrs": "Loại bỏ Ba Via",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cut edges requiring no additional sanding.":
     "Môi trường vi oxy được kiểm soát đảm bảo đốt cháy hoàn toàn. Kết quả: các cạnh cắt mịn, không ba via, không cần chà nhám thêm.",
    "Lower Gas Costs": "Giảm Chi phí Khí",
    "Optimized N₂/O₂ mixing ratio reduces nitrogen usage by approximately one third compared to pure nitrogen.":
     "Tỷ lệ trộn N₂/O₂ được tối ưu hóa giảm sử dụng nitơ khoảng một phần ba so với nitơ tinh khiết.",
    "Maintenance-Free": "Không Cần Bảo trì",
    "Power consumption: only 2 kWh in 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Tiêu thụ điện: chỉ 2 kWh trong 24 giờ. Không giống như máy nén khí yêu cầu thay bộ lọc/dầu mỗi 3.000 giờ, thiết bị khí laser công nghiệp của chúng tôi không cần bảo trì.",
    "One-to-Two Laser Setup": "Cấu hình Một-đến-Hai",
    "A single mixed gas device can simultaneously supply two laser cutting machines, cutting equipment costs in half.":
     "Một thiết bị khí hỗn hợp có thể đồng thời cung cấp cho hai máy cắt laser, giảm một nửa chi phí thiết bị.",
    "Lens Protection": "Bảo vệ Thấu kính",
    "Unlike air compressors that introduce oil vapor and particulates, our closed-loop gas system delivers clean, dry gas that protects your laser optics.":
     "Không giống như máy nén khí đưa hơi dầu và hạt vào, hệ thống khí vòng kín của chúng tôi cung cấp khí sạch, khô bảo vệ quang học laser của bạn.",
    "Wide Compatibility": "Tương thích Rộng",
    "Compatible with all major laser brands: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. Supports from 12kW to 60kW.":
     "Tương thích với tất cả các thương hiệu laser lớn: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA và MESSER. Hỗ trợ từ 12kW đến 60kW.",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air":
     "So sánh Hiệu suất: Khí Hỗn hợp vs O₂ vs N₂ vs Không khí",
    "Pure Oxygen (O₂)": "Oxy Tinh khiết (O₂)",
    "Pure Nitrogen (N₂)": "Nitơ Tinh khiết (N₂)",
    "Air (Compressor)": "Không khí (Máy nén)",
    "Mixed Gas (N₂/O₂)": "Khí Hỗn hợp (N₂/O₂)",
    "Burred edges": "Cạnh có ba via",
    "Perfectly smooth": "Mịn hoàn hảo",
    "Low quality": "Chất lượng thấp",
    "Very high": "Rất cao",
    "Low (~33% savings)": "Thấp (~33% tiết kiệm)",
    "Frequent cleaning required": "Cần vệ sinh thường xuyên",
    "Minimal": "Tối thiểu",
    "Compressor maintenance": "Bảo trì máy nén",

    # ROI
    "Calculate Your Laser Cutting Gas Cost Savings": "Tính Toán Tiết Kiệm Chi phí Khí Cắt Laser",
    "Machine Power": "Công suất Máy",
    "Material Thickness": "Độ dày Vật liệu",
    "Daily Work Hours": "Giờ Làm việc Hàng ngày",
    "Gas Cost (/m³)": "Chi phí Khí (/m³)",
    "Calculate": "Tính toán",
    "Estimated Annual Savings": "Tiết Kiệm Hàng năm Ước tính",
    "Investment Payback Period": "Thời gian Hoàn vốn Đầu tư",
    "months": "tháng",
    "Estimated Annual Profit Increase (USD)": "Tăng Lợi nhuận Hàng năm Ước tính (USD)",
    "Get Free Parameters →": "Nhận Thông số Miễn phí →",
    "ROI Calculator": "Máy tính ROI",
    "Calculator": "Máy tính",

    # Air vs Mixed
    "Air Seems Free. The Reality Is Not.": "Không khí Có vẻ Miễn phí. Thực tế Không Phải.",
    "Why Air Costs More": "Tại sao Không khí Tốn Nhiều hơn",
    "High Maintenance Cost": "Chi phí Bảo trì Cao",
    "Air compressor systems require regular filter changes, oil changes, and dryer maintenance. Annual maintenance costs typically range from $2,000 to $5,000.":
     "Hệ thống máy nén khí yêu cầu thay bộ lọc, thay dầu và bảo trì máy sấy thường xuyên. Chi phí bảo trì hàng năm thường từ $2.000 đến $5.000.",
    "Poor Cut Quality": "Chất lượng Cắt Kém",
    "Air cutting cannot control oxidation, resulting in burrs and discoloration on cut edges.":
     "Cắt bằng không khí không thể kiểm soát oxy hóa, dẫn đến ba via và đổi màu trên các cạnh cắt.",
    "Lens Contamination": "Nhiễm bẩn Thấu kính",
    "Oil vapor and particulates from the compressor contaminate laser optics, reducing lens life.":
     "Hơi dầu và hạt từ máy nén làm nhiễm bẩn quang học laser, giảm tuổi thọ thấu kính.",
    "Energy Consumption": "Tiêu thụ Năng lượng",
    "Air compressors typically consume 15–30kW per hour. The mixed gas device consumes only 2kWh/24h.":
     "Máy nén khí thường tiêu thụ 15–30kW mỗi giờ. Thiết bị khí hỗn hợp chỉ tiêu thụ 2kWh/24h.",
    "Noise": "Tiếng ồn",
    "Air compressors produce 75–85dB of noise. The mixed gas device operates silently.":
     "Máy nén khí tạo ra tiếng ồn 75–85dB. Thiết bị khí hỗn hợp hoạt động im lặng.",

    # Parameters section
    "Cutting Parameters by Power": "Thông số Cắt theo Công suất",
    "View All Parameters →": "Xem Tất cả Thông số →",
    "Detailed Parameters →": "Thông số Chi tiết →",

    # Samples
    "Cutting Samples and Test Videos": "Mẫu Cắt và Video Thử nghiệm",
    "Real customer cutting results, tested across different materials and power levels.":
     "Kết quả cắt thực tế của khách hàng, được thử nghiệm trên các vật liệu và mức công suất khác nhau.",
    "Watch Video": "Xem Video",
    "Cutting Video": "Video Cắt",
    "Before / After": "Trước / Sau",

    # Global
    "GLOBAL NETWORK": "MẠNG LƯỚI TOÀN CẦU",
    "50+ Countries": "50+ Quốc gia",
    "500+ Systems Installed": "500+ Hệ thống Đã Lắp đặt",
    "30+ Distributors": "30+ Nhà phân phối",
    "Global After-Sales Support": "Hỗ trợ Hậu mãi Toàn cầu",
    "Asia": "Châu Á",
    "Europe": "Châu Âu",
    "Americas": "Châu Mỹ",
    "Africa": "Châu Phi",
    "Oceania": "Châu Đại Dương",

    # FAQ
    "Frequently Asked Questions": "Câu hỏi Thường gặp",

    # CTA
    "Ready to Increase Your Cutting Speed?": "Sẵn sàng Tăng Tốc độ Cắt?",
    "Contact us now for a customized solution and pricing.":
     "Liên hệ với chúng tôi ngay để có giải pháp và báo giá tùy chỉnh.",
    "Contact Us Now": "Liên hệ Ngay",
    "Get Free Consultation": "Nhận Tư vấn Miễn phí",
    "Get a Quote": "Nhận Báo giá",
    "How It Works →": "Cách Hoạt động →",

    # Footer
    "Brand Licensed Overseas Market Operation Agent:":
     "Đại lý Vận hành Thị trường Nước ngoài Được Cấp phép:",
    "All rights reserved.": "Đã đăng ký bản quyền.",
    "Gas Mixing Technology": "Công nghệ Trộn Khí",
    "Product": "Sản phẩm",
    "How It Works": "Cách Hoạt động",
    "Cutting Samples": "Mẫu Cắt",

    # Contact page
    "Get In Touch": "Liên hệ",
    "Contact Us": "Liên hệ với Chúng tôi",
    "Ready to increase your cutting speed? Send us your laser machine details and we'll provide customized parameters and pricing.":
     "Sẵn sàng tăng tốc độ cắt? Gửi cho chúng tôi chi tiết máy laser của bạn và chúng tôi sẽ cung cấp thông số và báo giá tùy chỉnh.",
    "Email": "Email",
    "Response within 24 hours": "Phản hồi trong vòng 24 giờ",
    "Phone / WeChat": "Điện thoại / WeChat",
    "WeChat: same number": "WeChat: cùng số",
    "WhatsApp": "WhatsApp",
    "Company": "Công ty",
    "Product Brand": "Thương hiệu Sản phẩm",
    "Mixed Gas Device — 13 Years in Laser Cutting Industry": "Thiết bị Khí Hỗn hợp — 13 Năm trong Ngành Cắt Laser",
    "Looking for a Distributor?": "Đang tìm Nhà phân phối?",
    "We're actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "Chúng tôi đang tích cực mở rộng mạng lưới đại lý toàn cầu. Các lãnh thổ độc quyền có sẵn cho các nhà phân phối đủ điều kiện.",
    "Apply for Agency →": "Đăng ký Đại lý →",
    "Send Us a Message": "Gửi Tin nhắn cho Chúng tôi",
    "Full Name *": "Họ và Tên *",
    "John Smith": "Nguyễn Văn A",
    "ABC Laser Ltd.": "Công ty TNHH Laser ABC",
    "john@company.com": "nguyenvana@congty.com",
    "Phone / WhatsApp": "Điện thoại / WhatsApp",
    "+1 234 567 8900": "+84 999 123 456",
    "Country": "Quốc gia",
    "e.g. Mexico, Thailand, India": "vd. Việt Nam, Thái Lan, Ấn Độ",
    "Inquiry Type": "Loại Yêu cầu",
    "Select one...": "Chọn...",
    "Pricing & Quote": "Giá & Báo giá",
    "Technical Parameters": "Thông số Kỹ thuật",
    "Distributor / Agent": "Nhà phân phối / Đại lý",
    "OEM / Customization": "OEM / Tùy chỉnh",
    "Other": "Khác",
    "Laser Machine Power": "Công suất Máy Laser",
    "Select laser power...": "Chọn công suất laser...",
    "Other / Multiple": "Khác / Nhiều",
    "Laser Machine Brand": "Thương hiệu Máy Laser",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "vd. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "Tin nhắn *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "Mô tả nhu cầu cắt của bạn — loại vật liệu, độ dày, thiết lập khí hiện tại, v.v.",
    "Send Message →": "Gửi Tin nhắn →",
    "Or contact us directly via": "Hoặc liên hệ trực tiếp với chúng tôi qua",
    "Message Sent Successfully!": "Đã Gửi Tin nhắn Thành công!",
    "Thank you for your inquiry. We'll respond within 24 hours.":
     "Cảm ơn bạn đã yêu cầu. Chúng tôi sẽ phản hồi trong vòng 24 giờ.",
    "Back to Home": "Về Trang chủ",

    # Parameters page
    "Cutting Parameters": "Thông số Cắt",
    "Below are detailed cutting parameters for different laser powers. All tests performed on real customer machines.":
     "Dưới đây là thông số cắt chi tiết cho các công suất laser khác nhau. Tất cả các thử nghiệm được thực hiện trên máy thực tế của khách hàng.",
    "Thickness": "Độ dày",
    "Mixed Gas Speed": "Tốc độ Khí Hỗn hợp",
    "Speed Increase": "Tăng Tốc độ",
    "Test Location": "Địa điểm Thử nghiệm",
    "Notes": "Ghi chú",
    "Mixed Gas Optimization": "Tối ưu hóa Khí Hỗn hợp",
    "Gas Consumption Comparison": "So sánh Tiêu thụ Khí",
    "Pure Nitrogen": "Nitơ Tinh khiết",
    "Mixed Gas": "Khí Hỗn hợp",
    "Savings": "Tiết kiệm",
    "per hour": "mỗi giờ",
    "per day": "mỗi ngày",
    "per month": "mỗi tháng",
    "per year": "mỗi năm",
    "Download Parameters": "Tải Thông số",
    "Get Technical Support": "Nhận Hỗ trợ Kỹ thuật",
    "View Parameters": "Xem Thông số",

    # Contact page meta
    "Contact LISHI LASER for mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Liên hệ LISHI LASER để biết giá và báo giá thiết bị khí hỗn hợp. Tương thích với tất cả các thương hiệu laser lớn (HANS, DNE, PENTA, LEAD, HSG, BODOR). Vận chuyển toàn cầu.",
    "Contact LISHI LASER | Get Mixed Gas Device Quote":
     "Liên hệ LISHI LASER | Nhận Báo giá Thiết bị Khí Hỗn hợp",

    # Parameters page meta
    "Carbon steel cutting speed parameters: 12kW to 60kW. Compare mixed gas vs oxygen cutting speeds. Data from real end user tests.":
     "Thông số tốc độ cắt thép carbon: 12kW đến 60kW. So sánh tốc độ cắt khí hỗn hợp vs oxy. Dữ liệu từ thử nghiệm thực tế của người dùng.",
    "20kW laser cutting parameters for 8mm carbon steel. Mixed gas vs oxygen cutting speed data for 12kW to 60kW lasers. Industrial gas mixing optimization guide with real end user data.":
     "Thông số cắt laser 20kW cho thép carbon 8mm. Dữ liệu tốc độ cắt khí hỗn hợp vs oxy cho laser 12kW đến 60kW. Hướng dẫn tối ưu hóa trộn khí công nghiệp với dữ liệu thực tế.",
    "Laser Cutting Parameters by Power | Mixed Gas vs O2 Speed Data":
     "Thông số Cắt Laser theo Công suất | Dữ liệu Tốc độ Khí Hỗn hợp vs O2",
    "Laser Cutting Parameters | LISHI LASER Mixed Gas Device":
     "Thông số Cắt Laser | LISHI LASER Thiết bị Khí Hỗn hợp",
    "20kW Laser Cutting Parameters | Mixed Gas vs O2 Speed Data":
     "Thông số Cắt Laser 20kW | Dữ liệu Tốc độ Khí Hỗn hợp vs O2",
    "20kW Laser Cutting Parameters & Gas Speed Data":
     "Thông số Cắt Laser 20kW & Dữ liệu Tốc độ Khí",
    "Need detailed parameters for your specific laser machine and use case?":
     "Cần thông số chi tiết cho máy laser và ứng dụng cụ thể của bạn?",
    "Contact Us for Custom Parameters →": "Liên hệ để có Thông số Tùy chỉnh →",

    # Additional UI labels
    "Work Hours per Day": "Giờ Làm việc mỗi Ngày",
    "Actual Cutting Time (Beam-On %)": "Thời gian Cắt Thực tế (Bật Tia %)",
    "Competitive Edge": "Lợi thế Cạnh tranh",
    "Watch Video": "Xem Video",
    "Video demonstration of mixed gas device": "Video trình diễn thiết bị khí hỗn hợp",
    "Mixed gas device cutting carbon steel": "Thiết bị khí hỗn hợp cắt thép carbon",
    "Mixed Gas Device": "Thiết bị Khí Hỗn hợp",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER Thiết bị Khí Hỗn hợp"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER Liên hệ"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "Sản xuất Công nghiệp > Thiết bị Cắt Laser"',

    # FAQ content
    "What is a mixed gas device and how does it work?":
     "Thiết bị khí hỗn hợp là gì và hoạt động như thế nào?",
    "The mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen mixture is used as an auxiliary gas in high-power laser cutting, delivering 3× faster cutting speed compared to pure oxygen on carbon steel while completely eliminating burrs.":
     "Thiết bị khí hỗn hợp chuyển đổi nitơ lỏng (N₂) và oxy lỏng (O₂) thành hỗn hợp khí N₂/O₂ được hiệu chuẩn chính xác (thường là 95%/5%). Hỗn hợp vi oxy này được sử dụng làm khí phụ trợ trong cắt laser công suất cao, mang lại tốc độ cắt nhanh gấp 3× so với oxy tinh khiết trên thép carbon trong khi loại bỏ hoàn toàn ba via.",
    "Is it compatible with my laser machine?":
     "Nó có tương thích với máy laser của tôi không?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it's compatible.":
     "Có. Thiết bị Khí Hỗn hợp LISHI LASER hoạt động với tất cả các thương hiệu laser lớn bao gồm HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA và MESSER. Hỗ trợ máy từ 12kW đến 60kW. Nếu máy của bạn sử dụng kết nối khí phụ trợ tiêu chuẩn, nó tương thích.",
    "What thicknesses can it cut?": "Nó có thể cắt những độ dày nào?",
    "The mixed gas device can cut carbon steel, stainless steel and aluminum from 1mm to 30mm. Cutting thickness depends on your laser power. Detailed cutting parameter tables are available on our parameters page below.":
     "Thiết bị khí hỗn hợp có thể cắt thép carbon, thép không gỉ và nhôm từ 1mm đến 30mm. Độ dày cắt phụ thuộc vào công suất laser của bạn. Bảng thông số cắt chi tiết có sẵn trên trang thông số của chúng tôi.",
    "Mixed gas is primarily used for carbon steel cutting where it delivers the best speed and quality. It also works well for stainless steel and aluminum, though the speed advantage is less pronounced for non-ferrous metals.":
     "Khí hỗn hợp chủ yếu được sử dụng để cắt thép carbon, nơi nó mang lại tốc độ và chất lượng tốt nhất. Nó cũng hoạt động tốt cho thép không gỉ và nhôm, mặc dù lợi thế tốc độ ít rõ rệt hơn đối với kim loại màu.",
    "How much faster is mixed gas compared to pure oxygen cutting?":
     "Khí hỗn hợp nhanh hơn bao nhiêu so với cắt oxy tinh khiết?",
    "Mixed gas cutting is 2.5× to 7× faster than pure oxygen cutting depending on material thickness. For example: 6mm carbon steel — mixed gas 18m/min vs oxygen 3m/min (6× faster); 12mm carbon steel — mixed gas 8m/min vs oxygen 1.5m/min (5.3× faster).":
     "Cắt khí hỗn hợp nhanh gấp 2,5× đến 7× so với cắt oxy tinh khiết tùy thuộc vào độ dày vật liệu. Ví dụ: thép carbon 6mm — khí hỗn hợp 18m/phút vs oxy 3m/phút (nhanh gấp 6×); thép carbon 12mm — khí hỗn hợp 8m/phút vs oxy 1,5m/phút (nhanh gấp 5,3×).",
    "How much nitrogen can be saved by using mixed gas instead of pure N₂?":
     "Có thể tiết kiệm bao nhiêu nitơ khi sử dụng khí hỗn hợp thay vì N₂ tinh khiết?",
    "Mixed gas reduces nitrogen consumption by 33–50% compared to pure N₂ cutting. The small percentage of oxygen (5%) allows the oxidation reaction to contribute cutting energy, meaning you need less total gas flow for the same cut.":
     "Khí hỗn hợp giảm tiêu thụ nitơ 33–50% so với cắt N₂ tinh khiết. Tỷ lệ nhỏ oxy (5%) cho phép phản ứng oxy hóa đóng góp năng lượng cắt, có nghĩa là bạn cần ít lưu lượng khí tổng hơn cho cùng một đường cắt.",
    "Does mixed gas really eliminate burrs?": "Khí hỗn hợp có thực sự loại bỏ ba via không?",
    "Yes. The controlled micro-oxygen content in the nitrogen/oxygen mixture enables complete combustion without the excessive oxidation that occurs with pure oxygen or air cutting. Result: clean, burr-free edges requiring no additional sanding or grinding.":
     "Có. Hàm lượng vi oxy được kiểm soát trong hỗn hợp nitơ/oxy cho phép đốt cháy hoàn toàn mà không có oxy hóa quá mức xảy ra với cắt oxy tinh khiết hoặc không khí. Kết quả: các cạnh sạch, không ba via, không cần chà nhám hoặc mài thêm.",
    "Is it difficult to install and maintain?": "Có khó lắp đặt và bảo trì không?",
    "Installation is simple — a compact unit that connects to your existing laser machine. Maintenance is minimal: only 2kWh/24h power consumption and a basic annual check. No moving parts, so no wear or frequent service needed.":
     "Lắp đặt đơn giản — một thiết bị nhỏ gọn kết nối với máy laser hiện có của bạn. Bảo trì tối thiểu: chỉ tiêu thụ điện 2kWh/24h và kiểm tra cơ bản hàng năm. Không có bộ phận chuyển động, vì vậy không có hao mòn hoặc cần bảo dưỡng thường xuyên.",
    "Can one mixed gas device supply two laser machines simultaneously?":
     "Một thiết bị khí hỗn hợp có thể cung cấp cho hai máy laser đồng thời không?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station can simultaneously supply two laser cutting machines with independent flow control, effectively halving your equipment cost per machine.":
     "Có. LISHI LASER là nhà sản xuất duy nhất cung cấp cấu hình một-đến-hai ổn định. Một trạm trộn có thể đồng thời cung cấp cho hai máy cắt laser với điều khiển lưu lượng độc lập, giảm một nửa chi phí thiết bị cho mỗi máy.",
    "What are the input gas pressure requirements?": "Yêu cầu áp suất khí đầu vào là gì?",
    "The LISHI LASER Mixed Gas Device has an input pressure requirement of 20–25 bar from liquid N₂ and O₂ storage tanks, with an output pressure range of 15–30 bar adjustable for different laser machines and cutting applications.":
     "Thiết bị Khí Hỗn hợp LISHI LASER yêu cầu áp suất đầu vào 20–25 bar từ bể chứa N₂ và O₂ lỏng, với phạm vi áp suất đầu ra 15–30 bar có thể điều chỉnh cho các máy laser và ứng dụng cắt khác nhau.",
    "Is it guaranteed?": "Có bảo hành không?",
    "Yes, all LISHI LASER Mixed Gas Devices are covered by a 1-year warranty from the date of purchase. Extended warranty options are available through our global after-sales support network.":
     "Có, tất cả Thiết bị Khí Hỗn hợp LISHI LASER được bảo hành 1 năm kể từ ngày mua. Các tùy chọn bảo hành mở rộng có sẵn thông qua mạng lưới hỗ trợ hậu mãi toàn cầu của chúng tôi.",
    "What laser power levels are supported by the LISHI LASER Mixed Gas Device?":
     "Thiết bị Khí Hỗn hợp LISHI LASER hỗ trợ những mức công suất laser nào?",
    "The device supports laser machines from 12KW to 60KW. 12KW handles up to 16mm carbon steel, 20KW up to 25mm, 30KW up to 30mm. Contact us for parameters specific to your power level.":
     "Thiết bị hỗ trợ máy laser từ 12KW đến 60KW. 12KW xử lý thép carbon đến 16mm, 20KW đến 25mm, 30KW đến 30mm. Liên hệ với chúng tôi để biết thông số cụ thể cho mức công suất của bạn.",

    # Misc
    "in Laser Metal Cutting Industry": "trong Ngành Cắt Laser Kim loại",
    "Laser Machine": "Máy Laser",
    "micro-oxygen laser cutting technology": "công nghệ cắt laser vi oxy",
}

TH = {
    # Meta + OG
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "อุปกรณ์ก๊าซผสม LISHI LASER สำหรับเครื่องตัดเลเซอร์ 12KW-60KW ตัดเร็วขึ้น 3 เท่า ไร้ครีบ ใช้ก๊าซน้อยลง 33% เทคโนโลยีอัตราส่วน N2/O2 สำหรับการตัดเหล็กกล้าคาร์บอน",
    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER อุปกรณ์ก๊าซผสม | ตัดเลเซอร์เร็วขึ้น 3×",
    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "อุปกรณ์ก๊าซผสมสำหรับเครื่องตัดเลเซอร์ 12KW-60KW ตัดเร็วขึ้น 3× ไร้ครีบ ใช้ก๊าซน้อยลง 33% เทคโนโลยีอัตราส่วน N2/O2",
    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "เครื่องผสมก๊าซตัดเลเซอร์ อุปกรณ์ผสมไนโตรเจนออกซิเจน การตัดเลเซอร์ไมโครออกซิเจน ตัดเลเซอร์เหล็กกล้าคาร์บอน เลเซอร์กำลังสูง 12kW 60kW ก๊าซผสมเทียบกับเครื่องอัดอากาศ กำจัดครีบตัดเลเซอร์ ลดการใช้ไนโตรเจน เครื่องผสมก๊าซเลเซอร์ Han's อุปกรณ์ก๊าซเลเซอร์อุตสาหกรรม การตั้งค่าก๊าซหนึ่งต่อสอง การเพิ่มประสิทธิภาพก๊าซช่วย",
    "LISHI LASER Mixed Gas Device": "อุปกรณ์ก๊าซผสม LISHI LASER",

    # OG/Twitter contact
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "ราคาและใบเสนอราคาอุปกรณ์ก๊าซผสม LISHI LASER เข้ากันได้กับเครื่องเลเซอร์ทุกแบรนด์หลัก (HANS, DNE, PENTA, LEAD, HSG, BODOR) มีบริการจัดส่งทั่วโลก",

    "Mixed gas device for carbon steel laser cutting — 3× faster than oxygen, zero burrs, 33% nitrogen savings":
     "อุปกรณ์ก๊าซผสมสำหรับตัดเลเซอร์เหล็กกล้าคาร์บอน — เร็วกว่าออกซิเจน 3× ไร้ครีบ ประหยัดไนโตรเจน 33%",
    "Get LISHI LASER mixed gas cutting parameters and pricing. Compatible with HANS, DNE, PENTA, LEAD, HSG, BODOR. Global shipping.":
     "รับพารามิเตอร์การตัดและราคาก๊าซผสม LISHI LASER เข้ากันได้กับ HANS, DNE, PENTA, LEAD, HSG, BODOR จัดส่งทั่วโลก",
    "LISHI LASER Mixed Gas Device | Industrial Laser Cutting Gas Mixer":
     "LISHI LASER อุปกรณ์ก๊าซผสม | เครื่องผสมก๊าซตัดเลเซอร์อุตสาหกรรม",

    # Hero
    "Cut <span class=\"accent\">3× Faster</span><br>with Mixed Gas Technology":
     "ตัด<span class=\"accent\">เร็วขึ้น 3×</span><br>ด้วยเทคโนโลยีก๊าซผสม",
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "โซลูชันก๊าซผสม N₂/O₂ สำหรับเครื่องตัดเลเซอร์ 12KW-60KW",
    "3× Faster Than O₂": "เร็วกว่า O₂ 3×",
    "Zero Burrs": "ไร้ครีบ",
    "33% Less Nitrogen": "ใช้ไนโตรเจนน้อยลง 33%",

    # Nav
    "Home": "หน้าแรก",
    "Principle": "หลักการ",
    "Advantages": "ข้อดี",
    "Parameters": "พารามิเตอร์",
    "Samples": "ตัวอย่าง",
    "Clients": "ลูกค้า",
    "Contact": "ติดต่อ",
    "FAQ": "คำถามที่พบบ่อย",
    "Primary navigation": "การนำทางหลัก",

    # Principle
    "What is a Mixed Gas Device?": "อุปกรณ์ก๊าซผสมคืออะไร?",
    "The mixed gas device combines high-purity liquid nitrogen (N₂) and liquid oxygen (O₂) through precision IGBT-controlled mixing technology.":
     "อุปกรณ์ก๊าซผสมรวมไนโตรเจนเหลว (N₂) และออกซิเจนเหลว (O₂) ความบริสุทธิ์สูงผ่านเทคโนโลยีการผสมควบคุมด้วย IGBT แม่นยำ",
    "The result is an auxiliary gas that is 3 times faster than pure oxygen for carbon steel cutting, and far more economical than pure nitrogen.":
     "ผลลัพธ์คือก๊าซช่วยที่เร็วกว่าออกซิเจนบริสุทธิ์ 3 เท่าสำหรับการตัดเหล็กกล้าคาร์บอน และประหยัดกว่าไนโตรเจนบริสุทธิ์มาก",

    # Advantages
    "Why Choose Mixed Gas Over O₂, N₂ or Air?": "ทำไมต้องเลือกก๊าซผสมแทน O₂, N₂ หรืออากาศ?",
    "Eliminate burrs in carbon steel laser cutting while reducing nitrogen consumption by 33%. Our maintenance-free gas supply system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "กำจัดครีบในการตัดเลเซอร์เหล็กกล้าคาร์บอนพร้อมลดการใช้ไนโตรเจน 33% ระบบจ่ายก๊าซที่ไม่ต้องบำรุงรักษาของเราเข้ากันได้กับ HAN'S, DNE, PENTA, LEAD, HSG, BODOR และแบรนด์หลักอื่นๆ",

    "3× Faster Cutting": "ตัดเร็วขึ้น 3×",
    "Increase laser cutting speed up to 3 times compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "เพิ่มความเร็วตัดเลเซอร์สูงสุด 3 เท่าเมื่อเทียบกับการตัดด้วยออกซิเจน ตัวอย่าง: เหล็กกล้าคาร์บอน 8mm ที่ 16m/นาทีด้วยก๊าซผสม เพียง 2–3m/นาทีด้วย O₂",
    "Eliminate Burrs": "กำจัดครีบ",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cut edges requiring no additional sanding.":
     "สภาพแวดล้อมไมโครออกซิเจนที่ควบคุมได้ช่วยให้การเผาไหม้สมบูรณ์ ผลลัพธ์: ขอบตัดเรียบไร้ครีบ ไม่ต้องขัดเพิ่ม",
    "Lower Gas Costs": "ลดต้นทุนก๊าซ",
    "Optimized N₂/O₂ mixing ratio reduces nitrogen usage by approximately one third compared to pure nitrogen.":
     "อัตราส่วนผสม N₂/O₂ ที่เหมาะสมลดการใช้ไนโตรเจนประมาณหนึ่งในสามเมื่อเทียบกับไนโตรเจนบริสุทธิ์",
    "Maintenance-Free": "ไม่ต้องบำรุงรักษา",
    "Power consumption: only 2 kWh in 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "การใช้พลังงาน: เพียง 2 kWh ใน 24 ชั่วโมง ต่างจากเครื่องอัดอากาศที่ต้องเปลี่ยนกรอง/น้ำมันทุก 3,000 ชั่วโมง อุปกรณ์ก๊าซเลเซอร์อุตสาหกรรมของเราไม่ต้องบำรุงรักษา",
    "One-to-Two Laser Setup": "การตั้งค่าหนึ่งต่อสอง",
    "A single mixed gas device can simultaneously supply two laser cutting machines, cutting equipment costs in half.":
     "อุปกรณ์ก๊าซผสมหนึ่งเครื่องสามารถจ่ายให้เครื่องตัดเลเซอร์สองเครื่องพร้อมกัน ลดต้นทุนอุปกรณ์ลงครึ่งหนึ่ง",
    "Lens Protection": "การปกป้องเลนส์",
    "Unlike air compressors that introduce oil vapor and particulates, our closed-loop gas system delivers clean, dry gas that protects your laser optics.":
     "ต่างจากเครื่องอัดอากาศที่นำไอน้ำมันและอนุภาคเข้ามา ระบบก๊าซวงปิดของเราส่งก๊าซสะอาดและแห้งที่ปกป้องเลนส์เลเซอร์ของคุณ",
    "Wide Compatibility": "ความเข้ากันได้กว้าง",
    "Compatible with all major laser brands: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. Supports from 12kW to 60kW.":
     "เข้ากันได้กับเครื่องเลเซอร์ทุกแบรนด์หลัก: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA และ MESSER รองรับตั้งแต่ 12kW ถึง 60kW",

    # Comparison table
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air":
     "การเปรียบเทียบประสิทธิภาพ: ก๊าซผสม vs O₂ vs N₂ vs อากาศ",
    "Pure Oxygen (O₂)": "ออกซิเจนบริสุทธิ์ (O₂)",
    "Pure Nitrogen (N₂)": "ไนโตรเจนบริสุทธิ์ (N₂)",
    "Air (Compressor)": "อากาศ (เครื่องอัด)",
    "Mixed Gas (N₂/O₂)": "ก๊าซผสม (N₂/O₂)",
    "Burred edges": "ขอบมีครีบ",
    "Perfectly smooth": "เรียบสมบูรณ์แบบ",
    "Low quality": "คุณภาพต่ำ",
    "Very high": "สูงมาก",
    "Low (~33% savings)": "ต่ำ (ประหยัด ~33%)",
    "Frequent cleaning required": "ต้องทำความสะอาดบ่อย",
    "Minimal": "น้อยที่สุด",
    "Compressor maintenance": "บำรุงรักษาเครื่องอัด",

    # ROI
    "Calculate Your Laser Cutting Gas Cost Savings": "คำนวณการประหยัดต้นทุนก๊าซตัดเลเซอร์ของคุณ",
    "Machine Power": "กำลังเครื่อง",
    "Material Thickness": "ความหนาวัสดุ",
    "Daily Work Hours": "ชั่วโมงทำงานต่อวัน",
    "Gas Cost (/m³)": "ต้นทุนก๊าซ (/m³)",
    "Calculate": "คำนวณ",
    "Estimated Annual Savings": "ประมาณการประหยัดต่อปี",
    "Investment Payback Period": "ระยะเวลาคืนทุน",
    "months": "เดือน",
    "Estimated Annual Profit Increase (USD)": "ประมาณการกำไรเพิ่มต่อปี (USD)",
    "Get Free Parameters →": "รับพารามิเตอร์ฟรี →",
    "ROI Calculator": "เครื่องคำนวณ ROI",
    "Calculator": "เครื่องคำนวณ",

    # Air vs Mixed
    "Air Seems Free. The Reality Is Not.": "อากาศดูเหมือนฟรี ความจริงไม่ใช่",
    "Why Air Costs More": "ทำไมอากาศถึงแพงกว่า",
    "High Maintenance Cost": "ค่าบำรุงรักษาสูง",
    "Air compressor systems require regular filter changes, oil changes, and dryer maintenance. Annual maintenance costs typically range from $2,000 to $5,000.":
     "ระบบเครื่องอัดอากาศต้องเปลี่ยนกรอง เปลี่ยนน้ำมัน และบำรุงรักษาเครื่องเป่าเป็นประจำ ค่าบำรุงรักษารายปีมักอยู่ระหว่าง $2,000 ถึง $5,000",
    "Poor Cut Quality": "คุณภาพการตัดต่ำ",
    "Air cutting cannot control oxidation, resulting in burrs and discoloration on cut edges.":
     "การตัดด้วยอากาศไม่สามารถควบคุมออกซิเดชัน ทำให้เกิดครีบและการเปลี่ยนสีบนขอบตัด",
    "Lens Contamination": "การปนเปื้อนเลนส์",
    "Oil vapor and particulates from the compressor contaminate laser optics, reducing lens life.":
     "ไอน้ำมันและอนุภาคจากเครื่องอัดทำให้เลนส์เลเซอร์ปนเปื้อน ลดอายุการใช้งานเลนส์",
    "Energy Consumption": "การใช้พลังงาน",
    "Air compressors typically consume 15–30kW per hour. The mixed gas device consumes only 2kWh/24h.":
     "เครื่องอัดอากาศมักใช้ 15–30kW ต่อชั่วโมง อุปกรณ์ก๊าซผสมใช้เพียง 2kWh/24h",
    "Noise": "เสียงรบกวน",
    "Air compressors produce 75–85dB of noise. The mixed gas device operates silently.":
     "เครื่องอัดอากาศผลิตเสียง 75–85dB อุปกรณ์ก๊าซผสมทำงานเงียบ",

    # Parameters section
    "Cutting Parameters by Power": "พารามิเตอร์การตัดตามกำลัง",
    "View All Parameters →": "ดูพารามิเตอร์ทั้งหมด →",
    "Detailed Parameters →": "พารามิเตอร์โดยละเอียด →",

    # Samples
    "Cutting Samples and Test Videos": "ตัวอย่างการตัดและวิดีโอทดสอบ",
    "Real customer cutting results, tested across different materials and power levels.":
     "ผลลัพธ์การตัดจริงของลูกค้า ทดสอบกับวัสดุและระดับกำลังต่างๆ",
    "Watch Video": "ดูวิดีโอ",
    "Cutting Video": "วิดีโอการตัด",
    "Before / After": "ก่อน / หลัง",

    # Global
    "GLOBAL NETWORK": "เครือข่ายทั่วโลก",
    "50+ Countries": "50+ ประเทศ",
    "500+ Systems Installed": "500+ ระบบที่ติดตั้ง",
    "30+ Distributors": "30+ ผู้จัดจำหน่าย",
    "Global After-Sales Support": "สนับสนุนหลังการขายทั่วโลก",
    "Asia": "เอเชีย",
    "Europe": "ยุโรป",
    "Americas": "อเมริกา",
    "Africa": "แอฟริกา",
    "Oceania": "โอเชียเนีย",

    # FAQ
    "Frequently Asked Questions": "คำถามที่พบบ่อย",

    # CTA
    "Ready to Increase Your Cutting Speed?": "พร้อมเพิ่มความเร็วในการตัดหรือยัง?",
    "Contact us now for a customized solution and pricing.":
     "ติดต่อเราตอนนี้เพื่อโซลูชันและราคาที่กำหนดเอง",
    "Contact Us Now": "ติดต่อเราเลย",
    "Get Free Consultation": "รับคำปรึกษาฟรี",
    "Get a Quote": "ขอใบเสนอราคา",
    "How It Works →": "วิธีการทำงาน →",

    # Footer
    "Brand Licensed Overseas Market Operation Agent:":
     "ตัวแทนดำเนินการตลาดต่างประเทศที่ได้รับอนุญาต:",
    "All rights reserved.": "สงวนลิขสิทธิ์ทั้งหมด",
    "Gas Mixing Technology": "เทคโนโลยีการผสมก๊าซ",
    "Product": "ผลิตภัณฑ์",
    "How It Works": "วิธีการทำงาน",
    "Cutting Samples": "ตัวอย่างการตัด",

    # Contact page
    "Get In Touch": "ติดต่อเรา",
    "Contact Us": "ติดต่อเรา",
    "Ready to increase your cutting speed? Send us your laser machine details and we'll provide customized parameters and pricing.":
     "พร้อมเพิ่มความเร็วในการตัด? ส่งรายละเอียดเครื่องเลเซอร์ของคุณมา แล้วเราจะให้พารามิเตอร์และราคาที่กำหนดเอง",
    "Email": "อีเมล",
    "Response within 24 hours": "ตอบกลับภายใน 24 ชั่วโมง",
    "Phone / WeChat": "โทรศัพท์ / WeChat",
    "WeChat: same number": "WeChat: เบอร์เดียวกัน",
    "WhatsApp": "WhatsApp",
    "Company": "บริษัท",
    "Product Brand": "แบรนด์ผลิตภัณฑ์",
    "Mixed Gas Device — 13 Years in Laser Cutting Industry": "อุปกรณ์ก๊าซผสม — 13 ปีในอุตสาหกรรมตัดเลเซอร์",
    "Looking for a Distributor?": "กำลังมองหาผู้จัดจำหน่าย?",
    "We're actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "เรากำลังขยายเครือข่ายตัวแทนทั่วโลกอย่างแข็งขัน มีเขตพื้นที่พิเศษสำหรับผู้จัดจำหน่ายที่มีคุณสมบัติ",
    "Apply for Agency →": "สมัครเป็นตัวแทน →",
    "Send Us a Message": "ส่งข้อความถึงเรา",
    "Full Name *": "ชื่อ-นามสกุล *",
    "John Smith": "สมชาย ใจดี",
    "ABC Laser Ltd.": "บริษัท เอบีซี เลเซอร์ จำกัด",
    "john@company.com": "somchai@company.co.th",
    "Phone / WhatsApp": "โทรศัพท์ / WhatsApp",
    "+1 234 567 8900": "+66 99 123 4567",
    "Country": "ประเทศ",
    "e.g. Mexico, Thailand, India": "เช่น ไทย, เวียดนาม, อินเดีย",
    "Inquiry Type": "ประเภทคำถาม",
    "Select one...": "เลือก...",
    "Pricing & Quote": "ราคาและใบเสนอราคา",
    "Technical Parameters": "พารามิเตอร์ทางเทคนิค",
    "Distributor / Agent": "ผู้จัดจำหน่าย / ตัวแทน",
    "OEM / Customization": "OEM / กำหนดเอง",
    "Other": "อื่นๆ",
    "Laser Machine Power": "กำลังเครื่องเลเซอร์",
    "Select laser power...": "เลือกกำลังเลเซอร์...",
    "Other / Multiple": "อื่นๆ / หลายค่า",
    "Laser Machine Brand": "แบรนด์เครื่องเลเซอร์",
    "e.g. HAN'S, DNE, PENTA, LEAD, BODOR": "เช่น HAN'S, DNE, PENTA, LEAD, BODOR",
    "Message *": "ข้อความ *",
    "Describe your cutting needs — material type, thickness, current gas setup, etc.":
     "อธิบายความต้องการตัดของคุณ — ประเภทวัสดุ ความหนา การตั้งค่าก๊าซปัจจุบัน ฯลฯ",
    "Send Message →": "ส่งข้อความ →",
    "Or contact us directly via": "หรือติดต่อเราโดยตรงผ่าน",
    "Message Sent Successfully!": "ส่งข้อความสำเร็จ!",
    "Thank you for your inquiry. We'll respond within 24 hours.":
     "ขอบคุณสำหรับคำถามของคุณ เราจะตอบกลับภายใน 24 ชั่วโมง",
    "Back to Home": "กลับหน้าแรก",

    # Parameters page
    "Cutting Parameters": "พารามิเตอร์การตัด",
    "Below are detailed cutting parameters for different laser powers. All tests performed on real customer machines.":
     "ด้านล่างนี้คือพารามิเตอร์การตัดโดยละเอียดสำหรับกำลังเลเซอร์ต่างๆ การทดสอบทั้งหมดทำบนเครื่องจริงของลูกค้า",
    "Thickness": "ความหนา",
    "Mixed Gas Speed": "ความเร็วก๊าซผสม",
    "Speed Increase": "เพิ่มความเร็ว",
    "Test Location": "สถานที่ทดสอบ",
    "Notes": "หมายเหตุ",
    "Mixed Gas Optimization": "การเพิ่มประสิทธิภาพก๊าซผสม",
    "Gas Consumption Comparison": "การเปรียบเทียบการใช้ก๊าซ",
    "Pure Nitrogen": "ไนโตรเจนบริสุทธิ์",
    "Mixed Gas": "ก๊าซผสม",
    "Savings": "ประหยัด",
    "per hour": "ต่อชั่วโมง",
    "per day": "ต่อวัน",
    "per month": "ต่อเดือน",
    "per year": "ต่อปี",
    "Download Parameters": "ดาวน์โหลดพารามิเตอร์",
    "Get Technical Support": "รับการสนับสนุนทางเทคนิค",
    "View Parameters": "ดูพารามิเตอร์",

    # Contact page meta
    "Contact LISHI LASER for mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "ติดต่อ LISHI LASER สำหรับราคาและใบเสนอราคาอุปกรณ์ก๊าซผสม เข้ากันได้กับเครื่องเลเซอร์ทุกแบรนด์หลัก (HANS, DNE, PENTA, LEAD, HSG, BODOR) มีบริการจัดส่งทั่วโลก",
    "Contact LISHI LASER | Get Mixed Gas Device Quote":
     "ติดต่อ LISHI LASER | ขอใบเสนอราคาอุปกรณ์ก๊าซผสม",

    # Parameters page meta
    "Carbon steel cutting speed parameters: 12kW to 60kW. Compare mixed gas vs oxygen cutting speeds. Data from real end user tests.":
     "พารามิเตอร์ความเร็วตัดเหล็กกล้าคาร์บอน: 12kW ถึง 60kW เปรียบเทียบความเร็วตัดก๊าซผสมกับออกซิเจน ข้อมูลจากการทดสอบผู้ใช้จริง",
    "20kW laser cutting parameters for 8mm carbon steel. Mixed gas vs oxygen cutting speed data for 12kW to 60kW lasers. Industrial gas mixing optimization guide with real end user data.":
     "พารามิเตอร์ตัดเลเซอร์ 20kW สำหรับเหล็กกล้าคาร์บอน 8mm ข้อมูลความเร็วตัดก๊าซผสมกับออกซิเจนสำหรับเลเซอร์ 12kW ถึง 60kW คู่มือการเพิ่มประสิทธิภาพการผสมก๊าซอุตสาหกรรมด้วยข้อมูลผู้ใช้จริง",
    "Laser Cutting Parameters by Power | Mixed Gas vs O2 Speed Data":
     "พารามิเตอร์ตัดเลเซอร์ตามกำลัง | ข้อมูลความเร็วก๊าซผสม vs O2",
    "Laser Cutting Parameters | LISHI LASER Mixed Gas Device":
     "พารามิเตอร์ตัดเลเซอร์ | LISHI LASER อุปกรณ์ก๊าซผสม",
    "20kW Laser Cutting Parameters | Mixed Gas vs O2 Speed Data":
     "พารามิเตอร์ตัดเลเซอร์ 20kW | ข้อมูลความเร็วก๊าซผสม vs O2",
    "20kW Laser Cutting Parameters & Gas Speed Data":
     "พารามิเตอร์ตัดเลเซอร์ 20kW และข้อมูลความเร็วก๊าซ",
    "Need detailed parameters for your specific laser machine and use case?":
     "ต้องการพารามิเตอร์โดยละเอียดสำหรับเครื่องเลเซอร์และการใช้งานเฉพาะของคุณ?",
    "Contact Us for Custom Parameters →": "ติดต่อเราเพื่อพารามิเตอร์ที่กำหนดเอง →",

    # Additional UI labels
    "Work Hours per Day": "ชั่วโมงทำงานต่อวัน",
    "Actual Cutting Time (Beam-On %)": "เวลาตัดจริง (เปิดลำแสง %)",
    "Competitive Edge": "ความได้เปรียบในการแข่งขัน",
    "Watch Video": "ดูวิดีโอ",
    "Video demonstration of mixed gas device": "วิดีโอสาธิตอุปกรณ์ก๊าซผสม",
    "Mixed gas device cutting carbon steel": "อุปกรณ์ก๊าซผสมตัดเหล็กกล้าคาร์บอน",
    "Mixed Gas Device": "อุปกรณ์ก๊าซผสม",

    # JSON-LD names
    '"name": "LISHI LASER Mixed Gas Device"': '"name": "LISHI LASER อุปกรณ์ก๊าซผสม"',
    '"name": "LISHI LASER Contact"': '"name": "LISHI LASER ติดต่อ"',
    '"category": "Industrial Manufacturing > Laser Cutting Equipment"': '"category": "การผลิตอุตสาหกรรม > อุปกรณ์ตัดเลเซอร์"',

    # FAQ content
    "What is a mixed gas device and how does it work?":
     "อุปกรณ์ก๊าซผสมคืออะไรและทำงานอย่างไร?",
    "The mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen mixture is used as an auxiliary gas in high-power laser cutting, delivering 3× faster cutting speed compared to pure oxygen on carbon steel while completely eliminating burrs.":
     "อุปกรณ์ก๊าซผสมแปลงไนโตรเจนเหลว (N₂) และออกซิเจนเหลว (O₂) เป็นส่วนผสมก๊าซ N₂/O₂ ที่ปรับเทียบอย่างแม่นยำ (ปกติ 95%/5%) ส่วนผสมไมโครออกซิเจนนี้ใช้เป็นก๊าซช่วยในการตัดเลเซอร์กำลังสูง ให้ความเร็วตัดเร็วกว่า 3× เมื่อเทียบกับออกซิเจนบริสุทธิ์บนเหล็กกล้าคาร์บอน พร้อมกำจัดครีบอย่างสมบูรณ์",
    "Is it compatible with my laser machine?":
     "เข้ากันได้กับเครื่องเลเซอร์ของฉันหรือไม่?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it's compatible.":
     "ใช่ อุปกรณ์ก๊าซผสม LISHI LASER ทำงานกับเครื่องเลเซอร์ทุกแบรนด์หลัก รวมถึง HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA และ MESSER รองรับเครื่องตั้งแต่ 12kW ถึง 60kW หากเครื่องของคุณใช้การเชื่อมต่อก๊าซช่วยมาตรฐาน ก็เข้ากันได้",
    "What thicknesses can it cut?": "ตัดความหนาได้เท่าไหร่?",
    "The mixed gas device can cut carbon steel, stainless steel and aluminum from 1mm to 30mm. Cutting thickness depends on your laser power. Detailed cutting parameter tables are available on our parameters page below.":
     "อุปกรณ์ก๊าซผสมสามารถตัดเหล็กกล้าคาร์บอน สแตนเลส และอลูมิเนียมได้ตั้งแต่ 1mm ถึง 30mm ความหนาในการตัดขึ้นอยู่กับกำลังเลเซอร์ของคุณ ตารางพารามิเตอร์การตัดโดยละเอียดมีอยู่ในหน้าพารามิเตอร์ของเรา",
    "Mixed gas is primarily used for carbon steel cutting where it delivers the best speed and quality. It also works well for stainless steel and aluminum, though the speed advantage is less pronounced for non-ferrous metals.":
     "ก๊าซผสมใช้เป็นหลักสำหรับการตัดเหล็กกล้าคาร์บอนซึ่งให้ความเร็วและคุณภาพที่ดีที่สุด นอกจากนี้ยังทำงานได้ดีกับสแตนเลสและอลูมิเนียม แม้ว่าข้อได้เปรียบด้านความเร็วจะน้อยกว่าสำหรับโลหะที่ไม่ใช่เหล็ก",
    "How much faster is mixed gas compared to pure oxygen cutting?":
     "ก๊าซผสมเร็วกว่าการตัดด้วยออกซิเจนบริสุทธิ์เท่าไหร่?",
    "Mixed gas cutting is 2.5× to 7× faster than pure oxygen cutting depending on material thickness. For example: 6mm carbon steel — mixed gas 18m/min vs oxygen 3m/min (6× faster); 12mm carbon steel — mixed gas 8m/min vs oxygen 1.5m/min (5.3× faster).":
     "การตัดด้วยก๊าซผสมเร็วขึ้น 2.5× ถึง 7× เมื่อเทียบกับการตัดด้วยออกซิเจนบริสุทธิ์ ขึ้นอยู่กับความหนาของวัสดุ ตัวอย่าง: เหล็กกล้าคาร์บอน 6mm — ก๊าซผสม 18m/นาที vs ออกซิเจน 3m/นาที (เร็วขึ้น 6×); เหล็กกล้าคาร์บอน 12mm — ก๊าซผสม 8m/นาที vs ออกซิเจน 1.5m/นาที (เร็วขึ้น 5.3×)",
    "How much nitrogen can be saved by using mixed gas instead of pure N₂?":
     "ประหยัดไนโตรเจนได้เท่าไหร่เมื่อใช้ก๊าซผสมแทน N₂ บริสุทธิ์?",
    "Mixed gas reduces nitrogen consumption by 33–50% compared to pure N₂ cutting. The small percentage of oxygen (5%) allows the oxidation reaction to contribute cutting energy, meaning you need less total gas flow for the same cut.":
     "ก๊าซผสมลดการใช้ไนโตรเจน 33–50% เมื่อเทียบกับการตัดด้วย N₂ บริสุทธิ์ ออกซิเจนเปอร์เซ็นต์เล็กน้อย (5%) ช่วยให้ปฏิกิริยาออกซิเดชันมีส่วนช่วยพลังงานตัด หมายความว่าคุณต้องการการไหลของก๊าซรวมน้อยลงสำหรับการตัดเดียวกัน",
    "Does mixed gas really eliminate burrs?": "ก๊าซผสมกำจัดครีบได้จริงหรือ?",
    "Yes. The controlled micro-oxygen content in the nitrogen/oxygen mixture enables complete combustion without the excessive oxidation that occurs with pure oxygen or air cutting. Result: clean, burr-free edges requiring no additional sanding or grinding.":
     "ใช่ ปริมาณไมโครออกซิเจนที่ควบคุมได้ในส่วนผสมไนโตรเจน/ออกซิเจนช่วยให้การเผาไหม้สมบูรณ์โดยไม่มีออกซิเดชันมากเกินไปที่เกิดกับการตัดด้วยออกซิเจนบริสุทธิ์หรืออากาศ ผลลัพธ์: ขอบสะอาดไร้ครีบ ไม่ต้องขัดหรือเจียรเพิ่ม",
    "Is it difficult to install and maintain?": "ติดตั้งและบำรุงรักษายากหรือไม่?",
    "Installation is simple — a compact unit that connects to your existing laser machine. Maintenance is minimal: only 2kWh/24h power consumption and a basic annual check. No moving parts, so no wear or frequent service needed.":
     "การติดตั้งง่าย — หน่วยขนาดกะทัดรัดที่เชื่อมต่อกับเครื่องเลเซอร์ที่มีอยู่ของคุณ การบำรุงรักษาน้อยที่สุด: ใช้พลังงานเพียง 2kWh/24h และตรวจสอบพื้นฐานประจำปี ไม่มีชิ้นส่วนเคลื่อนไหว จึงไม่มีการสึกหรอหรือต้องบริการบ่อย",
    "Can one mixed gas device supply two laser machines simultaneously?":
     "อุปกรณ์ก๊าซผสมหนึ่งเครื่องสามารถจ่ายให้เครื่องเลเซอร์สองเครื่องพร้อมกันได้หรือไม่?",
    "Yes. LISHI LASER is the only manufacturer offering a stable one-to-two configuration. One mixing station can simultaneously supply two laser cutting machines with independent flow control, effectively halving your equipment cost per machine.":
     "ใช่ LISHI LASER เป็นผู้ผลิตรายเดียวที่เสนอการกำหนดค่าหนึ่งต่อสองที่เสถียร สถานีผสมหนึ่งแห่งสามารถจ่ายให้เครื่องตัดเลเซอร์สองเครื่องพร้อมกันด้วยการควบคุมการไหลอิสระ ลดต้นทุนอุปกรณ์ต่อเครื่องลงครึ่งหนึ่งอย่างมีประสิทธิภาพ",
    "What are the input gas pressure requirements?": "ข้อกำหนดแรงดันก๊าซขาเข้าคืออะไร?",
    "The LISHI LASER Mixed Gas Device has an input pressure requirement of 20–25 bar from liquid N₂ and O₂ storage tanks, with an output pressure range of 15–30 bar adjustable for different laser machines and cutting applications.":
     "อุปกรณ์ก๊าซผสม LISHI LASER มีข้อกำหนดแรงดันขาเข้า 20–25 bar จากถังเก็บ N₂ และ O₂ เหลว โดยมีช่วงแรงดันขาออก 15–30 bar ปรับได้สำหรับเครื่องเลเซอร์และการใช้งานตัดต่างๆ",
    "Is it guaranteed?": "มีการรับประกันหรือไม่?",
    "Yes, all LISHI LASER Mixed Gas Devices are covered by a 1-year warranty from the date of purchase. Extended warranty options are available through our global after-sales support network.":
     "ใช่ อุปกรณ์ก๊าซผสม LISHI LASER ทั้งหมดรับประกัน 1 ปีนับจากวันที่ซื้อ มีตัวเลือกการรับประกันเพิ่มเติมผ่านเครือข่ายสนับสนุนหลังการขายทั่วโลกของเรา",
    "What laser power levels are supported by the LISHI LASER Mixed Gas Device?":
     "อุปกรณ์ก๊าซผสม LISHI LASER รองรับกำลังเลเซอร์ระดับใดบ้าง?",
    "The device supports laser machines from 12KW to 60KW. 12KW handles up to 16mm carbon steel, 20KW up to 25mm, 30KW up to 30mm. Contact us for parameters specific to your power level.":
     "อุปกรณ์รองรับเครื่องเลเซอร์ตั้งแต่ 12KW ถึง 60KW 12KW ตัดเหล็กกล้าคาร์บอนได้ถึง 16mm, 20KW ถึง 25mm, 30KW ถึง 30mm ติดต่อเราเพื่อขอพารามิเตอร์เฉพาะสำหรับระดับกำลังของคุณ",

    # Misc
    "in Laser Metal Cutting Industry": "ในอุตสาหกรรมตัดโลหะด้วยเลเซอร์",
    "Laser Machine": "เครื่องเลเซอร์",
    "micro-oxygen laser cutting technology": "เทคโนโลยีตัดเลเซอร์ไมโครออกซิเจน",
}


# ================================================================
# Build process
# ================================================================
def build_language(lang, translations):
    print(f"\n=== Building {lang} ===")
    for page in ['index', 'contact', 'parameters']:
        filename = f'{page}.html'
        src = os.path.join(BASE, filename)
        dst = os.path.join(BASE, lang, filename)

        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()

        # Step 1: Structural changes
        content = apply_structural(content, lang, page)

        # Step 2: Translate content
        content = translate(content, translations)

        with open(dst, 'w', encoding='utf-8') as f:
            f.write(content)

        # Verify
        hreflangs = content.count('hreflang')
        options = content.count('lang-option')
        print(f"  {filename}: {hreflangs} hreflangs, {options} lang-options")

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    trans_map = {'it': IT, 'de': DE, 'fr': FR, 'nl': NL, 'ru': RU, 'vi': VI, 'th': TH}
    if lang in trans_map:
        build_language(lang, trans_map[lang])
    else:
        print(f"No translations for {lang}")

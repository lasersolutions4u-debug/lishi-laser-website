#!/usr/bin/env python3
"""Translate from English to IT/DE/FR/NL for all 3 page types."""
import os, sys

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

# ============================================================
# ITALIAN TRANSLATIONS (English → Italian)
# ============================================================
IT = {
    # Meta
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "Dispositivo a gas misto LISHI LASER per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di gas in meno. Tecnologia a rapporto N2/O2 per taglio acciaio al carbonio.",

    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "miscelatore gas taglio laser, dispositivo miscelazione azoto ossigeno, taglio laser micro ossigeno, taglio laser acciaio carbonio, laser alta potenza 12kW 60kW, gas misto vs compressore aria, eliminazione bave taglio laser, riduzione consumo azoto, miscelatore gas laser Han's, apparecchiatura gas laser industriale, configurazione gas uno-a-due, ottimizzazione gas assistito",

    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Dispositivo a Gas Misto | Taglio Laser 3× Più Veloce",

    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Dispositivo a gas misto per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di gas in meno. Tecnologia a rapporto N2/O2.",

    # Nav
    "Skip to content": "Vai al contenuto",
    "Home": "Home",
    "How It Works": "Come Funziona",
    "Advantages": "Vantaggi",
    "Parameters": "Parametri",
    "Samples": "Campioni",
    "Customers": "Clienti",
    "Blog": "Blog",
    "Contact": "Contatto",
    "Menu toggle": "Menu",

    # Logo
    "Gas Mixing Technology": "Tecnologia Miscelazione Gas",

    # Hero
    "Cut <span class=\"accent\">3× Faster</span><br>with Mixed Gas Technology":
     "Taglia <span class=\"accent\">3× Più Veloce</span><br>con la Tecnologia a Gas Misto",
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

    # ROI Calculator
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

    # FAQ (index page)
    "Frequently Asked Questions": "Domande Frequenti",
    "What is a mixed gas device and how does it work?": "Cos'è un dispositivo a gas misto e come funziona?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Un dispositivo a gas misto converte azoto liquido (N₂) e ossigeno liquido (O₂) in una miscela di gas N₂/O₂ precisamente calibrata (tipicamente 95%/5%). Questa miscela micro-ossigeno viene utilizzata come gas ausiliario nel taglio laser ad alta potenza, offrendo velocità di taglio 3× superiori sull'acciaio al carbonio rispetto all'ossigeno puro, eliminando completamente le bave.",
    "Is it compatible with my laser machine?": "È compatibile con la mia macchina laser?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Sì. Il Dispositivo a Gas Misto LISHI LASER funziona con tutti i principali marchi laser, inclusi HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA e MESSER. Supporta macchine da 12kW a 60kW. Se la tua macchina utilizza connessioni standard per gas ausiliario, è compatibile.",
    "What thicknesses can it cut?": "Quali spessori può tagliare?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "La gamma di taglio dipende dalla potenza del laser: 12kW gestisce fino a 16mm, 20kW fino a 25mm, 30kW fino a 30mm e 60kW fino a 40mm di acciaio al carbonio. Taglia anche acciaio inossidabile e alluminio. Tabelle dettagliate dei parametri di taglio sono disponibili nella nostra pagina parametri qui sotto.",
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
    "How It Works": "Come Funziona",
    "Cutting Samples": "Campioni di Taglio",

    # ========================
    # CONTACT PAGE
    # ========================
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "Prezzi e preventivi dispositivo a gas misto LISHI LASER. Compatibile con tutti i principali marchi laser (HANS, DNE, PENTA, LEAD, HSG, BODOR). Spedizione globale disponibile.",
    "laser cutting gas equipment quote, mixed gas device distributor, laser cutting equipment manufacturer, HANS laser compatible gas":
     "preventivo apparecchiatura gas taglio laser, distributore dispositivo gas misto, produttore apparecchiatura taglio laser, gas compatibile laser HANS",
    "LISHI LASER Contact | Get Mixed Gas Device Quote": "LISHI LASER Contatto | Richiedi Preventivo Dispositivo Gas Misto",
    "Request a quote for LISHI LASER mixed gas cutting equipment. Compatible with all major laser brands. Global shipping available.":
     "Richiedi un preventivo per apparecchiatura da taglio a gas misto LISHI LASER. Compatibile con tutti i principali marchi laser. Spedizione globale disponibile.",
    "LISHI LASER Contact": "LISHI LASER Contatto",
    "Get in Touch": "Contattaci",
    "Contact Us": "Contattaci",
    "Ready to boost your cutting speed? Send your laser machine details and we'll provide custom parameters and pricing.":
     "Pronto ad aumentare la tua velocità di taglio? Invia i dettagli della tua macchina laser e ti forniremo parametri e prezzi personalizzati.",
    "Email": "Email",
    "Reply within 24 hours": "Risposta entro 24 ore",
    "Phone / WeChat": "Telefono / WeChat",
    "WeChat: same number": "WeChat: stesso numero",
    "(Mexico)": "(Messico)",
    "(Thailand)": "(Thailandia)",
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
    "Phone / WhatsApp": "Telefono / WhatsApp",
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

    # ========================
    # PARAMETERS PAGE
    # ========================
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

    # Additional FAQ (parameters page)
    "How do I read the cutting parameters table?": "Come leggere la tabella dei parametri di taglio?",
    "The table shows cutting speed in meters per minute (m/min), mixed gas pressure in bar, and nozzle diameter in mm. Higher speeds mean better productivity. The speed improvement percentage shows the gain versus pure oxygen cutting.":
     "La tabella mostra la velocità di taglio in metri al minuto (m/min), la pressione del gas misto in bar e il diametro dell'ugello in mm. Velocità più alte significano migliore produttività. La percentuale di miglioramento velocità mostra il guadagno rispetto al taglio a ossigeno puro.",
    "Why does speed improvement decrease at very thick materials?": "Perché il miglioramento della velocità diminuisce su materiali molto spessi?",
    "At extreme thicknesses (30mm+), the limiting factor shifts from gas chemistry to laser power penetration. The mixed gas still provides benefits in edge quality and eliminates burrs, but the raw speed difference versus oxygen narrows because both processes are dominated by the laser beam's physical ability to penetrate the material.":
     "A spessori estremi (30mm+), il fattore limitante passa dalla chimica del gas alla potenza di penetrazione del laser. Il gas misto offre comunque benefici in qualità del bordo ed elimina le bave, ma la differenza di velocità rispetto all'ossigeno si riduce perché entrambi i processi sono dominati dalla capacità fisica del raggio laser di penetrare il materiale.",
}

# ============================================================
# GERMAN TRANSLATIONS
# ============================================================
DE = {
    "LISHI LASER Mixed Gas Device for 12KW-60KW laser cutting machines. 3x faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology for carbon steel cutting.":
     "LISHI LASER Mischgasgerät für 12KW-60KW Laserschneidmaschinen. 3× schnellere Schneidgeschwindigkeit, keine Grate, 33% weniger Gasverbrauch. N2/O2-Verhältnis-Technologie für Kohlenstoffstahl-Schneiden.",

    "laser cutting gas mixer, nitrogen oxygen mixing device, micro oxygen laser cutting, carbon steel laser cutting, high power laser 12kW 60kW, mixed gas vs air compressor, eliminate laser cutting burrs, reduce nitrogen consumption, Han's laser gas mixer, industrial laser gas equipment, one-to-two laser gas setup, auxiliary gas optimization":
     "Laserschneid-Gasmischer, Stickstoff-Sauerstoff-Mischgerät, Mikro-Sauerstoff-Laserschneiden, Kohlenstoffstahl-Laserschneiden, Hochleistungslaser 12kW 60kW, Mischgas vs. Luftkompressor, Entfernung von Laserschneidgraten, Reduzierung des Stickstoffverbrauchs, Han's Laser Gasmischer, industrielle Lasergasausrüstung, Eins-zu-zwei Lasergas-Setup, Schutzgasoptimierung",

    "LISHI LASER Mixed Gas Device | 3× Faster Laser Cutting":
     "LISHI LASER Mischgasgerät | 3× Schnelleres Laserschneiden",

    "Mixed gas device for 12KW-60KW laser cutting machines. 3× faster cutting speed, zero burrs, 33% less gas consumption. N2/O2 ratio technology.":
     "Mischgasgerät für 12KW-60KW Laserschneidmaschinen. 3× schnellere Schneidgeschwindigkeit, keine Grate, 33% weniger Gasverbrauch. N2/O2-Verhältnis-Technologie.",

    "Skip to content": "Zum Inhalt springen",
    "Home": "Startseite",
    "How It Works": "Funktionsweise",
    "Advantages": "Vorteile",
    "Parameters": "Parameter",
    "Samples": "Proben",
    "Customers": "Kunden",
    "Blog": "Blog",
    "Contact": "Kontakt",
    "Menu toggle": "Menü umschalten",
    "Gas Mixing Technology": "Gasmischtechnologie",

    "Cut <span class=\"accent\">3× Faster</span><br>with Mixed Gas Technology":
     "Schneiden Sie <span class=\"accent\">3× Schneller</span><br>mit Mischgastechnologie",
    "N₂/O₂ mixed gas solution for 12KW-60KW laser cutting machines":
     "N₂/O₂ Mischgaslösung für 12KW-60KW Laserschneidmaschinen",
    "3× Faster than O₂": "3× Schneller als O₂",
    "Zero Burrs": "Keine Grate",
    "33% Less N₂": "33% Weniger N₂",
    "13 Years in Laser Metal Cutting": "13 Jahre im Laser-Metallschneiden",
    "LISHI LASER Mixed Gas Device delivers micro-oxygen cutting for high-power laser machines (12KW–60KW). No burrs, less gas consumption, and dramatically faster processing.":
     "Das LISHI LASER Mischgasgerät liefert Mikro-Sauerstoff-Schneiden für Hochleistungslaser (12KW–60KW). Keine Grate, weniger Gasverbrauch und drastisch schnellere Bearbeitung.",
    "Get Quote →": "Angebot Einholen →",
    "View Parameters": "Parameter Ansehen",

    "What is a Mixed Gas Device?": "Was ist ein Mischgasgerät?",
    "Our nitrogen oxygen mixing device uses": "Unser Stickstoff-Sauerstoff-Mischgerät verwendet",
    "to produce precisely calibrated N₂/O₂ mixed gas — eliminating burrs on carbon steel while delivering 3× faster cutting speed versus traditional oxygen cutting. Supports high-power laser machines from 12kW to 60kW.":
     "zur Erzeugung von präzise kalibriertem N₂/O₂-Mischgas — beseitigt Grate auf Kohlenstoffstahl bei 3× schnellerer Schneidgeschwindigkeit im Vergleich zum traditionellen Sauerstoffschneiden. Unterstützt Hochleistungslaser von 12kW bis 60kW.",
    "Micro-oxygen laser cutting technology": "Mikro-Sauerstoff-Laserschneidtechnologie",
    "Liquid N₂ + Liquid O₂": "Flüssiges N₂ + Flüssiges O₂",
    "Raw materials stored in tanks, pressure 20–25 bar": "Rohstoffe in Tanks gelagert, Druck 20–25 bar",
    "Vaporizer": "Verdampfer",
    "Converts liquid gases to gas form": "Wandelt Flüssiggase in Gasform um",
    "Mixed Gas Device": "Mischgasgerät",
    "Stable pressure + proportional mixing → N₂ 95% / O₂ 5%": "Stabiler Druck + proportionale Mischung → N₂ 95% / O₂ 5%",
    "To Laser Machine": "Zur Lasermaschine",
    "Output: 12–16 bar, flow rate up to 200m³/h": "Ausgang: 12–16 bar, Durchfluss bis zu 200m³/h",
    "Input: N₂ + O₂ at 20–25 bar. Output: N₂ purity ~95%, pressure 12–16 bar, max flow 200m³/h. Compact gas tank (capacity >3m³).":
     "Eingang: N₂ + O₂ bei 20–25 bar. Ausgang: N₂-Reinheit ~95%, Druck 12–16 bar, max. Durchfluss 200m³/h. Kompakter Gastank (Kapazität >3m³).",
    "Device Dimensions": "Geräteabmessungen",
    "800mm × 350mm × 1100mm, weight 90kg. One device simultaneously supports two laser machines (One-to-Two configuration).":
     "800mm × 350mm × 1100mm, Gewicht 90kg. Ein Gerät unterstützt gleichzeitig zwei Lasermaschinen (Eins-zu-zwei-Konfiguration).",
    "High cutting speed + zero burrs. After installation, simply adjust the N₂ 95% to O₂ 5% ratio for different sheet thicknesses. The built-in program makes operation intuitive.":
     "Hohe Schneidgeschwindigkeit + keine Grate. Nach der Installation passen Sie einfach das N₂ 95% zu O₂ 5%-Verhältnis für verschiedene Blechdicken an. Das integrierte Programm macht die Bedienung intuitiv.",
    "Broad Compatibility": "Breite Kompatibilität",
    "Works with all major brands: HAN'S, DNE, PENTA, LEAD, HSG and more. Compatible with BODOR, KIMLA, MESSER and other global brands.":
     "Funktioniert mit allen großen Marken: HAN'S, DNE, PENTA, LEAD, HSG und mehr. Kompatibel mit BODOR, KIMLA, MESSER und anderen globalen Marken.",

    "Why Mixed Gas Instead of O₂, N₂ or Air?": "Warum Mischgas statt O₂, N₂ oder Luft?",
    "Eliminate burrs in carbon steel laser cutting while cutting nitrogen consumption by 33%. Our maintenance-free gas delivery system is compatible with Han's laser, DNE, PENTA, LEAD, HSG, BODOR and all other major brands.":
     "Beseitigen Sie Grate beim Kohlenstoffstahl-Laserschneiden und reduzieren Sie den Stickstoffverbrauch um 33%. Unser wartungsfreies Gasversorgungssystem ist kompatibel mit HAN'S, DNE, PENTA, LEAD, HSG, BODOR und allen anderen großen Marken.",
    "Competitive Advantage": "Wettbewerbsvorteil",
    "3× Faster Cutting": "3× Schnelleres Schneiden",
    "Boost laser cutting speed up to 3× compared to oxygen cutting. Example: 8mm carbon steel at 16m/min with mixed gas, only 2–3m/min with O₂.":
     "Steigern Sie die Laserschneidgeschwindigkeit um das 3-fache im Vergleich zum Sauerstoffschneiden. Beispiel: 8mm Kohlenstoffstahl mit 16m/min mit Mischgas, nur 2–3m/min mit O₂.",
    "Eliminate Burrs": "Grate Beseitigen",
    "Controlled micro-oxygen environment ensures complete combustion. Result: smooth, burr-free cutting edges requiring no secondary grinding.":
     "Kontrollierte Mikro-Sauerstoff-Umgebung gewährleistet vollständige Verbrennung. Ergebnis: glatte, gratfreie Schnittkanten, die kein Nachschleifen erfordern.",
    "Cut Gas Costs": "Gaskosten Senken",
    "Reduce nitrogen consumption by 33–50% versus pure N₂ cutting. Cost comparison: mixed gas costs significantly less than air compressors when factoring in maintenance-free operation.":
     "Reduzieren Sie den Stickstoffverbrauch um 33–50% gegenüber reinem N₂-Schneiden. Kostenvergleich: Mischgas kostet deutlich weniger als Luftkompressoren bei wartungsfreiem Betrieb.",
    "Maintenance-Free": "Wartungsfrei",
    "Power consumption: only 2 kWh per 24 hours. Unlike air compressors that require filter/oil changes every 3,000 hours, our industrial laser gas equipment is maintenance-free.":
     "Stromverbrauch: nur 2 kWh pro 24 Stunden. Im Gegensatz zu Luftkompressoren, die alle 3.000 Stunden Filter-/Ölwechsel benötigen, ist unsere industrielle Lasergasausrüstung wartungsfrei.",
    "One-to-Two Laser Setup": "Eins-zu-zwei Laser-Setup",
    "The only manufacturer with stable one-to-two mixed gas equipment. One industrial gas mixing station powers two laser machines at different power levels simultaneously — no switching required.":
     "Der einzige Hersteller mit stabiler Eins-zu-zwei-Mischgasausrüstung. Eine industrielle Gasmischstation versorgt zwei Lasermaschinen gleichzeitig mit unterschiedlichen Leistungsstufen — kein Umschalten erforderlich.",
    "Lens Protection": "Linsenschutz",
    "Air compressors carry oil/water contamination risk that can burn laser head lenses ($5,000–50,000 loss). Our pure liquid gas source keeps your optical system pristine.":
     "Luftkompressoren bergen Öl-/Wasserkontaminationsrisiken, die Laserkopflinsen zerstören können ($5.000–50.000 Verlust). Unsere reine Flüssiggasquelle hält Ihr optisches System makellos.",
    "Performance Comparison: Mixed Gas vs O₂ vs N₂ vs Air": "Leistungsvergleich: Mischgas vs. O₂ vs. N₂ vs. Luft",
    "Factor": "Faktor",
    "Mixed Gas": "Mischgas",
    "O₂ (Oxygen)": "O₂ (Sauerstoff)",
    "N₂ (Nitrogen)": "N₂ (Stickstoff)",
    "Air": "Luft",
    "Cutting Speed": "Schneidgeschwindigkeit",
    "3× faster (e.g. 16m/min @ 8mm CS)": "3× schneller (z.B. 16m/min @ 8mm KS)",
    "30% slower than mixed gas": "30% langsamer als Mischgas",
    "Burrs possible on thick sheets": "Grate möglich bei dicken Blechen",
    "Cut Surface": "Schnittfläche",
    "Smooth, burr-free": "Glatt, gratfrei",
    "Oxidized, rough edges": "Oxidiert, raue Kanten",
    "Contaminated, rough": "Verschmutzt, rau",
    "Gas Consumption": "Gasverbrauch",
    "1/3 less than N₂": "1/3 weniger als N₂",
    "Similar total": "Ähnliche Summe",
    "High": "Hoch",
    "Very high (compressor)": "Sehr hoch (Kompressor)",
    "Power Cost": "Stromkosten",
    "2 kWh/24h": "2 kWh/24h",
    "Small Hole Piercing": "Kleinlochstechen",
    "Excellent — clean & fast": "Ausgezeichnet — sauber & schnell",
    "Some burr during piercing": "Etwas Grat beim Stechen",
    "Best for small holes": "Am besten für kleine Löcher",
    "Equipment Protection": "Geräteschutz",
    "No pipeline contamination": "Keine Rohrleitungskontamination",
    "Oil/water risk": "Öl-/Wasserrisiko",

    "ROI Calculator": "ROI-Rechner",
    "Calculator": "Rechner",
    "Calculate Your Laser Cutting Gas Cost Savings": "Berechnen Sie Ihre Gaskostenersparnis beim Laserschneiden",
    "See how much you could save with LISHI LASER mixed gas technology. Cut nitrogen consumption, eliminate burrs on carbon steel, and boost throughput.":
     "Sehen Sie, wie viel Sie mit der LISHI LASER Mischgastechnologie sparen können. Reduzieren Sie den Stickstoffverbrauch, beseitigen Sie Grate und steigern Sie den Durchsatz.",
    "Machine Power": "Maschinenleistung",
    "Material Thickness": "Materialdicke",
    "Daily Work Hours": "Tägliche Arbeitsstunden",
    "Actual Cutting Time (Beam On %)": "Tatsächliche Schneidzeit (Strahl an %)",
    "Typical shops run 40–70% — remaining time is loading, piercing, idle.": "Typische Betriebe arbeiten 40–70% — die restliche Zeit ist Laden, Stechen, Leerlauf.",
    "Profit Per Meter (USD/m)": "Gewinn pro Meter (USD/m)",
    "Your selling price minus material cost (USD)": "Ihr Verkaufspreis abzüglich Materialkosten (USD)",
    "Monthly N₂ Cost (USD)": "Monatliche N₂-Kosten (USD)",
    "Your current monthly nitrogen spend (USD)": "Ihre aktuellen monatlichen Stickstoffkosten (USD)",
    "Estimated Annual Profit Increase (USD)": "Geschätzte jährliche Gewinnsteigerung (USD)",
    "in nitrogen savings": "an Stickstoffeinsparung",
    "Theoretical ceiling based on your inputs. Real results depend on job mix, nesting efficiency and machine uptime.":
     "Theoretische Obergrenze basierend auf Ihren Eingaben. Tatsächliche Ergebnisse hängen vom Auftragsmix, der Verschachtelungseffizienz und der Maschinenverfügbarkeit ab.",
    "Want the full parameter table for your specific machine?": "Möchten Sie die vollständige Parametertabelle für Ihre Maschine?",
    "Get detailed cutting data tailored to your 12KW–60KW laser setup.": "Erhalten Sie detaillierte Schneiddaten für Ihr 12KW–60KW Laser-Setup.",
    "Get Free Parameters →": "Kostenlose Parameter Erhalten →",
    "Or contact us directly:": "Oder kontaktieren Sie uns direkt:",

    "Why Air Compressors Cost More": "Warum Luftkompressoren Mehr Kosten",
    "Air Looks Free. It Isn't.": "Luft Sieht Kostenlos Aus. Ist Sie Aber Nicht.",
    "Most users pick an air compressor for the low upfront cost — but three hidden costs eat your margin.":
     "Die meisten Anwender wählen einen Luftkompressor wegen der niedrigen Anschaffungskosten — aber drei versteckte Kosten fressen Ihre Marge.",
    "HIGH MAINTENANCE COST": "HOHE WARTUNGSKOSTEN",
    "Filter replacement every 500-1000 hours": "Filterwechsel alle 500-1000 Stunden",
    "Oil changes and system flushing": "Ölwechsel und Systemspülung",
    "Unexpected repair downtime": "Unerwartete Reparaturausfallzeiten",
    "2 kWh/24h — near zero maintenance": "2 kWh/24h — nahezu keine Wartung",
    "~$73/year electricity": "~$73/Jahr Strom",
    "POOR CUT QUALITY": "SCHLECHTE SCHNITTQUALITÄT",
    "Dark oxidation layer on cut surface": "Dunkle Oxidationsschicht auf der Schnittfläche",
    "Burrs and slag requiring rework": "Grate und Schlacke erfordern Nacharbeit",
    "Extra grinding/polishing labor": "Zusätzliche Schleif-/Polierarbeit",
    "Cannot deliver premium jobs": "Premium-Aufträge nicht lieferbar",
    "Silver-white surface, zero burrs": "Silber-weiße Oberfläche, keine Grate",
    "Ready to ship immediately": "Sofort versandfertig",
    "LENS CONTAMINATION RISK": "LINSENKONTAMINATIONSRISIKO",
    "Oil/water in compressed air": "Öl/Wasser in Druckluft",
    "Burns the laser head protection lens": "Zerstört die Laserkopf-Schutzlinse",
    "Lens replacement: $200–500 each time": "Linsenwechsel: $200–500 pro Mal",
    "Unplanned production stop": "Ungeplanter Produktionsstopp",
    "100% safe — pure liquid gas source": "100% sicher — reine Flüssiggasquelle",
    "Zero optical risk": "Kein optisches Risiko",
    "LISHI Mixed Gas: The Real Cost Saver": "LISHI Mischgas: Der echte Kostensparer",
    "While air looks free, your real cost is in maintenance, rework, and lens replacements. Mixed gas costs less long-term — and delivers superior quality.":
     "Luft sieht kostenlos aus, aber die wahren Kosten liegen in Wartung, Nacharbeit und Linsenwechseln. Mischgas kostet langfristig weniger — und liefert überlegene Qualität.",

    "Cutting Parameters by Power": "Schneidparameter nach Leistung",
    "Optimal carbon steel cutting thickness range for each laser power level. Mixed gas delivers consistent high-speed cutting across all thicknesses.":
     "Optimaler Kohlenstoffstahl-Schneiddickenbereich für jede Laserleistungsstufe. Mischgas liefert konsistentes Hochgeschwindigkeitsschneiden über alle Dicken.",
    "Mixed Gas Speed": "Mischgas-Geschwindigkeit",
    "Best for ≤16mm carbon steel": "Optimal für ≤16mm Kohlenstoffstahl",
    "Best for ≤25mm carbon steel": "Optimal für ≤25mm Kohlenstoffstahl",
    "Contact for details": "Kontakt für Details",
    "Best for ≤30mm carbon steel": "Optimal für ≤30mm Kohlenstoffstahl",
    "Higher powers (40KW, 60KW) available. Contact us for detailed parameters.": "Höhere Leistungen (40KW, 60KW) verfügbar. Kontaktieren Sie uns für detaillierte Parameter.",
    "View All Parameters →": "Alle Parameter Ansehen →",

    "Real Results": "Echte Ergebnisse",
    "Cutting Samples & Test Videos": "Schnittproben & Testvideos",
    "Real cutting footage from end users worldwide. No retouching — real data, real performance.":
     "Echte Schneidaufnahmen von Endanwendern weltweit. Keine Retusche — echte Daten, echte Leistung.",
    "12kW & 30kW · Professional Metal Fab": "12kW & 30kW · Professionelle Metallfertigung",
    "Dual-power setup, one device feeds two machines — 33% less gas, no speed compromise": "Dual-Power-Setup, ein Gerät versorgt zwei Maschinen — 33% weniger Gas, kein Geschwindigkeitsverlust",
    "Mixed gas for high-power lasers": "Mischgas für Hochleistungslaser",
    "30kW · 10–30mm Carbon Steel": "30kW · 10–30mm Kohlenstoffstahl",
    "Thick sheets, zero burrs. 10–14 m/min on 10mm, previously only possible with O₂": "Dicke Bleche, keine Grate. 10–14 m/min bei 10mm, zuvor nur mit O₂ möglich",
    "High-power mixed gas cutting": "Hochleistungs-Mischgasschneiden",
    "60kW · 30–40mm Carbon Steel": "60kW · 30–40mm Kohlenstoffstahl",
    "Ultra-thick cutting at 3.5 m/min. Where N₂ struggles, mixed gas dominates": "Ultra-dickes Schneiden mit 3,5 m/min. Wo N₂ kämpft, dominiert Mischgas",
    "Ultra-high-power mixed gas": "Ultra-Hochleistungs-Mischgas",
    "12kW · 3mm Aluminum": "12kW · 3mm Aluminium",
    "Smooth aluminum edges, zero oxidation. Faster than air, cleaner than N₂": "Glatte Aluminiumkanten, keine Oxidation. Schneller als Luft, sauberer als N₂",
    "Aluminum mixed gas cutting": "Aluminium-Mischgasschneiden",
    "12kW · 2mm Aluminum": "12kW · 2mm Aluminium",
    "Precision aluminum with micro-oxygen — speed and quality in a single pass": "Präzisionsaluminium mit Mikro-Sauerstoff — Geschwindigkeit und Qualität in einem Durchgang",
    "Thin aluminum mixed gas": "Dünnaluminium-Mischgas",
    "12kW · 1mm Aluminum": "12kW · 1mm Aluminium",
    "Paper-thin aluminum, zero burn. Mixed gas enables what N₂ can't achieve": "Papierdünnes Aluminium, kein Brennen. Mischgas ermöglicht, was N₂ nicht erreichen kann",
    "Precision thin aluminum cutting": "Präzisions-Dünnaluminiumschneiden",
    "Watch Video": "Video Ansehen",

    "GLOBAL NETWORK": "GLOBALES NETZWERK",
    "Where High-Power Lasers Cut.<br>Our Gas Flows.": "Wo Hochleistungslaser Schneiden.<br>Fließt Unser Gas.",
    "From mega-factories on the coast to workshops deep inland, mixed gas technology now powers laser cutters across four continents — and the footprint is expanding every quarter.":
     "Von Megafabriken an der Küste bis zu Werkstätten tief im Inland — Mischgastechnologie treibt heute Laserschneider auf vier Kontinenten an — und die Präsenz wächst jedes Quartal.",
    "Countries Stocked": "Länder Beliefert",
    "Continents Deployed": "Kontinente Erschlossen",
    "Power Range Served": "Abgedeckter Leistungsbereich",
    "Manufacturing Durability": "Fertigungsrobustheit",
    "The Next Territory is Still Open.": "Das Nächste Gebiet ist Noch Frei.",
    "Exclusive distributor partnerships available in select regions. Ship a container, build your market.":
     "Exklusive Vertriebspartnerschaften in ausgewählten Regionen verfügbar. Versenden Sie einen Container, bauen Sie Ihren Markt auf.",

    "Frequently Asked Questions": "Häufig Gestellte Fragen",
    "What is a mixed gas device and how does it work?": "Was ist ein Mischgasgerät und wie funktioniert es?",
    "A mixed gas device converts liquid nitrogen (N₂) and liquid oxygen (O₂) into a precisely calibrated N₂/O₂ gas mixture (typically 95%/5%). This micro-oxygen blend is used as auxiliary gas in high-power laser cutting, delivering 3× faster cutting speeds on carbon steel compared to pure oxygen while completely eliminating burrs.":
     "Ein Mischgasgerät wandelt flüssigen Stickstoff (N₂) und flüssigen Sauerstoff (O₂) in eine präzise kalibrierte N₂/O₂-Gasmischung (typisch 95%/5%) um. Diese Mikro-Sauerstoff-Mischung wird als Hilfsgas beim Hochleistungs-Laserschneiden verwendet und liefert 3× schnellere Schneidgeschwindigkeiten bei Kohlenstoffstahl im Vergleich zu reinem Sauerstoff bei vollständiger Gratfreiheit.",
    "Is it compatible with my laser machine?": "Ist es mit meiner Lasermaschine kompatibel?",
    "Yes. The LISHI LASER Mixed Gas Device works with all major laser brands including HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA and MESSER. It supports machines from 12kW to 60kW. If your machine uses standard auxiliary gas connections, it is compatible.":
     "Ja. Das LISHI LASER Mischgasgerät funktioniert mit allen großen Lasermarken, einschließlich HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA und MESSER. Es unterstützt Maschinen von 12kW bis 60kW. Wenn Ihre Maschine Standard-Hilfsgasanschlüsse verwendet, ist sie kompatibel.",
    "What thicknesses can it cut?": "Welche Dicken kann es schneiden?",
    "The cutting range depends on your laser power: 12kW handles up to 16mm, 20kW up to 25mm, 30kW up to 30mm, and 60kW up to 40mm carbon steel. It also cuts stainless steel and aluminum. Detailed cutting parameter tables are available on our parameters page below.":
     "Der Schneidbereich hängt von Ihrer Laserleistung ab: 12kW bearbeitet bis zu 16mm, 20kW bis zu 25mm, 30kW bis zu 30mm und 60kW bis zu 40mm Kohlenstoffstahl. Es schneidet auch Edelstahl und Aluminium. Detaillierte Schneidparametertabellen finden Sie auf unserer Parameterseite.",
    "How much gas does it save?": "Wie viel Gas spart es?",
    "Mixed gas reduces nitrogen consumption by 33–50% compared to pure N₂ cutting. Additionally, the device consumes only 2 kWh per 24 hours — essentially maintenance-free. The optimized mixing ratio means you get more cutting per unit of gas.":
     "Mischgas reduziert den Stickstoffverbrauch um 33–50% im Vergleich zu reinem N₂-Schneiden. Zusätzlich verbraucht das Gerät nur 2 kWh pro 24 Stunden — praktisch wartungsfrei. Das optimierte Mischverhältnis bedeutet mehr Schnittleistung pro Gaseinheit.",
    "Does it require regular maintenance?": "Erfordert es regelmäßige Wartung?",
    "No. Unlike air compressors that need filter/oil changes every 500–3,000 hours, the LISHI Mixed Gas Device is maintenance-free. There are no moving parts to wear out, no filters to replace, and no oil to change.":
     "Nein. Im Gegensatz zu Luftkompressoren, die alle 500–3.000 Stunden Filter-/Ölwechsel benötigen, ist das LISHI Mischgasgerät wartungsfrei. Keine beweglichen Teile, die verschleißen, keine Filter zum Wechseln und kein Öl zum Wechseln.",
    "Can one device supply two lasers?": "Kann ein Gerät zwei Laser versorgen?",
    "Yes. LISHI LASER is the only manufacturer offering a stable One-to-Two configuration. One mixing station feeds two laser machines at different power levels (e.g., 12kW + 20kW) simultaneously — no switching, no pressure drops.":
     "Ja. LISHI LASER ist der einzige Hersteller mit einer stabilen Eins-zu-zwei-Konfiguration. Eine Mischstation versorgt zwei Lasermaschinen gleichzeitig mit unterschiedlichen Leistungsstufen (z.B. 12kW + 20kW) — kein Umschalten, keine Druckabfälle.",
    "How is mixed gas different from air cutting?": "Wie unterscheidet sich Mischgas vom Luftschneiden?",
    "Air cutting produces oxidized, rough edges and carries oil/water contamination risk that can burn expensive laser head lenses ($5,000–50,000). Mixed gas from pure liquid source delivers smooth, bright, burr-free edges — and protects your optics.":
     "Luftschneiden erzeugt oxidierte, raue Kanten und birgt Öl-/Wasserkontaminationsrisiken, die teure Laserkopflinsen zerstören können ($5.000–50.000). Mischgas aus reiner Flüssigquelle liefert glatte, helle, gratfreie Kanten — und schützt Ihre Optik.",
    "How long does installation take?": "Wie lange dauert die Installation?",
    "Installation is straightforward and typically completed within one day. The device connects to your existing liquid gas supply and laser machine. We provide detailed installation guidance for all customers.":
     "Die Installation ist einfach und in der Regel innerhalb eines Tages abgeschlossen. Das Gerät wird an Ihre bestehende Flüssiggasversorgung und Lasermaschine angeschlossen. Wir bieten detaillierte Installationsanleitungen für alle Kunden.",

    "Ready to Boost Your Cutting Speed?": "Bereit, Ihre Schneidgeschwindigkeit zu Steigern?",
    "Connect one device to your laser machine and start cutting 3× faster today. Available for 6KW–60KW machines.":
     "Schließen Sie ein Gerät an Ihre Lasermaschine an und schneiden Sie noch heute 3× schneller. Verfügbar für 6KW–60KW Maschinen.",
    "Contact Us →": "Kontaktieren Sie Uns →",
    "Get Free Consultation": "Kostenlose Beratung",

    "Brand-Authorized Overseas Market Operations Agent:": "Markenautorisierter Überseemarkt-Operationsagent:",
    "© 2025 Jinan Euchio Machinery Co., Ltd. All rights reserved.": "© 2025 Jinan Euchio Machinery Co., Ltd. Alle Rechte vorbehalten.",
    "Product": "Produkt",
    "Cutting Samples": "Schnittproben",

    # Contact page
    "LISHI LASER mixed gas device pricing and quotes. Compatible with all major laser brands (HANS, DNE, PENTA, LEAD, HSG, BODOR). Global shipping available.":
     "LISHI LASER Mischgasgerät Preise und Angebote. Kompatibel mit allen großen Lasermarken (HANS, DNE, PENTA, LEAD, HSG, BODOR). Weltweiter Versand verfügbar.",
    "laser cutting gas equipment quote, mixed gas device distributor, laser cutting equipment manufacturer, HANS laser compatible gas":
     "Laserschneid-Gasausrüstung Angebot, Mischgasgerät Vertriebspartner, Laserschneidausrüstung Hersteller, HANS Laser kompatibles Gas",
    "LISHI LASER Contact | Get Mixed Gas Device Quote": "LISHI LASER Kontakt | Mischgasgerät Angebot Einholen",
    "Request a quote for LISHI LASER mixed gas cutting equipment. Compatible with all major laser brands. Global shipping available.":
     "Fordern Sie ein Angebot für LISHI LASER Mischgas-Schneidausrüstung an. Kompatibel mit allen großen Lasermarken. Weltweiter Versand verfügbar.",
    "LISHI LASER Contact": "LISHI LASER Kontakt",
    "Get in Touch": "Kontaktieren Sie Uns",
    "Contact Us": "Kontakt",
    "Ready to boost your cutting speed? Send your laser machine details and we'll provide custom parameters and pricing.":
     "Bereit, Ihre Schneidgeschwindigkeit zu steigern? Senden Sie Ihre Lasermaschinendaten und wir erstellen individuelle Parameter und Preise.",
    "Email": "E-Mail",
    "Reply within 24 hours": "Antwort innerhalb von 24 Stunden",
    "Phone / WeChat": "Telefon / WeChat",
    "WeChat: same number": "WeChat: gleiche Nummer",
    "Company": "Unternehmen",
    "Product Brand": "Produktmarke",
    "Mixed Gas Device — 13 years in laser cutting industry": "Mischgasgerät — 13 Jahre in der Laserschneidindustrie",
    "Looking for a distributor?": "Suchen Sie einen Vertriebspartner?",
    "We are actively expanding our global agent network. Exclusive territories available for qualified distributors.":
     "Wir erweitern aktiv unser globales Agentennetzwerk. Exklusive Gebiete für qualifizierte Vertriebspartner verfügbar.",
    "Agency Application →": "Agenturantrag →",
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
    "Or reach us directly via": "Oder erreichen Sie uns direkt via",
    "for faster response.": "für schnellere Antwort.",
    "Your Message Has Been Sent!": "Ihre Nachricht Wurde Gesendet!",
    "Thank you for your inquiry. We will respond within 24 hours.": "Vielen Dank für Ihre Anfrage. Wir werden innerhalb von 24 Stunden antworten.",
    "Back to Home": "Zurück zur Startseite",

    # Parameters page
    "Cutting Parameters": "Schneidparameter",
    "Detailed cutting parameters for different laser powers. All tests performed on real customer machines. Results verified by our engineering team.":
     "Detaillierte Schneidparameter für verschiedene Laserleistungen. Alle Tests auf echten Kundenmaschinen durchgeführt. Ergebnisse von unserem Ingenieurteam verifiziert.",
    "Thickness": "Dicke",
    "Speed Improvement": "Geschwindigkeitsverbesserung",
    "Test Location": "Teststandort",
    "Notes": "Anmerkungen",
    "Mixed Gas Optimization": "Mischgas-Optimierung",
    "Gas Consumption Comparison": "Gasverbrauchsvergleich",
    "Pure Nitrogen": "Reiner Stickstoff",
    "Mixed gas": "Mischgas",
    "Savings": "Einsparung",
    "per hour": "pro Stunde",
    "per day": "pro Tag",
    "per month": "pro Monat",
    "per year": "pro Jahr",
    "Download Parameters": "Parameter Herunterladen",
    "Get Technical Support": "Technischen Support Erhalten",

    "How do I read the cutting parameters table?": "Wie lese ich die Schneidparametertabelle?",
    "The table shows cutting speed in meters per minute (m/min), mixed gas pressure in bar, and nozzle diameter in mm. Higher speeds mean better productivity. The speed improvement percentage shows the gain versus pure oxygen cutting.":
     "Die Tabelle zeigt die Schneidgeschwindigkeit in Metern pro Minute (m/min), den Mischgasdruck in bar und den Düsendurchmesser in mm. Höhere Geschwindigkeiten bedeuten bessere Produktivität. Die Geschwindigkeitsverbesserung in Prozent zeigt den Gewinn gegenüber reinem Sauerstoffschneiden.",
    "Why does speed improvement decrease at very thick materials?": "Warum nimmt die Geschwindigkeitsverbesserung bei sehr dicken Materialien ab?",
    "At extreme thicknesses (30mm+), the limiting factor shifts from gas chemistry to laser power penetration. The mixed gas still provides benefits in edge quality and eliminates burrs, but the raw speed difference versus oxygen narrows because both processes are dominated by the laser beam's physical ability to penetrate the material.":
     "Bei extremen Dicken (30mm+) verschiebt sich der begrenzende Faktor von der Gaschemie zur Laserleistungsdurchdringung. Das Mischgas bietet weiterhin Vorteile bei der Kantenqualität und beseitigt Grate, aber der reine Geschwindigkeitsunterschied gegenüber Sauerstoff verringert sich, da beide Prozesse von der physikalischen Fähigkeit des Laserstrahls zur Materialdurchdringung dominiert werden.",
}

# ============================================================
# FRENCH TRANSLATIONS
# ============================================================
FR = {}
# Build FR by copying IT structure and translating key terms to French
# For brevity, I'll use a subset approach for FR and NL

# ============================================================
# DUTCH TRANSLATIONS
# ============================================================
NL = {}

# ============================================================
# Apply translations
# ============================================================
def translate_file(filepath, translations):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for english, target in translations.items():
        if english in content:
            content = content.replace(english, target)
        else:
            missing.append(english[:80])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    if missing:
        print(f"  {len(missing)} unmatched strings in {filepath}")
        for m in missing[:5]:
            print(f"    - {m}...")

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    translations = {'it': IT, 'de': DE, 'fr': FR, 'nl': NL}.get(lang, {})

    if not translations:
        print(f"Language {lang} translations not defined yet")
        sys.exit(1)

    for f in ['index.html', 'contact.html', 'parameters.html']:
        filepath = os.path.join(BASE, lang, f)
        if os.path.exists(filepath):
            translate_file(filepath, translations)

    print(f"\n{lang} translation done!")

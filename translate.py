#!/usr/bin/env python3
"""Translate HTML files from Turkish to target languages."""
import sys, os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

# Translation maps: Turkish → target language
# Italian translations
IT_TRANSLATIONS = {
    # Meta
    "12KW-60KW lazer kesim makineleri için LISHI LASER Karma Gaz Cihazı. 3 kat daha hızlı kesim, sıfır çapak, %33 daha az gaz tüketimi. Karbon çeliği kesimi için N2/O2 oran teknolojisi.":
     "Dispositivo a gas misto LISHI LASER per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di consumo gas in meno. Tecnologia a rapporto N2/O2 per taglio acciaio al carbonio.",

    "lazer kesim gaz karıştırıcı, nitrojen oksijen karışım cihazı, mikro oksijen lazer kesim, karbon çeliği lazer kesim, yüksek güçlü lazer 12kW 60kW, karma gaz vs hava kompresörü, lazer kesim çapaklarını giderme, nitrojen tüketimini azaltma, Han's lazer gaz karıştırıcı, endüstriyel lazer gaz ekipmanı, bire-iki lazer gaz kurulumu, yardımcı gaz optimizasyonu":
     "miscelatore gas taglio laser, dispositivo miscelazione azoto ossigeno, taglio laser micro ossigeno, taglio laser acciaio carbonio, laser alta potenza 12kW 60kW, gas misto vs compressore aria, eliminazione bave taglio laser, riduzione consumo azoto, miscelatore gas laser Han's, apparecchiatura gas laser industriale, configurazione gas uno-a-due, ottimizzazione gas assistito",

    "LISHI LASER Karma Gaz Cihazı | 3× Daha Hızlı Lazer Kesim":
     "LISHI LASER Dispositivo a Gas Misto | Taglio Laser 3× Più Veloce",

    "12KW-60KW lazer kesim makineleri için karma gaz cihazı. 3× daha hızlı kesim, sıfır çapak, %33 daha az gaz tüketimi. N2/O2 oran teknolojisi.":
     "Dispositivo a gas misto per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di consumo gas in meno. Tecnologia a rapporto N2/O2.",

    # Hero
    "Karma Gaz Teknolojisi ile<br><span class=\"accent\">3× Daha Hızlı</span> Kesin":
     "Taglia <span class=\"accent\">3× Più Veloce</span><br>con la Tecnologia a Gas Misto",

    "12KW-60KW lazer kesim makineleri için N₂/O₂ karma gaz çözümü":
     "Soluzione gas misto N₂/O₂ per macchine da taglio laser 12KW-60KW",

    "O₂'den 3 Kat Daha Hızlı":
     "3× Più Veloce dell'O₂",
    "Sıfır Çapak":
     "Zero Bave",
    "%33 Daha Az Azot":
     "33% Meno Azoto",

    # Nav
    "Ana Sayfa": "Home",
    "Çalışma Prensibi": "Principio di Funzionamento",
    "Avantajlar": "Vantaggi",
    "Parametreler": "Parametri",
    "Numuneler": "Campioni",
    "Müşteriler": "Clienti",
    "İletişim": "Contatto",
    "SSS": "FAQ",
    "Ana navigasyon": "Navigazione principale",

    # Principle
    "Karma Gaz Cihazı Nedir?": "Cos'è un Dispositivo a Gas Misto?",
    "Karma gaz cihazı, yüksek saflıkta sıvı nitrojen (N₂) ve sıvı oksijeni (O₂) hassas IGBT kontrollü karıştırma teknolojisi ile birleştirir.":
     "Il dispositivo a gas misto combina azoto liquido (N₂) e ossigeno liquido (O₂) ad alta purezza tramite tecnologia di miscelazione a controllo IGBT di precisione.",
    "Sonuç, karbon çeliği kesiminde saf oksijenden 3 kat daha hızlı, saf azottan çok daha ekonomik bir yardımcı gazdır.":
     "Il risultato è un gas assistito 3 volte più veloce dell'ossigeno puro per il taglio dell'acciaio al carbonio, e molto più economico dell'azoto puro.",

    # Advantages
    "Neden O₂, N₂ veya Hava Yerine Karma Gaz?": "Perché Gas Misto invece di O₂, N₂ o Aria?",
    "Lazer kesim karbon çeliğinde çapakları ortadan kaldırırken nitrojen tüketimini %33 azaltın. Bakım gerektirmeyen gaz besleme sistemimiz Han's lazer, DNE, PENTA, LEAD, HSG, BODOR ve diğer büyük markalarla uyumludur.":
     "Elimina le bave nel taglio laser dell'acciaio al carbonio riducendo il consumo di azoto del 33%. Il nostro sistema di alimentazione gas esente da manutenzione è compatibile con HAN'S, DNE, PENTA, LEAD, HSG, BODOR e tutti gli altri grandi marchi.",

    "3× Daha Hızlı Kesim": "Taglio 3× Più Veloce",
    "Oksijen kesime kıyasla lazer kesim hızını 3 kata kadar artırın. Örnek: 8mm karbon çeliği karma gaz ile 16m/dk, O₂ ile sadece 2–3m/dk.":
     "Aumenta la velocità di taglio laser fino a 3 volte rispetto al taglio a ossigeno. Esempio: acciaio al carbonio 8mm a 16m/min con gas misto, solo 2–3m/min con O₂.",
    "Sıfır Çapak, Temiz Kenar": "Zero Bave, Bordo Pulito",
    "Kontrollü mikro-oksijen ortamı tam yanma sağlar. Sonuç: ek zımpara gerektirmeyen pürüzsüz, çapaksız kesim kenarları.":
     "L'ambiente a micro-ossigeno controllato garantisce una combustione completa. Risultato: bordi di taglio lisci e senza bave che non richiedono ulteriore levigatura.",
    "Azot Tüketiminde %33 Tasarruf": "33% di Risparmio sul Consumo di Azoto",
    "Optimize edilmiş N₂/O₂ karışım oranı, saf azota kıyasla azot kullanımını yaklaşık üçte bir oranında azaltır.":
     "Il rapporto di miscelazione N₂/O₂ ottimizzato riduce l'uso di azoto di circa un terzo rispetto all'azoto puro.",
    "Bakım Gerektirmez": "Esente da Manutenzione",
    "Güç tüketimi: 24 saatte sadece 2 kWh. Her 3.000 saatte bir filtre/yağ değişimi gerektiren hava kompresörlerinin aksine, endüstriyel lazer gaz ekipmanımız bakım gerektirmez.":
     "Consumo energetico: solo 2 kWh in 24 ore. A differenza dei compressori d'aria che richiedono cambio filtri/olio ogni 3.000 ore, la nostra apparecchiatura gas laser industriale è esente da manutenzione.",
    "Geniş Uyumluluk": "Ampia Compatibilità",
    "Tüm büyük lazer markalarıyla uyumludur: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA ve MESSER. 12kW'dan 60kW'a kadar destekler.":
     "Compatibile con tutti i principali marchi laser: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA e MESSER. Supporta da 12kW a 60kW.",

    # ROI
    "Lazer Kesim Gaz Maliyet Tasarrufunuzu Hesaplayın": "Calcola il Risparmio sui Costi del Gas da Taglio Laser",
    "Makine Gücü": "Potenza Macchina",
    "Malzeme Kalınlığı": "Spessore Materiale",
    "Günlük Çalışma Saati": "Ore Lavorative Giornaliere",
    "Gaz Maliyeti (/m³)": "Costo Gas (/m³)",
    "Hesapla": "Calcola",
    "Yıllık Tahmini Tasarruf": "Risparmio Annuo Stimato",
    "Yatırım Geri Dönüş Süresi": "Periodo di Recupero dell'Investimento",
    "ay": "mesi",
    "Tahmini Yıllık Kâr Artışı (USD)": "Aumento Stimato del Profitto Annuo (USD)",
    "Ücretsiz Parametreleri Alın →": "Ottieni Parametri Gratuiti →",
    "ROI Hesaplayıcı": "Calcolatore ROI",
    "Hesaplayıcı": "Calcolatore",

    # Air vs Mixed
    "Hava Kompresörü ve Karma Gaz Karşılaştırması": "Confronto tra Compressore d'Aria e Gas Misto",
    "Hava Kompresörü Neden Daha Maliyetli": "Perché il Compressore d'Aria Costa di Più",
    "Yüksek Bakım Maliyeti": "Costo di Manutenzione Elevato",
    "Hava kompresörü sistemleri düzenli filtre değişimi, yağ değişimi ve kurutucu bakımı gerektirir. Yıllık bakım maliyeti genellikle $2.000–5.000 arasındadır.":
     "I sistemi con compressore d'aria richiedono cambio regolare di filtri, olio e manutenzione dell'essiccatore. Il costo di manutenzione annuale è tipicamente di $2.000–5.000.",
    "Düşük Kesim Kalitesi": "Scarsa Qualità di Taglio",
    "Hava ile kesimde oksidasyon kontrol edilemez, sonuç olarak kesim kenarlarında çapak ve renk değişimi oluşur.":
     "Il taglio ad aria non può controllare l'ossidazione, risultando in bave e scolorimento sui bordi di taglio.",
    "Lens Kontaminasyonu": "Contaminazione delle Lenti",
    "Kompresörden gelen yağ buharı ve partiküller lazer optiklerini kirleterek lens ömrünü kısaltır.":
     "I vapori d'olio e le particelle dal compressore contaminano l'ottica laser, riducendo la durata delle lenti.",
    "Enerji Tüketimi": "Consumo Energetico",
    "Hava kompresörleri tipik olarak saatte 15–30kW tüketir. Karma gaz cihazı yalnızca 2kWh/24h tüketir.":
     "I compressori d'aria consumano tipicamente 15–30kW all'ora. Il dispositivo a gas misto consuma solo 2kWh/24h.",
    "Gürültü": "Rumore",
    "Hava kompresörleri 75–85dB gürültü üretir. Karma gaz cihazı sessiz çalışır.":
     "I compressori d'aria producono 75–85dB di rumore. Il dispositivo a gas misto funziona silenziosamente.",
    "Gaz Besleme": "Alimentazione Gas",
    "Hava kompresörü sürekli çalışır. Karma gaz cihazı talep üzerine gaz üretir.":
     "Il compressore d'aria funziona continuamente. Il dispositivo a gas misto produce gas su richiesta.",

    # Parameters section
    "Güce Göre Kesim Parametreleri": "Parametri di Taglio per Potenza",
    "Tüm Parametreleri Görün →": "Visualizza Tutti i Parametri →",
    "Detaylı Parametreler →": "Parametri Dettagliati →",

    # Samples
    "Kesim Numuneleri ve Test Videoları": "Campioni di Taglio e Video di Test",
    "Gerçek müşteri kesim sonuçları, farklı malzeme ve güç seviyelerinde test edilmiştir.":
     "Risultati reali di taglio dei clienti, testati su diversi materiali e livelli di potenza.",
    "Video İzleyin": "Guarda il Video",
    "Kesim Videosu": "Video di Taglio",
    "Öncesi / Sonrası": "Prima / Dopo",

    # Global
    "KÜRESEL AĞ": "RETE GLOBALE",
    "50+ Ülke": "50+ Paesi",
    "500+ Kurulu Sistem": "500+ Sistemi Installati",
    "30+ Distribütör": "30+ Distributori",
    "Küresel Satış Sonrası Destek": "Supporto Post-Vendita Globale",
    "Asya": "Asia",
    "Avrupa": "Europa",
    "Amerika": "Americhe",
    "Afrika": "Africa",
    "Okyanusya": "Oceania",

    # FAQ
    "Sıkça Sorulan Sorular": "Domande Frequenti",

    # CTA
    "Kesim Hızınızı Artırmaya Hazır mısınız?": "Pronto ad Aumentare la Tua Velocità di Taglio?",
    "Hemen bizimle iletişime geçin, size özel çözüm ve fiyatlandırma sunalım.":
     "Contattaci subito per una soluzione e un preventivo personalizzati.",
    "Hemen İletişime Geçin": "Contattaci Ora",
    "Ücretsiz Danışmanlık Alın": "Ottieni una Consulenza Gratuita",
    "Teklif Alın": "Richiedi Preventivo",
    "Nasıl Çalışır →": "Come Funziona →",

    # Footer
    "Marka Lisanslı Yurtdışı Pazar Operasyon Acentesi:": "Agente Autorizzato per le Operazioni sul Mercato Estero:",
    "Tüm hakları saklıdır.": "Tutti i diritti riservati.",
    "Gaz Karışım Teknolojisi": "Tecnologia di Miscelazione Gas",
    "Ürün": "Prodotto",
    "Nasıl Çalışır": "Come Funziona",
    "Kesim Numuneleri": "Campioni di Taglio",

    # Contact page
    "İletişime Geçin": "Contattaci",
    "Bize Ulaşın": "Contattaci",
    "Kesim hızınızı artırmaya hazır mısınız? Lazer makinenizin detaylarını gönderin, size özel parametreler ve fiyatlandırma sunalım.":
     "Pronto ad aumentare la tua velocità di taglio? Invia i dettagli della tua macchina laser e ti forniremo parametri e prezzi personalizzati.",
    "E-posta": "Email",
    "24 saat içinde yanıt": "Risposta entro 24 ore",
    "Telefon / WeChat": "Telefono / WeChat",
    "WeChat: aynı numara": "WeChat: stesso numero",
    "WhatsApp": "WhatsApp",
    "Şirket": "Azienda",
    "Ürün Markası": "Marchio del Prodotto",
    "Karma Gaz Cihazı — Lazer kesim sektöründe 13 yıl": "Dispositivo a Gas Misto — 13 anni nel settore del taglio laser",
    "Distribütör mü arıyorsunuz?": "Cerchi un distributore?",
    "Global acente ağımızı aktif olarak genişletiyoruz. Nitelikli distribütörler için özel bölgeler mevcuttur.":
     "Stiamo espandendo attivamente la nostra rete globale di agenti. Territori esclusivi disponibili per distributori qualificati.",
    "Acentelik Başvurusu →": "Richiesta Distributore →",
    "Bize Mesaj Gönderin": "Inviaci un Messaggio",
    "Ad Soyad *": "Nome e Cognome *",
    "Ahmet Yılmaz": "Mario Rossi",
    "ABC Lazer Ltd. Şti.": "ABC Laser S.r.l.",
    "ahmet@sirket.com": "mario@azienda.it",
    "Telefon / WhatsApp": "Telefono / WhatsApp",
    "+90 555 123 4567": "+39 333 123 4567",
    "Ülke": "Paese",
    "örn. Türkiye, Almanya, Polonya": "es. Italia, Germania, Francia",
    "Talep Türü": "Tipo di Richiesta",
    "Seçiniz...": "Seleziona...",
    "Fiyatlandırma ve Teklif": "Prezzi e Preventivo",
    "Teknik Parametreler": "Parametri Tecnici",
    "Distribütör / Acente": "Distributore / Agente",
    "OEM / Özelleştirme": "OEM / Personalizzazione",
    "Diğer": "Altro",
    "Lazer Makinesi Gücü": "Potenza Macchina Laser",
    "Lazer gücü seçiniz...": "Seleziona potenza laser...",
    "Diğer / Birden Fazla": "Altro / Multiplo",
    "Lazer Makinesi Markası": "Marca Macchina Laser",
    "örn. HAN'S, DNE, PENTA, LEAD, BODOR": "es. HAN'S, DNE, PENTA, LEAD, BODOR",
    "Mesaj *": "Messaggio *",
    "Kesim ihtiyaçlarınızı belirtin — malzeme türü, kalınlık, mevcut gaz kurulumu, vb.":
     "Descrivi le tue esigenze di taglio — tipo di materiale, spessore, configurazione gas attuale, ecc.",
    "Mesaj Gönder →": "Invia Messaggio →",
    "Veya daha hızlı yanıt için doğrudan": "O per una risposta più rapida, contatta direttamente via",
    "ile iletişime geçin.": ".",
    "Mesajınız Başarıyla Gönderildi!": "Messaggio Inviato con Successo!",
    "Talebiniz için teşekkür ederiz. 24 saat içinde yanıt vereceğiz.":
     "Grazie per la tua richiesta. Ti risponderemo entro 24 ore.",
    "Ana Sayfaya Dön": "Torna alla Home",

    # Parameters page
    "Kesim Parametreleri": "Parametri di Taglio",
    "Aşağıda farklı lazer güçleri için ayrıntılı kesim parametreleri verilmiştir. Tüm testler gerçek müşteri makinelerinde yapılmıştır.":
     "Di seguito sono riportati i parametri di taglio dettagliati per diverse potenze laser. Tutti i test sono stati eseguiti su macchine reali dei clienti.",
    "Kalınlık": "Spessore",
    "Karma Gaz Hızı": "Velocità Gas Misto",
    "Hız Artışı": "Aumento Velocità",
    "Test Konumu": "Luogo del Test",
    "Notlar": "Note",
    "Karma Gaz Optimizasyonu": "Ottimizzazione Gas Misto",
    "Gaz Tüketim Karşılaştırması": "Confronto Consumo Gas",
    "Saf Azot": "Azoto Puro",
    "Karma Gaz": "Gas Misto",
    "Tasarruf": "Risparmio",
    "saatte": "all'ora",
    "günde": "al giorno",
    "ayda": "al mese",
    "yılda": "all'anno",
    "Parametreleri İndir": "Scarica Parametri",
    "Teknik Destek Alın": "Supporto Tecnico",
    "Parametreleri Görün": "Visualizza Parametri",

    # Misc section labels
    "Teklif": "Preventivo",
    "Numune": "Campione",
    "Referans": "Referenza",
}

def translate_file(filepath, translations):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for turkish, target in translations.items():
        if turkish in content:
            content = content.replace(turkish, target)
        else:
            print(f"  WARNING: Not found: {turkish[:80]}...")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Translated: {filepath}")

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'

    # Select translation map
    if lang == 'it':
        trans = IT_TRANSLATIONS

    for f in ['index.html', 'contact.html', 'parameters.html']:
        filepath = os.path.join(BASE, lang, f)
        if os.path.exists(filepath):
            translate_file(filepath, trans)

    print(f"\n{lang} translation complete!")

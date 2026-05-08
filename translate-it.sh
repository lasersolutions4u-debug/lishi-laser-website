#!/bin/bash
# Translate Italian pages from Turkish to Italian
BASE="/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public/it"

for f in index.html contact.html parameters.html; do
  FILE="$BASE/$f"

  # === Meta & Head ===
  sed -i '' 's|12KW-60KW lazer kesim makineleri için LISHI LASER Karma Gaz Cihazı. 3 kat daha hızlı kesim, sıfır çapak, %33 daha az gaz tüketimi. Karbon çeliği kesimi için N2/O2 oran teknolojisi.|Dispositivo a gas misto LISHI LASER per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di consumo gas in meno. Tecnologia a rapporto N2/O2 per taglio acciaio al carbonio.|' "$FILE"

  sed -i '' 's|lazer kesim gaz karıştırıcı, nitrojen oksijen karışım cihazı, mikro oksijen lazer kesim, karbon çeliği lazer kesim, yüksek güçlü lazer 12kW 60kW, karma gaz vs hava kompresörü, lazer kesim çapaklarını giderme, nitrojen tüketimini azaltma, Han'\''s lazer gaz karıştırıcı, endüstriyel lazer gaz ekipmanı, bire-iki lazer gaz kurulumu, yardımcı gaz optimizasyonu|miscelatore gas taglio laser, dispositivo miscelazione azoto ossigeno, taglio laser micro ossigeno, taglio laser acciaio carbonio, laser alta potenza 12kW 60kW, gas misto vs compressore aria, eliminazione bave taglio laser, riduzione consumo azoto, miscelatore gas laser Han'\''s, apparecchiatura gas laser industriale, configurazione gas laser uno-a-due, ottimizzazione gas assistito|' "$FILE"

  sed -i '' 's|LISHI LASER Karma Gaz Cihazı |3× Daha Hızlı Lazer Kesim|LISHI LASER Dispositivo a Gas Misto | Taglio Laser 3× Più Veloce|' "$FILE"

  sed -i '' 's|12KW-60KW lazer kesim makineleri için karma gaz cihazı. 3× daha hızlı kesim, sıfır çapak, %33 daha az gaz tüketimi. N2/O2 oran teknolojisi.|Dispositivo a gas misto per macchine da taglio laser 12KW-60KW. Taglio 3× più veloce, zero bave, 33% di consumo gas in meno. Tecnologia a rapporto N2/O2.|' "$FILE"

  # === JSON-LD ===
  sed -i '' 's|"name": "LISHI LASER Karma Gaz Cihazı"|"name": "LISHI LASER Dispositivo a Gas Misto"|g' "$FILE"

  sed -i '' 's|"description": "Yüksek güçlü lazer kesim makineleri için nitrojen oksijen karma gaz ekipmanı. 3 kat daha hızlı kesim, sıfır çapak, %33 daha az gaz tüketimi."|"description": "Apparecchiatura a gas misto azoto-ossigeno per macchine da taglio laser ad alta potenza. Taglio 3× più veloce, zero bave, 33% di consumo gas in meno."|' "$FILE"

  sed -i '' 's|"Endüstriyel Üretim > Lazer Kesim Ekipmanı"|"Produzione Industriale > Apparecchiatura Taglio Laser"|' "$FILE"

  sed -i '' 's|"Karma gaz cihazı nedir ve nasıl çalışır?"|"Cos'\''è un dispositivo a gas misto e come funziona?"|' "$FILE"

  sed -i '' 's|"Karma gaz cihazı, sıvı nitrojen (N₂) ve sıvı oksijeni (O₂) hassas bir şekilde kalibre edilmiş N₂\/O₂ gaz karışımına (tipik olarak %95\/%5) dönüştürür. Bu mikro-oksijen karışımı, yüksek güçlü lazer kesimde yardımcı gaz olarak kullanılır ve saf oksijene kıyasla karbon çeliğinde 3× daha hızlı kesim hızı sağlarken çapakları tamamen ortadan kaldırır."|"Il dispositivo a gas misto converte azoto liquido (N₂) e ossigeno liquido (O₂) in una miscela di gas N₂\/O₂ precisamente calibrata (tipicamente 95%\/5%). Questa miscela micro-ossigeno viene utilizzata come gas assistito nel taglio laser ad alta potenza, offrendo una velocità di taglio 3× superiore rispetto all'\''ossigeno puro su acciaio al carbonio ed eliminando completamente le bave."|' "$FILE"

  sed -i '' 's|"Lazer makinemle uyumlu mu?"|"È compatibile con la mia macchina laser?"|' "$FILE"

  sed -i '' 's|"Evet. LISHI LASER Karma Gaz Cihazı, HAN'\''S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA ve MESSER dahil tüm büyük lazer markalarıyla çalışır. 12kW'\''dan 60kW'\''a kadar makineleri destekler. Makineniz standart yardımcı gaz bağlantıları kullanıyorsa uyumludur."|"Sì. Il Dispositivo a Gas Misto LISHI LASER funziona con tutti i principali marchi laser, inclusi HAN'\''S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA e MESSER. Supporta macchine da 12kW a 60kW. Se la tua macchina utilizza connessioni standard per gas assistito, è compatibile."|' "$FILE"

  sed -i '' 's|"Hangi kalınlıkları kesebilir?"|"Quali spessori può tagliare?"|' "$FILE"

  sed -i '' 's|"Karma gaz cihazı 1mm'\''den 30mm'\''ye kadar karbon çeliği, paslanmaz çeliği ve alüminyumu kesebilir. Kesim kalınlığı lazer gücünüze bağlıdır. Aşağıdaki parametreler sayfamızda ayrıntılı kesim parametreleri tabloları mevcuttur."|"Il dispositivo a gas misto può tagliare acciaio al carbonio, acciaio inossidabile e alluminio da 1mm a 30mm. Lo spessore di taglio dipende dalla potenza del laser. Tabelle dettagliate dei parametri di taglio sono disponibili nella nostra pagina parametri qui sotto."|' "$FILE"

  sed -i '' 's|"Gerçekten çapakları ortadan kaldırıyor mu?"|"Elimina davvero le bave?"|' "$FILE"

  sed -i '' 's|"Evet. Azot\/oksijen karışımındaki kontrollü mikro-oksijen içeriği, saf oksijen veya hava kesiminde oluşan aşırı oksidasyon olmadan tam yanmayı sağlar. Sonuç: ek zımpara veya taşlama gerektirmeyen temiz, çapaksız kenarlar."|"Sì. Il contenuto controllato di micro-ossigeno nella miscela azoto\/ossigeno consente una combustione completa senza l'\''eccessiva ossidazione che si verifica con ossigeno puro o taglio ad aria. Il risultato: bordi puliti e senza bave che non richiedono ulteriore levigatura o molatura."|' "$FILE"

  sed -i '' 's|"Karma gaz cihazı ne kadar gaz tasarrufu sağlar?"|"Quanto gas fa risparmiare il dispositivo a gas misto?"|' "$FILE"

  sed -i '' 's|"Tipik olarak saf nitrojen kesimine kıyasla nitrojen tüketimini yaklaşık %33 azaltır. Azot ve oksijen arasındaki optimize edilmiş karışım oranı, daha az toplam gaz hacmi ile daha verimli kesim sağlar."|"In genere riduce il consumo di azoto di circa il 33% rispetto al taglio con azoto puro. Il rapporto di miscelazione ottimizzato tra azoto e ossigeno consente un taglio più efficiente con un volume totale di gas inferiore."|' "$FILE"

  sed -i '' 's|"Kurulumu ve bakımı zor mu?"|"È difficile da installare e mantenere?"|' "$FILE"

  sed -i '' 's|"Kurulumu basittir — mevcut lazer makinenize bağlanan kompakt bir ünitedir. Bakım minimumdur: sadece 2kWh\/24h güç tüketimi ve yıllık temel kontrol. Hareketli parça yoktur, bu nedenle aşınma veya sık servis gerektirmez."|"L'\''installazione è semplice — un'\''unità compatta che si collega alla tua macchina laser esistente. La manutenzione è minima: solo 2kWh\/24h di consumo energetico e un controllo di base annuale. Nessuna parte mobile, quindi nessuna usura o necessità di assistenza frequente."|' "$FILE"

  sed -i '' 's|"Garantili mi?"|"È garantito?"|' "$FILE"

  sed -i '' 's|"Evet, tüm LISHI LASER Karma Gaz Cihazları, satın alma tarihinden itibaren 1 yıl garanti kapsamındadır. Küresel satış sonrası destek ağımız aracılığıyla uzatılmış garanti seçenekleri mevcuttur."|"Sì, tutti i Dispositivi a Gas Misto LISHI LASER sono coperti da una garanzia di 1 anno dalla data di acquisto. Opzioni di garanzia estesa sono disponibili attraverso la nostra rete globale di assistenza post-vendita."|' "$FILE"

  # === Video descriptions ===
  sed -i '' 's|"LISHI LASER Karma Gaz Cihazı 20KW lazer kesim makinesi ile çalışırken"|"Dispositivo a Gas Misto LISHI LASER in funzione con macchina da taglio laser 20KW"|g' "$FILE"
  sed -i '' 's|"Karma gaz cihazı karbon çeliği keserken"|"Dispositivo a gas misto per taglio acciaio al carbonio"|g' "$FILE"
  sed -i '' 's|"Karma gaz cihazı demo videosu"|"Video dimostrativo dispositivo a gas misto"|g' "$FILE"
  sed -i '' 's|"Karma gaz cihazı çalışma prensibi"|"Principio di funzionamento dispositivo a gas misto"|g' "$FILE"
  sed -i '' 's|"Karma gaz cihazı kurulumu"|"Installazione dispositivo a gas misto"|g' "$FILE"

  # === META (contact.html specific) ===
  sed -i '' 's|LISHI LASER karma gaz cihazı fiyatlandırması ve teklifleri için iletişime geçin|Contatta per prezzi e offerte dispositivo a gas misto LISHI LASER|' "$FILE"
  sed -i '' 's|Tüm büyük lazer markalarıyla uyumlu|Compatibile con tutti i principali marchi laser|g' "$FILE"
  sed -i '' 's|Global sevkiyat mevcuttur|Spedizione globale disponibile|g' "$FILE"
  sed -i '' 's|lazer kesim gaz ekipmanı teklifi|offerta apparecchiatura gas taglio laser|' "$FILE"
  sed -i '' 's|karma gaz cihazı distribütörü|distributore dispositivo gas misto|' "$FILE"
  sed -i '' 's|lazer kesim ekipmanı üreticisi|produttore apparecchiatura taglio laser|' "$FILE"
  sed -i '' 's|HANS lazer uyumlu gaz|gas compatibile laser HANS|' "$FILE"
  sed -i '' 's|LISHI LASER karma gaz kesim ekipmanı için teklif isteyin|Richiedi un preventivo per apparecchiatura taglio gas misto LISHI LASER|' "$FILE"
  sed -i '' 's|Tüm büyük lazer markalarıyla uyumlu. Global sevkiyat mevcuttur.|Compatibile con tutti i principali marchi laser. Spedizione globale disponibile.|' "$FILE"

  # === Navigation ===
  sed -i '' 's|>Ana Sayfa<|>Home<|g' "$FILE"
  sed -i '' 's|>Çalışma Prensibi<|>Principio<|g' "$FILE"
  sed -i '' 's|>Avantajlar<|>Vantaggi<|g' "$FILE"
  sed -i '' 's|>Parametreler<|>Parametri<|g' "$FILE"
  sed -i '' 's|>Numuneler<|>Campioni<|g' "$FILE"
  sed -i '' 's|>Müşteriler<|>Clienti<|g' "$FILE"
  sed -i '' 's|>Blog<|>Blog<|g' "$FILE"
  sed -i '' 's|>İletişim<|>Contatto<|g' "$FILE"

  # === Footer ===
  sed -i '' 's|>Ürün<|>Prodotto<|' "$FILE"
  sed -i '' 's|>Nasıl Çalışır<|>Come Funziona<|' "$FILE"
  sed -i '' 's|>Kesim Numuneleri<|>Campioni di Taglio<|' "$FILE"
  sed -i '' 's|>İletişim<|>Contatto<|' "$FILE"

  # === Contact page specific ===
  sed -i '' 's|>Bize Ulaşın<|>Contattaci<|' "$FILE"
  sed -i '' 's|Kesim hızınızı artırmaya hazır mısınız?|Pronto ad aumentare la tua velocità di taglio?|' "$FILE"
  sed -i '' 's|Lazer makinenizin detaylarını gönderin, size özel parametreler ve fiyatlandırma sunalım.|Invia i dettagli della tua macchina laser e ti forniremo parametri e prezzi personalizzati.|' "$FILE"
  sed -i '' 's|>E-posta<|>Email<|' "$FILE"
  sed -i '' 's|24 saat içinde yanıt|Risposta entro 24 ore|' "$FILE"
  sed -i '' 's|>Telefon / WeChat<|>Telefono / WeChat<|' "$FILE"
  sed -i '' 's|WeChat: aynı numara|WeChat: stesso numero|' "$FILE"
  sed -i '' 's|>Şirket<|>Azienda<|' "$FILE"
  sed -i '' 's|>Ürün Markası<|>Marchio Prodotto<|' "$FILE"
  sed -i '' 's|Karma Gaz Cihazı — Lazer kesim sektöründe 13 yıl|Dispositivo a Gas Misto — 13 anni nel settore taglio laser|' "$FILE"
  sed -i '' 's|Distribütör mü arıyorsunuz?|Cerchi un distributore?|' "$FILE"
  sed -i '' 's|Global acente ağımızı aktif olarak genişletiyoruz. Nitelikli distribütörler için özel bölgeler mevcuttur.|Stiamo espandendo attivamente la nostra rete globale di agenti. Territori esclusivi disponibili per distributori qualificati.|' "$FILE"
  sed -i '' 's|Acentelik Başvurusu →|Richiesta Distributore →|' "$FILE"
  sed -i '' 's|>Bize Mesaj Gönderin<|>Inviaci un Messaggio<|' "$FILE"
  sed -i '' 's|Ad Soyad \*|Nome e Cognome *|' "$FILE"
  sed -i '' 's|Ahmet Yılmaz|Mario Rossi|' "$FILE"
  sed -i '' 's|>E-posta \*<|>Email *<|' "$FILE"
  sed -i '' 's|Telefon / WhatsApp|Telefono / WhatsApp|' "$FILE"
  sed -i '' 's|>Ülke<|>Paese<|' "$FILE"
  sed -i '' 's|örn. Türkiye, Almanya, Polonya|es. Italia, Germania, Francia|' "$FILE"
  sed -i '' 's|>Talep Türü<|>Tipo di Richiesta<|' "$FILE"
  sed -i '' 's|>Seçiniz...<|>Seleziona...<|' "$FILE"
  sed -i '' 's|>Fiyatlandırma ve Teklif<|>Prezzi e Preventivo<|' "$FILE"
  sed -i '' 's|>Teknik Parametreler<|>Parametri Tecnici<|' "$FILE"
  sed -i '' 's|>Distribütör / Acente<|>Distributore / Agente<|' "$FILE"
  sed -i '' 's|>OEM / Özelleştirme<|>OEM / Personalizzazione<|' "$FILE"
  sed -i '' 's|>Diğer<|>Altro<|' "$FILE"
  sed -i '' 's|>Lazer Makinesi Gücü<|>Potenza Macchina Laser<|' "$FILE"
  sed -i '' 's|>Lazer gücü seçiniz...<|>Seleziona potenza laser...<|' "$FILE"
  sed -i '' 's|>Diğer / Birden Fazla<|>Altro / Multiplo<|' "$FILE"
  sed -i '' 's|>Lazer Makinesi Markası<|>Marca Macchina Laser<|' "$FILE"
  sed -i '' 's|>Mesaj \*<|>Messaggio *<|' "$FILE"
  sed -i '' 's|Kesim ihtiyaçlarınızı belirtin — malzeme türü, kalınlık, mevcut gaz kurulumu, vb.|Descrivi le tue esigenze di taglio — tipo materiale, spessore, configurazione gas attuale, ecc.|' "$FILE"
  sed -i '' 's|>Mesaj Gönder →<|>Invia Messaggio →<|' "$FILE"
  sed -i '' 's|Veya daha hızlı yanıt için doğrudan|O per una risposta più rapida, contatta direttamente via|' "$FILE"
  sed -i '' 's|ile iletişime geçin.|. |' "$FILE"
  sed -i '' 's|>Mesajınız Başarıyla Gönderildi!<|>Messaggio Inviato con Successo!<|' "$FILE"
  sed -i '' 's|Talebiniz için teşekkür ederiz. 24 saat içinde yanıt vereceğiz.|Grazie per la tua richiesta. Ti risponderemo entro 24 ore.|' "$FILE"
  sed -i '' 's|>Ana Sayfaya Dön<|>Torna alla Home<|' "$FILE"

  # === Parameters page specific ===
  sed -i '' 's|>Kesim Parametreleri<|>Parametri di Taglio<|' "$FILE"
  sed -i '' 's|Aşağıda farklı lazer güçleri için ayrıntılı kesim parametreleri|Di seguito i parametri di taglio dettagliati per diverse potenze laser|' "$FILE"
  sed -i '' 's|Kalınlık|Spessore|g' "$FILE"
  sed -i '' 's|Karma Gaz Hızı|Velocità Gas Misto|g' "$FILE"
  sed -i '' 's|Hız Artışı|Aumento Velocità|g' "$FILE"
  sed -i '' 's|Test Konumu|Luogo Test|g' "$FILE"
  sed -i '' 's|Notlar|Note|g' "$FILE"
  sed -i '' 's|Karma Gaz Optimizasyonu|Ottimizzazione Gas Misto|' "$FILE"
  sed -i '' 's|Gaz Tüketim Karşılaştırması|Confronto Consumo Gas|' "$FILE"
  sed -i '' 's|Saf Azot|Azoto Puro|g' "$FILE"
  sed -i '' 's|Karma Gaz|Gas Misto|g' "$FILE"
  sed -i '' 's|Tasarruf|Risparmio|g' "$FILE"
  sed -i '' 's|saatte|all'\''ora|g' "$FILE"
  sed -i '' 's|günde|al giorno|g' "$FILE"
  sed -i '' 's|ayda|al mese|g' "$FILE"
  sed -i '' 's|yılda|all'\''anno|g' "$FILE"
  sed -i '' 's|>Parametreleri İndir<|>Scarica Parametri<|' "$FILE"
  sed -i '' 's|>Teknik Destek Alın<|>Ottieni Supporto Tecnico<|' "$FILE"

  # === Index page specific ===
  sed -i '' 's|Karma Gaz Teknolojisi ile 3× Daha Hızlı Kesin|Taglia 3× Più Veloce con la Tecnologia a Gas Misto|' "$FILE"
  sed -i '' 's|12KW-60KW lazer kesim makineleri için N₂\/O₂ karma gaz çözümü|Soluzione gas misto N₂\/O₂ per macchine da taglio laser 12KW-60KW|' "$FILE"
  sed -i '' 's|>Teklif Alın<|>Richiedi Preventivo<|' "$FILE"
  sed -i '' 's|>Nasıl Çalışır →<|>Come Funziona →<|' "$FILE"

  sed -i '' 's|>Karma Gaz Cihazı Nedir?<|>Cos'\''è un Dispositivo a Gas Misto?<|' "$FILE"
  sed -i '' 's|Karma gaz cihazı, yüksek saflıkta sıvı nitrojen \(N₂\) ve sıvı oksijeni \(O₂\) hassas IGBT kontrollü karıştırma teknolojisi ile birleştirir.|Il dispositivo a gas misto combina azoto liquido (N₂) e ossigeno liquido (O₂) ad alta purezza tramite tecnologia di miscelazione a controllo IGBT di precisione.|' "$FILE"
  sed -i '' 's|Sonuç, karbon çeliği kesiminde saf oksijenden 3 kat daha hızlı, saf azottan çok daha ekonomik bir yardımcı gazdır.|Il risultato è un gas assistito 3 volte più veloce dell'\''ossigeno puro per il taglio dell'\''acciaio al carbonio, e molto più economico dell'\''azoto puro.|' "$FILE"
  sed -i '' 's|>Video İzleyin<|>Guarda Video<|' "$FILE"

  sed -i '' 's|>Neden O₂, N₂ veya Hava Yerine Karma Gaz?<|>Perché Gas Misto invece di O₂, N₂ o Aria?<|' "$FILE"
  sed -i '' 's|>Kesim Hızı<|>Velocità di Taglio<|g' "$FILE"
  sed -i '' 's|>Kenar Kalitesi<|>Qualità del Bordo<|g' "$FILE"
  sed -i '' 's|>Gaz Maliyeti<|>Costo del Gas<|g' "$FILE"
  sed -i '' 's|>Bakım<|>Manutenzione<|g' "$FILE"
  sed -i '' 's|>Uyumluluk<|>Compatibilità<|g' "$FILE"
  sed -i '' 's|Saf Oksijen \(O₂\)|Ossigeno Puro (O₂)|g' "$FILE"
  sed -i '' 's|Saf Azot \(N₂\)|Azoto Puro (N₂)|g' "$FILE"
  sed -i '' 's|Hava \(Kompresör\)|Aria (Compressore)|g' "$FILE"
  sed -i '' 's|Karma Gaz \(N₂\/O₂\)|Gas Misto (N₂/O₂)|g' "$FILE"
  sed -i '' 's|Çapaklı kenarlar|Bordi con bave|g' "$FILE"
  sed -i '' 's|Mükemmel pürüzsüz|Perfettamente liscio|g' "$FILE"
  sed -i '' 's|Düşük kalite|Bassa qualità|g' "$FILE"
  sed -i '' 's|Çok yüksek|Molto alto|g' "$FILE"
  sed -i '' 's|Düşük \(~%33 tasarruf\)|Basso (~33% risparmio)|g' "$FILE"
  sed -i '' 's|Sık temizlik gerekir|Pulizia frequente richiesta|g' "$FILE"
  sed -i '' 's|Minimal|Minimo|g' "$FILE"
  sed -i '' 's|Kompresör bakımı|Manutenzione compressore|g' "$FILE"
  sed -i '' 's|>ROI Hesaplayıcı<|>Calcolatore ROI<|' "$FILE"
  sed -i '' 's|>Makine Gücü<|>Potenza Macchina<|' "$FILE"
  sed -i '' 's|>Malzeme Kalınlığı<|>Spessore Materiale<|' "$FILE"
  sed -i '' 's|>Günlük Çalışma Saati<|>Ore Lavorative Giornaliere<|' "$FILE"
  sed -i '' 's|>Gaz Maliyeti \(\/m³\)<|>Costo Gas (\/m³)|' "$FILE"
  sed -i '' 's|>Hesapla<|>Calcola<|' "$FILE"
  sed -i '' 's|>Yıllık Tahmini Tasarruf<|>Risparmio Annuo Stimato<|' "$FILE"
  sed -i '' 's|>Yatırım Geri Dönüş Süresi<|>Periodo di Recupero Investimento<|' "$FILE"
  sed -i '' 's|>ay<|>mesi<|' "$FILE"
  sed -i '' 's|Hava Kompresörü ve Karma Gaz Karşılaştırması|Confronto Compressore d'\''Aria e Gas Misto|' "$FILE"
  sed -i '' 's|>Yüksek Bakım Maliyeti<|>Costo Manutenzione Elevato<|' "$FILE"
  sed -i '' 's|>Düşük Kesim Kalitesi<|>Qualità Taglio Scarsa<|' "$FILE"
  sed -i '' 's|>Lens Kontaminasyonu<|>Contaminazione Lenti<|' "$FILE"
  sed -i '' 's|>Enerji Tüketimi<|>Consumo Energetico<|' "$FILE"
  sed -i '' 's|>Gürültü<|>Rumore<|' "$FILE"
  sed -i '' 's|Hava kompresörü sistemleri|I sistemi con compressore d'\''aria|' "$FILE"
  sed -i '' 's|Karma gaz cihazı yalnızca 2kWh\/24h tüketir|Il dispositivo a gas misto consuma solo 2kWh\/24h|' "$FILE"

  sed -i '' 's|>Güce Göre Kesim Parametreleri<|>Parametri di Taglio per Potenza<|' "$FILE"
  sed -i '' 's|>Detaylı Parametreler →<|>Parametri Dettagliati →<|' "$FILE"

  sed -i '' 's|>Kesim Numuneleri<|>Campioni di Taglio<|' "$FILE"
  sed -i '' 's|>Gerçek müşteri kesim sonuçları<|>Risultati reali di taglio dei clienti<|' "$FILE"

  sed -i '' 's|>KÜRESEL AĞ<|>RETE GLOBALE<|' "$FILE"
  sed -i '' 's|>Asya<|>Asia<|g' "$FILE"
  sed -i '' 's|>Avrupa<|>Europa<|g' "$FILE"
  sed -i '' 's|>Amerika<|>Americhe<|g' "$FILE"
  sed -i '' 's|>Afrika<|>Africa<|g' "$FILE"
  sed -i '' 's|>Okyanusya<|>Oceania<|g' "$FILE"
  sed -i '' 's|>50+<|>50+<|g' "$FILE"
  sed -i '' 's|>Ülke<|>Paesi<|g' "$FILE"
  sed -i '' 's|>500+<|>500+<|g' "$FILE"
  sed -i '' 's|>Kurulu Sistem<|>Sistemi Installati<|g' "$FILE"
  sed -i '' 's|>Müşteri<|>Clienti<|g' "$FILE"
  sed -i '' 's|>Distribütör<|>Distributori<|g' "$FILE"
  sed -i '' 's|>Küresel Satış Sonrası Destek<|>Supporto Post-Vendita Globale<|' "$FILE"

  sed -i '' 's|>Sıkça Sorulan Sorular<|>Domande Frequenti<|' "$FILE"

  sed -i '' 's|Kesim hızınızı bugün artırın!<|Aumenta la tua velocità di taglio oggi!|' "$FILE"
  sed -i '' 's|Hemen bizimle iletişime geçin, size özel çözüm ve fiyatlandırma sunalım.|Contattaci subito per una soluzione e un preventivo personalizzati.|' "$FILE"
  sed -i '' 's|>Hemen İletişime Geçin<|>Contattaci Ora<|g' "$FILE"
  sed -i '' 's|>Ücretsiz Danışmanlık Alın<|>Ottieni Consulenza Gratuita<|' "$FILE"

  # Footer
  sed -i '' 's|Marka Lisanslı Yurtdışı Pazar Operasyon Acentesi:|Agente Autorizzato Operazioni Mercato Estero:|' "$FILE"
  sed -i '' 's|Tüm hakları saklıdır.|Tutti i diritti riservati.|' "$FILE"
  sed -i '' 's|Gaz Karışım Teknolojisi|Tecnologia Miscelazione Gas|' "$FILE"

  # Breadcrumb
  sed -i '' 's|"name": "Ana Sayfa"|"name": "Home"|g' "$FILE"
  sed -i '' 's|"name": "İletişim"|"name": "Contatto"|' "$FILE"
  sed -i '' 's|"name": "Kesim Parametreleri"|"name": "Parametri di Taglio"|' "$FILE"

  # ContactPage JSON-LD
  sed -i '' 's|"name": "LISHI LASER İletişim"|"name": "LISHI LASER Contatto"|' "$FILE"

  # section labels
  sed -i '' 's|>İletişime Geçin<|>Mettiti in Contatto<|' "$FILE"
  sed -i '' 's|>Ürün<|>Prodotto<|' "$FILE"

done

echo "Italian translation complete"
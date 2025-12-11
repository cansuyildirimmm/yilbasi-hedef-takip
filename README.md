# 🎯 Yılbaşı Hedef Takip ve Kontrol Paneli Uygulaması 
<img width="1900" height="646" alt="Ekran görüntüsü 2025-12-11 235203" src="https://github.com/user-attachments/assets/f2e851b7-e51b-4045-96a2-3eceab43c4db" />

<img width="1887" height="556" alt="Ekran görüntüsü 2025-12-12 000551" src="https://github.com/user-attachments/assets/7b29fd09-5400-46e4-b70f-54a3e16967c6" />

<img width="1877" height="860" alt="Ekran görüntüsü 2025-12-12 000620" src="https://github.com/user-attachments/assets/2ac71390-d72c-4859-be03-d1932022eb8f" />

Bu uygulama, kullanıcıların yeni yıla motive bir başlangıç yapmalarını sağlamak amacıyla geliştirilmiş kişiselleştirilmiş bir hedef takip platformudur.

Kullanıcılar, bu web uygulaması aracılığıyla:
1. Yılbaşına kalan süreyi canlı olarak takip edebilir.
2. Bu sene **gerçekleştirdikleri başarıları** kaydedebilir (Yıl Sonu Özeti).
3. Gelecek **Yeni Yıl (2026) hedeflerini** belirleyip kaydedebilir.
4. Kayıtlı verilerine sadece kendi özel kontrol panellerinden erişebilirler.

## 🚀 Kullanılan Teknolojiler

Bu proje, Python tabanlı bir full-stack (tam yığın) mimari kullanılarak geliştirilmiştir.

| Alan | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Backend (Arka Yüz)** | Python, Flask | Hafif ve hızlı web çatısı (framework). |
| **Veritabanı (Database)** | SQLite | Kullanıcı ve hedef verilerini saklamak için basit ve dosya tabanlı bir veritabanı. |
| **Yetkilendirme (Auth)** | Flask-Login, Werkzeug | Güvenli kullanıcı oturumu ve şifre hash'leme. |
| **Frontend (Ön Yüz)** | HTML5, CSS3 | Duyarlı tasarım ve şık, yılbaşı temalı görsel efektler (CSS Shimmer/Parıltı). |
| **Sürüm Kontrolü** | Git & GitHub | Proje geçmişini yönetmek için. |

### Depoyu Klonlama

Projeyi GitHub'dan yerel makinenize indirin:

```bash
git clone [https://github.com/cansuyildirimmm/yilbasi-hedef-takip.git](https://github.com/cansuyildirimmm/yilbasi-hedef-takip.git)
cd yilbasi-hedef-takip

# Sanal ortamı oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin (Windows PowerShell)
.\venv\Scripts\Activate

# Gerekli kütüphaneleri kurun
pip install Flask Flask-SQLAlchemy Flask-Login werkzeug

# Veritabanı otomatik olarak oluşturulacak ve uygulama yerel sunucuda başlayacaktır.
python app.py

# Uygulama çalıştıktan sonra, tarayıcınızdan aşağıdaki adrese gidin:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)


# HALLET-TV

**Otonom yapay zekâ televizyonu**

HALLET-TV; yayın oynatma, içerik yönetimi, yapay zekâ destekli sunum ve operasyon süreçleri için geliştirilen ayrı bir projedir. Ana HALLET uygulamasından bağımsız sürüm kontrolü altında tutulur.

## Durum

- Sürüm hedefi: `6.12.1`
- Aktif teknik odak: HLS oynatma yaşam döngüsü, hata sonrası yeniden bağlanma, sürüm/paket bütünlüğü ve üretim öncesi doğrulama.
- Son release-gate notu: [HLS Release Gate Revalidation — 2026-10-29](docs/HLS-RELEASE-GATE-REVALIDATION-2026-10-29.md)
- Test kapsamı ve operasyon notları, doğrulama raporlarında ayrı ayrı belirtilir.

## Önemli yayın notu

Otomatik testlerin geçmesi tek başına gerçek canlı yayın veya üretim hazırlığını kanıtlamaz. Gerçek HLS kaynağıyla tarayıcı uçtan uca testi, üretim ortamı değişkenlerinin kontrolü ve yayın gözlemi tamamlanmadan sürüm “canlı yayına hazır” olarak işaretlenmemelidir.

## Güvenlik

- Gerçek erişim anahtarları, OAuth sırları, yayın anahtarları ve üretim `.env` dosyaları Git'e eklenmemelidir.
- Örnek ortam değişkenleri yalnızca sahte/boş değerler içermelidir.
- Üretim dağıtımı ve harici yayın başlatma, ayrıca doğrulanması gereken ayrı işlemlerdir.

# stringtr

stringtr, Python'ın standart string modülüne benzeyen, ancak Türkçe karakterleri ve Türkçe dil yapısına özgü harf sınıflandırmalarını içeren bir Python kütüphanesidir. ASCII karakter setleri elle tanımlanmıştır ve harici bir kütüphane bağımlılığı yoktur.

## Özellikler

**Temel Karakter Setleri (ASCII Tabanlı + Türkçe):**
- `stringtr.lowercase`: Tüm küçük harfler (ASCII + çğışıöü)
- `stringtr.uppercase`: Tüm büyük harfler (ASCII + ÇĞİŞİÖÜ)
- `stringtr.letters`: Tüm harfler (küçük + büyük, ASCII + Türkçe)
- `stringtr.digits`: Rakamlar (0–9)
- `stringtr.hexdigits`: Onaltılık (0–9, a–f, A–F)
- `stringtr.octdigits`: Sekizlik (0–7)
- `stringtr.punctuation`: ASCII noktalama (!”#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
- `stringtr.whitespace`: Boşluk karakterleri (spacer, tab, newline vb.)
- `stringtr.printable`: Yazdırılabilir tüm karakterler

**Türkçe'ye Özgü Karakter Setleri:**
- `stringtr.turkcekarakterler`: Sadece Türkçe harfler (ÇçĞğIıİiÖöŞşÜü)
- `stringtr.kalin_unluler`: Kalın ünlüler (aıouAIOU)
- `stringtr.ince_unluler`: İnce ünlüler (eıöüEİÖÜ)
- `stringtr.duz_unluler`: Düz ünlüler (aeıi)
- `stringtr.yuvarlak_unluler`: Yuvarlak ünlüler (oöuü)
- `stringtr.sert_unsuzler`: Sert ünsüzler (f s t k ç ş h p)
- `stringtr.yumusak_unsuzler`: Yumuşak ünsüzler (b c d ğ j l m n r v y z)
- `stringtr.unluler`: Tüm ünlüler (küçük + büyük)
- `stringtr.unsuzler`: Tüm ünsüzler (küçük + büyük)
- `stringtr.unluler_kucuk`: Küçük ünlüler
- `stringtr.unluler_buyuk`: Büyük ünlüler
- `stringtr.unsuzler_kucuk`: Küçük ünsüzler
- `stringtr.unsuzler_buyuk`: Büyük ünsüzler

## Örnek Veri

- `stringtr.fisler`: İlkokul fişlerinde kullanılan örnek cümleler listesi.

## Kurulum

```bash
pip install stringtr
```

## Kullanım

```python
from stringtr import stringtr

# Küçük harfler
print(stringtr.lowercase)

# Sadece Türkçe karakterler
print(stringtr.turkcekarakterler)

# Kalın ünlüler
print(stringtr.kalin_unluler)

# Örnek fiş cümlesi
print(stringtr.fisler[0])

# Büyük ünsüzler
print(stringtr.unsuzler_buyuk)
```

## Geliştirme

```bash
git clone https://github.com/cagrigungor/stringtr.git
cd stringtr
pip install -e .[dev]
pytest
```

## Lisans

MIT Lisansı. Detaylar için [LICENSE](LICENSE).

## Yazar

**Hasan Çağrı Güngör**  
✉️ iletisim@cagrigungor.com  
🔗 https://github.com/cagrigungor/stringtr

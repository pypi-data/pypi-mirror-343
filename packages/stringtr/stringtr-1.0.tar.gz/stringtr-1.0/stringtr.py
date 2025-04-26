# Python'ın standart string modülüne benzeyen,
# ancak Türkçe karakterleri de içeren karakter setleri sunan sınıf.
# Standart ASCII setleri elle tanımlanmıştır.
class stringtr:
    """
    Python'ın standart string modülüne benzeyen,
    ancak Türkçe karakterleri de içeren karakter setleri sunar.
    Standart ASCII karakter setleri bu sınıf içinde elle tanımlanmıştır.

    Özellikler:
    - lowercase: Küçük harfler (ASCII İngilizce + Türkçe)
    - uppercase: Büyük harfler (ASCII İngilizce + Türkçe)
    - letters: Tüm harfler (küçük + büyük, ASCII İngilizce + Türkçe)
    - digits: Rakamlar (ASCII)
    - hexdigits: Onaltılık (hexadecimal) rakamlar (ASCII)
    - octdigits: Sekizlik (octal) rakamlar (ASCII)
    - punctuation: Noktalama işaretleri (ASCII)
    - printable: Yazdırılabilir tüm karakterler (ASCII + Türkçe harfler)
    - whitespace: Boşluk karakterleri (ASCII)
    - fisler: Temel Türkçe cümle örnekleri listesi
    - turkcekarakterler: Sadece Türkçe özel karakterler (ünlü ve ünsüz)
    - kalin_unluler: Kalın ünlü harfler (a, ı, o, u)
    - ince_unluler: İnce ünlü harfler (e, i, ö, ü)
    - duz_unluler: Düz ünlü harfler (a, e, ı, i)
    - yuvarlak_unluler: Yuvarlak ünlü harfler (o, ö, u, ü)
    - sert_unsuzler: Sert ünsüz harfler (f, s, t, k, ç, ş, h, p)
    - yumusak_unsuzler: Yumuşak ünsüz harfler (b, c, d, g, ğ, j, l, m, n, r, v, y, z)
    - unluler: Tüm ünlü harfler (kalın + ince, küçük + büyük)
    - unsuzler: Tüm ünsüz harfler (sert + yumuşak, küçük + büyük)
    - unluler_kucuk: Tüm küçük ünlü harfler
    - unluler_buyuk: Tüm büyük ünlü harfler
    - unsuzler_kucuk: Tüm küçük ünsüz harfler
    - unsuzler_buyuk: Tüm büyük ünsüz harfler
    """

    # ASCII Küçük harfler elle tanımlandı
    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'

    # ASCII Büyük harfler elle tanımlandı
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Rakamlar: 0'dan 9'a kadar (ASCII)
    digits = '0123456789'

    # Onaltılık (Hexadecimal) rakamlar: 0-9, a-f, A-F (ASCII)
    hexdigits = digits + 'abcdef' + 'ABCDEF'

    # Sekizlik (Octal) rakamlar: 0-7 (ASCII)
    octdigits = '01234567'

    # Noktalama işaretleri: Standart ASCII noktalama karakterleri elle tanımlandı
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    # Boşluk karakterleri: Boşluk, tab, satır başı vb. (ASCII)
    whitespace = ' \t\n\r\v\f'


    # Küçük harfler: ASCII İngilizce alfabesi + Türkçe özel küçük harfler, alfabetik sırada.
    # 'i' ve 'ı' harflerinin sıralamasına dikkat edilmiştir.
    lowercase = ''.join(sorted(ascii_lowercase + 'çğışiöü', key=lambda x: 'abcçdefgğhıijklmnoöprsştuüvyz'.index(x)))

    # Büyük harfler: ASCII İngilizce alfabesi + Türkçe özel büyük harfler, alfabetik sırada.
    # 'İ' ve 'I' harflerinin sıralamasına dikkat edilmiştir.
    uppercase = ''.join(sorted(ascii_uppercase + 'ÇĞİŞİÖÜ', key=lambda x: 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'.index(x)))

    # Tüm harfler: Küçük ve büyük harflerin birleşimi.
    letters = lowercase + uppercase

    # Tüm yazdırılabilir karakterler: Rakamlar, harfler, noktalama, boşluk.
    printable = digits + letters + punctuation + whitespace

    # Temel Türkçe cümle örnekleri listesi
    fisler = [
        "Ali Ata Bak.",
        "Ali Topu Tut.",
        "Ömer Mısır Sever.",
        "Işık Ilık Süt İç.",
        "Bak Ali Bak.",
        "Emel Gel Ata Bak.",
        "İpek İpi Tut.",
        "Bayram Geldi.",
        "Bayrak As.",
        "Fener As.",
        "Cumhuriyet Çok Yaşa.",
        "Emel Eve Gel.",
        "Emel Bal Al.",
        "İpek Topu At.",
        "Zil Çaldı.",
        "Oya Okula Koş.",
        "Kalem Al.",
        "Resim Yap.",
        "Ekin Voleybol Oynadı.",
        "Adile Yere Çöp Atma.",
        "Elif Ağaç Dikti.",
        "Jale Bu Jandarma.",
        "Ali Bak."
    ]

    # Sadece Türkçe özel karakterler (ünlü ve ünsüz), alfabetik sırada.
    turkce_ozel_kucuk = 'çğışiöü'
    turkce_ozel_buyuk = 'ÇĞİŞİÖÜ'
    turkcekarakterler = ''.join(sorted(turkce_ozel_kucuk + turkce_ozel_buyuk, key=lambda x: 'abcçdefgğhıijklmnoöprsştuüvyzABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'.index(x)))

    # Kalın ünlü harfler (küçük)
    kalin_unluler_kucuk = 'aıou'
    # İnce ünlü harfler (küçük)
    ince_unluler_kucuk = 'eiiöü'

    # Kalın ünlü harfler (büyük)
    kalin_unluler_buyuk = kalin_unluler_kucuk.upper() # AIOU
    # İnce ünlü harfler (büyük)
    ince_unluler_buyuk = ince_unluler_kucuk.upper() # EİİÖÜ

    # Tüm küçük ünlü harfler
    unluler_kucuk = ''.join(sorted(kalin_unluler_kucuk + ince_unluler_kucuk, key=lambda x: 'aıoueiiöü'.index(x)))

    # Tüm büyük ünlü harfler
    unluler_buyuk = ''.join(sorted(kalin_unluler_buyuk + ince_unluler_buyuk, key=lambda x: 'AIİOUÖÜ'.index(x)))

    # Tüm ünlü harfler (küçük + büyük)
    unluler = unluler_kucuk + unluler_buyuk

    # Sert ünsüz harfler (küçük) (fıstıkçı şahap)
    sert_unsuzler_kucuk = 'fstkçşhp'
    # Yumuşak ünsüz harfler (küçük) (geri kalanlar)
    yumusak_unsuzler_kucuk = 'bcdğjlmnrvyz'

    # Sert ünsüz harfler (büyük)
    sert_unsuzler_buyuk = sert_unsuzler_kucuk.upper() # FSTKÇŞHP
    # Yumuşak ünsüz harfler (büyük)
    yumusak_unsuzler_buyuk = yumusak_unsuzler_kucuk.upper() # BCDĞJLMNRVYZ

    # Tüm küçük ünsüz harfler
    unsuzler_kucuk = ''.join(sorted(sert_unsuzler_kucuk + yumusak_unsuzler_kucuk, key=lambda x: 'bcçdfgğhjklmnprsştvyz'.index(x)))

    # Tüm büyük ünsüz harfler
    unsuzler_buyuk = ''.join(sorted(sert_unsuzler_buyuk + yumusak_unsuzler_buyuk, key=lambda x: 'BCÇDFGĞHJKLMNPRSŞTVYZ'.index(x)))

    # Tüm ünsüz harfler (küçük + büyük)
    unsuzler = unsuzler_kucuk + unsuzler_buyuk


    # Kalın ünlü harfler (hem küçük hem büyük, karışık) - Eski özellikler uyumluluk için tutuldu
    kalin_unluler = kalin_unluler_kucuk + kalin_unluler_buyuk
    # İnce ünlü harfler (hem küçük hem büyük, karışık) - Eski özellikler uyumluluk için tutuldu
    ince_unluler = ince_unluler_kucuk + ince_unluler_buyuk


# Kullanım örnekleri:
# print("Türkçe Küçük Harfler:", stringtr.lowercase)
# print("Türkçe Büyük Harfler:", stringtr.uppercase)
# print("Tüm Türkçe Harfler:", stringtr.letters)
# print("Rakamlar:", stringtr.digits)
# print("Noktalama:", stringtr.punctuation)
# print("ASCII Küçük Harfler (Elle Tanımlı):", stringtr.ascii_lowercase)
# print("Örnek Cümleler:", stringtr.fisler)
# print("Sadece Türkçe Karakterler:", stringtr.turkcekarakterler)
# print("Kalın Ünlüler:", stringtr.kalin_unluler) # Hem küçük hem büyük içerir
# print("İnce Ünlüler:", stringtr.ince_unluler) # Hem küçük hem büyük içerir
# print("Düz Ünlüler:", stringtr.duz_unluler)
# print("Yuvarlak Ünlüler:", stringtr.yuvarlak_unluler)
# print("Sert Ünsüzler (Küçük):", stringtr.sert_unsuzler_kucuk)
# print("Yumuşak Ünsüzler (Küçük):", stringtr.yumusak_unsuzler_kucuk)
# print("Sert Ünsüzler (Büyük):", stringtr.sert_unsuzler_buyuk)
# print("Yumuşak Ünsüzler (Büyük):", stringtr.yumusak_unsuzler_buyuk)
# print("Tüm Ünlüler:", stringtr.unluler) # Hem küçük hem büyük içerir
# print("Tüm Ünsüzler:", stringtr.unsuzler) # Hem küçük hem büyük içerir
# print("Küçük Ünlüler:", stringtr.unluler_kucuk)
# print("Büyük Ünlüler:", stringtr.unluler_buyuk)
# print("Küçük Ünsüzler:", stringtr.unsuzler_kucuk)
# print("Büyük Ünsüzler:", stringtr.unsuzler_buyuk)

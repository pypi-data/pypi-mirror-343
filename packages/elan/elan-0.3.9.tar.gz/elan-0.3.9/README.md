# ElanLibs

**`Efekan Nefesoğlu` ve `Elanur Tuana İşcen` Tarafından Geliştirilmiştir**

## Giriş

Elan, günlük programlama görevlerini kolaylaştırmak için geliştirilmiş çok yönlü bir Python kütüphanesidir. Bu kütüphane, yaygın matematik işlemleri, liste manipülasyonları, string (metin) işleme ve temel görüntü işleme görevleri için kullanımı kolay ve anlaşılır bir arayüz sunar.

Elan kütüphanesi, kod tekrarını azaltmak ve proje geliştirme sürecini hızlandırmak için tasarlanmıştır. Tek bir tutarlı arayüz ile farklı tipteki işlemleri gerçekleştirebilirsiniz.

## Amaç

Elan'ın amacı, tekerleği yeniden icat etmek yerine, yaygın kullanılan işlevleri tek bir pakette toplayarak geliştirme sürecinizi hızlandırmaktır. Kütüphane şu alanlarda yardımcı fonksiyonlar sunar:

- Temel matematiksel işlemleri
- Liste manipülasyonları
- Metin işleme ve dönüştürme
- Görüntü işleme (gri tonlama, boyutlandırma, döndürme)

## Kurulum

Elan kütüphanesi PyPI üzerinden kolayca kurulabilir:

```bash
pip install elan
```

### Bağımlılıklar

Elan kütüphanesinin düzgün çalışması için aşağıdaki gereksinimler otomatik olarak kurulur:

- Python 3.6 veya üzeri
- OpenCV (görüntü işleme işlevleri için)

## Kullanım

Elan kütüphanesini kullanmak için öncelikle ana sınıfı içe aktarmanız ve bir örnek oluşturmanız gerekir:

```python
from elan import elan

# Elan sınıfını başlat
el = elan()
```

Bu örnek üzerinden tüm fonksiyonlara erişebilirsiniz.

## Türkçe Fonksiyon İsimleri

Elan kütüphanesi, İngilizce metot isimlerinin yanı sıra Türkçe metot isimleri de sunar. Bu özellik, Türkçe döküman ve öğrenim sürecinde kolaylık sağlamak amacıyla eklenmiştir. Ana modüller de Türkçe alternatiflerle erişilebilir:

```python
from elan import elan

# Elan sınıfını başlat
el = elan()

# İngilizce modül isimleri
result1 = el.math.add(5, 3)          # Sonuç: 8
result2 = el.string.reverse("Elan")  # Sonuç: "nalE"
result3 = el.list.reverse([1, 2, 3]) # Sonuç: [3, 2, 1]
result4 = el.image.resize("foto.jpg", 800, 600) # Resmi boyutlandırır

# Türkçe modül isimleri
sonuc1 = el.mat.topla(5, 3)          # Sonuç: 8
sonuc2 = el.yazi.tersine_cevir("Elan") # Sonuç: "nalE"
sonuc3 = el.dizi.tersine_cevir([1, 2, 3]) # Sonuç: [3, 2, 1]
sonuc4 = el.goruntu.yeniden_boyutlandir("foto.jpg", 800, 600) # Resmi boyutlandırır
```

### Matematiksel İşlevler

`math` modülü, temel matematiksel işlemler için kullanışlı fonksiyonlar sağlar:

```python
# Toplama işlemi
sonuc = el.math.add(5, 3)  # Sonuç: 8

# Çıkarma işlemi
sonuc = el.math.subtract(10, 4)  # Sonuç: 6

# Çarpma işlemi
sonuc = el.math.multiply(3, 5)  # Sonuç: 15

# Bölme işlemi
sonuc = el.math.divide(10, 2)  # Sonuç: 5.0

# Üs alma
sonuc = el.math.power(2, 3)  # Sonuç: 8 (2³)

# Karekök
sonuc = el.math.square_root(16)  # Sonuç: 4.0

# Küpkök
sonuc = el.math.cube_root(27)  # Sonuç: 3.0

# Kare
sonuc = el.math.square(4)  # Sonuç: 16

# Küp
sonuc = el.math.cube(3)  # Sonuç: 27

# Faktöriyel
sonuc = el.math.factorial(5)  # Sonuç: 120 (5! = 5×4×3×2×1)
```

#### Çoklu Sayı İşlemleri

`math` modülü ayrıca birden fazla sayı ile çalışmanızı sağlayan fonksiyonlar da sunar:

```python
# İstediğiniz kadar sayıyı toplama
sonuc = el.math.sum_all(1, 2, 3, 4, 5)  # Sonuç: 15

# İstediğiniz kadar sayıyı çarpma
sonuc = el.math.multiply_all(1, 2, 3, 4, 5)  # Sonuç: 120

# Sayıların ortalamasını alma
sonuc = el.math.average(1, 2, 3, 4, 5)  # Sonuç: 3.0

# En büyük değeri bulma
sonuc = el.math.max_value(1, 5, 3, 9, 2)  # Sonuç: 9

# En küçük değeri bulma
sonuc = el.math.min_value(1, 5, 3, 9, 2)  # Sonuç: 1

# En büyük ve en küçük değer arasındaki farkı bulma (aralık)
sonuc = el.math.range_value(1, 5, 3, 9, 2)  # Sonuç: 8

# Sayıların medyanını bulma
sonuc = el.math.median(1, 3, 5, 7, 9)  # Sonuç: 5
sonuc = el.math.median(1, 3, 5, 7)  # Sonuç: 4.0 (çift sayıda eleman olduğunda ortadaki iki sayının ortalaması)
```

### Matematiksel İşlevler (Türkçe)

`mat` modülü, `math` modülünün Türkçe alternatifidir:

```python
# Toplama işlemi
sonuc = el.mat.topla(5, 3)  # Sonuç: 8

# Çıkarma işlemi
sonuc = el.mat.cikar(10, 4)  # Sonuç: 6

# Çarpma işlemi
sonuc = el.mat.carp(3, 5)  # Sonuç: 15

# Bölme işlemi
sonuc = el.mat.bol(10, 2)  # Sonuç: 5.0

# Üs alma
sonuc = el.mat.us(2, 3)  # Sonuç: 8 (2³)

# Karekök
sonuc = el.mat.karekok(16)  # Sonuç: 4.0

# Küpkök
sonuc = el.mat.kupkok(27)  # Sonuç: 3.0

# Kare
sonuc = el.mat.kare(4)  # Sonuç: 16

# Küp
sonuc = el.mat.kup(3)  # Sonuç: 27

# Faktöriyel
sonuc = el.mat.faktoriyel(5)  # Sonuç: 120 (5! = 5×4×3×2×1)

# İstediğiniz kadar sayıyı toplama
sonuc = el.mat.tumunu_topla(1, 2, 3, 4, 5)  # Sonuç: 15

# İstediğiniz kadar sayıyı çarpma
sonuc = el.mat.tumunu_carp(1, 2, 3, 4, 5)  # Sonuç: 120

# Sayıların ortalamasını alma
sonuc = el.mat.ortalama(1, 2, 3, 4, 5)  # Sonuç: 3.0

# En büyük değeri bulma
sonuc = el.mat.en_buyuk_deger(1, 5, 3, 9, 2)  # Sonuç: 9

# En küçük değeri bulma
sonuc = el.mat.en_kucuk_deger(1, 5, 3, 9, 2)  # Sonuç: 1

# En büyük ve en küçük değer arasındaki farkı bulma (aralık)
sonuc = el.mat.aralik_degeri(1, 5, 3, 9, 2)  # Sonuç: 8

# Sayıların medyanını bulma
sonuc = el.mat.medyan(1, 3, 5, 7, 9)  # Sonuç: 5
```

### String (Metin) İşlevleri

`string` modülü, metinlerle çalışmak için çeşitli yardımcı fonksiyonlar sunar:

```python
# Metni tersine çevirme
sonuc = el.string.reverse("Merhaba")  # Sonuç: "abahreM"

# İlk harfi büyük yapma
sonuc = el.string.capitalize("merhaba dünya")  # Sonuç: "Merhaba dünya"

# Tüm metni büyük harfe çevirme
sonuc = el.string.uppercase("merhaba")  # Sonuç: "MERHABA"

# Tüm metni küçük harfe çevirme
sonuc = el.string.lowercase("MERHABA")  # Sonuç: "merhaba"

# Her kelimenin ilk harfini büyük yapma
sonuc = el.string.title("merhaba dünya")  # Sonuç: "Merhaba Dünya"

# Harflerin büyük/küçük durumunu tersine çevirme
sonuc = el.string.swapcase("Merhaba")  # Sonuç: "mERHABA"

# Metnin sadece harflerden oluşup oluşmadığını kontrol etme
sonuc = el.string.isalpha("Merhaba")  # Sonuç: True
sonuc = el.string.isalpha("Merhaba123")  # Sonuç: False

# Metnin sadece rakamlardan oluşup oluşmadığını kontrol etme
sonuc = el.string.isdigit("12345")  # Sonuç: True
sonuc = el.string.isdigit("12a45")  # Sonuç: False

# Metindeki her kelimeyi tersine çevirme
sonuc = el.string.reverse_words("Merhaba Dünya")  # Sonuç: "abahreM aynüD"
```

### Dil Algılama ve Yazım Denetimi

String modülü, Türkçe ve İngilizce metinler için bazı dil işleme özellikleri içerir:

```python
# Dilin tespiti (Türkçe veya İngilizce)
dil = el.string.detect_language("merhaba dünya")  # Sonuç: "tr"
dil = el.string.detect_language("hello world")    # Sonuç: "en"

# NOT: Yazım denetimi ve düzeltme işlevleri implementation aşamasındadır
# İleri versiyonlarda eklenecektir
```

### String (Metin) İşlevleri (Türkçe)

`yazi` modülü, `string` modülünün Türkçe alternatifidir:

```python
# Metni tersine çevirme
sonuc = el.yazi.tersine_cevir("Merhaba")  # Sonuç: "abahreM"

# İlk harfi büyük yapma
sonuc = el.yazi.buyuk_harf_yap("merhaba dünya")  # Sonuç: "Merhaba dünya"

# Tüm metni büyük harfe çevirme
sonuc = el.yazi.buyuk_harfe_cevir("merhaba")  # Sonuç: "MERHABA"

# Tüm metni küçük harfe çevirme
sonuc = el.yazi.kucuk_harfe_cevir("MERHABA")  # Sonuç: "merhaba"

# Her kelimenin ilk harfini büyük yapma
sonuc = el.yazi.baslik_yap("merhaba dünya")  # Sonuç: "Merhaba Dünya"

# Harflerin büyük/küçük durumunu tersine çevirme
sonuc = el.yazi.buyuk_kucuk_degistir("Merhaba")  # Sonuç: "mERHABA"

# Metnin sadece harflerden oluşup oluşmadığını kontrol etme
sonuc = el.yazi.harf_mi("Merhaba")  # Sonuç: True
sonuc = el.yazi.harf_mi("Merhaba123")  # Sonuç: False

# Metnin sadece rakamlardan oluşup oluşmadığını kontrol etme
sonuc = el.yazi.rakam_mi("12345")  # Sonuç: True
sonuc = el.yazi.rakam_mi("12a45")  # Sonuç: False

# Metindeki her kelimeyi tersine çevirme
sonuc = el.yazi.kelimeleri_tersine_cevir("Merhaba Dünya")  # Sonuç: "abahreM aynüD"
```

### Liste İşlevleri

`list` modülü, listelerle çalışmak için kullanışlı fonksiyonlar sunar:

```python
# Listeyi ters çevirme
sonuc = el.list.reverse([1, 2, 3, 4, 5])  # Sonuç: [5, 4, 3, 2, 1]

# Listeyi sıralama
sonuc = el.list.sort([3, 1, 4, 2, 5])  # Sonuç: [1, 2, 3, 4, 5]

# Listeden tekrarlayan öğeleri kaldırma (benzersiz liste)
sonuc = el.list.unique([1, 2, 2, 3, 3, 4, 5, 5])  # Sonuç: [1, 2, 3, 4, 5]
```

### Liste İşlevleri (Türkçe)

`dizi` modülü, `list` modülünün Türkçe alternatifidir:

```python
# Listeyi tersine çevirme
sonuc = el.dizi.tersine_cevir([1, 2, 3, 4, 5])  # Sonuç: [5, 4, 3, 2, 1]

# Listeyi sıralama
sonuc = el.dizi.sirala([3, 1, 4, 2, 5])  # Sonuç: [1, 2, 3, 4, 5]

# Listeden tekrarlayan öğeleri kaldırma (benzersiz liste)
sonuc = el.dizi.benzersiz([1, 2, 2, 3, 3, 4, 5, 5])  # Sonuç: [1, 2, 3, 4, 5]
```

### Görüntü İşleme İşlevleri

`image` modülü, gelişmiş görüntü işleme işlevleri sunar. Bu modül OpenCV kütüphanesini arka planda kullanır ancak kullanıcının OpenCV bilmesine gerek kalmadan kolay bir arayüz sağlar:

```python
# Bir görüntüyü gri tonlamaya çevirme
gri_resim = el.image.to_grayscale('resim.jpg')
# veya işlenmiş görüntüyü doğrudan kaydetme
el.image.to_grayscale('resim.jpg', output_path='gri_resim.jpg')

# Bir görüntüyü yeniden boyutlandırma
boyutlandirilmis_resim = el.image.resize('resim.jpg', 800, 600)
# En-boy oranını koruyarak boyutlandırma
el.image.resize('resim.jpg', 800, 0, keep_aspect_ratio=True, output_path='boyutlandirilmis_resim.jpg')

# Bir görüntüyü döndürme (açı derece cinsinden)
dondurulmus_resim = el.image.rotate('resim.jpg', 90)  # 90 derece döndürme

# Görüntüyü kırpma (x, y, genişlik, yükseklik)
kirpilmis_resim = el.image.crop('resim.jpg', 100, 100, 300, 200)

# Görüntüye bulanıklık ekleme
bulanik_resim = el.image.add_blur('resim.jpg', blur_type='gaussian', kernel_size=5)
# Farklı bulanıklık tipleri: 'gaussian', 'median', 'box'

# Kenar tespiti yapma
kenarlar = el.image.detect_edges('resim.jpg', method='canny', threshold1=100, threshold2=200)
# Farklı kenar tespit yöntemleri: 'canny', 'sobel'

# Parlaklık ayarlama (1.0 değişim yok, >1.0 daha parlak, <1.0 daha karanlık)
parlak_resim = el.image.adjust_brightness('resim.jpg', factor=1.5)

# Kontrast ayarlama (1.0 değişim yok, >1.0 daha fazla kontrast, <1.0 daha az kontrast)
kontrastli_resim = el.image.adjust_contrast('resim.jpg', factor=1.3)

# Histogram eşitleme (görüntü iyileştirme)
iyilestirilmis_resim = el.image.equalize_histogram('resim.jpg')

# Görüntüye metin ekleme
resim_metin = el.image.add_text('resim.jpg', 'Merhaba Dünya', position=(50, 50), 
                               font_size=1, color=(255, 0, 0), thickness=2)

# Görüntüye dikdörtgen ekleme
resim_dikdortgen = el.image.add_rectangle('resim.jpg', top_left=(50, 50), 
                                         bottom_right=(150, 150), color=(0, 255, 0))

# Yüz tespiti
resim_yuzler, yuzler = el.image.detect_faces('resim.jpg', draw_rectangles=True)
print(f"Tespit edilen yüz sayısı: {len(yuzler)}")

# Sanatsal filtreler uygulama
sepya_resim = el.image.apply_filter('resim.jpg', filter_type='sepia')
negatif_resim = el.image.apply_filter('resim.jpg', filter_type='negative')
karakalem_resim = el.image.apply_filter('resim.jpg', filter_type='sketch')
karikatur_resim = el.image.apply_filter('resim.jpg', filter_type='cartoon')

# İki görüntüyü birleştirme (harmanlanma)
birlesik_resim = el.image.merge_images('resim1.jpg', 'resim2.jpg', 
                                      weight1=0.7, weight2=0.3)

# Görüntüyü kaydetme
el.image.save_image(iyilestirilmis_resim, 'sonuc.jpg')

# Not: Tüm fonksiyonlar hem dosya yolları hem de NumPy dizileri ile çalışabilir
# Ayrıca tüm fonksiyonlarda işlem sonucunu dosyaya kaydetmek için opsiyonel
# output_path parametresi kullanılabilir
```

### Görüntü İşleme Çoklu İşlem Örneği

```python
from elan import elan

el = elan()

# Adım adım görüntü işleme
resim_yolu = "ornek_resim.jpg"

# 1. Görüntüyü yükle ve boyutlandır
resim = el.image.resize(resim_yolu, 800, 600, keep_aspect_ratio=True)

# 2. Parlaklık ve kontrast ayarla
resim = el.image.adjust_brightness(resim, factor=1.2)  # Biraz daha parlak
resim = el.image.adjust_contrast(resim, factor=1.1)    # Biraz daha kontrastlı

# 3. Görüntüye hafif bulanıklık ekle (gürültüyü azaltmak için)
resim = el.image.add_blur(resim, blur_type='gaussian', kernel_size=3)

# 4. Histogram eşitleme ile detayları iyileştir
resim = el.image.equalize_histogram(resim)

# 5. Yüzleri tespit et ve dikdörtgen ile işaretle
resim, yuzler = el.image.detect_faces(resim, draw_rectangles=True)

# 6. Tespit sonucunu metin olarak ekle
if len(yuzler) > 0:
    metin = f"{len(yuzler)} yüz tespit edildi"
    resim = el.image.add_text(resim, metin, position=(20, 30), 
                             font_size=0.8, color=(0, 255, 0), thickness=2)

# 7. Sonuç görüntüsünü kaydet
el.image.save_image(resim, "islenmiş_resim.jpg")

print("Görüntü işleme tamamlandı!")
```

### Görüntü Filtreleri ve Efektler Örneği

```python
from elan import elan
import os

el = elan()

# Orjinal görüntü üzerinde farklı filtreler uygulama
resim_yolu = "ornek_resim.jpg"
sonuc_klasoru = "filtre_sonuclari"

# Sonuç klasörünü oluştur
os.makedirs(sonuc_klasoru, exist_ok=True)

# Tüm filtre tiplerini uygula
filtreler = ['sepia', 'negative', 'sketch', 'cartoon']

for filtre in filtreler:
    sonuc_yolu = os.path.join(sonuc_klasoru, f"{filtre}_resim.jpg")
    el.image.apply_filter(resim_yolu, filter_type=filtre, output_path=sonuc_yolu)
    print(f"{filtre} filtresi uygulandı: {sonuc_yolu}")

# Kenar tespiti
kenar_yolu = os.path.join(sonuc_klasoru, "kenarlar.jpg")
el.image.detect_edges(resim_yolu, method='canny', 
                     threshold1=100, threshold2=200, 
                     output_path=kenar_yolu)
print(f"Kenar tespiti tamamlandı: {kenar_yolu}")

# Farklı bulanıklık tipleri
bulaniklik_tipleri = ['gaussian', 'median', 'box']
for tip in bulaniklik_tipleri:
    bulanik_yolu = os.path.join(sonuc_klasoru, f"{tip}_bulanik.jpg")
    el.image.add_blur(resim_yolu, blur_type=tip, kernel_size=9, output_path=bulanik_yolu)
    print(f"{tip} bulanıklık uygulandı: {bulanik_yolu}")

print("Tüm filtreler ve efektler uygulandı!")
```

### Video İşleme İşlevleri

`video` modülü, kapsamlı video işleme özellikleri sunar. Bu modül OpenCV'yi arka planda kullanır ancak kullanıcının doğrudan OpenCV ile ilgilenmesine gerek kalmaz:

```python
from elan import elan

el = elan()

# Video hakkında bilgi alma
video_bilgisi = el.video.get_video_info("ornek_video.mp4")
print(f"Video çözünürlüğü: {video_bilgisi['width']}x{video_bilgisi['height']}")
print(f"FPS: {video_bilgisi['fps']}")
print(f"Toplam süre: {video_bilgisi['duration_formatted']}")

# Videodan belirli aralıklarla kare çıkarma
kareler = el.video.extract_frames(
    "ornek_video.mp4",
    output_dir="kareler",
    frame_interval=30,  # Her 30 karede bir kare çıkar
    max_frames=10       # En fazla 10 kare çıkar
)
print(f"{len(kareler)} kare çıkarıldı")

# Karelerden video oluşturma
el.video.create_video_from_frames(
    "kareler",
    "yeni_video.mp4",
    fps=30.0
)

# Videoyu farklı formata dönüştürme
el.video.convert_video(
    "ornek_video.mp4",
    "donusturulmus_video.mp4",
    codec="mp4v",
    resize=(640, 480)
)

# Video kırpma (belirli bir zaman aralığını alma)
el.video.trim_video(
    "ornek_video.mp4",
    "kirpilmis_video.mp4",
    start_time=10.5,    # 10.5 saniyeden başla
    end_time=20.0       # 20. saniyede bitir
)

# Videoya filtre uygulama
el.video.apply_filter_to_video(
    "ornek_video.mp4",
    "gri_video.mp4",
    filter_type="grayscale"  # Gri tonlama filtresi
)

# Videoya sepya filtresi uygulama
el.video.apply_filter_to_video(
    "ornek_video.mp4",
    "sepya_video.mp4",
    filter_type="sepia"
)

# Videoya bulanıklık filtresi uygulama
el.video.apply_filter_to_video(
    "ornek_video.mp4",
    "bulanik_video.mp4",
    filter_type="blur",
    kernel_size=15,
    blur_type="gaussian"
)

# Videoda hareket algılama
hareket_bilgileri = el.video.detect_motion(
    "ornek_video.mp4",
    "hareket_algilama.mp4",  # Hareketlerin belirtildiği çıktı videosu
    sensitivity=25.0,
    min_area=500
)

for hareket in hareket_bilgileri:
    print(f"Hareket algılandı: {hareket['timestamp_formatted']}")

# Videoya metin ekleme
el.video.add_text_to_video(
    "ornek_video.mp4",
    "metin_video.mp4",
    text="Elan Video İşleme",
    position=(50, 50),
    font_scale=1.0,
    color=(0, 255, 0),  # Yeşil
    thickness=2
)

# Video hızını değiştirme
el.video.speed_change(
    "ornek_video.mp4",
    "hizli_video.mp4",
    speed_factor=2.0  # 2 kat hızlı
)
el.video.speed_change(
    "ornek_video.mp4",
    "yavas_video.mp4",
    speed_factor=0.5  # 2 kat yavaş
)

# Birden fazla videoyu birleştirme
el.video.combine_videos(
    ["video1.mp4", "video2.mp4", "video3.mp4"],
    "birlesik_video.mp4",
    transition_frames=15  # 15 karelik yumuşak geçiş
)

# Videoda yüz algılama
yuz_bilgileri = el.video.detect_faces_in_video(
    "ornek_video.mp4",
    "yuz_algilama.mp4",
    scale_factor=1.1,
    min_neighbors=5,
    min_size=(30, 30),
    rectangle_color=(0, 0, 255)  # Kırmızı dikdörtgenler
)

print(f"Toplam {len(yuz_bilgileri)} karede yüz tespit edildi")
for bilgi in yuz_bilgileri:
    print(f"Kare {bilgi['frame']}: {bilgi['face_count']} yüz tespit edildi")

# Videoda yüz tanıma (face recognition)
# Not: Bu özellik için 'pip install face_recognition' gereklidir
tanima_bilgileri = el.video.recognize_faces_in_video(
    "ornek_video.mp4",
    "bilinen_kisiler",  # Her kişi için bir klasör içeren ana klasör
    "yuz_tanima.mp4",
    tolerance=0.6,  # Eşleşme hassasiyeti (düşük değer = daha kesin eşleşme)
    skip_frames=5    # Her 5 karede bir tanıma yap (performans için)
)

print(f"Toplam {len(tanima_bilgileri)} karede yüz tanıma yapıldı")
for bilgi in tanima_bilgileri:
    for yuz in bilgi['recognized_faces']:
        print(f"Tanınan kişi: {yuz['name']}, güven: {yuz['confidence']:.2f}")
```

### Video İşleme Senaryoları

#### Senaryo 1: Video Düzenleme İşlemi

```python
from elan import elan
import os

el = elan()

# Video düzenleme projesi
kaynak_video = "ham_video.mp4"
sonuc_klasoru = "video_projesi"
os.makedirs(sonuc_klasoru, exist_ok=True)

# 1. Video bilgilerini al
video_bilgisi = el.video.get_video_info(kaynak_video)
print(f"İşlenen video: {video_bilgisi['duration_formatted']} süre, {video_bilgisi['width']}x{video_bilgisi['height']} çözünürlük")

# 2. Videoyu parçalara ayır
bol1 = os.path.join(sonuc_klasoru, "bolum1.mp4")
bol2 = os.path.join(sonuc_klasoru, "bolum2.mp4")
bol3 = os.path.join(sonuc_klasoru, "bolum3.mp4")

# İlk 10 saniye
el.video.trim_video(kaynak_video, bol1, 0, 10)

# 15-25 saniye arası
el.video.trim_video(kaynak_video, bol2, 15, 25)

# 30-40 saniye arası
el.video.trim_video(kaynak_video, bol3, 30, 40)

# 3. Parçalara efekt uygula
efektli_bol1 = os.path.join(sonuc_klasoru, "efekt_bolum1.mp4")
efektli_bol2 = os.path.join(sonuc_klasoru, "efekt_bolum2.mp4")
efektli_bol3 = os.path.join(sonuc_klasoru, "efekt_bolum3.mp4")

# Birinci bölüme gri filtre
el.video.apply_filter_to_video(bol1, efektli_bol1, "grayscale")

# İkinci bölüme sepya filtre
el.video.apply_filter_to_video(bol2, efektli_bol2, "sepia")

# Üçüncü bölüme negatif filtre
el.video.apply_filter_to_video(bol3, efektli_bol3, "negative")

# 4. Efektli parçaları birleştir
sonuc_video = os.path.join(sonuc_klasoru, "sonuc_video.mp4")
el.video.combine_videos(
    [efektli_bol1, efektli_bol2, efektli_bol3],
    sonuc_video,
    transition_frames=10
)

# 5. Son videoya metin ekle
son_video = os.path.join(sonuc_klasoru, "final_video.mp4")
el.video.add_text_to_video(
    sonuc_video,
    son_video,
    text="Elan ile düzenlenmiştir",
    position=(20, 30),
    font_scale=0.8,
    color=(0, 255, 255)  # Sarı
)

print(f"Video düzenleme tamamlandı: {son_video}")
```

#### Senaryo 2: Hareket Algılama ve Zaman Atlamalı Video

```python
from elan import elan
import os
import datetime

el = elan()

# Hareket algılama ve zaman atlamalı video oluşturma
kaynak_video = "guvenlik_kamerasi.mp4"
sonuc_klasoru = "hareket_analizi"
os.makedirs(sonuc_klasoru, exist_ok=True)

# 1. Videoda hareket algılama
hareket_dosyasi = os.path.join(sonuc_klasoru, "hareket_video.mp4")
hareketler = el.video.detect_motion(
    kaynak_video,
    hareket_dosyasi,
    sensitivity=20.0,
    min_area=300
)

print(f"Toplam {len(hareketler)} hareket tespit edildi")

# 2. Hareket olan kısımları ayıkla
hareket_parcalari = []
if hareketler:
    video_bilgisi = el.video.get_video_info(kaynak_video)
    fps = video_bilgisi['fps']
    
    for i, hareket in enumerate(hareketler):
        # Hareket başlangıcından 2 saniye öncesi ve 3 saniye sonrasını al
        baslangic = max(0, hareket['timestamp'] - 2)
        bitis = min(video_bilgisi['duration'], hareket['timestamp'] + 3)
        
        # Bu parçayı video olarak çıkart
        parca_dosya = os.path.join(sonuc_klasoru, f"hareket_{i+1:03d}.mp4")
        el.video.trim_video(kaynak_video, parca_dosya, baslangic, bitis)
        hareket_parcalari.append(parca_dosya)
        
        print(f"Hareket {i+1}: {hareket['timestamp_formatted']} - alan: {hareket['max_area']:.0f} piksel")

# 3. Hareket parçalarını birleştir ve tarih bilgisi ekle
if hareket_parcalari:
    ozet_video = os.path.join(sonuc_klasoru, "ozet_video.mp4")
    el.video.combine_videos(hareket_parcalari, ozet_video, transition_frames=5)
    
    final_video = os.path.join(sonuc_klasoru, "final_hareket_ozeti.mp4")
    tarih = datetime.datetime.now().strftime("%d.%m.%Y")
    el.video.add_text_to_video(
        ozet_video,
        final_video,
        text=f"Hareket Özeti - {tarih}",
        position=(20, 30),
        font_scale=1.0,
        color=(0, 0, 255)  # Kırmızı
    )
    
    print(f"Hareket özet videosu oluşturuldu: {final_video}")
else:
    print("Hareket tespit edilemedi veya dosyalar oluşturulamadı")
```

#### Senaryo 3: Yüz Tanıma ve Takip Sistemi

```python
from elan import elan
import os
import datetime
import shutil

el = elan()

# Yüz tanıma ve takip sistemi
kaynak_video = "toplanti_kaydi.mp4"
sonuc_klasoru = "yuz_takip_sonuclari"
os.makedirs(sonuc_klasoru, exist_ok=True)

# Bilinen kişiler klasörü
bilinen_kisiler = "bilinen_kisiler"
if not os.path.exists(bilinen_kisiler):
    os.makedirs(bilinen_kisiler)
    
    # ÖRNEK: Gerçek uygulamada burası kişilere ait görüntülerle doldurulmalıdır
    # Burada yalnızca klasör yapısını gösteriyoruz
    for kisi in ["Ahmet", "Ayşe", "Mehmet"]:
        os.makedirs(os.path.join(bilinen_kisiler, kisi), exist_ok=True)

# 1. Önce tüm yüzleri tespit et
yuz_algilama_video = os.path.join(sonuc_klasoru, "yuz_algilama.mp4")
tespit_edilen_yuzler = el.video.detect_faces_in_video(
    kaynak_video,
    yuz_algilama_video,
    min_size=(50, 50)  # Daha büyük yüzleri tespit et
)

print(f"Toplam {len(tespit_edilen_yuzler)} karede yüz tespit edildi")

# 2. Tespit edilen yüzleri kullanarak yüz tanıma yap
yuz_tanima_video = os.path.join(sonuc_klasoru, "yuz_tanima.mp4")
tanima_sonuclari = el.video.recognize_faces_in_video(
    kaynak_video,
    bilinen_kisiler,
    yuz_tanima_video,
    tolerance=0.6,
    skip_frames=3  # Performans için her 3 karede bir tanıma yap
)

# 3. Kişi bazlı analiz yap
kisi_istatistikleri = {}

for bilgi in tanima_sonuclari:
    for yuz in bilgi['recognized_faces']:
        kisi = yuz['name']
        if kisi not in kisi_istatistikleri:
            kisi_istatistikleri[kisi] = {
                'ilk_gorunme': bilgi['timestamp'],
                'son_gorunme': bilgi['timestamp'],
                'toplam_sure': 0,
                'gorunme_sayisi': 1,
                'ortalama_guven': yuz['confidence']
            }
        else:
            # Kişi istatistiklerini güncelle
            kisi_istatistikleri[kisi]['son_gorunme'] = bilgi['timestamp']
            kisi_istatistikleri[kisi]['gorunme_sayisi'] += 1
            kisi_istatistikleri[kisi]['ortalama_guven'] += yuz['confidence']

# İstatistikleri hesapla ve rapor oluştur
rapor_dosyasi = os.path.join(sonuc_klasoru, "kisi_raporu.txt")
with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
    f.write(f"Yüz Tanıma Raporu - {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    f.write(f"Kaynak video: {kaynak_video}\n\n")
    
    for kisi, istatistik in kisi_istatistikleri.items():
        # Toplam süreyi hesapla
        toplam_sure = istatistik['son_gorunme'] - istatistik['ilk_gorunme']
        ortalama_guven = istatistik['ortalama_guven'] / istatistik['gorunme_sayisi']
        
        f.write(f"Kişi: {kisi}\n")
        f.write(f"  İlk görünme: {str(datetime.timedelta(seconds=int(istatistik['ilk_gorunme'])))}\n")
        f.write(f"  Son görünme: {str(datetime.timedelta(seconds=int(istatistik['son_gorunme'])))}\n")
        f.write(f"  Toplam süre: {str(datetime.timedelta(seconds=int(toplam_sure)))}\n")
        f.write(f"  Görünme sayısı: {istatistik['gorunme_sayisi']}\n")
        f.write(f"  Ortalama güven: {ortalama_guven:.2f}\n\n")

print(f"Kişi raporu oluşturuldu: {rapor_dosyasi}")

# 4. Sonuç videosu oluştur
print(f"Yüz algılama sonuç videosu: {yuz_algilama_video}")
print(f"Yüz tanıma sonuç videosu: {yuz_tanima_video}")
```

## Örnek Kullanım Senaryoları

### Senaryo 1: Metinsel İşlemler

```python
from elan import elan

el = elan()

# Kullanıcı girdisini işleme
metin = "merhaba dünya"
print(f"Orijinal metin: {metin}")
print(f"Başlık formatında: {el.string.title(metin)}")
print(f"Tersi: {el.string.reverse(metin)}")
print(f"Sadece harflerden mi oluşuyor? {el.string.isalpha(metin.replace(' ', ''))}")
```

### Senaryo 2: Basit Hesaplama Programı

```python
from elan import elan

el = elan()

# Hesaplama işlemleri
sayi1 = 10
sayi2 = 5

print(f"{sayi1} + {sayi2} = {el.math.add(sayi1, sayi2)}")
print(f"{sayi1} - {sayi2} = {el.math.subtract(sayi1, sayi2)}")
print(f"{sayi1} × {sayi2} = {el.math.multiply(sayi1, sayi2)}")
print(f"{sayi1} ÷ {sayi2} = {el.math.divide(sayi1, sayi2)}")
print(f"{sayi1}^{sayi2} = {el.math.power(sayi1, sayi2)}")
print(f"{sayi1}! = {el.math.factorial(sayi1)}")

# Çoklu sayılar ile işlemler
sayilar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Sayıların toplamı: {el.math.sum_all(*sayilar)}")
print(f"Sayıların çarpımı: {el.math.multiply_all(*sayilar)}")
print(f"Sayıların ortalaması: {el.math.average(*sayilar)}")
print(f"En büyük sayı: {el.math.max_value(*sayilar)}")
print(f"En küçük sayı: {el.math.min_value(*sayilar)}")
print(f"Sayıların aralığı: {el.math.range_value(*sayilar)}")
print(f"Sayıların medyanı: {el.math.median(*sayilar)}")
```

### Senaryo 3: Çokdilli Yazım Denetimi ve Düzeltme Uygulaması

```python
from elan import elan

el = elan()

# Dil tespiti
texts = ["merhaba dünya", "hello world", "merhaba world"]
for text in texts:
    dil = el.string.detect_language(text)
    print(f"'{text}' metni {dil} dilinde")

# NOT: Aşağıdaki yazım denetimi ve düzeltme işlevleri henüz uygulanma 
# aşamasında olup tam olarak çalışmayabilir. Gelecek sürümlerde bu 
# özellikler tam olarak desteklenecektir.

"""
# Yanlış yazılmış metinleri düzeltme
yanlis_metinler = {
    "tr": "meraba nasilsin bugun hva nasil",
    "en": "helo worl, how ar you tody"
}

for dil, metin in yanlis_metinler.items():
    duzeltilmis = el.string.correct_text(metin, language=dil)
    print(f"\n{dil.upper()} dili:")
    print(f"Orijinal: {metin}")
    print(f"Düzeltilmiş: {duzeltilmis}")

# Kullanıcı girdisi ile yazım denetimi
user_input = input("\nBir kelime yazın: ")
dil = el.string.detect_language(user_input)
print(f"Tespit edilen dil: {dil}")

oneriler = el.string.suggest_correction(user_input, language=dil, max_suggestions=5)
print(f"Öneriler: {oneriler}")
"""
```

### Senaryo 4: Görüntü İşleme Uygulaması

```python
from elan import elan
import cv2

el = elan()

# Orijinal görüntüyü yükle ve işle
resim_yolu = "ornek_resim.jpg"

# Gri tonlama dönüşümü
gri_resim = el.image.to_grayscale(resim_yolu)
cv2.imwrite("gri_resim.jpg", gri_resim)

# Görüntüyü yeniden boyutlandırma
boyutlandirilmis_resim = el.image.resize(resim_yolu, 300, 200)
cv2.imwrite("boyutlandirilmis_resim.jpg", boyutlandirilmis_resim)

# Görüntüyü döndürme
dondurulmus_resim = el.image.rotate(resim_yolu, 45)  # 45 derece döndürme
cv2.imwrite("dondurulmus_resim.jpg", dondurulmus_resim)

print("Görüntü işleme tamamlandı!")
```

## Sorun Giderme

### Sık Karşılaşılan Hatalar

**ImportError: No module named 'elan'**  
Çözüm: Paketi pip ile yüklediğinizden emin olun: `pip install elan`

**ModuleNotFoundError: No module named 'cv2'**  
Çözüm: OpenCV'yi yükleyin: `pip install opencv-python`

**OSError veya VideoCapture hatası**  
Çözüm: Video dosyalarınızın doğru formatta ve erişilebilir olduğundan emin olun. Bazı codec'ler ek modüller gerektirebilir.

**DLL hatası (Windows'ta)**  
Çözüm: Visual C++ yeniden dağıtılabilir paketlerinin güncel olduğundan emin olun.

**Yetersiz bellek hatası**  
Çözüm: Büyük videolar ile çalışırken, `resize` parametrelerini kullanarak boyutları küçültün veya `frame_interval` kullanarak işlenen kare sayısını azaltın.

## Performans İpuçları

1. Büyük videolar ile çalışırken, kare atlama (frame skipping) işlevlerini kullanın
2. Görüntü boyutlandırma ile bellek tüketimini azaltın
3. Video işleme sırasında tüm kareleri hafızada tutmak yerine, disk üzerine kaydedin
4. Hareket algılama için `min_area` değerini uygun şekilde ayarlayın

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

Herhangi bir soru, öneri veya geri bildirim için:

- GitHub: [https://github.com/efekannn5/ElanLibs](https://github.com/efekannn5/ElanLibs)
- E-posta: efekan8190nefesogeu@gmail.com

### Powered By Efekan Nefesoğlu

## Katkı Rehberi

Elan projesine katkıda bulunmak için:

1. Depoyu fork edin
2. Kendi branch'inizi oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik ekle'`)
4. Değişikliklerinizi branch'e push edin (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun

## Sık Sorulan Sorular

**S: Hangi Python sürümü gereklidir?**  
C: Elan, Python 3.6 veya üstü gerektirir.

**S: Elan kütüphanesini ticari projelerde kullanabilir miyim?**  
C: Evet, Elan MIT Lisansı altında yayınlanmıştır ve ticari kullanıma uygundur.

**S: Elan nasıl telaffuz edilir?**  
C: "E-LAN" şeklinde telaffuz edilir.

**S: Kütüphaneyi nasıl güncellerim?**  
C: `pip install --upgrade elan` komutunu kullanarak kütüphanenin son sürümünü yükleyebilirsiniz.

**S: Görüntü işleme fonksiyonları nasıl çalışır?**  
C: Görüntü işleme fonksiyonları, OpenCV kütüphanesini kullanır ve görüntü işleme işlemleri için bir OpenCV nesnesi döndürür.

**S: Yazım denetimi ve düzeltme işlevleri geliyor mu?**  
C: Evet, yazım denetimi ve düzeltme işlevleri geliştirme aşamasındadır ve gelecek sürümlerde eklenecektir.

**S: Video işleme işlevleri için Türkçe alternatifler de eklenecek mi?**  
C: Evet, video işleme modülü için Türkçe alternatif isimlendirmeler gelecek sürümlerde eklenecektir.


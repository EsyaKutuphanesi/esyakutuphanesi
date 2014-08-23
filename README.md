# Eşya Kütüphanesi

Eşya Kütüphanesi, eşyalarını ödünç alıp vererek çevrendekilerle paylaşmanı kolaylaştıran online bir platformdur.

Bu git deposu, Eşya Kütüphanesi web platformunun kaynak kodlarını içerir.


## Kurulum

Bağımlılıklar kurulmadan önce bir `virtualenv` yaratılması ve aktifleştirilmesi tavsiye edilir.

Sonrasında

    pip install -r requirements.txt       # Bağımlıkları kur
    cd src/                               # Uygulama klasörüne gir
    python manage.py database create      # Veritabanını yarat ve örnek veriyle doldur


## Çalıştırma

    cd src/                               # Daha önce girilmemişse
    python manage.py runserver            # Test sunucusunu başlat

`runserver` ile çalıştırılan test sunucusuna `0.0.0.0:5000`den ulaşılabilir.


## Yönetim

Veritabanı örnek veriyle doldurulmuşsa, sistemde bir adet test kullanıcısı öntanımlı olarak gelir. Bu kullanıcının bilgileri

Kullanıcı adı: `bilgi@esyakutuphanesi.com`  
Parola:        `ekekek`  

şeklindedir. Sisteme `http://0.0.0.0:5000/login` üzerinden, veya farklı IP ve port değerleri ile çalıştırılmışsa `ip:port/login` üzerinden, giriş yapılır. Öntanımlı kullanıcı, sistem üzerinde yönetici haklarına sahiptir ve sistemde oturum açtıktan sonra yönetim paneline `http://0.0.0.0:5000/admin/` / `ip:port/admin` üzerinden ulaşılabilir.

### Yönetim Komutları

`src/` dizini altında bulunan `manage.py` ve `resetrun.sh` dosyaları, projenin yönetimini kolaylaştıran bazı komutlar sunar. Dosya, `python manage.py` ile parametresiz olarak çağırıldığında aşağıdaki yardım çıktısını verir:

    usage: manage.py [-?] {database,runserver} ...

    positional arguments:
      {database,runserver}
        database            Perform database operations
        runserver           Runs the Flask development server i.e. app.run()

    optional arguments:
      -?, --help            show this help message and exit

### `runserver`

Yerel test sunucusunu çalıştırır. Ön tanımlı IP değeri `0.0.0.0`, ön tanımlı port değeri `5000` şeklindedir.

Örnek kullanım:

    python manage.py runserver                 # Ön tanımlı IP ve port değerleriyle çalış
    python manage.py runserver -P port         # Verilen port değeri ve öntanımlı IP ile çalış
    python manage.py runserver -h host         # Verilen host değeri ve öntanımlı port ile çalış

Komutun kullanımıyla ilgili diğer detaylara `python manage.py runserver --help` ile ulaşılabilir.

### `database create`

Projenin kullanacağı veritabanını yaratır. Ön tanımlı olarak örnek veriyi yükler.

Örnek kullanım:

    python manage.py database create           # Tabloları yaratıp örnek veriyi yükle
    python manage.py database create -s no     # Tabloları yarat ve örnek veriyi yükleme

### `database drop`

Projenin kullandığı veritabanını boşaltır. Çalışması `y` veya `yes` ile onaylanması gerekir.

Örnek kullanım:

    python manage.py database drop             # Tüm veriyi ve tabloları kaldır

### `database recreate`

Önce `drop`, sonra da `create` komutunun kullanılmasıyla yapılacak işi tek seferde yapar.

Örnek kullanım:

    python manage.py database recreate         # Tabloları sil, yarat ve örnek veriyi yükle
    python manage.py database recreate -s no   # Tabloları sil, yarat ve örnek veriyi yükleme

### `database populate`

Daha önce yaratılmış veritabanına örnek veriyi yükler. Veritabanı yaratılmamışsa hata verir.

Örnek kullanım:

    python manage.py populate                  # sample_data klasöründeki veriyi yükle

### resetrun.sh

Projeye ait veritabanın hızlıca sıfırlanıp, yeniden yüklenip test sunucusunun çalıştırılmasını sağlar.

`sh resetrun.sh` şeklinde kullanılabilir. Etkisi

    python manage.py database drop
    python manage.py database create -s no
    python manage.py database populate

    python manage.py runserver -h 0.0.0.0 -p 5000

komutlarının art arda kullanmasına eşittir.
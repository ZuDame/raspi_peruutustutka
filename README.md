# raspi_peruutustutka

Raspberry Pi – peruutustutka
Tämän projektityön tarkoitus on rakentaa järjestelmä, jossa Raspberry Pi:llä ja ultraäänisensorilla
simuloidaan peruutustutkaa. Kommunikaatio Raspberry Pi:n ja sensorin välillä tapahtuu käyttämällä I2Cväylää.
Yhteys Raspberry Pi:hin tulee ottaa SSH yhteyden avulla. Sensoria ohjaava ohjelmakoodi
kirjoitetaan Python-ohjelmointikielellä. Järjestelmän tulee ilmoittaa mittausinformaatio, etäisyys,
konsolissa, mutta myös summerin avulla imitoiden peruutustutkan käyttäytymistä.
Ultraäänisensorin kantama on muutama metri. Kun sensori havaitsee jotain yli metrin päässä, summeri
pysyy hiljaa. Kun tullaan alle metriin, niin summerista alkaa kuulumaan merkkisignaalia. Merkkisignaalin
tekemiseen käytetään PWM-signaalia. Kun lukema on metri, merkkisignaali on päällä 0.5s, jonka jälkeen
se on 0.5s hiljaa. Taajuden saa itse määrittää. Kymmenen senttimetrin välein merkkisignaalin pituus
lyhenee, kunnes jakson pituus on enää 0.1s. Kun etäisyys on alle kymmenen senttimetriä tai
ultraäänisensori ei saa lukemaa, summeri pitää yhtäjaksoista merkkisignaalia päällä. Sensorissa on lisäksi
valoisuusanturi jota voi käyttää hyödyksi.
Konsolilla etäisyyden tulee näkyä senttimetreinä.
Raspberry Pi – Käyttöönotto
Kattavat käyttöönotto-ohjeet löytyvät esimerkiksi osoitteesta http://elinux.org/RPi_Beginners.
Käytettävät muistikortit ovat esiasennettuja Raspbian-käyttöjärjestelmällä. Esiasetetut tunnukset ovat,
user: pi
password: raspberry
Rpi kannattaa pitää kiinni Internetissä, jotta pakettien ja päivitysten asentaminen onnistuu helposti.
Käyttöjärjestelmä kannattaa ensin päivittää komennolla sudo apt-get update.
I2C
Tutustu I2C väylän toimintaan (esim. http://en.wikipedia.org/wiki/I%C2%B2C) RPissä on vakiona I2C
väylä poistettu käytöstä. Kirjoita käsky sudo nano /etc/modprobe.d/raspiblacklist.conf. Avautuvasta
tiedostosta voidaan I2C väylä ottaa käyttöön kommentoimalla blacklist i2cbcm2708 risuaidalla pois.
Tämän lisäksi I2C-moduli on lisättävä kernelin boottilistaan.
Kirjoita sudo nano /etc/modules ja lisää avautuvaan tiedostoon rivi i2c-dev. I2Ceen käyttö vaatii myös
pakettien asentamisen. Kirjoita sudo apt-get install i2c-tools, jolla voidaan skannata I2C-väylää
(http://www.lm-sensors.org/wiki/I2CTools). Toinen asennettava paketti saadaan kirjoittamalla sudo
apt-get install python-smbus, jolla voidaan käyttää I2C-väylää Pythonilla.
Ohjelman konfigurointia varten lisätään käyttäjä Pi I2C käyttöoikeusryhmään käskyllä sudo adduser pi
i2c. Käynnistä järjestelmä uudelleen sudo reboot. Rpi:ssä on kaksi I2C kanavaa, 0 ja 1. Kurssin Rpi mallit
käyttävät oletuksena 1 kanavaa. 
Testataksesi onko väylässä kiinni mitään kirjoita i2cdetect –y 1, joka näyttää seuraavalta, jos mitään ei
ole kytketty
0 1 2 3 4 5 6 7 8 9 a b c d e f
00: -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
Mikäli i2c väylään on jotakin kytkettynä, sen numeerinen osoite näkyy tuossa listassa.
Esim. Jokin laite on osoitteeseen 60.
0 1 2 3 4 5 6 7 8 9 a b c d e f
00: -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: 60 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
Sensorin kytkeminen ja ohjaaminen
Sensorissa on neljä linjaa joita käytetään. Punainen kytketään virtaan +5V (VIN), musta maahan (GND),
sininen dataan (SDA) ja punakeltainen kellosignaaliin (SCL). Ultraäänisensorin logiikka toimii 5V
jännitteellä kun taas Raspin logiikka toimii 3.3V jännitteellä. Täten väliin tarvitaan tasokonvertteri.
Raspilta saa 5V ulos ultraäänisensoria varten.
Kytkennän helpottamiseksi on järkevää kytkeä kaikki ensin koekytkentälevylle, josta alkaa jakaa
johdotuksia eri komponenteille. Kun kytkentä on valmis, kannattaa ajaa i2cdetect, josta nähdään missä
osoitteessa sensori sijaitsee. Jos sensori ei tunnistaudu tarkista kytkentä ja kokeile vielä vaihtaa
tarkistettavaa kanavaa. Kuvan ohjeen komponentit eivät ole ihan yksi yhteen niiden kanssa joita olen
jakanut. Pussissa on kuitenkin vain yhdenlaisia vastuksia ja transistoreja, joten ongelmia ei pitäisi tulla.
http://elinux.org/RPi_Low-level_peripherals. 
Summerin kytkeminen
Summerin voi kytkeä Raspberry Pin GPIO pinneihin kiinni.
SMBus-komennot, olennaisimmat tämän harjoituksen kannalta
read_byte_data(addr,cmd)
Addr on osoite i2c väylässä, ja cmd vastaa osoitetta joka luetaan ultraäänisensorilta. Esim
read_byte_data(70,1) lukee mikä on sensorin havaitsema valoisuusaste.
http://www.robot-electronics.co.uk/htm/srf08tech.shtml
Raspilla on laaja community, joten lisätietojen kirjoittaminen tähän ei auttaisi sen enempää kuin
asioiden selvittäminen itse.
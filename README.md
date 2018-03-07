Raspberry-peruutustutka

Laitteisto:
Raspberry Pi zero W
HC-SR05-ultraäänisensori
Summeri HCM1206BX

Kytkentä:

HS-SR05:
GND-GND
ECHO-GPIO24
TRIG-GPIO23
VCC-3.3V

Sensori on speksattu toimimaan 5V jännitteellä, mutta se toimii myös välttävästi 3.3V käyttöjännitteellä, joten jännitteenjakoa ei tarviste käyttää. (testasimme 5v käyttöjännitettä jännitteenjaolla ja sensorin suorituskyvyssä ei huomattu manittavaa eroa)

Summeri HCM1206BX:
Vcc-GPIO4
GND-GND

Summeri on speksattu toimimaan 7v tasajännitteellä, mutta GPIO-pinnistä saatava 3.3v tuottaa riittävän voimakkaan äänen testikäyttöön. Oikeassa toteutuksessa summeria kannattaisi käyttää raspista saatavalla 5 voltilla transistorin avulla.

Toiminta:

Laite mittaa etäisyyttä kappaleisiin käyttäen ultraäänisensorin dataa. Yli metrin etäisyydellä laite on hiljaa. Metrin etäisyydellä laite piippaa 0,5s ja on 0,5s hiljaa. Kappaleen lähestyttäessä piippaamisen taajuus kasvaa. Alle 10cm etäisyydellä laite piippaa yhtäjaksoisesti.

Koodi:

Ultraäänisensorin Trig-pinniin syötetään jännite 10 mikrosekunniksi, jolloin ultraäänisensori lähettää kahdeksan sykliä ultraääntä. Aika, jona Trig-pinni saa arvon high tallennetaan. Echo-pinni nousee tasoon high, kun sensori kuulee kaiun lähettämästään äänestä. Aika, jona ECHO-pinni saa tason high tallennetaan. Ohjelma laskee äänen kulussa kuluvan ajan ja jakaa sen äänen nopeudella ilmassa (cm/s). Tuloksena saadaan kohteen etäisyys senttimetreinä. 

Summeria ohjataan pulssileveysmodulaatiolla, joka toteutetaan ohjelmistotasolla. Etäisyyden perusteella ohjelma muuttaa pulssileveysmodulaation taajuutta ja työsykliä tehtävänannon mukaisesti.  


Konsoliin laite tulostaa etäisyyden senttimereinä.


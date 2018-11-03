# TV Episodes

V projektni nalogi bom analiziral epizode televizijskih serij, ki imajo na strani IMDb vsaj 2000 glasov. Podatke bom pridobil iz strani: https://www.imdb.com/search/title?num_votes=2000,&sort=user_rating,desc&title_type=tv_episode

Za vsako epizodo bom razbral:
* id epizode
* naslov serije
* naslov epizode in leto njenega izida
* dolžino epizode
* žan
* število glasov
* režiserje


Delovne hipoteze:
* Katera serija ima v povprečju najbolje ocenjene epizode?
* Ali obstaja povezava med trajanjem in oceno epizode?
* V katerem petletju je izšlo največ epizod?
* Kateri režiser ustvarja najboljše epizode?
* Kakšna je povezava med številom glasov in oceno?
* Ali z se z leti kakovost serij izboljšuje?

Nato pa bom serije razdelil na komične in nekomične, pri čemer bom sklepal, da je trajanje komičnih serij manj kot 30 minut (to bom seveda tudi preveril). S temi podatki bom nato primerjal zvrsti med seboj:
* Ali so v povprečju bolje ocenjene komične ali nekomične serije?
* Katere serije so bolj gledane?


**Komentar**: Za razbiranje igralcev vsake epizode se nisem odločil, saj se ponavadi igralci v isti seriji pojavljajo v (skoraj) vsaki epizodi, torej bi s tem prišel do nepotrebnega ponavljanja podatkov. To, da se neka serija pojavi večkrat, namreč razberemo že z naslovom serije.


## Uvoz podatkov

Po uvozu podatkov s pomočjo datoteke `uvoz_podatkov.py` sem pridobil želene podatke, ki sem jih shranil v 3 različne csv datoteke ter eno skupno json datoteko. Datoteka `vse_epizode.json` torej vsebuje vse podatke za posamezno epizodo, datoteka `vse_epizode.csv` pa ji je zelo podobna, vendar slednja ne vsebuje režiserjev in zvrsti za posamezno epizodo, saj imamo v ta namen še dve pomožno datoteki. Prva, `reziserji.csv`, vsebuje id posamezne serije ter njene režiserje, druga, `zanri.csv` pa za vsako serijo pove njene žanre. Pri tem je bilo seveda nesmiselno shranjevati žanre za posamezne epizode, saj imajo vse epizode iste serije iste žanre.

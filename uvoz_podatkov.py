import orodja
import re



###############################################################################
# Najprej preberimo podatke iz interneta in stran zapišimo v obliko besedila.
###############################################################################

orodja.pripravi_imenik("spletna.csv")

for i in range(1, 9):
    url = (
        "https://www.imdb.com/search/title?num_votes=2000,&sort=user_rating,"
        "desc&title_type=tv_episode&view=advanced&page={}&count=500&ref_=adv_nxt'"
    ).format(i)
    orodja.shrani_spletno_stran(url, "serije-{}.html".format(i))

besedilo = ""
for i in range(1, 9):
    besedilo = besedilo + "\n" + orodja.vsebina_datoteke("serije-{}.html".format(i))


###############################################################################
# Iz dobljenega besedila želimo ustvariti slovar z iskanimi podatki.
###############################################################################

def poisci_epizode(niz):
    '''Funkcija, ki celoten niz razdeli na posamezne epizode.'''
    vzorec = re.compile(
        r"class=\"loadlate\""
        r"(.*?)"
        r"\n\n",
        re.DOTALL
        )
    seznam = []
    for ujemanje in vzorec.finditer(niz):
        seznam.append(ujemanje.group(1))
    return seznam

vzorec_epizode = re.compile(
    r"<span class=\"lister-item-index unbold text-primary\">"
    r"\d\.</span>.*?<a href=.*?>(?P<serija>.*?)</a>.*?"
    r"</small>.*?<a href=.*?>(?P<epizoda>.*?)</a>.*?"
#    r"<span class=\"lister-item-year text-muted unbold\">\((?P<leto>\d{4})\)</span.>.*?"
    r"<span class=\"runtime\">(?P<dolzina>.*?) min</span>.*?"
    r"<span class=\"genre\">(?P<zvrst>.*?)</span>.*?"
    r"imdb-rating\"></span>.*?<strong>(?P<ocena>.*?)</strong>.*?"
    r"Director:.*?>(?P<reziser>.*?)</a>.*?"
    r"<span name=\"nv\" data-value=\"\d+?\">(?P<st_glasov>.*?)</span>.*?",
    re.DOTALL
)

def pocisti_podatke(podatki):
    podatki['serija'] = podatki['serija'].strip()
    podatki['epizoda'] = podatki['epizoda'].strip()
#    podatki['leto'] = int(podatki['leto'])
    podatki['dolzina'] = int(podatki['dolzina'])
    podatki['zvrst'] = podatki['zvrst'].strip()
    podatki['zvrst'] = podatki['zvrst'].split(',')
    podatki['ocena'] = float(podatki['ocena'])
    podatki['reziser'] = podatki['reziser'].strip()
    podatki['st_glasov'] = float(podatki['st_glasov'].replace(',', '.'))
    return podatki

zapis_serij = []
for ujemanje in vzorec_epizode.finditer(besedilo):
    podatki_epizode = pocisti_podatke(ujemanje.groupdict())
    zapis_serij.append(podatki_epizode)


###############################################################################
# Podatke še zapišemo v csv in json datoteki.
###############################################################################

orodja.zapisi_json(zapis_serij, 'vse_epizode.json')

orodja.zapisi_csv(zapis_serij, ["serija", "epizoda", "leto", "dolzina",
    "zvrst", "ocena", "reziser", "st_glasov"], 'vse_epizode.csv')

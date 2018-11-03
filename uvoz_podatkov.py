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
    r"\d*,?\d*\.</span>.*?<a href=.*?>(?P<serija>.+?)</a>.*?"
    r"</small>.*?<a href=\"/title/tt(?P<id>\d+)/\?ref_=adv_li_tt\"[^>]*?"
    r">(?P<epizoda>.+?)</a>.*?"
    r"<span class=\"lister-item-year text-muted unbold\">\(\D*?\s?(?P<leto>\d+)\)</span>.*?"
    r"(<span class=\"runtime\">?(?P<dolzina>.*?) min</span>?.*?)?"
    r"<span class=\"genre\">(?P<zanr>.+?)</span>.*?"
    r"imdb-rating\"></span>.*?<strong>(?P<ocena>.+?)</strong>.*?"
    r"Directors?:(?P<reziserji>.+?)<span class=\"ghost\">.*?"
    r"<span name=\"nv\" data-value=\"\d+?\">(?P<st_glasov>.+?)</span>.*?",
    re.DOTALL
)


vzorec_osebe = re.compile(
    r"<a\s+href=\"/name/nm(?P<id>\d+)/?[^>]*?>(?P<ime>.+?)</a>",
    re.DOTALL
)


def izloci_osebe(niz):
    osebe = []
    for oseba in vzorec_osebe.finditer(niz):
        osebe.append({
            'id': int(oseba.groupdict()['id']),
            'ime': oseba.groupdict()['ime'],
        })
    return osebe


def izloci_zanre(epizode):
    zanri = []
    for element in epizode:
        for zanr in element.pop('zanr'):
            zanri.append({'serija': element['serija'], 'zanr': zanr})
    zanri.sort(key=lambda zanr: (zanr['serija'], zanr['zanr']))
    return zanri


def izloci_reziserje(epizode):
    vloge = []
    for element in epizode:
        for reziser in element.pop('reziserji'):
            vloge.append({'epizoda': element['id'], 'reziser': reziser['ime']})
    vloge.sort(key=lambda vloga: (vloga['epizoda'], vloga['reziser']))
    return vloge


def pocisti_podatke(podatki):
    podatki['serija'] = podatki['serija'].strip()
    podatki['epizoda'] = podatki['epizoda'].strip()
    podatki['leto'] = int(podatki['leto'])
    ## Problem nastopi pri prvi razbrani epizodi; ker gre za komično serijo, 
    ## nastavimo njeno dolžino na 20 min
    if podatki['dolzina']:
        podatki['dolzina'] = int(podatki['dolzina'])
    else:
        podatki['dolzina'] = 20
    podatki['zanr'] = podatki['zanr'].strip().split(', ')
    podatki['ocena'] = float(podatki['ocena'])
    podatki['reziserji'] = izloci_osebe(podatki['reziserji'])
    podatki['st_glasov'] = int(podatki['st_glasov'].replace(',', ''))
    return podatki


zapis_serij = []
razbitje = poisci_epizode(besedilo)
for i in range(0, len(razbitje)):
    for ujemanje in vzorec_epizode.finditer(razbitje[i]):
        podatki_epizode = pocisti_podatke(ujemanje.groupdict())
        zapis_serij.append(podatki_epizode)



###############################################################################
# Podatke zapišemo v json datoteko.
###############################################################################

orodja.zapisi_json(zapis_serij, 'vse_epizode.json')



###############################################################################
# Nato pa jih dokončno predelamo in zapišemo še v csv datoteke.
###############################################################################

zanri = izloci_zanre(zapis_serij)
vloge = izloci_reziserje(zapis_serij)

# Znebimo se nepotrebnih ponovitev zapisa žanrov posamezne serije

posodobi_zanre = []
for element in zanri:
    if element not in posodobi_zanre:
        posodobi_zanre.append(element)

zanri = posodobi_zanre

zapis_serij.sort(key=lambda epizoda: epizoda['id'])

orodja.zapisi_csv(zapis_serij, ["id", "serija", "epizoda", "leto", "dolzina",
    "ocena", "st_glasov"], 'vse_epizode.csv')
orodja.zapisi_csv(vloge, ["epizoda", "reziser"], 'reziserji.csv')    
orodja.zapisi_csv(zanri, ["serija", "zanr"], 'zanri.csv')

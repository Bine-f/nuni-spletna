# Spletna stran Matevž Nunar

Statična spletna stran s sedmimi podstranmi. Vsebina (besedila, rezultati, slike) je v mapi `content/`, videz pa v `static/style.css`. Skripta `build.py` iz tega zgradi končno stran v mapo `dist/`.

## Mape

| Mapa ali datoteka | Kaj je v njej |
|---|---|
| `content/*.json` | Vsa besedila, rezultati, seznam slik in kontakti. To ureja Matevž (prek Pages CMS). |
| `static/img/` | Slike, ki jih stran uporablja. |
| `static/style.css` | Barve, pisave, postavitev. |
| `build.py` | Zgradi stran v `dist/`. Ne potrebuje dodatnih knjižnic. |
| `.pages.yml` | Nastavitve urejevalnika Pages CMS. |
| `dist/` | Zgrajena stran. To se objavi. Ne urejaj je ročno, ker jo `build.py` vsakič prepiše. |

## Lokalni preizkus

**Samo ogled:** odpri `dist\index.html` z dvoklikom. Stran se odpre v brskalniku in povezave med podstranmi delujejo.

**Po spremembi vsebine:**

1. Enkrat namesti Python s [python.org/downloads](https://www.python.org/downloads/). Pri namestitvi obkljukaj **Add python.exe to PATH**.
2. Spremeni kaj v `content/*.json` (npr. v VS Codu).
3. Dvoklikni `zazeni.bat`. Stran se zgradi na novo in odpre v brskalniku.

Ročno v terminalu: `python build.py`, nato odpri `dist\index.html`.

Pri urejanju JSON datotek pazi na narekovaje in vejice. Če `build.py` javi napako, je skoraj vedno v JSON datoteki, ki jo je izpisal.

## Objava (enkratna nastavitev)

1. **GitHub:** ustvari repozitorij (npr. `nuni-spletna`) in vanj naloži vsebino te mape, brez mape `dist/`.
2. **Cloudflare Pages:** v Cloudflaru izberi *Workers & Pages → Create → Pages → Connect to Git*, izberi repozitorij in nastavi:
   - Build command: `python build.py`
   - Build output directory: `dist`
3. **Domena:** v projektu na Cloudflare Pages izberi *Custom domains* in dodaj domeno. Cloudflare pove, kateri DNS zapis dodati pri ponudniku domene (ali pa domeno v celoti preneseš na Cloudflare DNS). HTTPS se nastavi sam.
4. **Urejevalnik:** Matevž se prijavi na [app.pagescms.org](https://app.pagescms.org) z GitHub računom in izbere repozitorij. Urejevalnik prebere `.pages.yml`.
5. **Kontaktni obrazec:** na [web3forms.com](https://web3forms.com) vpiši Matevžev e-poštni naslov, dobiš ključ (Access Key) in ga v Pages CMS vpišeš pod *Kontakt → Web3Forms ključ*. Sporočila nato prihajajo na ta naslov.

Ko Matevž v Pages CMS shrani spremembo, Cloudflare stran v približno minuti zgradi in objavi na novo.

## Nasveti za slike

- Fotografije iz fotoaparata imajo 10 do 20 MB, kar stran zelo upočasni. Pred nalaganjem jih pomanjšaj na približno 2000 px po daljši stranici, npr. na [squoosh.app](https://squoosh.app) (format WebP ali JPG, kakovost okoli 75).
- Za naslovne fotografije so najboljše ležeče fotografije, kjer je oseba bolj na sredini ali desno, ker je naslov levo spodaj.

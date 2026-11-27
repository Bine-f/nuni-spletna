"""Zgradi spletno stran iz datotek v mapi content/ v mapo dist/.

Zagon:  python build.py
Vsebino urejaš v content/*.json (ali prek Pages CMS), videz v static/style.css.
Nobenih dodatnih knjižnic ni treba namestiti, dovolj je Python 3.
"""
import html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'dist')
ARTIFACT = '--artifact' in sys.argv  # interna možnost za Claudov predogled


def load(name):
    with open(os.path.join(ROOT, 'content', name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def e(s):
    return html.escape(str(s or ''), quote=True)


def paras(text):
    """Besedilo z delitvijo na odstavke (prazna vrstica) pretvori v <p>."""
    parts = [p.strip() for p in str(text or '').replace('\r', '').split('\n\n') if p.strip()]
    return '\n'.join(f'<p>{e(p)}</p>' for p in parts)


def img(path):
    return e(str(path or '').lstrip('/'))


PAGES = [
    ('index.html', 'Domov'),
    ('zgodba.html', 'Moja zgodba'),
    ('rezultati.html', 'Rezultati'),
    ('trenerstvo.html', 'Trenerstvo'),
    ('partnerji.html', 'Partnerji'),
    ('galerija.html', 'Galerija'),
    ('kontakt.html', 'Kontakt'),
]

K = load('kontakt')


def links(cur):
    return '\n'.join(
        f'<li><a href="{f}"{" aria-current=" + chr(34) + "page" + chr(34) if f == cur else ""}>{label}</a></li>'
        for f, label in PAGES)


def nav(cur):
    lang = '<span class="lang" title="Angleška verzija pride kasneje"><b>SLO</b> / ANG</span>'
    return f'''<header class="nav">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Domov"><img src="img/logo-white.png" alt="MN" width="67" height="28"></a>
    <div class="menu"><ul>{links(cur)}</ul>{lang}</div>
    <details class="burger"><summary>Meni</summary><nav aria-label="Meni"><ul>{links(cur)}</ul>{lang}</nav></details>
  </div>
</header>'''


def footer():
    items = [f'<a href="kontakt.html">{e(K["email"])}</a>']
    if K.get('instagram'):
        items.append(f'<a href="{e(K["instagram"])}" target="_blank" rel="noopener">Instagram</a>')
    if K.get('strava'):
        items.append(f'<a href="{e(K["strava"])}" target="_blank" rel="noopener">Strava</a>')
    items.append('<a href="partnerji.html">Za partnerje</a>')
    return f'''<footer>
  <div class="wrap">
    <span>© 2026 Matevž Nunar · Profesionalni triatlonec in trener</span>
    <span class="foot-nav">{''.join(items)}</span>
  </div>
</footer>'''


# Kje na posamezni naslovni fotografiji je bistveni del (x% y%).
HERO_POS = {'img/ph-partner.webp': '50% 6%', 'img/ph-galerija.webp': '25% 58%', 'img/ph-rezultati.webp': '50% 35%'}


def page_hero(eyebrow, title, image, pos=None):
    pos = pos or HERO_POS.get(image, '50% 50%')
    return f'''<section class="page-hero">
  <img src="{img(image)}" alt="" style="object-position:{pos}">
  <div class="wrap"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(title)}</h1></div>
</section>'''


# ---------------- strani ----------------
def page_home():
    d = load('domov'); z = d['zadnji_rezultat']
    teasers = ''.join(
        f'<a class="teaser" href="{href}"><img src="{img(d[key]["slika"])}" alt="" loading="lazy"><h3>{label}</h3><p>{e(d[key]["besedilo"])}</p></a>'
        for href, key, label in [('zgodba.html', 'kartica_zgodba', 'Moja zgodba'),
                                 ('rezultati.html', 'kartica_rezultati', 'Rezultati'),
                                 ('trenerstvo.html', 'kartica_trenerstvo', 'Trenerstvo')])
    ime = '<br>'.join(e(w) for w in d['ime'].split(' ', 1))
    return f'''<header class="hero" id="top">
  <img src="{img(d['slika'])}" alt="{e(d['ime'])}" fetchpriority="high">
  <div class="wrap">
    <p class="role">{e(d['vloga'])}</p>
    <h1>{ime}</h1>
    <p class="motto">{e(d['moto_1'])} <em>{e(d['moto_2'])}</em></p>
    <div class="cta"><a class="btn primary" href="trenerstvo.html">Treniraj z mano</a><a class="btn" href="partnerji.html">Za partnerje</a></div>
  </div>
</header>
<section class="latest" aria-label="Zadnji rezultat">
  <div class="wrap">
    <div class="place">{e(z['mesto'])}<small>.</small></div>
    <div>
      <p class="eyebrow">Zadnji rezultat · {e(z['datum'])}</p>
      <h3>{e(z['naslov'])}</h3>
      <p class="meta">{e(z['opis'])}</p>
      <div class="splits"><span>Plavanje <b>{e(z['plavanje'])}</b></span><span>Kolo <b>{e(z['kolo'])}</b></span><span>Tek <b>{e(z['tek'])}</b></span></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <p class="eyebrow">O meni</p>
    <h2>{e(d['uvod_naslov'])}</h2>
    <p class="lead" style="margin-top:22px">{e(d['uvod'])}</p>
    <div class="teasers">{teasers}</div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <h2>{e(d['pasica'])}</h2>
    <div class="cta" style="margin-top:0"><a class="btn primary" href="partnerji.html">Za sponzorje in partnerje</a><a class="btn" href="kontakt.html">Kontakt</a></div>
  </div>
</section>'''


def page_story():
    d = load('zgodba'); r = d['razdalja']
    ch = []
    for i, p in enumerate(d['poglavja']):
        extra = ''
        if i == len(d['poglavja']) - 1:
            extra = f'''<div class="distance" aria-label="Srednja triatlonska razdalja">
            <div><b>{e(r['plavanje'])}</b><span>plavanje</span></div><div><b>{e(r['kolo'])}</b><span>kolo</span></div>
            <div><b>{e(r['tek'])}</b><span>tek</span></div><div><b>{e(r['cas'])}</b><span>moj čas</span></div></div>'''
        ch.append(f'''<article class="chapter"><span class="yr">{e(p['oznaka'])}</span><h3>{e(p['naslov'])}</h3>
          <div class="prose">{paras(p['besedilo'])}</div>{extra}</article>''')
    cap = f'<figcaption>Foto: {e(d["portret_avtor"])}</figcaption>' if d.get('portret_avtor') else ''
    return page_hero('Moja zgodba', d['naslov'], d['slika']) + f'''
<section><div class="wrap"><div class="story-grid" style="margin-top:0">
  <figure><img src="{img(d['portret'])}" alt="Portret Matevža Nunarja">{cap}</figure>
  <div class="chapters">{''.join(ch)}</div>
</div></div></section>'''


def page_results():
    d = load('rezultati')
    pro = ''.join(
        f'<tr{" class=" + chr(34) + "win" + chr(34) if str(x["mesto"]).strip() == "1" else ""}><td class="pos">{e(x["mesto"])}.</td><td class="num">{e(x["datum"])}</td>'
        f'<td>{e(x["tekma"])}</td><td class="t">{e(x["cas"])}</td><td class="t"><small>{e(x["plavanje"])} / {e(x["kolo"])} / {e(x["tek"])}</small></td></tr>'
        for x in d['profesionalne'])
    dp = ''.join(
        f'<tr{" class=" + chr(34) + "win" + chr(34) if str(x["mesto"]).strip() == "1" else ""}><td class="pos">{e(x["mesto"])}.</td><td class="num">{e(x["datum"])}</td>'
        f'<td>{e(x["tekma"])}{" · " + e(x["opomba"]) if x.get("opomba") else ""}</td><td class="t">{e(x["cas"])}</td></tr>'
        for x in d['drzavna'])
    nxt = ''.join(
        f'<div><span>{e(x["serija"])}{" · " + e(x["datum"]) if x.get("datum") else ""}</span><b>{e(x["tekma"])}</b></div>'
        for x in d['prihajajoce'])
    note = f'<p class="note">{e(d["opomba"])}</p>' if d.get('opomba') else ''
    return page_hero('Rezultati', d['naslov'], d['slika']) + f'''
<section><div class="wrap">
  <div class="tbl-wrap"><table>
    <thead><tr><th>Mesto</th><th>Datum</th><th>Tekma</th><th>Čas</th><th>Plavanje / kolo / tek</th></tr></thead>
    <tbody>{pro}</tbody></table></div>
  <h3 class="subhead">{e(d['drzavna_naslov'])}</h3>
  <div class="tbl-wrap"><table>
    <thead><tr><th>Mesto</th><th>Datum</th><th>Tekma</th><th>Čas</th></tr></thead>
    <tbody>{dp}</tbody></table></div>
  <h3 class="subhead">{e(d['sezona_naslov'])}</h3>
  <div class="next">{nxt}</div>{note}
</div></section>'''


def page_coach():
    d = load('trenerstvo')
    pillars = ''.join(f'<li><b>{e(p["naslov"])}</b><span>{e(p["besedilo"])}</span></li>' for p in d['stebri'])
    return page_hero('Trenerstvo', d['naslov'], d['slika']) + f'''
<section><div class="wrap split">
  <div>
    <p class="eyebrow">Trenerstvo</p><h2>{e(d['podnaslov'])}</h2>
    <div class="prose" style="margin-top:22px">{paras(d['besedilo'])}</div>
    <ul class="pillars">{pillars}</ul>
    <div class="cta"><a class="btn primary" href="kontakt.html">Piši mi za sodelovanje</a></div>
  </div>
  <img src="{img(d['slika_ob_besedilu'])}" alt="" loading="lazy">
</div></section>
<section class="band"><div class="wrap">
  <div><p class="eyebrow">Paketi in cene</p><h2>{e(d['paketi_naslov'])}</h2></div>
  <div class="prose" style="max-width:40ch;color:var(--muted)">{paras(d['paketi_besedilo'])}</div>
</div></section>'''


def page_partners():
    d = load('partnerji')
    if d.get('partnerji'):
        logos = ''.join(
            (f'<a href="{e(p["povezava"])}" target="_blank" rel="noopener">' if p.get('povezava') else '<span>')
            + f'<img src="{img(p["logo"])}" alt="{e(p["ime"])}" loading="lazy">'
            + ('</a>' if p.get('povezava') else '</span>')
            for p in d['partnerji'])
        logos = f'<div class="logos">{logos}</div>'
    else:
        logos = f'<p class="empty">{e(d["prazno"])}</p>'
    return page_hero('Za sponzorje in partnerje', d['naslov'], d['slika']) + f'''
<section><div class="wrap">
  <div class="partner-grid" style="margin-top:0">
    <div class="prose">{paras(d['besedilo'])}</div>
    <div><h3>Sodelujva</h3><p style="color:var(--muted);margin-top:10px">{e(d['poziv'])}</p>
      <div class="cta"><a class="btn primary" href="kontakt.html">Pošlji povpraševanje</a></div></div>
  </div>
  <h3 class="subhead">Partnerji</h3>
  {logos}
</div></section>'''


GAL_PATTERN = ['a', 'b', 'c', 'c', 'c', 'd', 'e']


def page_gallery():
    d = load('galerija')
    imgs = '\n'.join(
        f'<img class="{GAL_PATTERN[i % len(GAL_PATTERN)]}" src="{img(x["slika"])}" alt="{e(x.get("opis"))}" loading="lazy">'
        for i, x in enumerate(d['slike']))
    note = f'<p class="note">{e(d["avtorji"])}</p>' if d.get('avtorji') else ''
    return page_hero('Galerija', d['naslov'], d['slika']) + f'''
<section><div class="wrap">
  <div class="gallery big" style="margin-top:0">{imgs}</div>{note}
</div></section>'''


def page_contact():
    d = K
    tel = ''.join(ch for ch in d['telefon'] if ch.isdigit() or ch == '+')
    items = [('E-pošta', f'<a href="mailto:{e(d["email"])}">{e(d["email"])}</a>'),
             ('Telefon', f'<a href="tel:{e(tel)}">{e(d["telefon"])}</a>')]
    if d.get('instagram'):
        handle = '@' + d['instagram'].rstrip('/').split('/')[-1].split('?')[0]
        items.append(('Instagram', f'<a href="{e(d["instagram"])}" target="_blank" rel="noopener">{e(handle)}</a>'))
    if d.get('strava'):
        items.append(('Strava', f'<a href="{e(d["strava"])}" target="_blank" rel="noopener">Matevž Nunar na Stravi</a>'))
    lst = ''.join(f'<div><span>{k}</span>{v}</div>' for k, v in items)
    key = e(d.get('web3forms_kljuc', ''))
    return page_hero('Kontakt', d['naslov'], d['slika']) + f'''
<section><div class="wrap contact-grid">
  <div class="contact-list">{lst}</div>
  <form id="contact-form" novalidate data-key="{key}">
    <h3>Pošlji sporočilo</h3>
    <label for="f-name">Ime in priimek<input id="f-name" name="name" required autocomplete="name"></label>
    <label for="f-company">Podjetje<input id="f-company" name="company" autocomplete="organization"></label>
    <label for="f-email">E-pošta<input id="f-email" name="email" type="email" required autocomplete="email"></label>
    <label for="f-type">Zanima me<select id="f-type" name="subject"><option>Sponzorstvo</option><option>Trenerstvo</option><option>Mediji</option><option>Drugo</option></select></label>
    <label for="f-msg">Sporočilo<textarea id="f-msg" name="message"></textarea></label>
    <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
    <button class="btn primary" type="submit">Pošlji</button>
    <p id="form-msg" role="status"></p>
  </form>
</div></section>
<script>
(function(){{
  var form=document.getElementById('contact-form'), msg=document.getElementById('form-msg');
  form.addEventListener('submit',function(ev){{
    ev.preventDefault();
    var name=form.name.value.trim(), email=form.email.value.trim();
    if(!name||email.indexOf('@')<1){{msg.textContent='Vpiši ime in veljaven e-poštni naslov.';return;}}
    var key=form.dataset.key;
    if(!key){{msg.textContent='Obrazec še ni povezan. Piši mi na {e(d["email"])}.';return;}}
    var data=new FormData(form); data.append('access_key',key); data.set('subject','Spletna stran: '+form.subject.value);
    msg.textContent='Pošiljam ...';
    fetch('https://api.web3forms.com/submit',{{method:'POST',body:data}}).then(function(r){{return r.json();}}).then(function(j){{
      if(j.success){{form.reset();msg.textContent='Hvala! Sporočilo je poslano, odgovorim v kratkem.';}}
      else{{msg.textContent='Sporočila ni bilo mogoče poslati. Piši mi na {e(d["email"])}.';}}
    }}).catch(function(){{msg.textContent='Sporočila ni bilo mogoče poslati. Piši mi na {e(d["email"])}.';}});
  }});
}})();
</script>'''


BODIES = {
    'index.html': (page_home, 'Matevž Nunar'),
    'zgodba.html': (page_story, 'Moja zgodba · Matevž Nunar'),
    'rezultati.html': (page_results, 'Rezultati · Matevž Nunar'),
    'trenerstvo.html': (page_coach, 'Trenerstvo · Matevž Nunar'),
    'partnerji.html': (page_partners, 'Partnerji · Matevž Nunar'),
    'galerija.html': (page_gallery, 'Galerija · Matevž Nunar'),
    'kontakt.html': (page_contact, 'Kontakt · Matevž Nunar'),
}

HEAD_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=Figtree:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="style.css">'''


def render(f):
    fn, title = BODIES[f]
    head = (f'<title>{e(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<meta name="description" content="Matevž Nunar, profesionalni triatlonec in trener.">\n'
            f'<link rel="icon" href="img/logo-black.png">\n{HEAD_LINKS}\n')
    main = f'{nav(f)}\n<main>\n{fn()}\n</main>\n{footer()}\n'
    if ARTIFACT and f == 'index.html':
        return head + main
    return ('<!doctype html>\n<html lang="sl">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + main + '</body>\n</html>\n')


def main():
    out = OUT + ('-artifact' if ARTIFACT else '')
    # Prepiše obstoječe datoteke (ne briše mape, da deluje tudi, ko je stran odprta v brskalniku).
    shutil.copytree(os.path.join(ROOT, 'static'), out, dirs_exist_ok=True)
    for f, _ in PAGES:
        with open(os.path.join(out, f), 'w', encoding='utf-8') as fh:
            fh.write(render(f))
    print('Stran zgrajena v', os.path.relpath(out, ROOT), '(' + ', '.join(f for f, _ in PAGES) + ')')


if __name__ == '__main__':
    main()

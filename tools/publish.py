# -*- coding: utf-8 -*-
"""Drop a newly exported one-pager into the repo as index.html.

    python tools/publish.py "C:/Users/user/Downloads/Exosomes_Spain2026_OnePage_v5.html"

The exported HTML never carries these, so they are re-applied every time:
  1. Open Graph / Twitter meta tags (link previews).
  2. Masking of the Spain partner's contact details — the repo is public and the
     deck's own internal note asks for permission before external distribution.
"""
import io, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'index.html')
BASE = 'https://baelab-create.github.io/drbae-spain2026/'
DESC = ('La verdad sobre los exosomas \u2014 de exosomas humanos a ves\u00edculas extracelulares '
        'vegetales. Ciencia, regulaci\u00f3n, formulaci\u00f3n y aplicaciones profesionales '
        'en piel y cuero cabelludo.')
TITLE = 'Exosomes in Professional Aesthetic Care \u2014 Spain 2026'

META = '''
<meta content="{d}" name="description"/>
<meta content="website" property="og:type"/>
<meta content="Dr. BAE | Exotokine" property="og:site_name"/>
<meta content="{t}" property="og:title"/>
<meta content="{d}" property="og:description"/>
<meta content="{b}" property="og:url"/>
<meta content="{b}assets/og-spain2026.jpg" property="og:image"/>
<meta content="{b}assets/og-spain2026.jpg" property="og:image:secure_url"/>
<meta content="image/jpeg" property="og:image:type"/>
<meta content="1200" property="og:image:width"/>
<meta content="630" property="og:image:height"/>
<meta content="Dr. BAE Exotokine \u2014 BLUE, TOCOFORTE, BLACK SCALP, PIDIROENNE PINK" property="og:image:alt"/>
<meta content="es_ES" property="og:locale"/>
<meta content="ko_KR" property="og:locale:alternate"/>
<meta content="en_US" property="og:locale:alternate"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{t}" name="twitter:title"/>
<meta content="{d}" name="twitter:description"/>
<meta content="{b}assets/og-spain2026.jpg" name="twitter:image"/>
<link href="{b}" rel="canonical"/>'''.format(d=DESC, t=TITLE, b=BASE)

VIEWPORT = '<meta content="width=device-width,initial-scale=1" name="viewport"/>'
CONTACT_RE = re.compile(r'<div class="src">\s*francis@peanillacosmetics\.es.*?</div>', re.S)
CONTACT_SAFE = '<div class="src">Contacto \u00b7 Peanilla Cosmetics (Espa\u00f1a)</div>'
# any stray phone / e-mail outside that block should stop the publish
LEAKS = [re.compile(r'francis@peanillacosmetics'), re.compile(r'611\s*052\s*657')]


def main(src):
    shutil.copyfile(src, PAGE)
    h = io.open(PAGE, encoding='utf-8').read()

    if 'og:image' in h:
        print('  og tags   : already present, skipped')
    else:
        if VIEWPORT not in h:
            raise SystemExit('viewport meta not found - cannot anchor og tags')
        h = h.replace(VIEWPORT, VIEWPORT + META, 1)
        print('  og tags   : inserted')

    h, n = CONTACT_RE.subn(CONTACT_SAFE, h)
    print('  contact   : masked (%d block%s)' % (n, '' if n == 1 else 's'))

    io.open(PAGE, 'w', encoding='utf-8', newline='').write(h)

    leaked = [p.pattern for p in LEAKS if p.search(h)]
    if leaked:
        raise SystemExit('LEFTOVER CONTACT DETAILS -> ' + ', '.join(leaked) +
                         '\n  fix index.html before committing')
    print('  leak check: clean')
    print('  -> index.html updated from', os.path.basename(src))
    print('  next: python tools/make_og.py   (only if the product shots changed)')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])

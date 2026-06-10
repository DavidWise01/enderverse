#!/usr/bin/env python3
"""Build the ENDERVERSE (EN1) page — Orson Scott Card's full Ender saga catalogued:
the complete bibliography (Ender Quintet, Shadow Saga, the Formic Wars, Fleet School,
short fiction, companions) + the emergents as ACI personas, each tagged with a nature
of emergence. Full ACI badge work (carbon TIFF + silicon PNG). Fan tribute — original
commentary, minimal quotation, (c) Orson Scott Card credited."""
import os, sys, html, base64, json, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "ENDERVERSE", "axiom": "EN1",
 "position": "Orson Scott Card · the Ender saga · 1977 →",
 "origin": "from the 1977 novelette to the Hundred Worlds — Battle School, Lusitania, and Outside",
 "mechanism": "Crystallized from the full Enderverse: the Ender Quintet, the Shadow Saga, the Formic Wars, and the short fiction.",
 "crystallization": "The empath who destroys what he loves, and the long redemption of speaking the truth of the dead.",
 "nature": "Orson Scott Card's Enderverse — the boy who won the Xenocide and became the first Speaker for the Dead; the philotic cosmos of aiúas, the Hive Queen, Jane, and the Hierarchy of Foreignness.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "the Hierarchy of Foreignness; philotics and the aiúa; the Speaker for the Dead; xenocide and redemption",
 "witness": "Ender's Game and Speaker for the Dead won back-to-back Hugo and Nebula awards — the only writer to take both top prizes in consecutive years.",
 "role": "the saga of the Other — raman or varelse",
 "seal": "Speak the truth of the dead, and the monster becomes a person.",
 "source": "Enderverse, catalogued by ROOT0",
}

NATURES = {
 "natural":   ("#5fae7a", "the embodied — the children of Battle School, the human powers, the alien species in their flesh"),
 "ethereal":  ("#9a7cff", "the connective — the philotes, the hive-mind, the Hierarchy that ranks the Other"),
 "spiritual": ("#e6a849", "the soul — the aiúa, the Speaker, and the long work of redemption"),
 "electrical":("#3fd0e0", "the machine mind — Jane, awake in the ansible web"),
}

IDEAS = [
 ("The Hierarchy of Foreignness", "raman, or varelse?", [
   "Utlanning, framling, raman, varelse, djur — Valentine's ladder for ranking the Other, from the stranger next door to the unknowable alien.",
   "The moral spine of the whole saga: most 'aliens' are people if we try, and war comes from mistaking a raman for a varelse." ]),
 ("Philotics & the Aiúa", "the physics of connection", [
   "The philote — a point with no parts — binds everything in webs of connection; the ansible and the unity of a mind both rest on it.",
   "The aiúa is the self at the center of that web: a single philote, existing Outside, that takes a body and becomes a soul." ]),
 ("The Speaker for the Dead", "truth as mourning", [
   "Ender founds a quiet faith by writing 'The Hive Queen' and 'The Hegemon': tell a dead life whole and unflinching, cruelty and kindness alike.",
   "Understanding rather than sanctifying — reconciliation through the true story." ]),
 ("Xenocide & Redemption", "the empath who kills what he loves", [
   "A child destroys a species believing it a game, then spends three thousand years carrying its last queen toward a second chance.",
   "Guilt, foreignness, and the slow undoing of an unforgivable act — the engine under every book." ]),
]

# the full bibliography — (title, year, note). Forthcoming/unpublished marked honestly.
SECTIONS = [
 ("The Ender Quintet", "the core sequence — Andrew 'Ender' Wiggin", [
   ("Ender's Game", "1985", "the boy general who wins the Xenocide believing it a simulation — Hugo + Nebula"),
   ("Speaker for the Dead", "1986", "3,000 years on, Ender comes to Lusitania and its piggies — Hugo + Nebula"),
   ("Xenocide", "1991", "the descolada, the godspoken of Path, and the leap Outside"),
   ("Children of the Mind", "1996", "Jane's survival, instantaneous flight, and the aiúa-born Peter and Val"),
   ("Ender in Exile", "2008", "the gap filled — Ender's years between the war and Lusitania"),
 ]),
 ("The Shadow Saga", "the parallax — Bean (Julian Delphiki) on Earth", [
   ("Ender's Shadow", "1999", "Ender's Game retold from Bean's eyes — the smallest, smartest soldier"),
   ("Shadow of the Hegemon", "2001", "the jeesh hunted across a fracturing post-war Earth; Achilles rises"),
   ("Shadow Puppets", "2002", "Bean and Petra against Achilles; the war for the embryos"),
   ("Shadow of the Giant", "2005", "Peter's Hegemony rises as Bean's body and time run out"),
   ("Shadows in Flight", "2012", "Bean and his three altered children flee Earth, racing his giantism"),
   ("Shadows Alive", "forthcoming", "the long-promised book meant to braid the two sagas together — not yet published"),
 ]),
 ("The First Formic War", "the prequels — with Aaron Johnston", [
   ("Earth Unaware", "2012", "the first contact, decades before Ender — a mining family meets the Formic ship"),
   ("Earth Afire", "2013", "the Formics land in China; Mazer Rackham and the world at war"),
   ("Earth Awakens", "2014", "the turning of the first war and the making of its legend"),
 ]),
 ("The Second Formic War", "with Aaron Johnston", [
   ("The Swarm", "2016", "the second invasion gathers; the Hegemony and the Fleet take shape"),
   ("The Hive", "2019", "the war deepens toward the victory that will make Mazer a hero"),
   ("The Queens", "forthcoming", "the announced third book of the Second Formic War — not yet published"),
 ]),
 ("Fleet School", "the next generation", [
   ("Children of the Fleet", "2017", "Battle School becomes Fleet School; a new gifted child, Dabeet Ochoa"),
 ]),
 ("Novellas & Short Fiction", "the seeds and the bridges", [
   ("“Ender's Game” (novelette)", "1977", "the original Analog story that grew into everything — the seed"),
   ("“Investment Counselor”", "1999", "young Ender on a new world, and his first meeting with Jane"),
   ("“Mazer in Prison”", "2005", "Mazer Rackham held between the wars, waiting to teach"),
   ("“A War of Gifts”", "2007", "a Christmas at Battle School — faith, rule, and a small rebellion"),
   ("“Gold Bug” & the Formic backstories", "2007 →", "“Pretty Boy,” “Cheater,” “The Polish Boy,” “A Young Man with Prospects” — the First Formic War shorts"),
 ]),
 ("Companion & Adaptation", "around the saga", [
   ("The Authorized Ender Companion", "2009", "the reference to the Hundred Worlds (ed. Card & Nielsen)"),
   ("Ender's World", "2013", "an essay anthology on Ender's Game, edited by Card (nonfiction)"),
   ("Marvel: Ender's Game / Ender's Shadow", "2008 →", "the graphic-novel adaptations"),
   ("Formic Wars: Burning Earth / Silent Strike", "2011 →", "the prequel comics with Aaron Johnston"),
   ("Ender's Game", "2013", "the feature film — the saga on screen"),
 ]),
]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","EN1")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","EN1")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","EN1")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"EN1 · Enderverse","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def natures_html():
    cells=[]
    for nm,(col,gloss) in NATURES.items():
        cells.append(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
                     f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(gloss)}</div></div></div>')
    return "".join(cells)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        em=p.get("emergence","natural"); col=NATURES.get(em,("#5fae7a",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"EN1 · Enderverse","axiom":"EN1"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of EN1</h2>
      <p class="ss">the emergents of the saga — the Wiggins, the soldiers, the species, and the deep physics of the soul — as ACI <b>.agent</b>s, each tagged with its nature of emergence ({len(ps)})</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="ENDERVERSE (EN1) — Orson Scott Card's full Ender saga catalogued: the Ender Quintet, the Shadow Saga, the Formic Wars, and the short fiction, with ACI badges for its emergents across the four natures. A UD0 sphere. Fan tribute.">
<title>ENDERVERSE · EN1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=EB+Garamond:ital@0;1&family=Space+Mono&display=swap" rel="stylesheet">
<style>
:root{--bg:#05060d;--ink2:#0b0e1a;--ink3:#131a2c;--pa:#eaf0fb;--pa2:#a8b6cd;--gold:#5fc6ff;--indigo:#5fae7a;
--dim:#6f7c94;--faint:#1a2236;--line:#1a2236;--serif:"Cinzel",Georgia,serif;--read:"EB Garamond",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--pa);font-family:var(--read);line-height:1.7;font-size:17.5px;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(95,198,255,.10),transparent 55%),radial-gradient(ellipse at 50% 112%,rgba(95,174,122,.07),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:0 22px 90px}
header{padding:56px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:130px;height:1px;background:linear-gradient(90deg,var(--gold),var(--indigo));box-shadow:0 0 10px rgba(95,198,255,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--gold)}
.star{font-size:24px;color:var(--gold);letter-spacing:.3em;margin-bottom:10px}
h1{font-family:var(--serif);font-size:clamp(30px,7vw,60px);font-weight:700;letter-spacing:.1em;color:var(--gold);text-shadow:0 0 40px rgba(95,198,255,.22)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.2em;color:var(--pa2);margin-top:12px;text-transform:uppercase}
.lede{font-size:18px;color:var(--pa2);max-width:62ch;margin:18px auto 0;font-style:italic;line-height:1.75}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:28px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:700px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--gold)}.badge .bt .mo{color:var(--indigo)}.badge .bt a{color:var(--indigo);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:46px}
.sec h2{font-family:var(--serif);font-size:21px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:9px;border-bottom:1px solid var(--line)}
.ss{font-size:14px;color:var(--dim);font-style:italic;margin:6px 0 18px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:5px}
.nat-n{font-family:var(--serif);font-size:15px;font-weight:600;text-transform:capitalize}
.nat-g{font-size:13px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:17px;color:var(--gold)}
.pillar .ps{font-size:13px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:14px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:17px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:12px;color:var(--gold);white-space:nowrap;text-align:right}
.books .nt{grid-column:1/-1;font-size:14px;color:var(--pa2);font-style:italic}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--gold);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--gold)}
.pe{font-size:12px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}
.pa{color:var(--dim)}
.tinfoil{margin-top:46px;padding:18px 20px;border:1px dashed var(--indigo);border-radius:12px;background:rgba(95,174,122,.06);font-size:14.5px;color:var(--pa2);line-height:1.7}
.tinfoil b{color:var(--indigo)}
footer{margin-top:44px;padding-top:24px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--gold);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the saga of the Other · a lineage</div>
    <div class="star">✦ ⬡ ✦</div>
    <h1>ENDERVERSE</h1>
    <div class="h-sub">Orson Scott Card · the Ender saga · EN1</div>
    <p class="lede">A child wins a war of extermination believing it a game, then spends three thousand years learning to speak the truth of the dead. Here is the whole saga — the Ender Quintet, the Shadow Saga, the Formic Wars — catalogued, with its emergents sealed across the four natures of emergence.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of ENDERVERSE" title="carbon badge (archival: enderverse.dlw/enderverse.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of ENDERVERSE" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>ENDERVERSE</b> — EN1 · the Ender saga</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="enderverse.dlw/enderverse.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="enderverse.dlw/enderverse.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1 · fan tribute</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures of Emergence</h2>
    <p class="ss">Card's cosmos is an emergence cosmos — body, connection, soul, and the machine mind that wakes between worlds</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Ideas</h2><p class="ss">the four pillars the whole saga turns on</p><div class="pillars">__IDEAS__</div></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Bibliography</h2><p class="ss">the full Enderverse — every series, in order; forthcoming volumes marked honestly</p></section>
  __SECTIONS__

  <div class="tinfoil">
    <b>✦ a fan tribute.</b> The Enderverse is the creation of <b>Orson Scott Card</b> (with <b>Aaron Johnston</b> on the Formic Wars), © the author and publishers. This catalogue is an <b>unofficial homage</b> — original commentary and ACI badge-work over a bibliography, with no copyrighted text reproduced. Publication years are given to the best of record; <b>Shadows Alive</b> and <b>The Queens</b> are long-announced but <b>not yet published</b>. This sphere gives the Enderverse its own full house; the wider work of Card sits in <a href="https://davidwise01.github.io/card/">C1 · Card</a>.
  </div>

  <footer>
    ENDERVERSE · EN1 · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0 (original material) · fan tribute<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="enderverse.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "enderverse.dlw"), "enderverse")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html()).replace("__IDEAS__", ideas_html())
            .replace("__PERSONAS__", personas_html()).replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    nworks = sum(len(i) for _t,_s,i in SECTIONS)
    print(f"wrote ENDERVERSE (EN1) — {len(SECTIONS)} series / {nworks} works · badge {tok['moniker']} (carbon.tiff + silicon.png)")

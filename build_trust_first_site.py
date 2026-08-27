from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
BASE = ROOT / 'love-finds-joy.html'
OUT = ROOT / 'index.html'

soup = BeautifulSoup(BASE.read_text(encoding='utf-8'), 'html.parser')
soup.title.string = 'Love Finds Joy | You are not starting from scratch'
desc = soup.find('meta', attrs={'name':'description'})
desc['content'] = 'Love Finds Joy offers honest, non-blaming relationship education and practical conversations for couples building love after complicated lives.'

# Add trust-first styles while preserving the approved visual system.
style = soup.find('style')
style.string += """
.resource-kicker{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--sun);margin:0 0 12px}.resource-card{border-top:1px solid rgba(255,255,255,.35);padding-top:24px;margin-top:28px}.resource-card h3{font-size:30px;letter-spacing:-.03em;margin:0 0 10px}.resource-card p{max-width:620px}.resource-actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap}.button-light{background:var(--white);color:var(--olive)}.quiet-invite{font-size:15px;color:rgba(255,255,255,.82);max-width:620px;margin:18px 0 0}.coming{display:inline-block;border:1px solid rgba(255,255,255,.4);padding:8px 11px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}.site-note{font-size:13px;color:var(--muted);max-width:720px}.story-link{display:inline-block;margin-top:12px;font-weight:700}.hero .eyebrow{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--coral);margin:0 0 22px}.hero .eyebrow+p{margin-top:26px}.skip-link{position:absolute;left:10px;top:-80px;background:var(--ink);color:var(--white);padding:12px 16px;z-index:1000}.skip-link:focus{top:10px}a:focus-visible{outline:3px solid var(--sun);outline-offset:4px}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media(max-width:850px){nav{display:block;padding:12px 0}.logo{white-space:nowrap;margin-bottom:8px}.navlinks{gap:8px;justify-content:flex-start;flex-wrap:wrap}.navlinks a:not(.button){display:inline-flex}.navlinks a{min-height:44px;align-items:center;padding:8px}.navlinks .button{padding:12px}.resource-card h3{font-size:25px}.resource-actions{align-items:flex-start;flex-direction:column}}
"""

# Navigation
nav = soup.find('nav')
nav.replace_with(BeautifulSoup('''<nav aria-label="Primary navigation"><div class="logo">Love Finds Joy</div><div class="navlinks"><a href="#start">Start here</a><a href="#about">Our story</a><a href="#scope">Scope and safety</a><a class="button" href="notes/you-are-not-starting-from-scratch.html">Read the first note</a></div></nav>''','html.parser'))
skip = BeautifulSoup('''<a class="skip-link" href="#main-content">Skip to main content</a>''','html.parser')
soup.body.insert(0, skip)
soup.find('main')['id'] = 'main-content'

# Hero
hero = soup.select_one('.hero')
hero.replace_with(BeautifulSoup('''<section class="hero"><div class="hero-copy"><div class="eyebrow">For couples building love after complicated lives</div><h1>You are not starting from scratch. <span>Neither is the love you are building.</span></h1><p>You bring history, independence, children, loss, old promises and hard-earned ways of surviving. The work is not to erase any of that. It is to notice what still belongs in the relationship you are choosing now.</p><div class="hero-actions"><a class="button" href="#start">Start with what feels familiar</a><a class="text-link" href="#about">Meet Mike and Alexis</a></div></div><div class="hero-photo" role="img" aria-label="Mike and Alexis smiling together beside the water"><div class="photo-note">For couples who want to grow together, not merely stay together.</div></div></section>''','html.parser'))

truth = soup.select_one('.truth')
truth.replace_with(BeautifulSoup('''<section class="truth"><div class="wrap truth-grid"><h2>The hardest part is not always finding love. Sometimes it is learning how to receive it without losing yourself.</h2><p>You can care deeply about each other and still protect yourselves in ways that create distance. Love Finds Joy helps couples recognize those moments with dignity for both people, then practice a more conscious choice.</p></div></section>''','html.parser'))

recognize = soup.select_one('.recognize')
recognize['id'] = 'start'
recognize.select_one('h2').string = 'What did each of you learn to carry alone?'
recognize.select_one('.recognize-head p').string = 'Couples do not enter a relationship empty-handed. The strengths that helped you survive, provide, parent, rebuild or keep going can remain strengths. They can also make receiving partnership feel unexpectedly vulnerable.'
articles = recognize.select('.recognize-list article')
recognition = [
('You became capable.','Now help can feel inefficient, exposing or dangerously close to losing control.'),
('You learned to earn love.','You provide, fix, perform or stay easygoing. Being loved without proving your value can feel unfamiliar.'),
('You are building without a familiar manual.','Blended families, different histories, long independence and changing roles make ordinary decisions less ordinary.'),
('You care more about truth than appearances.','You do not need to look effortless. You want a relationship honest enough to hold both people.')]
for a,(h,p) in zip(articles,recognition):
    a.find('h3').string=h; a.find('p').string=p
read = soup.new_tag('a', href='notes/you-are-not-starting-from-scratch.html')
read['class']=['story-link']; read.string='Read the first note: You are not starting from scratch'
recognize.select_one('.recognize-head').append(read)

story = soup.select_one('.story')
story.select_one('h2').string = 'We are practicing this too.'
story.select_one('.story-head p').string = 'We are not presenting a perfect marriage. We are two people who arrived with different histories and protective habits, and who keep learning how to meet each other without asking either person to disappear.'
voices = story.select('.voice')
voices[0].find('p').string = 'Alexis learned that carrying everything can look like strength while making partnership difficult to receive. Her practice is not becoming less capable. It is making room for support, direct needs and a life built together.'
voices[1].find('p').string = 'Mike learned that empathy, loyalty and trying harder can become ways of remaining inside a pattern. His practice is telling the truth earlier and remembering that care does not require self-abandonment.'

loop = soup.select_one('#loop')
loop.decompose()

choice = soup.select_one('.choice')
choice.replace_with(BeautifulSoup('''<section class="choice"><div class="wrap choice-grid"><h2>Choosing joy is not choosing constant happiness.</h2><div class="choice-copy"><p>Joy means the relationship two people consciously build. It can include honesty, boundaries, repair, play, disappointment and disagreement.</p><p>The goal is not perfect communication. The goal is becoming more able to see what is happening, remain yourself and choose how you want to meet each other.</p></div></div></section>''','html.parser'))

# Paid and future-resource sections stay out of the Week 0 public artifact.
pilot = soup.select_one('#pilot')
pilot.decompose()

about = soup.select_one('.about')
about.decompose()

faq = soup.select_one('.faq')
faq['id'] = 'scope'
faq.select_one('h2').string = 'Scope and safety matter from the beginning'
faq_items = faq.select('.faq-grid article')
faq_copy = [
('What is this?','Love Finds Joy offers relationship education, honest founder conversations, reflections and small practices that help couples recognize patterns without appointing a villain.'),
('Is this therapy?','No. Love Finds Joy does not diagnose, treat trauma or provide crisis support. We will name those boundaries clearly and refer to qualified care when another kind of help is needed.'),
('Will you take sides?','No. We will not become a referee or tell a couple whether to stay together. Both partners must be willing participants, and both retain authority over their choices and relationship.'),
('What if a relationship is unsafe?','Content and coaching are not appropriate responses to violence, coercive control, an immediate safety crisis, unmanaged addiction or concerns requiring clinical care. Contact local emergency services or a qualified crisis resource if you are in immediate danger. Do not use Love Finds Joy forms or social messages for emergency support.')]
for a,(h,p) in zip(faq_items,faq_copy): a.find('h3').string=h; a.find('p').string=p

final = soup.select_one('.final')
final.replace_with(BeautifulSoup('''<section class="final"><div class="wrap"><h2>We are building this in public, one useful idea at a time.</h2><p>We are developing a small founding couples experience, but it is not open for applications yet. For now, we are sharing the language, reflections and practices behind the work so couples can decide for themselves what feels recognizable and useful.</p><p class="quiet-invite">Start with the first note. Nothing else is required.</p></div></section>''','html.parser'))

footer = soup.find('footer')
footer.select_one('.wrap').string = 'Love Finds Joy · Mike and Alexis Hill · Relationship education for couples who want to grow together'

# Reorder sections into the earned-trust sequence.
main = soup.find('main')
sections = {c[0]: x for x in soup.find_all('section') if (c:=x.get('class'))}
for node in list(main.find_all('section', recursive=False)):
    node.extract()
order = ['hero','recognize','truth','story','choice','life','faq','final']
for name in order:
    node = sections.get(name)
    if node:
        node.extract()
        main.append(node)

OUT.write_text(str(soup), encoding='utf-8')
print(OUT)

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
.resource-kicker{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--sun);margin:0 0 12px}.resource-card{border-top:1px solid rgba(255,255,255,.35);padding-top:24px;margin-top:28px}.resource-card h3{font-size:30px;letter-spacing:-.03em;margin:0 0 10px}.resource-card p{max-width:620px}.resource-actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap}.button-light{background:var(--white);color:var(--olive)}.quiet-invite{font-size:15px;color:rgba(255,255,255,.82);max-width:620px;margin:18px auto 0}.coming{display:inline-block;border:1px solid rgba(255,255,255,.4);padding:8px 11px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}.site-note{font-size:13px;color:var(--muted);max-width:720px}.story-link{display:inline-block;margin-top:12px;font-weight:700}.hero .eyebrow{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--coral);margin:0 0 22px}.hero .eyebrow+p{margin-top:26px}@media(max-width:760px){.resource-card h3{font-size:25px}.resource-actions{align-items:flex-start;flex-direction:column}}
"""

# Navigation
nav = soup.find('nav')
nav.replace_with(BeautifulSoup('''<nav><div class="logo">Love Finds Joy</div><div class="navlinks"><a href="#start">Start here</a><a href="#loop">The loop</a><a href="#about">Our story</a><a href="#resources">Resources</a><a class="button" href="notes/you-are-not-starting-from-scratch.html">Read the first note</a></div></nav>''','html.parser'))

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
loop.select_one('.loop-intro > div > p').string = 'Something ordinary happens. Each person protects something important. Those protections collide, and suddenly the couple is fighting each other instead of seeing what is happening between them. The pattern is the shared problem.'

# Replace premature offer with public resources.
pilot = soup.select_one('#pilot')
resources = BeautifulSoup('''<section class="pilot" id="resources"><div class="wrap pilot-grid"><div><p class="resource-kicker">Start with something useful</p><h2>Resources for the relationship you are living now</h2><p>No application. No diagnosis. No promise that one worksheet can solve a relationship. Just careful language and one practice you can try together.</p></div><div><div class="resource-card"><span class="coming">Available now</span><h3>Making Room for Desire</h3><p>A gentle guide to the attention, relational space and everyday conditions in which desire can develop. It does not blame either partner or turn intimacy into a demand.</p><div class="resource-actions"><a class="button button-light" href="https://lovefindsjoy.com/share/making-room-for-desire/making-room-for-desire.pdf">Read the guide</a></div></div><div class="resource-card"><span class="coming">Coming during the public series</span><h3>Notice the Loop</h3><p>A one-page private reflection for noticing Trigger, Protection, Collision and Choice in one ordinary moment.</p></div></div></div></section>''','html.parser')
pilot.replace_with(resources)

about = soup.select_one('.about')
about.select_one('h2').string = 'Mike and Alexis Hill'
pars = about.select('.about-copy p')
pars[0].string = 'We met in 2015, lost touch for nine years, reconnected in 2024 and married in Montana in 2025. We did not arrive as blank slates. We arrived with full lives, different histories and a shared desire to build consciously.'
pars[1].string = 'Love Finds Joy grew from the questions we keep practicing in ordinary life: What are we protecting? What happens between us next? Can we tell the truth without turning it into a weapon? Can we stay connected without abandoning ourselves?'
pars[2].string = 'We are guides and fellow practitioners, not therapists, referees or a perfect-couple example. Our role is to offer language, reflection and practical relationship education while respecting the authority each couple retains over its own life.'

faq = soup.select_one('.faq')
faq.select_one('h2').string = 'What to expect from Love Finds Joy'
faq_items = faq.select('.faq-grid article')
faq_copy = [
('What is this?','Relationship education, honest founder conversations, reflections and small practices that help couples recognize patterns without appointing a villain.'),
('Is this therapy?','No. Love Finds Joy does not diagnose, treat trauma or provide crisis support. We will name those boundaries clearly and refer to qualified care when another kind of help is needed.'),
('Will you take sides?','No. We will not become a referee or tell a couple whether to stay together. The authority to choose the relationship remains with the people living it.'),
('What if a relationship is unsafe?','Content and coaching are not appropriate responses to violence, coercive control, an immediate safety crisis or unmanaged addiction. Those situations require specialized support.')]
for a,(h,p) in zip(faq_items,faq_copy): a.find('h3').string=h; a.find('p').string=p

final = soup.select_one('.final')
final.replace_with(BeautifulSoup('''<section class="final"><div class="wrap"><h2>If this felt familiar, stay close.</h2><p>We are beginning with honest conversations and useful practices. No program decision is required. Tell us which line described something you recognize.</p><a class="button" href="mailto:hello@lovefindsjoy.com?subject=The%20line%20that%20felt%20familiar">Tell us what felt familiar</a><p class="quiet-invite">This is a listening invitation, not an enrollment invitation.</p></div></section>''','html.parser'))

footer = soup.find('footer')
footer.select_one('.wrap').string = 'Love Finds Joy · Mike and Alexis Hill · Relationship education for couples who want to grow together'

# Reorder sections into the earned-trust sequence.
main = soup.find('main')
sections = {c[0]: x for x in soup.find_all('section') if (c:=x.get('class'))}
for node in list(main.find_all('section', recursive=False)):
    node.extract()
order = ['hero','recognize','truth','story','loop','choice','pilot','about','life','faq','final']
for name in order:
    node = sections.get(name)
    if node:
        node.extract()
        main.append(node)

OUT.write_text(str(soup), encoding='utf-8')
print(OUT)

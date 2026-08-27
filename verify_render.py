from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps, ImageDraw

BASE = Path(__file__).parent
OUT = BASE / "screenshots"
OUT.mkdir(exist_ok=True)
FILES = ["love-finds-joy.html", "concept-a-daylight.html", "concept-b-evening.html", "index.html", "notes/you-are-not-starting-from-scratch.html"]
MODES = {"desktop": (1440, 1000), "mobile": (390, 844)}
results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for filename in FILES:
        for mode, (width, height) in MODES.items():
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors, failures = [], []
            page.on("pageerror", lambda exc, bag=errors: bag.append(str(exc)))
            page.on("requestfailed", lambda req, bag=failures: bag.append(f"{req.url}: {req.failure}"))
            page.goto((BASE / filename).as_uri(), wait_until="networkidle")
            values = page.evaluate("""() => ({
                innerWidth: window.innerWidth,
                scrollWidth: document.documentElement.scrollWidth,
                text: document.body.innerText,
                links: [...document.querySelectorAll('a')].map(a => a.getAttribute('href')),
                fonts: [...new Set([...document.querySelectorAll('*')].map(e => getComputedStyle(e).fontFamily))],
                bodyFont: getComputedStyle(document.body).fontFamily,
                images: [...document.querySelectorAll('[role=img]')].length
            })""")
            assert values["scrollWidth"] <= values["innerWidth"], (filename, mode, values)
            assert not errors, (filename, mode, errors)
            assert not failures, (filename, mode, failures)
            if filename == "index.html":
                for required in ["You are not starting from scratch", "START WITH SOMETHING USEFUL", "This is a listening invitation, not an enrollment invitation"]:
                    assert required in values["text"], (filename, mode, required)
                for prohibited in ["Request a founding conversation", "Explore the founding experience", "Founding couples"]:
                    assert prohibited not in values["text"], (filename, mode, prohibited)
                assert values["images"] >= 5
            elif filename.startswith("notes/"):
                for required in ["You are not starting from scratch", "Recognition comes before correction", "A private five-minute reflection"]:
                    assert required in values["text"], (filename, mode, required)
                assert values["images"] >= 1
                assert any((href or "").startswith("mailto:") for href in values["links"])
            else:
                assert "Love is great. But it isn't enough." in values["text"]
                assert "Mike and Alexis" in values["text"]
                assert "Choose Joy" in values["text"]
                assert values["images"] >= 3
                assert any((href or "").startswith("mailto:") for href in values["links"])
            assert "arial" in values["bodyFont"].lower() or "helvetica" in values["bodyFont"].lower()
            shot = OUT / f"{Path(filename).stem}-{mode}.png"
            page.screenshot(path=str(shot), full_page=True)
            results.append((filename, mode, values["innerWidth"], values["scrollWidth"], len(values["links"]), str(shot)))
            page.close()
    browser.close()

cards = []
for f in FILES[:2]:
    img = Image.open(OUT / f"{Path(f).stem}-desktop.png").convert("RGB")
    crop = img.crop((0, 0, img.width, min(1300, img.height)))
    cards.append(ImageOps.fit(crop, (700, 650), method=Image.Resampling.LANCZOS, centering=(0.5, 0.0)))
sheet = Image.new("RGB", (1420, 710), (238, 239, 240))
for i, img in enumerate(cards):
    sheet.paste(img, (10 + i * 710, 10))
ImageDraw.Draw(sheet).text((20, 675), "A  DAYLIGHT", fill=(25,25,25))
ImageDraw.Draw(sheet).text((730, 675), "B  EVENING", fill=(25,25,25))
contact = OUT / "love-finds-joy-directions.jpg"
sheet.save(contact, quality=90)
print(f"VERIFIED {len(results)} renders")
for row in results: print(*row)
print("CONTACT_SHEET", contact)

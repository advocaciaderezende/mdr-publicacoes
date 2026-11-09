import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
out = root / 'imagens'
out.mkdir(exist_ok=True)
regular = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def render(title, body, target, page=None, total=None):
    img = Image.new('RGB', (1080, 1350), '#10243A')
    d = ImageDraw.Draw(img)
    d.rectangle((50, 45, 1030, 1300), outline='#C9A45C', width=4)
    d.text((95, 115), 'M DE R  |  ADVOCACIA', font=ImageFont.truetype(bold, 38), fill='#D9BA7D')
    def wrap(text, font, max_width):
        result = []
        for paragraph in str(text).split('\n'):
            line = ''
            for word in paragraph.split():
                candidate = (line + ' ' + word).strip()
                if line and d.textbbox((0, 0), candidate, font=font)[2] > max_width:
                    result.append(line)
                    line = word
                else:
                    line = candidate
            result.append(line)
        return result
    y = 270
    title_font = ImageFont.truetype(bold, 61)
    body_font = ImageFont.truetype(regular, 42)
    for line in wrap(str(title)[:120], title_font, 855):
        d.text((105, y), line, font=title_font, fill='white')
        y += 82
        if y > 620:
            break
    y += 65
    for line in wrap(str(body)[:550], body_font, 855):
        if y > 1120:
            break
        d.text((105, y), line, font=body_font, fill='#E7EAF0')
        y += 63
    footer = f'{page}/{total}  •  Conteúdo informativo' if page else 'Conteúdo informativo'
    d.text((105, 1220), footer, font=ImageFont.truetype(regular, 28), fill='#D9BA7D')
    img.save(target, quality=92, optimize=True)

for file in sorted((root / 'conteudos').glob('*.json')):
    data = json.loads(file.read_text(encoding='utf-8'))
    slides = data.get('slides')
    if isinstance(slides, list) and len(slides) >= 2:
        if len(slides) > 10:
            raise ValueError(f'{file.name}: máximo de 10 páginas por carrossel')
        for i, slide in enumerate(slides, 1):
            render(slide['titulo'], slide['texto'], out / f'{file.stem}-{i:02d}.jpg', i, len(slides))
    else:
        render(data['titulo'], data['texto'], out / f'{file.stem}.jpg')

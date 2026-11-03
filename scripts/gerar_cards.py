import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[1]
out=root/'imagens'
out.mkdir(exist_ok=True)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
for file in sorted((root/'conteudos').glob('*.json')):
    data=json.loads(file.read_text(encoding='utf-8'))
    title=str(data['titulo'])[:100]
    body=str(data['texto'])[:400]
    img=Image.new('RGB',(1080,1350),'#10243A')
    draw=ImageDraw.Draw(img)
    draw.rectangle((50,45,1030,1300),outline='#C9A45C',width=4)
    draw.text((95,115),'M DE R  |  ADVOCACIA',font=ImageFont.truetype(bold_path,38),fill='#D9BA7D')
    def lines(text,font,maxwidth):
        result=[]
        for paragraph in text.split('\\n'):
            line=''
            for word in paragraph.split():
                test=(line+' '+word).strip()
                if draw.textbbox((0,0),test,font=font)[2]>maxwidth and line:
                    result.append(line);line=word
                else:line=test
            result.append(line)
        return result
    titlefont=ImageFont.truetype(bold_path,66)
    bodyfont=ImageFont.truetype(font_path,43)
    y=295
    for line in lines(title,titlefont,865):
        draw.text((105,y),line,font=titlefont,fill='white');y+=92
    y+=85
    for line in lines(body,bodyfont,865):
        draw.text((105,y),line,font=bodyfont,fill='#E7EAF0');y+=65
        if y>1130:break
    draw.text((105,1220),'Conteúdo informativo',font=ImageFont.truetype(font_path,28),fill='#D9BA7D')
    img.save(out/(file.stem+'.jpg'),quality=92,optimize=True)

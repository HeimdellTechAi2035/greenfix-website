from PIL import Image
from pathlib import Path
import sys

p=Path('hero image.png')
if not p.exists():
    print('hero image not found at',p)
    sys.exit(1)
img=Image.open(p).convert('RGB')
# target sizes (width,height)
sizes=[(1200,630),(800,420),(480,252)]
for w,h in sizes:
    im=img.copy()
    im.thumbnail((w,h),Image.LANCZOS)
    out=Path(f'hero-{w}w.webp')
    im.save(out,format='WEBP',quality=80,method=6)
    print('saved',out)

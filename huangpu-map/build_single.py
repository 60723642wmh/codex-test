"""把 index.html + map.jpg + Leaflet 打包成一个可离线打开的 HTML 文件。

用法：python3 build_single.py   →  生成 黄埔海事处辖区图.html
"""
import base64
from pathlib import Path

here = Path(__file__).parent
page = (here / 'index.html').read_text(encoding='utf-8')
img = base64.b64encode((here / 'map.jpg').read_bytes()).decode()
leaflet = (here / 'vendor' / 'leaflet-1.9.4.js').read_text(encoding='utf-8')

cdn_tag = '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>'
assert cdn_tag in page and "L.imageOverlay('map.jpg'" in page
page = page.replace(cdn_tag, '<script>/* Leaflet 1.9.4 */\n' + leaflet.replace('</script', '<\\/script') + '\n</script>')
page = page.replace("L.imageOverlay('map.jpg'", "L.imageOverlay('data:image/jpeg;base64," + img + "'")
page = page.replace('<div class="app">', '</head>\n<body>\n<div class="app">', 1)
out = '<!doctype html>\n<html lang="zh-CN">\n<head>\n' + page + '\n</body>\n</html>\n'
(here / '黄埔海事处辖区图.html').write_text(out, encoding='utf-8')
print('written', len(out))

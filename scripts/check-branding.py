"""Vérifie que le site sert le dessin original et les exports enregistrés."""
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
MASTER_SHA = 'fc50d71ddfbc380fab698e85c85150988bcba5439e811a25f640ebff52183066'
master_path = ROOT / 'assets/lechappee-logo.png'
assert sha256(master_path.read_bytes()).hexdigest() == MASTER_SHA, 'Master original modifié'
manifest = json.loads((ROOT / 'assets/branding-manifest.json').read_text())
assert manifest['master_sha256'] == MASTER_SHA, 'Master différent de celui approuvé'
assert set(manifest['exports']) == {'assets/rouleur-logo.png', 'assets/favicon.png', 'assets/apple-touch-icon.png'}
for name, entry in manifest['exports'].items():
    with Image.open(ROOT / name) as image:
        assert list(image.size) == entry['size'], name
        assert image.mode == entry['mode'], name
        assert sha256(image.tobytes()).hexdigest() == entry['pixel_sha256'], name
with Image.open(master_path) as master, Image.open(ROOT / 'assets/rouleur-logo.png') as logo:
    box = (0, 0, 1254, 730)
    assert ImageChops.difference(master.convert('RGB').crop(box), logo.convert('RGB').crop(box)).getbbox() is None, 'Le symbole a été redessiné'
print('Logo du site identique au master ; exports vérifiés.')

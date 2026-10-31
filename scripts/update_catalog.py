"""Apply a reviewed, complete product list for one video; keep other videos intact."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from catalog_terms import CHANNELS, entry, normalize, sort_key, photography
from urllib.parse import urlparse

DATA_PATH = Path(__file__).resolve().parent.parent / 'site' / 'products.json'


def allowed(name, category):
    if photography(name):return False
    if re.search(r'차량|차박|캠핑|자전거|러닝화|런닝화|시계\s*(보관|상자)|와인더', name + ' ' + category):
        return False
    if re.search(r'시계|워치|watch', name + ' ' + category, re.I) and not re.search(r'충전|보조배터리|케이블', name):
        return category in {'스마트워치', '태블릿·스마트폰·웨어러블'}
    return True


def validate(data):
    assert set(data) == {'updated_at', 'videos', 'products'}, 'Unexpected catalog fields'
    datetime.fromisoformat(data['updated_at'])
    ids = set()
    for video in data['videos']:
        assert set(video) == {'id', 'channel', 'checked_at'}
        assert re.fullmatch(r'[A-Za-z0-9_-]{11}', video['id']) and video['id'] not in ids
        assert isinstance(video['channel'], str) and video['channel'].strip()
        datetime.fromisoformat(video['checked_at'])
        ids.add(video['id'])
    names = set()
    for product in data['products']:
        assert set(product) == {'category', 'name', 'offers'}
        assert product['name'] and product['category'] and product['name'] not in names
        assert allowed(product['name'], product['category']), product['name']
        assert product['offers'], product['name']
        names.add(product['name'])
        offers = set()
        for offer in product['offers']:
            assert {'video_id', 'time', 'price', 'code'} <= set(offer) <= {'video_id', 'time', 'price', 'option', 'code', 'code_url', 'code_note'}
            assert offer['video_id'] in ids
            assert offer['time'] is None or re.fullmatch(r'\d{1,2}(?::[0-5]\d){1,2}', offer['time'])
            assert isinstance(offer['price'], str)
            assert isinstance(offer.get('option', ''), str)
            assert isinstance(offer['code'], str)
            assert isinstance(offer.get('code_note', ''), str)
            if offer.get('code_url'):
                u = urlparse(offer['code_url'])
                assert offer['code'] and u.scheme == 'https' and u.hostname and not u.username and not u.password
            key = (offer['video_id'], offer['time'], offer.get('option', ''))
            assert key not in offers, (product['name'], key)
            offers.add(key)


def apply_video(data, snapshot):
    assert set(snapshot) == {'video', 'products'}
    video = dict(snapshot['video'])
    assert set(video) == {'id', 'channel', 'checked_at'}
    video['channel'] = CHANNELS.get(video['channel'], video['channel'])
    result = normalize(data)
    previous_codes = {}
    for product in result['products']:
        for offer in product['offers']:
            if offer['video_id'] == video['id'] and offer['code']:
                key = (product['name'], offer.get('option', ''))
                value = {k: offer[k] for k in ('code', 'code_url', 'code_note') if k in offer}
                assert key not in previous_codes or previous_codes[key] == value, 'Conflicting existing codes'
                previous_codes[key] = value
    result['videos'] = [v for v in result['videos'] if v['id'] != video['id']] + [video]
    for product in result['products']:
        product['offers'] = [o for o in product['offers'] if o['video_id'] != video['id']]
    by_name = {p['name']: p for p in result['products']}
    for raw in snapshot['products']:
        assert {'category', 'name', 'time', 'price'} <= set(raw) <= {'category', 'name', 'time', 'price', 'option', 'code', 'code_url', 'code_note'}
        item = entry(raw)
        if not allowed(item['name'], item['category']):
            continue
        name = item['name']
        if 'code' not in raw:
            item.update(previous_codes.get((name, item.get('option', '')), {}))
        if name not in by_name:
            by_name[name] = {'category': item['category'], 'name': name, 'offers': []}
        assert by_name[name]['category'] == item['category'], 'Category mismatch: ' + name
        by_name[name]['offers'].append({'video_id': video['id'], **{k: v for k, v in item.items() if k not in {'category', 'name'}}})
    result['products'] = [p for p in by_name.values() if p['offers']]
    result['products'].sort(key=sort_key)
    result['updated_at'] = max((v['checked_at'] for v in result['videos']), key=datetime.fromisoformat)
    validate(result)
    return result


def write_data(data, path=DATA_PATH):
    validate(data)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path)
    args = parser.parse_args()
    current = json.loads(DATA_PATH.read_text())
    updated = apply_video(current, json.loads(args.snapshot.read_text()))
    write_data(updated)
    print(f"{len(updated['products'])} products; updated {args.snapshot}")

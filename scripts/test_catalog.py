"""Check the published data and the video replacement workflow without network access."""
import json
import tempfile
from pathlib import Path

from catalog_terms import CATEGORIES, name, normalize, price
from update_catalog import DATA_PATH, allowed, apply_video, validate, write_data


def video(identifier, channel):
    return {'id': identifier, 'channel': channel, 'checked_at': '2026-10-31T22:00:00+09:00'}


base = {'updated_at': '2026-10-31T22:00:00+09:00',
        'videos': [video('aaaaaaaaaaa', '유튜버 A'), video('bbbbbbbbbbb', '유튜버 B')],
        'products': [{'category': '컴퓨터', 'name': '공통 제품', 'offers': [
            {'video_id': 'aaaaaaaaaaa', 'time': '01:20', 'price': '20만원'},
            {'video_id': 'bbbbbbbbbbb', 'time': '02:30', 'price': '21만원'}]},
            {'category': '공구·측정', 'name': '지난 제품', 'offers': [
                {'video_id': 'aaaaaaaaaaa', 'time': None, 'price': ''}]}]}
snapshot = {'video': video('aaaaaaaaaaa', '유튜버 A'), 'products': [
    {'category': '컴퓨터', 'name': '공통 제품', 'time': '01:25', 'price': '19만원'},
    {'category': '일반 시계', 'name': '일반 시계', 'time': None, 'price': '10만원'}]}
changed = apply_video(base, snapshot)
assert len(changed['products']) == 1
assert changed['products'][0]['offers'] == [
    {'video_id': 'bbbbbbbbbbb', 'time': '02:30', 'price': '21만 원', 'code': ''},
    {'video_id': 'aaaaaaaaaaa', 'time': '01:25', 'price': '19만 원', 'code': ''}]
assert apply_video(changed, snapshot) == changed
assert base['products'][0]['offers'][0]['price'] == '20만원'
added = apply_video(changed, {'video': video('ccccccccccc', '유튜버 C'), 'products': [
    {'category': '컴퓨터', 'name': '공통 제품', 'time': None, 'price': '18만원'}]})
assert len(added['products']) == 1 and len(added['products'][0]['offers']) == 3

for excluded in ['차량용 충전기', '캠핑 텐트', '자전거 라이트', '러닝화', '일반 시계',
                 '시계 보관함', 'ULANZI MA60 마그네틱 거치대', 'Hollyland LARK M2 무선 마이크']:
    assert not allowed(excluded, '생활·촬영 액세서리'), excluded
assert allowed('샤오미 Redmi Watch 6', '스마트워치')
assert allowed('Vention 애플워치 충전 보조배터리', '충전·전원')
assert allowed('ULANZI DC01 카드 케이스 겸 리더기', 'SD카드·리더기')
assert name('에디파이어 MR4 MKII 스피커') == 'Edifier MR4 MK2 스피커'
assert name('유그린 45W 보조배터리 10000mAh') == 'UGREEN 45W 보조배터리 10,000mAh'
assert price('20만원 초중반대') == '20만 원대 초중반'
assert price('270~290달러') == '$270~$290'

with_code = apply_video(changed, {'video': snapshot['video'], 'products': [
    {**snapshot['products'][0], 'code': 'CREATOR26',
     'code_url': 'https://www.youtube.com/watch?v=aaaaaaaaaaa', 'code_note': '행사 옵션 기준'}]})
preserved = apply_video(with_code, snapshot)
assert preserved['products'][0]['offers'][-1]['code'] == 'CREATOR26'
cleared = apply_video(with_code, {'video': snapshot['video'], 'products': [
    {**snapshot['products'][0], 'code': ''}]})
assert cleared['products'][0]['offers'][-1]['code'] == ''

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'catalog.json'
    write_data(added, path)
    before = path.read_bytes()
    invalid = json.loads(before)
    invalid['products'][0]['offers'][0]['video_id'] = 'not-in-registry'
    try:
        write_data(invalid, path)
    except AssertionError:
        pass
    else:
        raise AssertionError('Invalid source reference accepted')
    assert path.read_bytes() == before
    invalid = json.loads(before)
    invalid['products'][0]['offers'][0].update(code='TEST', code_url='javascript:alert(1)')
    try:
        validate(invalid)
    except AssertionError:
        pass
    else:
        raise AssertionError('Unsafe code URL accepted')

data = json.loads(DATA_PATH.read_text())
validate(data)
assert data['products'] and data['videos']
assert normalize(data) == data, 'Use the shared names, units and category ordering'
assert all(product['category'] in CATEGORIES for product in data['products'])
print(f"Catalog checks passed: {len(data['products'])} products, {len(data['videos'])} videos")

"""Shared display names and units for existing and newly added video entries."""
import re
from copy import deepcopy

CATEGORIES = ['미니 PC·노트북', '태블릿·스마트폰·웨어러블', 'CPU', '메모리(RAM)',
              'SSD·저장장치', '인클로저·스토리지 어댑터', 'SD카드·리더기', '청소기', '오디오', '모니터·프로젝터',
              '보조배터리·충전기·허브', '키보드·마우스·게임패드',
              '케이블·스마트기기 액세서리', '공구·생활가전·기타']
CHANNELS = {
 'playsin플레이신':'플레이신', '알잘남 - 알리 잘 알려주는 남자':'알잘남',
 '발품남':'발품파는남자', 'DIY Dr.K 닥터케이':'닥터케이', '영디비 0DiBi':'영디비',
 '테크몽 Techmong':'테크몽', '테크노사우루스 Technosaurus':'테크노사우루스',
 '승업키보드 SeungupKBD':'승업키보드', '다이렉트 웨이 Direct Way':'다이렉트 웨이',
 '대신남 말방구실험실':'대신남', '복구천재 꼬마신발':'꼬마신발',
 '로띠끼룩(Rotiggiluk)':'로띠끼룩', '사야되나? - IT도 패션이다':'사야되나',
 'IT리더 리더유: 리더런':'리더유', '기똥찬 똥찬 Amazing ddongchan':'기똥찬 똥찬',
 '삼백위키 WE IT KEY':'삼백위키', '힉스 HICS':'힉스',
}
BRANDS = [
 (r'\bU-?GREEN\b|유그린','UGREEN'), (r'\bBASEUS\b|베이스어스','Baseus'),
 (r'\bEDIFIER\b|에디파이어','Edifier'), (r'\bLOFREE\b|로프리','Lofree'),
 (r'\bTOOCKI\b|투키','Toocki'), (r'\bORICO\b|오리코','ORICO'),
 (r'\bULANZI\b|울란지','ULANZI'), (r'\bVention\b|벤션','Vention'),
 (r'\bASOM(?:E)?TECH\b|어썸테크','ASOMETECH'), (r'\bNIPOGI\b','NiPoGi'),
 (r'\bGMKTEC\b','GMKtec'), (r'\bNINKEAR\b','Ninkear'),
 (r'\bNETAC\b|넷액','Netac'), (r'\bFANXIANG\b|팬시앙','Fanxiang'),
 (r'\bKINGSPEC\b|킹스펙','KingSpec'), (r'\bWIMIUS\b|위미우스','WiMiUS'),
 (r'\bZEUSLAP\b|제우스랩','ZEUSLAP'), (r'\bUPERFECT\b|유퍼펙트','UPERFECT'),
 (r'\bAULA\b|독거미','AULA'), (r'\bMOVESPEED\b|무브스피드','MOVESPEED'),
 (r'\bLEXAR\b|렉사','Lexar'), (r'\bMARKLIFE\b|마크라이프','Marklife'),
 (r'\bSHOKZ\b|샥즈','SHOKZ'), (r'\bLINGBAO\b|링바오','LINGBAO'),
 (r'\bHAGIBIS\b|하기비스','HAGIBIS'),
 (r'\bALLDOCUBE\b|올도큐브','ALLDOCUBE'),
 (r'(?:샤오미\s*)?(?:\bMIJIA\b|미지아)','샤오미 MIJIA'),
]


def photography(product_name):
    return bool(re.search(r'렌즈|필터\s*키트|셀카봉|삼각대|무선\s*마이크|핀마이크|\b(?:SmallRig|TELESIN|Hollyland\s+LARK)\b|ULANZI\s+(?:MA02|MA30|MA38|MA39|MA60|MA67|MT-?44M|TT88)\b', product_name, re.I))


def units(value):
    value = re.sub(r'(?<![\d,])(\d{4,6})\s*mAh\b', lambda m:f'{int(m[1]):,}mAh', value, flags=re.I)
    value = re.sub(r'(\d)\s*(GB|TB|MHz|GHz|Gbps|W)\b', lambda m:m[1]+{'gb':'GB','tb':'TB','mhz':'MHz','ghz':'GHz','gbps':'Gbps','w':'W'}[m[2].lower()], value, flags=re.I)
    return re.sub(r'\s+', ' ', value).strip()


def name(value):
    value = units(value)
    for pattern, brand in BRANDS:
        value = re.sub(pattern, brand, value, flags=re.I)
    value = value.replace('미니PC', '미니 PC').replace('로봇청소기', '로봇 청소기').replace('무선청소기', '무선 청소기')
    value = value.replace('MR4 MKII', 'MR4 MK2').replace('iPlay 80 Mini Pro', 'iPlay 80 mini Pro')
    value = value.replace('USB-C oled', 'USB-C OLED').replace('C to C', 'USB-C to USB-C')
    value = value.replace('모델 확인', '모델 미확인').replace('세부 모델 확인', '세부 모델 미확인')
    value = value.replace('ZSUS PM14A 14인치 2K 모니터 (모델 미확인)', 'ZSUS 14인치 2K 모니터 (모델 미확인)')
    value = value.replace('ZEUSLAP P16K 16인치 2.5K 모니터 (모델 미확인)', 'ZEUSLAP 16인치 2.5K 모니터 (모델 미확인)')
    if re.search(r'SSD|NVMe|M\.2', value, re.I):
        value = re.sub(r'외장\s*케이스|외장\s*인클로저', '인클로저', value)
    value = re.sub(r'DDR([45])\s+(\d+)MHz', r'DDR\1-\2', value)
    value = re.sub(r'DDR([45])\s+(\d+GB)\s+(\d+)MHz', r'DDR\1-\3 \2', value)
    value = value.replace('데스크톱 램', '데스크톱 RAM').replace('데스크탑', '데스크톱')
    if value == 'MOVESPEED SU10 1TB 고속 저장장치':value = 'MOVESPEED SU10 외장 SSD 1TB'
    return value


def price(value):
    value = value.strip().replace('관포', '관부가세 포함 ')
    value = re.sub(r'₩\s*([\d,]+)', r'\1원', value)
    value = re.sub(r'(\d+(?:\.\d+)?)\s*만\s*원', r'\1만 원', value)
    modifiers = r'(극초반|극후반|초중반|중후반|초반|중반|후반)'
    value = re.sub(r'만 원\s*대?\s*'+modifiers+r'대?', r'만 원대 \1', value)
    value = re.sub(r'(\d+(?:\.\d+)?)\s*~\s*(\d+(?:\.\d+)?)\s*달러', r'$\1~$\2', value)
    value = re.sub(r'(?<![$\d])(\d+(?:\.\d+)?)~\$(\d+(?:\.\d+)?)', r'$\1~$\2', value)
    value = re.sub(r'(\d+(?:\.\d+)?)\s*달러', r'$\1', value)
    value = re.sub(r'(\$[\d.]+)\s*대?\s*'+modifiers+r'대?', r'\1대 \2', value)
    value = re.sub(r'(원|\$[\d.]+)(미만|이하|이상|안팎|내외)', r'\1 \2', value)
    return re.sub(r'\s+', ' ', value).strip()


def category(product_name, old):
    if old in {'RAM', '메모리(RAM)'}:return '메모리(RAM)'
    if old in {'PC 부품·저장장치', 'SSD·메모리카드·인클로저', 'SSD·저장장치', '인클로저·스토리지 어댑터', 'SD카드·리더기'}:
        if re.search(r'\bCPU\b', product_name):return 'CPU'
        if re.search(r'\bDDR[45]|SO-DIMM|데스크톱 (?:RAM|메모리)', product_name):return '메모리(RAM)'
        if re.search(r'인클로저|도킹|M\.2.*어댑터 카드', product_name):return '인클로저·스토리지 어댑터'
        if re.search(r'리더기|메모리카드|(?:micro)?SD', product_name) and 'SSD' not in product_name:return 'SD카드·리더기'
        return 'SSD·저장장치'
    if old in CATEGORIES:return old
    if old == '컴퓨터':return '미니 PC·노트북'
    if old in {'태블릿·휴대기기','스마트워치'}:return '태블릿·스마트폰·웨어러블'
    if old == '생활가전' and '청소기' in product_name:return '청소기'
    if old == '음향':return '오디오'
    if old == '화면·영상':return '모니터·프로젝터'
    if old in {'연결·네트워크','충전·전원'}:
        if '케이블' in product_name and not re.search(r'충전기|충전 스테이션|충전스테이션|보조배터리', product_name):return '케이블·스마트기기 액세서리'
        return '보조배터리·충전기·허브'
    if old == '입력·게임':return '키보드·마우스·게임패드'
    if old == '생활·촬영 액세서리':return '케이블·스마트기기 액세서리'
    if old in {'공구·측정','생활가전'}:return '공구·생활가전·기타'
    return old


def entry(item):
    result = dict(item)
    result['name'] = name(item['name'])
    result['category'] = category(result['name'], item['category'])
    if 'price' in item:
        result['price'] = price(item['price'])
        result['code'] = item.get('code', '').strip()
    if 'option' in item:result['option'] = units(item['option'])
    return result


def sort_key(product):
    n = product['name']
    rank = CATEGORIES.index(product['category']) if product['category'] in CATEGORIES else 99
    capacity = re.search(r'(\d+(?:\.\d+)?)(GB|TB)', n)
    size = float(capacity[1])*(1024 if capacity[2]=='TB' else 1) if capacity else float('inf')
    if product['category'] == '메모리(RAM)':return rank, ('DDR5' in n), ('SO-DIMM' in n), size, n
    if product['category'] in {'SSD·저장장치', '인클로저·스토리지 어댑터', 'SD카드·리더기'}:return rank, False, False, size, n
    return rank, False, False, 0, n


def normalize(data):
    result = deepcopy(data)
    for video in result['videos']:video['channel'] = CHANNELS.get(video['channel'], video['channel'])
    products = {}
    for product in result['products']:
        if product['category'] == '러닝화' or '러닝화' in product['name'] or photography(product['name']):continue
        p = entry(product)
        for offer in p['offers']:
            offer['price'] = price(offer['price'])
            offer['code'] = offer.get('code', '').strip()
            if 'option' in offer:offer['option'] = units(offer['option'])
        if p['name'] in products:
            current = products[p['name']]
            assert current['category'] == p['category']
            current['offers'].extend(o for o in p['offers'] if o not in current['offers'])
        else:products[p['name']] = p
    result['products'] = sorted(products.values(), key=sort_key)
    return result

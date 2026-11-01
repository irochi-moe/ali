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
RENAMES = {
 'FIREBAT R3 Ryzen 5 7430U 미니 PC':'FIREBAT R3 미니 PC', 'Ninkear M7 i7-1185G7 미니 PC':'Ninkear M7 미니 PC',
 'NiPoGi Intel N3350 미니 PC':'NiPoGi N3350 미니 PC',
 'ASUS TUF BE3600':'ASUS TUF BE3600 Wi-Fi 7 공유기', 'ASUS TUF BE6500':'ASUS TUF BE6500 Wi-Fi 7 공유기',
 '샤오미 Redmi Watch 6':'샤오미 Redmi Watch 6 스마트워치', '샤오미 Redmi Watch 6 Active':'샤오미 Redmi Watch 6 Active 스마트워치',
 '샤오미 Redmi Watch 6 Lite':'샤오미 Redmi Watch 6 Lite 스마트워치', '샤오미 Smart Band 10 Pro':'샤오미 Smart Band 10 Pro 스마트밴드',
 'Baseus 100W GaN 충전기 Mini':'Baseus 100W Mini GaN 충전기',
 'Essager 20,000mAh 65W 보조배터리':'Essager 65W 보조배터리 20,000mAh',
 'UGREEN Nexode Pro 보조배터리 25,000mAh (출력 확인)':'UGREEN Nexode Pro 보조배터리 25,000mAh (출력 미확인)',
 'Toocki USB-C OLED 전력표시 케이블2m 3개':'Toocki USB-C OLED 전력 표시 케이블 2m (3개 세트)',
 'FNIRSI LPM-10C 네티워크 케이블 테스터':'FNIRSI LPM-10C 네트워크 케이블 테스터',
 'SONOFF 이산화탄소 온습도계 SAWF-08P(스마트폰앱연동)':'SONOFF SAWF-08P 이산화탄소 온습도계',
 '체지방 체중계 FG2420UWB-A(스마트폰앱연동)':'FG2420UWB-A 체지방 체중계',
 '샤오미 전동 구강세정기 MEO705':'샤오미 MEO705 전동 구강세정기',
 '샤오미 MIJIA 기화식 가습기 800mL/h CJSJSQ04ZMZ':'샤오미 MIJIA CJSJSQ04ZMZ 기화식 가습기 800mL/h',
 '스위치 2 microSD Express 256GB':'스위치 2용 microSD Express 카드 256GB',
 'SIX NVMe SSD X7400 PCIe4.0 1TB':'SIX X7400 PCIe 4.0 SSD 1TB', 'Lofree Flow Lite 84 키보드':'Lofree Flow Lite 84키 키보드',
 'UGREEN CM630 캡쳐 보드':'UGREEN CM630 캡처 보드', 'MIXI 캐리어 20인치':'MIXI 20인치 캐리어',
 'WiMiUS G1 빔프로젝터':'WiMiUS G1 프로젝터', '플릭스톤 D10S 빔프로젝터':'플릭스톤 D10S 프로젝터',
 '레노버 AP602U Stylus Pro 2nd 펜':'레노버 AP602U Stylus Pro 2세대 펜',
 '태블릿 스탠드 금속홀더 마운트 암':'태블릿 금속 홀더 마운트 암 스탠드',
 'ASOMETECH 165W 충전스테이션':'ASOMETECH 165W 충전 스테이션', 'ASOMETECH 300W 충전스테이션':'ASOMETECH 300W 충전 스테이션',
 'ORICO SSD 인클로저 겸 11-in-1 멀티허브':'ORICO 11-in-1 SSD 인클로저 멀티 허브',
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
    value = re.sub(r'\s*\(브랜드 미확인\)', '', value).replace('세부 모델 미확인', '모델 미확인')
    return RENAMES.get(value, value)


def price(value):
    """Canonical form: '[약 ]$N(코드 적용|쿠폰+코드 적용, 카드 할인 전|카드 할인 후|<카드> 할인 후, 관부가세 별도, 배송비 별도)'."""
    value = value.strip().replace('관포', '관부가세 포함 ')
    value = re.sub(r'₩\s*([\d,]+)', r'\1원', value)
    value = re.sub(r'(\d+(?:\.\d+)?)\s*만\s*원', r'\1만 원', value)
    modifiers = r'(극초반|극후반|초중반|중후반|초반|중반|후반)'
    value = re.sub(r'만 원\s*대?\s*'+modifiers+r'대?', r'만 원대 \1', value)
    value = re.sub(r'(\d+(?:\.\d+)?)\s*~\s*(\d+(?:\.\d+)?)\s*달러', r'$\1~$\2', value)
    value = re.sub(r'(?<![$\d.])(\d+(?:\.\d+)?)~\$(\d+(?:\.\d+)?)', r'$\1~$\2', value)
    value = re.sub(r'(\d+(?:\.\d+)?)\s*달러', r'$\1', value)
    value = re.sub(r'(\$[\d.]+)\s*대?\s*'+modifiers+r'대?', r'\1대 \2', value)
    value = re.sub(r'(원|\$[\d.]+)(미만|이하|이상|안팎|내외)', r'\1 \2', value)
    value = re.sub(r'\$(\d+)\.(\d)(?!\d)', r'$\1.\g<2>0', value)
    value = re.sub(r'\s+', ' ', value).strip()
    m = re.fullmatch(r'([^(]+?)\s*\((.*)\)', value)
    if not m or value.startswith('표시가'):return value
    head, inner = m[1], m[2]
    tags = []
    if re.search(r'코드|쿠폰|적용', inner) or not re.search(r'결제 시|할인 후', inner):
        coupon = re.search(r'쿠폰|자동\s*할인|스토어\s*(?:할인|코드)|판매자', inner)
        count = re.search(r'코드 (\d)개', inner)
        tags.append(f'코드 {count[1]}개 적용' if count else '쿠폰+코드 적용' if coupon else '코드 적용')
    card = re.search(r'((?:[A-Za-z가-힣]+ (?:Visa|VISA|Master|Mastercard|MASTER)[·/]?)+?) (?:결제 시|할인 후)', inner)
    if card:tags.append(card[1].replace('VISA', 'Visa') + ' 할인 후')
    elif re.search(r'카드 (?:결제 )?할인 (?:적용|후)|카드 결제 할인|추가 할인 시|카드 할인 후', inner):tags.append('카드 할인 후')
    elif re.search(r'할인 전', inner):tags.append('카드 할인 전')
    amount = re.search(r'\$([\d.]+)', head)
    if '관부가세 포함' in inner:tags.append('관부가세 포함')
    elif (float(amount[1]) > 150 if amount else re.search(r'관세|부가세', inner)):tags.append('관부가세 별도')
    if '배송비 포함' in inner:tags.append('배송비 포함')
    elif '배송비' in inner:tags.append('배송비 별도')
    elif re.search(r'국내\s*배송', inner):tags.append('국내 배송')
    return f"{head}({', '.join(tags)})"


COLORS = {'black':'블랙', '검정색':'블랙', 'white':'화이트', 'gray':'그레이', 'grey':'그레이', 'silver':'실버',
          'blue':'블루', '파란색':'블루', 'yellow':'옐로', 'pink':'핑크', 'ivory':'아이보리', 'light gray':'라이트 그레이',
          'light grey':'라이트 그레이'}


def option(value):
    """Specs as 'CPU·RAM·저장장치', parts joined by '·', basic colors in Korean."""
    value = units(value)
    value = re.sub(r'\bChina Mainland\b\s*/?\s*|\s*/\s*China Mainland\b', '', value)
    value = re.sub(r'\b(?:Korea Plug|한국형 플러그)', 'KR 플러그', value)
    value = re.sub(r'\bEU Plug\b|(?<=[\s/·])EU$|^EU(?=,)', 'EU 플러그', value)
    value = re.sub(r'(?<![\w.])(\d{1,2})G?B?\s*[/ ]\s*(\d{3,4}|[12]T)(?:GB?|B)?(?![\w.])', lambda m:f"{m[1]}GB·{m[2]}{'B' if m[2].endswith('T') else 'GB'}", value)
    value = re.sub(r'(?<![\w.])(\d{1,2})G(?=\s)', r'\1GB', value)
    value = re.sub(r'\s+/\s+|(?<!\d)/(?!\d)|,\s+', '·', value)
    value = re.sub(r'(\d+(?:GB|TB))\s+(?=[A-Za-z가-힣])(?!RAM|ROM|SSD|MHz|또는)', r'\1·', value)
    for english, korean in sorted(COLORS.items(), key=lambda kv:-len(kv[0])):
        value = re.sub(rf'(?<![\w-])(?<!Space )(?<!cool )({english})(?=$|·| \d)', korean, value, flags=re.I)
    return re.sub(r'·+', '·', value).strip('· ')


def note(value):
    """Code notes: '$N 할인·선착순 N개·스토어 쿠폰 CODE(-$N)·...'"""
    value = re.sub(r'\s+', ' ', value).strip()
    value = re.sub(r'(?:색상별 )?선착순 (\d[\d,]*)\s*(?:장|개|대|명)', lambda m:m[0][:m[0].index('선착순')] + f'선착순 {m[1]}개', value)
    value = re.sub(r'(?<!선착순 )(\d+)\s*대 한정', r'선착순 \1개', value)
    value = re.sub(r'스토어\s*(?:쿠폰|코드)|판매자 코드', '스토어 쿠폰', value)
    value = re.sub(r'\+([A-Z0-9]*[A-Z][A-Z0-9]*)\(\$([\d.]+)\)', r'스토어 쿠폰 \1(-$\2)', value)
    value = re.sub(r'(스토어 쿠폰 [A-Z0-9]*[A-Z][A-Z0-9]*)\s*\(\$([\d.]+)\)', r'\1(-$\2)', value)
    value = re.sub(r'스토어 쿠폰 \$([\d.]+)', r'스토어 쿠폰 -$\1', value)
    value = re.sub(r'(스토어 쿠폰 \S+?)\s*(?:(?:함께|먼저)(?: 적용| 입력| 수령)?|별도|수집 필수|다운로드 후 적용)', r'\1', value)
    value = re.sub(r'(스토어 쿠폰 \S+?) 직접 수령', r'\1(직접 수령)', value)
    value = re.sub(r'카드 할인 (\S+) (?:VISA|Visa) -\$[\d.]+ 시 (\$[\d.]+)', r'\1 Visa 결제 시 \2', value)
    value = re.sub(r'\b(KB|우리) VISA 적용 시', lambda m:('KB국민' if m[1] == 'KB' else '우리') + ' Visa 결제 시', value)
    value = re.sub(r'\s*,\s+|\s+·\s+|,(?!\d{3})', '·', value)
    return value


def category(product_name, old):
    if old in {'RAM', '메모리(RAM)'}:return '메모리(RAM)'
    if old in {'PC 부품·저장장치', 'SSD·메모리카드·인클로저', 'SSD·저장장치', '인클로저·스토리지 어댑터', 'SD카드·리더기'}:
        if '허브' in product_name:return '보조배터리·충전기·허브'
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
    if 'option' in item:result['option'] = option(item['option'])
    if 'code_note' in item:result['code_note'] = note(item['code_note'])
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
            if 'option' in offer:offer['option'] = option(offer['option'])
            if 'code_note' in offer:offer['code_note'] = note(offer['code_note'])
        if p['name'] in products:
            current = products[p['name']]
            assert current['category'] == p['category']
            current['offers'].extend(o for o in p['offers'] if o not in current['offers'])
        else:products[p['name']] = p
    result['products'] = sorted(products.values(), key=sort_key)
    return result

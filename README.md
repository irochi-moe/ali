# 알리 제품 목록

제품 종류·유튜버별 제품, 예상 가격, 할인 코드 목록. 프레임워크나 패키지 설치 없이 정적 파일로 동작한다.

## GitHub Pages 배포

저장소의 Pages 배포 소스는 **GitHub Actions**로 설정되어 있다. 아래 명령으로 첫 배포를 시작한다.

```sh
git push -u origin main
```

`main`에 푸시하면 검증 후 자동 배포한다. Actions의 **GitHub Pages** 워크플로에서 수동 실행도 가능하다. 설정 위치는 **Settings → Pages → Build and deployment → Source**다.

배포 주소: <https://irochi-moe.github.io/ali/>. 워크플로는 `site/` 폴더만 배포한다.
설정 안내: [GitHub 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## 데이터 수정

원본은 `site/products.json` 하나다. 수정 후 빌드할 필요가 없다.

- `videos`: 영상 `id`, 통일된 유튜버 이름 `channel`, 실제 확인 시각 `checked_at`.
- `products`: `category`, 동일 제품에 공통으로 쓰는 `name`, 유튜버별 `offers`.
- `offers`: `video_id`, 타임라인 `time`, 예상 가격 `price`, 할인 코드 `code`. `option`, `code_url`, `code_note`는 필요할 때 추가한다.
- 미공개 가격·코드는 빈 문자열, 미확인 타임라인은 `null`이다. 할인 코드의 출처는 `code_url`, 짧은 사용 조건은 `code_note`에 넣는다. 통화·카드·관부가세 조건은 가격에 유지한다.
- `updated_at`과 `checked_at`은 `2026-10-31T23:29:27+09:00` 같은 시간대가 포함된 ISO 8601 형식이다. 파일 수정 시각 대신 실제 정보 확인 시각을 기록한다.

새 유튜버의 영상 ID를 `videos`에 추가한 뒤, 같은 제품의 `offers`에 연결한다. 규격·용량·세대가 다르면 제품을 구분한다. 제품명·단위·유튜버 별칭·카테고리 규칙은 `scripts/catalog_terms.py`에서 관리한다.

영상 하나의 전체 목록을 갱신할 때는 아래 형식의 JSON 파일을 만들고 `python3 scripts/update_catalog.py /경로/update.json`을 실행한다.

```json
{
  "video": {"id": "영상ID_11자리", "channel": "유튜버 이름", "checked_at": "2026-10-31T23:29:27+09:00"},
  "products": [
    {"category": "CPU", "name": "AMD Ryzen 7 9800X3D CPU", "time": "01:23", "price": "44만 원대", "code": ""}
  ]
}
```

이 명령은 해당 영상의 이전 항목을 전체 교체하고 다른 영상의 정보는 보존한다. 일부 제품만 넣으면 누락 제품은 해당 영상에서 제거된다. `code`를 생략하면 같은 제품·옵션의 기존 코드를 유지하며, `"code": ""`는 삭제를 뜻한다. 데이터 검증에 실패하면 원본 파일을 바꾸지 않는다.

차량·캠핑·자전거 전용품, 러닝화, 일반 시계·시계 보관함, 촬영 액세서리는 제외한다. 스마트워치는 포함한다. PC 부품은 CPU, 메모리, SSD·저장장치, 인클로저, SD카드·리더기를 구분한다. 자동 수집·예약 갱신은 하지 않는다.

## 로컬 확인

```sh
python3 scripts/test_catalog.py
node --check site/app.js
node --test tests/app.test.cjs
python3 -m http.server 8000 --directory site
```

브라우저에서 <http://localhost:8000/>을 연다. 데이터 파일을 가져오므로 HTML을 파일로 직접 여는 대신 HTTP 서버를 사용한다. 검증에는 Python 3와 Node.js 22 이상만 필요하다.

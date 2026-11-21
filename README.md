# centumnova.github.io
Official website of CENTUMNOVA

## 로컬 개발

Python 3.10 이상을 사용합니다. 별도의 패키지 설치는 필요하지 않습니다.
저장소 루트에서 실행합니다.

```sh
python3 build.py
python3 -m unittest discover -s tests
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

기본 한국어 경로는 `/`, 영어 경로는 `/en/`입니다. 약관과 개인정보처리방침도 각각 해당 언어 경로에서 제공됩니다. 소스 변경 후 빌드를 다시 실행하면 `_site/`가 갱신됩니다. 커밋 전에는 `python3 build.py --publish`로 브랜치 배포용 파일도 갱신해 함께 커밋합니다. 공개 파일을 삭제할 때는 해당 원본과 루트의 배포용 사본을 함께 삭제합니다.

## 콘텐츠 수정

- 임시 워드마크는 `build.py`의 `BRAND`와 `assets/mark.svg`에서 관리합니다. 언어별 슬로건과 회사 소개는 `build.py`의 `COPY`에서 수정합니다.
- 앱은 `data/apps.json` 배열에 추가합니다. 각 항목은 언어별 `name`과 `description`(`ko`, `en`), `status`(`planned`, `development`, `released`)를 사용합니다. 선택 항목으로 `icon`(`/assets/` 내 경로), `google_play`(HTTPS 스토어 주소), 언어별 `privacy`(HTTPS 또는 사이트 내 경로)를 지정할 수 있습니다. 스토어 링크는 `released`인 항목에만 표시됩니다. 사이트 자체 앱 정책을 추가하려면 해당 HTML을 `public/`에 넣고 그 주소를 연결합니다.
- 회사 주소에는 승인된 도로명과 건물번호까지만 사용합니다. Google Play 조직 인증에 필요한 전체 주소는 Google Play Console에서 직접 제출합니다.

## GitHub Pages 및 Search Console

1. 기존 `main` 브랜치 루트 배포와 **GitHub Actions** 배포를 모두 지원합니다. 저장소 관리자는 **Settings → Pages → Build and deployment → Source**에서 **GitHub Actions**를 선택해 배포 경로를 하나로 통일할 수 있습니다.
2. `main`에 변경사항을 반영하면 Actions의 **Deploy CENTUMNOVA to GitHub Pages**가 빌드, 검증, 배포를 실행합니다. 최초 설정 후 필요하면 **Run workflow**로 `main`에서 실행합니다.
3. 배포 후 [공식 사이트](https://centumnova.github.io/)와 양쪽 언어 페이지를 확인합니다. GitHub Pages 설정에서 HTTPS 적용 상태도 확인합니다.
4. Search Console에 `https://centumnova.github.io/` URL 접두어 속성을 추가합니다. Google에서 발급받은 HTML 확인 파일을 이름과 내용 그대로 `public/`에 두고 `main`으로 배포한 뒤 Search Console에서 확인을 실행합니다. 인증 파일은 소유권 유지에 필요하므로 배포 후에도 유지합니다. 사이트맵은 `https://centumnova.github.io/sitemap.xml`입니다.

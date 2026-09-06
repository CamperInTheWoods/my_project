# 도감길드 도감작 도우미 (maple-dogam)

메이플랜드 "도감작"(몬스터 드롭 아이템 컬렉션) 진행 상황을 추적하는 싱글 파일 웹앱.
검색 → 몹 선택 → 체크리스트 → 스톱워치/타임라인 → 통계/운계산기 → 완료 시 "도감"(책 UI)에 저장, 순서로 쓴다.

## 구조 — 빌드 없는 순수 정적 사이트

- **`index.html`** 이 사실상 전부다. HTML + `<style>` + `<script>`가 한 파일(약 800KB)에 다 들어있다.
  섹션은 파일 안 주석의 번호 헤더(`// 9. CORS 프록시`, `// 10. maplestory.io API...` 등)로 대충 구분되어 있으니
  `grep`으로 그 헤더들을 먼저 훑으면 전체 그림이 잡힌다.
- **`gyubok-dogam.js`** — "허규복" 통계 페이지용 별도 데이터 파일(`GYUBOK_DATA`), `index.html`에서 `<script src>`로 로드.
- 나머지는 이미지/SVG 에셋(`*-icon.png`, `leather-pattern.png`, `summer-bg.svg`).
- `npm`, 번들러, 빌드 스텝 전혀 없음. **로컬 개발은 그냥 `index.html`을 브라우저로 열거나,
  정적 서버 하나 띄우면 끝** (예: `npx serve .` 또는 `python -m http.server`).
- 상태 저장은 전부 `localStorage` (키: `mob_<id>`, `excl_<id>`, `tl_base_<id>`, `touch_<id>` 등). 백엔드/DB 없음.
- 몬스터 검색은 `maplestory.io` API를 직접 호출하고, 실패 시 `corsproxy.io` 등 CORS 프록시를 순차 폴백한다
  (`proxyFetch`, `searchByName` 근처, 9번 섹션).

## UI 핵심 개념 — "도감(책)" 오버레이

전체 화면이 `#mbook-overlay` (`.mbook-overlay`, z-index **9000**)라는 책 모양 오버레이 하나로 덮여 있고,
그 안에서 페이지(`_mbookPage`: `hunt`/`records`/`stats`/`gyubok`/`records`)를 전환하며 콘텐츠를 바꿔 끼운다.
실제 체크리스트(`.tab-panel`)도 이 오버레이 **안**에 중첩되어 있다.

**중요 — z-index 함정**: 이 책 오버레이가 z-index 9000으로 화면 전체를 덮기 때문에,
이후에 추가하는 모달/팝업은 반드시 **z-index를 9000보다 높게** 잡아야 한다.
안 그러면 "버튼 눌러도 아무 반응 없음"처럼 보이는 버그가 난다 (실제로는 열리지만 책 뒤에 가려짐).
2.007.1에서 결과창(`.result-overlay`)이 정확히 이 문제였음 (z-index 1000 → 9500로 수정).
새 오버레이형 UI를 만들 때는 기존 모달들(`prob-modal`, `stat-modal` = 9000, `result-overlay` = 9500)의
z-index를 먼저 확인하고 그보다 높게 맞출 것.

## 버전 표시 & 패치노트 — 릴리즈할 때 반드시 같이 갱신

- 화면 우하단 버전 라벨: `<div id="ver-label">...` (index.html 상단부 검색, `똘레로_X.YYY.Z` 형식).
- `PATCH_NOTES` 배열 (index.html에서 `const PATCH_NOTES = [` 검색) — 최신 항목을 배열 **맨 앞**에 추가.
  각 항목 형식:
  ```js
  { ver: 'X.YYY.Z', date: 'YY.MM.DD', feat: [...], fix: [...] }
  ```
  `feat`/`fix`는 있는 것만 넣으면 됨. 날짜는 실제 배포일(KST, `YY.MM.DD`).
- 버전 번호는 `X.YYY.Z` — YYY는 3자리 zero-pad, Z는 자잘한 패치. 기능 추가는 YYY를 올리고 Z를 0으로,
  버그 수정만이면 보통 Z만 올린다 (예: 2.007.0 → 버그 수정 → 2.007.1).
- ver-label과 PATCH_NOTES 버전 번호는 항상 일치시킬 것.

## 배포 구조 — 이 폴더는 별도 저장소로 미러링되어 실제 서비스된다

**여기(`my_project`)에 커밋/푸시하는 것만으로는 배포되지 않는다.** 실제 서비스는 별도 GitHub 저장소다.

| | |
|---|---|
| 개발 저장소 | `https://github.com/CamperInTheWoods/my_project.git` (모노레포, 이 폴더는 `sideproject/maple-dogam/`) |
| **배포(서비스) 저장소** | `https://github.com/CamperInTheWoods/maple_dogam.git` — **GitHub Pages**로 `main` 브랜치 루트를 서빙 |

두 저장소는 `git subtree split`으로 연결되어 있다. `my_project`의 git log에 보이는
`Split 'sideproject/maple-dogam/' into commit '...'` 커밋들이 그 흔적이다.

### 배포 절차 (수정 → 실제 사이트 반영까지)

```bash
# 1. 평소처럼 my_project에 커밋 (이 폴더 안에서 작업)
git add index.html
git commit -m "Release: X.YYY.Z - 한 줄 요약"
git push origin main

# 2. sideproject/maple-dogam/ 폴더만 뽑아서 임시 브랜치 생성 (반드시 my_project 루트에서 실행)
cd .. && cd ..   # my_project 루트로 이동
git subtree split --prefix=sideproject/maple-dogam -b deploy-X.Y.Z

# 3. 그 브랜치를 배포 저장소의 main에 push (실제 서비스 반영되는 순간)
git push https://github.com/CamperInTheWoods/maple_dogam.git deploy-X.Y.Z:main

# 4. 로컬 임시 브랜치 정리
git branch -D deploy-X.Y.Z
```

- 1번(my_project push)과 3번(maple_dogam push)은 **둘 다 해야** 개발 이력 보존 + 실제 배포가 끝난다.
  1번만 하고 끝내면 "커밋했는데 사이트에 반영 안 됨" 상태가 된다.
- 배포 확인: `https://api.github.com/repos/CamperInTheWoods/maple_dogam/commits?per_page=1` 로 최신 커밋 해시 확인,
  또는 실제 사이트 우하단 버전 라벨 확인.
- `maple_dogam` 저장소에는 `.git` 이력이 없는 이 폴더(index.html + 에셋)만 그대로 미러링된다 — 구조가 100% 동일해야 한다.

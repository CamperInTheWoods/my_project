# Git 입문 가이드

## Git이 뭔가요?

코드의 **변경 이력을 관리**하는 도구입니다.
쉽게 말하면 → "코드용 타임머신 + 구글 드라이브"

```
내 컴퓨터 (로컬)  ←→  GitHub (인터넷 저장소)
```

---

## 핵심 개념

| 용어 | 뜻 |
|------|-----|
| **Repository (저장소)** | git으로 관리되는 프로젝트 폴더 |
| **Commit** | 변경사항을 저장하는 행위 (저장 버튼) |
| **Push** | 내 컴퓨터 → GitHub 업로드 |
| **Pull** | GitHub → 내 컴퓨터 다운로드 |
| **Branch** | 독립적인 작업 공간 (복사본) |

---

## 처음 시작할 때 (최초 1회)

```bash
git init                                      # 현재 폴더를 git으로 관리 시작
git remote add origin [GitHub 주소]           # GitHub 저장소 연결
```

---

## 매번 쓰는 기본 흐름

```
수정 → add → commit → push
```

```bash
git status                    # 1. 뭐가 바뀌었는지 확인
git add .                     # 2. 모든 변경 파일 선택 (특정 파일만: git add 파일명)
git commit -m "변경 내용 설명" # 3. 저장
git push                      # 4. GitHub에 업로드
```

---

## git status 읽는 법

```
Changes not staged for commit:   ← 수정됐지만 add 안 한 파일 (빨간색)
Changes to be committed:         ← add 완료, commit 대기 중 (초록색)
Untracked files:                 ← git이 아직 모르는 새 파일 (빨간색)
```

---

## 브랜치 (Branch)

메인 코드를 건드리지 않고 새 기능을 만들 때 사용합니다.

```bash
git branch                    # 현재 브랜치 목록 확인
git branch 브랜치이름          # 새 브랜치 만들기
git checkout 브랜치이름        # 그 브랜치로 이동
git merge 브랜치이름           # 작업 완료 후 main에 합치기
```

```
main    ──────────────────────●
              \              /
feature        ●──●──●──●──●
```

---

## GitHub에서 코드 받아오기

```bash
git clone [GitHub 주소]        # 저장소 전체를 내 컴퓨터로 복사
git pull                       # 최신 변경사항만 받아오기
```

---

## 자주 쓰는 명령어 모음

```bash
git log                        # 커밋 히스토리 보기
git diff                       # 수정된 내용 상세 비교
git restore 파일명             # 수정 전으로 되돌리기
git branch -M main             # 브랜치 이름 바꾸기
git push -u origin main        # 처음 push할 때 (이후엔 git push만)
```

---

## 오늘 한 것 복습

```bash
git init
git remote add origin https://github.com/CamperInTheWoods/my_project.git
git add .
git commit -m "first commit"
git branch -M main
git push -u origin main
```

---

## 앞으로 코드 수정할 때마다

```bash
git add .
git commit -m "무엇을 바꿨는지 간단히"
git push
```

이 세 줄만 기억하면 됩니다!

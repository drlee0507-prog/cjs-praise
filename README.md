# 매일 아침 한 곡

일본선교회 최종순 집사님이 매일 아침 단톡방에 나눠주신 찬양 모음 홈페이지입니다.

## 내 PC에서 미리 보기

`index.html` 을 더블클릭하면 바로 열립니다 (songs.js, types.js 가 같은 폴더에 있어야 함).

## 처음 올리기 (GitHub Pages)

1. github.com 에 로그인 후 오른쪽 위 `+` > **New repository**
   - 이름 예: `praise` / **Public** 선택 / Create repository
2. 새 저장소 화면의 **uploading an existing file** 링크를 눌러, 이 폴더 안의 파일과 폴더를 모두 끌어다 놓고 **Commit changes**
   - `.github` 폴더는 숨김 폴더라 끌어다 놓을 때 빠지기 쉽습니다. 빠졌다면 `Add file > Create new file` 에서 이름을 `.github/workflows/titles.yml` 로 쓰고 내용을 붙여 넣으세요.
3. 저장소 **Settings > Pages** 에서 Source: `Deploy from a branch`, Branch: `main` / `(root)` > Save
4. 1~2분 뒤 `https://아이디.github.io/praise/` 로 접속됩니다.
5. 곡 제목 채우기: **Actions** 탭 > `곡 제목 채우기` > **Run workflow**
   (처음 한 번 실행하면 모든 곡의 유튜브 제목과 채널명이 `songs.js` 에 저장되어 검색이 잘 됩니다. 이후에는 `songs.js` 을 올릴 때마다 자동 실행됩니다.)

## 새 곡 추가하기

**방법 A - 카톡 내보내기로 한꺼번에 (한 달에 한 번 권장)**
```
python tools/parse_kakao.py 카톡대화.txt songs.js
```
만들어진 `songs.js` 을 저장소에 다시 업로드하면 됩니다. 기존 제목은 그대로 유지됩니다.

**방법 B - 한 곡씩 직접**
깃허브에서 `songs.js` 을 열어 연필 아이콘으로 편집하고, 마지막 줄 `];` 바로 앞에 한 줄 추가합니다 (앞줄 끝에 쉼표 필요).
```
{"id": "유튜브영상ID", "date": "2026-11-27", "time": "06:00", "note": "", "verse": "시편 23:1-6", "title": "", "channel": ""}
```
영상 ID는 `https://youtu.be/` 뒤의 11자리입니다.

## 창작 찬양 / 함께 만든 영상 표시

`types.js` 에 영상 ID별로 분류와 말씀을 적습니다.
```
window.TYPES = {
  "영상ID1": { "type": "creation", "verse": "시편 23:1-6" },
  "영상ID2": { "type": "video", "verse": "" }
};
```
- `creation`: 집사님 창작 찬양 (Suno), `video`: 집사님 곡에 여행 영상 등을 입혀 만든 유튜브 영상
- `verse`: 이 곡에 맞는 말씀을 직접 적습니다. 비워 두면 말씀을 표시하지 않습니다. (이 두 분류에는 그날의 "읽을 말씀"이 자동으로 붙지 않습니다.)
- 적지 않은 곡은 모두 "나눠주신 찬양"으로 보이고, 그날 집사님이 올리신 읽을 말씀이 자동으로 붙습니다.
- 여기 적은 영상은 다른 분이 단톡방에 올렸어도, 다음에 parse_kakao.py 를 돌릴 때 자동으로 포함됩니다.

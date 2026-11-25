"""songs.js 에서 제목이 비어 있는 곡의 유튜브 제목/채널명을 채웁니다 (API 키 불필요, oEmbed 사용).
깃허브 Actions 에서 자동 실행되며, 직접 실행해도 됩니다:  python tools/fetch_titles.py songs.js
"""
import json, sys, time, urllib.parse, urllib.request


def load(p):
    t = open(p, encoding='utf-8').read()
    return json.loads(t[t.index('['):t.rindex(']') + 1])

path = sys.argv[1] if len(sys.argv) > 1 else 'songs.js'
songs = load(path)
cache, changed = {}, 0
for s in songs:
    if s.get('title'):
        cache.setdefault(s['id'], (s['title'], s.get('channel', '')))
for s in songs:
    if s.get('title'):
        continue
    vid = s['id']
    if vid not in cache:
        url = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(f'https://www.youtube.com/watch?v={vid}')
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                d = json.load(r)
            cache[vid] = (d.get('title', ''), d.get('author_name', ''))
        except Exception as e:  # 삭제/비공개 영상
            cache[vid] = ('(재생할 수 없는 영상)', '')
            print('skip', vid, e)
        time.sleep(0.2)
    s['title'], s['channel'] = cache[vid]
    changed += 1
with open(path, 'w', encoding='utf-8') as f:
    f.write('window.SONGS = [\n' + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in songs) + '\n];\n')
print(f'{changed}곡 제목 채움')

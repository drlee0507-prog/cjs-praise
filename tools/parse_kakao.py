"""카카오톡 대화 내보내기(.txt)에서 최종순 집사님이 올린 유튜브 찬양 링크를 뽑아 songs.js 을 만듭니다.

사용법:  python tools/parse_kakao.py 카톡대화.txt songs.js
- 같은 날 올리신 "읽을 말씀 : ..." 도 함께 저장합니다.
- 이미 songs.js 이 있으면 저장된 곡 제목/채널명은 그대로 유지합니다.
"""
import json, os, re, sys


def load(p):
    t = open(p, encoding='utf-8').read()
    return json.loads(t[t.index('['):t.rindex(']') + 1])

SENDER = '최종순'
src, out = sys.argv[1], sys.argv[2]

date_re = re.compile(r'^-+ (\d{4})년 (\d{1,2})월 (\d{1,2})일 .*-+$')
msg_re = re.compile(r'^\[([^\]]+)\] \[(오전|오후) (\d{1,2}):(\d{2})\] ?(.*)$')
yt_re = re.compile(r'(?:youtu\.be/|youtube\.com/(?:watch\?(?:[^ ]*?&)?v=|shorts/|live/|embed/))([A-Za-z0-9_-]{11})')
url_re = re.compile(r'https?://\S+')

msgs, cur, day = [], None, None
for line in open(src, encoding='utf-8'):
    line = line.rstrip('\n')
    m = date_re.match(line)
    if m:
        day = '%s-%02d-%02d' % (m[1], int(m[2]), int(m[3])); cur = None; continue
    m = msg_re.match(line)
    if m and day:
        h = int(m[3]) % 12 + (12 if m[2] == '오후' else 0)
        cur = {'name': m[1], 'date': day, 'time': '%02d:%s' % (h, m[4]), 'text': m[5]}
        msgs.append(cur)
    elif cur is not None:
        cur['text'] += '\n' + line

verse = {}
for mg in msgs:
    if SENDER in mg['name']:
        v = re.match(r'^읽을 ?말씀 ?[:：] ?(.+)', mg['text'].strip())
        if v:
            verse.setdefault(mg['date'], v[1].split('\n')[0].strip())

old, oldnote = {}, {}
if os.path.exists(out):
    for x in load(out):
        if x.get('title'):
            old[x['id']] = (x['title'], x.get('channel', ''))
        if x.get('note'):
            oldnote[x['id']] = x['note']
# types.js 에 적힌 영상은 다른 분이 올렸어도 포함
tpath = os.path.join(os.path.dirname(os.path.abspath(out)), 'types.js')
extra = set(re.findall(r'"([A-Za-z0-9_-]{11})"\s*:', open(tpath, encoding='utf-8').read())) if os.path.exists(tpath) else set()

songs = []
for mg in msgs:
    ids = list(dict.fromkeys(yt_re.findall(mg['text'])))
    if SENDER not in mg['name']:
        ids = [v for v in ids if v in extra]
    if not ids:
        continue
    note = url_re.sub('', mg['text']).replace('메시지가 삭제되었습니다.', '').strip()
    for vid in ids:
        t, c = old.get(vid, ('', ''))
        n = note or oldnote.get(vid, '')
        songs.append({'id': vid, 'date': mg['date'], 'time': mg['time'], 'note': n,
                      'verse': verse.get(mg['date'], ''), 'title': t, 'channel': c})

with open(out, 'w', encoding='utf-8') as f:
    f.write('window.SONGS = [\n' + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in songs) + '\n];\n')
print(f'{len(songs)}개 게시, 고유 곡 {len({s["id"] for s in songs})}곡 저장 -> {out}')

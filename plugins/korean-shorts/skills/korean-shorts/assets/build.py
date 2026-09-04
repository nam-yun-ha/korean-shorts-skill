# -*- coding: utf-8 -*-
"""장면 하나를 index.html 로 굽는다.   사용:  python build.py s1"""
import io, sys, re, collections
sys.path.insert(0, '_gen')
sys.stdout.reconfigure(encoding='utf-8')
from chargen import clay_char, make_look, look_label

F = lambda n: round(n / 30, 4)

# ★ 캐릭터 외모 — 영상마다 여기만 바꾼다. 전 장면이 같은 사람이 된다.
#   씨앗은 아무 문자열이나 된다. 주제나 날짜를 넣으면 매 영상 다른 사람이 나온다.
#   같은 씨앗은 항상 같은 사람이므로, 한 장면만 다시 렌더해도 얼굴이 바뀌지 않는다.
LOOK = make_look('2026-01-01 주제를 여기에')


SCENES = {
    # 장면마다 아래 형태로 추가한다. 값은 전부 로컬 프레임.
    #   chars = 템플릿의 {{CHAR_*}} 자리 → (prefix, pose)   prefix 는 장면 안에서 유일해야 한다
    #   vals  = 템플릿의 {{xx_s}}/{{xx_d}} 자리 → 시작 프레임 / 지속 프레임
    's1': dict(
        chars={'CHAR_A': ('ca', 'cheer')},
        vals={
            'rb_s': F(4),  'rb_d': F(0),      # 리본  L4–끝
            'q1_s': F(2),  'q1_d': F(0),      # 자막1
        }),
}


def build(name):
    cfg = SCENES[name]
    s = io.open('_gen/%s.html' % name, encoding='utf-8').read()
    for slot, (prefix, pose) in cfg['chars'].items():
        s = s.replace('{{%s}}' % slot, clay_char(prefix, pose, LOOK))

    if name == 's7':                       # 예산 10칸 · 왼쪽 8칸이 5프레임 간격으로 꺼진다
        bl, wp = [], []
        for i in range(10):
            bl.append('        <div class="bl" id="b%d" style="left:%dpx"></div>' % (i, i * 90))
            if i < 8:
                wp.append('      tl.to("#b%d", { backgroundColor: "#3A2A2C", scaleY: .34, '
                          'duration: f(6), ease: "power2.in" }, f(%d));' % (i, 14 + i * 5))
        s = s.replace('{{BLOCKS}}', chr(10).join(bl)).replace('{{WIPE}}', chr(10).join(wp))
    for k, v in cfg['vals'].items():
        s = s.replace('{{%s}}' % k, str(v))
    assert '{{' not in s, '치환 안 됨: ' + s[s.index('{{'):s.index('{{') + 40]

    ids = re.findall(r'\sid="([^"]+)"', s)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    assert not dup, 'id 중복: %s' % dup          # ★ check 가 못 잡는 함정

    io.open('index.html', 'w', encoding='utf-8').write(s)
    print('%s → index.html  (%d bytes · id %d개 · 중복 없음)' % (name, len(s), len(ids)))
    print('   캐릭터: %s   [씨앗 %s]' % (look_label(LOOK), LOOK['seed']))


build(sys.argv[1] if len(sys.argv) > 1 else 's1')

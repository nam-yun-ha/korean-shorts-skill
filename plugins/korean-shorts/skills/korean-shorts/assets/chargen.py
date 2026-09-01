# -*- coding: utf-8 -*-
"""3D 클레이(Claymorphism) 캐릭터 SVG 생성기.

외부 이미지 의존 0. SVG 그라디언트 + 다중 drop-shadow 만으로 입체를 만든다.
viewBox 는 항상 "0 0 260 420".

clay_char(prefix, pose) -> str        # <svg> 안에 들어갈 내용
  prefix : 페이지 전역에서 유일해야 하는 id 접두사 (HyperFrames 규칙)
  pose   : 'grief' | 'cheer' | 'point'

애니메이션용 id
  {prefix}-arms  : cheer  — 두 팔 그룹 (rotation)
  {prefix}-arm   : point  — 가리키는 팔 + 펜 그룹 (rotation)
  {prefix}-d1..3 : grief  — 땀방울 3개
회전은 반드시 CSS `transform-box:fill-box; transform-origin:..%` 로. GSAP svgOrigin 금지.
"""


def _defs(P):
    return f'''    <defs>
      <radialGradient id="{P}-skin" cx="34%" cy="26%" r="80%">
        <stop offset="0%" stop-color="#FFEDCE"/>
        <stop offset="46%" stop-color="#FBD38D"/>
        <stop offset="100%" stop-color="#CE8A46"/>
      </radialGradient>
      <radialGradient id="{P}-hair" cx="30%" cy="20%" r="84%">
        <stop offset="0%" stop-color="#B9825A"/>
        <stop offset="48%" stop-color="#7B4A2D"/>
        <stop offset="100%" stop-color="#3A1D0F"/>
      </radialGradient>
      <linearGradient id="{P}-shirt" x1="14%" y1="2%" x2="88%" y2="100%">
        <stop offset="0%" stop-color="#8ACFF8"/>
        <stop offset="40%" stop-color="#3182CE"/>
        <stop offset="100%" stop-color="#153E74"/>
      </linearGradient>
      <linearGradient id="{P}-sleeve" x1="6%" y1="0%" x2="94%" y2="100%">
        <stop offset="0%" stop-color="#7CC4F5"/>
        <stop offset="50%" stop-color="#3182CE"/>
        <stop offset="100%" stop-color="#194780"/>
      </linearGradient>
      <linearGradient id="{P}-pants" x1="12%" y1="0%" x2="90%" y2="100%">
        <stop offset="0%" stop-color="#688EC4"/>
        <stop offset="48%" stop-color="#2C5282"/>
        <stop offset="100%" stop-color="#101F3B"/>
      </linearGradient>
      <linearGradient id="{P}-shoe" x1="18%" y1="0%" x2="82%" y2="100%">
        <stop offset="0%" stop-color="#3B5C8C"/>
        <stop offset="100%" stop-color="#0A1628"/>
      </linearGradient>
      <linearGradient id="{P}-warm" x1="12%" y1="0%" x2="88%" y2="100%">
        <stop offset="0%" stop-color="#FBD38D"/>
        <stop offset="45%" stop-color="#DD6B20"/>
        <stop offset="100%" stop-color="#89390F"/>
      </linearGradient>
      <radialGradient id="{P}-drop" cx="32%" cy="24%" r="82%">
        <stop offset="0%" stop-color="#F2FBFF"/>
        <stop offset="42%" stop-color="#7CC4F5"/>
        <stop offset="100%" stop-color="#1F5591"/>
      </radialGradient>
      <filter id="{P}-soft" x="-45%" y="-45%" width="190%" height="190%">
        <feDropShadow dx="0" dy="12" stdDeviation="11" flood-color="#04070A" flood-opacity=".55"/>
        <feDropShadow dx="0" dy="3"  stdDeviation="3"  flood-color="#04070A" flood-opacity=".40"/>
      </filter>
      <filter id="{P}-blur" x="-70%" y="-70%" width="240%" height="240%">
        <feGaussianBlur stdDeviation="7"/>
      </filter>
      <filter id="{P}-gnd" x="-70%" y="-260%" width="240%" height="620%">
        <feGaussianBlur stdDeviation="13"/>
      </filter>
    </defs>'''


def _ground(P):
    return (f'    <ellipse cx="130" cy="392" rx="86" ry="19" fill="#000" opacity=".72" '
            f'filter="url(#{P}-gnd)"/>')


def _body(P):
    """다리·신발·목·몸통 — 클레이 캡슐 + 볼륨 하이라이트."""
    return f'''    <g filter="url(#{P}-soft)">
      <rect x="96" y="268" width="30" height="98" rx="15" fill="url(#{P}-pants)"/>
      <rect x="134" y="268" width="30" height="98" rx="15" fill="url(#{P}-pants)"/>
      <rect x="84" y="348" width="50" height="32" rx="16" fill="url(#{P}-shoe)"/>
      <rect x="126" y="348" width="50" height="32" rx="16" fill="url(#{P}-shoe)"/>
      <rect x="114" y="136" width="32" height="34" rx="16" fill="#C07F3F"/>
      <path d="M130 148 C170 148 186 176 186 208 L190 252 C192 280 168 292 130 292 C92 292 68 280 70 252 L74 208 C74 176 90 148 130 148 Z" fill="url(#{P}-shirt)"/>
      <ellipse cx="97" cy="208" rx="14" ry="36" fill="#fff" opacity=".24" filter="url(#{P}-blur)"/>
      <path d="M108 152 L130 190 L152 152 C144 147 116 147 108 152 Z" fill="url(#{P}-warm)"/>
    </g>'''


def _body_run(P):
    """달리는 자세 — 뒷다리 뻗고 앞다리 굽힘, 몸통은 앞으로."""
    return f'''    <g filter="url(#{P}-soft)">
      <path d="M116 274 L62 346" stroke="url(#{P}-pants)" stroke-width="30" stroke-linecap="round" fill="none"/>
      <ellipse cx="54" cy="354" rx="27" ry="15" fill="url(#{P}-shoe)" transform="rotate(-28 54 354)"/>
      <path d="M146 276 L184 320 L162 372" stroke="url(#{P}-pants)" stroke-width="30" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <ellipse cx="156" cy="378" rx="27" ry="15" fill="url(#{P}-shoe)"/>
      <rect x="118" y="140" width="32" height="34" rx="16" fill="#C07F3F" transform="rotate(12 134 157)"/>
      <path d="M140 152 C180 156 194 184 190 216 L188 262 C186 288 162 298 126 294 C90 290 68 276 72 250 L82 204 C88 172 104 148 140 152 Z" fill="url(#{P}-shirt)"/>
      <ellipse cx="102" cy="212" rx="14" ry="34" fill="#fff" opacity=".24" filter="url(#{P}-blur)" transform="rotate(10 102 212)"/>
      <path d="M120 156 L142 194 L164 158 C156 152 128 150 120 156 Z" fill="url(#{P}-warm)"/>
    </g>'''


def _head(P):
    """뒷머리 구 -> 얼굴 구 -> 앞머리 캡(대칭) -> 하이라이트."""
    return f'''    <g filter="url(#{P}-soft)">
      <circle cx="130" cy="98" r="60" fill="url(#{P}-hair)"/>
      <circle cx="130" cy="106" r="52" fill="url(#{P}-skin)"/>
      <path d="M78 106 A52 52 0 0 1 182 106 L182 74 C158 94 102 94 78 74 Z" fill="url(#{P}-hair)"/>
      <ellipse cx="104" cy="86" rx="20" ry="12" fill="#fff" opacity=".36" filter="url(#{P}-blur)"/>
    </g>'''


_FACE = {
    'grief': '''    <path class="fl" d="M104 96 L121 108 L104 120"/>
    <path class="fl" d="M156 96 L139 108 L156 120"/>
    <path class="fl" d="M98 80 L120 91"/>
    <path class="fl" d="M162 80 L140 91"/>
    <path class="fl" d="M108 140 Q119 128 130 140 Q141 152 152 140"/>''',
    'cheer': '''    <ellipse cx="92" cy="126" rx="14" ry="10" fill="#F6AD55" opacity=".62"/>
    <ellipse cx="168" cy="126" rx="14" ry="10" fill="#F6AD55" opacity=".62"/>
    <path class="fl" d="M102 110 Q114 90 126 110"/>
    <path class="fl" d="M134 110 Q146 90 158 110"/>
    <path d="M110 128 Q130 162 150 128 Z" fill="#2D3748"/>
    <path d="M119 147 Q130 157 141 147 Z" fill="#E8697A"/>''',
    'rush': '''    <circle cx="110" cy="102" r="10" fill="#2D3748"/>
    <circle cx="150" cy="102" r="10" fill="#2D3748"/>
    <ellipse cx="130" cy="136" rx="17" ry="14" fill="#2D3748"/>
    <path class="fl" d="M96 84 L122 72"/>
    <path class="fl" d="M142 72 L168 84"/>''',
    'point': '''    <circle cx="112" cy="106" r="9" fill="#2D3748"/>
    <path class="fl" d="M140 108 Q152 93 164 108"/>
    <ellipse cx="132" cy="136" rx="15" ry="11" fill="#2D3748"/>
    <path class="fl" d="M100 84 L124 80"/>
    <path class="fl" d="M146 80 L168 86"/>''',
}


def _arms(P, pose):
    S, K = f'url(#{P}-sleeve)', f'url(#{P}-skin)'
    if pose == 'grief':
        return f'''    <g filter="url(#{P}-soft)">
      <path d="M92 190 Q50 162 62 116" stroke="{S}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <path d="M168 190 Q210 162 198 116" stroke="{S}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <circle cx="60" cy="110" r="19" fill="{K}"/>
      <circle cx="200" cy="110" r="19" fill="{K}"/>
    </g>'''
    if pose == 'cheer':
        return f'''    <g id="{P}-arms" filter="url(#{P}-soft)">
      <path d="M94 188 L40 82" stroke="{S}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <path d="M166 188 L220 82" stroke="{S}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <circle cx="35" cy="74" r="19" fill="{K}"/>
      <circle cx="225" cy="74" r="19" fill="{K}"/>
    </g>'''
    if pose == 'rush':
        return f'''    <path d="M102 202 L58 226 L44 258" stroke="{S}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <circle cx="40" cy="264" r="17" fill="{K}"/>
      <path d="M164 194 L216 208 L230 170" stroke="{S}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <circle cx="234" cy="164" r="17" fill="{K}"/>'''
    return f'''    <path d="M90 192 L74 262" stroke="{S}" stroke-width="30" stroke-linecap="round" fill="none"/>
    <g id="{P}-arm" filter="url(#{P}-soft)">
      <path d="M152 194 L230 110" stroke="{S}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <g transform="rotate(46 238 104)">
        <rect x="229" y="24" width="18" height="86" rx="9" fill="url(#{P}-warm)"/>
        <path d="M229 30 L238 0 L247 30 Z" fill="#FFEDCE"/>
        <rect x="229" y="88" width="18" height="11" fill="#6E2E0C" opacity=".5"/>
      </g>
      <circle cx="238" cy="104" r="19" fill="{K}"/>
    </g>'''


def _drops(P):
    """3D 물방울 땀 3개 — 통통 튀는 모션용 (grief 전용)."""
    d = 'M0 -17 C9 -3 14 4 14 12 A14 14 0 1 1 -14 12 C-14 4 -9 -3 0 -17Z'
    out = []
    for i, (x, y) in enumerate([(214, 60), (46, 54), (220, 138)], 1):
        out.append(
            f'    <g class="drop" id="{P}-d{i}" transform="translate({x},{y})">'
            f'<path d="{d}" fill="url(#{P}-drop)"/>'
            f'<ellipse cx="-4" cy="1" rx="4" ry="6" fill="#fff" opacity=".6"/></g>')
    return chr(10).join(out)


def _head_run(P):
    return f'''    <g filter="url(#{P}-soft)" transform="rotate(10 148 108)">
      <circle cx="148" cy="98" r="60" fill="url(#{P}-hair)"/>
      <circle cx="148" cy="106" r="52" fill="url(#{P}-skin)"/>
      <path d="M96 106 A52 52 0 0 1 200 106 L200 74 C176 94 120 94 96 74 Z" fill="url(#{P}-hair)"/>
      <ellipse cx="122" cy="86" rx="20" ry="12" fill="#fff" opacity=".36" filter="url(#{P}-blur)"/>
    </g>'''


def clay_char(prefix, pose):
    """그리는 순서: 접지그림자 -> 몸통 -> 머리 -> 팔 -> 얼굴 -> (땀방울)"""
    P = prefix
    if pose == 'rush':
        face = _FACE['rush'].replace('cx="110"', 'cx="128"').replace('cx="150"', 'cx="168"')
        face = face.replace('cx="130" cy="136"', 'cx="148" cy="136"')
        face = face.replace('M96 84 L122 72', 'M114 84 L140 72').replace('M142 72 L168 84', 'M160 72 L186 84')
        body = chr(10).join([_body_run(P), _head_run(P), _arms(P, pose), face,
                 _drops(P).replace('translate(214,60)', 'translate(214,48)')
                          .replace('translate(46,54)', 'translate(58,44)')
                          .replace('translate(220,138)', 'translate(228,120)')])
        lean = '    <g transform="rotate(11 130 340)">' + chr(10) + body + chr(10) + '    </g>'
        return chr(10).join([_defs(P), _ground(P), lean])
    parts = [_defs(P), _ground(P), _body(P), _head(P), _arms(P, pose), _FACE[pose]]
    if pose == 'grief':
        parts.append(_drops(P))
    return chr(10).join(parts)

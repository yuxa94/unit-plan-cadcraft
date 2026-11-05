#!/usr/bin/env python3
"""CADCraft MCP smoke test: draws a small walled room headless, saves DWG + PNG, reopens and checks.

    python smoke_test.py [--cli PATH] [--out DIR]

Uses only the standard library. Exit 0 = every check passed. This proves installation and the MCP
round trip only, not drawing quality.
"""
import argparse, base64, json, os, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from setup_mcp import find_cli  # noqa: E402


class Mcp:
    def __init__(self, cli):
        self.p = subprocess.Popen([cli, 'mcp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  text=True, encoding='utf-8')
        self.n = 0
        self.rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {},
                                'clientInfo': {'name': 'unit-plan-cadcraft-smoke', 'version': '1'}})
        self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})

    def send(self, msg):
        self.p.stdin.write(json.dumps(msg, ensure_ascii=False) + '\n')
        self.p.stdin.flush()

    def rpc(self, method, params):
        self.n += 1
        self.send({'jsonrpc': '2.0', 'id': self.n, 'method': method, 'params': params})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError('cadcraft-cli mcp closed the connection')
            r = json.loads(line)
            if r.get('id') == self.n:
                if 'error' in r:
                    raise RuntimeError(f"{method}: {r['error']}")
                return r['result']

    def tool(self, name, args=None):
        res = self.rpc('tools/call', {'name': name, 'arguments': args or {}})
        if res.get('isError'):
            raise RuntimeError(f"{name} failed: {res['content'][0].get('text', '')}")
        for part in res.get('content', []):
            if part['type'] == 'text':
                try:
                    return json.loads(part['text'])
                except ValueError:
                    return part['text']
            if part['type'] == 'image':
                return base64.b64decode(part['data'])

    def ex(self, command, **params):
        return self.tool('execute', {'command': command, 'params': params})

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=10)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--cli', help='cadcraft-cli path (default: auto-detect)')
    ap.add_argument('--out', default='smoke', help='output folder (default: ./smoke)')
    a = ap.parse_args()
    cli = a.cli or find_cli()
    if not cli:
        sys.exit('cadcraft-cli not found. Install CADCraft or pass --cli.')
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    dwg = out / 'smoke-v001.dwg'
    font = 'Malgun Gothic' if os.name == 'nt' else 'AppleSDGothicNeo'

    m = Mcp(cli)
    checks = []
    def check(name, ok, detail=''):
        checks.append({'check': name, 'pass': bool(ok), 'detail': detail})

    m.tool('new_drawing', {'metric': True})
    m.tool('save', {'path': str(dwg)})
    active = m.ex('lisp', code='(strcat (getvar "DWGPREFIX") (getvar "DWGNAME"))')['value'].strip('"')
    check('active drawing is the job file', Path(active).name == dwg.name, active)
    m.ex('setvar', name='INSUNITS', value=4)
    for name, color in (('A-WALL', 7), ('A-WALL-PATT', 8), ('A-ANNO-TEXT', 2), ('A-ANNO-DIMS', 4)):
        m.ex('layer.new', name=name, color=color)
    m.ex('layer.current', name='A-WALL')
    m.ex('pline', vertices=[[-100, -100], [6100, -100], [6100, 4100], [-100, 4100]], closed=True)
    m.ex('pline', vertices=[[100, 100], [5900, 100], [5900, 3900], [100, 3900]], closed=True)
    m.ex('layer.current', name='A-WALL-PATT')
    m.ex('hatch', points=[[0, 2000]], pattern='ANSI31', scale=20)
    m.ex('layer.current', name='A-ANNO-TEXT')
    m.ex('style', name='KOR', font=font, current=True)
    m.ex('text', at=[3000, 2000], text='거실', height=250, justify='MC')
    m.ex('layer.current', name='A-ANNO-DIMS')
    m.ex('dimstyle', name='A-100', DIMSCALE=100, DIMTXT=2.5, DIMASZ=2.5, DIMTSZ=1.5, current=True)
    m.ex('dimlinear', p1=[-100, -100], p2=[6100, -100], at=[3000, -900])

    shapes = m.ex('shapes', layer='A-WALL')['shapes']
    band = sum(s['area'] if i == 0 else -s['area'] for i, s in enumerate(sorted(shapes, key=lambda s: -s['area'])))
    check('wall band area 4,000,000 mm2', abs(band - 4_000_000) < 1, band)
    hatch = m.tool('query_entities', {'type': 'Hatch'})
    loops = hatch['entities'][0]['geometry']['loops'] if hatch.get('entities') else []
    check('hatch has outer loop and island', len(loops) == 2, len(loops))
    m.tool('save', {'path': str(dwg)})
    m.tool('save', {'path': str(out / 'smoke-v001.png')})

    reopened = m.tool('open', {'path': str(dwg)})
    check('reopen without warnings', not reopened.get('warnings'), reopened.get('warnings'))
    counts = m.tool('inspect_drawing', {})['counts']
    check('saved counts', counts == {'Polyline': 2, 'Hatch': 1, 'Text': 1, 'Dimension': 1}, counts)
    texts = [t['text'] for t in m.tool('find_text', {})['texts']]
    check('Korean text survives DWG', '거실' in texts, texts)
    (out / 'smoke-render.png').write_bytes(m.tool('render', {}))
    m.close()

    report = {'cli': cli, 'output': str(dwg), 'checks': checks, 'pass': all(c['pass'] for c in checks)}
    (out / 'smoke-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    for c in checks:
        print(('PASS ' if c['pass'] else 'FAIL ') + c['check'], '' if c['pass'] else c['detail'])
    print('report:', out / 'smoke-report.json')
    sys.exit(0 if report['pass'] else 1)


if __name__ == '__main__':
    main()

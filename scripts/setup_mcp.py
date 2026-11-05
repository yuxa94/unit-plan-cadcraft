#!/usr/bin/env python3
"""Find cadcraft-cli and print MCP settings for Codex and Claude Code.

    python setup_mcp.py                 # print settings only
    python setup_mcp.py --headless      # settings without the app bridge
    python setup_mcp.py --write-codex   # also add [mcp_servers.cadcraft] to ~/.codex/config.toml

--write-codex backs up config.toml first and never replaces an existing cadcraft entry.
"""
import argparse, os, shutil, sys, time
from pathlib import Path

PORT = 7979


def find_cli():
    exe = 'cadcraft-cli.exe' if os.name == 'nt' else 'cadcraft-cli'
    found = shutil.which('cadcraft-cli')
    if found:
        return found
    dirs = []
    if os.name == 'nt':
        try:
            import winreg
            for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                try:
                    with winreg.OpenKey(root, r'Software\CADCraft') as k:
                        dirs.append(winreg.QueryValueEx(k, 'InstallDir')[0])
                except OSError:
                    pass
        except ImportError:
            pass
        for env in ('LOCALAPPDATA', 'ProgramFiles', 'ProgramFiles(x86)'):
            base = os.environ.get(env)
            if base:
                dirs.append(os.path.join(base, 'Programs', 'ArtCraft', 'CADCraft') if env == 'LOCALAPPDATA'
                            else os.path.join(base, 'ArtCraft', 'CADCraft'))
    else:
        dirs += ['/Applications/CADCraft.app/Contents/MacOS', '/usr/local/bin', '/opt/homebrew/bin']
    dirs += [os.path.join(os.getcwd(), 'tools', 'cadcraft')]
    for d in dirs:
        p = Path(d) / exe
        if p.is_file():
            return str(p)
        for q in Path(d).glob(f'*/{exe}') if Path(d).is_dir() else []:
            return str(q)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--cli', help='cadcraft-cli path (default: auto-detect)')
    ap.add_argument('--headless', action='store_true', help='no app bridge (cadcraft-cli mcp only)')
    ap.add_argument('--write-codex', action='store_true', help='append the server to ~/.codex/config.toml')
    a = ap.parse_args()
    cli = a.cli or find_cli()
    if not cli:
        sys.exit('cadcraft-cli not found. Install CADCraft from github.com/storytold/cadcraft/releases '
                 'or pass --cli <path>.')
    args = ['mcp'] if a.headless else ['mcp', '--connect', f'127.0.0.1:{PORT}', '--lazy']
    toml_args = ', '.join('"%s"' % x for x in args)
    toml = f"[mcp_servers.cadcraft]\ncommand = '{cli}'\nargs = [{toml_args}]\n"
    print('cadcraft-cli:', cli)
    print('\n# Codex  (~/.codex/config.toml)\n' + toml)
    print('# Claude Code\nclaude mcp add cadcraft -- "' + cli + '" ' + ' '.join(args))
    if not a.headless:
        app = str(Path(cli).with_name('cadcraft.exe' if os.name == 'nt' else 'cadcraft'))
        print(f'\n# Open the app before the first CAD call\n"{app}" --control {PORT}')

    if a.write_codex:
        cfg = Path.home() / '.codex' / 'config.toml'
        text = cfg.read_text(encoding='utf-8') if cfg.exists() else ''
        if '[mcp_servers.cadcraft]' in text:
            print(f'\n{cfg} already has [mcp_servers.cadcraft]; left unchanged.')
            return
        cfg.parent.mkdir(parents=True, exist_ok=True)
        if cfg.exists():
            backup = cfg.with_name(f'config.toml.bak-{time.strftime("%Y%m%d-%H%M%S")}')
            shutil.copy2(cfg, backup)
            print('\nbackup:', backup)
        cfg.write_text(text.rstrip() + ('\n\n' if text.strip() else '') + toml, encoding='utf-8')
        print('added to', cfg, '- restart Codex.')


if __name__ == '__main__':
    main()

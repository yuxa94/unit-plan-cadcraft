# CADCraft 설치와 MCP 연결

CADCraft는 MCP 서버를 내장하고 있습니다. 별도 MCP 소스, Python 서버, LISP 디스패처, APPLOAD가 필요 없습니다. `cadcraft-cli mcp`가 곧 MCP 서버입니다.

## 1. CADCraft 설치 (Windows)

1. 공식 저장소 https://github.com/storytold/cadcraft/releases 에서 `cadcraft-<ver>-windows-x64.msi`를 받습니다. 저장소 소유자가 `storytold`인지 확인합니다.
2. 같은 릴리스의 `SHA256SUMS.txt`와 대조합니다: `Get-FileHash .\cadcraft-<ver>-windows-x64.msi`
3. 설치합니다. 기본은 현재 사용자 설치(`%LOCALAPPDATA%\Programs\ArtCraft\CADCraft\`)이고, 모든 사용자 설치는 `C:\Program Files\ArtCraft\CADCraft\`입니다. 두 실행 파일이 함께 설치됩니다.
   - `cadcraft.exe` — 화면이 있는 앱
   - `cadcraft-cli.exe` — 헤드리스 CLI와 MCP 서버
4. 관리자 권한이 없으면 `...-windows-x64-portable.zip`을 수업 폴더 안 `tools/cadcraft/`에 풀어 써도 됩니다.
5. 앱이 바로 꺼지면(일부 AMD 드라이버) PowerShell에서 `$env:WGPU_BACKEND="vulkan"` 후 실행합니다.

## 2. 두 가지 연결 방식

| 방식 | 설정 | 쓰는 때 |
|---|---|---|
| 앱에 연결 (권장) | 앱을 `cadcraft.exe --control 7979`로 열고, MCP는 `cadcraft-cli mcp --connect 127.0.0.1:7979 --lazy` | 에이전트가 그리는 과정을 화면에서 보고 직접 고칠 때 |
| 헤드리스 | `cadcraft-cli mcp` | 화면 없이 생성·검증만 할 때, 스모크 테스트 |

- `--connect`는 앱이 열려 있어야 합니다. `--lazy`를 붙이면 Codex가 먼저 켜져도 MCP가 시작되고, 첫 호출 때 앱에 연결합니다.
- `--launch`(앱 자동 실행)는 macOS 전용입니다. Windows에서는 앱을 직접 엽니다.
- 앱의 바로가기 대신 PowerShell로 열 때: `& "$env:LOCALAPPDATA\Programs\ArtCraft\CADCraft\cadcraft.exe" --control 7979`
- 앱은 시작할 때 세션 토큰 파일 `%LOCALAPPDATA%\cadcraft-control-7979.token`을 만들고, MCP 브리지가 자동으로 읽습니다. 토큰을 대화나 파일에 복사하지 않습니다.

## 3. Codex / Claude Code에 등록

`python unit-plan-cadcraft/scripts/setup_mcp.py`가 `cadcraft-cli.exe`를 찾아 설정 예문을 출력합니다. `--write-codex`를 주면 `~/.codex/config.toml`을 백업한 뒤 `[mcp_servers.cadcraft]` 항목이 없을 때만 추가합니다.

Codex (`~/.codex/config.toml`):

```toml
[mcp_servers.cadcraft]
command = 'C:\Users\<사용자>\AppData\Local\Programs\ArtCraft\CADCraft\cadcraft-cli.exe'
args = ["mcp", "--connect", "127.0.0.1:7979", "--lazy"]
```

Claude Code: `claude mcp add cadcraft -- "<cadcraft-cli.exe 전체 경로>" mcp --connect 127.0.0.1:7979 --lazy`

등록 후 Codex(또는 Claude Code)를 다시 시작합니다.

## 4. 연결 확인

1. `python unit-plan-cadcraft/scripts/smoke_test.py` — 헤드리스로 사각형·원·치수·한글 문자를 그리고 DWG로 저장한 뒤 다시 열어 확인합니다. `smoke/` 폴더에 결과 JSON·DWG·PNG가 남습니다.
2. 에이전트에게: "cadcraft MCP 도구 목록과 `inspect_drawing` 결과를 보여줘" — 앱에 연결된 경우 `screenshot`, `ui_inspect`, `ui_click`도 목록에 보입니다.

연결 성공과 스모크 테스트 통과는 설치 확인일 뿐입니다. 도면 품질의 근거가 아닙니다.

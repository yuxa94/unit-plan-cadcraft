# unit-plan-cadcraft

공동주택 단위세대 조닝을 CADCraft 도면으로 작성하는 교육용 참고 스킬입니다. [CADCraft](https://github.com/storytold/cadcraft)에 내장된 MCP 서버(`cadcraft-cli mcp`)를 Codex 또는 Claude Code에 연결해 사용합니다.

[yuxa94/unit-plan-cad](https://github.com/yuxa94/unit-plan-cad)(AutoCAD + file IPC/LISP/COM 전용)의 판단 원칙·작업 기록·조닝 입력 계약을 가져오고, 실행 계층을 CADCraft MCP 도구로 다시 썼습니다.

## 들어 있는 것

```text
SKILL.md                    입구 · 활성화 경계 · 작성/검증 원칙
AGENTS.md                   수업 중 에이전트 행동 규칙
agents/openai.yaml          명시 호출 전용 설정
references/
  connection.md             설치 · MCP 등록 · 연결 확인
  cadcraft-tools.md         검증한 MCP 호출과 주의점
  workflow.md               작업 기록 · 작성 순서 · 검증 · 수정
  input-contract.md         HTML 조닝 1.1 입력
  detail-rules.md · job-records.md · project-profile.md · benchmark.md
assets/
  examples/zoning-editor/   조닝 편집기 (HTML) · 온라인: https://share.planby.us/haemaru-week2/editor/
  examples/zoning-fixtures/ 가상 조닝 8종 (DXF · JSON · SVG)
  templates/job-records.json
scripts/
  setup_mcp.py              cadcraft-cli 찾기 · Codex/Claude 설정 출력
  smoke_test.py             헤드리스 작도 → DWG 저장 → 재열기 검사
```

## 빠른 시작 (Windows)

1. https://github.com/storytold/cadcraft/releases 에서 `cadcraft-<ver>-windows-x64.msi` 설치 (SHA256SUMS 대조)
2. `python unit-plan-cadcraft/scripts/setup_mcp.py` → 출력된 설정을 Codex에 등록 (`--write-codex`로 자동 추가 가능)
3. `python unit-plan-cadcraft/scripts/smoke_test.py` → 6개 검사 PASS 확인
4. CADCraft를 `--control 7979`로 열고 Codex를 다시 시작

## 확인한 범위

2026-11-05, CADCraft 0.17.1 (`cadcraft-cli` macOS universal, 헤드리스)에서 `smoke_test.py` 6개 검사를 통과했습니다: 활성 도면 경로, 벽 띠 면적, 해치 섬, DWG 재열기 경고 없음, 저장 객체 수, 한글 문자 보존. 2026-11-06에는 macOS 앱(공증된 DMG)을 `--control 7979`로 열고 `cadcraft-cli mcp --connect`로 붙여, 한국어 UI 창에 사각형·원이 그려지고 `screenshot`이 동작하는 것을 확인했습니다. Windows 설치·Malgun Gothic 글꼴과 실제 단위세대 작성은 이 기록에 포함되지 않았습니다. 수업 전 강사 PC에서 확인합니다.

CADCraft는 초기 개발 단계의 오픈소스(MIT/Apache-2.0)입니다. 결과는 설계 검토용이며 AutoCAD 출력과 같다고 주장하지 않습니다.

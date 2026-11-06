# CADCraft MCP 도구 안내

v0.17.1에서 실제로 호출해 확인한 형식입니다. 버전이 바뀌면 `list_commands {filter}`로 매개변수 문서를 다시 읽습니다. 명령 카탈로그 전체는 MCP 리소스 `cadcraft://commands`에도 있습니다.

## 도구

| 도구 | 용도 |
|---|---|
| `execute {command, params}` | 대화상자 없이 JSON으로 명령 실행. 만든 객체의 `handle`을 돌려줍니다. **작성은 이것을 기본으로 씁니다.** |
| `command_line {text}` | 사람처럼 명령줄에 입력 (`rectang 0,0 6000,4000`). 공백이 Enter입니다. 수업의 첫 작도 체험용. |
| `script {text}` | `.scr`처럼 여러 줄 입력 |
| `list_commands {filter?}` | 명령 id·별칭·매개변수 문서 |
| `inspect_drawing {entities?, limit?}` | 개수·범위·레이어·스타일·블록·undo 이력 |
| `query_entities {type?, layer?, window?, crossing?, limit?, offset?}` | handle과 형상 |
| `find_text {contains?, layer?, window?}` | TEXT·MTEXT·속성 문자 (한글 그대로) |
| `render {window?, width?}` | PNG. `window [[x0,y0],[x1,y1]]`로 상세 확대 |
| `new_drawing {metric}` · `open {path}` · `save {path}` · `cancel` | 파일. `save`에 `.png/.svg/.pdf`를 주면 내보내기 |
| `screenshot` · `ui_inspect` · `ui_click` | 앱에 연결했을 때만 |

## 작성 순서 예 (검증한 호출)

```json
{"tool":"new_drawing","args":{"metric":true}}
{"tool":"save","args":{"path":"<job>/outputs/plan-v001.dwg"}}
{"tool":"execute","args":{"command":"setvar","params":{"name":"INSUNITS","value":4}}}
{"tool":"execute","args":{"command":"layer.new","params":{"name":"A-WALL","color":7}}}
{"tool":"execute","args":{"command":"layer.current","params":{"name":"A-WALL"}}}
{"tool":"execute","args":{"command":"pline","params":{"vertices":[[-100,-100],[6100,-100],[6100,4100],[-100,4100]],"closed":true}}}
{"tool":"execute","args":{"command":"hatch","params":{"points":[[0,2000]],"pattern":"ANSI31","scale":20}}}
{"tool":"execute","args":{"command":"style","params":{"name":"KOR","font":"Malgun Gothic","current":true}}}
{"tool":"execute","args":{"command":"text","params":{"at":[3000,2000],"text":"거실","height":250,"justify":"MC"}}}
{"tool":"execute","args":{"command":"dimstyle","params":{"name":"A-100","DIMSCALE":100,"DIMTXT":2.5,"DIMASZ":2.5,"DIMTSZ":1.5,"current":true}}}
{"tool":"execute","args":{"command":"dimlinear","params":{"p1":[-100,-100],"p2":[6100,-100],"at":[3000,-900]}}}
{"tool":"execute","args":{"command":"arc","params":{"center":[2000,100],"radius":900,"start":0,"end":90}}}
```

## 자주 쓰는 명령 (`execute`)

| id | 매개변수 요약 |
|---|---|
| `layer.new` / `layer.current` / `layer.set` | `{name, color?, linetype?, lineweight?, current?}` / `{name}` / `{name, on?, frozen?, locked?, plot?, …}` |
| `line` · `pline` · `rectang` · `arc` · `circle` | `{points}` · `{vertices: [[x,y] \| {p, bulge}], closed?}` · `{p1, p2}` · `{center, radius, start, end}` 또는 `{p1,p2,p3}` |
| `offset` · `trim` · `mirror` · `copy` · `erase` | `{handle, distance, side}` · `{handle, pick \| fence \| crossing, edges?}` · `{handles, p1, p2}` · `{handles, delta}` · `{handles}` |
| `hatch` | `{points?: 내부점, handles?: 닫힌 객체, pattern, scale, angle, style: normal\|outer\|ignore}` |
| `text` · `mtext` · `style` | `{at, text, height, justify}` · `{at, text, height, width}` · `{name, font, current}` |
| `dimstyle` · `dimlinear` · `dimaligned` · `dimcontinue` | `{name, DIMSCALE, …, current}` · `{p1, p2, at}` 또는 `{object, at}`(연관) |
| `block` · `insert` | `{name, base, handles}` · `{name, file?: DWG/DXF, at, scale?, rotation?, attribs?}` |
| `properties` · `properties.set` | 선택/handle의 속성 읽기·쓰기, 치수 `textOverride` 확인 |
| `shapes` · `loops` · `texts` · `usage` | 닫힌 형상 면적·자기교차 · 선분 체인의 닫힘/틈 · 문자 · 레이어/블록 사용처 (모두 읽기 전용) |
| `undo` · `lisp` · `setvar` | `{count}` · `{code}` → `{value, output}` · `{name, value}` |

## 이번 시험에서 확인한 주의점

- **치수 축척**: 기본 `ISO-25`는 문자 2.5입니다. mm 도면(1:100)에서는 치수 문자가 거의 보이지 않으므로 `DIMSCALE 100` 스타일을 먼저 만듭니다.
- **현재 레이어**: `execute`로 만든 객체는 현재 레이어에 들어갑니다. 객체 종류를 바꿀 때마다 `layer.current`를 먼저 호출하거나 `properties.set {handles, layer}`로 옮깁니다.
- **한글**: TrueType 글꼴을 가진 문자 스타일을 씁니다 (Windows `Malgun Gothic`, macOS `AppleSDGothicNeo`). SHX 스타일의 한글은 대체 글꼴로 그려집니다. DWG 저장 후 다시 열어도 `find_text`에서 한글이 그대로 읽히는 것을 확인했습니다.
- **해치**: 내부점 `points`는 닫힌 경계 두 개 사이(벽 띠) 같은 섬 영역을 자동으로 찾습니다. 결과의 `loops`로 경계를 확인합니다.
- **저장**: `.dwg` 저장은 AutoCAD 2018 형식(AC1032)으로 기록됐습니다. 다시 `open`하면 `warnings`에 읽지 못한 항목이 나옵니다. 빈 배열인지 기록합니다.
- **활성 파일 확인**: `execute lisp {"code":"(strcat (getvar \"DWGPREFIX\") (getvar \"DWGNAME\"))"}`
- **앱 연결 screenshot**: 앱 연결 모드의 `screenshot`은 이미지를 바로 돌려주지 않고 임시 폴더의 PNG `path`와 크기를 돌려줍니다. 그 파일을 열어 확인합니다. 도면만 볼 때는 `render`가 더 간단합니다.
- **저장 전 활성 도면**: 앱에서 새로 만든 도면은 저장 전까지 `DWGNAME`이 `Drawing1`이고 경로가 비어 있습니다. 작업 경로로 `save`한 뒤 쓰기를 시작합니다.
- **명령줄 실패**: `command_line`은 잘못된 입력에도 오류 대신 다음 프롬프트를 돌려줄 수 있습니다. 결과의 `prompt`가 `Command:`로 돌아왔는지, `running`이 비었는지 봅니다. 남아 있으면 `cancel`.

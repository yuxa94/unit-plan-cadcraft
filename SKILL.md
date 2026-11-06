---
name: unit-plan-cadcraft
description: Educational reference skill for apartment unit-plan drafting in CADCraft through its built-in MCP server (cadcraft-cli mcp). Use only when the user explicitly invokes $unit-plan-cadcraft or asks to apply this completed packaged skill. Generic CAD drafting or skill-creation requests do not activate it.
---

# Unit plan CAD for CADCraft — teaching edition

## Educational activation boundary

This is a completed teaching reference, not the default workflow for exercises. Follow [the repository teaching instructions](AGENTS.md). Apply this skill only when the user directly invokes `$unit-plan-cadcraft` (Claude Code: `/unit-plan-cadcraft`) or explicitly asks to use this completed packaged skill. A request to connect CAD, draw a plan, create a new skill, or read this file for comparison is not an instruction to apply the completed workflow. Quoted examples are not invocations. Do not auto-install this skill or enable implicit invocation.

Create designer-review drawings in CADCraft from room zoning and a **user-supplied local project profile**. This package supplies instructions, a connection helper, a smoke test and synthetic examples. It contains no project DWGs, extracted parts or finished project drawings. It is an agent-assisted workflow, not a universal drafting engine. CADCraft is early-development open-source software: treat every result as a review candidate.

## Start

- New PC: read [connection](references/connection.md). Install CADCraft from the official `storytold/cadcraft` releases, register the MCP server with `scripts/setup_mcp.py`, then run `scripts/smoke_test.py` once.
- Tools: read [CADCraft tool guide](references/cadcraft-tools.md) before the first write. Prefer `execute` with JSON parameters over typed command lines; it returns handles.
- References: read [local project profile](references/project-profile.md). Ask for the user's authorized reference DWG/DXF and keep it outside this package. No project style is configured by default.
- Drafting: read [workflow](references/workflow.md), [detail rules](references/detail-rules.md) and [job records](references/job-records.md).
- HTML zoning: open the [editor](assets/examples/zoning-editor/index.html) (hosted copy: https://share.planby.us/haemaru-week2/editor/); read the [input contract](references/input-contract.md) for schema 1.1 effective regions and holes. Eight synthetic [fixtures](assets/examples/zoning-fixtures/README.md) exercise boundary conditions.

## Decide before affected drafting

Record units, boundary meaning, fixed structure/shafts, entrance, wall assemblies, opening and room-level schedules. Distinguish observation, proposal, user approval and unresolved information. Previous trial wall thicknesses are not defaults. Prepare line-plan options where layout changes are necessary and record the selection; keep already approved conditions.

## Generate and verify

Never draw into a reference drawing. Start each job with `new_drawing {metric: true}`, set `INSUNITS` 4 (mm), and immediately `save` it to the versioned job path (`outputs/plan-v001.dwg`). Before every write batch, confirm the active drawing with `execute lisp (getvar "DWGPREFIX")`/`(getvar "DWGNAME")`; if it is not the job file, stop. Create layers, a Korean-capable text style and a scaled dimension style first (see the tool guide), then draw in dependency order. Record each returned handle with its semantic ID in `object-map.json` and append each call to `operations/log.jsonl`.

Inspect reference parts with `query_entities`, `inspect_drawing` and `find_text`; measure frames, leaves and openings separately from block bounding boxes. Reuse matching physical parts at scale 1 through `insert {file, at, rotation}`; otherwise author a clearly identified review candidate. Recompute room labels, levels, opening tags and dimensions from this job. Check wall joins, finish/insulation terminations, hatch loops/islands (`shapes`, `loops`), opening swings and annotation collisions (`render {window}` crops).

Calls are serial. A tool result with `isError: true` changed nothing reliable: query the drawing before retrying. `execute undo` exists, but a manual edit made in the app is the user's: do not undo across it. Save versioned files (`plan-v002.dwg`), never overwrite the input. After saving, `open` the saved file and compare counts, Korean text, layers, dimensions and hatches; report any `warnings`. Report geometry, reference-detail, saved-file and plot verification separately. A connection check, smoke test or `isError: false` is not proof of drawing fidelity.

## Known CADCraft limits (v0.17)

SHX fonts are not read; dynamic blocks and in-place xref editing are missing; ellipses/splines are segment-approximated; DWG goes through the acadrust converter and entities CADCraft does not model are dropped on save. Plot styles (CTB/STB) and paper-space fidelity are not equivalent to AutoCAD. State these limits instead of claiming AutoCAD-equivalent output.

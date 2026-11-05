# Drafting and revision workflow (CADCraft)

## Job contract

Create a separate job directory outside this installed skill. Retain `input/`, `decisions.json`, `proposal.html`, `model.json`, `operations/log.jsonl`, `object-map.json`, `outputs/`, and `review.json` as each is needed. Each log line records the tool, arguments, returned handles and `isError`. Paths in the job record are relative to the job root. Record the project/profile version and input hash. Do not claim these records are produced by a universal engine: the agent prepares them using CAD tools and task-specific scripts.

`decisions.json` records units, boundary semantics, fixed geometry, wall assemblies, source status of each condition, selected proposal ID and approval message. Status values are `user_confirmed`, `project_confirmed`, `observed`, `proposed`, `unresolved`. A source drawing observation does not silently become a project standard.

For HTML JSON input, read [the schema contract](input-contract.md) and use effective outer-minus-holes geometry.

## Read and normalize

1. Open the input with MCP `open` (DXF preferred for zoning; record any `warnings`). Read polylines with `query_entities`, text with `find_text`, INSUNITS with `execute setvar`/`lisp (getvar "INSUNITS")` and known dimensions. If INSUNITS is unset, use confirmed dimensions/sidecar data and record the decision.
2. Match one room name to each closed room polygon. Detect missing/multiple labels, open/self-intersecting boundaries, overlaps and ambiguous exterior edges. Preserve text formatting while extracting the visible room name.
3. Separate unit envelope, spaces, fixed structural geometry/shafts, requested openings and adjustable furniture. Normalize to millimetres; keep original coordinates and transforms.
4. Represent shared walls once. A centerline is offset by each side's assembly; a finish-face boundary includes different offsets. Approximate zoning requires a proposed wall position before wall generation.

Bundled [fixtures](../assets/examples/zoning-fixtures/README.md) exercise eight conditions. They are invented six-room input examples, not project reference geometry; their wall assumptions apply only to that example.

## Coordinate project specifications

Read [job records](job-records.md) and populate the assembly, room-level, opening and sheet schedules before treating affected details as final. Propose missing consequential values together with source evidence; retain existing approvals. Distinguish wall core from total finished thickness, FL/SL datum and opening dimensions from product labels. Fixed test values are job-specific.

Use the user-supplied [project profile](project-profile.md), [detail rules](detail-rules.md) and [benchmark gate](benchmark.md). Reference reconstruction uses source geometry; new zoning uses the selected proposal. The revision's benchmark status starts pending, not inherited from installation smoke tests.

## Compare options

Generate offline HTML with two SVG line plans at the same scale: A preserves input constraints, B proposes useful improvements. Show room names, important widths, entrance/openings, fixed elements, changed boundaries and a concise change list. Declare any thickness/opening assumption. Do not manufacture an improvement if the supplied arrangement is already appropriate: B may propose furniture or door-swing improvements, or state no justified geometry change.

Record the option selected by the user and any accepted exceptions. Proposed geometry changes are not authorized merely because their diagram exists. The user may directly prescribe a layout in place of an option comparison.

## Resolve source geometry and draft

Use a dependency graph: spaces → shared walls/assemblies → wall joins → openings → frames/leaves/furniture → finish/insulation/hatch boundaries → centerlines → dimensions/annotations → sheet placement.

Wall assembly fields: `id`, `basis`, `core_mm`, `side_a_layers`, `side_b_layers`, `applies_to`, `corner_rule`, `opening_return_rule`, `source_status`. Each layer has material, thickness and display profile. Never supply nominal thickness from a hatch spacing or symbol scale alone. If a necessary assembly field is missing, group questions for affected walls while continuing independent work.

Account for T/L/cross joins; trim finish and insulation at openings. Create closed hatch loops with internal islands so doors/shafts are not incorrectly filled. Use material-specific patterns, angles and effective scale. Check corners and both ends of every interrupted insulation run.

Part placement uses a named measured anchor. With local anchor A, target T, reflection F and rotation R: insertion = T − RFA; point_world = RF point_local + insertion. Physical parts stay scale1. Confirm wall opening vs frame vs leaf vs nominal product dimension separately. Transform the hinge and swing direction together; retain part provenance and mark newly authored geometry.

Generate real CAD dimensions from geometry. Store the wall/opening IDs and anchor meaning for each dimension, not just screen coordinates. Follow whole/segment/opening/finish dimension chains found in the source. Validate actual measurement, displayed value and any text override. Use original styles only after checking entity overrides.

New components are review candidates. Record required dimensions, source convention and fit checks; review before promoting them to the reusable approved library. Generate boxed room/level groups and opening size/type bubbles from schedule IDs. Check fixed text in reused annotation blocks for stale source values.

## Verification and handoff

`review.json` has `coverage` entries for wall, door_window, furniture_equipment, centerline, finish, insulation, hatch, dimension, annotation and sheet. Each entry contains `required`, `status` (pass/fail/unresolved/not_applicable), `handles`, `checks`, `source_evidence`, `unresolved`. Also record unit/polygon checks, opening clearance/swing conflicts, hatch area/loop checks, layer/style checks, reference path status and font substitutions.

Read objects back after every stage (`inspect_drawing`, `query_entities`, `shapes`, `loops`). Save the new output only, under a new version name. Reopen the saved output with `open` and compare counts, representative geometry, Korean text, blocks, dimensions, hatches and dependencies. Inspect full sheet plus `render {window}` detail crops for wall joins, opening returns, hatch density and overlapping annotation. A category needs actual reference-based detail checks, not just an object-presence check. Use the job-record template for finish layers, insulation junctions, hatch regions, dimension hierarchy, room/level groups, opening tags and sheet composition. Keep architectural notes on the sheet and assumptions/diagnostics in a separate HTML review. A screenshot cannot prove hidden geometry or plot-style equivalence. If CTB/STB/SHX are missing, report exact limitations and do not claim matching plotted output.

## Revision contract

Track each generated entity with semantic ID and the handle returned by `execute` in `object-map.json`. CADCraft keeps handles across DWG save and reopen in the tested version; verify this per job before relying on it. Store the prior generated geometry/properties and asset hash. Before an update, compare prior generated state, current CAD state and intended new state. Preserve current entities that changed manually, newly added user objects, and intentional deletions. User edits conflicting with dependent updates are presented with location and options; unaffected work continues.

Duplicate/lost IDs or unknown ownership require resolving that affected region, not regenerating the whole drawing. Propagate accepted wall changes to connected openings, finish, insulation, hatches and dimensions. Keep previous output versions and receipts. This release supplies this agent procedure; it does not include a proven automatic three-way geometry merge engine.

## CADCraft execution safety

- Work in one job drawing. Before a write batch, read `(strcat (getvar "DWGPREFIX") (getvar "DWGNAME"))` through `execute lisp`; stop if it is not the job file. In the app-bridge mode the user may switch tabs.
- Never draw into, or `save` over, the input or a reference drawing. `save {path}` with a new version name.
- Calls are serial. After `isError: true` or a lost connection, query the drawing (`inspect_drawing`, undo history) before deciding what is missing; do not replay the whole batch.
- `command_line` is for teaching and quick checks. For generation use `execute` so each call returns a handle and fails loudly.
- When connected to the app, objects the user draws or edits by hand belong to the user. Compare against `object-map.json` before regenerating a region.

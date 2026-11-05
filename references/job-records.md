# Coordinated job records

These are agent-prepared records, not an implemented CAD generation engine. Copy [the JSON template](../assets/templates/job-records.json) into a separate job and populate it. Nulls and empty lists are unresolved data, never zero/default specifications. Preserve prior approved values and authority references.

## Schedules

- `wall_assemblies`: id, wall condition, boundary/reference-plane meaning, core, side_a/side_b layer stacks, material and display profile, junction and opening-return rules. Record whether a requested thickness means core or total. Include source handles/paths, status and approval applicability.
- `room_levels`: room id/name, datum, FL/SL in mm, source_status and approval. Keep each room's symbol/box/text associations.
- `openings`: id, host wall, connected spaces, type, frame/leaf/rough/clear/nominal sizes separately, height, sill, handing, installation clearance, tag formatting and selected asset/anchor. Unknown values stay null. A product or fire-performance designation needs actual evidence/approval, not a similar-looking block.
- `sheet`: drawing type/variant, paper and scale, frame asset, font/plot dependencies and verification state.

Source statuses: `observed`, `proposed`, `user_confirmed`, `project_confirmed`, `unresolved`. Observation is not approval for transfer to another project. Group missing choices into a consolidated proposal. Allow independent drafting while affected areas remain draft. Review records belong outside the installed skill.

## Coverage and review

For each wall, finish, insulation, hatch, door_window, furniture_equipment, centerline, dimension, annotation and sheet category, store `required`, `status`, source evidence, generated handles, concrete checks and unresolved issues. Status is `pass`, `fail`, `unresolved` or `not_applicable`. Only demonstrably absent scope may be not_applicable, with a reason; it cannot excuse an omitted required category.

Each check records expected relation/value, observed result, method and evidence path. Include nested context/transforms when handles alone are ambiguous. Track dimensions to semantic anchors and tags to schedule IDs. Candidate parts include status and review evidence; only reviewed parts enter the approved library.

Distinguish saved-DWG integrity, visual-detail review, reference benchmark and plotted-sheet checks. An all-present object inventory is not an all-pass coverage report. Produce HTML with full-sheet comparisons, matched detail crops, source/target locations and proposed/unresolved decisions. Keep architectural notes in CAD and debugging/assumption panels out of the presentation sheet.

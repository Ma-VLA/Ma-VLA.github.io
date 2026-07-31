# Ma-VLA Research Program

GitHub Pages site for Yubeen Ha's progressive research program in adaptive
vision-language-action robot control:
[ma-vla.github.io](https://ma-vla.github.io/).

## Public research progression

1. **Stage 1 — FlowBridge / E6 VLA Adaptation:** validated π0.5/v23 policy,
   explicit 7D action contract, ROS2 execution, and physical evaluation on the
   Dobot Magician E6.
2. **Transition 1 — E6 Validation to xArm6:** v1–v26 evidence review and
   transfer rationale.
3. **Stage 2A — Quest 3–xArm6 Demonstration Collection:** Quest 3 WebXR
   teleoperation and synchronized ROS2 demonstration-capture infrastructure.
4. **Stage 2B — xArm6 Policy Training and Deployment Contract:** the book
   classification and shelf-insertion task, the three-machine topology, and a
   collection-to-inference path executed end to end on recorded episodes.

## Site structure

- `index.html` — program thesis, cumulative architecture, public stages, and representative evidence
- `contents.html` — complete index of every page and section
- `research.html` — research-program narrative and collection-method comparison
- `projects/flowbridge.html` — validated Stage 1 research
- `transitions/e6-to-xarm6.html` — Transition 1 rationale and Stage 2B status
- `projects/quest3-xarm6.html` — operational Stage 2A collection system
- `projects/e7-xarm6-policy.html` — Stage 2B training and deployment contract
- `results.html` — protocol-separated E6 task and control experiments
- `technical/e6-policy-evolution.html` — curated Stage 1 technical analysis, including the v17–v26 vision-LoRA ablation
- `system/` — E6 system and ROS2 runtime details
- `publications.html` — KSCI record and JKSCI manuscript status
- `OWNERSHIP.md` — which machine's session owns which block, and how to add to a block you do not own

Every `<section>` carries a stable `id`. `contents.html` and external links depend
on them, so they are added but not renamed.

## Representative Stage 1 contract

- Model: `pi05_e6_v23_lora`, 20,000 steps
- Dataset: `dobot_e6_pick_place_orange_v16`, 198 episodes / 42,495 frames
- Action: six frame-to-frame joint-position deltas in degrees plus one
  absolute binary suction command
- Horizon: 16
- ROS2 executor: measured 16 Hz
- Action horizon: 16 / consume first 8 steps

Quantitative task results apply only to the validated Dobot E6 setup.

## Deployment

GitHub Pages deploys the repository root from `main`.

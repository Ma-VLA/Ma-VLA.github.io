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

## Site structure

- `index.html` — program thesis, cumulative architecture, public stages, and representative evidence
- `research.html` — research-program narrative and collection-method comparison
- `projects/flowbridge.html` — validated Stage 1 research
- `transitions/e6-to-xarm6.html` — Transition 1 rationale
- `projects/quest3-xarm6.html` — operational Stage 2A collection system
- `results.html` — protocol-separated E6 task and control experiments
- `technical/e6-policy-evolution.html` — curated Stage 1 technical analysis
- `system/` — E6 system and ROS2 runtime details
- `publications.html` — KSCI record and JKSCI manuscript status

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

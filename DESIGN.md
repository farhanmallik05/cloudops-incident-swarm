# Design System: CloudOps Autonomous Multi-Agent SRE Swarm Dashboard

## 1. Visual Theme & Atmosphere
A mission-critical CloudOps aerospace command center. Engineered for Site Reliability Engineers managing high-stakes cloud outages. Combines military terminal precision with modern glassmorphic telemetry.
- **Density:** Cockpit Dense (Density: 7) — High information density, real-time live log streams, and status cards calibrated for sub-second visual scanning.
- **Variance:** Offset Modular (Variance: 6) — Hierarchical 4-agent topology bar, dual-column console & post-mortem workspace, and floating chaos injection drawer.
- **Motion:** Responsive Real-Time Telemetry (Motion: 6) — Real-time SSE streaming pulses, glowing status pill blinks, and tactile button feedback.

## 2. Color Palette & Roles
- **OLED Void** (`#070a12`) — Mission control cockpit background
- **Graphite Shell** (`#0e1424`) — Double-bezel outer container enclosure
- **Substrate Panel** (`#131c33`) — Inner console workspace and incident trace card fill
- **Signal Indigo** (`#6366f1`) — Primary coordinator accent (Incident Commander)
- **Telemetry Emerald** (`#10b981`) — Log Triage Specialist and healthy service indicators
- **Diagnostic Violet** (`#a855f7`) — Root Cause Diagnostic Specialist and suspect commit highlights
- **Remediation Amber** (`#f59e0b`) — Safe rollback engine and awaiting human-in-the-loop approval
- **Panic Crimson** (`#f43f5e`) — CloudWatch alarm triggers, P1 chaos injections, and outage badges
- **Ghost Hairline** (`rgba(255, 255, 255, 0.08)`) — 1px structural dividing lines
- **Specular Highlight** (`rgba(255, 255, 255, 0.12)`) — Machined top edge refraction

## 3. Typography Rules
- **Display / Headers:** `Plus Jakarta Sans`, 700 Bold to 800 ExtraBold, tracking-tight.
- **Body & Labels:** `Plus Jakarta Sans`, 500 Medium to 600 SemiBold.
- **Console & Metrics:** `JetBrains Mono` with `tabular-nums` for all CloudWatch error logs, git commit SHAs, latency milliseconds, and token dollar costs ($0.05475 USD).
- **Banned:** Generic browser serif or unstyled system fonts.

## 4. Component Stylings
- **The "Double-Bezel" (Doppelrand):**
  - *Outer Frame:* `p-1.5 rounded-2xl bg-white/[0.04] ring-1 ring-white/10 shadow-2xl`
  - *Inner Core:* `rounded-[calc(1rem-0.25rem)] bg-[#0e1424]/95 shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)] p-5`
- **Agent Topology Cards:** 4 distinct specialist cards with color-coded avatar shields, model tier badges (Sonnet vs Haiku), and animated status indicators (`IDLE`, `INVESTIGATING`, `COMPLETED`).
- **Telemetry Console:** Machined terminal viewport with monospace log stream, colored timestamp tags, and auto-scrolling trace buffer.
- **Chaos Injection Controls:** Tactical buttons with striped hazard borders and instant fault simulation.
- **Human-in-the-Loop (HITL) Modal:** Hardware-backed KMS cryptographic signature verification panel with canonical JSON payload preview and one-click SRE approval.

## 5. Layout Principles
- **Command Cockpit Flow:** Top header with incident status & quick actions -> 4-Agent Swarm Topology Bar -> 2-Column Split (Live Trace Console vs Post-Mortem Synthesizer) -> Token Cost & Telemetry HUD.
- **Responsive Stack (< 1024px):** Agent cards collapse into a 2x2 grid, trace console and post-mortem stack vertically with preserved terminal scroll.

## 6. Motion Philosophy
- State change transitions: `transition-all duration-300 ease-[cubic-bezier(0.32,0.72,0,1)]`.
- Live pulse pings on active investigating agents.
- Real-time terminal auto-scroll without layout reflow jank.

## 7. Anti-Patterns (Banned)
- ❌ No blinding white surfaces in mission control
- ❌ No generic circular spinners — real-time pulse bars instead
- ❌ No unverified mutating actions — HMAC authorization gate strictly enforced
- ❌ No unformatted JSON dumps — human-readable post-mortem synthesis


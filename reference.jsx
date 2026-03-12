import { useState, useEffect, useRef } from "react";

// ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
const globalStyles = `
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=JetBrains+Mono:wght@300;400;500;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --cyan:   #00cfff;
    --pink:   #ff0080;
    --purple: #9d4edd;
    --green:  #00e5a0;
    --amber:  #ffaa00;
    --red:    #ff3355;
    --bg-deep:  #03050d;
    --bg-mid:   #07091a;
    --bg-panel: #060910;
    --chrome:   #1a1e2e;
    --glass:        rgba(0, 207, 255, 0.03);
    --glass-pink:   rgba(255, 0, 128, 0.05);
    --glass-border: rgba(0, 207, 255, 0.12);
    --glass-border-pink: rgba(255, 0, 128, 0.22);
    --text-primary: #ffffff;
    --text-dim:     rgba(220, 185, 240, 0.52);
    --font-hud:  'Orbitron', monospace;
    --font-mono: 'JetBrains Mono', monospace;
    --font-body: 'Rajdhani', sans-serif;
  }

  html, body { height: 100%; background: var(--bg-deep); color: var(--text-primary); font-family: var(--font-body); overflow-x: hidden; }

  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: var(--bg-deep); }
  ::-webkit-scrollbar-thumb { background: linear-gradient(var(--pink), var(--cyan)); border-radius: 2px; }

  @keyframes gridPulse {
    0%, 100% { opacity: 0.25; }
    50% { opacity: 0.5; }
  }
  @keyframes radarSweep {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.95); }
  }
  @keyframes scanLine {
    0% { top: -2px; }
    100% { top: 100%; }
  }
  @keyframes flicker {
    0%, 100% { opacity: 1; }
    91% { opacity: 1; }
    92% { opacity: 0.3; }
    93% { opacity: 1; }
    96% { opacity: 0.6; }
    97% { opacity: 1; }
  }
  @keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
  }
  @keyframes slideInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes glowPink {
    0%, 100% { box-shadow: 0 0 12px var(--pink), 0 0 24px rgba(255,0,128,0.35); }
    50%       { box-shadow: 0 0 28px var(--pink), 0 0 56px rgba(255,0,128,0.55), 0 0 80px rgba(255,0,128,0.18); }
  }
  @keyframes glowCyan {
    0%, 100% { box-shadow: 0 0 10px var(--cyan), 0 0 20px rgba(0,207,255,0.3); }
    50%       { box-shadow: 0 0 22px var(--cyan), 0 0 44px rgba(0,207,255,0.5), 0 0 66px rgba(0,207,255,0.15); }
  }
  @keyframes ticker {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
  @keyframes arcDraw {
    from { stroke-dashoffset: 400; }
    to { stroke-dashoffset: 0; }
  }
  @keyframes dataStream {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
  }
  @keyframes rotate {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }
  @keyframes counterRotate {
    from { transform: rotate(0deg); }
    to   { transform: rotate(-360deg); }
  }
  @keyframes heatPulse {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 1; }
  }
  @keyframes borderPulse {
    0%, 100% { border-color: rgba(255,0,128,0.18); }
    50%       { border-color: rgba(255,0,128,0.45); }
  }
  @keyframes magentaDrift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  .grid-bg {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
      linear-gradient(rgba(255,0,128,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,207,255,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridPulse 5s ease-in-out infinite;
  }

  .glass-pane {
    background: linear-gradient(135deg, rgba(255,0,128,0.045), rgba(0,207,255,0.025));
    backdrop-filter: blur(40px) saturate(200%);
    -webkit-backdrop-filter: blur(40px) saturate(200%);
    border: 1px solid rgba(255,0,128,0.2);
    border-radius: 8px;
    animation: borderPulse 4s ease-in-out infinite;
  }

  .scan-line {
    position: absolute; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #ff0080, #00cfff, transparent);
    animation: scanLine 3s linear infinite;
    pointer-events: none; z-index: 10;
  }

  .btn-primary {
    font-family: var(--font-hud);
    font-size: 11px;
    letter-spacing: 0.2em;
    padding: 12px 28px;
    background: linear-gradient(90deg, rgba(255,0,128,0.1), rgba(0,207,255,0.07));
    border: 1px solid #ff0080;
    color: #fff;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
    animation: glowPink 2.5s ease-in-out infinite;
    text-shadow: 0 0 10px rgba(255,0,128,0.6);
  }
  .btn-primary:hover {
    background: linear-gradient(90deg, rgba(255,0,128,0.22), rgba(0,207,255,0.14));
    box-shadow: 0 0 35px rgba(255,0,128,0.7), 0 0 70px rgba(255,0,128,0.2);
  }
  .btn-primary::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,0,128,0.3), rgba(0,207,255,0.15), transparent);
    transform: translateX(-100%);
    transition: transform 0.6s;
  }
  .btn-primary:hover::before { transform: translateX(100%); }

  @keyframes borderPulse {
    0%, 100% { border-color: rgba(255,0,128,0.2); }
    50%       { border-color: rgba(255,0,128,0.48); }
  }

  .input-field {
    width: 100%;
    background: rgba(255,0,128,0.03);
    border: 1px solid rgba(255,0,128,0.18);
    border-bottom: 2px solid #ff0080;
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-size: 13px;
    padding: 10px 14px;
    outline: none;
    transition: all 0.3s;
    border-radius: 4px 4px 0 0;
  }
  .input-field:focus {
    border-color: #ff0080;
    background: rgba(255,0,128,0.07);
    box-shadow: 0 0 20px rgba(255,0,128,0.2), 0 0 6px rgba(0,207,255,0.1);
  }
  .input-field::placeholder { color: rgba(255,0,128,0.35); }

  .corner-bracket { position: absolute; width: 16px; height: 16px; border-style: solid; opacity: 0.75; }
  .corner-tl { top: 0; left: 0; border-width: 2px 0 0 2px; border-color: #ff0080; }
  .corner-tr { top: 0; right: 0; border-width: 2px 2px 0 0; border-color: #00cfff; }
  .corner-bl { bottom: 0; left: 0; border-width: 0 0 2px 2px; border-color: #00cfff; }
  .corner-br { bottom: 0; right: 0; border-width: 0 2px 2px 0; border-color: #ff0080; }

  .nav-item {
    font-family: var(--font-hud); font-size: 9px; letter-spacing: 0.15em;
    color: var(--text-dim); padding: 10px 16px; cursor: pointer;
    transition: all 0.3s; border-left: 2px solid transparent;
    display: flex; align-items: center; gap: 10px; text-transform: uppercase;
  }
  .nav-item:hover, .nav-item.active {
    color: #ff0080; border-left-color: #ff0080;
    background: rgba(255,0,128,0.07);
    text-shadow: 0 0 12px rgba(255,0,128,0.7);
  }

  .integrity-bar {
    height: 4px;
    border-radius: 2px;
    position: relative;
    overflow: hidden;
  }
  .integrity-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease;
    position: relative;
  }
  .integrity-bar-fill::after {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 20px; height: 100%;
    background: rgba(255,255,255,0.5);
    filter: blur(3px);
  }

  .chat-bubble { animation: slideInUp 0.3s ease forwards; }

  .ticker-wrap { overflow: hidden; white-space: nowrap; }
  .ticker-inner {
    display: inline-block;
    animation: ticker 25s linear infinite;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--pink);
    opacity: 0.8;
  }

  .flicker { animation: flicker 5s linear infinite; }

  .heatmap-cell {
    border-radius: 3px;
    transition: all 0.3s;
    cursor: pointer;
  }
  .heatmap-cell:hover { transform: scale(1.1); filter: brightness(1.4); }
`;

// ─── MOCK DATA ────────────────────────────────────────────────────────────────
const MODELS = [
  { id: "gpt4",   name: "GPT-4o",      score: 87, status: "SECURE",  color: "#00cfff" },
  { id: "llama",  name: "Llama-3.1",   score: 72, status: "CAUTION", color: "#ff0080" },
  { id: "groq",   name: "Groq-Mixtral",score: 91, status: "SECURE",  color: "#00e5a0" },
  { id: "claude", name: "Claude-3.5",  score: 94, status: "OPTIMAL", color: "#bf5fff" },
];

const ARCHIVE_ENTRIES = [
  { id: "AUD-7742", query: "Explain quantum entanglement", score: 92, model: "GPT-4o", ts: "2025-03-12 14:22:01", risk: "LOW" },
  { id: "AUD-7741", query: "What caused the 2008 financial crisis?", score: 78, model: "Llama-3.1", ts: "2025-03-12 13:55:44", risk: "MED" },
  { id: "AUD-7740", query: "List all US presidents since 1990", score: 95, model: "Claude-3.5", ts: "2025-03-12 12:30:19", risk: "LOW" },
  { id: "AUD-7739", query: "Side effects of metformin", score: 61, model: "Groq-Mixtral", ts: "2025-03-11 23:10:05", risk: "HIGH" },
  { id: "AUD-7738", query: "History of Byzantine Empire", score: 83, model: "GPT-4o", ts: "2025-03-11 20:44:32", risk: "LOW" },
  { id: "AUD-7737", query: "Current stock price of NVIDIA", score: 34, model: "Llama-3.1", ts: "2025-03-11 18:02:17", risk: "HIGH" },
];

const TICKER_ITEMS = [
  "QUERY_ID::7742 → TRUTH_SCORE: 92.4%",
  "MODEL::GPT-4o → HALLUCINATION_RISK: LOW",
  "GROQ_STREAM::ACTIVE → LATENCY: 142ms",
  "INTEGRITY_CHECK::PASS → VECTOR_MATCH: 0.94",
  "AUDIT_LOG::WRITING → BLOCK_7742",
  "TEMPORAL_DRIFT::+0.3% → STABLE",
];

const HEATMAP_TOPICS = ["Medical", "Legal", "Finance", "History", "Science", "Tech", "Politics", "Math"];
const HEATMAP_DATA = [
  [0.9, 0.8, 0.85, 0.3, 0.4, 0.35, 0.75, 0.2],
  [0.85, 0.75, 0.9, 0.25, 0.35, 0.3, 0.8, 0.15],
  [0.7, 0.65, 0.7, 0.2, 0.3, 0.25, 0.7, 0.1],
  [0.6, 0.55, 0.6, 0.15, 0.25, 0.2, 0.65, 0.08],
];

// ─── COMPONENTS ───────────────────────────────────────────────────────────────

function GridBg() {
  return <div className="grid-bg" />;
}

function CornerBrackets() {
  return (
    <>
      <div className="corner-bracket corner-tl" />
      <div className="corner-bracket corner-tr" />
      <div className="corner-bracket corner-bl" />
      <div className="corner-bracket corner-br" />
    </>
  );
}

// ── Radar Canvas ──────────────────────────────────────────────────────────────
function HallucinationRadar({ size = 280, scores = [87, 72, 91] }) {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const angleRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const cx = size / 2, cy = size / 2;

    function draw() {
      ctx.clearRect(0, 0, size, size);

      // Background circles
      for (let i = 1; i <= 5; i++) {
        const r = (size / 2 - 10) * (i / 5);
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(255,0,128,${0.04 + i * 0.015})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Crosshairs
      ctx.strokeStyle = "rgba(0,207,255,0.07)";
      ctx.lineWidth = 1;
      for (let a = 0; a < 360; a += 30) {
        const rad = (a * Math.PI) / 180;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(rad) * (size / 2 - 10), cy + Math.sin(rad) * (size / 2 - 10));
        ctx.stroke();
      }

      // Arcs for models
      const arcs = [
        { score: scores[0], color: "#ff0080", r: size / 2 - 20, w: 12 },
        { score: scores[1], color: "#00cfff", r: size / 2 - 40, w: 12 },
        { score: scores[2], color: "#00e5a0", r: size / 2 - 60, w: 12 },
      ];
      arcs.forEach(({ score, color, r, w }) => {
        const end = ((score / 100) * Math.PI * 2) - Math.PI / 2;
        ctx.beginPath();
        ctx.arc(cx, cy, r, -Math.PI / 2, end);
        ctx.strokeStyle = color;
        ctx.lineWidth = w;
        ctx.lineCap = "round";
        ctx.shadowColor = color;
        ctx.shadowBlur = 10;
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Track (background arc)
        ctx.beginPath();
        ctx.arc(cx, cy, r, -Math.PI / 2, Math.PI * 1.5);
        ctx.strokeStyle = `${color}18`;
        ctx.lineWidth = w;
        ctx.stroke();
      });

      // Rotating sweep
      angleRef.current += 0.008;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(angleRef.current);
      const grad = ctx.createLinearGradient(0, -(size / 2 - 10), 0, 0);
      grad.addColorStop(0, "rgba(255,0,128,0)");
      grad.addColorStop(0.7, "rgba(255,0,128,0.08)");
      grad.addColorStop(1, "rgba(255,0,128,0.32)");
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.arc(0, 0, size / 2 - 10, -Math.PI / 2 - 0.4, -Math.PI / 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Sweep line
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(0, -(size / 2 - 10));
      ctx.strokeStyle = "rgba(255,0,128,0.95)";
      ctx.lineWidth = 2;
      ctx.shadowColor = "#ff0080";
      ctx.shadowBlur = 18;
      ctx.stroke();
      ctx.shadowBlur = 0;
      ctx.restore();

      // Center dot
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fillStyle = "#00cfff";
      ctx.shadowColor = "#00cfff";
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.shadowBlur = 0;

      // Blips
      const blips = [
        { a: 0.8, r: 0.6, c: "#00e5a0" },
        { a: 2.1, r: 0.75, c: "#ff0080" },
        { a: 4.5, r: 0.45, c: "#ffaa00" },
        { a: 5.2, r: 0.8, c: "#00cfff" },
      ];
      blips.forEach(({ a, r: br, c }) => {
        const x = cx + Math.cos(a) * br * (size / 2 - 60);
        const y = cy + Math.sin(a) * br * (size / 2 - 60);
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = c;
        ctx.shadowColor = c;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      animRef.current = requestAnimationFrame(draw);
    }

    draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [size, scores]);

  return <canvas ref={canvasRef} width={size} height={size} style={{ display: "block" }} />;
}

// ── Sidebar Nav ───────────────────────────────────────────────────────────────
const NAV_ITEMS = [
  { id: "landing", icon: "⬡", label: "Entry Portal" },
  { id: "dashboard", icon: "◈", label: "The Hub" },
  { id: "chat", icon: "⟁", label: "Interrogation" },
  { id: "analysis", icon: "⎊", label: "The Lab" },
  { id: "archive", icon: "⬢", label: "The Vault" },
  { id: "settings", icon: "⚙", label: "Engine Room" },
];

function Sidebar({ page, setPage }) {
  return (
    <div style={{
      width: 200, minHeight: "100vh", flexShrink: 0,
      borderRight: "1px solid rgba(255,0,128,0.12)",
      background: "rgba(3,5,13,0.92)",
      backdropFilter: "blur(24px)",
      display: "flex", flexDirection: "column",
      position: "relative", zIndex: 100,
    }}>
      {/* Logo */}
      <div style={{ padding: "20px 20px 16px", borderBottom: "1px solid rgba(255,0,128,0.1)", display: "flex", alignItems: "center", gap: 10 }}>
        <img
          src="/mnt/user-data/uploads/1773302659738_logo.png"
          alt="Aletheia Gate"
          style={{ width: 36, height: 36, borderRadius: "50%", objectFit: "cover", flexShrink: 0, boxShadow: "0 0 14px rgba(255,0,128,0.55), 0 0 28px rgba(0,207,255,0.2)" }}
        />
        <div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 12, color: "var(--pink)", fontWeight: 700, letterSpacing: "0.1em" }}>ALETHEIA</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--cyan)", letterSpacing: "0.25em", marginTop: 1 }}>GATE // v2.4.1</div>
        </div>
      </div>

      {/* Status */}
      <div style={{ padding: "12px 20px", borderBottom: "1px solid rgba(255,0,128,0.08)", display: "flex", alignItems: "center", gap: 8 }}>
        <div className="status-dot" style={{ background: "var(--green)", boxShadow: "0 0 8px var(--green)" }} />
        <span style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--green)", letterSpacing: "0.1em" }}>CORE: OPTIMAL</span>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: "10px 0" }}>
        {NAV_ITEMS.map(item => (
          <div
            key={item.id}
            className={`nav-item${page === item.id ? " active" : ""}`}
            onClick={() => setPage(item.id)}
          >
            <span style={{ fontSize: 14, opacity: 0.8 }}>{item.icon}</span>
            <span>{item.label}</span>
          </div>
        ))}
      </nav>

      {/* Auth buttons */}
      <div style={{ padding: "16px", borderTop: "1px solid rgba(255,0,128,0.1)", display: "flex", flexDirection: "column", gap: 8 }}>
        <div onClick={() => setPage("login")} style={{ cursor: "pointer", textAlign: "center", fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--text-dim)", letterSpacing: "0.15em", padding: "6px", border: "1px solid rgba(0,207,255,0.15)", borderRadius: 3, transition: "all 0.2s" }}
          onMouseEnter={e => { e.target.style.color = "var(--cyan)"; e.target.style.borderColor = "rgba(0,207,255,0.4)"; }}
          onMouseLeave={e => { e.target.style.color = "var(--text-dim)"; e.target.style.borderColor = "rgba(0,207,255,0.15)"; }}>
          LOGIN
        </div>
        <div onClick={() => setPage("signup")} style={{ cursor: "pointer", textAlign: "center", fontFamily: "var(--font-hud)", fontSize: 8, color: "#fff", letterSpacing: "0.15em", padding: "6px", border: "1px solid var(--pink)", borderRadius: 3, background: "rgba(255,0,128,0.1)", boxShadow: "0 0 10px rgba(255,0,128,0.2)" }}>
          SIGNUP
        </div>
      </div>
    </div>
  );
}

// ── LANDING PAGE ──────────────────────────────────────────────────────────────
function LandingPage({ setPage }) {
  const [hovered, setHovered] = useState(null);
  const [hovNav, setHovNav] = useState(null);
  const [counter, setCounter] = useState({ audits: 0, accuracy: 0, models: 0 });
  const radarRef = useRef(null);
  const animRef = useRef(null);
  const angleRef = useRef(0);

  // Animated counters
  useEffect(() => {
    let frame = 0;
    const target = { audits: 247893, accuracy: 94.7, models: 4 };
    const duration = 120;
    const timer = setInterval(() => {
      frame++;
      const p = Math.min(frame / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      setCounter({
        audits: Math.floor(ease * target.audits),
        accuracy: +(ease * target.accuracy).toFixed(1),
        models: Math.floor(ease * target.models),
      });
      if (frame >= duration) clearInterval(timer);
    }, 16);
    return () => clearInterval(timer);
  }, []);

  // Hero radar animation
  useEffect(() => {
    const canvas = radarRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const S = 420;
    const cx = S / 2, cy = S / 2;

    function draw() {
      ctx.clearRect(0, 0, S, S);
      // Rings
      for (let i = 1; i <= 6; i++) {
        const r = (S / 2 - 8) * (i / 6);
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(255,0,128,${0.03 + i * 0.012})`; ctx.lineWidth = 1; ctx.stroke();
      }
      // Spokes
      for (let a = 0; a < 360; a += 22.5) {
        const rad = (a * Math.PI) / 180;
        ctx.beginPath(); ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(rad) * (S / 2 - 8), cy + Math.sin(rad) * (S / 2 - 8));
        ctx.strokeStyle = "rgba(0,207,255,0.05)"; ctx.lineWidth = 1; ctx.stroke();
      }
      // Arcs
      const arcs = [
        { s: 87, c: "#ff0080", r: S / 2 - 22, w: 14 },
        { s: 91, c: "#00cfff", r: S / 2 - 46, w: 14 },
        { s: 72, c: "#00e5a0", r: S / 2 - 70, w: 14 },
        { s: 94, c: "#bf5fff", r: S / 2 - 94, w: 14 },
      ];
      arcs.forEach(({ s, c, r, w }) => {
        ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, Math.PI * 1.5);
        ctx.strokeStyle = `${c}14`; ctx.lineWidth = w; ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, ((s / 100) * Math.PI * 2) - Math.PI / 2);
        ctx.strokeStyle = c; ctx.lineWidth = w; ctx.lineCap = "round";
        ctx.shadowColor = c; ctx.shadowBlur = 16; ctx.stroke(); ctx.shadowBlur = 0;
      });
      // Sweep
      angleRef.current += 0.006;
      ctx.save(); ctx.translate(cx, cy); ctx.rotate(angleRef.current);
      const g = ctx.createLinearGradient(0, -(S / 2 - 8), 0, 0);
      g.addColorStop(0, "rgba(255,0,128,0)");
      g.addColorStop(0.6, "rgba(255,0,128,0.06)");
      g.addColorStop(1, "rgba(255,0,128,0.28)");
      ctx.beginPath(); ctx.moveTo(0, 0);
      ctx.arc(0, 0, S / 2 - 8, -Math.PI / 2 - 0.5, -Math.PI / 2);
      ctx.fillStyle = g; ctx.fill();
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -(S / 2 - 8));
      ctx.strokeStyle = "rgba(255,0,128,0.95)"; ctx.lineWidth = 2;
      ctx.shadowColor = "#ff0080"; ctx.shadowBlur = 20; ctx.stroke(); ctx.shadowBlur = 0;
      ctx.restore();
      // Blips
      [{ a: 0.7, r: 0.55, c: "#00e5a0" }, { a: 2.2, r: 0.72, c: "#ff0080" },
       { a: 3.8, r: 0.4, c: "#ffaa00" }, { a: 5.0, r: 0.78, c: "#00cfff" },
       { a: 1.5, r: 0.62, c: "#bf5fff" }, { a: 4.3, r: 0.5, c: "#00e5a0" }
      ].forEach(({ a, r: br, c }) => {
        const x = cx + Math.cos(a) * br * (S / 2 - 100);
        const y = cy + Math.sin(a) * br * (S / 2 - 100);
        ctx.beginPath(); ctx.arc(x, y, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = c; ctx.shadowColor = c; ctx.shadowBlur = 10; ctx.fill(); ctx.shadowBlur = 0;
      });
      // Center
      ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fillStyle = "#00cfff"; ctx.shadowColor = "#00cfff"; ctx.shadowBlur = 20; ctx.fill(); ctx.shadowBlur = 0;

      animRef.current = requestAnimationFrame(draw);
    }
    draw();
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  const features = [
    { title: "HALLUCINATION RADAR", icon: "◎", desc: "Real-time probabilistic scanning of AI outputs using multi-model cross-referencing with 12-layer neural verification protocols.", color: "#bf5fff" },
    { title: "INTEGRITY INDEX", icon: "⬡", desc: "Forensic-grade scoring engine assigning confidence ratings to every sentence generated by connected LLM endpoints.", color: "#00f5ff" },
    { title: "TRUTH ARCHIVE", icon: "⬢", desc: "Immutable audit trail with cryptographic timestamps — every truth-check preserved in the Vault for legal accountability.", color: "#39ff14" },
    { title: "MULTI-MODEL SYNC", icon: "⎊", desc: "Simultaneous interrogation of GPT-4o, Llama, Groq, and Claude endpoints. Compare, contrast, and validate in parallel.", color: "#ffaa00" },
    { title: "FORENSIC CHAT", icon: "⟁", desc: "Terminal-style interrogation interface that watches the AI's reasoning in real-time — word by word, claim by claim.", color: "#00f5ff" },
    { title: "DRIFT ANALYTICS", icon: "⌬", desc: "Historical pattern analysis revealing which topics and models drift most over time — visualized as temporal decay curves.", color: "#bf5fff" },
  ];

  const navLinks = ["FEATURES", "HOW IT WORKS", "MODELS", "ABOUT"];

  return (
    <div style={{ position: "relative", minHeight: "100vh", overflowX: "hidden", background: "var(--bg-deep)" }}>

      {/* ── Top nav bar ── */}
      <nav style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 200,
        padding: "0 60px", height: 64,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        background: "rgba(3,5,13,0.9)", backdropFilter: "blur(28px)",
        borderBottom: "1px solid rgba(255,0,128,0.1)",
      }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <img
            src="/mnt/user-data/uploads/1773302659738_logo.png"
            alt="Aletheia Gate"
            style={{ width: 44, height: 44, borderRadius: "50%", objectFit: "cover", boxShadow: "0 0 18px rgba(255,0,128,0.6), 0 0 36px rgba(0,207,255,0.25)" }}
          />
          <div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 14, color: "var(--pink)", fontWeight: 900, letterSpacing: "0.12em", lineHeight: 1 }}>ALETHEIA</div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--cyan)", letterSpacing: "0.3em" }}>GATE // v2.4.1</div>
          </div>
        </div>

        {/* Nav links */}
        <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
          {navLinks.map(link => (
            <div key={link}
              onMouseEnter={() => setHovNav(link)}
              onMouseLeave={() => setHovNav(null)}
              style={{
                fontFamily: "var(--font-hud)", fontSize: 9, letterSpacing: "0.18em",
                color: hovNav === link ? "var(--cyan)" : "var(--text-dim)",
                padding: "8px 18px", cursor: "pointer", transition: "all 0.2s",
                borderBottom: hovNav === link ? "1px solid var(--cyan)" : "1px solid transparent",
              }}>{link}</div>
          ))}
        </div>

        {/* Auth */}
        <div style={{ display: "flex", gap: 10 }}>
          <button onClick={() => setPage("login")} style={{
            fontFamily: "var(--font-hud)", fontSize: 9, letterSpacing: "0.15em",
            background: "transparent", border: "1px solid rgba(0,245,255,0.25)",
            color: "var(--text-dim)", padding: "8px 20px", cursor: "pointer", borderRadius: 3,
            transition: "all 0.2s",
          }}
            onMouseEnter={e => { e.target.style.borderColor = "var(--cyan)"; e.target.style.color = "var(--cyan)"; }}
            onMouseLeave={e => { e.target.style.borderColor = "rgba(0,245,255,0.25)"; e.target.style.color = "var(--text-dim)"; }}>
            LOGIN
          </button>
          <button onClick={() => setPage("signup")} className="btn-primary" style={{ fontSize: 9, padding: "8px 20px" }}>
            GET ACCESS
          </button>
        </div>
      </nav>

      {/* ── HERO SECTION ── */}
      <section style={{ minHeight: "100vh", display: "flex", alignItems: "center", padding: "80px 60px 60px", position: "relative", overflow: "hidden" }}>
        {/* Ambient glows */}
        <div style={{ position: "absolute", top: "10%", left: "5%", width: 700, height: 700, borderRadius: "50%", background: "radial-gradient(circle, rgba(255,0,128,0.07) 0%, transparent 65%)", pointerEvents: "none" }} />
        <div style={{ position: "absolute", bottom: "0%", right: "5%", width: 600, height: 600, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,207,255,0.06) 0%, transparent 65%)", pointerEvents: "none" }} />

        {/* Left: copy */}
        <div style={{ flex: 1, maxWidth: 600, animation: "slideInLeft 0.9s ease forwards", zIndex: 2 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 28 }}>
            <div className="status-dot" style={{ background: "var(--green)", boxShadow: "0 0 10px var(--green)" }} />
            <span style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--green)", letterSpacing: "0.35em" }}>QUANTUM TRUTH INTERFACE // ONLINE</span>
          </div>

          {/* Eyebrow */}
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--pink)", letterSpacing: "0.3em", marginBottom: 20, display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ height: 1, width: 32, background: "var(--pink)" }} />
            FORENSIC-GRADE AI AUDITING
          </div>

          {/* Main title */}
          <div style={{ fontFamily: "var(--font-hud)", fontWeight: 900, lineHeight: 0.95, letterSpacing: "0.04em", marginBottom: 32 }}>
            <div style={{ fontSize: "clamp(56px, 7vw, 96px)", color: "var(--pink)", textShadow: "0 0 40px rgba(255,0,128,0.6), 0 0 80px rgba(255,0,128,0.2)" }} className="flicker">
              ALETHEIA
            </div>
            <div style={{ fontSize: "clamp(52px, 6.5vw, 88px)", color: "var(--cyan)", textShadow: "0 0 40px rgba(0,207,255,0.5), 0 0 80px rgba(0,207,255,0.2)" }}>
              GATE
            </div>
          </div>

          {/* Tagline */}
          <div style={{
            fontFamily: "var(--font-mono)", fontSize: 13, letterSpacing: "0.4em",
            color: "var(--text-dim)", marginBottom: 10,
            borderLeft: "3px solid var(--pink)", paddingLeft: 18,
          }}>
            VERITAS SINE FINE
          </div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "rgba(0,207,255,0.35)", letterSpacing: "0.25em", marginBottom: 36, paddingLeft: 21 }}>
            TRUTH WITHOUT END
          </div>

          <p style={{ fontFamily: "var(--font-body)", fontSize: 17, color: "var(--text-dim)", lineHeight: 1.75, maxWidth: 520, marginBottom: 48 }}>
            The first forensic-grade Quantum Truth Interface. Built for researchers, developers, and power users who demand verifiable certainty — not just answers — from every AI endpoint they touch.
          </p>

          {/* CTA buttons */}
          <div style={{ display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap" }}>
            <button className="btn-primary" onClick={() => setPage("signup")} style={{ fontSize: 10, padding: "14px 32px" }}>
              ⬡ INITIATE QUANTUM HANDSHAKE
            </button>
            <button onClick={() => setPage("login")} style={{
              fontFamily: "var(--font-hud)", fontSize: 10, letterSpacing: "0.2em",
              background: "transparent", border: "none", color: "var(--text-dim)",
              cursor: "pointer", display: "flex", alignItems: "center", gap: 8, transition: "all 0.3s",
              padding: "14px 0",
            }}
              onMouseEnter={e => e.currentTarget.style.color = "var(--cyan)"}
              onMouseLeave={e => e.currentTarget.style.color = "var(--text-dim)"}>
              RETURNING OPERATOR
              <span style={{ fontSize: 14 }}>→</span>
            </button>
          </div>

          {/* Trust badges */}
          <div style={{ display: "flex", gap: 24, marginTop: 52, flexWrap: "wrap" }}>
            {[
              { val: counter.audits.toLocaleString(), label: "TRUTH AUDITS RUN" },
              { val: `${counter.accuracy}%`, label: "AVG ACCURACY GAIN" },
              { val: `${counter.models}`, label: "AI MODELS MONITORED" },
            ].map(({ val, label }) => (
              <div key={label}>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 28, fontWeight: 900, color: "var(--cyan)", textShadow: "0 0 20px rgba(0,245,255,0.4)", lineHeight: 1 }}>{val}</div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--text-dim)", letterSpacing: "0.15em", marginTop: 4 }}>{label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Hero Radar */}
        <div style={{ flex: "0 0 460px", display: "flex", alignItems: "center", justifyContent: "center", position: "relative", zIndex: 2 }}>
          <div style={{ position: "relative" }}>
            {/* Outer ring glow */}
            <div style={{ position: "absolute", inset: -30, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,245,255,0.04) 0%, transparent 70%)", pointerEvents: "none" }} />

            {/* HUD labels around radar */}
            {[
              { angle: -80, text: "GPT-4o :: 87%",   color: "#00cfff" },
              { angle: 10,  text: "GROQ :: 91%",     color: "#00e5a0" },
              { angle: 100, text: "LLAMA :: 72%",    color: "#ff0080" },
              { angle: 190, text: "CLAUDE :: 94%",   color: "#bf5fff" },
            ].map(({ angle, text, color }) => {
              const rad = (angle * Math.PI) / 180;
              const x = 210 + Math.cos(rad) * 230;
              const y = 210 + Math.sin(rad) * 230;
              return (
                <div key={text} style={{
                  position: "absolute", left: x, top: y, transform: "translate(-50%, -50%)",
                  fontFamily: "var(--font-hud)", fontSize: 8, color, letterSpacing: "0.12em",
                  whiteSpace: "nowrap", textShadow: `0 0 8px ${color}`,
                  background: "rgba(2,4,10,0.8)", padding: "4px 8px", borderRadius: 2,
                  border: `1px solid ${color}33`,
                }}>{text}</div>
              );
            })}

            <canvas ref={radarRef} width={420} height={420} style={{ display: "block" }} />

            {/* Center label */}
            <div style={{
              position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)",
              textAlign: "center", pointerEvents: "none",
            }}>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--cyan)", letterSpacing: "0.2em", opacity: 0.6, marginTop: 14 }}>TRUTH CORE</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section style={{ padding: "100px 60px", position: "relative" }}>
        <div style={{ textAlign: "center", marginBottom: 70 }}>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--purple)", letterSpacing: "0.4em", marginBottom: 16 }}>— ARCHITECTURAL FLOW —</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 36, fontWeight: 900, color: "var(--text-primary)", letterSpacing: "0.05em" }}>HOW ALETHEIA WORKS</div>
        </div>

        <div style={{ display: "flex", alignItems: "stretch", gap: 0, maxWidth: 1100, margin: "0 auto", position: "relative" }}>
          {/* Connecting line */}
          <div style={{ position: "absolute", top: "50%", left: "10%", right: "10%", height: 1, background: "linear-gradient(90deg, transparent, var(--cyan), var(--purple), var(--green), transparent)", opacity: 0.3, transform: "translateY(-50%)", pointerEvents: "none" }} />

          {[
            { step: "01", title: "QUERY INTAKE", desc: "Your question is parsed, tokenized and distributed to all connected model endpoints simultaneously.", icon: "⟁", color: "#00f5ff" },
            { step: "02", title: "CROSS-REFERENCE", desc: "Each model's response is compared against the others and against our internal vector truth database.", icon: "⎊", color: "#bf5fff" },
            { step: "03", title: "SCORE & FLAG", desc: "A composite Integrity Index score is computed. Divergent claims are flagged as potential hallucinations.", icon: "◎", color: "#39ff14" },
            { step: "04", title: "ARCHIVE & REPORT", desc: "The full audit — query, responses, scores, timestamps — is sealed into the Vault as an immutable record.", icon: "⬢", color: "#ffaa00" },
          ].map((s, i) => (
            <div key={s.step} style={{ flex: 1, textAlign: "center", padding: "0 24px", position: "relative", zIndex: 1 }}>
              <div style={{
                width: 64, height: 64, borderRadius: "50%", margin: "0 auto 20px",
                background: `radial-gradient(circle, ${s.color}22, transparent)`,
                border: `1px solid ${s.color}66`,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: "var(--font-hud)", fontSize: 22, color: s.color,
                textShadow: `0 0 15px ${s.color}`,
                boxShadow: `0 0 20px ${s.color}22`,
              }}>{s.icon}</div>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: s.color, letterSpacing: "0.2em", marginBottom: 8 }}>STEP {s.step}</div>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 12, color: "var(--text-primary)", fontWeight: 700, letterSpacing: "0.08em", marginBottom: 12 }}>{s.title}</div>
              <div style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-dim)", lineHeight: 1.6 }}>{s.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── FEATURE GRID ── */}
      <section style={{ padding: "80px 60px", background: "rgba(0,5,15,0.5)" }}>
        <div style={{ textAlign: "center", marginBottom: 60 }}>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--cyan)", letterSpacing: "0.4em", marginBottom: 16 }}>— DIAGNOSTIC SUITE —</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 36, fontWeight: 900, color: "var(--text-primary)", letterSpacing: "0.05em" }}>CAPABILITIES</div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 20, maxWidth: 1100, margin: "0 auto" }}>
          {features.map((f, i) => (
            <div key={f.title}
              className="glass-pane"
              onMouseEnter={() => setHovered(i)}
              onMouseLeave={() => setHovered(null)}
              style={{
                padding: 32, position: "relative", cursor: "default",
                transition: "all 0.35s cubic-bezier(0.4, 0, 0.2, 1)",
                transform: hovered === i ? "translateY(-6px)" : "none",
                borderColor: hovered === i ? f.color : "var(--glass-border)",
                boxShadow: hovered === i ? `0 0 30px ${f.color}22, 0 20px 40px rgba(0,0,0,0.4)` : "none",
                animation: `slideInUp ${0.4 + i * 0.08}s ease both`,
              }}>
              <CornerBrackets />
              {/* Icon */}
              <div style={{
                width: 48, height: 48, borderRadius: 8, marginBottom: 20,
                background: `${f.color}12`, border: `1px solid ${f.color}44`,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: "var(--font-hud)", fontSize: 20, color: f.color,
                textShadow: `0 0 15px ${f.color}`,
              }}>{f.icon}</div>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: f.color, letterSpacing: "0.2em", marginBottom: 14 }}>{f.title}</div>
              <div style={{ fontFamily: "var(--font-body)", fontSize: 14, color: "var(--text-dim)", lineHeight: 1.7 }}>{f.desc}</div>

              {/* Hover indicator */}
              {hovered === i && (
                <div style={{ position: "absolute", bottom: 16, right: 16, fontFamily: "var(--font-hud)", fontSize: 8, color: f.color, letterSpacing: "0.15em" }}>
                  EXPLORE →
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* ── DESIGN PILLARS ── */}
      <section style={{ padding: "100px 60px" }}>
        <div style={{ textAlign: "center", marginBottom: 60 }}>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--purple)", letterSpacing: "0.4em", marginBottom: 16 }}>— TECHNICAL BACKBONE —</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 36, fontWeight: 900, color: "var(--text-primary)", letterSpacing: "0.05em" }}>BUILT FOR POWER USERS</div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24, maxWidth: 1100, margin: "0 auto" }}>
          {[
            {
              title: "GLASSMORPHIC HUD", color: "#00cfff", icon: "◈",
              items: ["backdrop-filter: blur(40px)", "High saturation overlays", "Holographic floating panes", "Military-grade visual language"],
            },
            {
              title: "MULTI-MODEL CORE", color: "#ff0080", icon: "⎊",
              items: ["Groq / Mixtral integration", "OpenAI GPT-4o endpoint", "Meta Llama 3.1 pipeline", "Anthropic Claude gateway"],
            },
            {
              title: "FORENSIC PERSISTENCE", color: "#00e5a0", icon: "⬢",
              items: ["SurrealDB audit trail", "Cryptographic timestamps", "Immutable session records", "PDF evidence export"],
            },
          ].map(({ title, color, icon, items }) => (
            <div key={title} className="glass-pane" style={{ padding: 32, position: "relative" }}>
              <CornerBrackets />
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 28, color, marginBottom: 12, textShadow: `0 0 20px ${color}` }}>{icon}</div>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 10, color, letterSpacing: "0.2em", marginBottom: 20 }}>{title}</div>
              {items.map(item => (
                <div key={item} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                  <div style={{ width: 4, height: 4, borderRadius: "50%", background: color, flexShrink: 0, boxShadow: `0 0 6px ${color}` }} />
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)" }}>{item}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA SECTION ── */}
      <section style={{
        padding: "100px 60px", textAlign: "center", position: "relative",
        background: "linear-gradient(180deg, transparent, rgba(255,0,128,0.03), transparent)",
        borderTop: "1px solid rgba(255,0,128,0.08)", borderBottom: "1px solid rgba(255,0,128,0.08)",
      }}>
        <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%,-50%)", width: 600, height: 300, borderRadius: "50%", background: "radial-gradient(ellipse, rgba(255,0,128,0.06) 0%, transparent 70%)", pointerEvents: "none" }} />

        <div style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: "var(--pink)", letterSpacing: "0.4em", marginBottom: 20 }}>
          — BEGIN YOUR AUDIT —
        </div>
        <div style={{ fontFamily: "var(--font-hud)", fontSize: "clamp(32px, 4vw, 56px)", fontWeight: 900, color: "var(--text-primary)", letterSpacing: "0.05em", marginBottom: 20, lineHeight: 1.1 }}>
          READY TO INTERROGATE<br />
          <span style={{ color: "var(--pink)", textShadow: "0 0 30px rgba(255,0,128,0.5)" }}>YOUR AI?</span>
        </div>
        <p style={{ fontFamily: "var(--font-body)", fontSize: 16, color: "var(--text-dim)", maxWidth: 500, margin: "0 auto 48px", lineHeight: 1.7 }}>
          Join researchers and developers using Aletheia Gate to verify, audit, and trust the AI outputs that matter.
        </p>

        <div style={{ display: "flex", gap: 16, justifyContent: "center", alignItems: "center" }}>
          <button className="btn-primary" onClick={() => setPage("signup")} style={{ fontSize: 11, padding: "16px 48px" }}>
            ⬡ CREATE CLEARANCE — FREE
          </button>
          <button onClick={() => setPage("login")} style={{
            fontFamily: "var(--font-hud)", fontSize: 9, letterSpacing: "0.2em",
            background: "transparent", border: "1px solid rgba(0,207,255,0.25)",
            color: "var(--text-dim)", padding: "16px 36px", cursor: "pointer", borderRadius: 2, transition: "all 0.3s",
          }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = "var(--cyan)"; e.currentTarget.style.color = "var(--cyan)"; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(0,207,255,0.25)"; e.currentTarget.style.color = "var(--text-dim)"; }}>
            RETURNING OPERATOR
          </button>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={{
        padding: "40px 60px",
        borderTop: "1px solid rgba(255,0,128,0.08)",
        display: "flex", justifyContent: "space-between", alignItems: "center",
        background: "rgba(3,5,13,0.8)",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <img
            src="/mnt/user-data/uploads/1773302659738_logo.png"
            alt="Aletheia Gate"
            style={{ width: 32, height: 32, borderRadius: "50%", objectFit: "cover", boxShadow: "0 0 12px rgba(255,0,128,0.5)" }}
          />
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 11, color: "var(--pink)", fontWeight: 700, letterSpacing: "0.15em" }}>ALETHEIA GATE</div>
          <div style={{ width: 1, height: 14, background: "rgba(0,207,255,0.25)" }} />
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)" }}>VERITAS SINE FINE</div>
        </div>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", display: "flex", gap: 20 }}>
          {["PRIVACY", "TERMS", "RESEARCH", "API"].map(link => (
            <span key={link} style={{ cursor: "pointer", transition: "color 0.2s" }}
              onMouseEnter={e => e.target.style.color = "var(--cyan)"}
              onMouseLeave={e => e.target.style.color = "var(--text-dim)"}>
              {link}
            </span>
          ))}
        </div>
        <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--text-dim)", letterSpacing: "0.15em", display: "flex", alignItems: "center", gap: 8 }}>
          <div className="status-dot" style={{ background: "var(--green)", boxShadow: "0 0 6px var(--green)" }} />
          ALL SYSTEMS NOMINAL
        </div>
      </footer>
    </div>
  );
}

// ── AUTH PAGES ────────────────────────────────────────────────────────────────
function SignupPage({ setPage }) {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [scanning, setScanning] = useState(false);
  const [field, setField] = useState(null);

  const handleSubmit = () => {
    setScanning(true);
    setTimeout(() => { setScanning(false); setPage("dashboard"); }, 2000);
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 40 }}>
      <div style={{ width: "100%", maxWidth: 460 }}>
        <div className="glass-pane" style={{ padding: 48, position: "relative", overflow: "hidden" }}>
          <CornerBrackets />
          <div className="scan-line" />

          <div className="hud-label" style={{ marginBottom: 6, color: "var(--pink)" }}>PHASE 1 // IDENTITY CREATION PROTOCOL</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 22, color: "var(--cyan)", marginBottom: 6, fontWeight: 700 }}>CREATE CLEARANCE</div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)", marginBottom: 36 }}>Biometric verification active — session will be initialized upon clearance.</div>

          {[
            { key: "username", label: "OPERATOR ID", placeholder: "Enter callsign...", type: "text" },
            { key: "email", label: "SECURE CHANNEL", placeholder: "Email endpoint...", type: "email" },
            { key: "password", label: "ENCRYPTION KEY", placeholder: "Min 16 chars recommended...", type: "password" },
          ].map(({ key, label, placeholder, type }) => (
            <div key={key} style={{ marginBottom: 24 }}>
              <div className="hud-label" style={{ marginBottom: 8 }}>{label}</div>
              <input
                className="input-field"
                type={type}
                placeholder={placeholder}
                value={form[key]}
                onFocus={() => setField(key)}
                onBlur={() => setField(null)}
                onChange={e => setForm({ ...form, [key]: e.target.value })}
                style={{ borderColor: field === key ? "var(--pink)" : "rgba(255,0,128,0.15)" }}
              />
              {field === key && (
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--green)", marginTop: 4, letterSpacing: "0.15em" }}>
                  ◉ INPUT STREAM ENCRYPTED
                </div>
              )}
            </div>
          ))}

          <div style={{ background: "rgba(255,0,128,0.05)", border: "1px solid rgba(255,0,128,0.2)", borderRadius: 4, padding: "12px 16px", marginBottom: 28 }}>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.15em", marginBottom: 6 }}>TERMS OF DISCLOSURE</div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", lineHeight: 1.6 }}>
              All AI outputs processed by Aletheia Gate are forensic in nature. Integrity scores are probabilistic assessments. No guarantee of absolute truth is implied. All interrogation sessions are logged to the Vault for research accountability.
            </div>
          </div>

          <button className="btn-primary" onClick={handleSubmit} style={{ width: "100%", textAlign: "center", justifyContent: "center" }}>
            {scanning ? (
              <span style={{ display: "flex", alignItems: "center", gap: 8, justifyContent: "center" }}>
                <span style={{ animation: "rotate 1s linear infinite", display: "inline-block" }}>◈</span>
                SCANNING IDENTITY...
              </span>
            ) : "⬡ INITIALIZE CLEARANCE"}
          </button>

          <div style={{ textAlign: "center", marginTop: 20, fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)" }}>
            Existing operator? <span onClick={() => setPage("login")} style={{ color: "var(--pink)", cursor: "pointer" }}>ACCESS HUB →</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function LoginPage({ setPage }) {
  const [decrypting, setDecrypting] = useState(false);

  const handleLogin = () => {
    setDecrypting(true);
    setTimeout(() => { setDecrypting(false); setPage("dashboard"); }, 2200);
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 40 }}>
      {/* Dim overlay */}
      <div style={{ position: "fixed", inset: 0, background: "radial-gradient(ellipse at center, transparent 30%, rgba(2,4,10,0.8) 100%)", zIndex: 1, pointerEvents: "none" }} />

      <div style={{ width: "100%", maxWidth: 420, position: "relative", zIndex: 2 }}>
        <div className="glass-pane" style={{ padding: 52, position: "relative", overflow: "hidden", boxShadow: "0 0 60px rgba(255,0,128,0.08), 0 0 120px rgba(0,207,255,0.04)" }}>
          <CornerBrackets />
          {!decrypting && <div className="scan-line" />}

          {/* Logo center */}
          <div style={{ textAlign: "center", marginBottom: 32 }}>
            <img src="/mnt/user-data/uploads/1773302659738_logo.png" alt="Aletheia Gate"
              style={{ width: 72, height: 72, borderRadius: "50%", objectFit: "cover", boxShadow: "0 0 30px rgba(255,0,128,0.5), 0 0 60px rgba(0,207,255,0.2)" }} className="flicker" />
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.25em", marginTop: 12 }}>PHASE 1 // SECURE HANDSHAKE</div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--text-dim)", letterSpacing: "0.15em", marginTop: 4 }}>SESSION INITIALIZATION PROTOCOL</div>
          </div>

          {decrypting ? (
            <div style={{ textAlign: "center", padding: "40px 0" }}>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 14, color: "var(--pink)", animation: "pulse 0.6s ease-in-out infinite", marginBottom: 12 }}>DECRYPTING...</div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", marginBottom: 4 }}>Verifying operator credentials against secure vault...</div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)", marginBottom: 20 }}>Initializing SurrealDB forensic session...</div>
              <div style={{ height: 2, background: "rgba(255,0,128,0.1)", borderRadius: 2, overflow: "hidden" }}>
                <div style={{ height: "100%", animation: "dataStream 1s linear infinite", backgroundSize: "200% 100%", backgroundImage: "linear-gradient(90deg, transparent, var(--pink), var(--cyan), transparent)", width: "100%" }} />
              </div>
            </div>
          ) : (
            <>
              {["OPERATOR ID", "ENCRYPTION KEY"].map((label, i) => (
                <div key={label} style={{ marginBottom: 20 }}>
                  <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--cyan)", letterSpacing: "0.15em", marginBottom: 8 }}>{label}</div>
                  <input className="input-field" type={i === 1 ? "password" : "text"} placeholder={i === 0 ? "Enter callsign..." : "Enter encryption key..."} />
                </div>
              ))}
              <button className="btn-primary" onClick={handleLogin} style={{ width: "100%", textAlign: "center", justifyContent: "center", marginTop: 8 }}>
                ◈ INITIATE HANDSHAKE
              </button>
            </>
          )}

          <div style={{ textAlign: "center", marginTop: 20, fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)" }}>
            New operator? <span onClick={() => setPage("signup")} style={{ color: "var(--pink)", cursor: "pointer" }}>CREATE CLEARANCE →</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── DASHBOARD ─────────────────────────────────────────────────────────────────
function Dashboard({ setPage }) {
  const [tick, setTick] = useState(0);
  const [scores] = useState([87, 72, 91]);
  const [activePhase, setActivePhase] = useState(3);

  useEffect(() => {
    const t = setInterval(() => setTick(n => n + 1), 1000);
    return () => clearInterval(t);
  }, []);

  const phases = [
    { id: 1, label: "GATE", sub: "Auth & Session", icon: "⬡", done: true },
    { id: 2, label: "INTERROGATION", sub: "Query Routing", icon: "⟁", done: true },
    { id: 3, label: "RADAR AUDIT", sub: "Forensic Scan", icon: "◎", done: false, active: true },
    { id: 4, label: "INDEX", sub: "Model Ranking", icon: "⬢", done: false },
    { id: 5, label: "VAULT", sub: "Persistence", icon: "⬢", done: false },
  ];

  return (
    <div style={{ padding: "36px 40px", animation: "slideInLeft 0.5s ease forwards" }}>

      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28 }}>
        <div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--pink)", letterSpacing: "0.35em", marginBottom: 6 }}>PHASE 3 // FORENSIC AUDIT ENGINE</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 26, fontWeight: 900, color: "var(--text-primary)", letterSpacing: "0.05em" }}>THE HUB</div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", marginTop: 4 }}>Air Traffic Control for AI Truth — real-time multi-model monitoring</div>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          {[
            { label: "GROQ", color: "#00e5a0" },
            { label: "OPENAI", color: "#00cfff" },
            { label: "LLAMA", color: "#ff0080" },
            { label: "SURREAL DB", color: "#bf5fff" },
          ].map(s => (
            <div key={s.label} className="glass-pane" style={{ padding: "6px 12px", display: "flex", alignItems: "center", gap: 6, borderColor: `${s.color}33` }}>
              <div className="status-dot" style={{ background: s.color, boxShadow: `0 0 6px ${s.color}` }} />
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: s.color, letterSpacing: "0.1em" }}>{s.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Pipeline Progress Bar */}
      <div className="glass-pane" style={{ padding: "16px 24px", marginBottom: 28, borderColor: "rgba(255,0,128,0.2)" }}>
        <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.2em", marginBottom: 14 }}>TRUTH FILTER PIPELINE // ACTIVE</div>
        <div style={{ display: "flex", alignItems: "center", gap: 0 }}>
          {phases.map((p, i) => (
            <div key={p.id} style={{ display: "flex", alignItems: "center", flex: 1 }}>
              <div
                onClick={() => setActivePhase(p.id)}
                style={{
                  display: "flex", flexDirection: "column", alignItems: "center", gap: 6, cursor: "pointer",
                  padding: "8px 12px", borderRadius: 6, flex: 1,
                  background: p.active ? "rgba(255,0,128,0.1)" : p.done ? "rgba(0,229,160,0.05)" : "transparent",
                  border: p.active ? "1px solid rgba(255,0,128,0.35)" : "1px solid transparent",
                  transition: "all 0.3s",
                }}>
                <div style={{
                  width: 32, height: 32, borderRadius: "50%",
                  background: p.active ? "rgba(255,0,128,0.2)" : p.done ? "rgba(0,229,160,0.15)" : "rgba(255,255,255,0.05)",
                  border: `2px solid ${p.active ? "#ff0080" : p.done ? "#00e5a0" : "rgba(255,255,255,0.1)"}`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontFamily: "var(--font-hud)", fontSize: 12,
                  color: p.active ? "#ff0080" : p.done ? "#00e5a0" : "var(--text-dim)",
                  boxShadow: p.active ? "0 0 16px rgba(255,0,128,0.5)" : p.done ? "0 0 8px rgba(0,229,160,0.3)" : "none",
                  animation: p.active ? "pulse 1.5s ease-in-out infinite" : "none",
                }}>
                  {p.done && !p.active ? "✓" : p.id}
                </div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: p.active ? "var(--pink)" : p.done ? "var(--green)" : "var(--text-dim)", letterSpacing: "0.1em", textAlign: "center" }}>{p.label}</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 7, color: "var(--text-dim)", textAlign: "center" }}>{p.sub}</div>
              </div>
              {i < phases.length - 1 && (
                <div style={{ width: 24, height: 2, background: i < 2 ? "linear-gradient(90deg, #00e5a0, #ff0080)" : "rgba(255,255,255,0.08)", margin: "0 4px", flexShrink: 0, borderRadius: 1 }} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Active Query Display */}
      <div className="glass-pane" style={{ padding: "12px 20px", marginBottom: 24, borderColor: "rgba(0,207,255,0.2)", display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--cyan)", letterSpacing: "0.2em", flexShrink: 0, display: "flex", alignItems: "center", gap: 8 }}>
          <div className="status-dot" style={{ background: "var(--pink)", boxShadow: "0 0 8px var(--pink)" }} />
          AUDITING
        </div>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)", flex: 1, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis" }}>
          "Analyze the long-term side effects of metformin on patients with type-2 diabetes"
        </div>
        <div style={{ display: "flex", gap: 16, flexShrink: 0 }}>
          {["GPT-4o", "LLAMA", "GROQ"].map((m, i) => (
            <div key={m} style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: ["#00cfff", "#ff0080", "#00e5a0"][i], letterSpacing: "0.1em", display: "flex", alignItems: "center", gap: 5 }}>
              <div style={{ width: 4, height: 4, borderRadius: "50%", background: ["#00cfff", "#ff0080", "#00e5a0"][i], animation: "pulse 1s ease-in-out infinite" }} />
              {m}::STREAMING
            </div>
          ))}
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: 24, alignItems: "start" }}>

        {/* Radar */}
        <div className="glass-pane" style={{ padding: 24, position: "relative" }}>
          <CornerBrackets />
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.2em", marginBottom: 4 }}>PHASE 3 // FORENSIC SCAN</div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: "var(--text-primary)", marginBottom: 16, letterSpacing: "0.1em" }}>HALLUCINATION RADAR</div>
          <HallucinationRadar size={244} scores={scores} />
          {/* Legend */}
          <div style={{ marginTop: 18, display: "flex", flexDirection: "column", gap: 10 }}>
            {[
              { c: "#ff0080", label: "GPT-4o", val: scores[0], arc: "OUTER ARC" },
              { c: "#00cfff", label: "Groq-Mixtral", val: scores[2], arc: "MID ARC" },
              { c: "#00e5a0", label: "Llama-3.1", val: scores[1], arc: "INNER ARC" },
            ].map(({ c, label, val, arc }) => (
              <div key={label} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ width: 10, height: 10, borderRadius: "50%", background: c, boxShadow: `0 0 8px ${c}`, flexShrink: 0 }} />
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)", flex: 1 }}>{label}</span>
                <span style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "rgba(255,255,255,0.2)", marginRight: 6 }}>{arc}</span>
                <span style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: c, fontWeight: 700 }}>{val}%</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 16, padding: "10px 14px", background: "rgba(255,0,128,0.06)", borderRadius: 4, border: "1px solid rgba(255,0,128,0.15)" }}>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--pink)", letterSpacing: "0.15em", marginBottom: 4 }}>SWEEP = ACTIVE AUDIT</div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)", lineHeight: 1.5 }}>Rotating laser indicates live cross-referencing. Arc thickness = evidence strength.</div>
          </div>
        </div>

        {/* Right column */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>

          {/* Integrity Index */}
          <div className="glass-pane" style={{ padding: 24 }}>
            <CornerBrackets />
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--cyan)", letterSpacing: "0.2em", marginBottom: 4 }}>PHASE 4 // MODEL RANKING</div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: "var(--text-primary)", marginBottom: 18, letterSpacing: "0.1em" }}>INTEGRITY INDEX</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
              {MODELS.map(m => (
                <div key={m.id} style={{
                  background: `${m.color}08`,
                  border: `1px solid ${m.color}28`,
                  borderRadius: 6, padding: 16, position: "relative",
                  transition: "all 0.3s",
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
                    <span style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--text-primary)", letterSpacing: "0.05em" }}>{m.name}</span>
                    <span style={{
                      fontFamily: "var(--font-hud)", fontSize: 7,
                      color: m.color, background: `${m.color}18`,
                      padding: "3px 8px", borderRadius: 2, letterSpacing: "0.1em",
                    }}>{m.status}</span>
                  </div>
                  <div style={{ fontFamily: "var(--font-hud)", fontSize: 30, color: m.color, fontWeight: 900, textShadow: `0 0 20px ${m.color}`, lineHeight: 1 }}>{m.score}</div>
                  <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", letterSpacing: "0.1em", margin: "6px 0 8px" }}>TRUTH CONFIDENCE</div>
                  <div className="integrity-bar" style={{ background: `${m.color}18` }}>
                    <div className="integrity-bar-fill" style={{ width: `${m.score}%`, background: `linear-gradient(90deg, ${m.color}66, ${m.color})` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Stats + CTA row */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr) auto", gap: 14, alignItems: "stretch" }}>
            {[
              { label: "AUDITS TODAY", val: "247", icon: "⬢", c: "var(--cyan)" },
              { label: "AVG TRUTH SCORE", val: "84.2%", icon: "◎", c: "var(--green)" },
              { label: "HIGH RISK FLAGS", val: "12", icon: "⚠", c: "var(--amber)" },
            ].map(s => (
              <div key={s.label} className="glass-pane" style={{ padding: 18, textAlign: "center" }}>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 18, color: s.c, marginBottom: 6 }}>{s.icon}</div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 24, color: s.c, fontWeight: 900, textShadow: `0 0 15px ${s.c}` }}>{s.val}</div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", letterSpacing: "0.1em", marginTop: 4 }}>{s.label}</div>
              </div>
            ))}
            <button onClick={() => setPage("chat")} className="btn-primary" style={{ fontSize: 9, padding: "0 20px", animation: "glowPink 2.5s ease-in-out infinite" }}>
              ⟁ BEGIN<br />INTERROGATION
            </button>
          </div>

          {/* Phase 5 Vault preview */}
          <div className="glass-pane" style={{ padding: 20, borderColor: "rgba(191,95,255,0.2)" }}>
            <CornerBrackets />
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
              <div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--purple)", letterSpacing: "0.2em", marginBottom: 2 }}>PHASE 5 // PERSISTENCE</div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: "var(--text-primary)", letterSpacing: "0.1em" }}>RECENT VAULT ENTRIES</div>
              </div>
              <button onClick={() => setPage("archive")} style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--purple)", background: "rgba(191,95,255,0.08)", border: "1px solid rgba(191,95,255,0.25)", padding: "5px 14px", borderRadius: 2, cursor: "pointer", letterSpacing: "0.1em" }}>
                OPEN VAULT →
              </button>
            </div>
            {ARCHIVE_ENTRIES.slice(0, 3).map(e => {
              const rc = e.risk === "LOW" ? "var(--green)" : e.risk === "MED" ? "var(--amber)" : "var(--red)";
              return (
                <div key={e.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 0", borderBottom: "1px solid rgba(255,0,128,0.06)" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--pink)", flexShrink: 0, width: 80 }}>{e.id}</span>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{e.query}</span>
                  <span style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: e.score > 80 ? "var(--green)" : e.score > 60 ? "var(--amber)" : "var(--red)", flexShrink: 0 }}>{e.score}%</span>
                  <span style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: rc, background: `${rc}18`, padding: "2px 7px", borderRadius: 2, flexShrink: 0 }}>{e.risk}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── CHAT PAGE ─────────────────────────────────────────────────────────────────
function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "system", text: "PHASE 2 — INTERROGATION PROTOCOL ACTIVE. Query will be routed to all connected model endpoints. Forensic radar monitoring enabled." },
    { role: "assistant", text: "Operator clearance verified. Submit your query and it will be distributed across GPT-4o, Llama-3.1, and Groq-Mixtral simultaneously. Each response passes through the hallucination radar. Truth scores and model divergence flags appear alongside every answer." },
  ]);
  const [input, setInput] = useState("");
  const [meterVal, setMeterVal] = useState(88);
  const [analyzing, setAnalyzing] = useState(false);
  const [selectedModel, setSelectedModel] = useState("all");
  const endRef = useRef(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(m => [...m, { role: "user", text: userMsg }]);
    setAnalyzing(true);
    setMeterVal(Math.floor(Math.random() * 30) + 30);

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: `You are the Aletheia Gate forensic truth engine — a specialized AI auditing assistant that is part of a multi-model truth verification pipeline. 
The user's query is being simultaneously analyzed by GPT-4o, Llama-3.1, and Groq-Mixtral as part of the forensic pipeline.
Answer questions with precise, factual accuracy. Structure your response clearly.
At the end, ALWAYS append exactly this block:
---FORENSIC_AUDIT---
TRUTH_ANALYSIS: [1-sentence confidence assessment]
HALLUCINATION_RISK: [LOW / MEDIUM / HIGH]
EVIDENCE_STRENGTH: [STRONG / MODERATE / WEAK]
CROSS_REF_NOTES: [Brief note on verifiability]`,
          messages: [{ role: "user", content: userMsg }],
        }),
      });
      const data = await response.json();
      const text = data.content?.map(b => b.text || "").join("") || "Signal lost. Re-transmit query.";
      const score = Math.floor(Math.random() * 20) + 75;
      setMeterVal(score);
      setMessages(m => [...m, { role: "assistant", text, score }]);
    } catch {
      setMessages(m => [...m, { role: "assistant", text: "CONNECTION INTERRUPTED. Endpoint unreachable.", score: 0 }]);
    }
    setAnalyzing(false);
  };

  const meterColor = meterVal > 80 ? "var(--green)" : meterVal > 60 ? "var(--amber)" : "var(--red)";

  const renderMessage = (text) => {
    if (!text.includes("---FORENSIC_AUDIT---")) {
      return <span style={{ whiteSpace: "pre-wrap" }}>{text}</span>;
    }
    const [body, audit] = text.split("---FORENSIC_AUDIT---");
    const lines = audit.trim().split("\n");
    return (
      <>
        <span style={{ whiteSpace: "pre-wrap" }}>{body.trim()}</span>
        <div style={{ marginTop: 14, padding: "12px 14px", background: "rgba(255,0,128,0.06)", border: "1px solid rgba(255,0,128,0.2)", borderRadius: 4 }}>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.2em", marginBottom: 10 }}>◈ FORENSIC AUDIT RESULTS</div>
          {lines.map((line, i) => {
            const [key, ...val] = line.split(":");
            const value = val.join(":").trim();
            const isRisk = value === "HIGH" || value === "MEDIUM";
            const isGood = value === "LOW" || value === "STRONG";
            const valColor = isRisk ? "var(--red)" : isGood ? "var(--green)" : "var(--cyan)";
            return key && value ? (
              <div key={i} style={{ display: "flex", gap: 10, marginBottom: 6, alignItems: "baseline" }}>
                <span style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", letterSpacing: "0.1em", width: 140, flexShrink: 0 }}>{key.trim()}</span>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: valColor }}>{value}</span>
              </div>
            ) : null;
          })}
        </div>
      </>
    );
  };

  return (
    <div style={{ height: "100vh", display: "flex", gap: 0, overflow: "hidden" }}>
      {/* Chat area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", padding: "32px 32px 0" }}>
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20 }}>
          <div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.3em", marginBottom: 4 }}>PHASE 2 // MULTI-MODEL ROUTING</div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 20, fontWeight: 900, color: "var(--text-primary)", letterSpacing: "0.05em" }}>THE INTERROGATION</div>
          </div>
          {/* Model selector */}
          <div style={{ display: "flex", gap: 6 }}>
            {[
              { id: "all", label: "ALL MODELS", c: "var(--pink)" },
              { id: "gpt4", label: "GPT-4o", c: "#00cfff" },
              { id: "llama", label: "LLAMA", c: "#ff0080" },
              { id: "groq", label: "GROQ", c: "#00e5a0" },
            ].map(m => (
              <div key={m.id} onClick={() => setSelectedModel(m.id)} style={{
                fontFamily: "var(--font-hud)", fontSize: 7, letterSpacing: "0.1em",
                color: selectedModel === m.id ? "#fff" : "var(--text-dim)",
                padding: "5px 12px", borderRadius: 2, cursor: "pointer",
                background: selectedModel === m.id ? `${m.c}22` : "transparent",
                border: `1px solid ${selectedModel === m.id ? m.c : "rgba(255,255,255,0.08)"}`,
                transition: "all 0.2s",
              }}>{m.label}</div>
            ))}
          </div>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: 14, paddingRight: 6, paddingBottom: 20 }}>
          {messages.map((msg, i) => (
            <div key={i} className="chat-bubble" style={{ alignSelf: msg.role === "user" ? "flex-end" : "flex-start", maxWidth: "82%" }}>
              {msg.role === "system" ? (
                <div style={{
                  fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--pink)", letterSpacing: "0.08em",
                  padding: "8px 14px", border: "1px solid rgba(255,0,128,0.2)", borderRadius: 4,
                  background: "rgba(255,0,128,0.05)", lineHeight: 1.5,
                }}>
                  ◈ SYSTEM — {msg.text}
                </div>
              ) : (
                <div className="glass-pane" style={{
                  padding: "14px 18px",
                  borderColor: msg.role === "user" ? "rgba(0,207,255,0.25)" : "rgba(255,0,128,0.18)",
                  borderRadius: msg.role === "user" ? "8px 8px 0 8px" : "8px 8px 8px 0",
                  animation: "none",
                }}>
                  {msg.role === "assistant" && (
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
                      <div className="status-dot" style={{ background: "var(--pink)", boxShadow: "0 0 6px var(--pink)" }} />
                      <span style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.15em" }}>ALETHEIA ENGINE // CLAUDE-3.5</span>
                      {msg.score && (
                        <span style={{
                          fontFamily: "var(--font-hud)", fontSize: 7,
                          color: msg.score > 80 ? "var(--green)" : msg.score > 60 ? "var(--amber)" : "var(--red)",
                          background: msg.score > 80 ? "rgba(0,229,160,0.12)" : "rgba(255,170,0,0.12)",
                          padding: "2px 8px", borderRadius: 2, letterSpacing: "0.1em", marginLeft: "auto",
                        }}>
                          TRUTH SCORE: {msg.score}%
                        </span>
                      )}
                    </div>
                  )}
                  {msg.role === "user" && (
                    <div style={{ display: "flex", gap: 8, marginBottom: 8, alignItems: "center" }}>
                      <div className="status-dot" style={{ background: "var(--cyan)", boxShadow: "0 0 6px var(--cyan)" }} />
                      <span style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--cyan)", letterSpacing: "0.15em" }}>OPERATOR QUERY // ROUTED TO {selectedModel === "all" ? "3 MODELS" : selectedModel.toUpperCase()}</span>
                    </div>
                  )}
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-primary)", lineHeight: 1.75 }}>
                    {msg.role === "assistant" ? renderMessage(msg.text) : msg.text}
                  </div>
                </div>
              )}
            </div>
          ))}
          {analyzing && (
            <div style={{ alignSelf: "flex-start" }}>
              <div className="glass-pane" style={{ padding: "12px 18px", display: "flex", gap: 12, alignItems: "center", animation: "none", borderColor: "rgba(255,0,128,0.2)" }}>
                <div style={{ animation: "rotate 0.8s linear infinite", color: "var(--pink)", fontSize: 16 }}>◈</div>
                <div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--pink)", marginBottom: 2 }}>Routing query to all endpoints...</div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)" }}>Cross-referencing · Scoring · Auditing</div>
                </div>
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Input */}
        <div style={{ padding: "16px 0", borderTop: "1px solid rgba(255,0,128,0.1)" }}>
          <div className="glass-pane" style={{ display: "flex", gap: 0, overflow: "hidden", padding: 0, animation: "none" }}>
            <input
              style={{
                flex: 1, background: "transparent", border: "none",
                padding: "14px 18px", fontFamily: "var(--font-mono)", fontSize: 13,
                color: "var(--text-primary)", outline: "none",
              }}
              placeholder="Enter query for multi-model forensic analysis..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && sendMessage()}
            />
            <button onClick={sendMessage} style={{
              background: "rgba(255,0,128,0.12)", border: "none",
              borderLeft: "1px solid rgba(255,0,128,0.2)",
              color: "var(--pink)", padding: "14px 22px", cursor: "pointer",
              fontFamily: "var(--font-hud)", fontSize: 8, letterSpacing: "0.15em",
              transition: "all 0.2s",
            }}
              onMouseEnter={e => e.currentTarget.style.background = "rgba(255,0,128,0.22)"}
              onMouseLeave={e => e.currentTarget.style.background = "rgba(255,0,128,0.12)"}>
              TRANSMIT ⟁
            </button>
          </div>
        </div>
      </div>

      {/* Side HUD */}
      <div style={{ width: 210, borderLeft: "1px solid rgba(255,0,128,0.1)", padding: "32px 18px", display: "flex", flexDirection: "column", gap: 20, background: "rgba(3,5,13,0.5)" }}>
        <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.2em" }}>PHASE 3 // SIDE-SCAN HUD</div>

        {/* Mini radar */}
        <div className="glass-pane" style={{ padding: 16, textAlign: "center", animation: "none" }}>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", letterSpacing: "0.1em", marginBottom: 10 }}>HALLUCINATION METER</div>
          <HallucinationRadar size={150} scores={[meterVal, meterVal - 15, meterVal + 5]} />
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 22, color: meterColor, fontWeight: 900, marginTop: 10, textShadow: `0 0 15px ${meterColor}` }}>
            {meterVal}%
          </div>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: meterColor, letterSpacing: "0.1em", marginTop: 2 }}>
            {meterVal > 80 ? "◉ SECURE" : meterVal > 60 ? "◎ REVIEW" : "⚠ RISK"}
          </div>
        </div>

        {/* Multi-model stream status */}
        <div className="glass-pane" style={{ padding: 14, animation: "none" }}>
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", letterSpacing: "0.12em", marginBottom: 12 }}>MODEL STREAM STATUS</div>
          {[
            { name: "GPT-4o", c: "#00cfff", lat: "142ms" },
            { name: "Llama-3.1", c: "#ff0080", lat: "198ms" },
            { name: "Groq-Mixtral", c: "#00e5a0", lat: "89ms" },
          ].map(m => (
            <div key={m.name} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
              <div className="status-dot" style={{ background: m.c, boxShadow: `0 0 5px ${m.c}`, flexShrink: 0 }} />
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)", flex: 1 }}>{m.name}</span>
              <span style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: m.c }}>{m.lat}</span>
            </div>
          ))}
        </div>

        {/* Session stats */}
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {[
            { label: "SESSION QUERIES", val: messages.filter(m => m.role === "user").length },
            { label: "AVG TRUTH SCORE", val: `${Math.floor(messages.filter(m => m.score).reduce((s, m) => s + m.score, 0) / Math.max(messages.filter(m => m.score).length, 1))}%` },
            { label: "RISK FLAGS", val: messages.filter(m => m.score && m.score < 70).length },
          ].map(({ label, val }) => (
            <div key={label} className="glass-pane" style={{ padding: "10px 12px", animation: "none" }}>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", letterSpacing: "0.1em", marginBottom: 4 }}>{label}</div>
              <div style={{ fontFamily: "var(--font-hud)", fontSize: 18, color: "var(--cyan)", fontWeight: 700 }}>{val}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── ANALYSIS / LAB ────────────────────────────────────────────────────────────
function AnalysisPage() {
  const [selectedModels, setSelectedModels] = useState(["gpt4", "claude"]);
  const weeks = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"];
  const driftData = {
    gpt4: [81, 83, 79, 85, 87, 84, 88, 87],
    llama: [68, 70, 65, 72, 71, 69, 74, 72],
    groq: [88, 89, 91, 90, 92, 91, 93, 91],
    claude: [90, 92, 91, 93, 94, 93, 95, 94],
  };
  const maxH = 120;

  return (
    <div style={{ padding: "40px", animation: "slideInLeft 0.5s ease" }}>
      <div style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--pink)", letterSpacing: "0.3em", marginBottom: 6 }}>FORENSIC ANALYTICS // DEEP ANALYSIS SUITE</div>
      <div style={{ fontFamily: "var(--font-hud)", fontSize: 24, fontWeight: 700, marginBottom: 4 }}>THE LAB</div>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", marginBottom: 32 }}>Historical pattern analysis — model drift, topic heatmaps, head-to-head comparisons</div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 24 }}>
        {/* Drift Chart */}
        <div className="glass-pane" style={{ padding: 28 }}>
          <CornerBrackets />
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--cyan)", letterSpacing: "0.18em", marginBottom: 4 }}>TEMPORAL DRIFT ANALYSIS</div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)", marginBottom: 14 }}>Truth score stability over time per model</div>
          <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
            {MODELS.map(m => (
              <div key={m.id} onClick={() => setSelectedModels(s => s.includes(m.id) ? s.filter(x => x !== m.id) : [...s, m.id])}
                style={{
                  fontFamily: "var(--font-hud)", fontSize: 8, padding: "4px 10px", borderRadius: 2, cursor: "pointer",
                  border: `1px solid ${m.color}`,
                  background: selectedModels.includes(m.id) ? `${m.color}22` : "transparent",
                  color: selectedModels.includes(m.id) ? m.color : "var(--text-dim)",
                  letterSpacing: "0.1em", transition: "all 0.2s",
                }}>{m.name}</div>
            ))}
          </div>
          {/* Chart */}
          <div style={{ height: maxH + 40, position: "relative", display: "flex", flexDirection: "column", justifyContent: "flex-end" }}>
            {[60, 70, 80, 90, 100].map(v => (
              <div key={v} style={{
                position: "absolute", left: 0, right: 0,
                bottom: ((v - 60) / 40) * maxH,
                borderTop: "1px dashed rgba(255,0,128,0.08)",
                display: "flex", alignItems: "flex-end"
              }}>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--text-dim)", marginBottom: 2, marginRight: 4 }}>{v}</span>
              </div>
            ))}
            {MODELS.filter(m => selectedModels.includes(m.id)).map(m => {
              const vals = driftData[m.id];
              return (
                <svg key={m.id} style={{ position: "absolute", inset: 0, width: "100%", height: maxH }} viewBox={`0 0 100 ${maxH}`} preserveAspectRatio="none">
                  <polyline
                    points={vals.map((v, i) => `${(i / (vals.length - 1)) * 100},${maxH - ((v - 60) / 40) * maxH}`).join(" ")}
                    fill="none" stroke={m.color} strokeWidth="1.5" strokeLinejoin="round"
                    style={{ filter: `drop-shadow(0 0 4px ${m.color})` }}
                  />
                  {vals.map((v, i) => (
                    <circle key={i} cx={(i / (vals.length - 1)) * 100} cy={maxH - ((v - 60) / 40) * maxH} r="2" fill={m.color} />
                  ))}
                </svg>
              );
            })}
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: maxH + 8 }}>
              {weeks.map(w => <span key={w} style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--text-dim)" }}>{w}</span>)}
            </div>
          </div>
        </div>

        {/* Model Comparison */}
        <div className="glass-pane" style={{ padding: 28 }}>
          <CornerBrackets />
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--pink)", letterSpacing: "0.18em", marginBottom: 4 }}>HEAD-TO-HEAD BATTLE</div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)", marginBottom: 18 }}>Same query — different model truth scores</div>
          {[
            { q: "Explain quantum superposition", scores: [87, 91] },
            { q: "Side effects of aspirin overdose", scores: [61, 88] },
            { q: "Current US inflation rate", scores: [34, 42] },
            { q: "How does TCP/IP work?", scores: [95, 93] },
          ].map(({ q, scores }) => (
            <div key={q} style={{ marginBottom: 18 }}>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", marginBottom: 8 }}>"{q}"</div>
              <div style={{ display: "flex", gap: 10 }}>
                {["GPT-4o", "Claude-3.5"].map((name, mi) => {
                  const s = scores[mi];
                  const c = s > 80 ? "var(--green)" : s > 60 ? "var(--amber)" : "var(--red)";
                  return (
                    <div key={name} style={{ flex: 1, background: `${c}0a`, border: `1px solid ${c}33`, borderRadius: 4, padding: "8px 12px" }}>
                      <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--text-dim)", marginBottom: 4 }}>{name}</div>
                      <div style={{ fontFamily: "var(--font-hud)", fontSize: 16, color: c, fontWeight: 700 }}>{s}%</div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Heatmap */}
      <div className="glass-pane" style={{ padding: 28 }}>
        <CornerBrackets />
        <div className="hud-label" style={{ marginBottom: 20 }}>HALLUCINATION HEATMAP BY TOPIC</div>
        <div style={{ display: "flex", gap: 2, alignItems: "center", marginBottom: 10 }}>
          <div style={{ width: 60 }} />
          {HEATMAP_TOPICS.map(t => (
            <div key={t} style={{ flex: 1, fontFamily: "var(--font-hud)", fontSize: 7, color: "var(--text-dim)", textAlign: "center", letterSpacing: "0.05em" }}>{t.slice(0, 4)}</div>
          ))}
        </div>
        {HEATMAP_DATA.map((row, ri) => (
          <div key={ri} style={{ display: "flex", gap: 2, marginBottom: 2, alignItems: "center" }}>
            <div style={{ width: 60, fontFamily: "var(--font-hud)", fontSize: 8, color: "var(--text-dim)", textAlign: "right", paddingRight: 10 }}>
              {["GPT-4o", "Llama", "Groq", "Claude"][ri]}
            </div>
            {row.map((val, ci) => {
              const intensity = val;
              const r = Math.floor(255 * intensity);
              const g = Math.floor(255 * (1 - intensity) * 0.5);
              return (
                <div key={ci} className="heatmap-cell" style={{
                  flex: 1, height: 32, borderRadius: 3,
                  background: `rgba(${r}, ${g}, 20, ${0.4 + intensity * 0.5})`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  animation: `heatPulse ${1.5 + val}s ease-in-out infinite`,
                }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "rgba(255,255,255,0.7)" }}>
                    {Math.round(val * 100)}
                  </span>
                </div>
              );
            })}
          </div>
        ))}
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 16 }}>
          <span className="hud-label" style={{ fontSize: 7 }}>RISK SCALE:</span>
          <div style={{ height: 6, width: 200, background: "linear-gradient(90deg, rgba(0,100,20,0.8), rgba(255,170,0,0.8), rgba(255,0,50,0.8))", borderRadius: 3 }} />
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--green)" }}>LOW</span>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--red)", marginLeft: "auto" }}>HIGH</span>
        </div>
      </div>
    </div>
  );
}

// ── ARCHIVE / VAULT ───────────────────────────────────────────────────────────
function ArchivePage() {
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const filtered = ARCHIVE_ENTRIES.filter(e =>
    e.query.toLowerCase().includes(search.toLowerCase()) || e.id.includes(search)
  );

  const riskColor = r => r === "LOW" ? "var(--green)" : r === "MED" ? "var(--amber)" : "var(--red)";

  return (
    <div style={{ padding: "40px", animation: "slideInLeft 0.5s ease" }}>
      <div style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--purple)", letterSpacing: "0.3em", marginBottom: 6 }}>PHASE 5 // IMMUTABLE AUDIT TRAIL</div>
      <div style={{ fontFamily: "var(--font-hud)", fontSize: 24, fontWeight: 700, marginBottom: 4 }}>THE VAULT</div>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", marginBottom: 32 }}>Every interrogation sealed here — timestamped, scored, retrievable for legal or research accountability</div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 360px", gap: 24, alignItems: "start" }}>
        <div className="glass-pane" style={{ padding: 28 }}>
          <CornerBrackets />
          <div style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 24 }}>
            <div style={{ flex: 1 }}>
              <input
                className="input-field"
                placeholder="Search audit logs by query or ID..."
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </div>
            <div className="hud-label">{filtered.length} RECORDS</div>
          </div>

          {/* Table */}
          <div style={{ fontFamily: "var(--font-hud)", fontSize: 8, display: "grid", gridTemplateColumns: "120px 1fr 80px 100px 80px", gap: 0, color: "var(--text-dim)", letterSpacing: "0.1em", borderBottom: "1px solid rgba(0,245,255,0.1)", paddingBottom: 10, marginBottom: 10 }}>
            <span>AUDIT ID</span><span>QUERY</span><span>SCORE</span><span>MODEL</span><span>RISK</span>
          </div>
          {filtered.map(e => (
            <div key={e.id} onClick={() => setSelected(e)} style={{
              display: "grid", gridTemplateColumns: "120px 1fr 80px 100px 80px",
              padding: "12px 8px", cursor: "pointer", borderRadius: 4,
              background: selected?.id === e.id ? "rgba(0,245,255,0.05)" : "transparent",
              borderLeft: selected?.id === e.id ? "2px solid var(--cyan)" : "2px solid transparent",
              transition: "all 0.2s",
              marginBottom: 2,
            }}
              onMouseEnter={el => el.currentTarget.style.background = "rgba(0,245,255,0.03)"}
              onMouseLeave={el => el.currentTarget.style.background = selected?.id === e.id ? "rgba(0,245,255,0.05)" : "transparent"}
            >
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--cyan)" }}>{e.id}</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-primary)", paddingRight: 16 }}>{e.query}</span>
              <span style={{ fontFamily: "var(--font-hud)", fontSize: 10, color: e.score > 80 ? "var(--green)" : e.score > 60 ? "var(--amber)" : "var(--red)" }}>{e.score}%</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)" }}>{e.model}</span>
              <span style={{ fontFamily: "var(--font-hud)", fontSize: 8, color: riskColor(e.risk), background: `${riskColor(e.risk)}18`, padding: "3px 8px", borderRadius: 2, textAlign: "center", alignSelf: "center" }}>{e.risk}</span>
            </div>
          ))}
        </div>

        {/* Detail panel */}
        {selected ? (
          <div className="glass-pane" style={{ padding: 28, position: "sticky", top: 40 }}>
            <CornerBrackets />
            <div className="hud-label" style={{ marginBottom: 16, color: "var(--cyan)" }}>AUDIT RECORD DETAIL</div>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 14, color: "var(--text-primary)", marginBottom: 20 }}>{selected.id}</div>
            {[
              { l: "QUERY", v: selected.query },
              { l: "TRUTH SCORE", v: `${selected.score}%` },
              { l: "MODEL", v: selected.model },
              { l: "RISK LEVEL", v: selected.risk },
              { l: "TIMESTAMP", v: selected.ts },
            ].map(({ l, v }) => (
              <div key={l} style={{ marginBottom: 14, paddingBottom: 14, borderBottom: "1px solid rgba(0,245,255,0.07)" }}>
                <div className="hud-label" style={{ marginBottom: 4, fontSize: 7 }}>{l}</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-primary)" }}>{v}</div>
              </div>
            ))}
            <button className="btn-primary" style={{ width: "100%", textAlign: "center", marginTop: 8, animation: "none" }}>
              ⬢ EXPORT PROOF-OF-TRUTH PDF
            </button>
          </div>
        ) : (
          <div className="glass-pane" style={{ padding: 28, textAlign: "center", color: "var(--text-dim)" }}>
            <div style={{ fontFamily: "var(--font-hud)", fontSize: 28, marginBottom: 12 }}>⬢</div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 11 }}>Select an audit record to view details and export</div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── SETTINGS ──────────────────────────────────────────────────────────────────
function SettingsPage() {
  const [sensitivity, setSensitivity] = useState(75);
  const [keys, setKeys] = useState({ openai: "", groq: "", anthropic: "" });
  const [toggles, setToggles] = useState({ temporal: true, semantic: true, factual: false, realtime: true });

  return (
    <div style={{ padding: "40px", animation: "slideInLeft 0.5s ease" }}>
      <div style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: "var(--pink)", letterSpacing: "0.3em", marginBottom: 6 }}>SYSTEM CONFIGURATION // ENGINE ROOM</div>
      <div style={{ fontFamily: "var(--font-hud)", fontSize: 24, fontWeight: 700, marginBottom: 4 }}>SETTINGS</div>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-dim)", marginBottom: 32 }}>Tune radar sensitivity, connect API endpoints, and manage analysis modules</div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        {/* Sensitivity */}
        <div className="glass-pane" style={{ padding: 28 }}>
          <CornerBrackets />
          <div className="hud-label" style={{ marginBottom: 20 }}>RADAR SENSITIVITY</div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)" }}>Detection Threshold</span>
              <span style={{ fontFamily: "var(--font-hud)", fontSize: 14, color: "var(--cyan)", fontWeight: 700 }}>{sensitivity}%</span>
            </div>
            <input type="range" min={0} max={100} value={sensitivity} onChange={e => setSensitivity(+e.target.value)}
              style={{ width: "100%", accentColor: "var(--pink)", cursor: "pointer" }} />
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 6 }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)" }}>PERMISSIVE</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-dim)" }}>STRICT</span>
            </div>
          </div>

          <div className="hud-label" style={{ marginBottom: 16, marginTop: 24 }}>ANALYSIS MODULES</div>
          {Object.entries(toggles).map(([key, val]) => (
            <div key={key} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)", textTransform: "uppercase" }}>{key.replace(/([A-Z])/g, " $1")} CHECK</span>
              <div onClick={() => setToggles(t => ({ ...t, [key]: !t[key] }))}
                style={{
                  width: 40, height: 20, borderRadius: 10, cursor: "pointer",
                  background: val ? "rgba(0,245,255,0.3)" : "rgba(255,255,255,0.1)",
                  border: `1px solid ${val ? "var(--cyan)" : "rgba(255,255,255,0.2)"}`,
                  position: "relative", transition: "all 0.3s",
                }}>
                <div style={{
                  position: "absolute", top: 2,
                  left: val ? 22 : 2,
                  width: 14, height: 14, borderRadius: "50%",
                  background: val ? "var(--cyan)" : "rgba(255,255,255,0.4)",
                  transition: "all 0.3s",
                  boxShadow: val ? "0 0 8px var(--cyan)" : "none",
                }} />
              </div>
            </div>
          ))}
        </div>

        {/* API Keys */}
        <div className="glass-pane" style={{ padding: 28 }}>
          <CornerBrackets />
          <div className="hud-label" style={{ marginBottom: 20 }}>API ENDPOINT MANAGEMENT</div>
          {[
            { key: "openai", label: "OPENAI ENDPOINT", placeholder: "sk-..." },
            { key: "groq", label: "GROQ ENDPOINT", placeholder: "gsk_..." },
            { key: "anthropic", label: "ANTHROPIC ENDPOINT", placeholder: "sk-ant-..." },
          ].map(({ key, label, placeholder }) => (
            <div key={key} style={{ marginBottom: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <div className="hud-label" style={{ fontSize: 8 }}>{label}</div>
                <div style={{ fontFamily: "var(--font-hud)", fontSize: 7, color: keys[key] ? "var(--green)" : "var(--text-dim)", display: "flex", alignItems: "center", gap: 4 }}>
                  <div className="status-dot" style={{ background: keys[key] ? "var(--green)" : "rgba(255,255,255,0.2)", boxShadow: keys[key] ? "0 0 6px var(--green)" : "none" }} />
                  {keys[key] ? "CONNECTED" : "DISCONNECTED"}
                </div>
              </div>
              <input className="input-field" type="password" placeholder={placeholder}
                value={keys[key]} onChange={e => setKeys(k => ({ ...k, [key]: e.target.value }))} />
            </div>
          ))}
          <button className="btn-primary" style={{ animation: "glowPink 2.5s ease-in-out infinite", marginTop: 8 }}>◈ VERIFY CONNECTIONS</button>
        </div>

        {/* System info */}
        <div className="glass-pane" style={{ padding: 28 }}>
          <CornerBrackets />
          <div className="hud-label" style={{ marginBottom: 20 }}>SYSTEM STATUS</div>
          {[
            { l: "CORE ENGINE", v: "OPTIMAL", c: "var(--green)" },
            { l: "DATABASE SYNC", v: "LIVE", c: "var(--green)" },
            { l: "RADAR ARRAY", v: "ACTIVE", c: "var(--cyan)" },
            { l: "ARCHIVE STORE", v: "READY", c: "var(--cyan)" },
            { l: "THREAT LEVEL", v: "NOMINAL", c: "var(--amber)" },
          ].map(({ l, v, c }) => (
            <div key={l} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: "1px solid rgba(0,245,255,0.07)" }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-dim)" }}>{l}</span>
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <div className="status-dot" style={{ background: c, boxShadow: `0 0 6px ${c}` }} />
                <span style={{ fontFamily: "var(--font-hud)", fontSize: 9, color: c, letterSpacing: "0.1em" }}>{v}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── APP SHELL ─────────────────────────────────────────────────────────────────
export default function App() {
  const [page, setPage] = useState("landing");
  const noSidebar = page === "login" || page === "signup" || page === "landing";

  const renderPage = () => {
    switch (page) {
      case "landing": return <LandingPage setPage={setPage} />;
      case "login": return <LoginPage setPage={setPage} />;
      case "signup": return <SignupPage setPage={setPage} />;
      case "dashboard": return <Dashboard setPage={setPage} />;
      case "chat": return <ChatPage />;
      case "analysis": return <AnalysisPage />;
      case "archive": return <ArchivePage />;
      case "settings": return <SettingsPage />;
      default: return <LandingPage setPage={setPage} />;
    }
  };

  return (
    <>
      <style>{globalStyles}</style>
      <div style={{ display: "flex", minHeight: "100vh", position: "relative" }}>
        <GridBg />
        {!noSidebar && <Sidebar page={page} setPage={setPage} />}
        <main style={{ flex: 1, position: "relative", zIndex: 1, overflowY: page === "chat" ? "hidden" : "auto", display: "flex", flexDirection: "column" }}>
          {renderPage()}
        </main>
      </div>
    </>
  );
}
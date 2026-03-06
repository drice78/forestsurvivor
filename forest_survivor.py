import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Forest Survivor: Zelda Edition",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    section[data-testid="stSidebar"] { display: none; }
    iframe { border: none; display: block; }
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Dungeon Master: A Zelda Saga</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:100%; height:100%; background:#050e05; color:#c8d8c8;
  font-family:'Press Start 2P','Courier New',monospace; overflow:hidden; user-select:none; }

/* ── Name screen ── */
#nameScreen { position:fixed; inset:0; background:#050e05; z-index:300;
  display:flex; flex-direction:row; align-items:stretch; }

#nameLeft { flex:1; display:flex; flex-direction:column; align-items:center;
  justify-content:center; gap:11px; padding:20px; }
#nameLeft h1 { font-size:clamp(13px,2.5vw,20px); color:#f0c040; text-shadow:0 0 20px #f0a000; }
#nameLeft h2 { font-size:clamp(7px,1.3vw,10px); color:#78c858; }
#nameLeft p  { font-size:clamp(5px,.9vw,7px); color:#80a880; text-align:center;
  max-width:400px; line-height:1.9; }
#nameInput { background:#0a1a0a; border:2px solid #f0c040; color:#f0f0a0;
  font-family:inherit; font-size:15px; padding:7px 12px; border-radius:4px;
  text-align:center; width:260px; outline:none; }
#nameInput:focus { box-shadow:0 0 12px #f0a00050; }

.sliderRow { display:flex; align-items:center; gap:10px; }
.sliderRow label { font-size:6px; color:#f0c040; }
.diffRow { display:flex; gap:5px; }
.diffBtn { font-family:inherit; font-size:6px; padding:4px 9px;
  border:2px solid #2d5a1b; background:#0d280d; color:#90d878;
  cursor:pointer; border-radius:3px; }
.diffBtn.sel { background:#1a5a1a; border-color:#f0c040; color:#f0c040; }

/* leaderboard panel */
#nameRight { width:240px; background:#0a1a0a; border-left:2px solid #2d5a1b;
  display:flex; flex-direction:column; padding:12px; gap:6px; overflow-y:auto; }
#nameRight h3 { font-size:8px; color:#f0c040; text-align:center; margin-bottom:4px; }
.lbRow { display:flex; justify-content:space-between; font-size:7px; padding:4px 6px;
  border-bottom:1px solid #1a3a1a; }
.lbRow.top1 { color:#f0c040; }
.lbRow.top2 { color:#c0c0c0; }
.lbRow.top3 { color:#c08040; }
#lbEmpty { font-size:6px; color:#507050; text-align:center; padding:12px; }
.lbLegend { font-size:5px; color:#507050; line-height:1.8; margin-top:auto; }

/* ── App layout ── */
#app { display:none; flex-direction:column; width:100vw; height:100vh; }
#topBar { height:30px; background:#0a1f0a; border-bottom:2px solid #2d5a1b;
  display:flex; align-items:center; padding:0 10px; gap:16px; flex-shrink:0; }
#topTitle  { font-size:9px; color:#f0c040; }
#timeDisp  { font-size:8px; color:#e0d0a0; }
#blessingDisp { font-size:7px; color:#f0c040; }
#floorDisp { font-size:8px; color:#d0a0ff; margin-left:auto; }
#scoreDisp { font-size:7px; color:#a0f0a0; }
#rupeeDisp { font-size:8px; color:#00e8ff; }
#floorBanner { position:absolute; top:8px; left:50%; transform:translateX(-50%);
  background:rgba(0,0,0,.75); color:#f0c040; font-size:9px; padding:3px 12px;
  border:1px solid #5a4000; border-radius:4px; pointer-events:none; z-index:3;
  white-space:nowrap; text-shadow:0 0 8px #b08000; letter-spacing:.5px; }
#mobileStats { display:none; align-items:center; gap:8px; font-size:7px; margin-left:auto; }

#mainRow { display:flex; flex:1; overflow:hidden; }
#canvasWrap { position:relative; flex:1; overflow:hidden; background:#0a1a0a; }
#gameCanvas { display:block; image-rendering:pixelated; }
#nightVig { position:absolute; inset:0; pointer-events:none; z-index:2;
  background:radial-gradient(ellipse at center,rgba(0,0,10,.05) 20%,rgba(0,0,30,.88) 100%);
  opacity:0; transition:opacity 2s; }
#timebar { position:absolute; bottom:4px; left:4px; right:4px; height:6px;
  background:#111; border:1px solid #333; border-radius:3px; z-index:3; }
#timefill { height:100%; border-radius:3px; transition:width .4s,background .8s; }

/* Triforce flash effect */
#triFlash { position:absolute; inset:0; pointer-events:none; z-index:10;
  background:radial-gradient(circle at center,rgba(255,220,0,.7) 0%,rgba(240,180,0,.3) 50%,transparent 100%);
  display:none; }
#triFlash.on { display:block; animation:triPulse 3s ease-out forwards; }
@keyframes triPulse {
  0%   { opacity:0; transform:scale(.8); }
  15%  { opacity:1; transform:scale(1.05); }
  40%  { opacity:.9; }
  100% { opacity:0; transform:scale(1.1); }
}
/* Triforce blessing golden border */
#canvasWrap.blessed { box-shadow:inset 0 0 20px rgba(240,192,0,.5); }

/* UI panel */
#uiPanel { width:220px; background:#090f09; border-left:2px solid #2d5a1b;
  display:flex; flex-direction:column; padding:6px; gap:5px; overflow-y:auto; flex-shrink:0; }
.uiBox { background:#0d1f0d; border:1px solid #1e4a1e; border-radius:3px; padding:5px; }
.uiLbl { font-size:6px; color:#f0c040; text-transform:uppercase; letter-spacing:1px; margin-bottom:3px; }
.uiVal { font-size:9px; color:#90d878; }
.heart { font-size:12px; line-height:1; }
#heartsRow { display:flex; flex-wrap:wrap; gap:1px; margin-top:2px; }
/* XP bar */
#xpBarOuter { height:7px; background:#0a1a0a; border:1px solid #1e4a1e; border-radius:3px; margin-top:3px; }
#xpBarFill  { height:100%; background:linear-gradient(90deg,#3080e0,#60b0ff); border-radius:3px;
  width:0%; transition:width .4s; }
#xpText { font-size:5px; color:#6090c0; margin-top:2px; }
#invList { max-height:130px; overflow-y:auto; }
.invItem { font-size:7px; padding:3px 4px; border:1px solid #1a3a1a; margin-bottom:2px;
  border-radius:2px; cursor:pointer; color:#a8c8a8; display:flex; align-items:center; gap:3px; }
.invItem:hover { border-color:#f0c040; color:#f0e060; }
.invItem.eq { border-color:#4090f0; color:#80c0ff; }
#tfDisp { font-size:12px; letter-spacing:4px; margin-top:2px; }
#opStatus { font-size:6px; color:#a0c8a0; line-height:1.9; }

/* Minimap */
#minimap { display:block; margin:0 auto; border:1px solid #2d5a1b;
  border-radius:2px; image-rendering:pixelated; }
.mmLegend { font-size:5px; color:#507050; line-height:1.9; margin-top:3px; }

/* ── D-pad controls ── */
#dpad { display:none; grid-template-columns:repeat(3,44px); grid-template-rows:repeat(3,44px);
  gap:3px; padding:8px; flex-shrink:0; align-self:center; border-right:2px solid #2d5a1b; }
.dpBtn { width:44px; height:44px; background:#0d280d; border:2px solid #2d5a1b;
  border-radius:9px; color:#90d878; font-size:18px; display:flex; align-items:center;
  justify-content:center; cursor:pointer; font-family:inherit;
  -webkit-tap-highlight-color:transparent; touch-action:manipulation; user-select:none; }
.dpBtn:active { background:#2a6a2a; transform:scale(.86); }
.dpBlank { visibility:hidden; pointer-events:none; width:44px; height:44px; }
/* show D-pad only on touch/coarse-pointer devices */
@media (pointer:coarse) { #dpad { display:grid; } #bottomRow { height:130px; } }
/* mobile responsive layout */
@media (max-width:640px) {
  #uiPanel { display:none; }
  #mobileStats { display:flex !important; }
  #topTitle { display:none; }
  #bottomRow { height:130px; }
  #actionBar { width:160px; }
  #actionBar .btn { font-size:6px; padding:6px 4px; min-height:30px; }
}

/* bottom row */
#bottomRow { height:95px; background:#050e05; border-top:2px solid #2d5a1b;
  display:flex; flex-shrink:0; }
#msgLog { flex:1; overflow-y:auto; padding:5px 8px; font-size:8px; line-height:1.9; }
#actionBar { width:190px; border-left:2px solid #2d5a1b; padding:5px;
  display:flex; flex-direction:column; gap:3px; justify-content:center; }

/* buttons */
.btn { font-family:inherit; font-size:7px; padding:4px 7px; border:2px solid #2d5a1b;
  background:#0d280d; color:#90d878; cursor:pointer; border-radius:3px;
  text-align:center; transition:background .1s; width:100%; }
.btn:hover { background:#1a4a1a; color:#c8f0a8; }
.btn:active { transform:scale(.97); }
.btn-gold { border-color:#c09020; color:#f0c040; background:#1a1200; }
.btn-gold:hover { background:#2a2000; }
.btn-red  { border-color:#7a2020; color:#f08080; background:#1a0808; }
.btn-red:hover { background:#2a1010; }
.btn-tri  { border-color:#c09020; color:#f0c040; background:#1a1400;
  animation:glowBtn 1.5s ease-in-out infinite; }
@keyframes glowBtn {
  0%,100% { box-shadow:none; }
  50% { box-shadow:0 0 10px rgba(240,192,0,.6); }
}

/* overlay */
#overlay { display:none; position:absolute; inset:0; background:rgba(0,0,0,.88);
  z-index:50; align-items:center; justify-content:center; }
#overlay.on { display:flex; }
#oBox { background:#0d200d; border:3px solid #f0c040; border-radius:6px; padding:20px;
  max-width:460px; width:93%; text-align:center; max-height:88vh; overflow-y:auto; }
#oBox h2 { font-size:13px; color:#f0c040; margin-bottom:10px; }
#oBox p  { font-size:8px; color:#c0d8c0; margin-bottom:6px; line-height:1.8; }
.oRow { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; margin-top:10px; }
.oRow .btn { width:auto; padding:6px 12px; }

/* message colours */
.mi { color:#90d878; } .md { color:#f07878; } .mw { color:#f0c040; }
.ml { color:#c090f0; font-style:italic; } .ms { color:#60e8ff; }

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:#050e05; }
::-webkit-scrollbar-thumb { background:#2d5a1b; border-radius:2px; }
</style>
</head>
<body>

<!-- ══════════ NAME / SETTINGS SCREEN ══════════ -->
<div id="nameScreen">
  <div id="nameLeft">
    <h1>⚔️ DUNGEON MASTER ⚔️</h1>
    <h2>— A Zelda Saga —</h2>
    <p>Drawn into a cursed dungeon of five floors, you must fight your way to the deepest abyss.<br>
       Defeat each floor's guardian to descend. Survive the darkness. Become the Dungeon Master.</p>

    <input id="nameInput" type="text" placeholder="Enter hero name..." maxlength="12" />

    <div class="sliderRow">
      <label>Difficulty:</label>
      <div class="diffRow">
        <button class="diffBtn" id="dEasy"  onclick="setDiff('easy')">Easy</button>
        <button class="diffBtn sel" id="dNorm" onclick="setDiff('normal')">Normal</button>
        <button class="diffBtn" id="dHard"  onclick="setDiff('hard')">Hard</button>
      </div>
    </div>

    <button class="btn btn-gold" onclick="startGame()"
      style="width:210px;font-size:9px;padding:9px;">⚔️ BEGIN ADVENTURE</button>

    <p><span style="color:#f0c040">Goal</span>: Defeat the floor boss to descend · 5 floors total<br>
       Arrow Keys / WASD · <span style="color:#f0c040">I</span>=Inventory
       <span style="color:#f0c040">F</span>=Forage
       <span style="color:#f0c040">R</span>=Rest
       <span style="color:#f0c040">Space</span>=Look<br>
       🪓 Stone Axe (Wood+Stone) chops trees &nbsp;·&nbsp; 🚣 Find Boats to sail water<br>
       🔱 Collect all 3 Triforce pieces for a special blessing!</p>
  </div>

  <!-- Leaderboard panel -->
  <div id="nameRight">
    <h3>🏆 HIGH SCORES</h3>
    <div id="lbList"><div id="lbEmpty">No scores yet.<br>Be the first survivor!</div></div>
    <div class="lbLegend">
      Score = Floor × 500 + Rupees<br>
      + Triforce × 300<br>
      + Outposts × 150<br>
      + Levels × 100<br>
      × Difficulty bonus
    </div>
  </div>
</div>

<!-- ══════════ MAIN APP ══════════ -->
<div id="app">
  <div id="topBar">
    <div id="topTitle">⚔️ Dungeon Master</div>
    <div id="timeDisp">☀️ Day 1 · Morning</div>
    <div id="blessingDisp"></div>
    <div id="floorDisp">Floor: 1 / 5</div>
    <div id="scoreDisp">⭐ 0</div>
    <div id="rupeeDisp">💎 0</div>
    <span id="mobileStats">
      <span id="msHp">❤️ 12</span>
      <span id="msLv">Lv1</span>
      <span id="msRup">💎 0</span>
      <span id="msNight">⚔️ Fl.1/5</span>
    </span>
  </div>

  <div id="mainRow">
    <div id="canvasWrap">
      <canvas id="gameCanvas"></canvas>
      <div id="nightVig"></div>
      <div id="floorBanner">🌲 The Haunted Forest  |  Floor 1/5</div>
      <div id="triFlash"></div>
      <div id="timebar"><div id="timefill"></div></div>
      <div id="overlay">
        <div id="oBox">
          <h2 id="oTitle"></h2>
          <div id="oContent"></div>
          <div class="oRow" id="oBtns"></div>
        </div>
      </div>
    </div>

    <div id="uiPanel">
      <div class="uiBox">
        <div class="uiLbl">Hero</div>
        <div class="uiVal" id="uiName">—</div>
      </div>
      <div class="uiBox">
        <div class="uiLbl">Health</div>
        <div id="heartsRow"></div>
      </div>
      <div class="uiBox">
        <div class="uiLbl">Level <span id="uiLevel">1</span></div>
        <div id="xpBarOuter"><div id="xpBarFill"></div></div>
        <div id="xpText">0 / 50 XP</div>
      </div>
      <div class="uiBox">
        <div class="uiLbl">Equipment</div>
        <div style="font-size:7px;color:#a0c8a0;line-height:1.9;">
          ⚔️ <span id="eqW">Fists</span><br>
          🛡️ <span id="eqA">None</span>
        </div>
      </div>
      <div class="uiBox">
        <div class="uiLbl">Inventory (<span id="invCnt">0</span>/20)</div>
        <div id="invList"></div>
      </div>
      <div class="uiBox">
        <div class="uiLbl">Triforce Quest</div>
        <div id="tfDisp">△△△</div>
        <div id="blessingBar" style="display:none;font-size:6px;color:#f0c040;margin-top:3px;"></div>
      </div>
      <div class="uiBox">
        <div class="uiLbl">Outposts</div>
        <div id="opStatus"></div>
      </div>
      <!-- Minimap -->
      <div class="uiBox">
        <div class="uiLbl">Minimap</div>
        <canvas id="minimap" width="160" height="160"></canvas>
        <div class="mmLegend">
          <span style="color:#fff">■</span> You &nbsp;
          <span style="color:#00ffcc">■</span> Camp &nbsp;
          <span style="color:#ff4040">■</span> Locked<br>
          <span style="color:#00ff80">■</span> Open &nbsp;
          <span style="color:#f0c040">·</span> Chest &nbsp;
          <span style="color:#ff8800">·</span> Key &nbsp;
          <span style="color:#ffff00">✦</span> Tri
        </div>
      </div>
    </div>
  </div>

  <div id="bottomRow">
    <!-- D-pad (shown on touch devices via CSS) -->
    <div id="dpad">
      <div class="dpBlank"></div>
      <button class="dpBtn" id="dpUp"   aria-label="Move Up">▲</button>
      <div class="dpBlank"></div>
      <button class="dpBtn" id="dpLeft" aria-label="Move Left">◀</button>
      <div class="dpBlank"></div>
      <button class="dpBtn" id="dpRight" aria-label="Move Right">▶</button>
      <div class="dpBlank"></div>
      <button class="dpBtn" id="dpDown" aria-label="Move Down">▼</button>
      <div class="dpBlank"></div>
    </div>
    <div id="msgLog"></div>
    <div id="actionBar">
      <button class="btn"       onclick="doForage()">🌿 Forage (F)</button>
      <button class="btn"       onclick="doRest()">💤 Rest (R)</button>
      <button class="btn btn-gold" onclick="openInvScreen()">🎒 Inventory (I)</button>
      <button class="btn"       onclick="doLook()">👁️ Look (Space)</button>
    </div>
  </div>
</div>

<script>
// ╔══════════════════════════════════════════════════════════╗
// ║                     CONSTANTS                           ║
// ╚══════════════════════════════════════════════════════════╝
const MW=80, MH=80;
const TS=40;
const ACT_PER_HOUR=4;
const DAY_START=6, DAY_END=20;
const MM_S=2; // minimap pixels per tile

const T={GR:0,TR:1,DT:2,WA:3,ST:4,SA:5,TH:6};
const E={CHEST:'chest',KEY:'key',OUTPOST:'outpost',CAMP:'camp',TRI:'triforce',
         BOAT:'boat',BOK:'bokoblin',KEE:'keese',SKU:'skulltula',LIZ:'lizalfos',
         DEER:'deer',RAB:'rabbit',FOX:'fox',
         GLEEOK:'gleeok',DARKLYNEL:'darklynel',
         CHUCHU:'chuchu',WIZZROBE:'wizzrobe',DARKKNIGHT:'darkknight',PHANTOM:'phantom',
         DESCENT:'descent'};

const DIFF_MULT={easy:[0.55,0.55,0.6,1.0], normal:[0.80,0.75,1.0,1.5], hard:[1.15,1.10,1.4,2.0]};

// ── Konami code ↑↑↓↓←→←→  (or press ` backtick for direct access) ──
let _konamiSeq=[];
const KONAMI=['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight'];
function _pushKonami(key){
  _konamiSeq.push(key);
  if(_konamiSeq.length>KONAMI.length) _konamiSeq.shift();
  // Find longest KONAMI prefix that matches the tail of _konamiSeq
  let kMatch=0;
  const sl=_konamiSeq.length;
  for(let len=Math.min(sl,KONAMI.length);len>=1;len--){
    if(_konamiSeq.slice(sl-len).every((k,i)=>k===KONAMI[i])){ kMatch=len; break; }
  }
  // Show subtle progress dots in the top bar once 3+ keys are in
  const bd=document.getElementById('blessingDisp');
  if(bd&&kMatch>=3&&kMatch<KONAMI.length&&G&&!G.bloodMoon&&!G.monsterFrenzy)
    bd.textContent='🔑'.repeat(kMatch);
  if(G&&_konamiSeq.join(',')===KONAMI.join(',')){ _konamiSeq=[]; openCheatMenu(); }
}

const BOSSES={
  gleeok:{
    name:'Gleeok', ic:'🐉', hp:30, atk:4, def:2, xp:150, rMin:40, rMax:80,
    drops:['Master Sword','Blue Potion','Hylian Shield'],
    special:{name:'Flame Breath', every:3, type:'flame', dmg:5,
             warn:'🔥 Gleeok rears its heads — FLAME BREATH incoming!'},
  },
  darklynel:{
    name:'Dark Lynel', ic:'🦁', hp:55, atk:6, def:3, xp:250, rMin:60, rMax:120,
    drops:['Master Sword','Blue Potion','Hylian Shield','Fairy'],
    special:{name:'Berserker Spin', every:4, type:'spin', hits:2,
             warn:'🌀 Dark Lynel winds up — BERSERKER SPIN incoming!'},
  },
  forestwarden:{
    name:'Forest Warden', ic:'🌲', hp:28, atk:3, def:1, xp:180, rMin:40, rMax:70,
    drops:['Master Sword','Blue Potion','Red Potion','Hylian Shield'],
    special:{name:'Root Snare', every:3, type:'snare', dmg:3,
             warn:'🌿 Forest Warden summons roots — ROOT SNARE incoming!'},
  },
  stonegolem:{
    name:'Stone Golem', ic:'🗿', hp:45, atk:4, def:4, xp:220, rMin:50, rMax:90,
    drops:['Master Sword','Hylian Shield','Blue Potion','Stone Axe'],
    special:{name:'Tremor', every:3, type:'tremor', dmg:4,
             warn:'🪨 The Golem stomps — TREMOR incoming!'},
  },
  firedrake:{
    name:'Fire Drake', ic:'🔥', hp:60, atk:6, def:2, xp:270, rMin:55, rMax:100,
    drops:['Master Sword','Blue Potion','Hylian Shield','Fairy'],
    special:{name:'Inferno Breath', every:3, type:'flame', dmg:8,
             warn:'🔥 Fire Drake rears up — INFERNO BREATH incoming!'},
  },
  shadowknight:{
    name:'Shadow Knight', ic:'⚔️', hp:75, atk:6, def:3, xp:320, rMin:55, rMax:110,
    drops:['Master Sword','Blue Potion','Hylian Shield','Fairy'],
    special:{name:'Phase Strike', every:4, type:'spin', hits:2,
             warn:'🌑 Shadow Knight phases — PHASE STRIKE incoming!'},
  },
  darklord:{
    name:'The Dark Lord', ic:'👑', hp:100, atk:8, def:4, xp:500, rMin:60, rMax:120,
    drops:['Master Sword','Blue Potion','Hylian Shield','Fairy'],
    special:{name:'Void Blast', every:3, type:'flame', dmg:10,
             warn:'💀 The Dark Lord raises his hand — VOID BLAST incoming!'},
  },
};

let diffKey='normal';
function setDiff(k){
  diffKey=k;
  ['easy','normal','hard'].forEach(d=>{
    const el=document.getElementById('d'+d.charAt(0).toUpperCase()+d.slice(1));
    if(el) el.classList.toggle('sel',d===k);
  });
}

const LEVEL_CFG=[null, // 1-indexed
  { // Floor 1: Haunted Forest
    name:'The Haunted Forest', icon:'🌲', floorNum:1,
    desc:'Ancient trees hide terrible monsters...',
    monPool:[E.BOK,E.KEE,E.BOK,E.SKU],
    bossType:'forestwarden',
    TCOL:{[T.GR]:'#274f18',[T.TR]:'#1a4509',[T.DT]:'#0e2a05',[T.WA]:'#19366a',[T.ST]:'#444444',[T.SA]:'#7a6a3a',[T.TH]:'#1a3306'},
    MMAP:{[T.GR]:[39,79,24],[T.TR]:[26,69,9],[T.DT]:[14,42,5],[T.WA]:[25,54,106],[T.ST]:[85,85,85],[T.SA]:[122,106,58],[T.TH]:[26,51,6]},
    TEM:{[T.TR]:'🌲',[T.DT]:'🌳',[T.ST]:'🪨',[T.TH]:'🌿'},
    bgColor:'#050e05', borderColor:'#2d5a1b', titleColor:'#78c858',
    waterName:'River', nightName:'Night', dawnName:'Dawn',
  },
  { // Floor 2: Stone Caverns
    name:'The Stone Caverns', icon:'🪨', floorNum:2,
    desc:'Deep tunnels riddled with rock and shadow...',
    monPool:[E.SKU,E.LIZ,E.CHUCHU,E.SKU],
    bossType:'stonegolem',
    TCOL:{[T.GR]:'#252530',[T.TR]:'#18182a',[T.DT]:'#100f1a',[T.WA]:'#6b2800',[T.ST]:'#5a5a70',[T.SA]:'#3a3848',[T.TH]:'#1a1825'},
    MMAP:{[T.GR]:[37,37,48],[T.TR]:[24,24,42],[T.DT]:[16,15,26],[T.WA]:[107,40,0],[T.ST]:[90,90,112],[T.SA]:[58,56,72],[T.TH]:[26,24,37]},
    TEM:{[T.TR]:'🪨',[T.DT]:'💎',[T.ST]:'🗿',[T.TH]:'🕸️'},
    bgColor:'#0a0a14', borderColor:'#4a4a6a', titleColor:'#9090c0',
    waterName:'Lava', nightName:'Dark Cycle', dawnName:'Torch-light',
  },
  { // Floor 3: Lava Forge
    name:'The Lava Forge', icon:'🔥', floorNum:3,
    desc:'Rivers of molten rock and ancient forges of war...',
    monPool:[E.LIZ,E.WIZZROBE,E.LIZ,E.CHUCHU],
    bossType:'firedrake',
    TCOL:{[T.GR]:'#3a1a08',[T.TR]:'#200800',[T.DT]:'#200a00',[T.WA]:'#e83a00',[T.ST]:'#4a2818',[T.SA]:'#5a3020',[T.TH]:'#280800'},
    MMAP:{[T.GR]:[58,26,8],[T.TR]:[32,8,0],[T.DT]:[32,10,0],[T.WA]:[232,58,0],[T.ST]:[74,40,24],[T.SA]:[90,48,32],[T.TH]:[40,8,0]},
    TEM:{[T.TR]:'🌋',[T.DT]:'🔥',[T.ST]:'⛏️',[T.TH]:'🌑'},
    bgColor:'#140500', borderColor:'#8a3010', titleColor:'#f08040',
    waterName:'Lava', nightName:'Inferno', dawnName:'Cooling',
  },
  { // Floor 4: Dark Castle
    name:'The Dark Castle', icon:'🏰', floorNum:4,
    desc:'Shadow-cloaked battlements where dark knights patrol...',
    monPool:[E.DARKKNIGHT,E.WIZZROBE,E.DARKKNIGHT,E.PHANTOM],
    bossType:'shadowknight',
    TCOL:{[T.GR]:'#1a1a2a',[T.TR]:'#0f0f20',[T.DT]:'#08080f',[T.WA]:'#0a0a50',[T.ST]:'#353545',[T.SA]:'#252535',[T.TH]:'#0d0d1a'},
    MMAP:{[T.GR]:[26,26,42],[T.TR]:[15,15,32],[T.DT]:[8,8,15],[T.WA]:[10,10,80],[T.ST]:[53,53,69],[T.SA]:[37,37,53],[T.TH]:[13,13,26]},
    TEM:{[T.TR]:'🗼',[T.DT]:'⚫',[T.ST]:'🔩',[T.TH]:'🌀'},
    bgColor:'#05050f', borderColor:'#3030a0', titleColor:'#7070e0',
    waterName:'Abyss', nightName:'Dark Watch', dawnName:'Pale Light',
  },
  { // Floor 5: Shadow Abyss
    name:'The Shadow Abyss', icon:'💀', floorNum:5,
    desc:'The final darkness. The Dark Lord awaits his challenger...',
    monPool:[E.DARKKNIGHT,E.PHANTOM,E.WIZZROBE,E.DARKKNIGHT],
    bossType:'darklord',
    TCOL:{[T.GR]:'#150010',[T.TR]:'#0a0008',[T.DT]:'#050005',[T.WA]:'#300030',[T.ST]:'#3a0040',[T.SA]:'#200025',[T.TH]:'#0a0010'},
    MMAP:{[T.GR]:[21,0,16],[T.TR]:[10,0,8],[T.DT]:[5,0,5],[T.WA]:[48,0,48],[T.ST]:[58,0,64],[T.SA]:[32,0,37],[T.TH]:[10,0,16]},
    TEM:{[T.TR]:'💀',[T.DT]:'🌑',[T.ST]:'💠',[T.TH]:'🌀'},
    bgColor:'#050008', borderColor:'#800080', titleColor:'#c060ff',
    waterName:'Void', nightName:'Eternal Dark', dawnName:'Shadow Shift',
  },
];

// ── Items ──────────────────────────────────────────────────
const ITEMS={
  'Wooden Sword':    {ic:'⚔️', tp:'weapon', atk:1,  desc:'A simple carved sword.'},
  'Iron Sword':      {ic:'⚔️', tp:'weapon', atk:2,  desc:'A sturdy iron blade.'},
  'Master Sword':    {ic:'⚔️', tp:'weapon', atk:5,  desc:"The sacred blade of evil's bane!"},
  "Biggoron's Sword":{ic:'🗡️', tp:'weapon', atk:7,  desc:"A colossal blade forged by Biggoron. Unstoppable!"},
  'Deku Stick':      {ic:'🪵', tp:'weapon', atk:1,  desc:'A dried Deku stick.'},
  'Stone Axe':       {ic:'🪓', tp:'axe',    atk:2,  desc:'Chop trees AND fight! Equip to cut through forest.'},
  'Hylian Shield':   {ic:'🛡️', tp:'armor',  def:3,  desc:'The legendary Hylian Shield!'},
  'Iron Shield':     {ic:'🛡️', tp:'armor',  def:2,  desc:'A solid iron shield.'},
  'Wooden Shield':   {ic:'🛡️', tp:'armor',  def:1,  desc:'A basic wooden shield.'},
  'Red Potion':      {ic:'🧪', tp:'use',    heal:4, desc:'Restores 2 hearts.'},
  'Blue Potion':     {ic:'🫙', tp:'use',    heal:99,desc:'Restores ALL hearts!'},
  'Fairy':           {ic:'🧚', tp:'use',    revive:true, desc:'Auto-revives once if you fall.'},
  'Stamella Shroom': {ic:'🍄', tp:'use',    heal:2, desc:'Restores 1 heart.'},
  'Hylian Shroom':   {ic:'🍄', tp:'use',    heal:3, desc:'Restores 1.5 hearts.'},
  'Berries':         {ic:'🫐', tp:'use',    heal:1, desc:'Restores 0.5 hearts.'},
  'Wood':            {ic:'🪵', tp:'mat',    desc:'Useful wood for crafting.'},
  'Stone':           {ic:'🪨', tp:'mat',    desc:'A chunk of stone.'},
  'Monster Fang':    {ic:'🦷', tp:'mat',    desc:'A fang from a defeated monster.'},
  'Monster Horn':    {ic:'🔱', tp:'mat',    desc:'A curved horn from a Lizalfos.'},
  'Keese Wing':      {ic:'🪶', tp:'mat',    desc:'A leathery Keese wing.'},
  'Spider Silk':     {ic:'🕸️', tp:'mat',    desc:'Strong silk from a Skulltula.'},
  'Lantern':         {ic:'🏮', tp:'tool',   desc:'Lights up the night. Reduces monster spawns!'},
  'Map Fragment':    {ic:'🗺️', tp:'tool',   desc:'Reveals a hidden area of the map.'},
  'Arrows (5)':      {ic:'🏹', tp:'ammo',   desc:'A bundle of 5 arrows.'},
  'Boat':            {ic:'🚣', tp:'boat',   desc:'A wooden rowboat. Lets you sail across water!'},
  'Outpost Key 1':   {ic:'🗝️', tp:'key', opens:0, desc:'Key to Outpost Oaken.'},
  'Outpost Key 2':   {ic:'🗝️', tp:'key', opens:1, desc:'Key to Outpost Hollow.'},
  'Outpost Key 3':   {ic:'🗝️', tp:'key', opens:2, desc:'Key to Outpost Grimrock.'},
  'Outpost Key 4':   {ic:'🗝️', tp:'key', opens:3, desc:'Key to Outpost Duskwood.'},
  'Outpost Key 5':   {ic:'🗝️', tp:'key', opens:4, desc:'Key to Outpost Zephyr.'},
  'Triforce of Power':   {ic:'🔱', tp:'tri', piece:0, desc:'A shard of the Triforce of Power!'},
  'Triforce of Wisdom':  {ic:'🔱', tp:'tri', piece:1, desc:'A shard of the Triforce of Wisdom!'},
  'Triforce of Courage': {ic:'🔱', tp:'tri', piece:2, desc:'A shard of the Triforce of Courage!'},
};

const RECIPES=[
  {result:'Stone Axe',    needs:['Wood','Stone'],              desc:'Chop trees & fight'},
  {result:'Deku Stick',   needs:['Wood','Wood'],               desc:'Basic weapon'},
  {result:'Wooden Shield',needs:['Wood','Wood','Wood'],        desc:'Light defense'},
  {result:'Iron Sword',   needs:['Monster Fang','Stone','Wood'],desc:'Strong blade'},
  {result:'Red Potion',   needs:['Stamella Shroom','Berries'], desc:'Healing potion'},
  {result:'Map Fragment', needs:['Spider Silk','Keese Wing'],  desc:'Reveals map area'},
];

const OP_NAMES=['Oaken','Hollow','Grimrock','Duskwood','Zephyr'];

const LORE=[
  "The ancient trees whisper... Three goddesses hid the Triforce here for safekeeping. Find all three pieces.",
  "Carved into bark: 'Monsters grow bolder each night. Seek the outposts for shelter and safety.'",
  "A faded note: 'The five keys were scattered by the forest guardians. Search everywhere — in chests, near ruins.'",
  "Stone inscription: 'He who unites the Triforce shall be blessed by the Golden Power of the Three Goddesses.'",
  "Old journal entry: 'Night 50 brought Lizalfos. Only the lantern kept them at bay. Craft one early!'",
];

const MON={
  bokoblin: {name:'Bokoblin', ic:'👺', hp:4,  atk:1, def:0, rMin:5,  rMax:12, xp:15, drops:['Monster Fang','Berries','Wood']},
  keese:    {name:'Keese',    ic:'🦇', hp:2,  atk:1, def:0, rMin:2,  rMax:7,  xp:8,  drops:['Keese Wing']},
  skulltula:{name:'Skulltula',ic:'🕷️', hp:4,  atk:2, def:0, rMin:6,  rMax:15, xp:22, drops:['Spider Silk','Monster Fang']},
  lizalfos: {name:'Lizalfos', ic:'🦎', hp:7,  atk:2, def:1, rMin:12, rMax:22, xp:35, drops:['Monster Horn','Monster Fang']},
  chuchu:     {name:'Rock ChuChu',  ic:'🟣', hp:6,  atk:2, def:2, rMin:8,  rMax:20, xp:28, drops:['Stone','Stone','Monster Fang']},
  wizzrobe:   {name:'Wizzrobe',     ic:'🧙', hp:5,  atk:4, def:0, rMin:14, rMax:28, xp:40, drops:['Blue Potion','Monster Horn','Arrows (5)']},
  darkknight: {name:'Dark Knight',  ic:'🗡️', hp:10, atk:4, def:2, rMin:18, rMax:35, xp:50, drops:['Iron Sword','Iron Shield','Monster Fang']},
  phantom:    {name:'Phantom',      ic:'👻', hp:9,  atk:5, def:1, rMin:20, rMax:40, xp:55, drops:['Blue Potion','Monster Horn','Hylian Shield']},
};

const SHOP=[
  {name:'Red Potion',      price:20},
  {name:'Stamella Shroom', price:10},
  {name:'Arrows (5)',      price:15},
  {name:'Wooden Shield',   price:30},
  {name:'Lantern',         price:50},
  {name:'Map Fragment',    price:35},
  {name:'Fairy',           price:80},
  {name:'Stone Axe',       price:40},
  {name:'Boat',            price:60},
];

// ── Seeded noise for terrain ────────────────────────────────
let _nSeed=0;
function setNoiseSeed(s){_nSeed=s;}
function noise(x,y){
  const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;
  const s=_nSeed;
  function ph(a,b){let n=Math.sin(a*127.1+b*311.7+s*0.937)*43758.5453;return n-Math.floor(n);}
  const sm=t=>t*t*(3-2*t),lerp=(a,b,t)=>a+t*(b-a);
  return lerp(lerp(ph(xi,yi),ph(xi+1,yi),sm(xf)),lerp(ph(xi,yi+1),ph(xi+1,yi+1),sm(xf)),sm(yf));
}

// ╔══════════════════════════════════════════════════════════╗
// ║                   GAME STATE                            ║
// ╚══════════════════════════════════════════════════════════╝
let G={};

function newGame(name,totalNights,diff){
  setNoiseSeed(Math.floor(Math.random()*999983));
  const md=genMap();
  G={
    screen:'play', totalNights:9999, diff,
    pl:{
      name, x:md.cx, y:md.cy,
      hp:12, maxHp:12, atk:1, def:0, rupees:10,
      inv:[], eq:{w:null,a:null},
      hasFairy:false, hasLantern:false, hasBoat:false, hasAxe:false, onWater:false,
      xp:0, level:1, xpCap:50,
    },
    map:md.tiles, ents:md.ents,
    fog:Array.from({length:MH},()=>Array(MW).fill(true)),
    time:{hour:8, acts:0, night:0, isNight:false},
    triforce:[false,false,false],
    triforceBlessing:0,
    opOpen:[false,false,false,false,false],
    combat:null, combatRound:0, done:false, _pendingXP:0,
    cheats:{active:false, nayru:false, din:false},
    // Dungeon Master mode
    dungeonLevel:1, levelBossDefeated:false, levelBossId:null,
    // Events & bosses
    bloodMoon:false, bloodMoonNights:[],
    monsterFrenzy:false, stormActive:false,
    harvestLeft:0, eventCooldown:0,
    bossSpawned:[false,false],
  };
  // Pre-compute blood moon nights (every 8 nights fixed)
  for(let p=1;p<=9;p++){
    const bn=p*8;
    G.bloodMoonNights.push(bn);
  }
  reveal(md.cx,md.cy,4);
  spawnFloorBoss();
}

// ╔══════════════════════════════════════════════════════════╗
// ║               HIGH SCORE SYSTEM                         ║
// ╚══════════════════════════════════════════════════════════╝
function calcScore(){
  const dm=DIFF_MULT[G.diff]||DIFF_MULT.normal;
  const base=(G.dungeonLevel-1)*500 + G.pl.rupees
    + G.triforce.filter(t=>t).length*300
    + G.opOpen.filter(u=>u).length*150
    + (G.pl.level-1)*100;
  return Math.round(base * dm[3]);
}

function loadScores(){
  try{ return JSON.parse(localStorage.getItem('fsSurvivorScores')||'[]'); }
  catch{ return []; }
}

function saveScore(){
  const sc=calcScore();
  // Cheated runs are shown their score but never saved to the leaderboard
  if(G.cheats&&G.cheats.active) return sc;
  const scores=loadScores();
  scores.push({
    name:G.pl.name, score:sc,
    floor:G.dungeonLevel, diff:G.diff,
    tf:G.triforce.filter(t=>t).length,
    op:G.opOpen.filter(u=>u).length,
    level:G.pl.level,
    date:new Date().toLocaleDateString()
  });
  scores.sort((a,b)=>b.score-a.score);
  scores.splice(10);
  localStorage.setItem('fsSurvivorScores',JSON.stringify(scores));
  return sc;
}

function renderLeaderboard(){
  const scores=loadScores();
  const list=document.getElementById('lbList');
  const empty=document.getElementById('lbEmpty');
  if(!scores.length){
    if(empty) empty.style.display='block';
    return;
  }
  if(empty) empty.style.display='none';
  const diffIcons={easy:'🟢',normal:'🟡',hard:'🔴'};
  list.innerHTML=scores.slice(0,8).map((s,i)=>{
    const cls=i===0?'top1':i===1?'top2':i===2?'top3':'';
    return `<div class="lbRow ${cls}">
      <span>${i===0?'🥇':i===1?'🥈':i===2?'🥉':'  '} ${s.name} ${diffIcons[s.diff]||''}</span>
      <span>${s.score.toLocaleString()}</span>
    </div>
    <div style="font-size:5px;color:#405040;padding:0 6px 3px">
      Fl${s.floor||1} · Lv${s.level||1} · 🔱${s.tf}/3 · 🏰${s.op}/5 · ${s.date}
    </div>`;
  }).join('');
}

// ╔══════════════════════════════════════════════════════════╗
// ║                  MAP GENERATION                         ║
// ╚══════════════════════════════════════════════════════════╝
function genMap(){
  const tiles=Array.from({length:MH},()=>Array(MW).fill(T.GR));
  const ents=[];
  let seed=(Date.now()*_nSeed+12345)&0x7fffffff;
  function r(){seed=(seed*1664525+1013904223)&0x7fffffff;return seed/0x7fffffff;}

  for(let y=0;y<MH;y++) for(let x=0;x<MW;x++){
    if(x===0||x===MW-1||y===0||y===MH-1){tiles[y][x]=T.WA;continue;}
    const n=noise(x/14,y/14);
    if(n<.22)      tiles[y][x]=T.WA;
    else if(n<.35) tiles[y][x]=T.SA;
    else if(n>.80) tiles[y][x]=T.DT;
    else if(n>.64) tiles[y][x]=T.TR;
    else           tiles[y][x]=T.GR;
    if(tiles[y][x]===T.GR&&r()<.14) tiles[y][x]=T.TR;
    if(tiles[y][x]===T.GR&&r()<.04) tiles[y][x]=T.ST;
  }

  // Thorny thicket clusters — scattered across the map, forcing detours
  const THICKET_CLUSTERS=13;
  for(let c=0;c<THICKET_CLUSTERS;c++){
    const tcx=5+Math.floor(r()*(MW-10));
    const tcy=5+Math.floor(r()*(MH-10));
    if(Math.abs(tcx-40)<9&&Math.abs(tcy-40)<9) continue; // keep center open
    const sz=4+Math.floor(r()*6); // cluster of 4–9 tiles
    for(let i=0;i<sz;i++){
      const tx=tcx+Math.floor(r()*7)-3;
      const ty=tcy+Math.floor(r()*7)-3;
      if(tx<2||tx>=MW-2||ty<2||ty>=MH-2) continue;
      if(tiles[ty][tx]===T.GR||tiles[ty][tx]===T.SA) tiles[ty][tx]=T.TH;
    }
  }

  const cx=40,cy=40;
  clearZone(tiles,cx,cy,4);
  const reach=bfs(tiles,cx,cy);

  const opIdeal=[[14,14],[65,14],[14,65],[65,65],[40,22]];
  const opPos=opIdeal.map(([ox,oy])=>nearestReach(ox,oy,reach,tiles));
  opPos.forEach(([ox,oy],i)=>{
    clearZone(tiles,ox,oy,2);
    ents.push({tp:E.OUTPOST,x:ox,y:oy,id:`op_${i}`,idx:i,locked:true});
  });

  ents.push({tp:E.CAMP,x:cx,y:cy,id:'camp'});

  // Re-compute reach after clearing outpost areas
  const reach2=bfs(tiles,cx,cy);

  const chestPool=[
    'Wooden Sword','Wooden Sword','Iron Sword','Deku Stick','Stone Axe',
    'Wooden Shield','Iron Shield','Hylian Shield','Master Sword',
    'Red Potion','Red Potion','Blue Potion',
    'Stamella Shroom','Stamella Shroom','Hylian Shroom','Berries',
    'Lantern','Map Fragment','Arrows (5)','Boat',
    'Stone','Stone','Wood','Wood','Monster Fang',
  ];
  for(let i=0;i<18;i++){
    const [ex,ey]=openReach(tiles,ents,r,reach2);
    const loot=chestPool[Math.floor(r()*chestPool.length)];
    ents.push({tp:E.CHEST,x:ex,y:ey,id:`ch_${i}`,loot,opened:false});
  }
  for(let i=0;i<5;i++){
    const [ex,ey]=openReach(tiles,ents,r,reach2);
    ents.push({tp:E.KEY,x:ex,y:ey,id:`k_${i}`,item:`Outpost Key ${i+1}`});
  }
  ['Triforce of Power','Triforce of Wisdom','Triforce of Courage'].forEach((nm,i)=>{
    const [ex,ey]=openReach(tiles,ents,r,reach2);
    ents.push({tp:E.TRI,x:ex,y:ey,id:`tri_${i}`,piece:i,item:nm});
  });

  // Boats near shorelines
  let boats=0;
  for(let attempt=0;attempt<3000&&boats<3;attempt++){
    const x=2+Math.floor(r()*(MW-4)),y=2+Math.floor(r()*(MH-4));
    if(!reach2[y][x]) continue;
    if(tiles[y][x]===T.WA||tiles[y][x]===T.TR||tiles[y][x]===T.DT) continue;
    const adj=[[0,1],[0,-1],[1,0],[-1,0]].some(([dx,dy])=>{
      const nx=x+dx,ny=y+dy;
      return nx>=0&&nx<MW&&ny>=0&&ny<MH&&tiles[ny][nx]===T.WA;
    });
    if(!adj||ents.some(e=>e.x===x&&e.y===y)) continue;
    if(Math.abs(x-cx)<=6&&Math.abs(y-cy)<=6) continue;
    ents.push({tp:E.BOAT,x,y,id:`boat_${boats}`});
    boats++;
  }

  // Roaming bokoblin patrols — 4 persistent wanderers placed well away from camp
  const mb=MON[E.BOK];
  for(let i=0;i<4;i++){
    const [rbx,rby]=openReach(tiles,ents,r,reach2);
    if(Math.abs(rbx-cx)<10&&Math.abs(rby-cy)<10) continue; // skip if spawned near camp
    ents.push({
      tp:E.BOK,x:rbx,y:rby,id:`roam_${i}`,name:mb.name,roaming:true,
      hp:mb.hp+2,maxHp:mb.hp+2,atk:mb.atk,def:mb.def,drops:mb.drops,
    });
  }

  return {tiles,ents,cx,cy};
}

function bfs(tiles,sx,sy){
  const vis=Array.from({length:MH},()=>Array(MW).fill(false));
  const q=[[sx,sy]]; vis[sy][sx]=true;
  while(q.length){
    const [x,y]=q.shift();
    for(const [dx,dy] of [[0,1],[0,-1],[1,0],[-1,0]]){
      const nx=x+dx,ny=y+dy;
      if(nx<0||nx>=MW||ny<0||ny>=MH||vis[ny][nx]) continue;
      const t=tiles[ny][nx];
      if(t===T.WA||t===T.TR||t===T.DT||t===T.TH) continue;
      vis[ny][nx]=true; q.push([nx,ny]);
    }
  }
  return vis;
}

function nearestReach(ox,oy,reach,tiles){
  if(ox>=0&&ox<MW&&oy>=0&&oy<MH&&reach[oy][ox]) return [ox,oy];
  for(let rad=1;rad<40;rad++){
    for(let dy=-rad;dy<=rad;dy++) for(let dx=-rad;dx<=rad;dx++){
      if(Math.abs(dx)!==rad&&Math.abs(dy)!==rad) continue;
      const nx=ox+dx,ny=oy+dy;
      if(nx<2||nx>=MW-2||ny<2||ny>=MH-2) continue;
      if(reach[ny][nx]&&tiles[ny][nx]!==T.WA) return [nx,ny];
    }
  }
  return [ox,oy];
}

function clearZone(tiles,cx,cy,rad){
  for(let dy=-rad;dy<=rad;dy++) for(let dx=-rad;dx<=rad;dx++){
    const nx=cx+dx,ny=cy+dy;
    if(nx>=0&&nx<MW&&ny>=0&&ny<MH) tiles[ny][nx]=T.GR;
  }
}

function openReach(tiles,ents,r,reach){
  for(let i=0;i<3000;i++){
    const x=2+Math.floor(r()*(MW-4)),y=2+Math.floor(r()*(MH-4));
    const t=tiles[y][x];
    if(t===T.WA||t===T.TR||t===T.DT) continue;
    if(!reach[y][x]) continue;
    if(ents.some(e=>e.x===x&&e.y===y)) continue;
    if(Math.abs(x-40)<=7&&Math.abs(y-40)<=7) continue;
    return [x,y];
  }
  for(let i=0;i<3000;i++){
    const x=2+Math.floor(r()*(MW-4)),y=2+Math.floor(r()*(MH-4));
    if(tiles[y][x]!==T.WA&&!ents.some(e=>e.x===x&&e.y===y)) return [x,y];
  }
  return [10,10];
}

// ╔══════════════════════════════════════════════════════════╗
// ║                    RENDERING                            ║
// ╚══════════════════════════════════════════════════════════╝
let cvs,ctx,camX=0,camY=0;

const TCOL={[T.GR]:'#274f18',[T.TR]:'#1a4509',[T.DT]:'#0e2a05',
            [T.WA]:'#19366a',[T.ST]:'#444',[T.SA]:'#7a6a3a',[T.TH]:'#1a3306'};
const TEM={[T.TR]:'🌲',[T.DT]:'🌳',[T.ST]:'🪨',[T.TH]:'🌿'};
const EEM={[E.CHEST]:'📦',[E.KEY]:'🗝️',[E.OUTPOST]:'🏰',[E.CAMP]:'⛺',
           [E.TRI]:'🔱',[E.BOAT]:'🚣',[E.BOK]:'👺',[E.KEE]:'🦇',
           [E.SKU]:'🕷️',[E.LIZ]:'🦎',[E.DEER]:'🦌',[E.RAB]:'🐇',[E.FOX]:'🦊',
           [E.GLEEOK]:'🐉',[E.DARKLYNEL]:'🦁',
           [E.CHUCHU]:'🟣',[E.WIZZROBE]:'🧙',[E.DARKKNIGHT]:'🗡️',[E.PHANTOM]:'👻',[E.DESCENT]:'🪜'};

function moveCam(){
  camX=G.pl.x*TS-cvs.width/2+TS/2;
  camY=G.pl.y*TS-cvs.height/2+TS/2;
  camX=Math.max(0,Math.min(camX,MW*TS-cvs.width));
  camY=Math.max(0,Math.min(camY,MH*TS-cvs.height));
}

function draw(){
  if(!cvs||G.screen!=='play') return;
  moveCam();
  const {width:W,height:H}=cvs;
  ctx.clearRect(0,0,W,H);
  const txS=Math.floor(camX/TS),tyS=Math.floor(camY/TS);
  const txE=Math.ceil((camX+W)/TS),tyE=Math.ceil((camY+H)/TS);

  // tiles
  const lvlTCOL=(G&&G.dungeonLevel&&LEVEL_CFG[G.dungeonLevel])?LEVEL_CFG[G.dungeonLevel].TCOL:LEVEL_CFG[1].TCOL;
  const lvlTEM=(G&&G.dungeonLevel&&LEVEL_CFG[G.dungeonLevel])?LEVEL_CFG[G.dungeonLevel].TEM:LEVEL_CFG[1].TEM;
  for(let ty=tyS;ty<tyE&&ty<MH;ty++) for(let tx=txS;tx<txE&&tx<MW;tx++){
    if(tx<0||ty<0) continue;
    const sx=tx*TS-camX,sy=ty*TS-camY;
    const fog=G.fog[ty][tx];
    let col=fog?'#060e06':lvlTCOL[G.map[ty][tx]]||'#274f18';
    ctx.fillStyle=col; ctx.fillRect(sx,sy,TS,TS);
    if(!fog){
      ctx.strokeStyle='rgba(0,0,0,.12)'; ctx.strokeRect(sx,sy,TS,TS);
      const em=lvlTEM[G.map[ty][tx]];
      if(em){ctx.font=`${TS-8}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
             ctx.fillText(em,sx+TS/2,sy+TS/2);}
    }
  }

  // entities
  ctx.textAlign='center'; ctx.textBaseline='middle';
  G.ents.forEach(e=>{
    if(e.gone||e.dead) return;
    if(G.fog[e.y][e.x]) return;
    const sx=e.x*TS-camX+TS/2,sy=e.y*TS-camY+TS/2;
    ctx.shadowBlur=0;
    if(e.tp===E.TRI)          {ctx.shadowColor='#f0c040';ctx.shadowBlur=18;}
    else if(e.tp===E.OUTPOST) {ctx.shadowColor=G.opOpen[e.idx]?'#00ff80':'#ff3040';ctx.shadowBlur=10;}
    else if(e.tp===E.CAMP)    {ctx.shadowColor='#60ff80';ctx.shadowBlur=8;}
    else if(e.tp===E.BOAT)    {ctx.shadowColor='#60b8ff';ctx.shadowBlur=10;}
    else if(e.isFloorBoss)    {ctx.shadowColor='#ffd700';ctx.shadowBlur=35;}
    else if(e.tp===E.DESCENT) {ctx.shadowColor='#00ffff';ctx.shadowBlur=15;}
    else if(e.tp===E.GLEEOK)  {ctx.shadowColor='#ff5500';ctx.shadowBlur=28;}
    else if(e.tp===E.DARKLYNEL){ctx.shadowColor='#aa00ff';ctx.shadowBlur=28;}
    ctx.font=`${TS-4}px serif`;
    ctx.fillText(e.tp===E.CHEST?(e.opened?'📭':'📦'):EEM[e.tp]||'?',sx,sy);
    ctx.shadowBlur=0;
  });

  // player — golden glow during blessing
  const px=G.pl.x*TS-camX+TS/2, py=G.pl.y*TS-camY+TS/2;
  ctx.shadowColor=G.triforceBlessing>0?'#f0c040':G.pl.onWater?'#60b8ff':'#80ff80';
  ctx.shadowBlur=G.triforceBlessing>0?20:12;
  ctx.font=`${TS}px serif`;
  ctx.fillText(G.pl.onWater?'🚣':'🧝',px,py);
  ctx.shadowBlur=0;

  updateHUD();
  drawMinimap();
}

// ── Minimap ─────────────────────────────────────────────────
function drawMinimap(){
  const mc=document.getElementById('minimap');
  if(!mc||!G.map) return;
  const mctx=mc.getContext('2d');
  mc.width=MW*MM_S; mc.height=MH*MM_S;

  // Terrain via ImageData (fast pixel fill)
  const img=mctx.createImageData(MW*MM_S,MH*MM_S);
  const d=img.data;
  const TC=(LEVEL_CFG[G.dungeonLevel||1]||LEVEL_CFG[1]).MMAP||{
    [T.GR]:[39,79,24],[T.TR]:[26,69,9],[T.DT]:[14,42,5],
    [T.WA]:[25,54,106],[T.ST]:[85,85,85],[T.SA]:[122,106,58],[T.TH]:[26,51,6],
  };
  for(let ty=0;ty<MH;ty++) for(let tx=0;tx<MW;tx++){
    const c=G.fog[ty][tx]?[4,8,4]:(TC[G.map[ty][tx]]||TC[T.GR]);
    for(let dy=0;dy<MM_S;dy++) for(let dx=0;dx<MM_S;dx++){
      const i=((ty*MM_S+dy)*(MW*MM_S)+(tx*MM_S+dx))*4;
      d[i]=c[0];d[i+1]=c[1];d[i+2]=c[2];d[i+3]=255;
    }
  }
  mctx.putImageData(img,0,0);

  // Entity dots
  function dot(tx,ty,color,size=3){
    if(G.fog[ty][tx]) return;
    mctx.fillStyle=color;
    const px=tx*MM_S, py=ty*MM_S;
    mctx.fillRect(px-Math.floor(size/2),py-Math.floor(size/2),size,size);
  }

  G.ents.forEach(e=>{
    if(e.gone||e.dead) return;
    if(G.fog[e.y][e.x]) return;
    if(e.tp===E.OUTPOST)       dot(e.x,e.y,G.opOpen[e.idx]?'#00ff80':'#ff4040',5);
    else if(e.tp===E.CAMP)     dot(e.x,e.y,'#00ffcc',5);
    else if(e.tp===E.CHEST&&!e.opened) dot(e.x,e.y,'#f0c040',3);
    else if(e.tp===E.KEY)      dot(e.x,e.y,'#ff8800',3);
    else if(e.tp===E.TRI)      dot(e.x,e.y,'#ffff60',4);
    else if(e.tp===E.BOAT)     dot(e.x,e.y,'#60b8ff',3);
    else if(e.isFloorBoss)     dot(e.x,e.y,'#ffd700',7);
    else if(e.tp===E.DESCENT)  dot(e.x,e.y,'#00ffff',6);
    else if(e.tp===E.GLEEOK)   dot(e.x,e.y,'#ff5500',6);
    else if(e.tp===E.DARKLYNEL)dot(e.x,e.y,'#cc00ff',6);
  });

  // Viewport rectangle
  if(cvs){
    const vpW=Math.floor(cvs.width/TS),vpH=Math.floor(cvs.height/TS);
    const vpX=Math.floor(camX/TS),vpY=Math.floor(camY/TS);
    mctx.strokeStyle='rgba(255,255,255,0.25)';
    mctx.lineWidth=1;
    mctx.strokeRect(vpX*MM_S,vpY*MM_S,vpW*MM_S,vpH*MM_S);
  }

  // Player dot (always on top, always visible)
  const ppx=G.pl.x*MM_S, ppy=G.pl.y*MM_S;
  mctx.fillStyle=G.triforceBlessing>0?'#f0c040':'#ffffff';
  mctx.fillRect(ppx-2,ppy-2,5,5);
}

// ── HUD ─────────────────────────────────────────────────────
function updateHUD(){
  const h=G.time.hour;
  const names=['Midnight','Dead of Night','Dead of Night','Before Dawn','Before Dawn','Dawn',
               'Dawn','Morning','Morning','Midday','Midday','Afternoon','Afternoon','Afternoon',
               'Afternoon','Late Afternoon','Evening','Evening','Dusk','Dusk',
               'Nightfall','Night','Night','Night'];
  const icon=G.time.isNight?'🌙':(h<7||h>18?'🌅':'☀️');
  const lvlCfgNow=LEVEL_CFG[G.dungeonLevel||1]||LEVEL_CFG[1];
  const nightWord=G.time.isNight?lvlCfgNow.nightName:lvlCfgNow.dawnName;
  document.getElementById('timeDisp').textContent=`${icon} Day ${G.time.night+1} · ${nightWord}`;
  const floorEl=document.getElementById('floorDisp');
  if(floorEl) floorEl.textContent=`Floor: ${G.dungeonLevel||1} / 5${G.levelBossDefeated?' ✅':''}`;
  const floorBannerEl=document.getElementById('floorBanner');
  if(floorBannerEl) floorBannerEl.textContent=`${lvlCfgNow.icon} ${lvlCfgNow.name}  |  Floor ${G.dungeonLevel||1}/5${G.levelBossDefeated?' ✅':''}`;
  document.getElementById('rupeeDisp').textContent=`💎 ${G.pl.rupees}`;
  document.getElementById('scoreDisp').textContent=`⭐ ${calcScore().toLocaleString()}`;

  // Triforce blessing + event status in top bar
  const blessed=G.triforceBlessing>0;
  let statusMsg='';
  if(G.bloodMoon&&G.time.isNight)  statusMsg='🔴 BLOOD MOON';
  else if(blessed)                  statusMsg=`🔱 Blessed: ${G.triforceBlessing} nights`;
  else if(G.monsterFrenzy&&G.time.isNight) statusMsg='👹 Frenzy!';
  else if(G.stormActive&&G.time.isNight)   statusMsg='⛈️ Storm';
  else if(G.harvestLeft>0)                 statusMsg=`🌿 Harvest ×${G.harvestLeft}`;
  document.getElementById('blessingDisp').textContent=statusMsg;

  // Night vignette: blood moon = red, blessing = gold, normal = dark blue
  const vig=document.getElementById('nightVig');
  if(G.time.isNight||blessed){
    vig.style.opacity='1';
    if(G.bloodMoon)
      vig.style.background='radial-gradient(ellipse at center,rgba(20,0,0,.1) 20%,rgba(90,0,0,.88) 100%)';
    else if(blessed)
      vig.style.background='radial-gradient(ellipse at center,rgba(30,20,0,.05) 20%,rgba(50,35,0,.55) 100%)';
    else
      vig.style.background='radial-gradient(ellipse at center,rgba(0,0,10,.05) 20%,rgba(0,0,30,.88) 100%)';
  } else {
    vig.style.opacity='0';
  }

  // Golden border when blessed
  document.getElementById('canvasWrap').classList.toggle('blessed',blessed);

  const fill=document.getElementById('timefill');
  fill.style.width=(h/24*100)+'%';
  fill.style.background=G.time.isNight?'#3050d0':(h<8||h>18?'#c08040':'#f0c040');

  document.getElementById('uiName').textContent=G.pl.name;

  let hh='';
  for(let i=0;i<G.pl.maxHp;i+=2){
    const goldHeart=blessed;
    if(G.pl.hp>=i+2)       hh+=`<span class="heart">${goldHeart?'💛':'❤️'}</span>`;
    else if(G.pl.hp===i+1) hh+='<span class="heart">🧡</span>';
    else                    hh+='<span class="heart" style="opacity:.25">🖤</span>';
  }
  document.getElementById('heartsRow').innerHTML=hh;

  // XP bar
  const lvlEl=document.getElementById('uiLevel');
  const xpFill=document.getElementById('xpBarFill');
  const xpTxt=document.getElementById('xpText');
  if(lvlEl) lvlEl.textContent=G.pl.level+(G.pl.level>=10?' ★':'');
  if(xpFill) xpFill.style.width=(G.pl.level>=10?100:Math.min(100,Math.round(G.pl.xp/G.pl.xpCap*100)))+'%';
  if(xpTxt)  xpTxt.textContent=G.pl.level>=10?'MAX LEVEL':`${G.pl.xp} / ${G.pl.xpCap} XP`;

  document.getElementById('eqW').textContent=G.pl.eq.w||(G.pl.atk>1?`ATK ${G.pl.atk}`:'Fists');
  document.getElementById('eqA').textContent=G.pl.eq.a||(G.pl.def>0?`DEF ${G.pl.def}`:'None');
  document.getElementById('invCnt').textContent=G.pl.inv.length;

  const il=document.getElementById('invList');
  il.innerHTML=G.pl.inv.map((nm,i)=>{
    const d=ITEMS[nm]||{ic:'?'};
    const eq=G.pl.eq.w===nm||G.pl.eq.a===nm;
    return `<div class="invItem ${eq?'eq':''}" onclick="quickUse(${i})">${d.ic} <span style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis">${nm}</span></div>`;
  }).join('');

  const tf=G.triforce;
  document.getElementById('tfDisp').textContent=(tf[0]?'🔱':'△')+(tf[1]?'🔱':'△')+(tf[2]?'🔱':'△');
  const bb=document.getElementById('blessingBar');
  if(blessed){
    bb.style.display='block';
    const pct=Math.round((G.triforceBlessing/12)*100);
    bb.innerHTML=`✨ Blessing ${pct}% · +3 ATK · -60% spawns<br>
      <div style="height:4px;background:#1a3a1a;border-radius:2px;margin-top:2px;">
        <div style="height:100%;width:${pct}%;background:#f0c040;border-radius:2px;transition:width .5s"></div>
      </div>`;
  } else { bb.style.display='none'; }

  document.getElementById('opStatus').innerHTML=
    G.opOpen.map((u,i)=>
      `<span style="color:${u?'#00ff80':'#ff6060'}">${u?'🏰✅':'🏰🔒'}</span> <span style="color:${u?'#a0d890':'#a07070'};font-size:6px">${OP_NAMES[i]}</span>`
    ).join('<br>');

  // Mobile compact stats (top bar on small screens)
  const msHp=document.getElementById('msHp');
  const msLv=document.getElementById('msLv');
  const msRup=document.getElementById('msRup');
  const msNight=document.getElementById('msNight');
  if(msHp)    msHp.textContent=`❤️ ${G.pl.hp}/${G.pl.maxHp}`;
  if(msLv)    msLv.textContent=`Lv${G.pl.level}`;
  if(msRup)   msRup.textContent=`💎 ${G.pl.rupees}`;
  if(msNight) msNight.textContent=`⚔️ Fl.${G.dungeonLevel||1}/5`;
}

// ╔══════════════════════════════════════════════════════════╗
// ║                TIME & MOVEMENT                          ║
// ╚══════════════════════════════════════════════════════════╝
function tick(n=1){
  for(let i=0;i<n;i++){
    G.time.acts++;
    if(G.time.acts%ACT_PER_HOUR===0){
      G.time.hour=(G.time.hour+1)%24;
      const was=G.time.isNight;
      G.time.isNight=G.time.hour<DAY_START||G.time.hour>=DAY_END;
      if(!was&&G.time.isNight){
        G.time.night++;
        if(G.triforceBlessing>0) G.triforceBlessing--;
        G.eventCooldown=Math.max(0,G.eventCooldown-1);
        checkNightEvents();
        msg(`🌙 Night ${G.time.night} falls... monsters awaken!`,'md');
        if(G.time.night>=G.totalNights){triggerVictory();return;}
      } else if(was&&!G.time.isNight){
        G.bloodMoon=false; G.monsterFrenzy=false; G.stormActive=false;
        msg(`☀️ Dawn breaks! Day ${G.time.night+1} begins. Safe for now.`,'ms');
        purgeMonsters();
        if(Math.random()<0.28) shiftRivers();
      }
    }
  }
}

function canWalk(x,y){
  if(x<0||x>=MW||y<0||y>=MH) return false;
  const t=G.map[y][x];
  if(t===T.WA) return G.pl.hasBoat;
  return t!==T.TR&&t!==T.DT;
}

function move(dx,dy){
  if(G.screen!=='play'||G.done) return;
  const nx=G.pl.x+dx, ny=G.pl.y+dy;
  if(nx<0||nx>=MW||ny<0||ny>=MH) return;
  const t=G.map[ny][nx];

  if(t===T.TH){
    msg('🌿 Dense thorny thickets block the way! Find another path.','mw');
    draw(); return;
  }
  if(t===T.TR||t===T.DT){
    if(G.pl.hasAxe){
      G.map[ny][nx]=T.GR;
      G.pl.x=nx; G.pl.y=ny;
      reveal(nx,ny,3); tick(2);
      msg(`🪓 You chop down the ${t===T.DT?'mighty':''}tree and push through!`+(Math.random()<.7?' You find some Wood.':''),'mi');
      if(Math.random()<.7) addItem('Wood');
      stepOn();
    } else {
      msg('🌲 A tree blocks the way! Craft or find a Stone Axe to chop through.','mw');
    }
    draw(); return;
  }
  if(t===T.WA&&!G.pl.hasBoat){
    msg('🌊 Water blocks the way! Find a 🚣 Boat near the shoreline to sail.','mw');
    draw(); return;
  }

  G.pl.x=nx; G.pl.y=ny;
  G.pl.onWater=(t===T.WA);
  reveal(nx,ny,3); tick();
  stepOn();
  if(G.time.isNight) trySpawn();
  draw();
}

function reveal(cx,cy,rad){
  // Thunderstorm caps vision to 2 tiles
  if(G&&G.stormActive&&G.time&&G.time.isNight) rad=Math.min(rad,2);
  for(let dy=-rad;dy<=rad;dy++) for(let dx=-rad;dx<=rad;dx++){
    const nx=cx+dx,ny=cy+dy;
    if(nx>=0&&nx<MW&&ny>=0&&ny<MH&&Math.hypot(dx,dy)<=rad) G.fog[ny][nx]=false;
  }
}

// ╔══════════════════════════════════════════════════════════╗
// ║            ENTITY INTERACTIONS                          ║
// ╚══════════════════════════════════════════════════════════╝
function stepOn(){
  G.ents.forEach(e=>{
    if(e.gone||e.dead||e.x!==G.pl.x||e.y!==G.pl.y) return;
    onStep(e);
  });
}

function onStep(e){
  switch(e.tp){
    case E.CAMP: msg('⛺ Back at camp. You feel a little safer here.','mi'); break;
    case E.KEY:
      if(addItem(e.item)){e.gone=true;msg(`🗝️ Found ${e.item}!`,'ms');} break;
    case E.BOAT:
      if(!G.pl.hasBoat){G.pl.hasBoat=true;addItem('Boat');e.gone=true;
        msg('🚣 You found a boat! Walk into water to sail.','ms');} break;
    case E.TRI:
      if(!G.triforce[e.piece]){
        G.triforce[e.piece]=true; addItem(e.item); e.gone=true;
        msg(`🔱 TRIFORCE PIECE FOUND! ${e.item}!`,'mw');
        if(G.triforce.every(t=>t)) triforceComplete();
        else msg(`🔱 ${G.triforce.filter(t=>t).length}/3 pieces — keep searching!`,'mw');
      } break;
    case E.CHEST:
      if(!e.opened){e.opened=true;showChest(e.loot);} break;
    case E.OUTPOST: showOutpost(e); break;
    case E.BOK: case E.KEE: case E.SKU: case E.LIZ:
      case E.CHUCHU: case E.WIZZROBE: case E.DARKKNIGHT: case E.PHANTOM:
      if(!e.dead) startCombat(e); break;
    case E.GLEEOK: case E.DARKLYNEL:
      if(!e.dead) startCombat(e); break;
    case E.DEER: case E.RAB: case E.FOX:
      msg(`A ${e.tp} scampers into the undergrowth!`,'mi'); e.gone=true; break;
    case E.DESCENT:
      if(G.levelBossDefeated){
        if(G.dungeonLevel>=5){ triggerDungeonMaster(); }
        else { descendLevel(); }
      } else {
        msg('🚪 The passage is sealed. Defeat the floor guardian first!','mw');
      }
      break;
  }
}

// ╔══════════════════════════════════════════════════════════╗
// ║          🔱 TRIFORCE COMPLETE EFFECT                    ║
// ╚══════════════════════════════════════════════════════════╝
function triforceComplete(){
  // Activate blessing
  G.triforceBlessing=12;
  G.pl.maxHp=Math.min(G.pl.maxHp+4,20);
  G.pl.hp=G.pl.maxHp; // full heal

  // Flash overlay
  const flash=document.getElementById('triFlash');
  flash.classList.remove('on');
  void flash.offsetWidth; // reflow
  flash.classList.add('on');
  setTimeout(()=>flash.classList.remove('on'),3500);

  msg('✨✨✨ THE TRIFORCE IS COMPLETE! THE GOLDEN POWER IS YOURS! ✨✨✨','mw');

  showO('🔱 TRIFORCE COMPLETE! 🔱',
    `<div style="font-size:48px;margin:8px 0;animation:triPulse 1.5s ease-out">🔱</div>
     <p style="color:#f0c040;font-size:12px;margin:8px 0">THE GOLDEN POWER IS YOURS!</p>
     <p>Din, Nayru, and Farore bless you with their divine power!</p>
     <hr style="border-color:#c09020;margin:10px 0">
     <p>✅ Maximum hearts increased by <span style="color:#f0c040">+2</span></p>
     <p>✅ Fully healed to <span style="color:#f0c040">maximum health</span></p>
     <p>✅ <span style="color:#f0c040">Triforce Blessing</span> active for 12 nights:</p>
     <p style="font-size:7px;color:#c0b060">  ⚔️ +3 bonus ATK in all combat<br>
       👾 60% fewer monster spawns<br>
       🌙 Night vignette turns golden<br>
       💛 Hearts glow with golden power</p>`,
    [{t:'Feel the Power!',f:'closeO()',cls:'btn-tri'}]);
}

// ╔══════════════════════════════════════════════════════════╗
// ║             CHARACTER PROGRESSION                       ║
// ╚══════════════════════════════════════════════════════════╝
function gainXP(n){
  if(!G||G.pl.level>=10) return;
  G.pl.xp+=n;
  while(G.pl.xp>=G.pl.xpCap && G.pl.level<10){
    G.pl.xp-=G.pl.xpCap;
    G.pl.level++;
    G.pl.xpCap=G.pl.level*50;
    showLevelUp();
    return; // pause here — chooseUpgrade will resume
  }
  updateHUD();
}

function showLevelUp(){
  msg(`⬆️ LEVEL UP! Now Level ${G.pl.level}!`,'ms');
  const isMax=G.pl.level>=10;
  if(isMax){
    // Max level: automatic dual bonus
    G.pl.atk++;G.pl.def++;
    msg('★ MAX LEVEL! +1 ATK & +1 DEF awarded!','mw');
    showO('★ MAX LEVEL! ★',
      `<p style="color:#f0c040;font-size:13px">LEVEL 10 REACHED!</p>
       <p>You are a true champion of Hyrule!</p>
       <p>✅ +1 ATK (now ${G.pl.atk}) &nbsp;·&nbsp; ✅ +1 DEF (now ${G.pl.def})</p>`,
      [{t:'Champion!',f:'closeO()',cls:'btn-tri'}]);
    updateHUD();
    return;
  }
  // Milestone level 5: show choice + bonus hint
  const milestone=G.pl.level===5;
  showO(`⬆️ LEVEL UP! Lv ${G.pl.level}`,
    `<p style="color:#60e060">You've grown stronger, hero!</p>
     ${milestone?`<p style="color:#f0c040">🌟 Milestone Level 5!</p>`:''}
     <p>Choose your advancement:</p>`,
    [{t:`⚔️ +1 ATK (${G.pl.atk}→${G.pl.atk+1})`,f:"chooseUpgrade('atk')",cls:'btn-red'},
     {t:`🛡️ +1 DEF (${G.pl.def}→${G.pl.def+1})`,f:"chooseUpgrade('def')"},
     {t:`❤️ +2 Max HP (${G.pl.maxHp}→${G.pl.maxHp+2})`,f:"chooseUpgrade('hp')",cls:'btn-gold'}]);
}

function chooseUpgrade(type){
  if(type==='atk'){G.pl.atk++;msg(`⚔️ ATK increased to ${G.pl.atk}!`,'ms');}
  else if(type==='def'){G.pl.def++;msg(`🛡️ DEF increased to ${G.pl.def}!`,'ms');}
  else if(type==='hp'){
    G.pl.maxHp=Math.min(G.pl.maxHp+2,24);
    G.pl.hp=Math.min(G.pl.hp+2,G.pl.maxHp);
    msg(`❤️ Max HP increased to ${G.pl.maxHp}!`,'ms');
  }
  // Level 5 milestone: extra free bonus
  if(G.pl.level===5){
    G.pl.hp=G.pl.maxHp;
    msg('🌟 Level 5 milestone — fully healed!','ms');
  }
  closeO();
  // Check if another level-up is still pending
  if(G.pl.xp>=G.pl.xpCap && G.pl.level<10){
    G.pl.xp-=G.pl.xpCap;
    G.pl.level++;
    G.pl.xpCap=G.pl.level*50;
    showLevelUp();
    return;
  }
  draw();
}

// Called from victory overlay "Continue" when a level-up was pending
function collectXPAndClose(){
  const xp=G._pendingXP||0;
  G._pendingXP=0;
  closeO();
  if(xp>0) gainXP(xp);
  else draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                 INVENTORY                               ║
// ╚══════════════════════════════════════════════════════════╝
function addItem(nm){
  if(G.pl.inv.length>=20){msg('Inventory full! (20/20) — drop something first.','mw');return false;}
  G.pl.inv.push(nm); return true;
}

function quickUse(i){
  const nm=G.pl.inv[i]; if(!nm) return;
  const d=ITEMS[nm]; if(!d) return;
  if(d.tp==='weapon'){G.pl.eq.w=nm;G.pl.atk=d.atk;G.pl.hasAxe=false;msg(`Equipped ${nm} (ATK +${d.atk}).`,'mi');}
  else if(d.tp==='axe'){G.pl.eq.w=nm;G.pl.atk=d.atk;G.pl.hasAxe=true;msg(`🪓 Stone Axe equipped! Chop trees and fight.`,'ms');}
  else if(d.tp==='armor'){G.pl.eq.a=nm;G.pl.def=d.def;msg(`Equipped ${nm} (DEF +${d.def}).`,'mi');}
  else if(d.tp==='use'){useConsumable(i);}
  else if(d.tp==='boat'){G.pl.hasBoat=true;msg('🚣 Boat ready! Walk into water to sail.','ms');}
  else if(d.tp==='tool'&&nm==='Lantern'){G.pl.hasLantern=true;msg('🏮 Lantern lit! Monsters will be less bold.','ms');}
  else if(d.tp==='tool'&&nm==='Map Fragment'){G.pl.inv.splice(i,1);revealFragment();msg('🗺️ Map fragment revealed a new area!','ms');}
  else{msg(`${nm}: ${d.desc}`,'mi');}
  draw();
}

function useConsumable(i){
  const nm=G.pl.inv[i];const d=ITEMS[nm];
  G.pl.inv.splice(i,1);
  if(d.revive){G.pl.hasFairy=true;msg('🧚 Fairy captured! Auto-revive ready.','ms');}
  else if(d.heal){G.pl.hp=Math.min(G.pl.hp+d.heal,G.pl.maxHp);msg(`Used ${nm}.`,'ms');}
}

function revealFragment(){
  const cx=10+Math.floor(Math.random()*(MW-20));
  const cy=10+Math.floor(Math.random()*(MH-20));
  reveal(cx,cy,7);
}

function dropItem(i){
  const nm=G.pl.inv.splice(i,1)[0];
  if(G.pl.eq.w===nm){G.pl.eq.w=null;G.pl.atk=1;G.pl.hasAxe=false;}
  if(G.pl.eq.a===nm){G.pl.eq.a=null;G.pl.def=0;}
  if(nm==='Boat'){G.pl.hasBoat=false;G.pl.onWater=false;}
  msg(`Dropped ${nm}.`,'mi'); draw();
}

function openInvScreen(){
  if(G.pl.inv.length===0){msg('Your inventory is empty.','mi');return;}
  let html=`<p style="color:#90d878">${G.pl.inv.length}/20 items</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:8px;">`;
  G.pl.inv.forEach((nm,i)=>{
    const d=ITEMS[nm]||{ic:'?',desc:''};
    const eq=G.pl.eq.w===nm||G.pl.eq.a===nm;
    const lbl=d.tp==='weapon'||d.tp==='armor'||d.tp==='axe'?'Equip':d.tp==='use'?'Use':'Use';
    html+=`<div style="background:#0a1a0a;border:1px solid ${eq?'#4090f0':'#2d5a1b'};padding:5px;border-radius:3px;text-align:left;">
      <div style="font-size:9px;">${d.ic} <span style="font-size:7px;color:${eq?'#80c0ff':'#a8c8a8'}">${nm}</span></div>
      <div style="font-size:5px;color:#607060;margin:2px 0">${d.desc}</div>
      <button class="btn" style="font-size:6px;padding:2px 5px;margin-top:2px" onclick="quickUse(${i});closeO()">${lbl}</button>
      <button class="btn btn-red" style="font-size:6px;padding:2px 5px;margin-top:2px" onclick="dropItem(${i});closeO()">Drop</button>
    </div>`;
  });
  html+='</div>';
  showO('🎒 Inventory',html,[{t:'Close',f:'closeO()'}]);
}

// ╔══════════════════════════════════════════════════════════╗
// ║                  CHEST & OUTPOSTS                       ║
// ╚══════════════════════════════════════════════════════════╝
function showChest(loot){
  const d=ITEMS[loot]||{ic:'?',desc:''};
  showO('📦 Chest Opened!',
    `<p>You pry open the old chest and find...</p>
     <p style="font-size:24px;margin:10px 0">${d.ic}</p>
     <p style="color:#f0c040;font-size:10px">${loot}</p>
     <p style="font-size:7px;color:#90c890">${d.desc}</p>`,
    [{t:'Take It!',f:`takeChest('${loot.replace(/'/g,"\\'")}')`,cls:'btn-gold'},{t:'Leave It',f:'closeO()'}]
  );
}
function takeChest(loot){closeO();if(addItem(loot))msg(`Got ${loot} from chest!`,'ms');draw();}

function showOutpost(e){
  const idx=e.idx,nm=OP_NAMES[idx];
  if(!G.opOpen[idx]){
    const key=`Outpost Key ${idx+1}`, has=G.pl.inv.includes(key);
    if(has){
      showO(`🏰 Outpost ${nm}`,`<p>A fortified outpost. You have the ${key}!</p>`,
        [{t:'🗝️ Unlock',f:`unlockOp(${idx})`,cls:'btn-gold'},{t:'Leave',f:'closeO()'}]);
    } else {
      showO(`🏰 Outpost ${nm} (Locked)`,
        `<p>A fortified outpost. The door is locked.</p><p>You need <span style="color:#f0c040">${key}</span> to enter.</p>`,
        [{t:'Leave',f:'closeO()'}]);
    }
  } else { opMenu(idx,nm); }
}

function unlockOp(idx){
  const key=`Outpost Key ${idx+1}`;
  const ki=G.pl.inv.indexOf(key); if(ki>=0) G.pl.inv.splice(ki,1);
  G.opOpen[idx]=true;
  G.ents.find(e=>e.tp===E.OUTPOST&&e.idx===idx).locked=false;
  msg(`🏰 Outpost ${OP_NAMES[idx]} unlocked! A safe refuge secured.`,'ms');
  opMenu(idx,OP_NAMES[idx]);
}

function opMenu(idx,nm){
  showO(`🏰 Outpost ${nm}`,`<p>A safe haven in the cursed forest.</p>`,
    [{t:'💤 Sleep Safely',f:'opSleep()',cls:'btn-gold'},{t:'⚒️ Crafting',f:'openCraft()'},
     {t:'🧙 Merchant',f:'openShop()'},{t:'📜 Lore',f:`readLore(${idx})`},{t:'Leave',f:'closeO()'}]);
}

function opSleep(){
  const was=G.time.isNight; G.time.hour=8; G.time.isNight=false;
  if(was){G.time.night++;if(G.triforceBlessing>0)G.triforceBlessing--;
    msg(`💤 Slept safely! Night ${G.time.night} passed.`,'ms');}
  else msg('💤 You rest and feel refreshed.','mi');
  // Blessing gives full heal at outpost, normal gives partial
  G.pl.hp=Math.min(G.pl.hp+(G.triforceBlessing>0?G.pl.maxHp:4),G.pl.maxHp);
  G.bloodMoon=false; G.monsterFrenzy=false; G.stormActive=false;
  purgeMonsters(); closeO();
  if(G.time.night>=G.totalNights){triggerVictory();return;}
  draw();
}

function readLore(i){
  showO('📜 Ancient Inscription',
    `<p style="font-style:italic;color:#c090f0;line-height:1.9">"${LORE[i%LORE.length]}"</p>`,
    [{t:'Close',f:'closeO()'}]);
}

function openCraft(){
  let html=`<p style="color:#90d878">Combine materials to forge new items.</p>`;
  RECIPES.forEach((rec,i)=>{
    const can=rec.needs.every(n=>G.pl.inv.includes(n));
    const d=ITEMS[rec.result]||{ic:'?'};
    html+=`<div style="border:1px solid #2d5a1b;padding:5px;margin:4px 0;border-radius:3px">
      <div style="font-size:8px;color:${can?'#f0c040':'#506050'}">${d.ic} ${rec.result}</div>
      <div style="font-size:6px;color:#506050">Needs: ${rec.needs.join(' + ')}</div>
      <div style="font-size:5px;color:#708060;margin:1px 0">${rec.desc||''}</div>
      ${can?`<button class="btn btn-gold" style="margin-top:3px;padding:3px 8px" onclick="craft(${i})">Craft!</button>`:'<span style="font-size:5px;color:#405040">Missing materials</span>'}
    </div>`;
  });
  showO('⚒️ Crafting Bench',html,[{t:'Close',f:'closeO()'}]);
}

function craft(i){
  const rec=RECIPES[i];
  rec.needs.forEach(n=>{const j=G.pl.inv.indexOf(n);if(j>=0)G.pl.inv.splice(j,1);});
  if(addItem(rec.result)){msg(`⚒️ Crafted ${rec.result}!`,'ms');gainXP(5);}
  closeO(); draw();
}

function openShop(){
  let html=`<p>A grinning merchant gestures to his wares.</p>
    <p style="color:#00e8ff">💎 ${G.pl.rupees} rupees</p>`;
  SHOP.forEach((s,i)=>{
    const can=G.pl.rupees>=s.price, d=ITEMS[s.name]||{ic:'?'};
    html+=`<div style="border:1px solid #2d5a1b;padding:5px;margin:3px;display:flex;justify-content:space-between;align-items:center;border-radius:3px">
      <span style="font-size:8px">${d.ic} ${s.name}</span>
      <span><span style="font-size:7px;color:#00e8ff">💎${s.price}</span>
      ${can?`<button class="btn btn-gold" style="padding:2px 8px;margin-left:4px" onclick="buy(${i})">Buy</button>`:''}</span>
    </div>`;
  });
  showO('🧙 Wandering Merchant',html,[{t:'Leave',f:'closeO()'}]);
}

function buy(i){
  const s=SHOP[i];
  if(G.pl.rupees<s.price){msg('Not enough rupees!','mw');return;}
  if(addItem(s.name)){
    G.pl.rupees-=s.price; msg(`Bought ${s.name} for 💎${s.price}!`,'ms');
    if(s.name==='Boat') G.pl.hasBoat=true;
    if(s.name==='Lantern') G.pl.hasLantern=true;
  }
  closeO(); openShop();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                    COMBAT                               ║
// ╚══════════════════════════════════════════════════════════╝
function startCombat(e){G.combat=e;G.combatRound=0;G.screen='combat';showCombat();}

function showCombat(){
  const e=G.combat;
  const isBoss=e.isBoss;
  const mb=isBoss?(BOSSES[e.bossType]||{ic:'👹',name:'Boss'}):(MON[e.tp]||{ic:'👹',name:'Monster'});
  const blessBonus=G.triforceBlessing>0?3:0;
  const pAtk=G.pl.atk+blessBonus;

  // Boss HP bar
  const bossBar=isBoss?`
    <div style="margin:4px 0 6px">
      <div style="font-size:6px;color:#ff8040;margin-bottom:2px">BOSS HP: ${e.hp} / ${e.maxHp}</div>
      <div style="height:9px;background:#1a0000;border:1px solid #7a1010;border-radius:4px">
        <div style="height:100%;width:${Math.max(0,Math.round(e.hp/e.maxHp*100))}%;
          background:linear-gradient(90deg,#c02020,#ff6040);border-radius:4px;transition:width .3s"></div>
      </div>
    </div>`:'';

  // Special-move warning (shows when NEXT round will be a special)
  const sp=mb.special;
  const nextRoundSpecial=sp&&G.combatRound>0&&(G.combatRound%sp.every===sp.every-1);
  const spWarn=nextRoundSpecial?
    `<div style="font-size:7px;color:#ff3030;margin-top:4px;animation:glowBtn .7s ease-in-out infinite">
       ⚠️ ${sp.warn}</div>`:'';

  const roundLine=isBoss?
    `<div style="font-size:6px;color:#c08040;margin-top:3px">Round ${G.combatRound+1}${nextRoundSpecial?' — ⚠️ SPECIAL NEXT':''}</div>`:'';

  showO(`${isBoss?'💥 BOSS BATTLE: ':'⚔️ '}${mb.ic} ${e.name}`,
    `${bossBar}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0">
      <div style="background:#0a2a0a;padding:7px;border-radius:4px;border:1px solid #2d7a2d">
        <div style="font-size:9px;color:#78e878">🧝 ${G.pl.name}</div>
        <div style="font-size:7px;margin-top:3px">❤️ ${G.pl.hp}/${G.pl.maxHp}</div>
        <div style="font-size:7px">⚔️${pAtk}${blessBonus?` <span style="color:#f0c040">(+${blessBonus}🔱)</span>`:''} 🛡️${G.pl.def}</div>
      </div>
      <div style="background:#2a0a0a;padding:7px;border-radius:4px;border:1px solid #7a2d2d">
        <div style="font-size:9px;color:#e87878">${mb.ic} ${e.name}</div>
        <div style="font-size:7px;margin-top:3px">💀 ${e.hp}/${e.maxHp}</div>
        <div style="font-size:7px">⚔️${e.atk} 🛡️${e.def}</div>
      </div>
    </div>
    ${roundLine}${spWarn}
    <div style="font-size:7px;color:#f0c040;margin-top:3px">Night ${G.time.night}${G.triforceBlessing>0?' — 🔱 BLESSED':''}</div>`,
    [{t:'⚔️ Attack',f:'cAttack()',cls:'btn-red'},{t:'🛡️ Defend',f:'cDefend()'},
     {t:'🧪 Heal',f:'cHeal()'},{t:'💨 Flee',f:'cFlee()'}]);
}

function d6(){return 1+Math.floor(Math.random()*6);}

function cAttack(){
  const e=G.combat;
  G.combatRound++;
  const bonus=G.triforceBlessing>0?3:0;
  const pr=d6()+G.pl.atk+bonus, pd=Math.max(0,pr-e.def);
  e.hp-=pd;
  // DIN'S FIRE: instant kill on non-bosses
  if(G.cheats.din&&!e.isBoss) e.hp=0;
  let m=`You roll 🎲${pr-G.pl.atk-bonus}+${G.pl.atk+bonus}→${pd} dmg to ${e.name}!${G.cheats.din&&!e.isBoss?' 🔥 Din\'s Fire!':''}`;
  if(e.hp<=0){winCombat(e,m);return;}

  // Determine enemy counter-attack (boss special or normal)
  let ed=0;
  const isBoss=e.isBoss;
  const sp=isBoss?(BOSSES[e.bossType]||{}).special:null;
  const doSpecial=sp&&(G.combatRound%sp.every===0);

  if(doSpecial){
    if(sp.type==='flame'){
      // Flame Breath: fixed damage, ignores DEF entirely
      ed=sp.dmg;
      m+=` | 🔥 ${sp.name}! Fixed ${ed} dmg — no shield blocks this!`;
    } else if(sp.type==='spin'){
      // Berserker Spin: two separate hits, each reduced by DEF
      const h1=Math.max(0,d6()+e.atk-G.pl.def);
      const h2=Math.max(0,d6()+e.atk-G.pl.def);
      ed=h1+h2;
      m+=` | 🌀 ${sp.name}! DOUBLE HIT ${h1}+${h2}=${ed} dmg!`;
    }
  } else {
    ed=Math.max(0,d6()+e.atk-G.pl.def);
    m+=` | ${e.name} hits for ${ed}!`;
  }

  const finalEd=G.cheats.nayru?0:ed;
  G.pl.hp-=finalEd;
  msg(m+(G.cheats.nayru?' 🛡️ Nayru protects you!':''),'md');
  if(G.pl.hp<=0){loseCombat();return;}
  showCombat();
}

function cDefend(){
  const e=G.combat;
  const er=d6()+e.atk;
  let ed=Math.max(0,er-G.pl.def-3);
  if(G.cheats.nayru) ed=0;
  G.pl.hp-=ed;
  msg(`You brace! ${e.name} hits for ${ed} dmg (partially blocked).${G.cheats.nayru?' 🛡️ Nayru protects you!':''}`,'mi');
  if(G.pl.hp<=0){loseCombat();return;}
  showCombat();
}

function cHeal(){
  const pi=G.pl.inv.findIndex(n=>(ITEMS[n]||{}).heal>0);
  if(pi<0){msg('No healing items!','mw');showCombat();return;}
  useConsumable(pi);
  const e=G.combat, er=d6()+e.atk;
  const ed=G.cheats.nayru?0:Math.max(0,er-G.pl.def);
  G.pl.hp=Math.max(0,G.pl.hp-ed);
  msg(`You healed! But ${e.name} attacks for ${ed}!${G.cheats.nayru?' 🛡️ Nayru protects you!':''}`,'mw');
  if(G.pl.hp<=0){loseCombat();return;}
  showCombat();
}

function cFlee(){
  const ename=G.combat?G.combat.name:'monster';
  if(Math.random()<0.45+Math.floor(G.time.night/5)*0.04){
    G.pl.x=Math.max(1,Math.min(MW-2,G.pl.x+(Math.random()<.5?-3:3)));
    G.pl.y=Math.max(1,Math.min(MH-2,G.pl.y+(Math.random()<.5?-3:3)));
    // Bosses regenerate to full HP if you flee — no free chip damage!
    const fled=G.combat;
    if(fled&&fled.isBoss){ fled.hp=fled.maxHp; }
    G.screen='play'; G.combat=null; closeO();
    msg(`You fled from the ${ename}!${fled&&fled.isBoss?' The boss recovers to full HP!':''}`,'mw');
  } else {
    const e=G.combat, er=d6()+e.atk, ed=Math.max(0,er-G.pl.def);
    G.pl.hp=Math.max(0,G.pl.hp-ed);
    msg(`Failed to flee! ${ename} strikes for ${ed}!`,'md');
    if(G.pl.hp<=0){loseCombat();return;}
    showCombat();
  }
}

function winCombat(e,lastMsg){
  e.dead=true;
  const isBoss=e.isBoss;
  const mb=isBoss?(BOSSES[e.bossType]||{rMin:0,rMax:5,drops:[],xp:0}):(MON[e.tp]||{rMin:0,rMax:5,drops:[],xp:0});
  const rp=(mb.rMin||0)+Math.floor(Math.random()*((mb.rMax||5)-(mb.rMin||0)));
  G.pl.rupees+=rp;
  const drops=mb.drops||[];
  const drop=drops[Math.floor(Math.random()*drops.length)];
  const gotDrop=drop&&Math.random()<(isBoss?0.90:0.55);
  if(gotDrop) addItem(drop);
  const xpGain=mb.xp||0;
  const willLevel=G.pl.level<10&&(G.pl.xp+xpGain)>=G.pl.xpCap;
  G._pendingXP=(G._pendingXP||0)+xpGain;
  msg(`${lastMsg} → VICTORY! +💎${rp}${gotDrop?` + ${drop}`:''}${xpGain?` +${xpGain}XP`:''}!`,'ms');
  G.screen='play'; G.combat=null;
  // Check if the defeated enemy was the floor boss
  if(e.isFloorBoss && e.id===G.levelBossId){
    G.levelBossDefeated=true;
    // Spawn descent portal at boss location
    G.ents.push({tp:E.DESCENT, x:e.x, y:e.y, id:`descent_${G.dungeonLevel}`, gone:false});
    msg(`🎉 FLOOR GUARDIAN DEFEATED! A descent portal has appeared!`,'ms');
  }
  if(e.isFloorBoss && G.dungeonLevel===5 && e.id===G.levelBossId){
    // Special: final boss triggers Dungeon Master ending
    setTimeout(()=>triggerDungeonMaster(), 1500);
  }
  const bossHeader=isBoss?`<p style="color:#ff8040;font-size:11px">⚔️ BOSS DEFEATED! ⚔️</p>`:'';
  showO(isBoss?'🏆 BOSS DEFEATED!':'⚔️ Victory!',
    `${bossHeader}
     <p style="color:#60ff60;font-size:${isBoss?12:11}px">You defeated the ${e.name}!</p>
     <p>+💎${rp} Rupees${gotDrop?`<br>${ITEMS[drop]?.ic||''} ${drop} dropped!`:''}</p>
     ${xpGain?`<p style="color:#60a0ff">✨ +${xpGain} XP${willLevel?' — LEVEL UP READY!':''}</p>`:''}`,
    [{t:willLevel?'⬆️ Level Up!':'Continue',f:'collectXPAndClose()',cls:willLevel?'btn-tri':'btn-gold'}]);
  draw();
}

function loseCombat(){
  G.screen='play'; G.combat=null;
  if(G.pl.hasFairy){
    G.pl.hasFairy=false; G.pl.hp=Math.ceil(G.pl.maxHp/2);
    msg('🧚 A Fairy revived you! Half health restored!','ms');
    closeO(); draw(); return;
  }
  G.pl.x=40; G.pl.y=40; G.pl.onWater=false;
  G.pl.hp=Math.ceil(G.pl.maxHp/3);
  G.time.night=Math.min(G.time.night+1,G.totalNights-1);
  G.time.hour=8; G.time.isNight=false;
  const dropped=G.pl.inv.splice(0,Math.min(2,G.pl.inv.length));
  purgeMonsters(); reveal(40,40,4);
  showO('💀 You Fell!',
    `<p>Darkness claimed you... you wake at camp.</p>
     <p style="color:#f07878">Night: ${G.time.night}/${G.totalNights}</p>
     ${dropped.length?`<p style="color:#a07040">Dropped: ${dropped.join(', ')}</p>`:''}`,
    [{t:'Rise & Survive!',f:'closeO()',cls:'btn-gold'}]);
  msg(`💀 Defeated! Camp. Night: ${G.time.night}/${G.totalNights}. Lost: ${dropped.join(', ')||'nothing'}.`,'md');
  draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║             MONSTER SPAWNING                            ║
// ╚══════════════════════════════════════════════════════════╝
function trySpawn(){
  if(!G.time.isNight) return;
  const dm=DIFF_MULT[G.diff]||DIFF_MULT.normal;
  let chance=Math.min(0.06+G.time.night*0.0025,0.20)*dm[2];
  if(G.pl.hasLantern)      chance*=0.45;
  if(G.triforceBlessing>0) chance*=0.40;
  if(G.bloodMoon)          chance*=2.0;   // blood moon doubles spawns
  if(G.monsterFrenzy)      chance*=1.75;  // frenzy boosts spawns
  if(Math.random()>chance) return;
  const n=G.time.night;
  const lvlPool=(LEVEL_CFG[G.dungeonLevel||1]||LEVEL_CFG[1]).monPool;
  const pool=lvlPool;
  const tp=pool[Math.floor(Math.random()*pool.length)];
  const mb=MON[tp]||MON[E.BOK];
  const scale=(1+n*0.03)*dm[0], atkS=(1+n*0.02)*dm[1];
  const ang=Math.random()*Math.PI*2, dist=3+Math.floor(Math.random()*3);
  let ex=Math.round(G.pl.x+Math.cos(ang)*dist);
  let ey=Math.round(G.pl.y+Math.sin(ang)*dist);
  ex=Math.max(1,Math.min(MW-2,ex)); ey=Math.max(1,Math.min(MH-2,ey));
  if(G.map[ey][ex]===T.WA||G.map[ey][ex]===T.TR||G.map[ey][ex]===T.DT||G.map[ey][ex]===T.TH) return;
  G.ents.push({tp,x:ex,y:ey,id:`m_${Date.now()}_${Math.random()}`,name:mb.name,
    hp:Math.max(1,Math.ceil(mb.hp*scale)),maxHp:Math.max(1,Math.ceil(mb.hp*scale)),
    atk:Math.max(1,Math.ceil(mb.atk*atkS)),def:Math.ceil(mb.def*scale),drops:mb.drops});
  reveal(ex,ey,2);
  msg(`👹 A ${mb.name} ${mb.ic} emerges from the shadows!`,'md');
}

function purgeMonsters(){
  G.ents=G.ents.filter(e=>{
    // Roaming bokoblins and bosses persist through dawn
    if(e.roaming||e.isBoss||e.isFloorBoss) return true;
    // Regular monsters disappear at dawn unless very close to player
    if([E.BOK,E.KEE,E.SKU,E.LIZ,E.CHUCHU,E.WIZZROBE,E.DARKKNIGHT,E.PHANTOM].includes(e.tp))
      return Math.abs(e.x-G.pl.x)+Math.abs(e.y-G.pl.y)<3;
    return true;
  });
}

function shiftRivers(){
  const SAFE_DIST=7; // stay clear of camp center (40,40)
  const entTiles=new Set(G.ents.filter(e=>!e.dead&&!e.gone).map(e=>`${e.x},${e.y}`));
  const DIRS=[[0,1],[0,-1],[1,0],[-1,0]];

  // Tiles where water could recede (water adjacent to walkable land)
  const recede=[];
  // Tiles where water could advance (walkable land adjacent to water, not near camp/outpost)
  const advance=[];

  for(let ty=2;ty<MH-2;ty++) for(let tx=2;tx<MW-2;tx++){
    if(Math.abs(tx-40)<SAFE_DIST&&Math.abs(ty-40)<SAFE_DIST) continue; // protect camp area
    if(entTiles.has(`${tx},${ty}`)) continue; // never shift under an entity
    if(tx===G.pl.x&&ty===G.pl.y) continue;   // never shift under player

    const t=G.map[ty][tx];
    const hasAdj=(testT)=>DIRS.some(([dx,dy])=>{
      const nx=tx+dx,ny=ty+dy;
      return nx>=0&&nx<MW&&ny>=0&&ny<MH&&G.map[ny][nx]===testT;
    });

    if(t===T.WA&&hasAdj(T.GR)) recede.push([tx,ty]);
    if((t===T.GR||t===T.SA)&&hasAdj(T.WA)) advance.push([tx,ty]);
  }

  // Shuffle and pick 2–4 of each
  const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  const n=2+Math.floor(Math.random()*3);
  let shifted=false;

  shuffle(recede).slice(0,n).forEach(([tx,ty])=>{G.map[ty][tx]=T.SA; shifted=true;});
  shuffle(advance).slice(0,n).forEach(([tx,ty])=>{G.map[ty][tx]=T.WA; shifted=true;});

  if(shifted){
    // If the player is now standing in water without a boat, nudge them to adjacent land
    if(G.map[G.pl.y][G.pl.x]===T.WA&&!G.pl.hasBoat){
      for(const [dx,dy] of DIRS){
        const nx=G.pl.x+dx,ny=G.pl.y+dy;
        if(nx>=0&&nx<MW&&ny>=0&&ny<MH){
          const nt=G.map[ny][nx];
          if(nt!==T.WA&&nt!==T.TR&&nt!==T.DT&&nt!==T.TH){G.pl.x=nx;G.pl.y=ny;break;}
        }
      }
      msg('🌊 The river shifted and swept you to shore!','md');
    } else {
      msg('🌊 Overnight the river has shifted — find new paths!','mw');
    }
  }
}

// ╔══════════════════════════════════════════════════════════╗
// ║           NIGHT EVENTS & BOSS SPAWNING                  ║
// ╚══════════════════════════════════════════════════════════╝
function checkNightEvents(){
  const night=G.time.night;
  if(night<=0) return;

  // ── Blood Moon (pre-scheduled) ───────────────────────────
  G.bloodMoon=G.bloodMoonNights.includes(night);
  if(G.bloodMoon){
    msg('🔴 THE BLOOD MOON RISES! Monsters are frenzied!','md');
    showO('🔴 BLOOD MOON!',
      `<div style="font-size:36px;margin:6px 0">🌕</div>
       <p style="color:#ff4040;font-size:11px">THE BLOOD MOON RISES!</p>
       <p>Ancient evil surges through the dungeon!</p>
       <p style="color:#f08080;font-size:7px">
         ⚠️ Monster spawn rate doubled<br>
         ⚠️ Monsters drop extra rupees<br>
         ⚠️ The sky runs crimson until dawn</p>`,
      [{t:'Face the Night!',f:'closeO()',cls:'btn-red'}]);
  }

  // ── Random events (~35% chance, 2-night cooldown, skip blood moons) ──
  if(!G.bloodMoon && G.eventCooldown===0 && Math.random()<0.35){
    rollRandomEvent();
    G.eventCooldown=2;
  }
}

function spawnFloorBoss(){
  const lvl=G.dungeonLevel;
  const cfg=LEVEL_CFG[lvl];
  if(!cfg) return;
  const bb=BOSSES[cfg.bossType];
  if(!bb) return;
  let bx,by,found=false;
  for(let attempt=0;attempt<500;attempt++){
    const ang=Math.random()*Math.PI*2, dist=20+Math.floor(Math.random()*18);
    bx=Math.round(40+Math.cos(ang)*dist);
    by=Math.round(40+Math.sin(ang)*dist);
    bx=Math.max(4,Math.min(MW-5,bx)); by=Math.max(4,Math.min(MH-5,by));
    const t=G.map[by][bx];
    if(t!==T.WA&&t!==T.TR&&t!==T.DT&&t!==T.TH){ found=true; break; }
  }
  if(!found){bx=35;by=15;}
  const bossId=`floorboss_${lvl}`;
  G.ents=G.ents.filter(e=>e.id!==bossId);
  G.ents.push({
    tp: E.GLEEOK, // reuse GLEEOK entity type for rendering glow; we'll differentiate by isBoss+bossType
    x:bx, y:by, id:bossId,
    name:bb.name, isBoss:true, isFloorBoss:true, bossType:cfg.bossType,
    hp:bb.hp, maxHp:bb.hp, atk:bb.atk, def:bb.def,
    drops:bb.drops, xp:bb.xp, rMin:bb.rMin||40, rMax:bb.rMax||80,
  });
  G.levelBossId=bossId;
  G.levelBossDefeated=false;
  msg(`⚠️ The floor guardian ${bb.ic} ${bb.name} lurks somewhere on this floor!`,'md');
}

function spawnBoss(type){
  const bb=BOSSES[type];
  // Find a walkable tile well away from camp
  let bx,by,found=false;
  for(let attempt=0;attempt<500;attempt++){
    const ang=Math.random()*Math.PI*2, dist=18+Math.floor(Math.random()*20);
    bx=Math.round(40+Math.cos(ang)*dist);
    by=Math.round(40+Math.sin(ang)*dist);
    bx=Math.max(3,Math.min(MW-4,bx)); by=Math.max(3,Math.min(MH-4,by));
    const t=G.map[by][bx];
    if(t!==T.WA&&t!==T.TR&&t!==T.DT){ found=true; break; }
  }
  if(!found){bx=35;by=15;}
  G.ents.push({
    tp: type==='gleeok'?E.GLEEOK:E.DARKLYNEL,
    x:bx, y:by, id:`boss_${type}`,
    name:bb.name, isBoss:true, bossType:type,
    hp:bb.hp, maxHp:bb.hp, atk:bb.atk, def:bb.def,
    drops:bb.drops, xp:bb.xp, rMin:bb.rMin, rMax:bb.rMax,
  });
  msg(`⚠️ ${bb.ic} THE ${bb.name.toUpperCase()} HAS APPEARED somewhere in the forest!`,'md');
  showO(`⚠️ ${bb.ic} BOSS ALERT!`,
    `<p style="color:#ff8040;font-size:11px">${bb.ic} ${bb.name} has emerged!</p>
     <p>A fearsome boss now stalks the forest.</p>
     <p style="font-size:7px;color:#c09060">It appears on your minimap as a large orange/purple dot.<br>
     Defeat it for legendary loot and a massive XP bonus!</p>
     <p style="font-size:7px;color:#a07070">⚠️ It is very powerful — come prepared!</p>`,
    [{t:'Hunt It!',f:'closeO()',cls:'btn-red'},{t:'Later...',f:'closeO()'}]);
}

function rollRandomEvent(){
  const events=['traveller','cache','star','storm','harvest','frenzy'];
  triggerEvent(events[Math.floor(Math.random()*events.length)]);
}

function triggerEvent(id){
  G.stormActive=false; G.harvestLeft=0; G.monsterFrenzy=false;
  switch(id){
    case 'traveller': evtTraveller(); break;
    case 'cache':     evtCache();     break;
    case 'star':      evtStar();      break;
    case 'storm':     evtStorm();     break;
    case 'harvest':   evtHarvest();   break;
    case 'frenzy':    evtFrenzy();    break;
  }
}

function evtTraveller(){
  const items=['Red Potion','Stamella Shroom','Arrows (5)','Wood','Stone','Berries','Wooden Shield'];
  const gift=items[Math.floor(Math.random()*items.length)];
  const rp=5+Math.floor(Math.random()*16);
  const d=ITEMS[gift]||{ic:'?'};
  G.pl.rupees+=rp; addItem(gift);
  showO('👤 Lost Traveller',
    `<p>A weary traveller stumbles out of the darkness.</p>
     <p style="font-style:italic;color:#c0d0c0">"Thank the goddesses — company! Take this..."</p>
     <p style="color:#f0c040;font-size:10px">${d.ic} ${gift} + 💎${rp}</p>`,
    [{t:'Thank Them!',f:'closeO()',cls:'btn-gold'}]);
  msg(`👤 Lost Traveller gave you ${gift} and 💎${rp}!`,'ms');
}

function evtCache(){
  const pool=['Wood','Stone','Red Potion','Arrows (5)','Stamella Shroom','Monster Fang','Berries'];
  let placed=0;
  for(let i=0;i<3&&placed<2;i++){
    const ang=Math.random()*Math.PI*2, dist=2+Math.floor(Math.random()*4);
    let ex=Math.round(G.pl.x+Math.cos(ang)*dist);
    let ey=Math.round(G.pl.y+Math.sin(ang)*dist);
    ex=Math.max(1,Math.min(MW-2,ex)); ey=Math.max(1,Math.min(MH-2,ey));
    const t=G.map[ey][ex];
    if(t===T.WA||t===T.TR||t===T.DT) continue;
    const loot=pool[Math.floor(Math.random()*pool.length)];
    G.ents.push({tp:E.CHEST,x:ex,y:ey,id:`ev_cache_${Date.now()}_${i}`,loot,opened:false});
    reveal(ex,ey,2); placed++;
  }
  showO('📦 Abandoned Cache',
    `<p>You spot something glinting in the undergrowth...</p>
     <p style="color:#f0c040">Supplies hidden nearby — search the area!</p>`,
    [{t:'Search!',f:'closeO()',cls:'btn-gold'}]);
  msg('📦 Abandoned Cache spotted nearby!','ms');
}

function evtStar(){
  const rp=20+Math.floor(Math.random()*31);
  G.pl.rupees+=rp;
  showO('🌠 Shooting Star!',
    `<p>A brilliant streak of light crosses the sky.</p>
     <p style="color:#f0c040;font-size:11px">Fortune smiles: +💎${rp} rupees!</p>`,
    [{t:'Make a Wish!',f:'closeO()',cls:'btn-gold'}]);
  msg(`🌠 A shooting star grants you 💎${rp}!`,'ms');
}

function evtStorm(){
  G.stormActive=true;
  showO('⛈️ Thunderstorm!',
    `<p style="color:#8080ff">Lightning crackles through the canopy!</p>
     <p>The storm limits your sight to <span style="color:#f0c040">2 tiles</span> tonight.</p>
     <p style="font-size:7px;color:#a0a0f0">Find shelter or move carefully...</p>`,
    [{t:'Hunker Down',f:'closeO()'}]);
  msg('⛈️ Thunderstorm! Vision limited to 2 tiles tonight.','mw');
}

function evtHarvest(){
  G.harvestLeft=3;
  showO('🌿 Bountiful Harvest!',
    `<p style="color:#60e060">Nature is generous tonight!</p>
     <p>Your next <span style="color:#f0c040">3 forages</span> are guaranteed finds!</p>`,
    [{t:'Start Foraging!',f:'closeO()',cls:'btn-gold'}]);
  msg('🌿 Bountiful Harvest! Next 3 forages guaranteed!','ms');
}

function evtFrenzy(){
  G.monsterFrenzy=true;
  showO('👹 Monster Frenzy!',
    `<p style="color:#ff8040">A dark presence stirs in the forest!</p>
     <p>Monster spawn rate is <span style="color:#ff4040">×1.75</span> until dawn!</p>`,
    [{t:'Stay Vigilant!',f:'closeO()',cls:'btn-red'}]);
  msg('👹 Monster Frenzy! Monsters rampage until dawn!','md');
}

// ╔══════════════════════════════════════════════════════════╗
// ║               ACTION BUTTONS                            ║
// ╚══════════════════════════════════════════════════════════╝
function doForage(){
  if(G.screen!=='play'||G.done) return;
  if(G.pl.onWater){msg('🌊 Cannot forage while sailing!','mw');return;}
  tick(2);
  const pool=['Berries','Berries','Berries','Stamella Shroom','Wood','Wood','Stone','Monster Fang','Keese Wing'];
  const guaranteed=G.harvestLeft>0;
  if(guaranteed) G.harvestLeft--;
  if(guaranteed||Math.random()<0.68){
    const f=pool[Math.floor(Math.random()*pool.length)];
    if(addItem(f)){
      msg(`🌿 Found ${ITEMS[f]?.ic||''} ${f}!${guaranteed?' (Bountiful Harvest)':''}` ,'ms');
      gainXP(3);
    }
  } else msg('🌿 Nothing useful here.','mi');
  if(Math.random()<0.22){const rp=1+Math.floor(Math.random()*6);G.pl.rupees+=rp;msg(`💎${rp} rupees!`,'ms');}
  if(G.time.isNight) trySpawn();
  draw();
}

function doRest(){
  if(G.screen!=='play'||G.done) return;
  if(G.pl.onWater){msg('🌊 Cannot rest while on water!','mw');return;}
  if(G.time.isNight) msg('⚠️ Resting at night is risky — monsters may find you!','mw');
  tick(3); G.pl.hp=Math.min(G.pl.hp+2,G.pl.maxHp);
  msg('💤 You rest and recover 1 heart.','mi');
  if(G.time.isNight) trySpawn();
  draw();
}

function doLook(){
  if(G.screen!=='play'||G.done) return;
  reveal(G.pl.x,G.pl.y,5); tick();
  const nearby=G.ents.filter(e=>!e.gone&&!e.dead&&Math.abs(e.x-G.pl.x)+Math.abs(e.y-G.pl.y)<=5);
  if(!nearby.length) msg('👁️ The forest stretches endlessly around you...','mi');
  else msg(`👁️ Nearby: ${nearby.map(e=>EEM[e.tp]+' '+e.tp).join(', ')}`,G.time.isNight?'md':'mi');
  if(G.time.isNight) msg('🌙 The shadows writhe. Stay alert!','md');
  draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                   VICTORY                               ║
// ╚══════════════════════════════════════════════════════════╝
function triggerVictory(){
  G.done=true; G.screen='win';
  const finalScore=saveScore();
  const tc=G.triforce.filter(t=>t).length, oc=G.opOpen.filter(u=>u).length;
  const dm=DIFF_MULT[G.diff]||DIFF_MULT.normal;
  showO('🚁 RESCUE!',
    `<div style="font-size:36px;margin:8px 0">🚁</div>
     <p style="color:#f0e860;font-size:12px">YOU SURVIVED ${G.totalNights} NIGHTS!</p>
     <p>The rescue helicopter descends through the canopy!</p>
     <p>Hero: <span style="color:#f0c040">${G.pl.name}</span>
        (${G.diff} difficulty)</p>
     <hr style="border-color:#2d5a1b;margin:8px 0">
     <p>🔱 Triforce: ${tc}/3 ${tc===3?'🏆 COMPLETE!':''}</p>
     <p>🏰 Outposts: ${oc}/5 unlocked</p>
     <p>💎 Rupees: ${G.pl.rupees}</p>
     <hr style="border-color:#c09020;margin:8px 0">
     <p style="font-size:11px;color:#f0c040">⭐ FINAL SCORE: ${finalScore.toLocaleString()}</p>
     <p style="font-size:7px;color:#a0b890">(Nights×50 + Rupees + Triforce + Outposts) × ${dm[3]}x</p>
     <p style="font-size:6px;color:#90a890;margin-top:6px">Score saved to leaderboard!</p>`,
    [{t:'▶️ New Game',f:'restartGame()',cls:'btn-gold'}]);
  msg(`🚁 RESCUED! Score: ${finalScore.toLocaleString()}`,'mw');
}

function restartGame(){
  G=null;
  closeO();
  document.getElementById('app').style.display='none';
  document.getElementById('nameScreen').style.display='flex';
  document.getElementById('nameInput').value='';
  renderLeaderboard();
}

function triggerDungeonMaster(){
  G.done=true;
  saveScore();
  showO('👑 DUNGEON MASTER! 👑',
    `<div style="font-size:48px;margin:8px 0;animation:triPulse 1.5s ease-out infinite">👑</div>
     <p style="color:#f0c040;font-size:12px;margin:8px 0">YOU ARE THE DUNGEON MASTER!</p>
     <p>The Dark Lord has fallen. The dungeon trembles and bows before you.</p>
     <p>All five floors have been conquered. The cursed dungeon is yours.</p>
     <p style="color:#60e8ff">Final Score: ${calcScore().toLocaleString()}</p>`,
    [{t:'🏆 Submit Score', f:'saveScore();renderLeaderboard();closeO()', cls:'btn-tri'},
     {t:'▶️ New Game',     f:'restartGame()',                            cls:'btn-gold'}]);
  msg('👑 YOU ARE THE DUNGEON MASTER! The dark power is yours!','mw');
}

function descendLevel(){
  const nextLevel=G.dungeonLevel+1;
  if(nextLevel>5){
    // Should not happen — final victory is triggered on boss defeat
    triggerDungeonMaster();
    return;
  }
  const cfg=LEVEL_CFG[nextLevel];
  showO(`⬇️ Descending to Floor ${nextLevel}`,
    `<div style="font-size:32px;margin:8px 0">${cfg.icon}</div>
     <p style="color:#f0c040;font-size:11px">${cfg.name}</p>
     <p>${cfg.desc}</p>
     <p style="color:#60e8ff;font-size:7px">Your stats and inventory carry forward.<br>The floor guardian awaits...</p>`,
    [{t:`⬇️ Descend to Floor ${nextLevel}`, f:'doDescend()', cls:'btn-gold'}]);
}

function doDescend(){
  const nextLevel=G.dungeonLevel+1;
  G.dungeonLevel=nextLevel;
  G.levelBossDefeated=false;
  G.levelBossId=null;
  // Regen the map but keep player stats
  const savedPl={...G.pl};
  const savedTriforce=[...G.triforce];
  const savedBlessing=G.triforceBlessing;
  const savedOpOpen=[...G.opOpen];
  const cfg=LEVEL_CFG[nextLevel];
  // New map
  const md=genMap();
  G.map=md.tiles;
  G.ents=md.ents;
  G.fog=Array.from({length:MH},()=>Array(MW).fill(true));
  // Restore player at new camp position
  G.pl={...savedPl, x:md.cx, y:md.cy, onWater:false};
  G.triforce=savedTriforce;
  G.triforceBlessing=savedBlessing;
  G.opOpen=savedOpOpen;
  G.bossSpawned=[false,false];
  G.bloodMoon=false; G.monsterFrenzy=false; G.stormActive=false;
  G.combat=null; G.screen='play';
  // Reveal starting area
  reveal(md.cx,md.cy,4);
  closeO();
  spawnFloorBoss();
  msg(`🏚️ You descend to Floor ${nextLevel}: ${cfg.name}`,'ml');
  msg(`⚔️ Seek and defeat the floor guardian to continue your descent.`,'mw');
  draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                   OVERLAY                               ║
// ╚══════════════════════════════════════════════════════════╝
// ╔══════════════════════════════════════════════════════════╗
// ║              CHEAT CODES  (↑↑↓↓←→←→)                   ║
// ╚══════════════════════════════════════════════════════════╝
function openCheatMenu(){
  if(!G||G.done) return;
  const c=G.cheats;
  showO('★ CHEAT CODES ★',
    `<p style="color:#f0c040;font-size:9px">The goddesses hear your prayer...</p>
     <p style="color:#ff6060;font-size:6px">⚠️ Activating any cheat disables the leaderboard for this run</p>
     ${c.active?'<p style="color:#ff8040;font-size:6px">⚡ Cheats active — score will not be saved</p>':''}`,
    [{t:`${c.nayru?'✅ ':''}NAYRU — Invincibility`,     f:"cheatNayru()",   cls:c.nayru?'btn-tri':''},
     {t:`${c.din  ?'✅ ':''}DIN — One-Hit Monsters`,    f:"cheatDin()",     cls:c.din  ?'btn-tri':''},
     {t:'RUPEES — Wallet +999',                         f:"cheatRupees()",  cls:'btn-gold'},
     {t:'TRIFORCE — Complete Quest',                    f:"cheatTriforce()",cls:'btn-gold'},
     {t:"BIGGORON — Legendary Sword",                   f:"cheatBiggoron()",cls:'btn-red'},
     {t:'Close',                                        f:"closeO()"}]);
}
function cheatNayru(){
  G.cheats.active=true; G.cheats.nayru=!G.cheats.nayru;
  msg(G.cheats.nayru?"🛡️ NAYRU'S LOVE active — you take no damage!":"🛡️ Nayru's protection lifted.",'mw');
  openCheatMenu();
}
function cheatDin(){
  G.cheats.active=true; G.cheats.din=!G.cheats.din;
  msg(G.cheats.din?"🔥 DIN'S FIRE active — monsters fall in one hit!":"🔥 Din's fire extinguished.",'mw');
  openCheatMenu();
}
function cheatRupees(){
  G.cheats.active=true; G.pl.rupees+=999;
  msg(`💎 999 rupees granted! Total: ${G.pl.rupees}`,'mw');
  openCheatMenu();
}
function cheatTriforce(){
  G.cheats.active=true;
  if(G.triforce.every(t=>t)){ msg('🔱 Triforce already complete!','mw'); openCheatMenu(); return; }
  G.triforce=[true,true,true];
  G.ents=G.ents.filter(e=>e.tp!==E.TRI);
  closeO();
  triforceComplete(); // shows its own overlay
}
function cheatBiggoron(){
  G.cheats.active=true;
  const sword="Biggoron's Sword";
  if(!G.pl.inv.includes(sword)) G.pl.inv.push(sword);
  G.pl.eq.w=sword;
  msg("🗡️ BIGGORON'S SWORD equipped! Overwhelming ATK +7!",'mw');
  updateHUD();
  openCheatMenu();
}

function showO(title,content,btns){
  document.getElementById('oTitle').textContent=title;
  document.getElementById('oContent').innerHTML=content;
  document.getElementById('oBtns').innerHTML=
    btns.map(b=>`<button class="btn ${b.cls||''}" onclick="${b.f}">${b.t}</button>`).join('');
  document.getElementById('overlay').classList.add('on');
}
function closeO(){
  document.getElementById('overlay').classList.remove('on');
  G.screen='play'; draw();
}

function msg(text,cls='mi'){
  const log=document.getElementById('msgLog');
  const d=document.createElement('div');
  d.className=cls; d.textContent=text;
  log.appendChild(d); log.scrollTop=log.scrollHeight;
  while(log.children.length>60) log.removeChild(log.firstChild);
}

// ╔══════════════════════════════════════════════════════════╗
// ║                  KEYBOARD INPUT                         ║
// ╚══════════════════════════════════════════════════════════╝
document.addEventListener('keydown',e=>{
  // Never intercept keys while the user is typing in any text input
  const active=document.activeElement;
  if(active&&(active.tagName==='INPUT'||active.tagName==='TEXTAREA')) return;
  // Konami code — track arrow keys whenever the game is loaded
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)&&G) _pushKonami(e.key);
  if(!G||!G.screen||G.screen==='combat') return;
  const ovOpen=document.getElementById('overlay').classList.contains('on');
  if(ovOpen){if(e.key==='Escape') closeO(); return;}
  switch(e.key){
    case 'ArrowUp':   case 'w':case 'W': e.preventDefault();move(0,-1);break;
    case 'ArrowDown': case 's':case 'S': e.preventDefault();move(0,1); break;
    case 'ArrowLeft': case 'a':case 'A': e.preventDefault();move(-1,0);break;
    case 'ArrowRight':case 'd':case 'D': e.preventDefault();move(1,0); break;
    case 'i':case 'I': openInvScreen(); break;
    case 'f':case 'F': doForage(); break;
    case 'r':case 'R': doRest(); break;
    case ' ': e.preventDefault();doLook(); break;
    case '`': openCheatMenu(); break; // backtick = direct cheat menu
  }
});

// ╔══════════════════════════════════════════════════════════╗
// ║     ROAMING ENEMIES & ANIMAL SPAWNING                   ║
// ╚══════════════════════════════════════════════════════════╝
// ── Roaming bokoblin AI ──────────────────────────────────────
setInterval(()=>{
  if(!G||!G.screen||G.screen!=='play'||G.done) return;
  const isNight=G.time.isNight;
  const DETECT=isNight?9:4; // larger detection range at night
  const MOVE_CHANCE=isNight?0.75:0.25;
  let needDraw=false;

  G.ents.forEach(e=>{
    if(!e.roaming||e.dead||e.gone) return;
    if(Math.random()>MOVE_CHANCE) return;

    const dx_=G.pl.x-e.x, dy_=G.pl.y-e.y;
    const dist=Math.abs(dx_)+Math.abs(dy_);
    let mx=0,my=0;

    if(dist<=DETECT){
      // Chase player — move along the dominant axis toward them
      if(Math.abs(dx_)>=Math.abs(dy_)) mx=dx_>0?1:-1;
      else my=dy_>0?1:-1;
    } else {
      // Random wander
      const dirs=[[0,1],[0,-1],[1,0],[-1,0]];
      const [rdx,rdy]=dirs[Math.floor(Math.random()*dirs.length)];
      mx=rdx; my=rdy;
    }

    const nx=e.x+mx, ny=e.y+my;
    if(nx<1||nx>=MW-1||ny<1||ny>=MH-1) return;
    const t=G.map[ny][nx];
    if(t===T.WA||t===T.TR||t===T.DT||t===T.TH) return;
    // Don't stack onto another entity
    if(G.ents.some(o=>!o.dead&&!o.gone&&o!==e&&o.x===nx&&o.y===ny&&
       ![E.DEER,E.RAB,E.FOX].includes(o.tp))) return;

    e.x=nx; e.y=ny;
    needDraw=true;

    // If roaming bok steps onto the player — trigger combat!
    if(nx===G.pl.x&&ny===G.pl.y&&G.screen==='play'){
      msg(`👺 A Bokoblin patrol ambushes you!`,'md');
      G.combat=e; G.combatRound=0; G.screen='combat'; showCombat();
    }
  });

  if(needDraw&&G.screen==='play') draw();
},2000);

// ── Animal spawning (daytime ambience) ───────────────────────
setInterval(()=>{
  if(!G||!G.screen||G.screen!=='play'||G.time.isNight||G.done) return;
  if(Math.random()>.35) return;
  const types=[E.DEER,E.RAB,E.FOX];
  const tp=types[Math.floor(Math.random()*types.length)];
  const ang=Math.random()*Math.PI*2,dist=3+Math.floor(Math.random()*4);
  let ex=Math.round(G.pl.x+Math.cos(ang)*dist);
  let ey=Math.round(G.pl.y+Math.sin(ang)*dist);
  ex=Math.max(1,Math.min(MW-2,ex)); ey=Math.max(1,Math.min(MH-2,ey));
  if(G.map[ey][ex]===T.WA||G.map[ey][ex]===T.TR||G.map[ey][ex]===T.DT||G.map[ey][ex]===T.TH) return;
  G.ents=G.ents.filter(e=>![E.DEER,E.RAB,E.FOX].includes(e.tp));
  G.ents.push({tp,x:ex,y:ey,id:`an_${Date.now()}`});
  reveal(ex,ey,2); draw();
},4500);

// ╔══════════════════════════════════════════════════════════╗
// ║                    START GAME                           ║
// ╚══════════════════════════════════════════════════════════╝
function startGame(){
  const name=(document.getElementById('nameInput').value.trim()||'Hero').substring(0,12);
  const totalNights=9999;
  document.getElementById('nameScreen').style.display='none';
  document.getElementById('app').style.display='flex';
  cvs=document.getElementById('gameCanvas'); ctx=cvs.getContext('2d');
  function resize(){
    const w=document.getElementById('canvasWrap');
    cvs.width=w.clientWidth; cvs.height=w.clientHeight;
    if(G&&G.screen) draw();
  }
  resize(); window.addEventListener('resize',resize);
  newGame(name,totalNights,diffKey);
  msg(`⚔️ Welcome, ${name}! You enter the dungeon. Five floors await.`,'ml');
  msg('Seek the floor guardian and defeat it to descend deeper.','mw');
  msg('ARROW KEYS/WASD to move · Step on items to collect them.','mi');
  msg('🪓 Craft Stone Axe (Wood+Stone) to chop through obstacles.','mi');
  msg('🔱 Find all 3 Triforce pieces for a powerful golden blessing!','mw');

  // ── D-pad button listeners ──
  function dpMove(dx,dy){
    if(!G||!G.screen||G.screen==='combat') return;
    const ovOpen=document.getElementById('overlay').classList.contains('on');
    if(ovOpen) return;
    move(dx,dy);
  }
  const dpMap={dpUp:[0,-1],dpDown:[0,1],dpLeft:[-1,0],dpRight:[1,0]};
  const dpKonami={dpUp:'ArrowUp',dpDown:'ArrowDown',dpLeft:'ArrowLeft',dpRight:'ArrowRight'};
  Object.entries(dpMap).forEach(([id,[dx,dy]])=>{
    const btn=document.getElementById(id);
    if(!btn) return;
    // touchstart fires before the 300 ms click delay — use it for responsive feel
    btn.addEventListener('touchstart',e=>{e.preventDefault();dpMove(dx,dy);_pushKonami(dpKonami[id]);},{passive:false});
    btn.addEventListener('click',()=>dpMove(dx,dy));
  });

  // ── Swipe detection on canvas ──
  let _tx=0,_ty=0;
  cvs.addEventListener('touchstart',e=>{
    if(e.touches.length!==1) return;
    _tx=e.touches[0].clientX; _ty=e.touches[0].clientY;
  },{passive:true});
  cvs.addEventListener('touchend',e=>{
    if(e.changedTouches.length!==1) return;
    const dx=e.changedTouches[0].clientX-_tx;
    const dy=e.changedTouches[0].clientY-_ty;
    const adx=Math.abs(dx), ady=Math.abs(dy);
    if(Math.max(adx,ady)<24) return; // too short — treat as tap
    const ovOpen=document.getElementById('overlay').classList.contains('on');
    if(ovOpen){closeO();return;}
    if(!G||!G.screen||G.screen==='combat') return;
    if(adx>ady) move(dx>0?1:-1,0); else move(0,dy>0?1:-1);
  },{passive:true});

  draw();
}

document.getElementById('nameInput').addEventListener('keydown',e=>{
  if(e.key==='Enter') startGame();
});

// Load leaderboard on page load
renderLeaderboard();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=800, scrolling=False)

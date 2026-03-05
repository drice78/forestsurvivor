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
<title>Forest Survivor: Zelda Edition</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:100%; height:100%; background:#050e05; color:#c8d8c8;
  font-family:'Press Start 2P','Courier New',monospace; overflow:hidden; user-select:none; }

/* ── Name screen ── */
#nameScreen { position:fixed; inset:0; background:#050e05; z-index:300;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; }
#nameScreen h1 { font-size:clamp(14px,3vw,22px); color:#f0c040; text-shadow:0 0 20px #f0a000; }
#nameScreen h2 { font-size:clamp(8px,1.5vw,11px); color:#78c858; }
#nameScreen p  { font-size:clamp(6px,1vw,8px); color:#80a880; text-align:center;
  max-width:440px; line-height:1.9; }
#nameInput { background:#0a1a0a; border:2px solid #f0c040; color:#f0f0a0;
  font-family:inherit; font-size:16px; padding:8px 14px; border-radius:4px;
  text-align:center; width:280px; outline:none; }
#nameInput:focus { box-shadow:0 0 12px #f0a00050; }

/* night slider row */
.sliderRow { display:flex; align-items:center; gap:10px; }
.sliderRow label { font-size:7px; color:#f0c040; }
#nightSlider { -webkit-appearance:none; width:140px; height:6px; border-radius:3px;
  background:#1a4a1a; outline:none; cursor:pointer; }
#nightSlider::-webkit-slider-thumb { -webkit-appearance:none; width:16px; height:16px;
  border-radius:50%; background:#f0c040; cursor:pointer; border:2px solid #0a1a0a; }
#nightsVal { font-size:11px; color:#f0c040; min-width:30px; text-align:center; }
.diffRow { display:flex; gap:6px; }
.diffBtn { font-family:inherit; font-size:7px; padding:5px 10px;
  border:2px solid #2d5a1b; background:#0d280d; color:#90d878;
  cursor:pointer; border-radius:3px; }
.diffBtn.sel { background:#1a5a1a; border-color:#f0c040; color:#f0c040; }

/* ── App layout ── */
#app { display:none; flex-direction:column; width:100vw; height:100vh; }
#topBar { height:30px; background:#0a1f0a; border-bottom:2px solid #2d5a1b;
  display:flex; align-items:center; padding:0 10px; gap:18px; flex-shrink:0; }
#topTitle { font-size:9px; color:#f0c040; }
#timeDisp { font-size:8px; color:#e0d0a0; }
#nightCtr { font-size:8px; color:#c0d8ff; margin-left:auto; }
#rupeeDisp { font-size:8px; color:#00e8ff; }
#boatInd   { font-size:8px; color:#60b8ff; }

/* main row */
#mainRow { display:flex; flex:1; overflow:hidden; }
#canvasWrap { position:relative; flex:1; overflow:hidden; background:#0a1a0a; }
#gameCanvas { display:block; image-rendering:pixelated; }
#nightVig { position:absolute; inset:0; pointer-events:none; z-index:2;
  background:radial-gradient(ellipse at center,rgba(0,0,10,.05) 20%,rgba(0,0,30,.88) 100%);
  opacity:0; transition:opacity 2s; }
#timebar { position:absolute; bottom:4px; left:4px; right:4px; height:6px;
  background:#111; border:1px solid #333; border-radius:3px; z-index:3; }
#timefill { height:100%; border-radius:3px; transition:width .4s,background .8s; }

/* UI panel */
#uiPanel { width:210px; background:#090f09; border-left:2px solid #2d5a1b;
  display:flex; flex-direction:column; padding:6px; gap:5px; overflow-y:auto; flex-shrink:0; }
.uiBox { background:#0d1f0d; border:1px solid #1e4a1e; border-radius:3px; padding:5px; }
.uiLbl { font-size:6px; color:#f0c040; text-transform:uppercase; letter-spacing:1px; margin-bottom:3px; }
.uiVal { font-size:9px; color:#90d878; }
.heart { font-size:13px; line-height:1; }
#heartsRow { display:flex; flex-wrap:wrap; gap:1px; margin-top:2px; }
#invList { max-height:150px; overflow-y:auto; }
.invItem { font-size:7px; padding:3px 4px; border:1px solid #1a3a1a; margin-bottom:2px;
  border-radius:2px; cursor:pointer; color:#a8c8a8; display:flex; align-items:center; gap:3px; }
.invItem:hover { border-color:#f0c040; color:#f0e060; }
.invItem.eq { border-color:#4090f0; color:#80c0ff; }
#tfDisp { font-size:13px; letter-spacing:4px; margin-top:2px; }
#opStatus { font-size:7px; color:#a0c8a0; line-height:1.8; }

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
.btn-blue { border-color:#204080; color:#80c0ff; background:#081020; }
.btn-blue:hover { background:#102030; }

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

/* scrollbar */
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:#050e05; }
::-webkit-scrollbar-thumb { background:#2d5a1b; border-radius:2px; }
</style>
</head>
<body>

<!-- ══════════ NAME / SETTINGS SCREEN ══════════ -->
<div id="nameScreen">
  <h1>🌲 FOREST SURVIVOR 🌲</h1>
  <h2>— A Zelda-Themed Tale —</h2>
  <p>Stranded deep in the cursed Hyrulean forest, you must survive until rescue arrives.<br>
     Brave the monsters, unlock outposts, find the Triforce — and make it home!</p>

  <input id="nameInput" type="text" placeholder="Enter your hero's name..." maxlength="12" />

  <div class="sliderRow">
    <label>Survival Nights:</label>
    <input id="nightSlider" type="range" min="10" max="200" value="100"
      oninput="document.getElementById('nightsVal').textContent=this.value" />
    <span id="nightsVal">100</span>
  </div>

  <div class="sliderRow" style="gap:6px">
    <label>Difficulty:</label>
    <div class="diffRow">
      <button class="diffBtn" id="dEasy"   onclick="setDiff('easy')">Easy</button>
      <button class="diffBtn sel" id="dNorm" onclick="setDiff('normal')">Normal</button>
      <button class="diffBtn" id="dHard"   onclick="setDiff('hard')">Hard</button>
    </div>
  </div>

  <button class="btn btn-gold" onclick="startGame()" style="width:210px;font-size:9px;padding:9px;">⚔️ BEGIN ADVENTURE</button>
  <p>Arrow Keys / WASD to move &nbsp;·&nbsp; Step on items to collect them<br>
     <span style="color:#f0c040">I</span>=Inventory &nbsp;
     <span style="color:#f0c040">F</span>=Forage &nbsp;
     <span style="color:#f0c040">R</span>=Rest &nbsp;
     <span style="color:#f0c040">Space</span>=Look Around<br>
     🪓 Craft a Stone Axe to chop trees &nbsp;·&nbsp; 🚣 Find a Boat to sail water</p>
</div>

<!-- ══════════ MAIN APP ══════════ -->
<div id="app">
  <div id="topBar">
    <div id="topTitle">🌲 Forest Survivor</div>
    <div id="timeDisp">☀️ Day 1 · Morning</div>
    <div id="boatInd"></div>
    <div id="nightCtr">Night: 0 / 100</div>
    <div id="rupeeDisp">💎 0</div>
  </div>

  <div id="mainRow">
    <div id="canvasWrap">
      <canvas id="gameCanvas"></canvas>
      <div id="nightVig"></div>
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
      </div>
      <div class="uiBox">
        <div class="uiLbl">Outposts</div>
        <div id="opStatus">🔒🔒🔒🔒🔒</div>
      </div>
    </div>
  </div>

  <div id="bottomRow">
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

const T={GR:0,TR:1,DT:2,WA:3,ST:4,SA:5};
const E={CHEST:'chest',KEY:'key',OUTPOST:'outpost',CAMP:'camp',TRI:'triforce',
         BOAT:'boat',
         BOK:'bokoblin',KEE:'keese',SKU:'skulltula',LIZ:'lizalfos',
         DEER:'deer',RAB:'rabbit',FOX:'fox'};

// difficulty multipliers  [monHp, monAtk, spawnMult]
const DIFF_MULT={easy:[0.55,0.55,0.6], normal:[0.80,0.75,1.0], hard:[1.15,1.10,1.4]};
let diffKey='normal';
function setDiff(k){
  diffKey=k;
  ['easy','normal','hard'].forEach(d=>{
    document.getElementById('d'+d.charAt(0).toUpperCase()+d.slice(1)).classList.toggle('sel',d===k);
  });
}

// ── Items ──────────────────────────────────────────────────
const ITEMS={
  'Wooden Sword':    {ic:'⚔️', tp:'weapon', atk:1,  desc:'A simple carved sword.'},
  'Iron Sword':      {ic:'⚔️', tp:'weapon', atk:2,  desc:'A sturdy iron blade.'},
  'Master Sword':    {ic:'⚔️', tp:'weapon', atk:5,  desc:"The sacred blade of evil's bane!", rare:true},
  'Deku Stick':      {ic:'🪵', tp:'weapon', atk:1,  desc:'A dried Deku stick.'},
  'Stone Axe':       {ic:'🪓', tp:'axe',    atk:2,  desc:'Chop trees AND fight! Equip to cut through forest.'},
  'Hylian Shield':   {ic:'🛡️', tp:'armor',  def:3,  desc:'The legendary Hylian Shield!', rare:true},
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

// ── Crafting ───────────────────────────────────────────────
const RECIPES=[
  {result:'Stone Axe',    needs:['Wood','Stone'],           desc:'Chop trees & fight monsters'},
  {result:'Deku Stick',   needs:['Wood','Wood'],            desc:'Basic weapon'},
  {result:'Wooden Shield',needs:['Wood','Wood','Wood'],     desc:'Light defense'},
  {result:'Iron Sword',   needs:['Monster Fang','Stone','Wood'], desc:'Strong blade'},
  {result:'Red Potion',   needs:['Stamella Shroom','Berries'],   desc:'Healing potion'},
  {result:'Map Fragment', needs:['Spider Silk','Keese Wing'],    desc:'Reveals map area'},
];

const OP_NAMES=['Oaken','Hollow','Grimrock','Duskwood','Zephyr'];

const LORE=[
  "The ancient trees whisper... Three goddesses hid the Triforce here for safekeeping.",
  "Carved into bark: 'Monsters grow bolder with every passing night. Seek the outposts.'",
  "A faded note: 'The five keys were scattered by the guardians. Search everywhere.'",
  "Stone inscription: 'He who unites the Triforce shall overcome the curse of this forest.'",
  "Old journal: 'On night 50 the Lizalfos appeared. I hid in Outpost Grimrock for days...'",
];

// ── Monster base stats (nerfed from v1) ────────────────────
const MON={
  bokoblin: {name:'Bokoblin', ic:'👺', hp:4,  atk:1, def:0, rMin:5,  rMax:12, drops:['Monster Fang','Berries','Wood']},
  keese:    {name:'Keese',    ic:'🦇', hp:2,  atk:1, def:0, rMin:2,  rMax:7,  drops:['Keese Wing']},
  skulltula:{name:'Skulltula',ic:'🕷️', hp:4,  atk:2, def:0, rMin:6,  rMax:15, drops:['Spider Silk','Monster Fang']},
  lizalfos: {name:'Lizalfos', ic:'🦎', hp:7,  atk:2, def:1, rMin:12, rMax:22, drops:['Monster Horn','Monster Fang']},
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

// ╔══════════════════════════════════════════════════════════╗
// ║                   GAME STATE                            ║
// ╚══════════════════════════════════════════════════════════╝
let G={};

function newGame(name, totalNights, diff){
  const md=genMap();
  G={
    screen:'play',
    totalNights,
    diff,
    pl:{
      name, x:md.cx, y:md.cy,
      hp:12, maxHp:12,
      atk:1, def:0,
      rupees:10,
      inv:[], eq:{w:null,a:null},
      hasFairy:false, hasLantern:false, hasBoat:false, hasAxe:false,
      onWater:false,
    },
    map:md.tiles,
    ents:md.ents,
    fog:Array.from({length:MH},()=>Array(MW).fill(true)),
    time:{hour:8, acts:0, night:0, isNight:false},
    triforce:[false,false,false],
    opOpen:[false,false,false,false,false],
    combat:null,
    done:false,
  };
  reveal(md.cx,md.cy,4);
}

// ╔══════════════════════════════════════════════════════════╗
// ║                  MAP GENERATION                         ║
// ╚══════════════════════════════════════════════════════════╝
function genMap(){
  const tiles=Array.from({length:MH},()=>Array(MW).fill(T.GR));
  const ents=[];
  let seed=Date.now()&0xfffff;
  function r(){seed=(seed*1664525+1013904223)&0x7fffffff; return seed/0x7fffffff;}

  // Terrain
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

  // Camp at centre — clear a good-sized area
  const cx=40,cy=40;
  clearZone(tiles,cx,cy,4);

  // BFS reachable from camp
  const reach=bfs(tiles,cx,cy);

  // 5 Outpost ideal positions — moved to nearest reachable spot
  const opIdeal=[[14,14],[65,14],[14,65],[65,65],[40,22]];
  const opPos=opIdeal.map(([ox,oy])=>nearestReachable(ox,oy,reach,tiles));
  opPos.forEach(([ox,oy],i)=>{
    clearZone(tiles,ox,oy,2);
    // re-confirm reachable after clearing (clearing can open paths)
    ents.push({tp:E.OUTPOST,x:ox,y:oy,id:`op_${i}`,idx:i,locked:true});
  });

  // Chests (18) — only in reachable areas
  const chestPool=[
    'Wooden Sword','Wooden Sword','Iron Sword','Deku Stick','Stone Axe',
    'Wooden Shield','Iron Shield','Hylian Shield','Master Sword',
    'Red Potion','Red Potion','Blue Potion',
    'Stamella Shroom','Stamella Shroom','Hylian Shroom','Berries',
    'Lantern','Map Fragment','Arrows (5)','Boat',
    'Stone','Stone','Wood','Wood','Monster Fang',
  ];
  for(let i=0;i<18;i++){
    const [ex,ey]=openReach(tiles,ents,r,reach);
    const loot=chestPool[Math.floor(r()*chestPool.length)];
    ents.push({tp:E.CHEST,x:ex,y:ey,id:`ch_${i}`,loot,opened:false});
  }

  // Outpost keys
  for(let i=0;i<5;i++){
    const [ex,ey]=openReach(tiles,ents,r,reach);
    ents.push({tp:E.KEY,x:ex,y:ey,id:`k_${i}`,item:`Outpost Key ${i+1}`});
  }

  // Triforce pieces
  ['Triforce of Power','Triforce of Wisdom','Triforce of Courage'].forEach((nm,i)=>{
    const [ex,ey]=openReach(tiles,ents,r,reach);
    ents.push({tp:E.TRI,x:ex,y:ey,id:`tri_${i}`,piece:i,item:nm});
  });

  // Boats — place 3 near shorelines
  let boatsPlaced=0;
  for(let attempt=0;attempt<3000&&boatsPlaced<3;attempt++){
    const x=2+Math.floor(r()*(MW-4)), y=2+Math.floor(r()*(MH-4));
    if(tiles[y][x]===T.WA||tiles[y][x]===T.TR||tiles[y][x]===T.DT) continue;
    if(!reach[y][x]) continue;
    // Must be adjacent to water
    const adjWater=[[0,1],[0,-1],[1,0],[-1,0]].some(([dx,dy])=>{
      const nx=x+dx,ny=y+dy;
      return nx>=0&&nx<MW&&ny>=0&&ny<MH&&tiles[ny][nx]===T.WA;
    });
    if(!adjWater) continue;
    if(ents.some(e=>e.x===x&&e.y===y)) continue;
    if(Math.abs(x-cx)<=6&&Math.abs(y-cy)<=6) continue;
    ents.push({tp:E.BOAT,x,y,id:`boat_${boatsPlaced}`});
    boatsPlaced++;
  }

  return {tiles,ents,cx,cy};
}

// BFS from (sx,sy) — returns 2D boolean reachability grid (ignores trees)
function bfs(tiles,sx,sy){
  const vis=Array.from({length:MH},()=>Array(MW).fill(false));
  const q=[[sx,sy]]; vis[sy][sx]=true;
  while(q.length){
    const [x,y]=q.shift();
    for(const [dx,dy] of [[0,1],[0,-1],[1,0],[-1,0]]){
      const nx=x+dx,ny=y+dy;
      if(nx<0||nx>=MW||ny<0||ny>=MH||vis[ny][nx]) continue;
      const t=tiles[ny][nx];
      if(t===T.WA||t===T.TR||t===T.DT) continue;
      vis[ny][nx]=true; q.push([nx,ny]);
    }
  }
  return vis;
}

// Find nearest reachable tile to (ox,oy)
function nearestReachable(ox,oy,reach,tiles){
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

function noise(x,y){
  const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;
  function ph(a,b){let n=Math.sin(a*127.1+b*311.7)*43758.5453;return n-Math.floor(n);}
  const s=t=>t*t*(3-2*t),lerp=(a,b,t)=>a+t*(b-a);
  return lerp(lerp(ph(xi,yi),ph(xi+1,yi),s(xf)),lerp(ph(xi,yi+1),ph(xi+1,yi+1),s(xf)),s(yf));
}

function clearZone(tiles,cx,cy,rad){
  for(let dy=-rad;dy<=rad;dy++) for(let dx=-rad;dx<=rad;dx++){
    const nx=cx+dx,ny=cy+dy;
    if(nx>=0&&nx<MW&&ny>=0&&ny<MH) tiles[ny][nx]=T.GR;
  }
}

// Find open walkable spot that is reachable
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
  // fallback
  for(let i=0;i<3000;i++){
    const x=2+Math.floor(r()*(MW-4)),y=2+Math.floor(r()*(MH-4));
    if(tiles[y][x]===T.WA) continue;
    if(!ents.some(e=>e.x===x&&e.y===y)) return [x,y];
  }
  return [10,10];
}

// ╔══════════════════════════════════════════════════════════╗
// ║                  RENDERING                              ║
// ╚══════════════════════════════════════════════════════════╝
let cvs,ctx,camX=0,camY=0;

const TCOL={[T.GR]:'#274f18',[T.TR]:'#1a4509',[T.DT]:'#0e2a05',
            [T.WA]:'#19366a',[T.ST]:'#444',[T.SA]:'#7a6a3a'};
const TEM={[T.TR]:'🌲',[T.DT]:'🌳',[T.SA]:null,[T.ST]:'🪨'};
// Water gets a wave tint when on boat
const EEM={[E.CHEST]:'📦',[E.KEY]:'🗝️',[E.OUTPOST]:'🏰',[E.CAMP]:'⛺',
           [E.TRI]:'🔱',[E.BOAT]:'🚣',
           [E.BOK]:'👺',[E.KEE]:'🦇',[E.SKU]:'🕷️',[E.LIZ]:'🦎',
           [E.DEER]:'🦌',[E.RAB]:'🐇',[E.FOX]:'🦊'};

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
  for(let ty=tyS;ty<tyE&&ty<MH;ty++) for(let tx=txS;tx<txE&&tx<MW;tx++){
    if(tx<0||ty<0) continue;
    const sx=tx*TS-camX,sy=ty*TS-camY;
    const fog=G.fog[ty][tx];
    let col=fog?'#060e06':TCOL[G.map[ty][tx]]||'#274f18';
    // water shimmer when on boat
    if(!fog&&G.map[ty][tx]===T.WA&&G.pl.hasBoat) col='#2a5aaa';
    ctx.fillStyle=col;
    ctx.fillRect(sx,sy,TS,TS);
    if(!fog){
      ctx.strokeStyle='rgba(0,0,0,.12)';ctx.strokeRect(sx,sy,TS,TS);
      const em=TEM[G.map[ty][tx]];
      if(em){ctx.font=`${TS-8}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
             ctx.fillText(em,sx+TS/2,sy+TS/2);}
    }
  }

  // entities
  ctx.textAlign='center';ctx.textBaseline='middle';
  G.ents.forEach(e=>{
    if(e.gone||e.dead) return;
    if(G.fog[e.y][e.x]) return;
    const sx=e.x*TS-camX+TS/2,sy=e.y*TS-camY+TS/2;
    ctx.shadowBlur=0;
    if(e.tp===E.TRI)    {ctx.shadowColor='#f0c040';ctx.shadowBlur=18;}
    else if(e.tp===E.OUTPOST){ctx.shadowColor=G.opOpen[e.idx]?'#00ff80':'#ff3040';ctx.shadowBlur=10;}
    else if(e.tp===E.CAMP)   {ctx.shadowColor='#60ff80';ctx.shadowBlur=8;}
    else if(e.tp===E.BOAT)   {ctx.shadowColor='#60b8ff';ctx.shadowBlur=10;}
    ctx.font=`${TS-4}px serif`;
    const em=e.tp===E.CHEST?(e.opened?'📭':'📦'):EEM[e.tp]||'?';
    ctx.fillText(em,sx,sy);
    ctx.shadowBlur=0;
  });

  // player (shows boat emoji when on water)
  const px=G.pl.x*TS-camX+TS/2,py=G.pl.y*TS-camY+TS/2;
  ctx.shadowColor=G.pl.onWater?'#60b8ff':'#80ff80';ctx.shadowBlur=12;
  ctx.font=`${TS}px serif`;
  ctx.fillText(G.pl.onWater?'🚣':'🧝',px,py);
  ctx.shadowBlur=0;

  updateHUD();
}

function updateHUD(){
  const h=G.time.hour;
  const names=['Midnight','Dead of Night','Dead of Night','Before Dawn','Before Dawn','Dawn',
               'Dawn','Morning','Morning','Midday','Midday','Afternoon','Afternoon','Afternoon',
               'Afternoon','Late Afternoon','Evening','Evening','Dusk','Dusk',
               'Nightfall','Night','Night','Night'];
  const icon=G.time.isNight?'🌙':(h<7||h>18?'🌅':'☀️');
  document.getElementById('timeDisp').textContent=`${icon} Day ${G.time.night+1} · ${names[h]||''}`;
  document.getElementById('nightCtr').textContent=`Night: ${G.time.night} / ${G.totalNights}`;
  document.getElementById('rupeeDisp').textContent=`💎 ${G.pl.rupees}`;
  document.getElementById('boatInd').textContent=G.pl.onWater?'🚣 Sailing':
                                                  G.pl.hasBoat?'🚣 Have Boat':'';

  const fill=document.getElementById('timefill');
  fill.style.width=(h/24*100)+'%';
  fill.style.background=G.time.isNight?'#3050d0':(h<8||h>18?'#c08040':'#f0c040');
  document.getElementById('nightVig').style.opacity=G.time.isNight?'1':'0';

  document.getElementById('uiName').textContent=G.pl.name;

  // hearts
  let hh='';
  for(let i=0;i<G.pl.maxHp;i+=2){
    if(G.pl.hp>=i+2)       hh+='<span class="heart">❤️</span>';
    else if(G.pl.hp===i+1) hh+='<span class="heart">💛</span>';
    else                    hh+='<span class="heart" style="opacity:.25">🖤</span>';
  }
  document.getElementById('heartsRow').innerHTML=hh;
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
  document.getElementById('opStatus').innerHTML=
    G.opOpen.map((u,i)=>u?`🏰✅ ${OP_NAMES[i]}`:`🏰🔒 ${OP_NAMES[i]}`).join('<br>');
}

// ╔══════════════════════════════════════════════════════════╗
// ║               TIME & MOVEMENT                           ║
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
        msg(`🌙 Night ${G.time.night} falls... monsters awaken!`,'md');
        if(G.time.night>=G.totalNights){triggerVictory();return;}
      } else if(was&&!G.time.isNight){
        msg(`☀️ Dawn breaks! Day ${G.time.night+1} begins. Safe for now.`,'ms');
        purgeMonsters();
      }
    }
  }
}

function canWalk(x,y){
  if(x<0||x>=MW||y<0||y>=MH) return false;
  const t=G.map[y][x];
  if(t===T.WA) return G.pl.hasBoat;   // water needs boat
  return t!==T.TR&&t!==T.DT;          // trees block unless cut
}

function move(dx,dy){
  if(G.screen!=='play'||G.done) return;
  const nx=G.pl.x+dx, ny=G.pl.y+dy;
  if(nx<0||nx>=MW||ny<0||ny>=MH) return;
  const t=G.map[ny][nx];

  // Tree-cutting with axe
  if(t===T.TR||t===T.DT){
    if(G.pl.hasAxe){
      G.map[ny][nx]=T.GR;
      G.pl.x=nx; G.pl.y=ny;
      reveal(nx,ny,3);
      tick(2); // chopping costs extra actions
      msg('🪓 You chop down the tree and push through!'+(t===T.DT?' It was a mighty tree.':''),'mi');
      // chopping gives wood
      if(Math.random()<0.7) addItem('Wood');
      stepOn();
    } else {
      msg('🌲 A tree blocks the way! Craft or find a Stone Axe to chop through.','mw');
    }
    draw(); return;
  }

  // Water without boat
  if(t===T.WA&&!G.pl.hasBoat){
    msg('🌊 Water blocks the way! Find a 🚣 Boat to sail across.','mw');
    draw(); return;
  }

  // Normal move
  G.pl.x=nx; G.pl.y=ny;
  G.pl.onWater=(t===T.WA);
  reveal(nx,ny,3);
  tick();
  stepOn();
  if(G.time.isNight) trySpawn();
  draw();
}

function reveal(cx,cy,rad){
  for(let dy=-rad;dy<=rad;dy++) for(let dx=-rad;dx<=rad;dx++){
    const nx=cx+dx,ny=cy+dy;
    if(nx>=0&&nx<MW&&ny>=0&&ny<MH&&Math.hypot(dx,dy)<=rad) G.fog[ny][nx]=false;
  }
}

// ╔══════════════════════════════════════════════════════════╗
// ║              ENTITY INTERACTIONS                        ║
// ╚══════════════════════════════════════════════════════════╝
function stepOn(){
  G.ents.forEach(e=>{
    if(e.gone||e.dead) return;
    if(e.x!==G.pl.x||e.y!==G.pl.y) return;
    onStep(e);
  });
}

function onStep(e){
  switch(e.tp){
    case E.CAMP:
      msg('⛺ Back at camp. You feel a little safer here.','mi'); break;
    case E.KEY:
      if(addItem(e.item)){e.gone=true;msg(`🗝️ Found ${e.item}!`,'ms');} break;
    case E.BOAT:
      if(!G.pl.hasBoat){
        G.pl.hasBoat=true; addItem('Boat'); e.gone=true;
        msg('🚣 You found a boat! You can now sail across water.','ms');
      } break;
    case E.TRI:
      if(!G.triforce[e.piece]){
        G.triforce[e.piece]=true; addItem(e.item); e.gone=true;
        msg(`🔱 TRIFORCE PIECE FOUND! ${e.item}!`,'mw');
        if(G.triforce.every(t=>t)){
          msg('✨ THE TRIFORCE IS COMPLETE! Ancient power surges — +4 max HP!','mw');
          G.pl.maxHp=Math.min(G.pl.maxHp+4,20);
          G.pl.hp=Math.min(G.pl.hp+4,G.pl.maxHp);
        }
      } break;
    case E.CHEST:
      if(!e.opened){e.opened=true;showChest(e.loot);} break;
    case E.OUTPOST:
      showOutpost(e); break;
    case E.BOK: case E.KEE: case E.SKU: case E.LIZ:
      if(!e.dead) startCombat(e); break;
    case E.DEER: case E.RAB: case E.FOX:
      msg(`A ${e.tp} scampers into the undergrowth!`,'mi'); e.gone=true; break;
  }
}

// ╔══════════════════════════════════════════════════════════╗
// ║                INVENTORY                                ║
// ╚══════════════════════════════════════════════════════════╝
function addItem(nm){
  if(G.pl.inv.length>=20){msg('Inventory full! (20/20) — drop something first.','mw');return false;}
  G.pl.inv.push(nm); return true;
}

function quickUse(i){
  const nm=G.pl.inv[i]; if(!nm) return;
  const d=ITEMS[nm]; if(!d) return;
  if(d.tp==='weapon'){
    G.pl.eq.w=nm; G.pl.atk=d.atk; G.pl.hasAxe=false;
    msg(`Equipped ${nm} (ATK +${d.atk}).`,'mi');
  } else if(d.tp==='axe'){
    G.pl.eq.w=nm; G.pl.atk=d.atk; G.pl.hasAxe=true;
    msg(`🪓 Stone Axe equipped! You can now chop trees and fight.`,'ms');
  } else if(d.tp==='armor'){
    G.pl.eq.a=nm; G.pl.def=d.def;
    msg(`Equipped ${nm} (DEF +${d.def}).`,'mi');
  } else if(d.tp==='use'){
    useConsumable(i);
  } else if(d.tp==='boat'){
    G.pl.hasBoat=true;
    msg('🚣 Boat ready! Walk into water to sail.','ms');
  } else if(d.tp==='tool'&&nm==='Lantern'){
    G.pl.hasLantern=true;
    msg('🏮 Lantern lit! Monsters will be less bold at night.','ms');
  } else if(d.tp==='tool'&&nm==='Map Fragment'){
    G.pl.inv.splice(i,1); revealFragment();
    msg('🗺️ Map fragment revealed a new area!','ms');
  } else {
    msg(`${nm}: ${d.desc}`,'mi');
  }
  draw();
}

function useConsumable(i){
  const nm=G.pl.inv[i]; const d=ITEMS[nm];
  G.pl.inv.splice(i,1);
  if(d.revive){G.pl.hasFairy=true; msg('🧚 Fairy captured! Auto-revive ready.','ms');}
  else if(d.heal){
    G.pl.hp=Math.min(G.pl.hp+d.heal,G.pl.maxHp);
    msg(`Used ${nm}. Restored ${Math.min(d.heal,d.heal)/2} hearts.`,'ms');
  }
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
  let html=`<p style="color:#90d878">${G.pl.inv.length}/20 items held</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:8px;">`;
  G.pl.inv.forEach((nm,i)=>{
    const d=ITEMS[nm]||{ic:'?',desc:''};
    const eq=G.pl.eq.w===nm||G.pl.eq.a===nm;
    const lbl=d.tp==='weapon'||d.tp==='armor'||d.tp==='axe'?'Equip':d.tp==='use'?'Use':'Use';
    html+=`<div style="background:#0a1a0a;border:1px solid ${eq?'#4090f0':'#2d5a1b'};padding:5px;border-radius:3px;text-align:left;">
      <div style="font-size:10px;">${d.ic} <span style="font-size:7px;color:${eq?'#80c0ff':'#a8c8a8'}">${nm}</span></div>
      <div style="font-size:6px;color:#607060;margin:2px 0">${d.desc}</div>
      <button class="btn" style="font-size:6px;padding:2px 5px;margin-top:2px" onclick="quickUse(${i});closeO()">${lbl}</button>
      <button class="btn btn-red" style="font-size:6px;padding:2px 5px;margin-top:2px" onclick="dropItem(${i});closeO()">Drop</button>
    </div>`;
  });
  html+='</div>';
  showO('🎒 Inventory',html,[{t:'Close',f:'closeO()'}]);
}

// ╔══════════════════════════════════════════════════════════╗
// ║                     CHEST                               ║
// ╚══════════════════════════════════════════════════════════╝
function showChest(loot){
  const d=ITEMS[loot]||{ic:'?',desc:''};
  showO('📦 Chest Opened!',
    `<p>You pry open the old chest and find...</p>
     <p style="font-size:22px;margin:10px 0">${d.ic}</p>
     <p style="color:#f0c040;font-size:10px">${loot}</p>
     <p style="font-size:7px;color:#90c890">${d.desc}</p>`,
    [{t:'Take It!',f:`takeChest('${loot.replace(/'/g,"\\'")}')`,cls:'btn-gold'},{t:'Leave It',f:'closeO()'}]
  );
}
function takeChest(loot){closeO();if(addItem(loot))msg(`Got ${loot} from chest!`,'ms');draw();}

// ╔══════════════════════════════════════════════════════════╗
// ║                    OUTPOSTS                             ║
// ╚══════════════════════════════════════════════════════════╝
function showOutpost(e){
  const idx=e.idx,nm=OP_NAMES[idx];
  if(!G.opOpen[idx]){
    const key=`Outpost Key ${idx+1}`;
    const has=G.pl.inv.includes(key);
    if(has){
      showO(`🏰 Outpost ${nm}`,
        `<p>A fortified outpost. You have the ${key}!</p>`,
        [{t:'🗝️ Unlock',f:`unlockOp(${idx})`,cls:'btn-gold'},{t:'Leave',f:'closeO()'}]);
    } else {
      showO(`🏰 Outpost ${nm} (Locked)`,
        `<p>A fortified outpost. The door is locked.</p><p>You need <span style="color:#f0c040">${key}</span> to enter.</p>`,
        [{t:'Leave',f:'closeO()'}]);
    }
  } else {
    opMenu(idx,nm);
  }
}

function unlockOp(idx){
  const key=`Outpost Key ${idx+1}`;
  const ki=G.pl.inv.indexOf(key);
  if(ki>=0) G.pl.inv.splice(ki,1);
  G.opOpen[idx]=true;
  G.ents.find(e=>e.tp===E.OUTPOST&&e.idx===idx).locked=false;
  msg(`🏰 Outpost ${OP_NAMES[idx]} unlocked! A safe refuge secured.`,'ms');
  opMenu(idx,OP_NAMES[idx]);
}

function opMenu(idx,nm){
  showO(`🏰 Outpost ${nm}`,
    `<p>A safe haven in the cursed forest. What will you do?</p>`,
    [
      {t:'💤 Sleep Safely',f:'opSleep()',cls:'btn-gold'},
      {t:'⚒️ Crafting',f:'openCraft()'},
      {t:'🧙 Merchant',f:'openShop()'},
      {t:`📜 Lore`,f:`readLore(${idx})`},
      {t:'Leave',f:'closeO()'},
    ]
  );
}

function opSleep(){
  const was=G.time.isNight;
  G.time.hour=8; G.time.isNight=false;
  if(was){G.time.night++;msg(`💤 Slept safely! Night ${G.time.night} passed.`,'ms');}
  else msg('💤 You rest and feel refreshed.','mi');
  G.pl.hp=Math.min(G.pl.hp+4,G.pl.maxHp);
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
  let html=`<p style="color:#90d878">Combine materials to craft items at this bench.</p>`;
  RECIPES.forEach((rec,i)=>{
    const can=rec.needs.every(n=>G.pl.inv.includes(n));
    const d=ITEMS[rec.result]||{ic:'?'};
    html+=`<div style="border:1px solid #2d5a1b;padding:5px;margin:4px 0;border-radius:3px">
      <div style="font-size:8px;color:${can?'#f0c040':'#506050'}">${d.ic} ${rec.result}</div>
      <div style="font-size:7px;color:#506050">Needs: ${rec.needs.join(' + ')}</div>
      <div style="font-size:6px;color:#708060;margin:1px 0">${rec.desc||''}</div>
      ${can?`<button class="btn btn-gold" style="margin-top:3px;padding:3px 8px" onclick="craft(${i})">Craft!</button>`:'<span style="font-size:6px;color:#405040">Missing materials</span>'}
    </div>`;
  });
  showO('⚒️ Crafting Bench',html,[{t:'Close',f:'closeO()'}]);
}

function craft(i){
  const rec=RECIPES[i];
  rec.needs.forEach(n=>{const j=G.pl.inv.indexOf(n);if(j>=0)G.pl.inv.splice(j,1);});
  if(addItem(rec.result)) msg(`⚒️ Crafted ${rec.result}!`,'ms');
  closeO(); draw();
}

function openShop(){
  let html=`<p>A mysterious merchant grins behind a cluttered stall.</p>
    <p style="color:#00e8ff">Your rupees: 💎 ${G.pl.rupees}</p>`;
  SHOP.forEach((s,i)=>{
    const can=G.pl.rupees>=s.price;
    const d=ITEMS[s.name]||{ic:'?'};
    html+=`<div style="border:1px solid #2d5a1b;padding:5px;margin:3px;display:flex;justify-content:space-between;align-items:center;border-radius:3px">
      <span style="font-size:8px">${d.ic} ${s.name}</span>
      <span>
        <span style="font-size:7px;color:#00e8ff">💎${s.price}</span>
        ${can?`<button class="btn btn-gold" style="padding:2px 8px;margin-left:4px" onclick="buy(${i})">Buy</button>`:''}
      </span>
    </div>`;
  });
  showO('🧙 Wandering Merchant',html,[{t:'Leave',f:'closeO()'}]);
}

function buy(i){
  const s=SHOP[i];
  if(G.pl.rupees<s.price){msg('Not enough rupees!','mw');return;}
  if(addItem(s.name)){
    G.pl.rupees-=s.price;
    msg(`Bought ${s.name} for 💎${s.price}!`,'ms');
    // special flags
    if(s.name==='Boat'){G.pl.hasBoat=true;}
    if(s.name==='Lantern'){G.pl.hasLantern=true;}
  }
  closeO(); openShop();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                    COMBAT                               ║
// ╚══════════════════════════════════════════════════════════╝
function startCombat(e){G.combat=e;G.screen='combat';showCombat();}

function showCombat(){
  const e=G.combat;
  const mb=MON[e.tp]||{ic:'👹',name:'Monster'};
  showO(`⚔️ ${mb.ic} ${e.name} Attacks!`,
    `<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0">
      <div style="background:#0a2a0a;padding:7px;border-radius:4px;border:1px solid #2d7a2d">
        <div style="font-size:9px;color:#78e878">🧝 ${G.pl.name}</div>
        <div style="font-size:7px;margin-top:3px">❤️ ${G.pl.hp}/${G.pl.maxHp}</div>
        <div style="font-size:7px">⚔️${G.pl.atk} 🛡️${G.pl.def}</div>
      </div>
      <div style="background:#2a0a0a;padding:7px;border-radius:4px;border:1px solid #7a2d2d">
        <div style="font-size:9px;color:#e87878">${mb.ic} ${e.name}</div>
        <div style="font-size:7px;margin-top:3px">💀 ${e.hp}/${e.maxHp}</div>
        <div style="font-size:7px">⚔️${e.atk} 🛡️${e.def}</div>
      </div>
    </div>
    <div style="font-size:7px;color:#f0c040">Night ${G.time.night} — Choose your action!</div>`,
    [
      {t:'⚔️ Attack',f:'cAttack()',cls:'btn-red'},
      {t:'🛡️ Defend',f:'cDefend()'},
      {t:'🧪 Heal',f:'cHeal()'},
      {t:'💨 Flee',f:'cFlee()'},
    ]
  );
}

function d6(){return 1+Math.floor(Math.random()*6);}

function cAttack(){
  const e=G.combat;
  const pr=d6()+G.pl.atk, pd=Math.max(0,pr-e.def);
  e.hp-=pd;
  let m=`You roll 🎲${pr-G.pl.atk}+${G.pl.atk}→${pd} dmg to ${e.name}!`;
  if(e.hp<=0){winCombat(e,m);return;}
  const er=d6()+e.atk, ed=Math.max(0,er-G.pl.def);
  G.pl.hp-=ed;
  m+=` | ${e.name} hits for ${ed} dmg!`;
  msg(m,'md');
  if(G.pl.hp<=0){loseCombat();return;}
  showCombat();
}

function cDefend(){
  const e=G.combat;
  const er=d6()+e.atk, ed=Math.max(0,er-G.pl.def-3);
  G.pl.hp-=ed;
  msg(`You brace! ${e.name} hits for ${ed} dmg (blocked some).`,'mi');
  if(G.pl.hp<=0){loseCombat();return;}
  showCombat();
}

function cHeal(){
  const pi=G.pl.inv.findIndex(n=>(ITEMS[n]||{}).heal>0);
  if(pi<0){msg('No healing items in inventory!','mw');showCombat();return;}
  useConsumable(pi);
  const e=G.combat;
  const er=d6()+e.atk, ed=Math.max(0,er-G.pl.def);
  G.pl.hp=Math.max(0,G.pl.hp-ed);
  msg(`You healed! But ${e.name} attacks for ${ed} dmg!`,'mw');
  if(G.pl.hp<=0){loseCombat();return;}
  showCombat();
}

function cFlee(){
  const pct=0.45+Math.floor(G.time.night/5)*0.04;
  const ename=G.combat?G.combat.name:'monster';
  if(Math.random()<pct){
    const ox=G.pl.x,oy=G.pl.y;
    G.pl.x=Math.max(1,Math.min(MW-2,ox+(Math.random()<.5?-3:3)));
    G.pl.y=Math.max(1,Math.min(MH-2,oy+(Math.random()<.5?-3:3)));
    G.screen='play'; G.combat=null; closeO();
    msg(`You fled from the ${ename}!`,'mw');
  } else {
    const e=G.combat;
    const er=d6()+e.atk, ed=Math.max(0,er-G.pl.def);
    G.pl.hp=Math.max(0,G.pl.hp-ed);
    msg(`Failed to flee! ${ename} strikes for ${ed} dmg!`,'md');
    if(G.pl.hp<=0){loseCombat();return;}
    showCombat();
  }
}

function winCombat(e,lastMsg){
  e.dead=true;
  const mb=MON[e.tp]||{rMin:0,rMax:5,drops:[]};
  const rp=mb.rMin+Math.floor(Math.random()*(mb.rMax-mb.rMin));
  G.pl.rupees+=rp;
  const drop=mb.drops[Math.floor(Math.random()*mb.drops.length)];
  const gotDrop=drop&&Math.random()<0.55;
  if(gotDrop) addItem(drop);
  msg(`${lastMsg} → VICTORY! +💎${rp}${gotDrop?` + ${drop}`:''}!`,'ms');
  G.screen='play'; G.combat=null;
  showO('⚔️ Victory!',
    `<p style="color:#60ff60;font-size:11px">You defeated the ${e.name}!</p>
     <p>+💎${rp} Rupees${gotDrop?`<br>${ITEMS[drop]?.ic||''} ${drop} dropped!`:''}</p>`,
    [{t:'Continue',f:'closeO()',cls:'btn-gold'}]);
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
     <p style="color:#f07878">A day has passed. Night: ${G.time.night}/${G.totalNights}</p>
     ${dropped.length?`<p style="color:#a07040">You dropped: ${dropped.join(', ')}</p>`:''}
     <p>Stay closer to camp at night!</p>`,
    [{t:'Rise & Survive!',f:'closeO()',cls:'btn-gold'}]);
  msg(`💀 Defeated! Woke at camp. Night: ${G.time.night}/${G.totalNights}. Lost: ${dropped.join(', ')||'nothing'}.`,'md');
  draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║              MONSTER SPAWNING                           ║
// ╚══════════════════════════════════════════════════════════╝
function trySpawn(){
  if(!G.time.isNight) return;
  const dm=DIFF_MULT[G.diff]||DIFF_MULT.normal;
  let chance=Math.min(0.06+G.time.night*0.0025,0.20)*dm[2];
  if(G.pl.hasLantern) chance*=0.45;
  if(Math.random()>chance) return;

  const n=G.time.night;
  let pool;
  if(n<10)       pool=[E.KEE,E.KEE,E.BOK];
  else if(n<30)  pool=[E.KEE,E.BOK,E.BOK,E.SKU];
  else if(n<60)  pool=[E.BOK,E.SKU,E.SKU,E.LIZ];
  else           pool=[E.SKU,E.LIZ,E.LIZ];

  const tp=pool[Math.floor(Math.random()*pool.length)];
  const mb=MON[tp];
  const scale=(1+n*0.03)*dm[0];
  const atkScale=(1+n*0.02)*dm[1];

  const ang=Math.random()*Math.PI*2;
  const dist=3+Math.floor(Math.random()*3);
  let ex=Math.round(G.pl.x+Math.cos(ang)*dist);
  let ey=Math.round(G.pl.y+Math.sin(ang)*dist);
  ex=Math.max(1,Math.min(MW-2,ex)); ey=Math.max(1,Math.min(MH-2,ey));
  if(G.map[ey][ex]===T.WA||G.map[ey][ex]===T.TR||G.map[ey][ex]===T.DT) return;

  G.ents.push({
    tp,x:ex,y:ey,id:`m_${Date.now()}_${Math.random()}`,
    name:mb.name,
    hp:Math.max(1,Math.ceil(mb.hp*scale)),
    maxHp:Math.max(1,Math.ceil(mb.hp*scale)),
    atk:Math.max(1,Math.ceil(mb.atk*atkScale)),
    def:Math.ceil(mb.def*scale),
    drops:mb.drops,
  });
  reveal(ex,ey,2);
  msg(`👹 A ${mb.name} ${mb.ic} emerges from the shadows!`,'md');
}

function purgeMonsters(){
  G.ents=G.ents.filter(e=>{
    if([E.BOK,E.KEE,E.SKU,E.LIZ].includes(e.tp)){
      return Math.abs(e.x-G.pl.x)+Math.abs(e.y-G.pl.y)<3;
    }
    return true;
  });
}

// ╔══════════════════════════════════════════════════════════╗
// ║                ACTION BUTTONS                           ║
// ╚══════════════════════════════════════════════════════════╝
function doForage(){
  if(G.screen!=='play'||G.done) return;
  if(G.pl.onWater){msg('🌊 Cannot forage while sailing!','mw');return;}
  tick(2);
  const pool=['Berries','Berries','Berries','Stamella Shroom','Wood','Wood','Stone','Monster Fang','Keese Wing'];
  if(Math.random()<0.68){
    const f=pool[Math.floor(Math.random()*pool.length)];
    if(addItem(f)) msg(`🌿 Foraging: found ${ITEMS[f]?.ic||''} ${f}!`,'ms');
  } else msg('🌿 You search but find nothing useful this time.','mi');
  if(Math.random()<0.22){
    const rp=1+Math.floor(Math.random()*6);
    G.pl.rupees+=rp; msg(`Spotted 💎${rp} rupees glinting in the leaves!`,'ms');
  }
  if(G.time.isNight) trySpawn();
  draw();
}

function doRest(){
  if(G.screen!=='play'||G.done) return;
  if(G.pl.onWater){msg('🌊 Cannot rest properly while on water!','mw');return;}
  if(G.time.isNight) msg('⚠️ Resting at night is risky — monsters may find you!','mw');
  tick(3);
  G.pl.hp=Math.min(G.pl.hp+2,G.pl.maxHp);
  msg('💤 You rest briefly and recover 1 heart.','mi');
  if(G.time.isNight) trySpawn();
  draw();
}

function doLook(){
  if(G.screen!=='play'||G.done) return;
  reveal(G.pl.x,G.pl.y,5); tick();
  const nearby=G.ents.filter(e=>{
    if(e.gone||e.dead) return false;
    return Math.abs(e.x-G.pl.x)+Math.abs(e.y-G.pl.y)<=5;
  });
  if(!nearby.length) msg('👁️ The forest stretches endlessly around you...','mi');
  else msg(`👁️ Nearby: ${nearby.map(e=>EEM[e.tp]+' '+e.tp).join(', ')}`,
           G.time.isNight?'md':'mi');
  if(G.time.isNight) msg('🌙 The shadows writhe. Stay alert!','md');
  draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                   VICTORY                               ║
// ╚══════════════════════════════════════════════════════════╝
function triggerVictory(){
  G.done=true; G.screen='win';
  const tc=G.triforce.filter(t=>t).length;
  const oc=G.opOpen.filter(u=>u).length;
  showO('🚁 RESCUE!',
    `<div style="font-size:36px;margin:10px 0">🚁</div>
     <p style="color:#f0e860;font-size:12px">YOU SURVIVED ${G.totalNights} NIGHTS!</p>
     <p>The rescue helicopter descends through the canopy!</p>
     <p>Hero: <span style="color:#f0c040">${G.pl.name}</span></p>
     <hr style="border-color:#2d5a1b;margin:10px 0">
     <p>🔱 Triforce: ${tc}/3 ${tc===3?'🏆 COMPLETE!':''}</p>
     <p>🏰 Outposts: ${oc}/5 unlocked</p>
     <p>💎 Rupees: ${G.pl.rupees}</p>
     <p style="font-size:7px;color:#90a890;margin-top:8px">The legend of ${G.pl.name} will be remembered in Hyrule forever.</p>`,
    [{t:'🏆 Play Again',f:'location.reload()',cls:'btn-gold'}]);
  msg(`🚁 THE RESCUE HELICOPTER HAS ARRIVED! YOU SURVIVED ${G.totalNights} NIGHTS!`,'mw');
}

// ╔══════════════════════════════════════════════════════════╗
// ║                    OVERLAY                              ║
// ╚══════════════════════════════════════════════════════════╝
function showO(title,content,btns){
  document.getElementById('oTitle').textContent=title;
  document.getElementById('oContent').innerHTML=content;
  document.getElementById('oBtns').innerHTML=
    btns.map(b=>`<button class="btn ${b.cls||''}" onclick="${b.f}">${b.t}</button>`).join('');
  document.getElementById('overlay').classList.add('on');
}
function closeO(){
  document.getElementById('overlay').classList.remove('on');
  G.screen='play';
  draw();
}

// ╔══════════════════════════════════════════════════════════╗
// ║                   MESSAGES                              ║
// ╚══════════════════════════════════════════════════════════╝
function msg(text,cls='mi'){
  const log=document.getElementById('msgLog');
  const d=document.createElement('div');
  d.className=cls; d.textContent=text;
  log.appendChild(d);
  log.scrollTop=log.scrollHeight;
  while(log.children.length>60) log.removeChild(log.firstChild);
}

// ╔══════════════════════════════════════════════════════════╗
// ║                  KEYBOARD INPUT                         ║
// ╚══════════════════════════════════════════════════════════╝
document.addEventListener('keydown',e=>{
  if(G.screen==='combat') return;
  const ovOpen=document.getElementById('overlay').classList.contains('on');
  if(ovOpen){if(e.key==='Escape') closeO(); return;}
  switch(e.key){
    case 'ArrowUp':    case 'w': case 'W': e.preventDefault(); move(0,-1); break;
    case 'ArrowDown':  case 's': case 'S': e.preventDefault(); move(0,1);  break;
    case 'ArrowLeft':  case 'a': case 'A': e.preventDefault(); move(-1,0); break;
    case 'ArrowRight': case 'd': case 'D': e.preventDefault(); move(1,0);  break;
    case 'i': case 'I': openInvScreen(); break;
    case 'f': case 'F': doForage(); break;
    case 'r': case 'R': doRest(); break;
    case ' ': e.preventDefault(); doLook(); break;
  }
});

// ╔══════════════════════════════════════════════════════════╗
// ║           ANIMAL SPAWNING (daytime)                     ║
// ╚══════════════════════════════════════════════════════════╝
setInterval(()=>{
  if(!G||!G.screen||G.screen!=='play'||G.time.isNight||G.done) return;
  if(Math.random()>0.35) return;
  const types=[E.DEER,E.RAB,E.FOX];
  const tp=types[Math.floor(Math.random()*types.length)];
  const ang=Math.random()*Math.PI*2,dist=3+Math.floor(Math.random()*4);
  let ex=Math.round(G.pl.x+Math.cos(ang)*dist);
  let ey=Math.round(G.pl.y+Math.sin(ang)*dist);
  ex=Math.max(1,Math.min(MW-2,ex)); ey=Math.max(1,Math.min(MH-2,ey));
  if(G.map[ey][ex]===T.WA||G.map[ey][ex]===T.TR||G.map[ey][ex]===T.DT) return;
  G.ents=G.ents.filter(e=>![E.DEER,E.RAB,E.FOX].includes(e.tp));
  G.ents.push({tp,x:ex,y:ey,id:`an_${Date.now()}`});
  reveal(ex,ey,2); draw();
},4000);

// ╔══════════════════════════════════════════════════════════╗
// ║                   START GAME                            ║
// ╚══════════════════════════════════════════════════════════╝
function startGame(){
  const name=(document.getElementById('nameInput').value.trim()||'Hero').substring(0,12);
  const totalNights=parseInt(document.getElementById('nightSlider').value)||100;
  document.getElementById('nameScreen').style.display='none';
  document.getElementById('app').style.display='flex';

  cvs=document.getElementById('gameCanvas');
  ctx=cvs.getContext('2d');
  function resize(){
    const w=document.getElementById('canvasWrap');
    cvs.width=w.clientWidth; cvs.height=w.clientHeight;
    if(G&&G.screen) draw();
  }
  resize();
  window.addEventListener('resize',resize);

  newGame(name,totalNights,diffKey);

  msg(`🌲 Welcome, ${name}! Survive ${totalNights} nights. The helicopter comes after that.`,'ml');
  msg(`Use ARROW KEYS or WASD to move. Step onto items/chests to interact.`,'mi');
  msg(`🪓 Craft a Stone Axe (Wood+Stone) to chop through trees.`,'mw');
  msg(`🚣 Find a Boat near shorelines to sail across water.`,'mw');
  msg(`🌙 Days advance as you act. Find outpost keys hidden around the forest.`,'mi');
  draw();
}

document.getElementById('nameInput').addEventListener('keydown',e=>{
  if(e.key==='Enter') startGame();
});
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=760, scrolling=False)

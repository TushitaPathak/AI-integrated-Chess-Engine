# Chess Engine - Flask + python-chess

from flask import Flask, render_template_string, request, jsonify, session
import chess

app = Flask(__name__)
app.secret_key = "chess-key"

PIECE_VAL = {chess.PAWN:100,chess.KNIGHT:320,chess.BISHOP:330,chess.ROOK:500,chess.QUEEN:900,chess.KING:20000}

PST = {
    chess.PAWN:   [0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0],
    chess.KNIGHT: [-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
    chess.BISHOP: [-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20],
    chess.ROOK:   [0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0],
    chess.QUEEN:  [-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],
    chess.KING:   [-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20],
}
KING_EG = [-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50]

def is_endgame(b):
    q=len(b.pieces(chess.QUEEN,chess.WHITE))+len(b.pieces(chess.QUEEN,chess.BLACK))
    m=sum(len(b.pieces(pt,c)) for pt in (chess.ROOK,chess.BISHOP,chess.KNIGHT) for c in (chess.WHITE,chess.BLACK))
    return q==0 or (q==2 and m<=2)

def score(b):
    if b.is_checkmate(): return -99999 if b.turn==chess.WHITE else 99999
    if b.is_stalemate() or b.is_insufficient_material(): return 0
    eg=is_endgame(b); total=0
    for pt in PIECE_VAL:
        pst=KING_EG if (pt==chess.KING and eg) else PST[pt]
        for sq in b.pieces(pt,chess.WHITE):
            total+=PIECE_VAL[pt]+pst[(7-chess.square_rank(sq))*8+chess.square_file(sq)]
        for sq in b.pieces(pt,chess.BLACK):
            total-=PIECE_VAL[pt]+pst[chess.square_rank(sq)*8+chess.square_file(sq)]
    return total

def mvv_lva(b,m):
    if b.is_capture(m):
        v=b.piece_at(m.to_square); a=b.piece_at(m.from_square)
        return 10000+(PIECE_VAL.get(v.piece_type,0) if v else 50)-(PIECE_VAL.get(a.piece_type,100) if a else 100)
    b.push(m); ck=b.is_check(); b.pop()
    return 5000 if ck else 0

def order_moves(b,moves): return sorted(moves,key=lambda m:mvv_lva(b,m),reverse=True)

def quiesce(b,alpha,beta):
    sp=score(b)
    if sp>=beta: return beta
    if alpha<sp: alpha=sp
    for m in order_moves(b,[x for x in b.legal_moves if b.is_capture(x)]):
        b.push(m); val=-quiesce(b,-beta,-alpha); b.pop()
        if val>=beta: return beta
        if val>alpha: alpha=val
    return alpha

def minimax(b,depth,alpha,beta,maxi):
    if depth==0: return quiesce(b,alpha,beta)
    if b.is_game_over(): return score(b)
    if maxi:
        bv=-float('inf')
        for m in order_moves(b,list(b.legal_moves)):
            b.push(m); val=minimax(b,depth-1,alpha,beta,False); b.pop()
            bv=max(bv,val); alpha=max(alpha,val)
            if beta<=alpha: break
        return bv
    else:
        bv=float('inf')
        for m in order_moves(b,list(b.legal_moves)):
            b.push(m); val=minimax(b,depth-1,alpha,beta,True); b.pop()
            bv=min(bv,val); beta=min(beta,val)
            if beta<=alpha: break
        return bv

def best(b,depth=3):
    bm=None; bv=-float('inf') if b.turn==chess.WHITE else float('inf')
    for m in order_moves(b,list(b.legal_moves)):
        b.push(m); val=minimax(b,depth-1,-float('inf'),float('inf'),b.turn==chess.WHITE); b.pop()
        if b.turn==chess.WHITE and val>bv: bv,bm=val,m
        elif b.turn==chess.BLACK and val<bv: bv,bm=val,m
    return bm

@app.route("/")
def index():
    session.setdefault("fen",chess.STARTING_FEN); session.setdefault("hist",[])
    return render_template_string(HTML)

@app.route("/move",methods=["POST"])
def move():
    b=chess.Board(session.get("fen",chess.STARTING_FEN))
    try: b.push_san(request.json["move"])
    except: return jsonify(ok=False,error="Invalid move")
    hist=session["hist"]+[request.json["move"]]; eng=None
    if not b.is_game_over():
        m=best(b,depth=2)  # depth=3 is stronger but may take 2-5s; lower to 2 for faster response
        if m: eng=b.san(m); b.push(m); hist.append(eng)
    session["fen"]=b.fen(); session["hist"]=hist
    return jsonify(ok=True,fen=b.fen(),engine=eng,hist=hist,over=b.is_game_over(),result=b.result() if b.is_game_over() else None)

@app.route("/reset",methods=["POST"])
def reset():
    session["fen"]=chess.STARTING_FEN; session["hist"]=[]
    return jsonify(ok=True)

HTML = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Chess</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#f5f0e8;font-family:Georgia,serif;color:#2c2218;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:32px 16px;gap:20px}
h1{font-size:26px;font-weight:600}h1 span{font-size:13px;color:#9a8878;font-weight:400;font-style:italic;margin-left:8px}
.layout{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap;justify-content:center}
.bshell{display:flex;flex-direction:column}.brow{display:flex;align-items:center}
.rv{display:flex;flex-direction:column;width:18px;margin-right:4px}.rvc{height:52px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#9a8878;font-family:monospace}
.fh{display:flex;margin-left:22px}.fhc{width:52px;height:16px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#9a8878;font-family:monospace}
#board{display:grid;grid-template-columns:repeat(8,52px);grid-template-rows:repeat(8,52px);border:1px solid #ddd5c4;box-shadow:0 4px 16px rgba(0,0,0,.10)}
.sq{width:52px;height:52px;display:flex;align-items:center;justify-content:center;font-size:32px;user-select:none}
.light{background:#eedfc0}.dark{background:#a07848}.hl{background:rgba(80,160,80,.55)!important}.hl2{background:rgba(80,160,80,.25)!important}
.wp{color:#fff;text-shadow:0 0 3px rgba(0,0,0,.7)}.bp{color:#1a0f00;text-shadow:0 0 2px rgba(255,255,255,.3)}
.side{display:flex;flex-direction:column;gap:12px;width:220px}
.card{background:#fff;border:1px solid #ddd5c4;border-radius:8px;padding:14px 16px}
.lbl{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#9a8878;font-family:monospace;margin-bottom:10px}
.irow{display:flex;gap:8px}
input{flex:1;font-family:monospace;font-size:14px;padding:8px 10px;border:1px solid #ddd5c4;border-radius:5px;background:#f5f0e8;color:#2c2218;outline:none}
input:focus{border-color:#5a7a3a}
.btn{font-family:Georgia,serif;font-size:13px;font-weight:600;padding:8px 14px;border:none;border-radius:5px;cursor:pointer;background:#5a7a3a;color:#fff}.btn:hover{opacity:.85}
.ghost{width:100%;margin-top:8px;background:transparent;border:1px solid #ddd5c4;color:#9a8878;font-size:12px;padding:7px;border-radius:5px;cursor:pointer;font-family:Georgia,serif}.ghost:hover{color:#2c2218;border-color:#bbb}
#err{display:none;margin-top:8px;font-size:12px;color:#b04040;font-style:italic}
#status{font-size:14px}#eng{display:none;margin-top:8px;font-family:monospace;font-size:15px;font-weight:600;color:#5a7a3a}
#hist{font-family:monospace;font-size:12px;color:#9a8878;line-height:1.9;max-height:130px;overflow-y:auto;word-break:break-word}
</style></head><body>
<h1>Chess <span>minimax · alpha-beta · quiescence</span></h1>
<div class="layout">
  <div class="bshell">
    <div class="brow"><div class="rv" id="rv"></div><div id="board"></div></div>
    <div class="fh" id="fh"></div>
  </div>
  <div class="side">
    <div class="card"><div class="lbl">Your move</div><div class="irow"><input id="mi" placeholder="e4, Nf3, O-O …" autocomplete="off"><button class="btn" onclick="go()">Play</button></div><button class="ghost" onclick="rst()">↺ new game</button><div id="err"></div></div>
    <div class="card"><div class="lbl">Engine</div><div id="status">White to move</div><div id="eng"></div></div>
    <div class="card"><div class="lbl">Moves</div><div id="hist">—</div></div>
  </div>
</div>
<script>
const F=['a','b','c','d','e','f','g','h'],SYM={p:'♟',r:'♜',n:'♞',b:'♝',q:'♛',k:'♚',P:'♙',R:'♖',N:'♘',B:'♗',Q:'♕',K:'♔'};
let g=new Chess(),hf=null,ht=null;
const rv=document.getElementById('rv');
for(let r=8;r>=1;r--){const d=document.createElement('div');d.className='rvc';d.textContent=r;rv.appendChild(d);}
const fh=document.getElementById('fh');const sp=document.createElement('div');sp.style.cssText='width:22px;flex-shrink:0';fh.appendChild(sp);
F.forEach(f=>{const d=document.createElement('div');d.className='fhc';d.textContent=f;fh.appendChild(d);});
function draw(fen){if(fen)g.load(fen);const b=document.getElementById('board');b.innerHTML='';for(let r=7;r>=0;r--)for(let c=0;c<8;c++){const sq=F[c]+(r+1),p=g.get(sq),d=document.createElement('div');d.className='sq '+((r+c)%2?'light':'dark')+(sq==hf?' hl':sq==ht?' hl2':'');if(p){d.textContent=SYM[p.color=='w'?p.type.toUpperCase():p.type];d.classList.add(p.color=='w'?'wp':'bp');}b.appendChild(d);}}
function showErr(m){const e=document.getElementById('err');e.textContent=m;e.style.display='block';setTimeout(()=>e.style.display='none',2800);}
function renderHist(h){if(!h.length){document.getElementById('hist').innerHTML='—';return;}let html='';h.forEach((m,i)=>{if(i%2==0)html+=`<span style="color:#c0b0a0">${i/2+1}.</span> `;html+=m+(i%2==0?' ':'<br>');});const el=document.getElementById('hist');el.innerHTML=html;el.scrollTop=el.scrollHeight;}
async function go(){const s=document.getElementById('mi').value.trim();if(!s)return;const t=g.move(s,{sloppy:true});if(!t)return showErr('Not valid — try e4, Nf3, O-O');g.undo();document.getElementById('status').textContent='Thinking…';const d=await(await fetch('/move',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({move:s})})).json();if(!d.ok)return showErr(d.error);document.getElementById('mi').value='';hf=t.from;ht=t.to;draw(d.fen);renderHist(d.hist);const eng=document.getElementById('eng');if(d.engine){eng.textContent='→ '+d.engine;eng.style.display='block';}else eng.style.display='none';document.getElementById('status').textContent=d.over?'Game over — '+d.result:'White to move';}
async function rst(){await fetch('/reset',{method:'POST'});g=new Chess();hf=ht=null;draw();renderHist([]);document.getElementById('status').textContent='White to move';document.getElementById('eng').style.display='none';}
document.getElementById('mi').addEventListener('keydown',e=>{if(e.key=='Enter')go();});
draw();
</script></body></html>"""

if __name__ == "__main__":
    print("Open http://localhost:5000")
    app.run(debug=True)

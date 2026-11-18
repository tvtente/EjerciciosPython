function OrderSelector({data = [], selected = null, onPick}) {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const W=720, H=340, L=60, R=25, T=25, B=55;
  const px = v => L + (v-7)/13*(W-L-R);
  const py = v => H-B-v/14*(H-T-B);
  const point = e => {
    const box=e.currentTarget.getBoundingClientRect();
    return {x:Math.max(L,Math.min(W-R,(e.clientX-box.left)/box.width*W)),
            y:Math.max(T,Math.min(H-B,(e.clientY-box.top)/box.height*H))};
  };
  const toggle = id => {
    // Primer clic desde "sin filtro" inicia una selección individual.
    const ids = selected === null ? [] : [...selected];
    onPick(ids.includes(id) ? ids.filter(x=>x!==id) : [...ids,id]);
  };
  const finish = e => {
    if (!start) return;
    const last=point(e);
    if (Math.abs(start.x-last.x)+Math.abs(start.y-last.y)>4) {
      onPick(data.filter(r=>px(r.hour)>=Math.min(start.x,last.x) && px(r.hour)<=Math.max(start.x,last.x)
        && py(r.units)>=Math.min(start.y,last.y) && py(r.units)<=Math.max(start.y,last.y)).map(r=>r.id));
    }
    setStart(null);setEnd(null);
    if(e.currentTarget.hasPointerCapture(e.pointerId)) e.currentTarget.releasePointerCapture(e.pointerId);
  };
  return <svg viewBox={`0 0 ${W} ${H}`} width="100%" role="group"
    aria-label="Pedidos: arrastra un rectángulo o pulsa un punto para seleccionar"
    style={{display:'block',background:'white',touchAction:'none',userSelect:'none',minHeight:240}}
    onPointerDown={e=>{if(e.button!==0)return; const p=point(e);setStart(p);setEnd(p);e.currentTarget.setPointerCapture(e.pointerId);}}
    onPointerMove={e=>{if(start)setEnd(point(e));}} onPointerUp={finish}
    onPointerCancel={()=>{setStart(null);setEnd(null);}}>
    {[0,2,4,6,8,10,12,14].map(v=><g key={'y'+v}>
      <line x1={L} x2={W-R} y1={py(v)} y2={py(v)} stroke="#e2e8f0"/>
      <text x={L-12} y={py(v)+4} textAnchor="end" fontSize="12" fill="#475569">{v}</text>
    </g>)}
    {[8,10,12,14,16,18,20].map(v=><g key={'x'+v}>
      <text x={px(v)} y={H-B+23} textAnchor="middle" fontSize="12" fill="#475569">{v}:00</text>
    </g>)}
    <line x1={L} x2={W-R} y1={H-B} y2={H-B} stroke="#64748b"/>
    <text x={W/2} y={H-8} textAnchor="middle" fontSize="13" fill="#334155">Hora del pedido</text>
    <text x="17" y={H/2} textAnchor="middle" transform={`rotate(-90 17 ${H/2})`} fontSize="13" fill="#334155">Unidades</text>
    {data.map(r=>{
      const active=selected===null||selected.includes(r.id);
      return <circle key={r.id} cx={px(r.hour)} cy={py(r.units)} r={active?9:7}
        fill={active?'#4f46e5':'#cbd5e1'} stroke={active?'#312e81':'#94a3b8'} strokeWidth="2"
        role="button" tabIndex="0" aria-label={`${r.id}, ${r.city}, ${r.units} unidades, ${r.revenue} euros`}
        aria-pressed={selected!==null&&selected.includes(r.id)} style={{cursor:'pointer'}}
        onPointerDown={e=>e.stopPropagation()} onClick={e=>{e.stopPropagation();toggle(r.id);}}
        onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle(r.id);}}}>
        <title>{`${r.id} · ${r.city} · ${r.revenue} €`}</title>
      </circle>;
    })}
    {start&&end&&<rect x={Math.min(start.x,end.x)} y={Math.min(start.y,end.y)}
      width={Math.abs(end.x-start.x)} height={Math.abs(end.y-start.y)}
      fill="#6366f122" stroke="#4f46e5" strokeDasharray="5 3" pointerEvents="none"/>}
  </svg>;
}

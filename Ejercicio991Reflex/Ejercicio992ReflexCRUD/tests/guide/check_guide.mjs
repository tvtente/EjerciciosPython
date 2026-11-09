/** Browser-independent checks for the generated local HTML.
 * Exercises the actual inline JavaScript with a small in-memory DOM adapter.
 * Does not launch a browser, open the editor, or read/write the clipboard.
 */
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=fs.readFileSync(new URL('../../entregables/guia_crud_interactiva.html',import.meta.url),'utf8');
const data=JSON.parse(html.match(/<script id="guide-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const events={},elements=new Map(),store=new Map();let clipboard='',lastDownload=null;
class Element{
 constructor(id=''){this.id=id;this.innerHTML='';this.textContent='';this.hidden=false;this.disabled=false;this.value='';this.attrs={};this.dataset={};this.scrollTop=0;this.listeners={};this.style={};this.classList={toggle:(name,on)=>{const v=on??!this.classes?.has(name);this.classes??=new Set();v?this.classes.add(name):this.classes.delete(name);return v;},contains:name=>this.classes?.has(name)||false,add:name=>{this.classes??=new Set();this.classes.add(name);},remove:name=>this.classes?.delete(name)};this.offsetTop=id.startsWith('line-')?Number(id.slice(5))*24:0;}
 addEventListener(n,fn){this.listeners[n]=fn;}
 setAttribute(k,v){this.attrs[k]=String(v);}getAttribute(k){return this.attrs[k]??null;}removeAttribute(k){delete this.attrs[k];}
 querySelectorAll(sel){if(sel==='button')return[...this.innerHTML.matchAll(/<button[^>]*data-flow="([^"]+)"/g)].map(m=>{const e=new Element();e.dataset.flow=m[1];return e;});return[];}
 scrollIntoView(){}focus(){document.activeElement=this;}append(){}remove(){}select(){}click(){if(this.download)lastDownload=this.download;}closest(){return this;}
}
for(const m of html.matchAll(/\bid="([^"]+)"/g))if(!elements.has(m[1]))elements.set(m[1],new Element(m[1]));
elements.get('guide-data').textContent=JSON.stringify(data);
const document={getElementById:id=>{if(id.startsWith('line-')&&!elements.has(id))elements.set(id,new Element(id));return elements.get(id)||null;},querySelectorAll:()=>[],addEventListener:(n,fn)=>events['document:'+n]=fn,createElement:()=>new Element(),body:new Element('body'),activeElement:{tagName:'BODY'},title:''};
const location={hash:''},stack=[{hash:'',state:null}];let cursor=0;
const history={replaceState(state,_,hash){stack[cursor]={hash,state};location.hash=hash;},pushState(state,_,hash){stack.splice(cursor+1);stack.push({hash,state});cursor++;location.hash=hash;},back(){if(cursor){cursor--;location.hash=stack[cursor].hash;events.popstate({state:stack[cursor].state});}},forward(){if(cursor<stack.length-1){cursor++;location.hash=stack[cursor].hash;events.popstate({state:stack[cursor].state});}}};
const context={document,location,history,URLSearchParams,URL:{createObjectURL:()=> 'blob:memory',revokeObjectURL:()=>{}},Blob,innerWidth:1440,navigator:{clipboard:{writeText:async value=>{clipboard=value;}}},localStorage:{getItem:key=>store.get(key),setItem:(k,v)=>store.set(k,v)},setTimeout:()=>1,clearTimeout(){},console};
context.window=context;context.isSecureContext=true;context.addEventListener=(n,fn)=>events[n]=fn;
vm.createContext(context);vm.runInContext(script,context);
const run=code=>vm.runInContext(code,context);
assert.equal(run('state.symbol'),'TodoState.add_todo');assert.ok(elements.get('codeBody').innerHTML.includes('data-symbol="TodoRepository.create"'));
run("symbolRoute('TodoRepository.create')");assert.equal(run('currentFile'),'todo_app/repository.py');assert.match(elements.get('theory').innerHTML,/validate_text/);
run("symbolRoute('validate_text')");assert.equal(run('selectedSymbol().start'),30);
history.back();assert.equal(run('state.symbol'),'TodoRepository.create');history.forward();assert.equal(run('state.symbol'),'validate_text');
for(const id of Object.keys(data.flows)){run(`setFlow(${JSON.stringify(id)})`);for(let i=0;i<data.flows[id].steps.length;i++){run(`pickStep(${i})`);assert.equal(run('state.symbol'),data.flows[id].steps[i].target);assert.ok(elements.get('diagram').innerHTML.includes('<svg'));}}
run("symbolRoute('TodoRepository.create'); symbolRoute('concept:Session.commit')");assert.equal(run('currentFile'),'todo_app/repository.py');assert.match(elements.get('theory').innerHTML,/Concepto externo/);
run("symbolRoute('Todo')");history.back();assert.equal(run('currentFile'),'todo_app/repository.py');
run("navigate({file:'todo_app/database.py',symbol:null,line:24})");assert.equal(run('state.line'),24);assert.match(elements.get('codeBody').innerHTML,/line-target/);
elements.get('search').value='create_all';run('search()');assert.match(elements.get('searchResults').innerHTML,/create_all/);
elements.get('search').value='zzzinexistentezzz';run('search()');assert.match(elements.get('searchResults').innerHTML,/No hay coincidencias/);
elements.get('search').value='';run('search()');assert.equal(elements.get('navigation').hidden,false);
run("symbolRoute('TodoRepository.create')");await elements.get('copyFile').listeners.click();assert.equal(clipboard,data.files['todo_app/repository.py'].source);
await elements.get('copySymbol').listeners.click();assert.equal(clipboard,data.files['todo_app/repository.py'].source.split('\n').slice(50,58).join('\n'));
elements.get('downloadFile').listeners.click();assert.equal(lastDownload,'repository.py');
run("symbolRoute('NoExiste')"); // Verify invalid fragment fallback through the actual decoder.
location.hash='#symbol=NoExiste';const fallback=run('readHash()');assert.equal(fallback.symbol,data.flows.create.entry);
// The shared guide must not depend on an editor or a machine-specific path.
assert.equal(data.projectRoot,undefined);
assert.ok(!html.includes('vscode://'));
assert.ok(!html.includes('/home/tvt/'));
assert.ok(!html.includes('Configurar la ruta'));
// All generated code anchors and graph targets resolve to a known symbol.
let links=0;for(const record of Object.values(data.files))for(const line of record.lines)for(const m of line.matchAll(/data-symbol="([^"]+)"/g)){assert.ok(data.symbols[m[1]],m[1]);links++;}
for(const s of Object.values(data.symbols))for(const target of [...s.calls,...s.references,...s.usedBy])assert.ok(data.symbols[target],target);
console.log(`OK: ${Object.keys(data.files).length} archivos, ${links} enlaces de código, ${Object.keys(data.flows).length} recorridos. Navegación, historial, búsqueda, copia exacta, descarga, conceptos y portabilidad comprobados sin navegador.`);

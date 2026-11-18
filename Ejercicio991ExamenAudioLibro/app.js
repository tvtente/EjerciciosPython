'use strict';
const form = document.querySelector('#download-form');
const message = document.querySelector('#mensaje');
const count = document.querySelector('#registros');
const storageKey = 'examenAudiolibroRegistros';
function readRecords() {
  const data = localStorage.getItem(storageKey);
  if (!data) return [];
  const records = JSON.parse(data);
  if (!Array.isArray(records)) throw new Error('Formato de registros incorrecto');
  return records;
}
function updateCount() {
  try { const n = readRecords().length; count.textContent = `${n} registro${n === 1 ? '' : 's'} guardado${n === 1 ? '' : 's'} en este navegador.`; }
  catch { count.textContent = 'No se pueden leer los registros de este navegador.'; }
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  message.textContent = '';
  try {
    const records = readRecords();
    records.push({ fecha: new Date().toISOString(), nombre: form.nombre.value.trim(), apellidos: form.apellidos.value.trim(), email: form.email.value.trim(), perfil: form.perfil.value });
    localStorage.setItem(storageKey, JSON.stringify(records));
    activeEmail = form.email.value.trim().toLocaleLowerCase();
    setAccess(records[records.length - 1]);
    form.reset(); updateCount();
    message.textContent = 'Registro completado.';
    if (dialog.open) dialog.close();
  } catch {
    message.textContent = 'No se ha podido guardar el registro en este navegador. Comprueba que el almacenamiento esté disponible.';
  }
});
document.querySelector('#exportar').addEventListener('click', () => {
  try {
    const records = readRecords();
    if (!records.length) { count.textContent = 'Todavía no hay registros para exportar.'; return; }
    const columns = ['fecha', 'nombre', 'apellidos', 'email', 'perfil'];
    const escapeCell = value => {
      let text = String(value ?? '');
      if (/^[\s]*[=+\-@\t\r]/.test(text)) text = "'" + text;
      return '"' + text.replace(/"/g, '""') + '"';
    };
    const csv = '\ufeff' + [columns.map(escapeCell).join(';'), ...records.map(record => columns.map(key => escapeCell(record[key])).join(';'))].join('\r\n');
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const link = document.createElement('a'); link.href = url; link.download = 'registros-audiolibro.csv';
    document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 60000);
    updateCount();
  } catch { count.textContent = 'No se han podido exportar los registros.'; }
});
updateCount();



const returnForm = document.querySelector('#return-form');
const returnMessage = document.querySelector('#return-message');
returnForm.addEventListener('submit', event => {
  event.preventDefault();
  try {
    const email = document.querySelector('#return-email').value.trim().toLocaleLowerCase();
    const person = readRecords().find(record => String(record.email || '').trim().toLocaleLowerCase() === email);
    if (person) {
      activeEmail = email;
      setAccess(person);
      returnMessage.textContent = `Hola, ${person.nombre}. Ya puedes descargar el audiolibro.`;
    } else {
      returnMessage.textContent = 'No encontramos ese correo en este navegador. Completa el formulario para registrarte.';
    }
  } catch {
    returnMessage.textContent = 'No se pueden consultar los registros de este navegador.';
  }
});
document.querySelector('#return-email').addEventListener('input', () => {
  returnMessage.textContent = '';
});
const dialog = document.querySelector('#access-dialog');
const card = document.querySelector('.form-card');
const originalParent = card.parentNode;
const originalNext = card.nextSibling;
const modalSlot = document.querySelector('#modal-form-slot');
const modalMessage = document.querySelector('#modal-login-message');
let activeEmail = '';
document.querySelector('#listen-button').addEventListener('click', event => {
  event.preventDefault();
  if (activeEmail) { downloadAudiobook(event); return; }
  modalSlot.appendChild(card);
  modalMessage.textContent = activeEmail ? 'Ya puedes descargar tu audiolibro.' : '';
  dialog.showModal();
});
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => {
  stopSample('');
  originalParent.insertBefore(card, originalNext);
  document.querySelector('#listen-button').focus();
});
document.querySelector('#modal-login').addEventListener('submit', event => {
  event.preventDefault();
  try {
    const email = document.querySelector('#modal-email').value.trim().toLocaleLowerCase();
    const person = readRecords().find(record => String(record.email || '').trim().toLocaleLowerCase() === email);
    if (person) {
      activeEmail = email;
      setAccess(person);
      modalMessage.textContent = `Hola, ${person.nombre}. Ya puedes descargar el audiolibro.`;
      dialog.close();
    } else {
      modalMessage.textContent = 'No encontramos ese correo en este navegador. Puedes registrarte abajo.';
    }
  } catch { modalMessage.textContent = 'No se pueden consultar los registros de este navegador.'; }
});
document.querySelector('#modal-email').addEventListener('input', () => { modalMessage.textContent = ''; });
// Conservamos la locución mientras el navegador la reproduce.
const samplePlay = document.querySelector('#sample-play');
const sampleStop = document.querySelector('#sample-stop');
const sampleStatus = document.querySelector('#sample-status');
const sampleVoice = document.querySelector('#sample-voice');
let sampleVoices = [];

function loadSampleVoices() {
  if (!('speechSynthesis' in window)) {
    sampleVoice.innerHTML = '<option value="">Voces no disponibles</option>';
    return;
  }
  const previous = sampleVoice.value;
  const voices = window.speechSynthesis.getVoices();
  const language = window.siteLang || 'es';
  sampleVoices = voices.filter(voice => voice.lang.toLowerCase().startsWith(language)).slice(0, 3);
  sampleVoice.replaceChildren();
  if (!sampleVoices.length) {
    sampleVoice.add(new Option(window.siteLang === 'ca' ? 'No hi ha veus disponibles per a aquest idioma' : 'No hay voces disponibles para este idioma', ''));
    return;
  }
  sampleVoices.forEach((voice, index) => sampleVoice.add(new Option(voice.name + ' (' + voice.lang + ')', String(index))));
  if (previous !== '' && Number(previous) < sampleVoices.length) sampleVoice.value = previous;
  else {
    const spanishSpain = sampleVoices.findIndex(voice => /^es[-_]ES/i.test(voice.lang));
    sampleVoice.value = String(spanishSpain >= 0 ? spanishSpain : 0);
  }
}
if ('speechSynthesis' in window) {
  loadSampleVoices();
  window.speechSynthesis.addEventListener('voiceschanged', loadSampleVoices);
} else { loadSampleVoices(); }
let sampleUtterance = null;
let sampleRun = 0;
let sampleState = 'idle';

function setSampleState(state, text) {
  sampleState = state;
  samplePlay.disabled = state === 'starting';
  samplePlay.textContent = state === 'playing' ? 'Ⅱ Pausar' : state === 'paused' ? '▶ Continuar' : '▶ Escuchar muestra';
  sampleStop.disabled = state === 'idle';
  sampleStatus.textContent = text;
}
function stopSample(text = 'Muestra detenida.') {
  sampleRun++;
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  sampleUtterance = null;
  setSampleState('idle', text);
}
samplePlay.addEventListener('click', () => {
  if (sampleState === 'playing') {
    window.speechSynthesis.pause();
    setSampleState('paused', 'Muestra en pausa.');
    return;
  }
  if (sampleState === 'paused') {
    window.speechSynthesis.resume();
    setSampleState('playing', 'Reproduciendo muestra…');
    return;
  }
  if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
    setSampleState('idle', 'Este navegador no admite lectura en voz alta. Puedes leer la muestra en pantalla.');
    return;
  }
  const synth = window.speechSynthesis;
  if (!sampleVoices.length) { setSampleState('idle', window.siteLang === 'ca' ? 'No hi ha cap veu instal·lada per a aquest idioma.' : 'No hay ninguna voz instalada para este idioma.'); return; }
  synth.cancel();
  // Algunos navegadores conservan el estado de pausa tras cancelar.
  synth.resume();
  const run = ++sampleRun;
  sampleUtterance = new SpeechSynthesisUtterance(document.querySelector('#sample-text').textContent.trim());
  sampleUtterance.lang = 'es-ES';
  const voice = sampleVoices[Number(sampleVoice.value)];
  if (voice) { sampleUtterance.voice = voice; sampleUtterance.lang = voice.lang; }
  sampleUtterance.onstart = () => {
    if (run === sampleRun) setSampleState('playing', 'Reproduciendo muestra…');
  };
  sampleUtterance.onend = () => {
    if (run === sampleRun) { sampleUtterance = null; setSampleState('idle', 'Muestra terminada.'); }
  };
  sampleUtterance.onerror = event => {
    if (run === sampleRun) {
      sampleUtterance = null;
      setSampleState('idle', 'No se pudo reproducir la voz. Comprueba las voces instaladas y el volumen del dispositivo.');
    }
  };
  setSampleState('starting', 'Preparando la voz…');
  try { synth.speak(sampleUtterance); }
  catch { if (run === sampleRun) setSampleState('idle', 'No se pudo iniciar la voz en este navegador.'); }
});
sampleStop.addEventListener('click', () => stopSample());
document.querySelector('#export-json').addEventListener('click', () => {
  try {
    const records = readRecords();
    if (!records.length) { count.textContent = 'Todavía no hay registros para exportar.'; return; }
    const url = URL.createObjectURL(new Blob([JSON.stringify(records, null, 2)], { type: 'application/json;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'data.json';
    document.body.appendChild(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 60000);
    count.textContent = 'Archivo data.json descargado. Guárdalo en un lugar seguro.';
  } catch { count.textContent = 'No se han podido exportar los registros.'; }
});
document.querySelector('#import-json').addEventListener('change', async event => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    const imported = JSON.parse(await file.text());
    if (!Array.isArray(imported) || !imported.every(record => record && typeof record === 'object' && !Array.isArray(record) && ['fecha', 'nombre', 'apellidos', 'email', 'perfil'].every(key => typeof record[key] === 'string') && record.email.trim())) throw new Error('Formato inválido');
    const records = readRecords();
    const known = new Set(records.map(record => JSON.stringify([record.fecha, record.nombre, record.apellidos, record.email, record.perfil])));
    let added = 0;
    for (const record of imported) {
      const clean = Object.fromEntries(['fecha', 'nombre', 'apellidos', 'email', 'perfil'].map(key => [key, record[key]]));
      const key = JSON.stringify([clean.fecha, clean.nombre, clean.apellidos, clean.email, clean.perfil]);
      if (!known.has(key)) { records.push(clean); known.add(key); added++; }
    }
    localStorage.setItem(storageKey, JSON.stringify(records));
    count.textContent = `Importación completada: ${added} registro(s) añadido(s). Total: ${records.length}.`;
  } catch { count.textContent = 'No se pudo importar el archivo. Comprueba que sea un data.json válido de esta página.'; }
  event.target.value = '';
});

function createAudiobookUrl() {
  const isCatalan = window.siteLang === 'ca';
  const chapterJson = JSON.stringify(isCatalan ? catalanChapters : audiobookChapters).replace(/</g, '\\u003c');
  const template = isCatalan ? catalanPlayerTemplate(audiobookTemplate) : audiobookTemplate;
  const html = template.replace('__CHAPTERS_JSON__', () => chapterJson).replace('const list=ordered.length?ordered:voices;', 'const list=ordered.slice(0,3);').replace("synth.cancel();runToken++;index=0;playing=true;paused=false;setButtons();speakNext(runToken);", "if (!voices[Number(voiceSelect.value)] || !voiceSelect.value) { statusEl.textContent = document.documentElement.lang === 'ca' ? 'Instal·la una veu catalana per escoltar l’audiollibre.' : 'Instala una voz española para escuchar el audiolibro.'; return; } synth.cancel();runToken++;index=0;playing=true;paused=false;setButtons();speakNext(runToken);");
  return URL.createObjectURL(new Blob([html], { type: 'text/html;charset=utf-8' }));
}
function downloadAudiobook(event) {
  event.preventDefault();
  const url = createAudiobookUrl();
  const link = document.createElement('a');
  link.href = url;
  link.download = 'Audiolibro_Usabilidad_Accesibilidad.html';
  document.body.appendChild(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}

const adminDialog = document.querySelector('#admin-dialog');
document.querySelector('#open-admin').addEventListener('click', () => adminDialog.showModal());
document.querySelector('#close-admin').addEventListener('click', () => adminDialog.close());
const onlineButton = document.querySelector('#online-button');
const sampleDetails = document.querySelector('#sample-details');
onlineButton.addEventListener('click', () => {
  if (activeEmail) {
    const url = createAudiobookUrl();
    const player = window.open(url, '_blank');
    if (!player) {
      URL.revokeObjectURL(url);
      returnMessage.textContent = 'Permite las ventanas emergentes para abrir el audiolibro completo.';
    } else {
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    }
    return;
  }
  modalSlot.appendChild(card);
  dialog.showModal();
  sampleDetails.open = true;
  sampleDetails.querySelector('summary').focus();
});

function setAccess(person) {
  document.querySelector('#user-status').textContent = `◉ ${person.nombre}`;
  document.querySelector('#user-status').classList.add('signed-in');
  document.querySelector('.returning').hidden = true;
  document.querySelector('#logout').hidden = false;
  const button = document.querySelector('#listen-button');
  button.classList.add('download-ready');
  button.setAttribute('aria-label', 'Descargar audiolibro completo');
  onlineButton.textContent = '▶ Escuchar audiolibro completo';
}







document.querySelector('#logout').addEventListener('click', () => {
  activeEmail = '';
  document.querySelector('#user-status').textContent = '◉ Invitado';
  document.querySelector('#user-status').classList.remove('signed-in');
  document.querySelector('#logout').hidden = true;
  document.querySelector('.returning').hidden = false;
  returnForm.reset();
  returnMessage.textContent = '';
  document.querySelector('#modal-login').reset();
  modalMessage.textContent = '';
  const button = document.querySelector('#listen-button');
  button.classList.remove('download-ready');
  button.removeAttribute('aria-label');
  onlineButton.textContent = '▶ Escuchar muestra en línea';
  document.querySelector('#return-email').focus();
});



document.querySelector('#open-register').addEventListener('click', () => {
  modalSlot.appendChild(card);
  dialog.showModal();
  document.querySelector('#nombre').focus();
});

'use strict';
window.siteLang = 'es';
const translations = {
  'Saltar al contenido':'Ves al contingut', 'ESCUCHAR PARA INCLUIR':'ESCOLTAR PER INCLOURE', '◉ Invitado':'◉ Convidat', 'Salir':'Sortir', 'Gestionar registros':'Gestionar registres',
  '¿Ya te registraste?':'Ja t’has registrat?', 'Correo electrónico registrado':'Correu electrònic registrat', 'Acceder →':'Accedir →', 'AUDIOLIBRO GRATUITO':'AUDIOLLIBRE GRATUÏT',
  'Diseñar para todos':'Dissenyar per a tothom', 'empieza por escuchar.':'comença per escoltar.', 'Descubre cómo la usabilidad y la accesibilidad hacen del mundo digital un lugar más inclusivo.':'Descobreix com la usabilitat i l’accessibilitat fan del món digital un lloc més inclusiu.',
  'Descargar audiolibro':'Descarregar audiollibre', '▶ Escuchar muestra en línea':'▶ Escoltar una mostra en línia', '▶ Escuchar audiolibro completo':'▶ Escoltar l’audiollibre complet',
  'Escucha un fragmento aquí o regístrate para descargar el contenido completo.':'Escolta un fragment aquí o registra’t per descarregar el contingut complet.', 'Escucha con intención.':'Escolta amb intenció.', 'Diseña sin barreras.':'Dissenya sense barreres.',
  'EL CONOCIMIENTO SE COMPARTE':'EL CONEIXEMENT ES COMPARTEIX', 'Consigue tu audiolibro':'Aconsegueix el teu audiollibre', 'Nombre *':'Nom *', 'Apellidos *':'Cognoms *', 'Correo electrónico *':'Correu electrònic *', '¿A qué te dedicas? *':'A què et dediques? *', 'Selecciona una opción':'Selecciona una opció', 'Estudiante':'Estudiant', 'Diseño':'Disseny', 'Desarrollo':'Desenvolupament', 'Educación':'Educació', 'Otra profesión':'Una altra professió',
  'Acepto que mis datos se guarden en este navegador para registrar la descarga.':'Accepto que les meves dades es desin en aquest navegador per registrar la descàrrega.', '(obligatorio)':'(obligatori)', 'Registrarme':'Registrar-me', 'Registrarse':'Registrar-se', '* Campos obligatorios. Tus datos permanecen en este navegador.':'* Camps obligatoris. Les dades es mantenen en aquest navegador.', 'Usabilidad y accesibilidad para todas las personas.':'Usabilitat i accessibilitat per a totes les persones.',
  'Tu próxima escucha empieza aquí':'La teva propera escolta comença aquí', '¿Ya te registraste? Introduce tu correo':'Ja t’has registrat? Introdueix el correu', 'Acceder':'Accedir', 'Escuchar una muestra en línea':'Escoltar una mostra en línia',
  'Bienvenido a este audiolibro de estudio sobre usabilidad y accesibilidad en Internet. Esta guía breve presenta la situación actual en 2026. El objetivo es comprender qué significan la usabilidad y la accesibilidad web, por qué son importantes y cómo se aplican en el diseño de sitios y aplicaciones.':'Benvingut a aquest audiollibre d’estudi sobre usabilitat i accessibilitat a Internet. Aquesta guia breu presenta la situació actual el 2026. L’objectiu és comprendre què signifiquen la usabilitat i l’accessibilitat web, per què són importants i com s’apliquen al disseny de llocs i aplicacions.',
  'Voz del navegador':'Veu del navegador', '▶ Escuchar muestra':'▶ Escoltar la mostra', 'Ⅱ Pausar':'Ⅱ Pausar', '▶ Continuar':'▶ Continuar', '■ Detener':'■ Aturar', 'Los registros se guardan en este navegador. Puedes exportarlos o recuperar una copia JSON.':'Els registres es desen en aquest navegador. Pots exportar-los o recuperar una còpia JSON.', 'Descargar registros CSV ↓':'Descarregar registres CSV ↓', 'Descargar data.json ↓':'Descarregar data.json ↓', 'Importar registros JSON':'Importar registres JSON',
  'No se ha podido guardar el registro en este navegador. Comprueba que el almacenamiento esté disponible.':'No s’ha pogut desar el registre en aquest navegador. Comprova que l’emmagatzematge estigui disponible.', 'No se han podido exportar los registros.':'No s’han pogut exportar els registres.', 'Todavía no hay registros para exportar.':'Encara no hi ha registres per exportar.', 'No se pudo iniciar la voz en este navegador.':'No s’ha pogut iniciar la veu en aquest navegador.', 'Este navegador no admite lectura en voz alta. Puedes leer la muestra en pantalla.':'Aquest navegador no admet lectura en veu alta. Pots llegir la mostra a la pantalla.', 'No se pudo reproducir la voz. Comprueba las voces instaladas y el volumen del dispositivo.':'No s’ha pogut reproduir la veu. Comprova les veus instal·lades i el volum del dispositiu.', 'Archivo data.json descargado. Guárdalo en un lugar seguro.':'Fitxer data.json descarregat. Desa’l en un lloc segur.', 'Preparando la voz…':'Preparant la veu…', 'Reproduciendo muestra…':'Reproduint la mostra…', 'Muestra en pausa.':'Mostra en pausa.', 'Muestra detenida.':'Mostra aturada.', 'Muestra terminada.':'Mostra acabada.', 'Registro completado.':'Registre completat.', 'No encontramos ese correo en este navegador. Completa el formulario para registrarte.':'No hem trobat aquest correu en aquest navegador. Omple el formulari per registrar-te.', 'No encontramos ese correo en este navegador. Puedes registrarte abajo.':'No hem trobat aquest correu en aquest navegador. Pots registrar-te a continuació.', 'No se pueden consultar los registros de este navegador.':'No es poden consultar els registres d’aquest navegador.'
};
const originals = new WeakMap();
const attributeOriginals = new WeakMap();
function translatePage() {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.parentElement.closest('script, style, #language')) continue;
    const raw = node.nodeValue;
    const text = raw.trim();
    if (!text) continue;
    if (!originals.has(node)) originals.set(node, text);
    let original = originals.get(node);
    if (text !== original && text !== translations[original]) {
      const reverse = Object.keys(translations).find(key => translations[key] === text);
      original = reverse || text; originals.set(node, original);
    }
    let target = window.siteLang === 'ca' ? (translations[original] || original) : original;
    if (window.siteLang === 'ca') {
      target = target.replace(/^Hola, (.+)\. Ya puedes descargar el audiolibro\.$/, 'Hola, $1. Ja pots descarregar l’audiollibre.');
      target = target.replace(/^(\d+) registros? guardados? en este navegador\.$/, '$1 registre(s) desat(s) en aquest navegador.');
    }
    const updated = raw.replace(text, target);
    if (updated !== raw) node.nodeValue = updated;
  }
  document.querySelectorAll('[placeholder],[aria-label]').forEach(element => {
    for (const attr of ['placeholder','aria-label']) {
      if (!element.hasAttribute(attr)) continue;
      let values = attributeOriginals.get(element) || {};
      if (!(attr in values)) values[attr] = element.getAttribute(attr);
      attributeOriginals.set(element, values);
      const map = {'Tu correo electrónico':'El teu correu electrònic','Tu nombre':'El teu nom','Tus apellidos':'Els teus cognoms','Cerrar ventana':'Tancar la finestra','Ilustración de auriculares y ondas de sonido':'Il·lustració d’uns auriculars i ones de so','Descargar audiolibro completo':'Descarregar l’audiollibre complet'};
      element.setAttribute(attr, window.siteLang === 'ca' ? (map[values[attr]] || values[attr]) : values[attr]);
    }
  });
  document.documentElement.lang = window.siteLang;
}
function catalanPlayerTemplate(html) {
  const pairs = [
    ['lang="es"','lang="ca"'], ['Usabilidad y accesibilidad en Internet','Usabilitat i accessibilitat a Internet'],
    ['Audiolibro de estudio · basado en el dosier PDF adjunto · septiembre de 2026','Audiollibre d’estudi · basat en el dossier PDF adjunt · setembre de 2026'],
    ['Controles del audiolibro','Controls de l’audiollibre'], ['▶ Reproducir','▶ Reproduir'], ['Ⅱ Pausar','Ⅱ Pausar'], ['▶ Continuar','▶ Continuar'], ['■ Detener','■ Aturar'], ['Voz de Windows','Veu del navegador'], ['Cargando voces disponibles…','Carregant les veus disponibles…'], ['Velocidad','Velocitat'], ['Lenta','Lenta'], ['Normal','Normal'], ['Ágil','Àgil'], ['Rápida','Ràpida'],
    ['Preparado. Selecciona una voz española y pulsa Reproducir.','Preparat. Selecciona una veu catalana i prem Reproduir.'],
    ['La voz se obtiene de las voces instaladas en Windows y disponibles para el navegador. Para una voz masculina de España, selecciona «Microsoft Álvaro» si aparece en la lista.','La veu prové de les veus instal·lades al dispositiu i disponibles per al navegador.'],
    ['Contenido del audiolibro','Contingut de l’audiollibre'], ['Uso recomendado: abre este archivo con doble clic en Microsoft Edge o Google Chrome. No necesita conexión a Internet, pero sí una voz española instalada en Windows.','Obre aquest fitxer amb doble clic en un navegador compatible. Cal tenir instal·lada una veu catalana.'],
    ['/^es(-|_)/i','/^ca(-|_)/i'], ['/spanish|español/i','/catalan|català/i'], ['/es-ES/i','/ca-ES/i'], ['/^es-ES/i','/^ca-ES/i'], ["|| list.find(v=>/^ca-ES/i.test(v.lang))",'|| list.find(v=>/^ca-ES/i.test(v.lang))'],
    ['Audiolibro finalizado.','Audiollibre finalitzat.'], ['Reproduciendo: ','Reproduint: '], ['No se pudo reproducir este fragmento (','No s’ha pogut reproduir aquest fragment ('], ['). Comprueba la voz instalada.','). Comprova la veu instal·lada.'], ['Este navegador no admite síntesis de voz.','Aquest navegador no admet síntesi de veu.'], ['Audiolibro pausado.','Audiollibre en pausa.'], ['Continuando…','Continuant…'], ['Reproducción detenida.','Reproducció aturada.'], ['Voces disponibles: ','Veus disponibles: '], ['. Voz seleccionada: ','. Veu seleccionada: '], ['No se detectan voces instaladas','No s’han detectat veus instal·lades'], ['No se detectan voces. Instala una voz de español (España) en la configuración de Windows.','No s’han detectat veus. Instal·la una veu catalana al dispositiu.'], ['es-ES','ca-ES']
  ];
  for (const [from,to] of pairs) html = html.split(from).join(to);
  return html;
}
document.querySelector('#language').addEventListener('change', event => {
  stopSample('');
  window.siteLang = event.target.value;
  loadSampleVoices();
  translatePage();
});
translatePage();

let translationQueued = false;
new MutationObserver(() => {
  if (window.siteLang !== 'ca' || translationQueued) return;
  translationQueued = true;
  queueMicrotask(() => { translationQueued = false; translatePage(); });
}).observe(document.body, { childList: true, subtree: true, characterData: true });




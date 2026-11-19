// Residata S.R.L. — comportamiento del sitio. Sin dependencias.
const CORREO = 'rekteado@gmail.com';
const FORMSUBMIT = `https://formsubmit.co/ajax/${CORREO}`;
const API = 'https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com/api/';
const APP = 'https://dsu-uagrm.vercel.app/';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const sinMovimiento = matchMedia('(prefers-reduced-motion: reduce)').matches;
// Miles con espacio fino: el punto de la fuente matricial se confunde con un signo
const kg = (n) => n.toLocaleString('es-BO', { maximumFractionDigits: 1 }).replace(/\./g, '\u202f');

// Tablas: cada celda conserva el rótulo de su columna para la vista móvil en bloques
$$('.tarifario').forEach((t) => {
  const rotulos = $$('thead tr:first-child th', t).map((h) => h.textContent.trim());
  $$('tr', t).forEach((tr) => [...tr.children].forEach((c, i) => { if (c.tagName === 'TD') c.dataset.rotulo = rotulos[i] || ''; }));
});

// Menú móvil
const abrir = $('.abrir-menu');
if (abrir) abrir.addEventListener('click', () => {
  const m = $('.menu'); const v = !m.classList.contains('abierto');
  m.classList.toggle('abierto', v); abrir.setAttribute('aria-expanded', v);
});

// El ticket se imprime línea por línea
$$('.imprime').forEach((t) => {
  $$('.linea', t).forEach((l, i) => l.style.setProperty('--i', i));
  requestAnimationFrame(() => requestAnimationFrame(() => t.classList.add('listo')));
});

// Líneas guía de las capturas anotadas: se dibujan desde el rótulo hasta el punto
function guias(fig) {
  const svg = $('.guias', fig); if (!svg) return;
  const caja = fig.getBoundingClientRect();
  svg.setAttribute('viewBox', `0 0 ${caja.width} ${caja.height}`);
  svg.innerHTML = '';
  $$('.llamada', fig).forEach((ll) => {
    const r = $('.rotulo', ll).getBoundingClientRect();
    const [px, py] = ll.dataset.punto.split(',').map(Number);
    const x2 = (px / 100) * caja.width, y2 = (py / 100) * caja.height;
    const izquierda = r.left - caja.left > x2;
    const x1 = (izquierda ? r.left : r.right) - caja.left, y1 = r.top - caja.top + r.height / 2;
    // Trazo ortogonal: sale del rótulo, baja o sube en el margen y entra recto al punto
    const img = $('.captura', fig).getBoundingClientRect();
    const codo = izquierda ? x1 - 14 : (x1 + (img.left - caja.left)) / 2;
    // data-via: altura (%) de un pasillo libre por donde cruza antes de bajar al elemento
    const via = ll.dataset.via ? (Number(ll.dataset.via) / 100) * caja.height : null;
    const d = via === null ? `M${x1},${y1} H${codo} V${y2} H${x2}` : `M${x1},${y1} H${codo} V${via} H${x2} V${y2}`;
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', d); svg.append(p);
    const largo = Math.ceil(p.getTotalLength()); p.style.setProperty('--largo', largo);
    // Remate: trazo corto perpendicular al último tramo, junto al borde del elemento
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    const llegaVertical = via !== null;
    c.setAttribute('x1', llegaVertical ? x2 - 6 : x2); c.setAttribute('x2', llegaVertical ? x2 + 6 : x2);
    c.setAttribute('y1', llegaVertical ? y2 : y2 - 6); c.setAttribute('y2', llegaVertical ? y2 : y2 + 6); svg.append(c);
  });
}
$$('.anotado figure').forEach((fig) => {
  const dibujar = () => guias(fig);
  addEventListener('resize', dibujar); addEventListener('load', dibujar); dibujar();
  new IntersectionObserver(([e], o) => {
    if (e.isIntersecting) { fig.closest('.anotado').classList.add('visto'); o.disconnect(); }
  }, { threshold: 0.35 }).observe(fig);
});

// Calendario académico con el pronóstico
const cal = $('#calendario');
if (cal) {
  const datos = JSON.parse($('#datos-calendario').textContent);
  const max = Math.max(...datos.semanas.map((s) => s.kg + (s.margen || 0)));
  const barras = $('.semanas', cal), regla = $('.regla', cal);
  cal.style.setProperty('--n', datos.semanas.length);
  const meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  let mesPrevio = -1;
  datos.semanas.forEach((s, i) => {
    // Barras decorativas: el control accesible (teclado y tacto) es el deslizador
    const b = document.createElement('span');
    b.className = 'semana'; b.dataset.p = s.periodo; b.dataset.i = i;
    b.innerHTML = `<i style="--h:${(s.kg / max) * 100}%"></i>`;
    barras.append(b);
    const m = Number(s.desde.slice(3, 5)) - 1, span = document.createElement('span');
    if (m !== mesPrevio) { span.textContent = meses[m]; span.className = 'mes'; mesPrevio = m; }
    regla.append(span);
  });
  const deslizador = $('.deslizador', cal);
  deslizador.max = datos.semanas.length - 1;
  const mostrar = (i) => {
    const s = datos.semanas[i];
    $$('.semana', cal).forEach((b) => b.toggleAttribute('data-sel', b.dataset.i == i));
    deslizador.setAttribute('aria-valuetext', `Semana del ${s.desde}: ${(s.margen ? 'aproximadamente ' : '') + kg(s.kg)} kg, ${s.etiqueta}`);
    $('[data-l=kg]', cal).textContent = (s.margen ? '≈ ' : '') + kg(s.kg);
    $('[data-l=margen]', cal).textContent = s.margen ? `± ${String(s.margen).replace('.', ',')} kg · modelo ${s.modelo}` : 'kg pesados';
    $('[data-l=semana]', cal).textContent = `Semana del ${s.desde}`;
    $('[data-l=periodo]', cal).textContent = s.etiqueta;
    deslizador.value = i;
  };
  barras.addEventListener('click', (e) => { const b = e.target.closest('.semana'); if (b) mostrar(+b.dataset.i); });
  deslizador.addEventListener('input', () => mostrar(+deslizador.value));
  mostrar(datos.semanas.length - 1);
}

// Formularios: envío por FormSubmit al correo de la empresa
async function enviar(datos) {
  const r = await fetch(FORMSUBMIT, {
    method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({ _template: 'table', _captcha: 'false', ...datos }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || String(j.success) === 'false') throw new Error(j.message || `HTTP ${r.status}`);
  return j;
}
$$('form[data-envio]').forEach((f) => {
  f.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (f._honey && f._honey.value) return;
    const salida = $('.resultado', f), boton = $('button[type=submit]', f);
    const datos = Object.fromEntries(new FormData(f));
    delete datos._honey;
    datos._subject = `${f.dataset.envio} — ${datos.institucion || datos.nombre || 'sitio web'}`;
    boton.disabled = true; salida.className = 'resultado'; salida.textContent = 'Enviando…';
    try {
      await enviar(datos);
      salida.classList.add('ok');
      salida.textContent = f.dataset.gracias || 'Recibido. Le respondemos por correo en menos de un día hábil.';
      f.reset();
    } catch (err) {
      salida.classList.add('error');
      salida.innerHTML = `No se pudo enviar (${err.message}). Escríbanos directamente a <a href="mailto:${CORREO}">${CORREO}</a>.`;
    } finally { boton.disabled = false; }
  });
});

// Estado del servicio: la API responde 401 sin sesión, lo que confirma que está en línea
// La app web permite CORS (*) y bloquea no-cors por su política CORP; la API admite no-cors.
async function sondear(url, mode) {
  const t0 = performance.now();
  try { await fetch(url, { mode, cache: 'no-store' }); return Math.round(performance.now() - t0); }
  catch { return null; }
}
const estado = $('#estado-servicio');
if (estado) (async () => {
  for (const [sel, url, modo] of [['[data-s=app]', APP, 'cors'], ['[data-s=api]', API, 'no-cors']]) {
    const ms = await sondear(url, modo), b = $(sel, estado);
    b.textContent = ms === null ? 'Sin respuesta' : `En línea · ${ms} ms`;
    b.className = ms === null ? 'mal-t' : 'ok-t';
  }
  $('[data-s=hora]', estado).textContent = new Date().toLocaleString('es-BO');
})();

// Asistente: responde desde la base de conocimiento y deriva a una persona del equipo
const BASE = [
  { c: ['precio', 'plan', 'costo', 'cuesta', 'tarifa', 'pagar', 'suscrip'], r: 'Hay tres planes: <b>Inicial</b> sin costo (hasta 15 puntos), <b>Campus</b> a Bs 2 900 al mes y <b>Red</b> a Bs 7 500 al mes. El pago anual equivale a diez meses. <a href="planes.html">Ver planes</a>.' },
  { c: ['gratis', 'freemium', 'inicial', 'prueba'], r: 'El plan <b>Inicial</b> es gratuito sin límite de tiempo: una sede, hasta 15 puntos de recolección y 5 usuarios, con registro en campo, jornadas y tablero. No incluye predicción.' },
  { c: ['predic', 'random', 'forest', 'pronost', 'modelo', 'ia', 'inteligencia'], r: 'Residata entrena un <b>Random Forest Regressor</b> con el histórico de su institución (punto, tipo de residuo, día, semana y periodo académico) y pronostica kilos por punto con su margen de error. Está en los planes Campus y Red.' },
  { c: ['sensor', 'iot', 'hardware', 'balanza', 'bascula', 'báscula', 'equipo'], r: 'No necesita sensores ni contenedores especiales. El personal registra el peso desde el navegador del teléfono con la balanza que ya usa.' },
  { c: ['celular', 'telefono', 'teléfono', 'movil', 'móvil', 'app', 'instalar', 'android', 'iphone'], r: 'Funciona en el navegador de cualquier teléfono o computadora; no hay que instalar nada. La pantalla de campo está pensada para una mano y botones grandes.' },
  { c: ['demo', 'demostr', 'ver', 'probar'], r: 'Podemos mostrarle el sistema funcionando con datos de demostración. <a href="contacto.html">Solicite una demostración</a> y coordinamos fecha.' },
  { c: ['dato', 'segur', 'privac', 'respaldo', 'backup'], r: 'Los datos viajan cifrados (TLS), cada rol ve solo lo que le corresponde, toda operación queda en una bitácora y la base se respalda cada día. Detalle en la <a href="privacidad.html">política de privacidad</a>.' },
  { c: ['contrase', 'clave', 'acceso', 'ingresar', 'login', 'usuario'], r: 'Si olvidó su contraseña, el administrador de su institución la restablece desde Usuarios. Si el administrador no puede ingresar, abra un ticket y lo atendemos.' },
  { c: ['factura', 'nit', 'impuesto', 'iva'], r: 'Los precios publicados incluyen los impuestos de ley y se emite factura electrónica en línea.' },
  { c: ['power bi', 'powerbi', 'tablero', 'reporte', 'excel', 'pdf'], r: 'Incluye tablero de indicadores, mapa de calor y reportes en Excel y PDF. El plan Red agrega la conexión de solo lectura para Power BI.' },
  { c: ['capacita', 'curso', 'manual', 'aprender'], r: 'Cada plan de pago incluye capacitación inicial por rol. El manual de usuario por rol está en la sección de soporte.' },
  { c: ['novedad', 'version', 'versión', 'actualiza', 'cambio'], r: 'Publicamos cada versión en <a href="novedades.html">Novedades</a>, también disponible por RSS.' },
];
const NORM = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
function responder(texto) {
  const t = NORM(texto); let mejor = null, puntos = 0;
  for (const e of BASE) { const p = e.c.filter((k) => t.includes(NORM(k))).length; if (p > puntos) { puntos = p; mejor = e; } }
  return mejor ? mejor.r : null;
}
function asistente() {
  const boton = document.createElement('button');
  boton.className = 'asistente-boton'; boton.type = 'button';
  boton.setAttribute('aria-controls', 'asistente'); boton.setAttribute('aria-expanded', 'false');
  boton.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg><span>Asistente</span>';
  const panel = document.createElement('section');
  panel.className = 'asistente'; panel.id = 'asistente'; panel.setAttribute('aria-label', 'Asistente de Residata');
  panel.innerHTML = `<header><div><b>Asistente Residata</b><span>Respuestas inmediatas · un agente del equipo atiende lo demás</span></div><button type="button" aria-label="Cerrar asistente"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6 6 18"/></svg></button></header>
    <div class="charla" role="log" aria-live="polite"></div>
    <div class="sugerencias"></div>
    <form class="escribir"><label class="sr" for="pregunta">Escriba su pregunta</label><input id="pregunta" autocomplete="off" placeholder="Escriba su pregunta"><button>Enviar</button></form>`;
  document.body.append(boton, panel);
  const charla = $('.charla', panel), sug = $('.sugerencias', panel);
  const globo = (html, quien) => { const d = document.createElement('div'); d.className = `globo ${quien}`; d.innerHTML = html; charla.append(d); charla.scrollTop = charla.scrollHeight; return d; };
  const chips = (lista) => { sug.innerHTML = ''; lista.forEach(([t, f]) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.onclick = f; sug.append(b); }); };
  const preguntar = (t) => {
    globo(t.replace(/</g, '&lt;'), 'yo');
    const r = responder(t);
    if (r) { globo(r, 'bot'); chips([['¿Algo más?', () => $('#pregunta').focus()], ['Hablar con una persona', agente]]); }
    else { globo('No tengo esa respuesta en mi base. Le paso con una persona del equipo: deje sus datos y le escribimos.', 'bot'); agente(); }
  };
  function agente() {
    chips([]);
    const id = `RD-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-${Math.floor(1000 + Math.random() * 9000)}`;
    const d = globo(`<form class="ticket-form"><p style="margin:0 0 8px">Ticket <b>${id}</b> para un agente de soporte:</p>
      <div class="campo"><label for="t-nombre">Nombre</label><input id="t-nombre" name="nombre" required autocomplete="name"></div>
      <div class="campo"><label for="t-correo">Correo</label><input id="t-correo" name="email" type="email" required autocomplete="email"></div>
      <div class="campo"><label for="t-msg">Consulta</label><textarea id="t-msg" name="mensaje" required></textarea></div>
      <button class="boton primario" style="height:42px;width:100%">Abrir ticket</button><p class="resultado"></p></form>`, 'bot');
    const f = $('form', d);
    f.addEventListener('submit', async (e) => {
      e.preventDefault(); const s = $('.resultado', f), b = $('button', f); b.disabled = true; s.textContent = 'Enviando…';
      try {
        await enviar({ ...Object.fromEntries(new FormData(f)), ticket: id, origen: location.pathname, conversacion: [...charla.querySelectorAll('.globo.yo')].map((g) => g.textContent).join(' | '), _subject: `Ticket ${id} — soporte Residata` });
        s.className = 'resultado ok'; s.textContent = `Ticket ${id} abierto. Un agente le responde por correo dentro del horario de soporte.`; f.querySelectorAll('input,textarea,button').forEach((x) => (x.disabled = true));
      } catch (err) { s.className = 'resultado error'; s.innerHTML = `No se pudo abrir el ticket. Escriba a <a href="mailto:${CORREO}?subject=Ticket%20${id}">${CORREO}</a>.`; b.disabled = false; }
    });
  }
  const abrirPanel = (v) => {
    panel.classList.toggle('abierto', v); boton.setAttribute('aria-expanded', v);
    if (v && !charla.childElementCount) {
      globo('Hola. Respondo sobre planes, funcionamiento, seguridad y acceso. Si necesita algo más, le paso con un agente del equipo.', 'bot');
      chips([['¿Cuánto cuesta?', () => preguntar('¿Cuánto cuesta?')], ['¿Necesito sensores?', () => preguntar('¿Necesito sensores?')], ['¿Cómo predice?', () => preguntar('¿Cómo funciona la predicción?')], ['Hablar con una persona', agente]]);
    }
    if (v) $('#pregunta').focus();
  };
  boton.onclick = () => abrirPanel(!panel.classList.contains('abierto'));
  $('header button', panel).onclick = () => { abrirPanel(false); boton.focus(); };
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && panel.classList.contains('abierto')) { abrirPanel(false); boton.focus(); } });
  $('.escribir', panel).addEventListener('submit', (e) => { e.preventDefault(); const i = $('#pregunta'); if (i.value.trim()) { preguntar(i.value.trim()); i.value = ''; } });
  $$('[data-abrir-asistente]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); abrirPanel(true); }));
}
asistente();
if (sinMovimiento) document.documentElement.classList.add('quieto');

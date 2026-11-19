// Ejecuta la función real del sitio contra respuestas simuladas, sin peticiones a producción.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const fuente = fs.readFileSync(__dirname + '/js/site.js', 'utf8');
const funcion = fuente.slice(fuente.indexOf('async function sondear'), fuente.indexOf('const estado ='));
(async () => {
  let actual;
  const entorno = vm.createContext({ API: '/api/', performance, AbortSignal, fetch: async () => actual });
  vm.runInContext(funcion, entorno);
  for (const [status, ok] of [[200, true], [404, false], [500, false]]) {
    actual = { status, type: 'basic' };
    assert.equal(Boolean(await entorno.sondear('/app/', 'cors')), ok);
  }
  actual = { status: 401, type: 'basic' };
  assert.equal((await entorno.sondear('/api/', 'cors')).verificable, true);
  actual = { status: 0, type: 'opaque' };
  assert.equal((await entorno.sondear('/api/', 'no-cors')).verificable, false);
  entorno.fetch = async () => { throw new Error('sin red'); };
  assert.equal(await entorno.sondear('/app/', 'cors'), null);
  console.log('6 escenarios de salud aprobados: 200, 404, 500, API 401, opaco y fallo de red.');
})();

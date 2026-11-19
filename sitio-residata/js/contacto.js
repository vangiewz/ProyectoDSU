// Preselecciona el motivo cuando se llega desde un plan (planes.html?plan=campus)
const plan = new URLSearchParams(location.search).get('plan');
const motivo = document.getElementById('c-tipo');
if (plan && motivo) [...motivo.options].forEach((o) => { if (o.text.toLowerCase().includes(plan)) motivo.value = o.text; });

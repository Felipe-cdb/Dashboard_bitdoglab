let visitsChart;
let conversionChart;
let tempChart;

// Simples buffer para gráfico (tempo real)
const labels = [];
const visitsData = [];
const salesData = [];
const tempData = [];

async function carregarEstado() {
  const r = await fetch("/api/state");
  const data = await r.json();

  document.getElementById("visits").innerText = data.visits;
  document.getElementById("sales").innerText = data.sales;
  document.getElementById("temp").innerText = data.temperature ?? "--";
  document.getElementById("hum").innerText = data.humidity ?? "--";

  const hora = new Date().toLocaleTimeString();

  labels.push(hora);
  visitsData.push(data.visits);
  salesData.push(data.sales);
  tempData.push(data.temperature ?? 0);

  if (labels.length > 10) {
    labels.shift();
    visitsData.shift();
    salesData.shift();
    tempData.shift();
  }

  visitsChart.update();
  conversionChart.update();
  tempChart.update();
}

function initCharts() {
  visitsChart = new Chart(document.getElementById("chartVisits"), {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Visitas",
          data: visitsData,
          borderWidth: 3,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });

  conversionChart = new Chart(document.getElementById("chartConversion"), {
    type: "doughnut",
    data: {
      labels: ["Vendas", "Não converteram"],
      datasets: [
        {
          data: [0, 0],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });

  tempChart = new Chart(document.getElementById("chartTemp"), {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Temperatura (°C)",
          data: tempData,
          borderDash: [5, 5],
          borderWidth: 2,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

// Atualiza gráfico de conversão
function atualizarConversao() {
  const vendas = salesData.at(-1) || 0;
  const visitas = visitsData.at(-1) || 0;

  conversionChart.data.datasets[0].data = [
    vendas,
    Math.max(visitas - vendas, 0),
  ];
}

// Ciclo
initCharts();
carregarEstado();

setInterval(() => {
  carregarEstado().then(atualizarConversao);
}, 2000);

let tempChart;
let humChart;

/* =========================
   CARREGAR DADOS REAIS
========================= */
async function carregarEnvironment() {
  const r = await fetch("/api/environment/summary");
  const data = await r.json();

  // KPIs
  document.getElementById("avgTemp").innerText =
    data.avg_temp ?? "--";

  document.getElementById("avgHum").innerText =
    data.avg_humidity ?? "--";

  document.getElementById("maxTemp").innerText =
    data.max_temp ?? "--";

  // Conforto térmico simples
  let comfort = "Ideal";
  if (data.avg_temp > 28) comfort = "Quente";
  if (data.avg_temp < 20) comfort = "Frio";

  document.getElementById("comfortStatus").innerText = comfort;

  // Dados horários
  const labels = [];
  const temps = [];
  const hums = [];

  for (let h = 8; h <= 22; h++) {
    const key = String(h).padStart(2, "0");
    labels.push(`${key}h`);

    temps.push(data.hourly[key]?.temperature ?? null);
    hums.push(data.hourly[key]?.humidity ?? null);
  }

  // Atualiza gráficos
  tempChart.data.labels = labels;
  tempChart.data.datasets[0].data = temps;
  tempChart.update();

  humChart.data.labels = labels;
  humChart.data.datasets[0].data = hums;
  humChart.update();
}

/* =========================
   INIT CHARTS
========================= */
function initCharts() {

  tempChart = new Chart(document.getElementById("chartTemperature"), {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "Temperatura (°C)",
        borderColor: "#ef4444",
        tension: 0.4,
        data: []
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });

  humChart = new Chart(document.getElementById("chartHumidity"), {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "Umidade (%)",
        borderColor: "#0ea5e9",
        tension: 0.4,
        data: []
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

/* =========================
   INIT
========================= */
initCharts();
carregarEnvironment();

// Atualiza a cada 10s
setInterval(carregarEnvironment, 10000);

let visitsChart;
let conversionChart;
let tempChart;

/* ============================
   KPI + FUNIL (TEMPO REAL)
============================ */
async function carregarEstado() {
  const r = await fetch("/api/state");
  const data = await r.json();

  // KPIs
  document.getElementById("visits").innerText = data.visits;
  document.getElementById("sales").innerText = data.sales;
  document.getElementById("temp").innerText = data.temperature ?? "--";
  document.getElementById("hum").innerText = data.humidity ?? "--";

  // Funil
  const vendas = data.sales;
  const visitas = data.visits;

  conversionChart.data.datasets[0].data = [
    vendas,
    Math.max(visitas - vendas, 0),
  ];
  conversionChart.update();
}

/* ============================
   GRÁFICOS HORÁRIOS (AGREGADO)
============================ */
async function carregarGraficosHorarios() {
  const r = await fetch("/api/dashboard/hourly");
  const data = await r.json();

  const hours = [];
  const visits = [];
  const sales = [];
  const temps = [];

  for (let h = 8; h <= 22; h++) {
    const key = String(h).padStart(2, "0");
    hours.push(`${key}h`);
    visits.push(data.visits[key] || 0);
    sales.push(data.sales[key] || 0);
    temps.push(data.temperature[key] || null);
  }

  // Chart Visits
  visitsChart.data.labels = hours;
  visitsChart.data.datasets[0].data = visits;
  visitsChart.data.datasets[1].data = sales;
  visitsChart.update();

  // Chart Temp
  tempChart.data.labels = hours;
  tempChart.data.datasets[0].data = sales;
  tempChart.data.datasets[1].data = temps;
  tempChart.update();
}

/* ============================
   INIT CHARTS
============================ */
function initCharts() {

  // VISITAS x VENDAS
  visitsChart = new Chart(document.getElementById("chartVisits"), {
    type: "bar",
    data: {
      labels: [],
      datasets: [
        {
          label: "Visitantes",
          backgroundColor: "rgba(37,99,235,0.5)",
          data: []
        },
        {
          label: "Vendas",
          type: "line",
          borderColor: "#10b981",
          borderWidth: 3,
          tension: 0.4,
          data: []
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });

  // FUNIL
  conversionChart = new Chart(document.getElementById("chartConversion"), {
    type: "doughnut",
    data: {
      labels: ["Vendas", "Não converteram"],
      datasets: [{
        label: "Funil de Vendas",
        data: [0, 0],
        backgroundColor: ["#10b981", "#e5e7eb"]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });

  // TEMPERATURA x VENDAS
  tempChart = new Chart(document.getElementById("chartTemp"), {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Vendas",
          borderColor: "#10b981",
          tension: 0.4,
          yAxisID: "y",
          data: []
        },
        {
          label: "Temperatura (°C)",
          borderColor: "#ef4444",
          borderDash: [5, 5],
          tension: 0.4,
          yAxisID: "y1",
          data: []
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { position: "left", beginAtZero: true },
        y1: { position: "right", grid: { drawOnChartArea: false } }
      }
    }
  });
}

/* ============================
   CICLO DE ATUALIZAÇÃO
============================ */
initCharts();

// Inicial
carregarEstado();
carregarGraficosHorarios();

// Ciclos
setInterval(carregarEstado, 2000);          // KPIs + Funil
setInterval(carregarGraficosHorarios, 5000); // Gráficos horários

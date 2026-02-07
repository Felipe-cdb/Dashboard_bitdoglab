let tempChart;
let humChart;
let tempVsSalesChart;

/* =========================
   MOCK DATA (AMBIENTE)
========================= */
const hours = ["08h", "10h", "12h", "14h", "16h", "18h", "20h"];
const temperatures = [22, 24, 26, 28, 29, 27, 25];
const humidity = [68, 65, 60, 58, 55, 57, 60];
const sales = [5, 12, 20, 28, 26, 18, 10];

/* =========================
   KPIs
========================= */
function carregarKPIs() {
  const avgTemp =
    temperatures.reduce((a, b) => a + b, 0) / temperatures.length;

  const avgHum =
    humidity.reduce((a, b) => a + b, 0) / humidity.length;

  const maxTemp = Math.max(...temperatures);

  document.getElementById("avgTemp").innerText = avgTemp.toFixed(1);
  document.getElementById("avgHum").innerText = avgHum.toFixed(0);
  document.getElementById("maxTemp").innerText = maxTemp;

  // Conforto térmico simples
  let comfort = "Ideal";
  if (avgTemp > 28) comfort = "Quente";
  if (avgTemp < 20) comfort = "Frio";

  document.getElementById("comfortStatus").innerText = comfort;
}

/* =========================
   INIT CHARTS
========================= */
function initCharts() {

  // TEMPERATURA
  tempChart = new Chart(document.getElementById("chartTemperature"), {
    type: "line",
    data: {
      labels: hours,
      datasets: [{
        label: "Temperatura (°C)",
        borderColor: "#ef4444",
        tension: 0.4,
        data: temperatures
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // UMIDADE
  humChart = new Chart(document.getElementById("chartHumidity"), {
    type: "line",
    data: {
      labels: hours,
      datasets: [{
        label: "Umidade (%)",
        borderColor: "#0ea5e9",
        tension: 0.4,
        data: humidity
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // TEMP x VENDAS
  tempVsSalesChart = new Chart(
    document.getElementById("chartTempVsSales"),
    {
      type: "line",
      data: {
        labels: hours,
        datasets: [
          {
            label: "Vendas",
            borderColor: "#10b981",
            tension: 0.4,
            yAxisID: "y",
            data: sales
          },
          {
            label: "Temperatura (°C)",
            borderColor: "#ef4444",
            borderDash: [5, 5],
            tension: 0.4,
            yAxisID: "y1",
            data: temperatures
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
    }
  );
}

/* =========================
   INIT
========================= */
carregarKPIs();
initCharts();

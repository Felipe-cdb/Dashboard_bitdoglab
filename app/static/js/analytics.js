let monthlyChart;
let conversionTrendChart;
let tempVsSalesChart;

/* =========================
   MOCK DATA (TEMPORÁRIO)
========================= */
const months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"];
const visits = [320, 410, 380, 460, 520, 610];
const sales = [40, 62, 55, 78, 91, 120];
const temps = [24, 26, 25, 27, 29, 30];

/* =========================
   KPIs
========================= */
function carregarKPIs() {
  document.getElementById("totalVisits").innerText =
    visits.reduce((a, b) => a + b, 0);

  document.getElementById("totalSales").innerText =
    sales.reduce((a, b) => a + b, 0);

  const conversion =
    (sales.reduce((a, b) => a + b, 0) /
      visits.reduce((a, b) => a + b, 0)) * 100;

  document.getElementById("avgConversion").innerText =
    conversion.toFixed(1);

  document.getElementById("avgTemp").innerText =
    (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1);
}

/* =========================
   INIT CHARTS
========================= */
function initCharts() {

  // VISITAS x VENDAS (MENSAL)
  monthlyChart = new Chart(document.getElementById("chartMonthly"), {
    type: "bar",
    data: {
      labels: months,
      datasets: [
        {
          label: "Visitas",
          backgroundColor: "rgba(37,99,235,0.5)",
          data: visits
        },
        {
          label: "Vendas",
          backgroundColor: "rgba(16,185,129,0.7)",
          data: sales
        }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // TENDÊNCIA DE CONVERSÃO
  conversionTrendChart = new Chart(
    document.getElementById("chartConversionTrend"),
    {
      type: "line",
      data: {
        labels: months,
        datasets: [{
          label: "Conversão (%)",
          borderColor: "#6366f1",
          tension: 0.4,
          data: months.map((_, i) =>
            ((sales[i] / visits[i]) * 100).toFixed(1)
          )
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    }
  );

  // TEMPERATURA x VENDAS
  tempVsSalesChart = new Chart(
    document.getElementById("chartTempVsSales"),
    {
      type: "line",
      data: {
        labels: months,
        datasets: [
          {
            label: "Vendas",
            borderColor: "#10b981",
            tension: 0.4,
            yAxisID: "y",
            data: sales
          },
          {
            label: "Temperatura Média (°C)",
            borderColor: "#ef4444",
            borderDash: [5, 5],
            tension: 0.4,
            yAxisID: "y1",
            data: temps
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

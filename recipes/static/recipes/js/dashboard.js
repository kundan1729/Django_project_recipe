document.addEventListener('DOMContentLoaded', function() {
  const analytics = window.DASHBOARD_ANALYTICS || {labels: ['Easy','Medium','Hard'], data: [0,0,0] };
  const ctx = document.getElementById('difficultyChart');
  if (!ctx) return;
  new Chart(ctx.getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: analytics.labels,
      datasets: [{ data: analytics.data, backgroundColor: ['#34D399','#60A5FA','#F97316'] }]
    },
    options: { responsive: true }
  });
});

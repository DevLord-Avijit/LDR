setInterval(async () => {
  const res = await fetch('/status');
  const data = await res.json();
  document.getElementById('status').textContent = data.laser_status;
  document.getElementById('pos').textContent = data.position || "--";
}, 500);

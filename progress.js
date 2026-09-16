(async () => {
  const status = document.getElementById('progress-status');
  try {
    const response = await fetch('progress.json', {cache: 'no-store'});
    if (!response.ok) throw new Error('Progress unavailable');
    const data = await response.json();
    const checked = new Date(data.checkedAt);
    if (!Number.isInteger(data.sold) || data.sold < 0 || !Number.isInteger(data.goal) || data.goal <= 0 || !Number.isFinite(checked.getTime())) throw new Error('Invalid progress');
    document.getElementById('items-sold').textContent = data.sold.toLocaleString();
    document.getElementById('items-goal').textContent = data.goal.toLocaleString();
    const meter = document.getElementById('fundraiser-meter');
    meter.max = data.goal;
    meter.value = Math.min(data.sold, data.goal);
    meter.textContent = `${data.sold} of ${data.goal} items`;
    document.getElementById('progress-message').textContent = data.sold >= data.goal ? 'Goal reached! Thank you for supporting the arts.' : `${(data.goal - data.sold).toLocaleString()} more items to reach the goal. Every order helps!`;
    const stale = Date.now() - checked.getTime() > 3 * 60 * 60 * 1000;
    status.textContent = `${stale ? 'Last available count' : 'Last checked'}: ${checked.toLocaleString(undefined, {month:'short', day:'numeric', hour:'numeric', minute:'2-digit'})}. ${stale ? 'Check the shop for the latest total.' : 'Updates about hourly from School Shopping.'}`;
  } catch {
    status.textContent = 'The latest count is unavailable. Check the shop for current progress.';
  }
})();

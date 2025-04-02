<script lang="ts">
  import { onMount } from 'svelte';

  let scanProgress = 0;
  let metrics = {
    testingType: '',
    processedRequests: 0,
    effectivePayloads: 0,
    responseTime: ''
  };

  let results: any[] = [];
  let interval: any;

  let isPaused = false;
  let isStopped = false;

  onMount(async () => {
    await fetchScanStatus();
    interval = setInterval(fetchScanStatus, 2000);
  });

  async function fetchScanStatus() {
    try {
      const res = await fetch('http://localhost:5000/api/sql-scan-status');
      const data = await res.json();
      scanProgress = data.progress;
      metrics = data.metrics;
      results = data.results;
      isPaused = data.paused;
      if (scanProgress >= 100 || isStopped) clearInterval(interval);
    } catch (e) {
      console.error('Failed to fetch scan status:', e);
    }
  }

  async function pauseScan() {
    await fetch('http://localhost:5000/api/sql/pause', { method: 'POST' });
    isPaused = true;
  }

  async function resumeScan() {
    await fetch('http://localhost:5000/api/sql/resume', { method: 'POST' });
    isPaused = false;
  }

  async function stopScan() {
    isStopped = true;
    clearInterval(interval);
  }

  async function restartScan() {
    const confirmRestart = confirm('Are you sure you want to restart the scan?');
    if (confirmRestart) {
      await fetch('http://localhost:5000/api/sql/restart', { method: 'POST' });
      isStopped = false;
      scanProgress = 0;
      interval = setInterval(fetchScanStatus, 2000);
    }
  }
</script>

<div class="p-10 bg-white min-h-screen">
  <h1 class="text-4xl font-bold">SQL Injection</h1>
  <h2 class="text-lg text-gray-500 mb-6">Running</h2>

  <!-- Progress Indicator -->
  <div class="mb-8">
    <p class="text-sm">{scanProgress}% Scanning…</p>
    <div class="w-full bg-gray-200 rounded-full h-2">
      <div class="bg-blue-500 h-2 rounded-full" style="width: {scanProgress}%"></div>
    </div>
  </div>

  <!-- Metrics -->
  <div class="grid grid-cols-4 gap-4 text-center mb-8">
    <div>
      <p class="text-gray-500">Testing Type</p>
      <p class="font-semibold">{metrics.testingType}</p>
    </div>
    <div>
      <p class="text-gray-500">Processed Requests</p>
      <p class="font-semibold">{metrics.processedRequests}</p>
    </div>
    <div>
      <p class="text-gray-500">Effective Payloads</p>
      <p class="font-semibold">{metrics.effectivePayloads}</p>
    </div>
    <div>
      <p class="text-gray-500">Response Time</p>
      <p class="font-semibold">{metrics.responseTime}</p>
    </div>
  </div>

  <!-- Results Table -->
  <div class="overflow-x-auto mb-8">
    <table class="min-w-full border text-sm">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-2 border">#</th>
          <th class="p-2 border">Parameter</th>
          <th class="p-2 border">Method</th>
          <th class="p-2 border">Type</th>
          <th class="p-2 border">Payload</th>
          <th class="p-2 border">Status</th>
          <th class="p-2 border">Length</th>
          <th class="p-2 border">Vulnerability</th>
        </tr>
      </thead>
      <tbody>
        {#each results as row}
          <tr class="text-center">
            <td class="border p-2">{row.id}</td>
            <td class="border p-2">{row.parameter}</td>
            <td class="border p-2">{row.method}</td>
            <td class="border p-2">{row.type}</td>
            <td class="border p-2">{row.payload}</td>
            <td class="border p-2">{row.status}</td>
            <td class="border p-2">{row.length}</td>
            <td class="border p-2 text-{row.vulnerable ? 'red-500' : 'green-600'}">{row.vulnerable ? 'True' : 'False'}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  <!-- Action Buttons -->
  <div class="flex gap-4">
    {#if !isPaused}
      <button class="bg-blue-100 text-blue-700 px-4 py-2 rounded hover:bg-blue-200" on:click={pauseScan} title="Pause the scan temporarily without losing progress">Pause</button>
    {:else}
      <button class="bg-yellow-100 text-yellow-700 px-4 py-2 rounded hover:bg-yellow-200" on:click={resumeScan} title="Resume the scan">Resume</button>
    {/if}

    <button class="bg-red-100 text-red-700 px-4 py-2 rounded hover:bg-red-200" on:click={stopScan} title="Stop the scan completely">Stop</button>

    <button class="bg-gray-100 text-gray-800 px-4 py-2 rounded hover:bg-gray-200" on:click={restartScan} title="Restart the scan with confirmation">Restart</button>

    <button class="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 ml-auto" title="Open the scan terminal">Show Terminal</button>
  </div>
</div>

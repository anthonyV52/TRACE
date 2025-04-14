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
  let terminalLogs: string[] = []; 
  let structure: Record<string, any[]> = {};
  let expandedTable: string | null = null;

  let isPaused = false;
  let isStopped = false;
  let interval: any;
  let activeTab = 'scan';

  onMount(async () => {
    await fetchScanStatus();
    await fetchLogs(); 
    await fetchStructure();
    interval = setInterval(() => {
      fetchScanStatus();
      fetchLogs(); 
    }, 2000);
  });

  async function fetchScanStatus() {
    try {
      const res = await fetch('http://localhost:8000/api/sql-scan-status');
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

  async function fetchLogs() { 
    try {
      const res = await fetch('http://localhost:8000/api/sql/logs');
      const data = await res.json();
      terminalLogs = data.logs;
    } catch (e) {
      console.error('Failed to fetch terminal logs:', e);
    }
  }

  async function fetchStructure() {
    try {
      const res = await fetch('http://localhost:8000/api/sql/structure');
      structure = await res.json();
    } catch (e) {
      console.error('Failed to fetch structure:', e);
    }
  }

  async function pauseScan() {
    await fetch('http://localhost:8000/api/sql/pause', { method: 'POST' });
    isPaused = true;
  }

  async function resumeScan() {
    await fetch('http://localhost:8000/api/sql/resume', { method: 'POST' });
    isPaused = false;
  }

  async function stopScan() {
    isStopped = true;
    clearInterval(interval);
  }

  async function restartScan() {
    const confirmRestart = confirm('Are you sure you want to restart the scan?');
    if (confirmRestart) {
      await fetch('http://localhost:8000/api/sql/restart', { method: 'POST' });
      isStopped = false;
      scanProgress = 0;
      interval = setInterval(() => {
        fetchScanStatus();
        fetchLogs();
      }, 2000);
    }
  }

  function toggleTable(table: string) {
    expandedTable = expandedTable === table ? null : table;
  }
</script>

<div class="flex">
  <!-- Sidebar -->
  <aside class="w-20 bg-gray-100 min-h-screen p-4 flex flex-col gap-6 items-center border-r">
    <button class="w-10 h-10 rounded-full bg-cyan-200"></button>
    <button class="w-10 h-10 rounded-full bg-cyan-200"></button>
    <button class="w-10 h-10 rounded-full bg-cyan-200"></button>
    <button class="w-10 h-10 rounded-full bg-cyan-200"></button>
    <div class="mt-auto">
      <button class="w-10 h-10 rounded-full bg-gray-300"></button>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 p-10 bg-white flex flex-col min-h-screen items-center">
    <div class="w-full max-w-6xl">
      <h1 class="text-4xl font-bold text-center">SQL Injection</h1>
      <h2 class="text-lg text-gray-500 mb-6 text-center">Results</h2>

      <!-- Tabs -->
      <div class="flex justify-center mb-8 space-x-4">
        <button on:click={() => activeTab = 'scan'}
          class="px-4 py-2 font-semibold rounded-t-md"
          class:bg-blue-500={activeTab === 'scan'}
          class:bg-gray-200={activeTab !== 'scan'}>
          Scan Results
        </button>
        <button on:click={() => activeTab = 'structure'}
          class="px-4 py-2 font-semibold rounded-t-md"
          class:bg-blue-500={activeTab === 'structure'}
          class:bg-gray-200={activeTab !== 'structure'}>
          Database Structure
        </button>
      </div>

      {#if activeTab === 'scan'}
        <!-- Progress Indicator -->
        <div class="w-full flex justify-center items-center mb-12 px-4">
          <div class="flex items-center gap-6 w-full max-w-4xl">
            <div class="flex items-center justify-center w-12 h-12 border-2 border-cyan-500 rounded-full text-base font-bold text-gray-800">
              {scanProgress}%
            </div>
            <div class="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden shadow-inner">
              <div class="h-full bg-blue-500 transition-all duration-500 ease-in-out" style="width: {scanProgress}%;"></div>
            </div>
            <div class="text-sm font-medium text-gray-600 ml-2">Scanning…</div>
          </div>
        </div>

        <!-- Metrics -->
        <div class="w-full mb-12 flex justify-center">
          <table class="w-auto text-sm text-center table-fixed border-separate border-spacing-x-12">
            <thead>
              <tr class="text-gray-600">
                <th>Testing Type</th>
                <th>Processed Requests</th>
                <th>Effective Payloads</th>
                <th>Response Time</th>
              </tr>
            </thead>
            <tbody>
              <tr class="font-extrabold text-xl text-black">
                <td>{metrics.testingType || '—'}</td>
                <td>{metrics.processedRequests}</td>
                <td>{metrics.effectivePayloads}</td>
                <td>{metrics.responseTime}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Results Table -->
        <div class="overflow-x-auto mb-8 shadow border rounded w-full">
          <table class="min-w-full text-sm text-center">
            <thead class="bg-blue-500 text-white">
              <tr>
                <th class="p-3">#</th>
                <th class="p-3">Parameter</th>
                <th class="p-3">Method</th>
                <th class="p-3">Type</th>
                <th class="p-3">Payload</th>
                <th class="p-3">Status</th>
                <th class="p-3">Length</th>
                <th class="p-3">Vulnerable</th>
              </tr>
            </thead>
            <tbody class="bg-gray-100">
              {#each results as row}
                <tr class="border-t">
                  <td class="p-2">{row.id}</td>
                  <td class="p-2">{row.parameter}</td>
                  <td class="p-2">{row.method}</td>
                  <td class="p-2">{row.type}</td>
                  <td class="p-2">{row.payload}</td>
                  <td class="p-2">{row.status}</td>
                  <td class="p-2">{row.length}</td>
                  <td class="p-2 font-semibold text-{row.vulnerable ? 'red-500' : 'green-600'}">{row.vulnerable ? 'True' : 'False'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>

        <!-- Terminal -->
        <div class="p-4 bg-black text-white font-mono text-sm rounded h-64 overflow-y-auto shadow mb-8 border border-gray-600">
          <h3 class="text-white font-bold mb-2">Live Terminal Output</h3>
          <div class="whitespace-pre-line">
            {#each terminalLogs as log}
              <div>{log}</div>
            {/each}
          </div>
        </div>

        <!-- Controls -->
        <div class="mt-auto flex gap-4 justify-center pt-4 border-t border-gray-200 w-full">
          {#if !isPaused}
            <button class="bg-blue-500 text-black px-6 py-2 rounded hover:bg-blue-600" on:click={pauseScan}>Pause</button>
          {:else}
            <button class="bg-blue-500 text-black px-6 py-2 rounded hover:bg-blue-600" on:click={resumeScan}>Resume</button>
          {/if}
          <button class="bg-blue-500 text-black px-6 py-2 rounded hover:bg-blue-600" on:click={stopScan}>Stop</button>
          <button class="bg-blue-500 text-black px-6 py-2 rounded hover:bg-blue-600" on:click={restartScan}>Restart</button>
        </div>
      {/if}

      {#if activeTab === 'structure'}
        <div class="w-full max-w-5xl space-y-6 px-2">
          {#each Object.entries(structure) as [table, columns]}
            <div class="border shadow rounded">
              <button
                class="w-full text-left px-4 py-2 font-semibold bg-gray-100 hover:bg-gray-200"
                on:click={() => toggleTable(table)}
              >
                📁 {table}
              </button>

              {#if expandedTable === table}
                <table class="min-w-full text-sm text-left">
                  <thead class="bg-gray-200">
                    <tr>
                      <th class="p-2">Column</th>
                      <th class="p-2">Type</th>
                      <th class="p-2">Nullable</th>
                      <th class="p-2">Key</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each columns as col}
                      <tr class="border-t">
                        <td class="p-2">{col.column}</td>
                        <td class="p-2">{col.type}</td>
                        <td class="p-2">{col.nullable}</td>
                        <td class="p-2">{col.key}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              {/if}
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </main>
</div>

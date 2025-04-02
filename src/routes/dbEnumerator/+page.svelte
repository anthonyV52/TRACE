<script lang="ts">
  import { onMount } from "svelte";
  let tables = [];
  let columnNames = {};
  let tableData = {};

  // Fetch table names and columns from the backend
  async function fetchDatabaseInfo() {
    try {
      const response = await fetch("http://localhost:8000/enumerate-db");
      const data = await response.json();
      tables = data.tableNames;
      columnNames = data.columnNames;
      tableData = data.table;
    } catch (err) {
      console.error("Error fetching database information:", err);
    }
  }

  onMount(() => {
    fetchDatabaseInfo();
  });
</script>

<div class="container">
  <h1>Database Enumeration</h1>
  <button on:click={fetchDatabaseInfo}>Refresh Tables</button>

  <div class="section">
    <h2>Tables:</h2>
    <div class="table">
      {#each tables as table}
        <ul class="table-list">
          <li><strong>{table}</strong></li>
          {#each columnNames[table] as column}
            <li class="column-item">{column}</li>
          {/each}
        </ul>
      {/each}
    </div>
  </div>

  <div class="section">
    <h2>Table Data:</h2>
    <div class="tableData">
      {#each Object.keys(tableData) as table}
        <div class="table">
          <h3>{table} Data:</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Property</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {#each tableData[table] as row}
                <tr>
                  {#each Object.entries(row.properties) as [key, value]}
                    <td class="data-cell">
                      <strong>{key}:</strong> {Array.isArray(value) ? value.join(', ') : value}
                    </td>
                  {/each}
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/each}
    </div>
  </div>
</div>

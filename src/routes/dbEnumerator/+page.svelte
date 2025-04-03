<script lang="ts">
  import { onMount } from "svelte";
  let projects = [];
  let tableData = {};
  let searchQuery = "";

  async function fetchDatabaseInfo() {
    try {
      const response = await fetch("http://localhost:8000/enumerate-db");
      const data = await response.json();
      tableData = data.table; // Table data from the backend
    } catch (err) {
      console.error("Error fetching database information:", err);
    }
  }

  function searchProjects() {
    // Filter the projects based on the search query
    projects = Object.values(tableData.Project).flat().filter((project: any) => 
      project.properties.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }

  onMount(() => {
    fetchDatabaseInfo();
  });
</script>

<div class="container">
  <h1>Database Enumeration</h1>
  <button on:click={fetchDatabaseInfo}>Refresh Tables</button>

  <!-- Projects Section -->
  <div class="section">
    <h2>Projects:</h2>

    <!-- Search bar for projects -->
    <input 
      type="text" 
      placeholder="Search for a project..." 
      bind:value={searchQuery} 
      on:input={searchProjects}
      class="search-bar"
    />

    <!-- Scrollable projects list -->
    <div class="projects-list">
      {#each projects as project}
        <div class="project-item">
          <strong>{project.properties.name}</strong><br />
          <span>Owner: {project.properties.owner}</span><br />
          <span>Locked: {project.properties.isLocked ? "🔒" : "🔓"}</span><br />
          <span>ID: {project.properties.id}</span><br />
          <span>IP List: {project.properties.IPList.join(", ")}</span><br />
          <span>Files: {project.properties.files.join(", ")}</span><br />
        </div>
      {/each}
    </div>
  </div>

  <!-- Table Data Section (only if needed) -->
  <div class="section" style="display: none;"> <!-- Hide this section for now -->
    <h2>Table Data:</h2>
    <div class="tableData">
      {#each Object.keys(tableData) as table}
        <ul>
          <li><strong>{table}</strong></li>
          {#each tableData[table] as row}
            <li>{JSON.stringify(row)}</li>
          {/each}
        </ul>
      {/each}
    </div>
  </div>
</div>

<!-- Add some basic styling here for your search bar and layout -->
<style>
  .container {
    padding: 20px;
  }

  .search-bar {
    padding: 10px;
    width: 100%;
    margin-bottom: 20px;
    font-size: 16px;
  }

  .projects-list {
    max-height: 400px; /* Limit height for scrolling */
    overflow-y: auto;  /* Enable vertical scrolling */
    padding-right: 10px;
    border: 1px solid #ccc;
    background-color: #f9f9f9;
  }

  .project-item {
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }

  .project-item:last-child {
    border-bottom: none;
  }

  .section {
    margin-bottom: 30px;
  }

  h1, h2 {
    font-family: 'Arial', sans-serif;
    color: #333;
  }
</style>

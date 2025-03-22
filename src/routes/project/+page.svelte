<script lang="ts">
    let name: string = "";
    let owner_id: string = "";
    let message: string = "";
  
    interface Project {
      id: number;
      name: string;
      owner_id: number;
    }
  
    let projects: Project[] = [];
    let showDialog: boolean = false;
  
    async function createProject() {
      try {
        const response = await fetch("http://localhost:8000/project/create", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name,
            owner_id: parseInt(owner_id)
          })
        });
  
        const result = await response.json();
  
        if (response.ok) {
          message = `✅ ${result.message} (ID: ${result.project_id})`;
          projects.push({ id: result.project_id, name, owner_id: parseInt(owner_id) });
          showDialog = false;
          name = "";
          owner_id = "";
        } else {
          message = `❌ ${result.detail || 'Error creating project'}`;
        }
      } catch (err) {
        if (err instanceof Error) {
          message = `❌ ${err.message}`;
        } else {
          message = `❌ An unknown error occurred.`;
        }
      }
    }
  
    function exportProjects() {
      const dataStr = JSON.stringify(projects, null, 2);
      const blob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "projects.json";
      a.click();
      URL.revokeObjectURL(url);
    }
  
    function importProjects(event: Event) {
      const input = event.target as HTMLInputElement;
      const file = input.files?.[0];
      if (!file) return;
  
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedData = JSON.parse(e.target?.result as string);
          if (Array.isArray(importedData)) {
            projects = importedData;
            message = "✅ Projects imported successfully!";
          } else {
            message = "❌ Invalid file format.";
          }
        } catch (e) {
          message = "❌ Failed to parse JSON.";
        }
      };
      reader.readAsText(file);
    }
  </script>
  
  <style>
    .container {
      display: flex;
      flex-direction: column;
      gap: 2rem;
      padding: 2rem;
      color: #fff;
      background-color: #111827;
      min-height: 100vh;
    }
  
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: #304e70;
      padding: 2rem 2rem;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
  
    .header-bar h1 {
      font-size: 2rem;
      margin: 0;
    }
  
  
    .nav-buttons a {
      text-decoration: none;
    }
  
    .nav-buttons button {
      background-color: #00ffff;
      color: #000;
      padding: 0.6rem 1.2rem;
      border: none;
      border-radius: 1rem;
      font-size: 1rem;
      font-weight: 500;
      cursor: pointer;
    }
  
    .projects-section,
    .create-section,
    .export-section,
    .import-section {
      background-color: #1f2937;
      padding: 1.5rem;
      border-radius: 1rem;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
    }
  
    .form-container {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
  
    input[type="text"],
    input[type="number"] {
      padding: 0.5rem;
      border-radius: 0.5rem;
      border: none;
      background-color: #374151;
      color: white;
    }
  
    button {
      background-color: #00ffff;
      border: none;
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      border-radius: 1rem;
      cursor: pointer;
      color: #000;
    }
  
    .file-upload-container {
      position: relative;
      display: inline-block;
      margin-top: 1rem;
    }
  
    .file-upload-label {
      background-color: #00ffff;
      color: #000;
      padding: 0.75rem 1.5rem;
      border-radius: 1rem;
      cursor: pointer;
      display: inline-block;
    }
  
    input[type="file"] {
      display: none;
    }
  
    .message {
      margin-top: 1rem;
      font-weight: bold;
    }
  
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.6);
      display: flex;
      justify-content: center;
      align-items: center;
    }
  
    .modal-content {
      background-color: #1f2937;
      padding: 2rem;
      border-radius: 1rem;
      width: 90%;
      max-width: 400px;
    }
  </style>
  
  <div class="container">
    <!-- ✅ Top Header with Nav Buttons -->
    <div class="header-bar">
      <h1>TRACE System</h1>
      <div class="nav-buttons">
        <a href="/"><button>🏠 Home</button></a>
        <a href="/database"><button>📊 Db Enumerator</button></a>
        <a href="/settings"><button>⚙️ Settings</button></a>
      </div>
    </div>
  
    <!-- ✅ Project List Section -->
    <div class="projects-section">
      <h2>📁 Projects</h2>
      {#if projects.length === 0}
        <p>No projects yet.</p>
      {:else}
        <ul>
          {#each projects as project}
            <li>{project.name} (Owner ID: {project.owner_id})</li>
          {/each}
        </ul>
      {/if}
    </div>
  
    <!-- ✅ Create Project Section -->
    <div class="create-section">
      <h2>➕ Create New Project</h2>
      <button on:click={() => showDialog = true}>Create Project</button>
    </div>
  
    <!-- ✅ Export Section -->
    <div class="export-section">
      <h2>⬇️ Export Projects</h2>
      <button on:click={exportProjects}>Download JSON</button>
    </div>
  
    <!-- ✅ Import Section -->
    <div class="import-section">
      <h2>⬆️ Import Projects</h2>
      <div class="file-upload-container">
        <label class="file-upload-label">
          Choose JSON File
          <input type="file" accept="application/json" on:change={importProjects} />
        </label>
      </div>
    </div>
  
    <!-- ✅ Message -->
    {#if message}
      <div class="message">{message}</div>
    {/if}
  </div>
  
  <!-- ✅ Modal Dialog -->
  {#if showDialog}
    <div class="modal">
      <div class="modal-content">
        <h3>Create a New Project</h3>
        <div class="form-container">
          <label>
            Project Name:
            <input type="text" bind:value={name} placeholder="Enter project name" />
          </label>
          <label>
            Owner ID:
            <input type="number" bind:value={owner_id} placeholder="Enter owner ID" />
          </label>
          <button on:click={createProject}>Create</button>
          <button on:click={() => showDialog = false}>Cancel</button>
          {#if message}
            <div class="message">{message}</div>
          {/if}
        </div>
      </div>
    </div>
  {/if}
  
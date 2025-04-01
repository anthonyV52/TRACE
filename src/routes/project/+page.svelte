<script lang="ts">
  import { onMount } from "svelte";
  import "$lib/styles/trace.css";

  let name: string = "";
  let owner_id: string = "";
  let user_id: string = ""; // NEW: for identifying current user
  let message: string = "";

  interface Project {
    id: number;
    name: string;
    owner_id: number;
  }

  let projects: Project[] = [];
  let showDialog: boolean = false;

  function setUser() {
    if (!String(user_id).trim()) {
      message = "❌ Please enter a valid user ID.";
      return;
    }
    message = `✅ User ID set to ${user_id}`;
  }

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
        projects.push({ id: result.project_id, name, owner_id: parseInt(user_id) });
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

  async function openProject(project_id: number) {
    try {
      const response = await fetch(`http://localhost:8000/project/${project_id}?requester_id=${user_id}`);
      const result = await response.json();

      if (response.ok) {
        message = `✅ Opened project: ${result.project.name}`;
      } else {
        message = `❌ ${result.detail || 'Failed to open project'}`;
      }
    } catch (err) {
      message = `❌ Failed to connect to server.`;
    }
  }

  async function loadProjects() {
    try {
      const response = await fetch("http://localhost:8000/project");
      const result = await response.json();

      if (Array.isArray(result)) {
        projects = result;
      } else {
        console.log("Backend returned:", result);
      }
    } catch (err) {
      console.error("Error fetching projects:", err);
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

  onMount(() => {
    loadProjects();
  });
</script>


!-- Add login section above header -->
<div class="container">
  <div class="user-section">
    <label>
      Enter User ID:
      <input type="number" bind:value={user_id} placeholder="Your ID (e.g. 1)" />
    </label>
    <button on:click={setUser}>Set User</button>
    {#if user_id}
      <p>👤 Current User ID: <strong>{user_id}</strong></p>
    {/if}
  </div>

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
          <li>
            {project.name} (Owner ID: {project.owner_id})
            <button on:click={() => openProject(project.id)}>Open</button>
          </li>
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
        <button on:click={createProject}>Create</button>
        <button on:click={() => showDialog = false}>Cancel</button>
        {#if message}
          <div class="message">{message}</div>
        {/if}
      </div>
    </div>
  </div>
{/if}

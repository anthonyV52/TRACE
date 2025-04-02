<script lang="ts">
  import { onMount } from "svelte";
  import "$lib/styles/trace.css";
  import { goto } from "$app/navigation";

  let name: string = "";
  let user_id: string = "";
  let message: string = "";
  let projects: { id: string; name: string; owner: string; isLocked: boolean; files: string[] }[] = [];
  let showDialog = false;

  let newProjectId = "";
  let newOwnerInitials = "";

  function setUser() {
    const parsedId = parseInt(user_id);
    const trimmedName = name.trim();

    if (!trimmedName || isNaN(parsedId)) {
      message = "❌ Please enter both a valid User ID and Name.";
      return;
    }

    message = `✅ Logged in as ${name} (ID: ${user_id})`;
  }

  async function createProject() {
    const parsedId = parseInt(user_id);
    if (!newProjectId.trim() || !name.trim() || !newOwnerInitials.trim()) {
      message = "❌ Please enter all project details.";
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/project/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: newProjectId.trim(),
          name: name.trim(),
          owner: newOwnerInitials.trim(),
          isLocked: false,
          files: [],
          IPList: []
        })
      });

      const result = await response.json();

      if (response.ok) {
        message = `✅ ${result.message}`;
        projects.push({ id: newProjectId, name, owner: newOwnerInitials, isLocked: false, files: [] });
        showDialog = false;
        name = "";
        newProjectId = "";
        newOwnerInitials = "";
      } else {
        message = `❌ ${result.detail || 'Error creating project'}`;
      }
    } catch {
      message = `❌ Failed to connect to server.`;
    }
  }

  async function openProject(project_id: string) {
    const parsedId = parseInt(user_id);
    if (!parsedId || isNaN(parsedId)) {
      message = "❌ Please set a valid User ID before opening a project.";
      return;
    }

    goto(`/project/${project_id}?requester_id=${parsedId}`);
  }

  async function loadProjects() {
    try {
      const response = await fetch("http://localhost:8000/project");
      const result = await response.json();
      if (Array.isArray(result)) {
        projects = result;
      }
    } catch (err) {
      console.error("Error fetching projects:", err);
    }
  }

  onMount(() => {
    loadProjects();
  });
</script>

<div class="container">
  <div class="user-section">
    <label>User ID:<input type="number" bind:value={user_id} /></label>
    <label>Name:<input type="text" bind:value={name} /></label>
    <button on:click={setUser}>Set User</button>
    {#if user_id && name}<p>👤 Current User: <strong>{name} (ID: {user_id})</strong></p>{/if}
  </div>

  <div class="header-bar">
    <h1>TRACE System</h1>
    <div class="nav-buttons">
      <a href="/database"><button>📊 Db Enumerator</button></a>
      <a href="/settings"><button>⚙️ Settings</button></a>
    </div>
  </div>

  {#if message}<div class="message">{message}</div>{/if}

  <div class="projects-section">
    <h2>📁 Projects</h2>
    {#if projects.length === 0}
      <p>No projects yet.</p>
    {:else}
      <ul>
        {#each projects as project}
          <li>
            <strong>{project.name}</strong> — ID: {project.id}, Owner: {project.owner}, Locked: {project.isLocked ? "🔒" : "🔓"}
            <button on:click={() => openProject(project.id)}>Open</button>
          </li>
        {/each}
      </ul>
    {/if}
  </div>

  <div class="create-section">
    <h2>➕ Create New Project</h2>
    <button on:click={() => showDialog = true}>Create Project</button>
  </div>

  <div class="export-section">
    <h2>⬇️ Export Projects</h2>
    <button on:click={() => {
      const dataStr = JSON.stringify(projects, null, 2);
      const blob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "projects.json";
      a.click();
      URL.revokeObjectURL(url);
    }}>Download JSON</button>
  </div>

  <div class="import-section">
    <h2>⬆️ Import Projects</h2>
    <label class="file-upload-label">
      Choose JSON File
      <input type="file" accept="application/json" on:change={(e) => {
        const input = e.target as HTMLInputElement;
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
          } catch {
            message = "❌ Failed to parse JSON.";
          }
        };
        reader.readAsText(file);
      }} />
    </label>
  </div>

  {#if showDialog}
    <div class="modal">
      <div class="modal-content">
        <h3>Create a New Project</h3>
        <div class="form-container">
          <label>Project ID:<input type="text" bind:value={newProjectId} /></label>
          <label>Project Name:<input type="text" bind:value={name} /></label>
          <label>Owner Initials:<input type="text" bind:value={newOwnerInitials} /></label>
          <button on:click={createProject}>✅ Create</button>
          <button on:click={() => showDialog = false}>❌ Cancel</button>
          {#if message}<div class="message">{message}</div>{/if}
        </div>
      </div>
    </div>
  {/if}
</div>
<script lang="ts">
  import { onMount } from "svelte";
  import "$lib/styles/trace.css";
  import { goto } from "$app/navigation";

  let name: string = "";
  let user_id: string = "";
  let message: string = "";
  let projects: { id: number; name: string; owner_id: number }[] = [];
  let showDialog = false;
  let adminMode = false;
  let allowedUsers: { id: number; name: string }[] = [];

  // Admin-only new user fields
  let newUserId = "";
  let newUserName = "";

  function setUser() {
    const parsedId = parseInt(user_id);
    const trimmedName = name.trim();

    if (!trimmedName || isNaN(parsedId)) {
      message = "❌ Please enter both a valid User ID and Name.";
      return;
    }

    const found = allowedUsers.find(
      (u) => u.id === parsedId && u.name.toLowerCase() === trimmedName.toLowerCase()
    );

    if (!found) {
      message = "❌ User not recognized. Please contact an admin.";
      return;
    }

    if (parsedId === 1 && !adminMode) {
      const token = prompt("Enter admin token:");
      if (token === "supersecret") {
        adminMode = true;
        message = `✅ Logged in as ${name} (Admin ID: ${user_id})`;
      } else {
        message = "❌ Invalid admin token.";
        return;
      }
    } else {
      message = `✅ Logged in as ${name} (ID: ${user_id})`;
    }
  }

  function addUser() {
    const id = parseInt(newUserId);
    const trimmedName = newUserName.trim();

    if (!trimmedName || isNaN(id)) {
      message = "❌ Please enter a valid new user ID and name.";
      return;
    }

    if (allowedUsers.some((u) => u.id === id)) {
      message = "❌ That User ID is already taken.";
      return;
    }

    allowedUsers.push({ id, name: trimmedName });
    message = `✅ Added user "${trimmedName}" with ID ${id}`;
    newUserId = "";
    newUserName = "";
  }

  async function createProject() {
    const parsedId = parseInt(user_id);
    if (!name.trim() || isNaN(parsedId)) {
      message = "❌ Please enter a valid project name and user ID.";
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/project/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.trim(),
          owner_id: parsedId
        })
      });

      const result = await response.json();

      if (response.ok) {
        message = `✅ ${result.message} (ID: ${result.project_id})`;
        projects.push({ id: result.project_id, name, owner_id: parsedId });
        showDialog = false;
        name = "";
      } else {
        message = `❌ ${result.detail || 'Error creating project'}`;
      }
    } catch {
      message = `❌ Failed to connect to server.`;
    }
  }

  async function openProject(project_id: number) {
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
    } catch {
      message = "❌ Failed to parse JSON.";
    }
  };
  reader.readAsText(file);
}

  onMount(() => {
    loadProjects();

    // Preload a few allowed users (admin + test users)
    allowedUsers = [
      { id: 1, name: "Admin" },
      { id: 2, name: "Alice" },
      { id: 3, name: "Bob" }
    ];
  });
</script>

<div class="container">
  <div class="user-section">
    <label>
      User ID:
      <input type="number" bind:value={user_id} placeholder="Enter User ID" />
    </label>
    <label>
      Name:
      <input type="text" bind:value={name} placeholder="Enter Name" />
    </label>
    <button on:click={setUser}>Set User</button>
    {#if user_id && name}
      <p>👤 Current User: <strong>{name} (ID: {user_id})</strong></p>
    {/if}
  </div>

  {#if adminMode}
    <div class="admin-section">
      <h3>🔐 Admin Panel — Create New User</h3>
      <label>
        New User ID:
        <input type="number" bind:value={newUserId} placeholder="ID" />
      </label>
      <label>
        New User Name:
        <input type="text" bind:value={newUserName} placeholder="Name" />
      </label>
      <button on:click={addUser}>➕ Add User</button>
    </div>
  {/if}

  <div class="header-bar">
    <h1>TRACE System</h1>
    <div class="nav-buttons">
      <a href="/"><button>🏠 Home</button></a>
      <a href="/database"><button>📊 Db Enumerator</button></a>
      <a href="/settings"><button>⚙️ Settings</button></a>
    </div>
  </div>

  {#if message}
  <div class="message">{message}</div>
  {/if}

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

  <div class="create-section">
    <h2>➕ Create New Project</h2>
    <button on:click={() => showDialog = true}>Create Project</button>
  </div>

  <div class="export-section">
    <h2>⬇️ Export Projects</h2>
    <button on:click={exportProjects}>Download JSON</button>
  </div>
  
  <div class="import-section">
    <h2>⬆️ Import Projects</h2>
    <div class="file-upload-container">
      <label class="file-upload-label">
        Choose JSON File
        <input type="file" accept="application/json" on:change={importProjects} />
      </label>
    </div>
  </div>
  

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
</div>

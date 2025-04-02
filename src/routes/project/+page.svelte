<script lang="ts">
  import { onMount } from "svelte";
  import "$lib/styles/trace.css";
  import { goto } from "$app/navigation";

  let name: string = "";
  let user_id: string = "";
  let message: string = "";
  let projects: { id: string; name: string; owner: string; isLocked: boolean; files: string[] }[] = [];
  let showDialog = false;
  let adminMode = false;
  let allowedUsers: { id: number; name: string }[] = [];

  let newUserId = "";
  let newUserName = "";

  // Project Manager fields
  let newProjectId = "";
  let newProjectName = "";
  let startDate = "";
  let startTime = "";
  let leadAnalyst = "";
  let projectDescription = "";
  let uploadedFiles: File[] = [];

  function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      uploadedFiles = Array.from(input.files);
    }
  }

  function removeFile(index: number) {
    uploadedFiles.splice(index, 1);
  }

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

  async function createProject() {
    if (!newProjectName || !startDate || !startTime || !leadAnalyst) {
      message = "❌ Please fill all required fields.";
      return;
    }

    try {
      const projectPayload = {
        name: newProjectName,
        owner: leadAnalyst,
        dateRange: [startDate, startDate],
        files: uploadedFiles.map((file) => file.name),
        description: projectDescription,
        IPList: [],
        isLocked: false,
        id: newProjectId || Math.random().toString(36).substring(2, 8)
      };

      const res = await fetch("http://localhost:8000/project/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(projectPayload)
      });

      const data = await res.json();
      if (res.ok) {
        message = `✅ ${data.message}`;
        showDialog = false;
        projects.push(projectPayload);
        // Reset fields
        newProjectId = "";
        newProjectName = "";
        leadAnalyst = "";
        projectDescription = "";
        startDate = "";
        startTime = "";
        uploadedFiles = [];
      } else {
        message = `❌ ${data.detail || "Could not create project"}`;
      }
    } catch (err) {
      message = "❌ Failed to connect to server.";
    }
  }

  async function loadProjects() {
    try {
      const response = await fetch("http://localhost:8000/project");
      const data = await response.json();
      if (Array.isArray(data)) {
        projects = data;
      }
    } catch (err) {
      console.error("Error loading projects:", err);
    }
  }

  async function openProject(projectId: string) {
    if (!user_id) {
      message = "❌ Please log in first.";
      return;
    }
    goto(`/project/${projectId}?requester_id=${user_id}`);
  }

  async function loadUsers() {
    try {
      const res = await fetch("http://localhost:8000/users");
      const data = await res.json();
      if (Array.isArray(data)) {
        allowedUsers = data;
      } else {
        console.warn("Unexpected user data", data);
      }
    } catch (err) {
      console.error("Failed to fetch users:", err);
    }
  }

  onMount(() => {
    loadUsers();
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
      <a href="/sql-injection"><button>🧪 SQL Injection</button></a>
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

            const isValid = (typeof importedData.name === "string" &&
                             typeof importedData.id === "string" &&
                             typeof importedData.owner === "string" &&
                             typeof importedData.isLocked === "boolean" &&
                             Array.isArray(importedData.files) &&
                             importedData.IPList.every(ip => Array.isArray(ip) && ip.length === 2 && 
                             typeof ip[0] === "string" && typeof ip[1] === "number")
            )

            if (isValid) {
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

  <!-- Modal UI -->
{#if showDialog}
<div class="modal">
  <div class="modal-content">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h3>Create Project</h3>
      <button on:click={() => showDialog = false} style="font-size: 1.2rem;">✖</button>
    </div>

    <div class="form-container">
      <label>
        Project Name (required):
        <input type="text" bind:value={newProjectName} placeholder="Project Name" required />
      </label>

      <label>
        Start Date (required):
        <input type="date" bind:value={startDate} required />
      </label>

      <label>
        Start Time (required):
        <input type="time" bind:value={startTime} required />
      </label>

      <label>
        Lead Analyst Initials (required):
        <input type="text" bind:value={leadAnalyst} placeholder="e.g. JD" required />
      </label>

      <label>
        Project Description (optional):
        <textarea bind:value={projectDescription} placeholder="Enter description..."></textarea>
      </label>

      <label>
        File Upload (optional):
        <input type="file" multiple on:change={handleFileUpload} />
      </label>

      {#if uploadedFiles.length > 0}
        <ul>
          {#each uploadedFiles as file, index}
            <li>{file.name} <button on:click={() => removeFile(index)}>🗑️</button></li>
          {/each}
        </ul>
      {/if}

      <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
        <button on:click={() => showDialog = false}>Cancel</button>
        <button on:click={createProject}>Create</button>
      </div>
    </div>
  </div>
</div>
{/if}

</div>
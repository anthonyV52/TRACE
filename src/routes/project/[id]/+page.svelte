<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { currentUser } from "$lib/stores/user";
  import { get } from "svelte/store";
  import { goto } from "$app/navigation";
  

  let projectId: string = "";
  let requesterId = get(currentUser)?.id || "";

  let project: any = null;
  let message: string = "";
  let loading = true;

  $: projectId = $page.params.id;

  async function loadProject() {
    try {
      const res = await fetch(`http://localhost:8000/project/${projectId}?requester_id=${requesterId}`);
      const data = await res.json();
      if (res.ok) {
        let rawList = data.project.IPList;
        try {
          if (typeof rawList === "string") {
            rawList = JSON.parse(rawList);
          }
        } catch (e) {
          console.warn("Could not parse IPList:", rawList);
        }
        data.project.IPList = Array.isArray(rawList) ? rawList : [];
        project = data.project;
      } else {
        message = data.detail || "Project not found.";
      }
    } catch (err) {
      message = "❌ Failed to load project.";
    } finally {
      loading = false;
    }
  }

  async function toggleProjectLock() {
  const user = get(currentUser);
  if (!user) {
    message = "❌ You must be logged in.";
    return;
  }

  try {
    const res = await fetch(`http://localhost:8000/project/${projectId}/lock?requester_id=${user.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ lock: !project.isLocked })  // ✅ send JSON body
    });

    const result = await res.json();

    if (res.ok) {
      project.isLocked = !project.isLocked;
      message = `✅ ${result.message}`;
    } else {
      message = `❌ ${result.detail || "Failed to toggle lock."}`;
    }
  } catch (err) {
    message = "❌ Network error.";
  }
}


  function goBack() {
    goto("/");
  }

  onMount(loadProject);
</script>

<style>
  .project-container {
    padding: 2rem;
  }

  .project-info {
    background: #f5f5f5;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
  }

  .back-button {
    margin-bottom: 1rem;
  }

  .toggle-button {
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 0.3rem;
    cursor: pointer;
  }

  .toggle-button:hover {
    background-color: #1d4ed8;
  }
</style>

<div class="project-container">
  <button on:click={goBack} class="back-button">⬅️ Back to Projects</button>
  <h1>📊 Project Dashboard</h1>

  {#if $currentUser}
    <p>Welcome back, {$currentUser.name}!</p>
  {/if}

  {#if loading}
    <p>Loading project data...</p>
  {:else if message}
    <p class="error">{message}</p>
  {:else if project}
    <div class="project-info">
      <h2>{project.name}</h2>
      <p><strong>Project ID:</strong> {project.id}</p>
      <p><strong>Owner:</strong> {project.owner}</p>
      <p><strong>Locked:</strong> {project.isLocked ? "🔒 Locked" : "🔓 Unlocked"}</p>
      <p><strong>Files:</strong> {project.files.length > 0 ? project.files.join(", ") : "No files"}</p>
      <p><strong>IP List:</strong></p>
      <ul>
        {#each project.IPList as [ip, port]}
          <li>{ip}:{port}</li>
        {/each}
      </ul>
    </div>

    <!-- ✅ Lock/Unlock Button (Admin + Owner Only) -->
    {#if $currentUser && $currentUser.id === 1}
      <button on:click={toggleProjectLock} class="toggle-button">
        {project.isLocked ? "🔓 Unlock Project" : "🔒 Lock Project"}
      </button>
    {/if}
  {/if}
</div>

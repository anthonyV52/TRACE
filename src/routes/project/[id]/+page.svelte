<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
  
    let projectId: string = "";
    let requesterId: string = "";
    let project: any = null;
    let message: string = "";
    let loading = true;
  
    $: projectId = $page.params.id;
    $: requesterId = $page.url.searchParams.get("requester_id") || "";
  
    onMount(async () => {
  try {
    const res = await fetch(`http://localhost:8000/project/${projectId}?requester_id=${requesterId}`);
    const data = await res.json();
    if (res.ok) {
      // Parse IPList from string to array of tuples if needed
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
});

  </script>
  
  <style>
    .project-container {
      padding: 2rem;
    }
    .project-info {
      background: #f5f5f5;
      padding: 1rem;
      border-radius: 0.5rem;
    }
  </style>
  
  <div class="project-container">
    <h1>📊 Project Dashboard</h1>
  
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
    {/if}
  </div>
  
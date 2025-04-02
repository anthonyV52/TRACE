<script lang="ts">
    import { onMount } from "svelte";
    import { currentUser } from "$lib/stores/user";
    import { get } from "svelte/store";
    import { goto } from "$app/navigation";
  
    let projects: any[] = [];
    let message: string = "";
  
    async function loadProjects() {
      try {
        const res = await fetch("http://localhost:8000/project");
        const data = await res.json();
        if (Array.isArray(data)) {
          projects = data;
        }
      } catch (err) {
        message = "❌ Failed to fetch projects.";
        console.error(err);
      }
    }
  
    async function deleteProject(id: string) {
      const user = get(currentUser);
      if (!user) {
        message = "❌ You must be logged in to delete a project.";
        return;
      }
  
      const confirmDelete = confirm(`Are you sure you want to delete project "${id}"?`);
      if (!confirmDelete) return;
  
      try {
        const res = await fetch(`http://localhost:8000/project-manager/${id}/delete?requester_id=${user.id}`, {
          method: "DELETE"
        });
  
        const data = await res.json();
  
        if (res.ok) {
          message = `✅ ${data.message}`;
          projects = projects.filter(p => p.id !== id);
        } else {
          message = `❌ ${data.detail || 'Failed to delete project.'}`;
        }
      } catch (err) {
        message = "❌ Error deleting project.";
        console.error(err);
      }
    }
    function goBack() {
    goto("/project");
    }
  
    onMount(() => {
      loadProjects();
    });
  </script>
  
  <style>
    .project-list {
      padding: 2rem;
    }
  
    .project-card {
      padding: 1rem;
      background: #f5f5f5;
      border-radius: 0.5rem;
      margin-bottom: 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    button {
      background-color: #dc2626;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.3rem;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #b91c1c;
    }
  
    .message {
      margin: 1rem 2rem;
      font-weight: bold;
    }
  </style>
  
  <div class="project-list">
    <h1>🗑️ Project Deletion</h1>
    <button on:click={goBack} style="margin-bottom: 1rem;">⬅️ Back to Projects</button>
  
    {#if message}
      <div class="message">{message}</div>
    {/if}
  
    {#each projects as project}
      <div class="project-card">
        <div>
          <strong>{project.name}</strong><br />
          ID: {project.id} — Owner: {project.owner}
        </div>
        <button on:click={() => deleteProject(project.id)}>Delete</button>
      </div>
    {/each}
  </div>
  
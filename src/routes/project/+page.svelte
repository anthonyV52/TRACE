<script lang="ts">
    import { onMount } from 'svelte';
  
    let name: string = "";
    let owner_id: string = "";
    let message: string = "";
  
    interface Project {
      id: number;
      name: string;
      owner_id: number;
    }
  
    let projects: Project[] = []; // ✅ Typed list of projects
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
          showDialog = false; // Close dialog on success
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
  
    .projects-section, .create-section {
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
  
    input {
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
  
    .message {
      margin-top: 1rem;
      font-weight: bold;
    }
  
    .modal {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
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
  
    <!-- ✅ Create Project Button -->
    <div class="create-section">
      <button on:click={() => showDialog = true}>➕ Create New Project</button>
    </div>
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
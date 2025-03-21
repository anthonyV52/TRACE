<script>
    import { onMount } from 'svelte';
  
    let name = "";
    let owner_id = "";
    let message = "";
  
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
    .form-container {
      max-width: 400px;
      margin: 5rem auto;
      padding: 2rem;
      background-color: #1f2937;
      color: #fff;
      border-radius: 1rem;
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
  
    label, input {
      display: block;
      width: 100%;
      margin-bottom: 1rem;
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
      margin-top: 1rem;
    }
  
    .message {
      margin-top: 1rem;
      font-weight: bold;
    }
  </style>
  
  <div class="form-container">
    <h2>Create a New Project</h2>
    <label>
      Project Name:
      <input type="text" bind:value={name} placeholder="Enter project name" />
    </label>
    <label>
      Owner ID:
      <input type="number" bind:value={owner_id} placeholder="Enter owner ID" />
    </label>
    <button on:click={createProject}>Create Project</button>
  
    {#if message}
      <div class="message">{message}</div>
    {/if}
  </div>
  
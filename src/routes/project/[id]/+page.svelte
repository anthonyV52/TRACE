<script lang="ts">
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
  
    let project: any = null;
    let message: string = "";
    let loading = true;
  
    $: projectId = $page.params.id;
    $: requesterId = $page.url.searchParams.get("requester_id");
  
    onMount(async () => {
      try {
        const res = await fetch(`http://localhost:8000/project/${projectId}?requester_id=${requesterId}`);
        const data = await res.json();
        if (res.ok) {
          project = data.project;
        } else {
          message = data.detail || "Project not found.";
        }
      } catch (err) {
        message = "Failed to load project.";
      } finally {
        loading = false;
      }
    });
  </script>
  
  {#if loading}
    <p>Loading project...</p>
  {:else if message}
    <p class="text-red-500">{message}</p>
  {:else}
    <div class="p-6 rounded shadow bg-white max-w-xl mx-auto mt-8 space-y-4">
      <h1 class="text-2xl font-bold text-blue-600">{project.name}</h1>
      <p><strong>Project ID:</strong> {project.id}</p>
      <p><strong>Owner ID:</strong> {project.owner_id}</p>
      <p><strong>Locked:</strong> {project.locked ? 'Yes' : 'No'}</p>
      <button on:click={() => goto('/')} class="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
        ← Back to Projects
      </button>
    </div>
  {/if}
  
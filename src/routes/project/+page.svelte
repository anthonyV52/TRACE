<script lang="ts">
    import { onMount } from "svelte";

    let name = "";
    let owner = "";
    let format = "csv";
    let filename = "";
    
    // Explicitly define project type
    let projects: { name: string; owner: string; archived: boolean }[] = [];

    async function createProject() {
        await fetch("http://localhost:8000/create_project", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, owner })
        });
        alert("Project created!");
        loadProjects();
    }

    async function deleteProject(projectName: string) {
        await fetch("http://localhost:8000/delete_project", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: projectName, owner })
        });
        alert("Project deleted!");
        loadProjects();
    }

    async function importProject() {
        await fetch("http://localhost:8000/import_project", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ filename, owner })
        });
        alert("Project imported!");
        loadProjects();
    }

    async function exportProject(projectName: string) {
        let res = await fetch("http://localhost:8000/export_project", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: projectName, format, owner })
        });
        let data = await res.json();
        alert(`Exported file: ${data.exported_file}`);
    }

    async function archiveProject(projectName: string) {
        await fetch("http://localhost:8000/archive_project", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: projectName, owner })
        });
        alert("Project archived!");
        loadProjects();
    }

    async function loadProjects() {
        let res = await fetch(`http://localhost:8000/display_projects/${owner}`);
        let data = await res.json();
        projects = data.projects || [];
    }

    onMount(() => {
        loadProjects();
    });
</script>

<h1>Project Manager</h1>

<h2>Create a Project</h2>
<input type="text" bind:value={name} placeholder="Project Name" />
<input type="text" bind:value={owner} placeholder="Owner Name" />
<button on:click={createProject}>Create</button>

<h2>Import a Project</h2>
<input type="text" bind:value={filename} placeholder="File Name (.csv or .xml)" />
<button on:click={importProject}>Import</button>

<h2>Your Projects</h2>
<button on:click={loadProjects}>Refresh Projects</button>
<ul>
    {#each projects as project}
        <li>
            {project.name} {project.archived ? "(Archived)" : ""}
            <button on:click={() => deleteProject(project.name)}>Delete</button>
            <button on:click={() => exportProject(project.name)}>Export</button>
            <button on:click={() => archiveProject(project.name)}>Archive</button>
        </li>
    {/each}
</ul>

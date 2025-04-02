<script lang="ts">
  import { goto } from '$app/navigation';

  let formData = {
    url: '',
    port: '',
    username: '',
    password: '',
    enumLevel: '',
    timeout: '',
    additional: '',
    enumeration: true
  };

  function handleSubmit() {
    goto('/sql-injection/running');
  }
</script>

  <!-- Main Content -->
  <div class="sql">
    <!-- Header -->
    <header class="header">
      <h1>SQL Injection</h1>
    </header>

  <div class="space-y-5 max-w-lg">
    <label class="flex items-center gap-2">
      <input
        type="checkbox"
        bind:checked={formData.enumeration}
        class="w-5 h-5 accent-blue-600"
      />
      <span class="text-md">Database Enumeration</span>
    </label>

    <div>
    <label for="url" class="block text-sm font-medium mb-1">Target URL *</label>
    <input
        id="url"
        type="text"
        bind:value={formData.url}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder="https://example.com"
    />
    </div>


    <div>
      <label class="block text-sm font-medium mb-1">Port</label>
      <input
        id="port"
        type="text"
        bind:value={formData.port}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder=""
      />
    </div>

    <div>
      <label class="block text-sm font-medium mb-1">Database Username</label>
      <input
        id= "username"
        type="text"
        bind:value={formData.username}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder="username"
      />
    </div>

    <div>
      <label class="block text-sm font-medium mb-1">Database Password</label>
      <input
        id = "password"
        type="password"
        bind:value={formData.password}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder="password"
      />
    </div>

    <div>
      <label class="block text-sm font-medium mb-1">Enumeration Level</label>
      <input
        id="enumlevel"
        type="text"
        bind:value={formData.enumLevel}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder=""
      />
    </div>

    <div>
      <label class="block text-sm font-medium mb-1">Time Out</label>
      <input
        id="timeout"
        type="text"
        bind:value={formData.timeout}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder=""
      />
    </div>

    <div>
      <label class="block text-sm font-medium mb-1">Additional Parameters (if applicable)</label>
      <input
        id="additional"
        type="text"
        bind:value={formData.additional}
        class="w-full p-2 border border-gray-300 rounded"
        placeholder="NULL"
      />
    </div>
  </div>

  <button
    on:click={handleSubmit}
    class="mt-6 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
  >
    Start
  </button>
</div>

<style>
  input:focus {
    margin: 2rem auto;
    outline: none;
    border-color: #fff;
    box-shadow: 0 0 0 1px #fff;
    background-color: #fff;
    font-family: Arial, sans-serif;
    color: #333;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }    

</style>

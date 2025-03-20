<script>
    let password = "";
    let username = "";
    /**
	 * @type {null}
	 */
    let passwordStrength = null;
    /**
	 * @type {null}
	 */
    let usernameStrength = null;
    let message = "";
  
    const apiUrl = "http://127.0.0.1:8000";
  
    async function storePassword() {
      const res = await fetch(`${apiUrl}/store-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: password }),
      });
      const data = await res.json();
      message = data.message || data.detail;
    }
  
    async function storeUsername() {
      const res = await fetch(`${apiUrl}/store-username`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: username }),
      });
      const data = await res.json();
      message = data.message || data.detail;
    }
  
    async function checkPasswordStrength() {
      const res = await fetch(`${apiUrl}/password-strength`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: password }),
      });
      const data = await res.json();
      passwordStrength = data.strength || "Error";
    }
  
    async function checkUsernameStrength() {
      const res = await fetch(`${apiUrl}/username-strength`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: username }),
      });
      const data = await res.json();
      usernameStrength = data.strength || "Error";
    }
  </script>
  
  <main>
    <h1>FastAPI + Svelte</h1>
  
    <div>
      <h2>Password</h2>
      <input type="password" bind:value={password} placeholder="Enter password" />
      <button on:click={storePassword}>Store Password</button>
      <button on:click={checkPasswordStrength}>Check Strength</button>
      {#if passwordStrength !== null}
        <p>Password Strength: {passwordStrength}/5</p>
      {/if}
    </div>
  
    <div>
      <h2>Username</h2>
      <input type="text" bind:value={username} placeholder="Enter username" />
      <button on:click={storeUsername}>Store Username</button>
      <button on:click={checkUsernameStrength}>Check Strength</button>
      {#if usernameStrength !== null}
        <p>Username Strength: {usernameStrength}/5</p>
      {/if}
    </div>
  
    {#if message}
      <p>{message}</p>
    {/if}
  </main>
  
  <style>
    main {
      font-family: Arial, sans-serif;
      max-width: 400px;
      margin: auto;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
      box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    input {
      display: block;
      width: 100%;
      padding: 8px;
      margin: 5px 0;
    }
    button {
      margin: 5px;
      padding: 8px 12px;
      cursor: pointer;
    }
  </style>
  
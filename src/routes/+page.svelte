<script>
    let password = "";
    let username = "";
    let passwordStrength = null;
    let usernameStrength = null;
    let message = "";

    // ✅ Updated API base URL to correctly point to `/credentials`
    const apiUrl = "http://127.0.0.1:8000/credentials";

    // ✅ Store Password API call
    async function storePassword() {
        try {
            const res = await fetch(`${apiUrl}/store-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ value: password })
            });

            const data = await res.json();
            console.log("Store Password Response:", data);

            if (res.ok) {
                message = data.message || "Password stored successfully.";
            } else {
                message = data.detail || "Error storing password.";
            }
        } catch (error) {
            console.error("Fetch error:", error);
            message = "Failed to connect to server.";
        }
    }

    // ✅ Store Username API call
    async function storeUsername() {
        try {
            const res = await fetch(`${apiUrl}/store-username`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ value: username })
            });

            const data = await res.json();
            console.log("Store Username Response:", data);

            if (res.ok) {
                message = data.message || "Username stored successfully.";
            } else {
                message = data.detail || "Error storing username.";
            }
        } catch (error) {
            console.error("Fetch error:", error);
            message = "Failed to connect to server.";
        }
    }

    // ✅ Check Password Strength API call
    async function checkPasswordStrength() {
        try {
            const res = await fetch(`${apiUrl}/password-strength`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ value: password })
            });

            const data = await res.json();
            console.log("Password Strength Response:", data);

            if (res.ok) {
                passwordStrength = data.strength ?? "Unknown";
            } else {
                passwordStrength = "Error";
                message = data.detail || "Error checking password strength.";
            }
        } catch (error) {
            console.error("Fetch error:", error);
            passwordStrength = "Error";
            message = "Failed to connect to server.";
        }
    }

    // ✅ Check Username Strength API call
    async function checkUsernameStrength() {
        try {
            const res = await fetch(`${apiUrl}/username-strength`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ value: username })
            });

            const data = await res.json();
            console.log("Username Strength Response:", data);

            if (res.ok) {
                usernameStrength = data.strength ?? "Unknown";
            } else {
                usernameStrength = "Error";
                message = data.detail || "Error checking username strength.";
            }
        } catch (error) {
            console.error("Fetch error:", error);
            usernameStrength = "Error";
            message = "Failed to connect to server.";
        }
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

<div>
    <a href="/project">Visit Project Page</a>
    <a href="/database">Visit Db_enumerator Page</a>
</div>

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

<script>
    let message = "Loading...";

    async function fetchData() {
        try {
            const res = await fetch("http://localhost:8000/api/data", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
                mode: "cors"
            });

            if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);

            const data = await res.json();
            message = data.message;
        } catch (error) {
            message = "Error fetching data!";
            console.error("Fetch error:", error);
        }
    }

    fetchData();
</script>

<h1>{message}</h1>

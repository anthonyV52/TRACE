<script>
  let projectDetails = "This is the trace subsystem 3 portion of the porject and a simple launch page";
  function goToNextPage() {
    window.location.href = "/project"; // Replace with your actual route
  }
</script>
<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #fff;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .details {
    text-align: center;
    max-width: 600px;
    font-size: 1.25rem;
    padding: 2rem;
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 1rem;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
  }

  .start-button {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    background-color: #00ffff;
    color: #000;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.2rem;
    border-radius: 2rem;
    cursor: pointer;
    box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    transition: all 0.3s ease;
  }

  .start-button:hover {
    background-color: #00cccc;
    box-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff;
  }
</style>

<div class="details">
  <h1>Elevate your security strategy with TRACE</h1>
  <p>{projectDetails}</p>
</div>

<button class="start-button" on:click={goToNextPage}>Start</button>

import { writable } from "svelte/store";

export const currentUser = writable<{ id: number; name: string } | null>(null);

// Load from localStorage if it exists
if (typeof localStorage !== "undefined") {
  const stored = localStorage.getItem("currentUser");
  if (stored) {
    try {
      currentUser.set(JSON.parse(stored));
    } catch (err) {
      console.warn("Invalid user in localStorage");
    }
  }

  // Keep it synced
  currentUser.subscribe((value) => {
    if (value) {
      localStorage.setItem("currentUser", JSON.stringify(value));
    } else {
      localStorage.removeItem("currentUser");
    }
  });
}

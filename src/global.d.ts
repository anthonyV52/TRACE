/// <reference types="svelte" />
// src/global.d.ts
declare namespace svelteHTML {
    interface HTMLAttributes<T> {
      'on:clickoutside'?: () => void; // example
    }
  }
  
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    // Force everything into a single JS bundle — no code-splitting
    rollupOptions: {
      output: {
        // Disable dynamic imports / chunk splitting
        manualChunks: undefined,
        inlineDynamicImports: true,
      },
    },
  },
});

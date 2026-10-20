// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://automatingcats.net',

  output: "static",

  markdown: {
    syntaxHighlight: "shiki",

    shikiConfig: {
      theme: "github-dark",
      wrap: false,
    },
  },
});

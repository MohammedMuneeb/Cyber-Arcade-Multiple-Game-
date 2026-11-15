const fs = require('fs');
const path = require('path');

const distDir = path.resolve(__dirname, '../arcade-mobile/dist');
const htmlFile = path.join(distDir, 'index.html');
const assetsDir = path.join(distDir, 'assets');

const files = fs.readdirSync(assetsDir);
const cssFileName = files.find(f => f.endsWith('.css'));

// Grab ALL JS files (in case Vite still splits)
const jsFileNames = files.filter(f => f.endsWith('.js')).sort((a, b) => {
  // Put index-*.js last so it can reference the others
  if (a.startsWith('index-')) return 1;
  if (b.startsWith('index-')) return -1;
  return 0;
});

let html = fs.readFileSync(htmlFile, 'utf8');
const css = fs.readFileSync(path.join(assetsDir, cssFileName), 'utf8');

// Combine all JS into one block
let allJs = jsFileNames.map(fn => {
  return fs.readFileSync(path.join(assetsDir, fn), 'utf8');
}).join('\n;\n');

// In WebView inline script (non-module), import.meta is invalid syntax and throws a fatal parse error.
// Replace Vite's import.meta.resolve/import.meta.url with window.location fallback:
allJs = allJs.replace(/import\.meta\.resolve\?new URL\(import\.meta\.resolve\(e\)\):new URL\(e,import\.meta\.url\)/g, 'new URL(e, window.location.href)');
allJs = allJs.replace(/import\.meta\.url/g, 'window.location.href');

// Replace CSS link with inline <style>
html = html.replace(/<link rel="stylesheet"[^>]+>/, `<style>\n${css}\n</style>`);

// Replace the module script tag with a regular inline script containing ALL JS
html = html.replace(/<script type="module"[^>]+><\/script>/, `<script>\n${allJs.replace(/<\/script>/gi, '<\\/script>')}\n</script>`);

// Remove Google Fonts links (offline mode — fonts won't load in WebView anyway)
html = html.replace(/<link rel="preconnect"[^>]*>/g, '');
html = html.replace(/<link\s+href="https:\/\/fonts\.googleapis\.com[^>]*>/g, '');

const output = `// Auto-generated self-contained arcade bundle for Expo WebView
export const ARCADE_HTML = ${JSON.stringify(html)};
`;

fs.writeFileSync(path.join(__dirname, 'arcadeHtml.js'), output, 'utf8');
console.log(`Successfully generated arcadeHtml.js! Size: ${(output.length / 1024).toFixed(1)} KB`);
console.log(`Inlined ${jsFileNames.length} JS file(s): ${jsFileNames.join(', ')}`);

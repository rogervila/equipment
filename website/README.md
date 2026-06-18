# Equipment Website

This website is built with Docusaurus and deployed on Vercel.

## Install

```bash
npm ci
```

## Develop

```bash
npm run start
```

## Build

```bash
npm run build
```

The build writes generated files to `build/`. Vercel runs the same npm-based build path.

## LLM Files

The public LLM files are generated during `npm run build` by `docusaurus-plugin-llms`:

- `https://equipment-python.vercel.app/llms.txt`
- `https://equipment-python.vercel.app/llms-full.txt`

Do not hand-edit generated files in `build/`. Update the source docs under `docs/` and the plugin root content in `docusaurus.config.js` when the LLM output needs to change.

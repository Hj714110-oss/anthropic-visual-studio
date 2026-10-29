# Public and local assets

The public library has three original MIT examples: `STUDIO-thought`, `STUDIO-growth`, `STUDIO-connection`. They are newly authored geometric examples, not Anthropic illustrations or archive reconstructions.

`assets/library/catalog.json` records actual SVG paths, source hashes and license. `assets/prepared/` contains recolorable forms using `__INK__`, `__PAPER__`, `__ACCENT__`. The scaffold copies used original files and writes `sources.json`.

## Optional local archive

```text
python scripts/import_local_assets.py --from <existing-private-skill-folder>
```

Input must be an extracted private skill folder containing `assets/library/catalog.json`, `assets/prepared/`, and optionally `assets/fonts/`. ZIPs are not automatically fetched or extracted. The importer verifies referenced original files and hashes, then copies only the known library, prepared, and font directories to `assets/local/`. It refuses to overwrite an existing import. Catalog queries merge the public and local libraries.

Local content is ignored by Git. It retains its original licensing and historical-version limits. Missing large reconstructions remain preview-only. Inspect returned paths; `full_version_reconstruction` is a historical pointer, not a delivered file. Exclude blank responses from designs.

If all three private font files exist, the scaffold includes them with local @font-face declarations. Otherwise it uses installed system fonts without failed remote requests. The private font names are AnthropicSerifWebText.ttf, AnthropicSansWebText.ttf and AnthropicMonoVariable.ttf. Chinese glyphs require fallback. File possession does not change permissions.

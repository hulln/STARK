# Data

The corpus file used for this verification is the official UD Slovenian SSJ dev file:

- Repository: [`UniversalDependencies/UD_Slovenian-SSJ`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ)
- File: [`sl_ssj-ud-dev.conllu`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu)
- Commit: [`212197db9aebc89dbdf8c1631f3fcc29b88840d4`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/commit/212197db9aebc89dbdf8c1631f3fcc29b88840d4)
- Raw download: [`sl_ssj-ud-dev.conllu`](https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu)
- Local expected path: `nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu`
- SHA-256: `2999a1ac8261df77e71c4e824c8e036e4845f84748f36d04bc7b730d7daf9d9a`
- Line count: `31883`
- Sentence count: `1250`

Download command:

```bash
curl -L -o nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu \
  https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu
```

Verify the checksum:

```bash
sha256sum nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu
```

The `.conllu` file is intentionally ignored by git. The saved outputs, reports, manifest, checksum, and download command are tracked so the comparison remains reproducible without committing the corpus file itself.

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

## Train and test splits (comparison extended to the whole SSJ treebank)

The same comparison was extended to the `train` and `test` splits of the same
treebank, obtained online from UD the same way as the dev file.

| Split | Local path | SHA-256 | Lines | Sentences |
|---|---|---|---|---|
| train | `data/sl_ssj-ud-train.UD-Slovenian-SSJ-212197d.conllu` | `c6991732aaecf8d6346bb10e154898093337ad93c6f029c0bd7c55ba94957243` | `261861` | `10903` |
| test  | `data/sl_ssj-ud-test.UD-Slovenian-SSJ-212197d.conllu`  | `c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0` | `30916`  | `1282`  |

Latest-version note: at the time of writing, UD master HEAD is
[`17011b12eae4e522da4d1eeeffd439085466623c`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/commit/17011b12eae4e522da4d1eeeffd439085466623c),
which is newer than the dev pin `212197db…`. The `dev`, `train`, and `test`
files are **byte-identical** at both commits (verified by SHA-256), so these
files are simultaneously the latest online version and consistent with the dev
file already used. The `212197d` suffix is kept only for naming consistency.

Download commands (latest master; identical content to the dev pin):

```bash
curl -L -o nh-work/complexity-comparison/data/sl_ssj-ud-train.UD-Slovenian-SSJ-212197d.conllu \
  https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/master/sl_ssj-ud-train.conllu
curl -L -o nh-work/complexity-comparison/data/sl_ssj-ud-test.UD-Slovenian-SSJ-212197d.conllu \
  https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/master/sl_ssj-ud-test.conllu
```

See `docs/SSJ_TRAIN_TEST_RESULTS.md` for the train/test comparison results.

## Git tracking

The `.conllu` files are intentionally ignored by git. The saved outputs, reports, manifest, checksum, and download command are tracked so the comparison remains reproducible without committing the corpus file itself.

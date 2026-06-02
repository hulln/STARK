#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_WORK_DIR = BASE_DIR / "tmp/syntcomplex-run"
DEFAULT_OUTPUT = BASE_DIR / "outputs/syntcomplex/syntcomplex_sl_ssj_dev.tsv"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the pinned SyntComplex reference script on the pinned SSJ dev data."
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=DEFAULT_WORK_DIR,
        help="Generated working directory for SyntComplex hardcoded input paths.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination for SyntComplex ssj_results.tsv.",
    )
    parser.add_argument(
        "--keep-work-dir",
        action="store_true",
        help="Keep the generated work directory after running.",
    )
    return parser.parse_args()


def touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def main():
    args = parse_args()
    source_dir = BASE_DIR / "external/SyntComplex"
    corpus = BASE_DIR / "data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu"

    if not (source_dir / "scripts/calculate_metrics.py").exists():
        raise FileNotFoundError(source_dir / "scripts/calculate_metrics.py")
    if not corpus.exists():
        raise FileNotFoundError(corpus)

    if args.work_dir.exists():
        shutil.rmtree(args.work_dir)
    shutil.copytree(source_dir, args.work_dir)

    ssj_dir = args.work_dir / "UD_Slovenian-SSJ-master"
    sst_dir = args.work_dir / "UD_Slovenian-SST-master"
    ssj_dir.mkdir(parents=True, exist_ok=True)
    sst_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(corpus, ssj_dir / "sl_ssj-ud-dev.conllu")
    touch(ssj_dir / "sl_ssj-ud-train.conllu")
    touch(ssj_dir / "sl_ssj-ud-test.conllu")
    touch(sst_dir / "sl_sst-ud-train.conllu")
    touch(sst_dir / "sl_sst-ud-test.conllu")

    subprocess.run(
        [sys.executable, "scripts/calculate_metrics.py"],
        cwd=args.work_dir,
        check=True,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.work_dir / "ssj_results.tsv", args.output)

    if not args.keep_work_dir:
        shutil.rmtree(args.work_dir)
        if args.work_dir.parent == DEFAULT_WORK_DIR.parent:
            try:
                args.work_dir.parent.rmdir()
            except OSError:
                pass

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

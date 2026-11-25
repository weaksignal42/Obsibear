#!/usr/bin/env python3
"""Obsibear — construit les thèmes Obsidian inspirés des thèmes de Bear.

Chaque thème vit dans themes/<dossier>/ (theme.css + manifest.json).
Le script y ajoute les polices de Bear, lues dans l'application Bear installée,
converties en woff2 et intégrées en base64. Les polices ne sont jamais
versionnées : elles appartiennent à Shiny Frog.

Usage :
    python3 build.py                          # construit tous les thèmes dans dist/
    python3 build.py olive-dunk               # un seul thème
    python3 build.py --install ~/chemin/vers/MonCoffre
    python3 build.py --bear /Applications/Bear.app

Dépendances : pip install -r requirements.txt  (fonttools, brotli)
"""
import argparse
import base64
import io
import json
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
THEMES = ROOT / "themes"

# (famille CSS, fichier dans Bear.app/Contents/Resources, graisse, style)
FACES = [
    ("Olive Bear Sans", "BearSansUI-Regular.otf", 400, "normal"),
    ("Olive Bear Sans", "BearSansUI-Italic.otf", 400, "italic"),
    ("Olive Bear Sans", "BearSansUI-Medium.otf", 500, "normal"),
    ("Olive Bear Sans", "BearSansUI-MediumItalic.otf", 500, "italic"),
    ("Olive Bear Sans", "BearSansUI-Bold.otf", 700, "normal"),
    ("Olive Bear Sans", "BearSansUI-BoldItalic.otf", 700, "italic"),
    # La police de titre « Regular » de Bear a une graisse réelle de 600.
    ("Olive Bear Sans Heading", "BearSansUIHeading-Regular.otf", 600, "normal"),
    ("Olive Bear Sans Heading", "BearSansUIHeading-RegularItalic.otf", 600, "italic"),
    ("Olive Bear Sans Heading", "BearSansUIHeading-Bold.otf", 700, "normal"),
    ("Olive Bear Sans Heading", "BearSansUIHeading-BoldItalic.otf", 700, "italic"),
    ("Olive Roboto Mono", "RobotoMono-Regular.ttf", 400, "normal"),
]


def font_faces(resources: Path) -> str:
    blocks = ["/* ---------- Polices de Bear intégrées (usage personnel) ---------- */"]
    for family, filename, weight, style in FACES:
        path = resources / filename
        if not path.exists():
            raise SystemExit(f"Police introuvable : {path}")
        font = TTFont(path)
        font.flavor = "woff2"
        buf = io.BytesIO()
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        blocks.append(
            "@font-face {\n"
            f'  font-family: "{family}";\n'
            f'  src: url(data:font/woff2;base64,{data}) format("woff2");\n'
            f"  font-weight: {weight};\n"
            f"  font-style: {style};\n"
            "  font-display: block;\n"
            "}"
        )
    return "\n".join(blocks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("themes", nargs="*", help="dossiers de themes/ à construire (défaut : tous)")
    parser.add_argument("--bear", default="/Applications/Bear.app", help="chemin de Bear.app")
    parser.add_argument("--install", metavar="COFFRE", help="copie les thèmes dans <COFFRE>/.obsidian/themes/")
    args = parser.parse_args()

    folders = [THEMES / t for t in args.themes] or sorted(p for p in THEMES.iterdir() if p.is_dir())
    fonts = font_faces(Path(args.bear).expanduser() / "Contents" / "Resources")

    for folder in folders:
        if not (folder / "theme.css").exists():
            raise SystemExit(f"Thème introuvable : {folder}")
        name = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))["name"]
        css = (folder / "theme.css").read_text(encoding="utf-8").rstrip() + "\n\n" + fonts

        out = ROOT / "dist" / name
        out.mkdir(parents=True, exist_ok=True)
        (out / "theme.css").write_text(css, encoding="utf-8")
        shutil.copy(folder / "manifest.json", out / "manifest.json")
        print(f"Construit : {name}  ({len(css) // 1024} Ko)")

        if args.install:
            target = Path(args.install).expanduser() / ".obsidian" / "themes" / name
            target.mkdir(parents=True, exist_ok=True)
            for f in ("theme.css", "manifest.json"):
                shutil.copy(out / f, target / f)
            print(f"  installé dans : {target}")


if __name__ == "__main__":
    main()

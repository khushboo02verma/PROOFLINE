"""Agent 1 - Librarian. Indexes every file in the library and reads hidden metadata in images.

Job: know what exists before anyone writes anything. No interpretation."""
from __future__ import annotations

import re

from ..core import RunContext, md_table

DATE_IN_NAME = re.compile(r"(20\d\d)[-_](\d\d)[-_](\d\d)")


def image_metadata(path) -> dict:
    from PIL import Image
    from PIL.ExifTags import GPSTAGS, TAGS

    meta = {}
    with Image.open(path) as im:
        meta["size"] = f"{im.width}x{im.height}"
        exif = im.getexif()
        for k, v in exif.items():
            meta[TAGS.get(k, str(k))] = str(v)
        gps = exif.get_ifd(0x8825)
        if gps:
            g = {GPSTAGS.get(k, str(k)): v for k, v in gps.items()}

            def deg(t):
                return round(float(t[0]) + float(t[1]) / 60 + float(t[2]) / 3600, 4)

            try:
                meta["GPS"] = f"{deg(g['GPSLatitude'])}{g.get('GPSLatitudeRef', '')}, {deg(g['GPSLongitude'])}{g.get('GPSLongitudeRef', '')}"
            except (KeyError, TypeError, ValueError):
                meta["GPS"] = str(g)
        for k, v in im.info.items():
            if k not in ("icc_profile", "exif", "dpi", "jfif", "jfif_version", "jfif_unit", "jfif_density"):
                meta[k] = str(v)
    return meta


def run(ctx: RunContext) -> dict:
    lib = ctx.library
    rows, index = [], []
    for p in lib.files:
        rel = lib.rel(p)
        m = DATE_IN_NAME.search(rel)
        entry = {"file": rel, "folder": rel.split("/")[0], "bytes": p.stat().st_size,
                 "date_hint": "-".join(m.groups()) if m else ""}
        if rel in lib.text_files():
            entry["lines"] = len(lib.text(rel).splitlines())
        if rel in lib.image_files():
            entry["image_meta"] = image_metadata(p)
        index.append(entry)
        rows.append([rel, entry["date_hint"], entry.get("lines", ""), entry["bytes"],
                     "; ".join(f"{k}={v}" for k, v in entry.get("image_meta", {}).items())])
    md = ["# Library index", "", f"Library: `{lib.root.name}` - {len(index)} files.", "",
          md_table(["File", "Date in name", "Lines", "Bytes", "Image metadata (EXIF / PNG text)"], rows)]
    ctx.write("00_library_index.md", "\n".join(md) + "\n")
    ctx.write_json("work/library_index.json", index)
    images_with_meta = [e for e in index if e.get("image_meta") and len(e["image_meta"]) > 1]
    ctx.note("librarian", f"indexed {len(index)} files; {len(images_with_meta)} images carry metadata")
    return {"index": index}

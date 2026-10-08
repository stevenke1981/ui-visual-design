#!/usr/bin/env python3
"""WCAG 2.x contrast checker for colour pairs or CSS custom-property tokens.

  python contrast.py "#203832" "#f3f6f5"                 # one pair (add --large for 3:1)
  python contrast.py --css style.css --list              # show theme blocks and colour tokens
  python contrast.py --css style.css --pairs "text/bg,muted/surface,focus/bg:3"
  python contrast.py --css style.css --pairs "..." --only ":root" --only "dark"

Always pass --pairs with the file's REAL token names (run --list first). The
built-in default pairs only fit files that use the names in web.md.
"fg/bg" needs 4.5:1 (normal text); ":3" = large text, icons, input borders,
focus rings (WCAG 1.4.3 / 1.4.11).

Semi-transparent colours (rgba(), #rrggbbaa) are alpha-composited: the
background over --base (default: the block's --bg / --surface or white), then
the foreground over that result. Results involving alpha are marked "(alpha)".

Theme blocks: every rule that declares custom properties is a block; the first
block (normally :root) supplies fallbacks. A block that overrides tokens only
for a component scope (e.g. ".record { --focus: ... }") is still checked against
page tokens; exclude it with --only or check it with explicit pairs.
Exit code 1 if any checked pair fails; missing tokens are listed, not failed.
"""
import argparse
import re
import sys

DEFAULT_PAIRS = [
    "text/bg", "muted/bg", "text/surface", "muted/surface",
    "brand/surface:3", "input-border/surface:3", "brand-ink/brand",
    "danger/surface", "danger-ink/danger", "focus/bg:3", "focus/surface:3",
]


def parse_color(value):
    """Return (r, g, b, a) with a in 0..1, or None."""
    v = value.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)\s*(?:[,/]\s*([\d.]+%?))?\s*\)", v)
    if m:
        a = m.group(4)
        alpha = 1.0 if a is None else (float(a[:-1]) / 100 if a.endswith("%") else float(a))
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), alpha)
    if v in ("white", "#fff"):
        return (255, 255, 255, 1.0)
    if v == "black":
        return (0, 0, 0, 1.0)
    return None


def over(fg, bg):
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def luminance(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def theme_blocks(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    blocks = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        decls = dict(re.findall(r"--([\w-]+)\s*:\s*([^;]+);", m.group(2)))
        if decls:
            blocks.append((" ".join(m.group(1).split()), decls))
    return blocks


def resolve(name, tokens, depth=0):
    v = tokens.get(name)
    if v is None or depth > 10:
        return None
    m = re.fullmatch(r"\s*var\(--([\w-]+)(?:\s*,\s*([^)]+))?\)\s*", v)
    if m:
        return resolve(m.group(1), tokens, depth + 1) or (parse_color(m.group(2)) if m.group(2) else None)
    return parse_color(v)


def check(fg, bg, need, label, base):
    alpha = fg[3] < 1 or bg[3] < 1
    bg_s = over(bg, base) if bg[3] < 1 else bg
    fg_s = over(fg, bg_s) if fg[3] < 1 else fg
    r = ratio(fg_s, bg_s)
    ok = r >= need
    print(f"{'PASS' if ok else 'FAIL'}  {r:5.2f}:1 (need {need}:1)  {label}{'  (alpha)' if alpha else ''}")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("colors", nargs="*")
    ap.add_argument("--css")
    ap.add_argument("--pairs", default=",".join(DEFAULT_PAIRS))
    ap.add_argument("--only", action="append", default=[], help="check only blocks whose selector contains this text (repeatable)")
    ap.add_argument("--list", action="store_true", help="list blocks and colour tokens, then exit")
    ap.add_argument("--base", default=None, help="colour under translucent backgrounds (default: block --bg/--surface, else white)")
    ap.add_argument("--large", action="store_true", help="3:1 threshold for a direct pair")
    a = ap.parse_args()
    white = (255, 255, 255, 1.0)
    if len(a.colors) == 2:
        fg, bg = (parse_color(c) for c in a.colors)
        if not fg or not bg:
            sys.exit("unparseable colour")
        base = parse_color(a.base) if a.base else white
        sys.exit(0 if check(fg, bg, 3 if a.large else 4.5, f"{a.colors[0]} on {a.colors[1]}", base) else 1)
    if not a.css:
        ap.print_help()
        sys.exit(2)
    blocks = theme_blocks(open(a.css, encoding="utf-8").read())
    if not blocks:
        sys.exit("no custom properties found")
    root = dict(blocks[0][1])
    if a.list:
        for label, decls in blocks:
            colours = [k for k in decls if resolve(k, {**root, **decls})]
            print(f"[{label}]\n  colour tokens: {', '.join(colours) or '-'}")
        return
    ok = True
    for idx, (label, decls) in enumerate(blocks):
        if a.only and not any(s in label for s in a.only):
            continue
        tokens = decls if idx == 0 else {**root, **decls}
        base = parse_color(a.base) if a.base else (resolve("bg", tokens) or resolve("surface", tokens) or white)
        if base[3] < 1:
            base = over(base, white)
        print(f"\n[{label[-70:]}]")
        missing = []
        for spec in a.pairs.split(","):
            spec = spec.strip()
            if not spec:
                continue
            need = 4.5
            if ":" in spec:
                spec, n = spec.rsplit(":", 1)
                need = float(n)
            f, b = spec.split("/")
            if idx > 0 and f not in decls and b not in decls:
                continue  # nothing in this block changes the pair; already checked in the base block
            fc, bc = resolve(f, tokens), resolve(b, tokens)
            if not fc or not bc:
                missing.append(f"--{f}/--{b}")
                continue
            ok &= check(fc, bc, need, f"--{f} on --{b}", base)
        if missing:
            print(f"skip  (token missing or not a colour): {', '.join(missing)}  -> run --list and pass real names")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

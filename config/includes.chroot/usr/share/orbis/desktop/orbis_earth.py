#!/usr/bin/python3
"""ORBIS Earth: lightweight offline GeoJSON viewer for the ORBIS desktop."""
import json
import math
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

BG = "#081b29"
PANEL = "#102b3b"
ACCENT = "#36cfc2"
TEXT = "#e4f3f5"
MUTED = "#8baab5"

class EarthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ORBIS Earth")
        self.root.geometry("1100x720")
        self.root.minsize(760, 480)
        self.root.configure(bg=BG)
        self.document = None
        self.source = "No dataset loaded"
        self.features = []
        self._build()
        self._draw_empty()

    def _build(self):
        header = tk.Frame(self.root, bg=PANEL, height=66)
        header.pack(fill="x")
        tk.Label(header, text="ORBIS", bg=PANEL, fg=ACCENT,
                 font=("DejaVu Sans", 19, "bold")).pack(side="left", padx=(22, 8), pady=15)
        tk.Label(header, text="EARTH  /  GEOSPATIAL EXPLORER", bg=PANEL, fg=TEXT,
                 font=("DejaVu Sans", 10, "bold")).pack(side="left", pady=20)
        tk.Button(header, text="Open GeoJSON", command=self.open_file,
                  bg=ACCENT, fg="#06202a", relief="flat", padx=16,
                  font=("DejaVu Sans", 10, "bold")).pack(side="right", padx=18, pady=14)
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=16)
        side = tk.Frame(body, bg=PANEL, width=245)
        side.pack(side="left", fill="y", padx=(0, 14))
        side.pack_propagate(False)
        tk.Label(side, text="DATASET", bg=PANEL, fg=ACCENT,
                 font=("DejaVu Sans", 9, "bold")).pack(anchor="w", padx=16, pady=(20, 6))
        self.file_label = tk.Label(side, text=self.source, bg=PANEL, fg=TEXT,
                                   wraplength=210, justify="left")
        self.file_label.pack(anchor="w", padx=16)
        tk.Label(side, text="LAYER SUMMARY", bg=PANEL, fg=ACCENT,
                 font=("DejaVu Sans", 9, "bold")).pack(anchor="w", padx=16, pady=(28, 8))
        self.summary = tk.Label(side, text="Features: —\nGeometries: —\nExtent: —",
                                bg=PANEL, fg=TEXT, justify="left", wraplength=215)
        self.summary.pack(anchor="w", padx=16)
        tk.Label(side, text="Offline viewer · GeoJSON · WGS84 lon/lat",
                 bg=PANEL, fg=MUTED, wraplength=210, justify="left").pack(side="bottom", anchor="w", padx=16, pady=18)
        self.canvas = tk.Canvas(body, bg="#0b2534", highlightthickness=1,
                                highlightbackground="#245365")
        self.canvas.pack(side="right", fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.redraw())

    def _draw_empty(self):
        self.canvas.create_text(350, 230, text="ORBIS EARTH", fill=ACCENT,
                                font=("DejaVu Sans", 25, "bold"))
        self.canvas.create_text(350, 270, text="Open a GeoJSON dataset to explore its features",
                                fill=TEXT, font=("DejaVu Sans", 11))

    def open_file(self):
        name = filedialog.askopenfilename(filetypes=[("GeoJSON", "*.geojson *.json"), ("All files", "*")])
        if not name:
            return
        try:
            data = json.loads(Path(name).read_text(encoding="utf-8"))
            self._validate_root(data)
            self.document = data
            self.source = Path(name).name
            self.features = self._features(data)
            points = [p for f in self.features for p in self._coordinates(f.get("geometry"))]
            if points:
                xs, ys = [p[0] for p in points], [p[1] for p in points]
                extent = f"{min(xs):.3f}, {min(ys):.3f}\n{max(xs):.3f}, {max(ys):.3f}"
            else:
                extent = "No coordinates"
            self.file_label.config(text=self.source)
            self.summary.config(text=f"Features: {len(self.features)}\nCoordinates: {len(points)}\nExtent (W,S / E,N):\n{extent}")
            self.redraw()
        except Exception as exc:
            messagebox.showerror("Cannot open dataset", str(exc))

    @staticmethod
    def _validate_root(data):
        if not isinstance(data, dict) or data.get("type") not in ("Feature", "FeatureCollection", "GeometryCollection", "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"):
            raise ValueError("Unsupported or invalid GeoJSON document.")

    @staticmethod
    def _features(data):
        kind = data.get("type")
        if kind == "FeatureCollection":
            return data.get("features", [])
        if kind == "Feature":
            return [data]
        if kind == "GeometryCollection":
            return [{"type": "Feature", "geometry": g, "properties": {}} for g in data.get("geometries", [])]
        return [{"type": "Feature", "geometry": data, "properties": {}}]

    @staticmethod
    def _coordinates(geometry):
        if not geometry:
            return []
        kind, coords = geometry.get("type"), geometry.get("coordinates")
        if kind == "GeometryCollection":
            return [p for g in geometry.get("geometries", []) for p in EarthApp._coordinates(g)]
        out = []
        def walk(value):
            if isinstance(value, (list, tuple)) and len(value) >= 2 and all(isinstance(v, (int, float)) for v in value[:2]):
                if math.isfinite(value[0]) and math.isfinite(value[1]):
                    out.append((value[0], value[1]))
            elif isinstance(value, (list, tuple)):
                for child in value:
                    walk(child)
        walk(coords)
        return out

    def redraw(self):
        if not self.canvas.winfo_exists():
            return
        self.canvas.delete("all")
        w, h = max(self.canvas.winfo_width(), 100), max(self.canvas.winfo_height(), 100)
        for lon in range(-180, 181, 30):
            x = (lon + 180) / 360 * w
            self.canvas.create_line(x, 0, x, h, fill="#153d4d")
        for lat in range(-60, 61, 30):
            y = (90 - lat) / 180 * h
            self.canvas.create_line(0, y, w, y, fill="#153d4d")
        if not self.document:
            self._draw_empty()
            return
        points = [p for f in self.features for p in self._coordinates(f.get("geometry"))]
        if not points:
            self.canvas.create_text(w/2, h/2, text="Dataset has no drawable coordinates", fill=TEXT)
            return
        minx, maxx = min(p[0] for p in points), max(p[0] for p in points)
        miny, maxy = min(p[1] for p in points), max(p[1] for p in points)
        dx, dy = max(maxx-minx, 0.01), max(maxy-miny, 0.01)
        scale = min((w-70)/dx, (h-70)/dy)
        ox = (w - dx*scale)/2
        oy = (h - dy*scale)/2
        def xy(p):
            return ox + (p[0]-minx)*scale, h - oy - (p[1]-miny)*scale
        def draw_geom(g):
            if not g:
                return
            kind, c = g.get("type"), g.get("coordinates")
            if kind == "GeometryCollection":
                for child in g.get("geometries", []): draw_geom(child)
            elif kind == "Point":
                x, y = xy(c); self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=ACCENT, outline="")
            elif kind == "MultiPoint":
                for p in c: draw_geom({"type":"Point", "coordinates":p})
            elif kind == "LineString":
                flat = [v for p in c for v in xy(p)]
                if len(flat) >= 4: self.canvas.create_line(*flat, fill=ACCENT, width=2)
            elif kind == "MultiLineString":
                for line in c: draw_geom({"type":"LineString", "coordinates":line})
            elif kind == "Polygon":
                for ring in c:
                    flat = [v for p in ring for v in xy(p)]
                    if len(flat) >= 6: self.canvas.create_polygon(*flat, fill="#1b8078", outline=ACCENT, stipple="gray25")
            elif kind == "MultiPolygon":
                for poly in c: draw_geom({"type":"Polygon", "coordinates":poly})
        for feature in self.features:
            draw_geom(feature.get("geometry"))

def main():
    root = tk.Tk()
    EarthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

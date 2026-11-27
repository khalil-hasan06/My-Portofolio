"""
================================================================================
          THE CELESTIAL ASTRAL LEVIATHAN (MASTERPIECE EDITION)
================================================================================
Spesies Mahakarya Paling Sempurna:
Perpaduan Naga Mistis Kosmik & Paus Samudra Bintang (Celestial Astral Leviathan).

Fitur:
- Pure Inverse Kinematics (Lurus sempurna saat melesat, lentur sutra saat meliuk)
- Kumis naga kembar 14 ruas yang berkibar dinamis (sangar & mistis)
- Sirip dayung bersayap (Pectoral flipper-wings) yang menekuk aerodinamis saat dive
- Ekor kipas sutra bercabang (Silk veil flukes) dengan semburan debu bintang
- Tanduk rusa emas-cyan, taring tajam, dan mata berlian bersinar
- Semburan Supernova Shockwave multi-warna saat klik

Cara Menjalankan:
   python dragon_companion.py
================================================================================
"""

import tkinter as tk
import math
import random

class CelestialLeviathanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Celestial Astral Leviathan — Masterpiece Edition")
        self.root.geometry("1050x720")
        self.root.configure(bg="#050510")

        self.canvas = tk.Canvas(root, bg="#050510", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.mouse_x = 525
        self.mouse_y = 360
        self.head_x = 525
        self.head_y = 360
        self.head_angle = 0.0
        self.speed = 0.0

        self.num_segments = 28
        self.seg_dist = 9.0
        self.segments = []

        for i in range(self.num_segments):
            radius = self.get_radius(i)
            self.segments.append({
                "x": self.mouse_x - i * self.seg_dist,
                "y": self.mouse_y,
                "angle": 0.0,
                "radius": radius
            })

        self.whisker_joints = 14
        self.whisker_dist = 6.8
        self.whisker_l = [{"x": self.mouse_x, "y": self.mouse_y, "vx": 0.0, "vy": 0.0} for _ in range(self.whisker_joints)]
        self.whisker_r = [{"x": self.mouse_x, "y": self.mouse_y, "vx": 0.0, "vy": 0.0} for _ in range(self.whisker_joints)]

        self.shockwaves = []
        self.particles = []
        self.time = 0

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)

        info = tk.Label(
            self.canvas,
            text="✨ THE CELESTIAL ASTRAL LEVIATHAN (VERSI PALING SEMPURNA)\nTarik cepat untuk melihat naga lurus seperti tombak — Klik untuk Supernova Shockwave!",
            bg="#050510",
            fg="#00E5FF",
            font=("Space Grotesk", 12, "bold")
        )
        info.place(relx=0.5, rely=0.06, anchor=tk.CENTER)

        self.animate()

    def get_radius(self, i):
        if i == 0:
            return 11.0
        if i < 6:
            return 10.0 + i * 0.7
        t = (i - 6) / max(1, self.num_segments - 7)
        return max(1.8, 14.0 * (1.0 - t * 0.88))

    def on_mouse_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_click(self, event):
        self.shockwaves.append({"x": event.x, "y": event.y, "r": 6.0, "max_r": 55.0, "life": 1.0, "decay": 0.04, "color": "#00E5FF"})
        self.shockwaves.append({"x": event.x, "y": event.y, "r": 2.0, "max_r": 35.0, "life": 1.0, "decay": 0.06, "color": "#FF6B9D"})

        colors = ["#00E5FF", "#00D4AA", "#6C63FF", "#FF6B9D", "#FFFFFF"]
        for _ in range(30):
            ang = random.uniform(0, math.pi * 2)
            spd = random.uniform(3.5, 9.5)
            self.particles.append({
                "x": event.x,
                "y": event.y,
                "vx": math.cos(ang) * spd,
                "vy": math.sin(ang) * spd,
                "size": random.uniform(2.0, 4.0),
                "life": 1.0,
                "decay": random.uniform(0.02, 0.035),
                "color": random.choice(colors)
            })

    def animate(self):
        self.time += 1
        self.canvas.delete("leviathan")

        dx = self.mouse_x - self.head_x
        dy = self.mouse_y - self.head_y
        dist = math.hypot(dx, dy)
        self.head_x += dx * 0.22
        self.head_y += dy * 0.22
        self.speed = dist

        if dist > 1.0:
            target_angle = math.atan2(dy, dx)
            diff = target_angle - self.head_angle
            while diff < -math.pi:
                diff += math.pi * 2
            while diff > math.pi:
                diff -= math.pi * 2
            self.head_angle += diff * 0.26

        self.segments[0]["x"] = self.head_x
        self.segments[0]["y"] = self.head_y
        self.segments[0]["angle"] = self.head_angle

        # Pure IK: 100% straight when moving fast!
        idle_amp = max(0.0, (1.0 - min(1.0, self.speed / 14.0))) * 2.0

        for i in range(1, self.num_segments):
            prev = self.segments[i - 1]
            curr = self.segments[i]

            sx = curr["x"] - prev["x"]
            sy = curr["y"] - prev["y"]
            s_dist = math.hypot(sx, sy) or 0.001

            nx = -sy / s_dist
            ny = sx / s_dist
            wave = math.sin(self.time * 0.11 - i * 0.34) * idle_amp if idle_amp > 0.05 else 0.0

            curr["x"] = prev["x"] + (sx / s_dist) * self.seg_dist + nx * wave
            curr["y"] = prev["y"] + (sy / s_dist) * self.seg_dist + ny * wave
            curr["angle"] = math.atan2(curr["y"] - prev["y"], curr["x"] - prev["x"])

        # Whiskers
        snout_x = self.head_x + math.cos(self.head_angle) * 17
        snout_y = self.head_y + math.sin(self.head_angle) * 17
        perp_x = -math.sin(self.head_angle)
        perp_y = math.cos(self.head_angle)

        self.whisker_l[0]["x"] = snout_x + perp_x * 3.5
        self.whisker_l[0]["y"] = snout_y + perp_y * 3.5
        self.whisker_r[0]["x"] = snout_x - perp_x * 3.5
        self.whisker_r[0]["y"] = snout_y - perp_y * 3.5

        def update_whisker(wh, side):
            for i in range(1, len(wh)):
                prev = wh[i - 1]
                curr = wh[i]
                curr["vx"] = curr["vx"] * 0.76 + (prev["x"] - curr["x"]) * 0.34
                curr["vy"] = curr["vy"] * 0.76 + (prev["y"] - curr["y"]) * 0.34
                flutter = math.sin(self.time * 0.2 + i * 0.55) * (1.2 + self.speed * 0.05) * side
                curr["vx"] += perp_x * flutter * 0.1
                curr["vy"] += perp_y * flutter * 0.1
                curr["x"] += curr["vx"]
                curr["y"] += curr["vy"]

                ddx = curr["x"] - prev["x"]
                ddy = curr["y"] - prev["y"]
                d = math.hypot(ddx, ddy) or 0.001
                curr["x"] = prev["x"] + (ddx / d) * self.whisker_dist
                curr["y"] = prev["y"] + (ddy / d) * self.whisker_dist

        update_whisker(self.whisker_l, 1)
        update_whisker(self.whisker_r, -1)

        # Draw Shockwaves
        for sw in self.shockwaves[:]:
            sw["r"] += (sw["max_r"] - sw["r"]) * 0.18
            sw["life"] -= sw["decay"]
            if sw["life"] <= 0:
                self.shockwaves.remove(sw)
                continue
            self.canvas.create_oval(
                sw["x"] - sw["r"], sw["y"] - sw["r"], sw["x"] + sw["r"], sw["y"] + sw["r"],
                outline=sw["color"], width=int(2 * sw["life"] + 1), tags="leviathan"
            )

        # Draw Stardust Particles
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] *= 0.95
            p["vy"] *= 0.95
            p["life"] -= p["decay"]
            if p["life"] <= 0:
                self.particles.remove(p)
                continue
            r = p["size"] * p["life"]
            self.canvas.create_oval(
                p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r,
                fill=p["color"], outline="", tags="leviathan"
            )

        # Draw Pectoral Wings/Flippers at segment 4
        s4 = self.segments[4]
        spd_fac = min(1.0, self.speed / 20.0)
        tuck = spd_fac * 0.55
        flap = math.sin(self.time * 0.12) * 0.25 * (1.0 - spd_fac * 0.5)
        span = 44 - spd_fac * 10
        for side in (-1, 1):
            rx = s4["x"]
            ry = s4["y"]
            ea = s4["angle"] + (side * (math.pi / 2.3) - tuck * side) + flap * side
            ex = rx + math.cos(ea) * (span * 0.55)
            ey = ry + math.sin(ea) * (span * 0.55)
            ta = ea + (side * 0.32) - tuck * 0.5 * side
            tx = ex + math.cos(ta) * (span * 0.75)
            ty = ey + math.sin(ta) * (span * 0.75)
            f2x = ex + math.cos(ta - side * 0.35) * (span * 0.55)
            f2y = ey + math.sin(ta - side * 0.35) * (span * 0.55)

            self.canvas.create_polygon(
                rx, ry, ex, ey, tx, ty, f2x, f2y,
                fill="#00D4AA", outline="#FFFFFF", width=1.5, tags="leviathan"
            )

        # Draw Dorsal Crest (Sirip Punggung)
        for i in range(2, self.num_segments - 4, 2):
            seg = self.segments[i]
            nx = -math.sin(seg["angle"])
            ny = math.cos(seg["angle"])
            len_c = seg["radius"] * 1.4
            bx = seg["x"] + nx * (seg["radius"] + len_c) - math.cos(seg["angle"]) * 8
            by = seg["y"] + ny * (seg["radius"] + len_c) - math.sin(seg["angle"]) * 8
            c = "#00E5FF" if i < 10 else ("#6C63FF" if i < 18 else "#FF6B9D")
            self.canvas.create_polygon(
                seg["x"], seg["y"], bx, by, seg["x"] - math.cos(seg["angle"]) * 10, seg["y"] - math.sin(seg["angle"]) * 10,
                fill=c, tags="leviathan"
            )

        # Draw Segments (Celestial Gradient from Cyan to Purple to Pink)
        for i in range(self.num_segments - 1, -1, -1):
            seg = self.segments[i]
            r = seg["radius"]
            t = i / self.num_segments
            if t < 0.3:
                color = "#00E5FF"
            elif t < 0.65:
                color = "#6C63FF"
            else:
                color = "#FF6B9D"

            self.canvas.create_oval(
                seg["x"] - r, seg["y"] - r, seg["x"] + r, seg["y"] + r,
                fill=color, outline="#FFFFFF", width=1, tags="leviathan"
            )

        # Draw Silk Veil Flukes (Ekor Kipas Sutra)
        tail = self.segments[-1]
        ta = tail["angle"]
        span = 26.0
        tip_l_x = tail["x"] + math.cos(ta) * 14 - math.sin(ta) * span
        tip_l_y = tail["y"] + math.sin(ta) * 14 + math.cos(ta) * span
        tip_r_x = tail["x"] + math.cos(ta) * 14 + math.sin(ta) * span
        tip_r_y = tail["y"] + math.sin(ta) * 14 - math.cos(ta) * span
        notch_x = tail["x"] + math.cos(ta) * 4
        notch_y = tail["y"] + math.sin(ta) * 4

        self.canvas.create_polygon(
            tail["x"], tail["y"],
            tail["x"] + math.cos(ta) * 6 - math.sin(ta) * (span * 0.65), tail["y"] + math.sin(ta) * 6 + math.cos(ta) * (span * 0.65),
            tip_l_x, tip_l_y,
            notch_x, notch_y,
            tip_r_x, tip_r_y,
            tail["x"] + math.cos(ta) * 6 + math.sin(ta) * (span * 0.65), tail["y"] + math.sin(ta) * 6 - math.cos(ta) * (span * 0.65),
            fill="#FF2A6D", outline="#FFFFFF", width=1.5, tags="leviathan"
        )

        # Draw Leviathan Head & Horns
        head = self.segments[0]
        hx, hy, ha = head["x"], head["y"], head["angle"]
        for side in (-1, 1):
            # Antler Horn
            h1x = hx - math.cos(ha) * 14 + math.cos(ha + math.pi/2 * side) * 12
            h1y = hy - math.sin(ha) * 14 + math.sin(ha + math.pi/2 * side) * 12
            h2x = hx - math.cos(ha) * 26 + math.cos(ha + math.pi/2 * side) * 16
            h2y = hy - math.sin(ha) * 26 + math.sin(ha + math.pi/2 * side) * 16
            self.canvas.create_polygon(hx, hy, h1x, h1y, h2x, h2y, fill="#FFE600", outline="#00E5FF", tags="leviathan")

        snout_x = hx + math.cos(ha) * 18
        snout_y = hy + math.sin(ha) * 18
        self.canvas.create_polygon(
            snout_x, snout_y,
            hx + math.cos(ha + 1.2) * 9, hy + math.sin(ha + 1.2) * 9,
            hx - math.cos(ha) * 8, hy - math.sin(ha) * 8,
            hx + math.cos(ha - 1.2) * 9, hy + math.sin(ha - 1.2) * 9,
            fill="#00E5FF", outline="#FFFFFF", tags="leviathan"
        )

        # Eyes
        for side in (-1, 1):
            ex = hx + math.cos(ha) * 3 + math.cos(ha + math.pi/2 * side) * 5
            ey = hy + math.sin(ha) * 3 + math.sin(ha + math.pi/2 * side) * 5
            self.canvas.create_oval(ex - 2, ey - 2, ex + 2, ey + 2, fill="#00FFFF", outline="#FFFFFF", tags="leviathan")

        # Whiskers
        for wh in (self.whisker_l, self.whisker_r):
            for i in range(1, len(wh)):
                prev = wh[i - 1]
                curr = wh[i]
                w_thick = max(1, int(3 * (1.0 - i / len(wh))))
                self.canvas.create_line(prev["x"], prev["y"], curr["x"], curr["y"], fill="#00E5FF", width=w_thick, tags="leviathan")

        # Celestial Azimuth Reticle
        self.canvas.create_oval(self.mouse_x - 8, self.mouse_y - 8, self.mouse_x + 8, self.mouse_y + 8, outline="#6C63FF", width=1, tags="leviathan")
        self.canvas.create_oval(self.mouse_x - 3, self.mouse_y - 3, self.mouse_x + 3, self.mouse_y + 3, fill="#00E5FF", outline="#FFFFFF", tags="leviathan")

        self.root.after(16, self.animate)

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = CelestialLeviathanApp(tk_root)
    tk_root.mainloop()

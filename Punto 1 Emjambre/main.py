"""
Drone Light Show — puntos embebidos (no lee imágenes)
- 40 drones, 3 figuras (dragón, robot, estrella)
- Cada figura: 30 contorno + 10 relleno = 40 objetivos
- Espacio 3D (figuras en plano XY con ligera variación Z)
- Cambio automático cada ~15s, reinicio entre figuras
- Colores por figura: robot (light blue), dragón (red), estrella (rainbow)
- Requisitos: numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import math
import random

# -----------------------------
# Config
# -----------------------------
AREA_SIZE = 1000.0
N_DRONES = 40
INTERVAL_MS = 50                      # intervalo de animación -> 20 FPS
SECONDS_PER_PHASE = 15                # cada figura ~15s
FRAMES_PER_PHASE = int(SECONDS_PER_PHASE * 1000 / INTERVAL_MS)
HOLD_FRAMES = int(2 * 1000 / INTERVAL_MS)   # breve hold (2s) después de converger
RESET_FRAMES = int(3 * 1000 / INTERVAL_MS)  # reinicio entre figuras (~3s)
TOTAL_PHASE_FRAMES = FRAMES_PER_PHASE + HOLD_FRAMES
DT = 1.0
MAX_SPEED = 18.0
SAFE_DISTANCE = 10.0
SEED = 42

np.random.seed(SEED)
random.seed(SEED)

# Colors
COLOR_ROBOT = "#7fb3ff"
COLOR_DRAGON = "#ff4d4d"
CMAP_RAINBOW = cm.get_cmap("hsv", N_DRONES)

# -----------------------------
# Utilities: distance matrix
# -----------------------------
def cdist_np(A, B):
    A = np.asarray(A)
    B = np.asarray(B)
    if A.size == 0 or B.size == 0:
        return np.zeros((A.shape[0], B.shape[0]))
    AA = np.sum(A**2, axis=1)[:, None]
    BB = np.sum(B**2, axis=1)[None, :]
    AB = A.dot(B.T)
    D2 = np.maximum(AA + BB - 2*AB, 0.0)
    return np.sqrt(D2)

# Greedy unique assignment (assign each drone a distinct target)
def greedy_unique_assign(positions, targets):
    M = len(positions)
    K = len(targets)
    assigned = -np.ones(M, dtype=int)
    if K == 0:
        return assigned
    D = cdist_np(positions, targets)
    # order drones by nearest-target distance (closer drones pick first)
    order = np.argsort(np.min(D, axis=1))
    free = set(range(K))
    for i in order:
        cand_order = np.argsort(D[i])
        for cand in cand_order:
            if cand in free:
                assigned[i] = cand
                free.remove(cand)
                break
        if assigned[i] == -1:
            # fallback: pick nearest (even if taken)
            assigned[i] = int(cand_order[0])
    return assigned

# -----------------------------
# Figure generators (30 contour + 10 fill)
# -----------------------------
def build_points(contour_pts, n_contour=30, n_fill=10):
    """Given contour points (Nx2), pick n_contour roughly evenly along contour
       and generate n_fill interior points by random barycentric combinations."""
    contour_pts = np.asarray(contour_pts)
    L = len(contour_pts)
    if L == 0:
        raise ValueError("Contour empty")
    # sample contour points evenly
    idxs = np.linspace(0, L-1, n_contour, dtype=int)
    chosen_contour = contour_pts[idxs % L]
    # interior fill: pick random convex combos of 3 random contour points
    fill = []
    for _ in range(n_fill):
        a, b, c = contour_pts[np.random.choice(L, 3, replace=False)]
        r1, r2 = np.random.rand(), np.random.rand()
        # barycentric-like coords, ensure inside triangle
        if r1 + r2 > 1:
            r1, r2 = 1-r1, 1-r2
        p = (1 - r1 - r2) * a + r1 * b + r2 * c
        fill.append(p)
    return np.vstack([chosen_contour, np.array(fill)])  # shape (n_contour+n_fill, 2)

def dragon_points(n_contour=30, n_fill=10, center=(400,500), scale=220):
    cx, cy = center
    t = np.linspace(0, 4*math.pi, 200)
    x = cx + scale * np.sin(t) * np.cos(0.5*t)
    y = cy + scale * np.sin(t) * 0.8 + scale*0.15*np.cos(0.2*t)
    contour = np.vstack([x, y]).T
    pts2d = build_points(contour, n_contour, n_fill)
    # add slight z variation later when mapping to 3D
    return pts2d

def robot_points(n_contour=30, n_fill=10, center=(500,500), scale=180):
    cx, cy = center
    w, h = scale, int(scale*1.1)
    # rectangle perimeter points (evenly sampled)
    perim = []
    # top edge
    for t in np.linspace(-w/2, w/2, 40, endpoint=False):
        perim.append((cx + t, cy + h/2))
    # right edge
    for t in np.linspace(h/2, -h/2, 30, endpoint=False):
        perim.append((cx + w/2, cy + t))
    # bottom
    for t in np.linspace(w/2, -w/2, 40, endpoint=False):
        perim.append((cx + t, cy - h/2))
    # left
    for t in np.linspace(-h/2, h/2, 30, endpoint=False):
        perim.append((cx - w/2, cy + t))
    perim = np.array(perim)
    # add head (a smaller rectangle on top center)
    head_w, head_h = w*0.4, h*0.25
    hx0 = cx - head_w/2
    hy0 = cy + h/2
    head = []
    for t in np.linspace(0, 2*math.pi, 30, endpoint=False):
        head.append((cx + (head_w/2)*math.cos(t), hy0 + (head_h/2)*math.sin(t)))
    contour = np.vstack([perim, head])
    pts2d = build_points(contour, n_contour, n_fill)
    return pts2d

def star_points(n_contour=30, n_fill=10, center=(600,500), scale=200):
    cx, cy = center
    # 5-point star outer/inner
    pts = []
    outer = scale
    inner = scale * 0.43
    for i in range(10):
        ang = 2*math.pi*i/10
        r = outer if i%2==0 else inner
        pts.append((cx + r*math.cos(ang), cy + r*math.sin(ang)))
    contour = np.array(pts)
    pts2d = build_points(contour, n_contour, n_fill)
    return pts2d

# Map 2D plane points to 3D positions (z small variation)
def to_3d_from_2d(pts2d, z_base=250, z_variation=8.0):
    pts3d = np.zeros((pts2d.shape[0], 3))
    pts3d[:,0:2] = pts2d
    pts3d[:,2] = z_base + (np.random.randn(pts2d.shape[0]) * z_variation)
    # clamp Z
    pts3d[:,2] = np.clip(pts3d[:,2], 20.0, AREA_SIZE*0.6)
    return pts3d

# Build the three target sets (40 points each)
DRAGON_2D = dragon_points(n_contour=30, n_fill=10, center=(320, 480), scale=240)
ROBOT_2D  = robot_points(n_contour=30, n_fill=10, center=(500, 480), scale=200)
STAR_2D   = star_points(n_contour=30, n_fill=10, center=(680, 480), scale=200)

DRAGON_TARGETS = to_3d_from_2d(DRAGON_2D, z_base=240, z_variation=6.0)
ROBOT_TARGETS  = to_3d_from_2d(ROBOT_2D,  z_base=230, z_variation=4.0)
STAR_TARGETS   = to_3d_from_2d(STAR_2D,   z_base=260, z_variation=10.0)

# -----------------------------
# Drone swarm class (3D, PSO-like per-target)
# -----------------------------
class DroneSwarm3D:
    def __init__(self, n=N_DRONES):
        self.n = n
        # initialize spread positions (avoid clustering)
        margin = 80
        self.pos = np.random.uniform(margin, AREA_SIZE-margin, (n, 3))
        # set initial z roughly mid altitude
        self.pos[:,2] = np.random.uniform(180, 320, n)
        self.vel = np.random.uniform(-2.0, 2.0, (n, 3))
        self.max_speed = MAX_SPEED

    def assign(self, targets):
        return greedy_unique_assign(self.pos[:,0:2], targets[:,0:2])

    def step(self, targets, assigned, w=0.6, c1=1.2, c2=1.6, rep_k=200.0):
        """
        PSO-like single-step:
        - cognitive term attracts to personal best (we use current pos as pb for simplicity)
        - social term attracts to assigned target (per-drone)
        - repulsion term to avoid collisions
        """
        N = self.n
        # desired positions are the assigned targets (3D)
        desired = np.copy(self.pos)
        for i in range(N):
            a = assigned[i]
            if a != -1:
                desired[i] = targets[a]

        # compute terms
        r1 = np.random.rand(N,1)
        r2 = np.random.rand(N,1)
        # cognitive toward current position (small)
        cognitive = c1 * r1 * (self.pos - self.pos)  # zero (we keep simple)
        social = c2 * r2 * (desired - self.pos)

        # repulsion
        repulsion = np.zeros((N,3))
        for i in range(N):
            dif = self.pos[i] - self.pos
            d = np.linalg.norm(dif, axis=1)
            d[i] = np.inf
            close_mask = d < SAFE_DISTANCE*2.0
            if np.any(close_mask):
                # push away weighted by closeness
                push = np.sum((dif[close_mask] / (d[close_mask][:,None] + 1e-6)), axis=0)
                repulsion[i] = push * rep_k

        # obstacle-free version (no static obstacles here)
        self.vel = w*self.vel + cognitive + social + repulsion * 0.001

        # clip speeds
        speed = np.linalg.norm(self.vel,axis=1)
        too = speed > self.max_speed
        if np.any(too):
            self.vel[too] = (self.vel[too].T * (self.max_speed / speed[too])).T

        # update positions
        self.pos += self.vel * DT
        # clamp positions into area
        self.pos[:,0] = np.clip(self.pos[:,0], 0, AREA_SIZE)
        self.pos[:,1] = np.clip(self.pos[:,1], 0, AREA_SIZE)
        self.pos[:,2] = np.clip(self.pos[:,2], 20.0, AREA_SIZE*0.6)

# -----------------------------
# Base positions for reset (circle near bottom center)
# -----------------------------
def compute_base_positions(n):
    angle = np.linspace(0, 2*math.pi, n, endpoint=False)
    center = np.array([AREA_SIZE*0.5, AREA_SIZE*0.1, 120.0])
    radius = 100.0
    pts = np.zeros((n,3))
    pts[:,0] = center[0] + radius * np.cos(angle)
    pts[:,1] = center[1] + radius * np.sin(angle)
    pts[:,2] = center[2]
    return pts

BASE_POSITIONS = compute_base_positions(N_DRONES)

# -----------------------------
# Animation & Phase control
# -----------------------------
def run_animation():
    swarm = DroneSwarm3D(N_DRONES)

    phases = [
        ("Robot", ROBOT_TARGETS, COLOR_ROBOT),
        ("Reset", BASE_POSITIONS, "#aaaaaa"),
        ("Dragon", DRAGON_TARGETS, COLOR_DRAGON),
        ("Reset", BASE_POSITIONS, "#aaaaaa"),
        ("Star", STAR_TARGETS, None),   # None => rainbow
        ("Reset", BASE_POSITIONS, "#aaaaaa"),
    ]
    # frames per phase: for target phases we use FRAMES_PER_PHASE + HOLD_FRAMES; reset phases use RESET_FRAMES
    # We'll iterate phases cyclically
    # Prepare plot
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('k')
    ax.xaxis.set_pane_color((0,0,0,1))
    ax.yaxis.set_pane_color((0,0,0,1))
    ax.zaxis.set_pane_color((0,0,0,1))
    ax.set_xlim(0, AREA_SIZE); ax.set_ylim(0, AREA_SIZE); ax.set_zlim(0, AREA_SIZE*0.6)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    title = ax.set_title("", color='w')

    # initial scatter
    xs = swarm.pos[:,0]; ys = swarm.pos[:,1]; zs = swarm.pos[:,2]
    scat = ax.scatter(xs, ys, zs, s=48, edgecolors='k', linewidth=0.3)
    targ_scat = ax.scatter([],[],[], s=70, c='yellow', marker='x', alpha=0.7)

    # phase state
    phase_idx = 0
    frame_in_phase = 0
    # compute frame counts for phases
    def phase_frame_count(name):
        if name == "Reset":
            return RESET_FRAMES
        else:
            return FRAMES_PER_PHASE + HOLD_FRAMES

    # initialize assigned targets
    current_targets = phases[phase_idx][1]
    current_color = phases[phase_idx][2]
    assigned = swarm.assign(current_targets)

    # helper to get drone colors
    def colors_for_phase(color_flag):
        if color_flag is None:
            # rainbow
            cols = CMAP_RAINBOW(np.arange(N_DRONES))[:,:3]
            return cols
        else:
            return np.array([color_flag]*N_DRONES)

    drone_colors = colors_for_phase(current_color)
    scat.set_color(drone_colors)

    # update function
    def update(frame):
        nonlocal phase_idx, frame_in_phase, current_targets, current_color, assigned, drone_colors
        phase_name, targets, color_flag = phases[phase_idx]
        total_frames = phase_frame_count(phase_name)

        # On first frame of phase, recompute assignments
        if frame_in_phase == 0:
            assigned = swarm.assign(targets)
            drone_colors = colors_for_phase(color_flag)
            scat.set_color(drone_colors)
            targ_scat._offsets3d = (targets[:,0], targets[:,1], targets[:,2])

        # swarm moves toward targets (only during target and reset frames)
        if phase_name == "Reset":
            # reset: we want them to move to base quickly; use fewer PSO frames but stronger alpha (handled by step)
            swarm.step(targets, assigned)
        else:
            # normal target convergence
            swarm.step(targets, assigned)

        # update scatter points
        pos = swarm.pos
        scat._offsets3d = (pos[:,0], pos[:,1], pos[:,2])
        title.set_text(f"Phase: {phase_name} ({phase_idx+1}/{len(phases)}) Frame {frame_in_phase+1}/{total_frames}")

        frame_in_phase += 1
        if frame_in_phase >= total_frames:
            # advance to next phase
            phase_idx = (phase_idx + 1) % len(phases)
            frame_in_phase = 0

        return scat, targ_scat, title

    ani = animation.FuncAnimation(fig, update, interval=INTERVAL_MS, blit=False)
    plt.show()

if __name__ == "__main__":
    run_animation()

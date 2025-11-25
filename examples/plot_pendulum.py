#!/usr/bin/env python3
"""
Visualization script for double pendulum motion.
Plots trajectories and animates the pendulum.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import L1, L2

# Time array
t = np.linspace(0, 10, 500)

# Generate time-dependent angles (example: sine waves)
theta1 = 0.5 * np.sin(0.5 * t)
theta2 = 0.3 * np.sin(1.0 * t + np.pi/4)

# Compute positions of P1 and P2
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)

x2 = x1 + L2 * np.sin(theta1 + theta2)
y2 = y1 - L2 * np.cos(theta1 + theta2)

# -------------------------------------------------------------------
# 1) Trajectory Plot
# -------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot P1 trajectory
ax1.plot(x1, y1, 'b-', linewidth=1, alpha=0.7, label='P1 trajectory')
ax1.scatter(x1[0], y1[0], c='green', s=100, marker='o', label='Start', zorder=5)
ax1.scatter(x1[-1], y1[-1], c='red', s=100, marker='x', label='End', zorder=5)
ax1.set_xlabel('x (m)')
ax1.set_ylabel('y (m)')
ax1.set_title('Link 1 Endpoint (P1) Trajectory')
ax1.grid(True, alpha=0.3)
ax1.axis('equal')
ax1.legend()

# Plot P2 trajectory
ax2.plot(x2, y2, 'r-', linewidth=1, alpha=0.7, label='P2 trajectory')
ax2.scatter(x2[0], y2[0], c='green', s=100, marker='o', label='Start', zorder=5)
ax2.scatter(x2[-1], y2[-1], c='red', s=100, marker='x', label='End', zorder=5)
ax2.set_xlabel('x (m)')
ax2.set_ylabel('y (m)')
ax2.set_title('Link 2 Endpoint (P2) Trajectory')
ax2.grid(True, alpha=0.3)
ax2.axis('equal')
ax2.legend()

plt.tight_layout()
plt.savefig('examples/trajectories.png', dpi=150)
print("Trajectory plot saved to examples/trajectories.png")

# -------------------------------------------------------------------
# 2) Animation
# -------------------------------------------------------------------
fig_anim = plt.figure(figsize=(8, 8))
ax_anim = fig_anim.add_subplot(111)
ax_anim.set_xlim(-2.5, 2.5)
ax_anim.set_ylim(-2.5, 0.5)
ax_anim.set_xlabel('x (m)')
ax_anim.set_ylabel('y (m)')
ax_anim.set_title('Double Pendulum Animation')
ax_anim.grid(True, alpha=0.3)
ax_anim.axis('equal')

# Initialize plot elements
line, = ax_anim.plot([], [], 'o-', lw=3, markersize=10, color='navy', label='Links')
trace1, = ax_anim.plot([], [], 'b-', lw=0.5, alpha=0.3, label='P1 trace')
trace2, = ax_anim.plot([], [], 'r-', lw=0.5, alpha=0.3, label='P2 trace')
time_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes, fontsize=12)
ax_anim.legend(loc='upper right')

# Trace history
trace1_x, trace1_y = [], []
trace2_x, trace2_y = [], []

def init():
    """Initialize animation."""
    line.set_data([], [])
    trace1.set_data([], [])
    trace2.set_data([], [])
    time_text.set_text('')
    return line, trace1, trace2, time_text

def animate(i):
    """Update animation frame."""
    # Current positions
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    
    line.set_data(thisx, thisy)
    
    # Update traces
    trace1_x.append(x1[i])
    trace1_y.append(y1[i])
    trace2_x.append(x2[i])
    trace2_y.append(y2[i])
    
    # Keep only recent trace (last 100 points)
    if len(trace1_x) > 100:
        trace1_x.pop(0)
        trace1_y.pop(0)
        trace2_x.pop(0)
        trace2_y.pop(0)
    
    trace1.set_data(trace1_x, trace1_y)
    trace2.set_data(trace2_x, trace2_y)
    
    time_text.set_text(f'Time: {t[i]:.2f} s')
    
    return line, trace1, trace2, time_text

# Create animation
anim = FuncAnimation(fig_anim, animate, init_func=init,
                     frames=len(t), interval=20, blit=True, repeat=True)

# Save animation
anim.save('examples/pendulum_animation.gif', writer='pillow', fps=30, dpi=100)
print("Animation saved to examples/pendulum_animation.gif")

plt.show()

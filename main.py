# main.py

from sympy import symbols
from sympy.physics.mechanics import dynamicsymbols
from pendulum.model import create_frames
from pendulum.kinematics import compute_angular_velocities, compute_point_kinematics
from pendulum.energy import compute_kinetic_energy
from pendulum.numeric import lambdify_expr
import config as cfg

# -------------------------------------------------------------------
# 1) Symbols and frames
# -------------------------------------------------------------------
t = symbols('t') # t is a symbol that represents time.
theta1, theta2 = dynamicsymbols('theta1 theta2') # theta1 and theta2 are symbols that represent the angles of the pendulum.

# time-derivatives
theta1d  = theta1.diff(t) # theta1dot is the time-derivative of theta1.
theta2d  = theta2.diff(t) # theta2dot is the time-derivative of theta2.
theta1dd = theta1d.diff(t) # theta1ddot is the second time-derivative of theta1.
theta2dd = theta2d.diff(t) # theta2ddot is the second time-derivative of theta2.

# physical parameter (constant, not dynamicsymbol)
L1, L2 = symbols('L1 L2') # L1 and L2 are symbols that represent the lengths of the pendulum.
m1, m2 = symbols('m1 m2') # m1 and m2 are symbols that represent the masses of the pendulum.

N, A, B = create_frames()

# -------------------------------------------------------------------
# 2) Angular velocities (frame.ang_vel_in)
# -------------------------------------------------------------------
wA_N, wB_N = compute_angular_velocities(N, A, B) # wA_N and wB_N are the angular velocities of frames A and B in the inertial frame N.

# Substitute derivatives -> plain symbols
u1, u2 = symbols('u1 u2')     # theta1dot, theta2dot
subs_vel = {theta1d: u1, theta2d: u2} # dictionary for substitution

wA_N_sub = wA_N.subs(subs_vel) # substitute derivatives
wB_N_sub = wB_N.subs(subs_vel) # substitute derivatives

# Lambdify angular velocity of A in N
f_wA = lambdify_expr(wA_N_sub.to_matrix(N), [u1, u2]) # convert to numpy function
f_wB = lambdify_expr(wB_N_sub.to_matrix(N), [u1, u2]) # convert to numpy function

print("Angular velocity of frame A in N:")
print(f_wA(1.0, 2.0))  # example: u1=1 rad/s, u2=2 rad/s

print("\nAngular velocity of frame B in N:")
print(f_wB(1.0, 2.0))

# -------------------------------------------------------------------
# 3) Point kinematics (Point.vel, Point.acc)
# -------------------------------------------------------------------
velP1, velP2, accP1, accP2 = compute_point_kinematics(N, A, B, L1, L2) # velP1/P2 and accP1/P2 are velocities and accelerations in N

# -------------------------------------------------------------------
# 4) Kinetic Energy
# -------------------------------------------------------------------
KE = compute_kinetic_energy(m1, m2, velP1, velP2)

# Substitute derivatives -> plain symbols
a1, a2 = symbols('a1 a2')     # theta1ddot, theta2ddot
subs_acc = {
    theta1d: u1,
    theta2d: u2,
    theta1dd: a1,
    theta2dd: a2
}

velP1_sub = velP1.subs(subs_vel)
velP2_sub = velP2.subs(subs_vel)
accP1_sub = accP1.subs(subs_acc) # substitute derivatives
accP2_sub = accP2.subs(subs_acc) # substitute derivatives
KE_sub = KE.subs(subs_vel)

# Lambdify velocity
f_velP1 = lambdify_expr(velP1_sub.to_matrix(N), [L1, theta1, u1, u2])
f_velP2 = lambdify_expr(velP2_sub.to_matrix(N), [L1, L2, theta1, theta2, u1, u2])

# Lambdify acceleration
f_accP1 = lambdify_expr(accP1_sub.to_matrix(N), [L1, theta1, theta2, u1, u2, a1, a2]) # convert to numpy function
f_accP2 = lambdify_expr(accP2_sub.to_matrix(N), [L1, L2, theta1, theta2, u1, u2, a1, a2]) # convert to numpy function

# Lambdify kinetic energy
f_KE = lambdify_expr(KE_sub, [m1, m2, L1, L2, theta1, theta2, u1, u2])

print("\nVelocity of point P1 (end of link 1) in N:")
print(f_velP1(cfg.L1, 0.5, 1.0, 2.0))

print("\nVelocity of point P2 (end of link 2) in N:")
print(f_velP2(cfg.L1, cfg.L2, 0.5, 0.3, 1.0, 2.0))

print("\nAcceleration of point P1 (end of link 1) in N:")
print(f_accP1(cfg.L1, 0.5, 0.3, 1.0, 2.0, 0.2, 0.1)) #testing it with values: L1=1, theta1=0.5 rad, theta2=0.3 rad, u1=1 rad/s, u2=2 rad/s, a1=0.2 rad/s^2, a2=0.1 rad/s^2

print("\nAcceleration of point P2 (end of link 2) in N:")
print(f_accP2(cfg.L1, cfg.L2, 0.5, 0.3, 1.0, 2.0, 0.2, 0.1)) #testing it with values: L1=1, L2=1, theta1=0.5 rad, theta2=0.3 rad, u1=1 rad/s, u2=2 rad/s, a1=0.2 rad/s^2, a2=0.1 rad/s^2

print("\nTotal Kinetic Energy:")
print(f_KE(cfg.m1, cfg.m2, cfg.L1, cfg.L2, 0.5, 0.3, 1.0, 2.0))
  
# -------------------------------------------------------------------
# Some test Values for Acceleration of point

#Test Case 1: Both links at rest
# f_accP1(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
# f_accP2(1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# Test Case 2: Fast rotation of second link
# f_accP1(1.0, 0.5, 0.5, 1.0, 0.0, 0.1, 0.0)
# f_accP2(1.0, 1.0, 0.5, 0.5, 1.0, 4.0, 0.1, 0.3)

# Test Case 3: Reverse rotation
# f_accP1(1.5, 0.5, 0.3, 1.0, -1.0, 0.2, -0.2)
# f_accP2(1.5, 1.5, 0.5, 0.3, 1.0, -1.0, 0.2, -0.2)

# Test Case 4: Larger links
# f_accP1(2.0, 0.5, 0.3, 1.5, 2.0, 0.3, 0.2)
# f_accP2(2.0, 2.0, 0.5, 0.3, 1.5, 2.0, 0.3, 0.2)

# -------------------------------------------------------------------
 

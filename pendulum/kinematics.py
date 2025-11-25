# pendulum/kinematics.py

from sympy import Symbol
from sympy.physics.mechanics import Point

def compute_angular_velocities(N, A, B):
    """
    Angular velocities using frame.ang_vel_in()
    """
    wA_N = A.ang_vel_in(N)   # angular velocity of A in N
    wB_N = B.ang_vel_in(N)   # angular velocity of B in N
    return wA_N, wB_N


def compute_point_kinematics(N, A, B, L1, L2):
    """
    Linear kinematics (velocity and acceleration) using Point.vel() and Point.acc()
    """
    # Origin
    O = Point('O')
    O.set_vel(N, 0)

    # Point at the end of link 1
    P1 = O.locatenew('P1', L1 * A.x)
    P1.v2pt_theory(O, N, A)

    # Point at the end of link 2
    P2 = P1.locatenew('P2', L2 * B.x)
    P2.v2pt_theory(P1, N, B)

    return P1.vel(N), P2.vel(N), P1.acc(N), P2.acc(N)

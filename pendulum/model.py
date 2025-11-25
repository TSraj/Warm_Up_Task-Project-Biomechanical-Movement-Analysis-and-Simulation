# pendulum/model.py

from sympy.physics.mechanics import ReferenceFrame, dynamicsymbols

def create_frames():
    N = ReferenceFrame('N')  # inertial frame. N The world frame

    theta1, theta2 = dynamicsymbols('theta1 theta2')

    # the frames for the pendulum links

    A = N.orientnew('A', 'Axis', [theta1, N.z])  # link 1 frame. the first link, rotated by angle θ₁
    B = A.orientnew('B', 'Axis', [theta2, A.z])  # link 2 frame. the second link, rotated by angle θ₂

    return N, A, B
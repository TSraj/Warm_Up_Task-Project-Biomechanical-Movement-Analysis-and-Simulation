from sympy.physics.mechanics import dot

def compute_kinetic_energy(m1, m2, vP1, vP2):
    """
    Compute the total kinetic energy of the system.
    KE = 0.5 * m * v^2
    """
    KE1 = 0.5 * m1 * dot(vP1, vP1)
    KE2 = 0.5 * m2 * dot(vP2, vP2)
    
    return KE1 + KE2

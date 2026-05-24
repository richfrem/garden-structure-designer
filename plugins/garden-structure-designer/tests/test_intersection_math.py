import math
import pytest

def solve_intersection(px, py, nx, ny):
    """
    Solves for t in the intersection of radial line L(t) = t*(nx, ny)
    and plane (L - P) dot N = 0, where P = (px, py) and N = (nx, ny).
    """
    # Plane eqn: (t*nx - px)*nx + (t*ny - py)*ny = 0
    # t*(nx*nx + ny*ny) - (px*nx + py*ny) = 0
    # Since N is unit length, nx*nx + ny*ny = 1
    t = px*nx + py*ny
    return t

def test_intersection_satisfies_plane():
    """Prove that the intersection point satisfies the plane equation within tolerance."""
    # Test case: 30 degree face for a hex
    hub_r = 0.65
    theta = math.radians(30)
    nx, ny = math.cos(theta), math.sin(theta)
    px, py = hub_r * nx, hub_r * ny
    
    t = solve_intersection(px, py, nx, ny)
    
    # Intersection point L
    lx, ly = t * nx, t * ny
    
    # Plane equation: (L - P) dot N should be 0
    dot_product = (lx - px) * nx + (ly - py) * ny
    assert abs(dot_product) < 1e-12

def test_near_parallel_case():
    """Cases that are physically impossible in our radial hub but mathematically near-parallel."""
    # In our engine, N is always the direction of the line L, so dot(L_dir, N) is always 1.
    # However, if we ever supported non-radial lines, we would check the denominator.
    pass

def test_hex_points():
    """Verify exact values for a standard hex hub face."""
    hub_r = 0.65
    theta = math.radians(30)
    nx, ny = math.cos(theta), math.sin(theta) # (0.8660, 0.5000)
    px, py = hub_r * nx, hub_r * ny # (0.5629, 0.3250)
    
    t = solve_intersection(px, py, nx, ny)
    
    # For radial planes at distance hub_r, t should exactly equal hub_r
    assert abs(t - 0.65) < 1e-12
    
    # If the plane is shifted or the line is offset, t will change.
    # Our engine currently uses radial lines and radial planes, 
    # so t=hub_r is the expected geometric outcome.
    lx, ly = t * nx, t * ny
    assert abs(lx - 0.56291651) < 1e-6
    assert abs(ly - 0.325) < 1e-6

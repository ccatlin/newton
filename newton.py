"""
This is a little module to create Newton polynomials, interpolation polynomials 
in the Newton basis, from a set of supplied funcational points. For more info,
please see:
http://wikipedia.org/wiki/Newton_polynomial 
http://wikipedia.org/wiki/Divided_differences
Note: Use at your own risk.
"""

def div_diff_function(known_points):
    """Create a forward divided difference function from a set of points.
    Inputs: known_points - [(x0,y0),(x1,y1),...,(xn,yn)], a table of known 
                           function points, where each x value is unique.
    Returns: A function from (x0, x1, ..., xj) tuples to real numbers, e.g. 
             f(x1,x2,x3) = f(x2,x3) - f(x1,x2) /
                                x3  - x1       
    """
    f_cache = {(xi,):yi for xi,yi in sorted(known_points)}
    
    def f(xs):
        """Divided difference function, a linear approximation of the i-j 
        derivative from (xi,f(xi)) to (xi+j,f(xi+j)).
        Inputs: xs - tuple of (xi, xi+1, ..., xi+j) sequential, known x values. 
        Returns: a real value represnting the forward divided difference."""
        xi_tuple = tuple(sorted(xs))
        if xi_tuple not in f_cache:
            f_cache[xi_tuple] = (f(xi_tuple[1:]) - f(xi_tuple[:-1])) /  \
                             float(xi_tuple[-1]  -   xi_tuple[0])
        return f_cache[xi_tuple]
    
    return f

def interpolation_polynomial(known_points, get_string=False):
    """Create an interpolation polynomial of upto n degree passing through all 
    of the supplied n+1 points.
    Inputs: known_points - a table of known points on your function supplied 
                        as a list of (x,y) tuples, where each x value is unique.
            get_string - flag to get the poynomial's string representation.
    Returns: p - an approximation polynomial for your function.
             p_string - a string representation of newton basis polynomial.
    """
    x_knots = sorted(point[0] for point in known_points)
    n = len(x_knots) - 1
    div_diffs = div_diff_function(known_points)
    
    # coefficients - f(x0), f(x0,x1), ..., f(x0,x1,...,xn+1):
    coeffs = [div_diffs(x_knots[:i+1]) for i in range(len(x_knots))]
    
    # polynomial:
    def p(x):
        """Interpolation polynomial p(x) = c0 + c1(x - x0) + c2(x - x0)(x - x1) + ...
        Inputs: x - real value x in [x0,xn]
        Returns: real valued approximation"""
        total = coeffs[0]  # coeffs[0] = div_diff(x0) = y0
        basis = 1
        for i in range(n): 
            basis = basis * (x - x_knots[i])
            total = total + coeffs[i+1] * basis
        return total
    
    return (p, _str_newton_poly(coeffs, x_knots)) if get_string else p

def _str_newton_poly(coeffs, x_knots):
    """Create a string representation of the polynomial with the supplied
    coefficients and a newton basis based on the x_knots.  
    'p(x) = c0 + c1(x - x0) + c2(x - x0)(x - x1) + ...'
    Inputs: coeffs - ordered coefficients
            x_knots - sequential xi values used in the newton basis
    Returns: a string representation of newton basis polynomial.
    """
    basis, poly_string = '', str(coeffs[0])
    for ci,xi in zip(coeffs[1:], x_knots[:-1]):
        # basis (x - x0)(x - x1)...(x - xi)
        if xi < 0:
            basis += '(x + ' + str(-xi) + ')'
        elif xi == 0:
            basis += 'x'
        else:
            basis += '(x - ' + str(xi) + ')'
        
        # append the ith's term, e.g. ci(x-x0)(x-x1)...(x-xi)
        add = ' + ' if ci >= 0 else ' - '
        if ci == 0:
            next
        elif abs(ci) == 1: 
            poly_string += add + basis
        else:
            poly_string += add + str(abs(ci)) + basis
    return 'p(x) = ' + poly_string


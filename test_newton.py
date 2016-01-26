import unittest
import newton
import math

class NewtonTestCase(unittest.TestCase):
    def test_zero_degree_polynomial(self):
        """Are zero degree (constant) polynomials handled correctly?"""
        # f(x) = 2
        p, p_str = newton.interpolation_polynomial([(0,2)], get_string=True)
        self.assertEqual(p(-3.14), 2)
        self.assertEqual(p_str, 'p(x) = 2')
    
    def test_known_points_equal_themselves(self):
        # f(x) = 2x
        x_knots = range(1,5)
        p = newton.interpolation_polynomial([(x,2*x) for x in x_knots])
        for x in x_knots:
            self.assertEqual(p(x), 2*x)
    
    def test_polynomial_interpolates_to_itself(self):
        def f(x): return 4*x**3 + 2*x + 1
        x_knots = [x for x in range(-2,2)]
        p = newton.interpolation_polynomial([(x,f(x)) for x in x_knots])
        self.assertEqual(p(0.5), f(0.5))
    
    def test_str_newton_poly(self):
        exp_str = 'p(x) = -1 + 2(x + 3) - 4(x + 3)(x - 5)x'
        p_str = newton._str_newton_poly([-1,2,0,-4], [-3,5,0,100])
        self.assertEqual(exp_str, p_str)
    
    def test_divided_differences(self):
        #    f       | div diff
        # x0 = 1  0  |
        #            |  2
        # x1 = 2  2  |     1
        #            |  5     0
        # x2 = 4  12 |     1
        #            |  8
        # x3 = 5  20 |
        known_points = [(1,0), (2,2), (4,12), (5,20)]
        div_diff = newton.div_diff_function(known_points)
        self.assertEqual(div_diff((4,)), 12)
        self.assertEqual(div_diff((4,5)), 8)
        self.assertEqual(div_diff((1,2,4,5)), 0)

if __name__ == '__main__':
    unittest.main()


# newton
This is a little module to create [Newton (interpolation) polynomials](https://en.wikipedia.org/wiki/Newton_polynomial) from a set of supplied funcation points (e.g. (-2,4), (-1,1), (0,0), (1,1), (2,4)). It is useful for calculating intermediate values in unknown or computationally expensive functions.

There is no guarantee of correctness. Please use at your own risk.

# Functions
* *interpolation_polynomial* - creates a Newton polynomial based on the supplied points.
  * For a set of n+1 points, the approximation polynomial will have degree up to n.
  * If called with get_string=True, also returns a string represnetation of the polynomial.
* *div_diff_function* - creates a [divided difference function](https://en.wikipedia.org/wiki/Divided_differences) based on the supplied points. 

# Examples:
Approximate f(x) = 1/(x^2 + 1).
```
import newton

known_points = [(-2, 0.2), (-1, 0.5), (0, 1.0), (1, 0.5), (2, 0.2)]
p, p_string = newton.interpolation_polynomial(known_points, get_string=True)
p_string  # 'p(x) = 0.2 + 0.3(x + 2) + 0.1(x + 2)(x + 1) - 0.2(x + 2)(x + 1)x + 0.1(x + 2)(x + 1)x(x - 1)'
p(0.75)   # 0.694140625 (vs 0.64)
```
Divided differences for:
```
# (xi, yi) | div diff
# (1,  0)  |
#          |  2
# (2,  2)  |     1
#          |  5     0
# (4,  12) |     1
#          |  8
# (5,  20) |

g = newton.div_diff_function([(1,0), (2,2), (4,12), (5,20)])
g[(4,)]      # 12
g[(4,5)]     # 8
g[(1,2,4,5)] # 0
```


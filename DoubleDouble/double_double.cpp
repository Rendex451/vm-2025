#ifndef DOUBLEDOUBLE_H
#define DOUBLEDOUBLE_H

#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cfloat>
#include <cstdint>
#include <array>
#include <vector>
#include <string>

namespace doubledouble {

class DoubleDouble
{
public:

    double upper{0.0};
    double lower{0.0};

    constexpr
    DoubleDouble() {}

    constexpr
    DoubleDouble(double x, double y)
    {
        if (std::isnan(x) || std::isnan(y)) {
            upper = NAN;
            lower = NAN;
            return;
        }
        bool xinf = std::isinf(x);
        bool yinf = std::isinf(y);
        if (xinf && yinf) {
            if (x != y) {
                upper = NAN;
                lower = NAN;
            }
            else {
                upper = x;
                lower = 0.0;
            }
        }
        else if (xinf) {
            upper = x;
            lower = 0.0;
        }
        else if (yinf) {
            upper = y;
            lower = 0.0;
        }
        else {
            
            
            double r = x + y;
            double t = r - x;
            double e = (x - (r - t)) + (y - t);
            upper = r;
            lower = e;
        }
    }

    constexpr
    DoubleDouble(double upper) : upper(upper)
    {
        if (std::isnan(upper)) {
            lower = NAN;
        }
    }
    DoubleDouble operator-() const;
    DoubleDouble operator+(double x) const;
    DoubleDouble operator+(const DoubleDouble& x) const;
    DoubleDouble operator-(double x) const;
    DoubleDouble operator-(const DoubleDouble& x) const;
    DoubleDouble operator*(double x) const;
    DoubleDouble operator*(const DoubleDouble& x) const;
    DoubleDouble operator/(double x) const;
    DoubleDouble operator/(const DoubleDouble& x) const;

    DoubleDouble& operator+=(double x);
    DoubleDouble& operator+=(const DoubleDouble& x);
    DoubleDouble& operator-=(double x);
    DoubleDouble& operator-=(const DoubleDouble& x);
    DoubleDouble& operator*=(double x);
    DoubleDouble& operator*=(const DoubleDouble& x);
    DoubleDouble& operator/=(double x);
    DoubleDouble& operator/=(const DoubleDouble& x);

    bool operator==(const DoubleDouble& x) const;
    bool operator==(double x) const;
    bool operator!=(const DoubleDouble& x) const;
    bool operator!=(double x) const;
    bool operator<(double x) const;
    bool operator<(const DoubleDouble& x) const;
    bool operator<=(double x) const;
    bool operator<=(const DoubleDouble& x) const;
    bool operator>(double x) const;
    bool operator>(const DoubleDouble& x) const;
    bool operator>=(double x) const;
    bool operator>=(const DoubleDouble& x) const;
    DoubleDouble sqrt() const;
    DoubleDouble custom_sqrt() const;

};

inline const DoubleDouble dd_sqrt2{1.4142135623730951, -9.667293313452913e-17};
inline const DoubleDouble dd_sqrt1_2{0.7071067811865476, -4.833646656726457e-17};
inline const DoubleDouble dd_e{2.7182818284590452, 1.44564689172925013472e-16};
inline const DoubleDouble dd_ln2{0.6931471805599453, 2.3190468138462996e-17};
inline const DoubleDouble dd_pi{3.1415926535897932, 1.22464679914735317636e-16};
inline const DoubleDouble dd_pi_2{1.5707963267948966, 6.123233995736766e-17};
inline const DoubleDouble dd_1_pi{0.3183098861837907, -1.9678676675182486e-17};
inline const DoubleDouble dd_1_sqrtpi{0.5641895835477563,7.66772980658294e-18};
inline const DoubleDouble dd_2_sqrtpi{1.1283791670955126, 1.533545961316588e-17};
inline const DoubleDouble dd_sqrt_pi_2{1.2533141373155003, -9.164289990229583e-17};
inline const DoubleDouble dd_sqrt_2_pi{0.7978845608028654, -4.98465440455546e-17};
inline DoubleDouble two_sum_quick(double x, double y)
{
    double r = x + y;
    double e = y - (r - x);
    return DoubleDouble(r, e);
}


inline DoubleDouble two_sum(double x, double y)
{
    double r = x + y;
    double t = r - x;
    double e = (x - (r - t)) + (y - t);
    return DoubleDouble(r, e);
}


inline DoubleDouble two_difference(double x, double y)
{
    double r = x - y;
    double t = r - x;
    double e = (x - (r - t)) - (y + t);
    return DoubleDouble(r, e);
}


inline DoubleDouble two_product(double x, double y)
{
    double r = x*y;
    double e = fma(x, y, -r);
    return DoubleDouble(r, e);
}


inline DoubleDouble DoubleDouble::operator-() const
{
    return DoubleDouble(-upper, -lower);
}

inline DoubleDouble DoubleDouble::operator+(double x) const
{
    DoubleDouble re = two_sum(upper, x);
    re.lower += lower;
    return two_sum_quick(re.upper, re.lower);
}

inline DoubleDouble operator+(double x, const DoubleDouble& y)
{
    return y + x;
}

inline DoubleDouble DoubleDouble::operator+(const DoubleDouble& x) const
{
    DoubleDouble re = two_sum(upper, x.upper);
    re.lower += lower + x.lower;
    return two_sum_quick(re.upper, re.lower);
}

inline DoubleDouble DoubleDouble::operator-(double x) const
{
    DoubleDouble re = two_difference(upper, x);
    re.lower += lower;
    return two_sum_quick(re.upper, re.lower);
}

inline DoubleDouble operator-(double x, const DoubleDouble& y)
{
    return -y + x;
}

inline DoubleDouble DoubleDouble::operator-(const DoubleDouble& x) const
{
    DoubleDouble re = two_difference(upper, x.upper);
    re.lower += lower - x.lower;
    return two_sum_quick(re.upper, re.lower);
}

inline DoubleDouble DoubleDouble::operator*(double x) const
{
    DoubleDouble re = two_product(upper, x);
    re.lower += lower * x;
    return two_sum_quick(re.upper, re.lower);
}

inline DoubleDouble operator*(double x, const DoubleDouble& y)
{
    return y * x;
}

inline DoubleDouble DoubleDouble::operator*(const DoubleDouble& x) const
{
    DoubleDouble re = two_product(upper, x.upper);
    re.lower += upper*x.lower + lower*x.upper;
    return two_sum_quick(re.upper, re.lower);
}

inline DoubleDouble DoubleDouble::operator/(double x) const
{
    double r = upper/x;
    DoubleDouble sf = two_product(r, x);
    double e = (upper - sf.upper - sf.lower + lower)/x;
    return two_sum_quick(r, e);
}

inline DoubleDouble operator/(double x, const DoubleDouble& y)
{
    return DoubleDouble(x, 0.0) / y;
}

inline DoubleDouble DoubleDouble::operator/(const DoubleDouble& x) const
{
    double r = upper/x.upper;
    DoubleDouble sf = two_product(r, x.upper);
    double e = (upper - sf.upper - sf.lower + lower - r*x.lower)/x.upper;
    return two_sum_quick(r, e);
}

inline DoubleDouble& DoubleDouble::operator+=(double x)
{
    DoubleDouble re = two_sum(upper, x);
    re.lower += lower;
    *this = two_sum_quick(re.upper, re.lower);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator+=(const DoubleDouble& x)
{
    DoubleDouble re = two_sum(upper, x.upper);
    re.lower += lower + x.lower;
    *this = two_sum_quick(re.upper, re.lower);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator-=(double x)
{
    DoubleDouble re = two_difference(upper, x);
    re.lower += lower;
    *this = two_sum_quick(re.upper, re.lower);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator-=(const DoubleDouble& x)
{
    DoubleDouble re = two_difference(upper, x.upper);
    re.lower += lower - x.lower;
    *this = two_sum_quick(re.upper, re.lower);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator*=(double x)
{
    DoubleDouble re = two_product(upper, x);
    re.lower += lower * x;
    *this = two_sum_quick(re.upper, re.lower);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator*=(const DoubleDouble& x)
{
    DoubleDouble re = two_product(upper, x.upper);
    re.lower += upper*x.lower + lower*x.upper;
    *this = two_sum_quick(re.upper, re.lower);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator/=(double x)
{
    double r = upper/x;
    DoubleDouble sf = two_product(r, x);
    double e = (upper - sf.upper - sf.lower + lower)/x;
    *this = two_sum_quick(r, e);
    return *this;
}

inline DoubleDouble& DoubleDouble::operator/=(const DoubleDouble& x)
{
    double r = upper/x.upper;
    DoubleDouble sf = two_product(r, x.upper);
    double e = (upper - sf.upper - sf.lower + lower - r*x.lower)/x.upper;
    *this = two_sum_quick(r, e);
    return *this;
}

inline bool DoubleDouble::operator==(const DoubleDouble& x) const
{
    return (upper == x.upper) && (lower == x.lower);
}

inline bool DoubleDouble::operator==(double x) const
{
    return (upper == x) && (lower == 0.0);
}

inline bool operator==(double x, const DoubleDouble& y)
{
    return y == x;
}

inline bool DoubleDouble::operator!=(const DoubleDouble& x) const
{
    return (upper != x.upper) || (lower != x.lower);
}

inline bool DoubleDouble::operator!=(double x) const
{
    return (upper != x) || (lower != 0.0);
}

inline bool operator!=(double x, const DoubleDouble& y)
{
    return y != x;
}

inline bool DoubleDouble::operator<(const DoubleDouble& x) const
{
    return (upper < x.upper) || ((upper == x.upper) && (lower < x.lower));
}

inline bool DoubleDouble::operator<(double x) const
{

    return (upper < x) || ((upper == x) && (lower < 0.0));
}

inline bool operator<(double x, const DoubleDouble& y)
{
    return y >= x;
}

inline bool DoubleDouble::operator<=(const DoubleDouble& x) const
{
    return (upper < x.upper) || ((upper == x.upper) && (lower <= x.lower));
}

inline bool DoubleDouble::operator<=(double x) const
{
    return (upper < x) || ((upper == x) && (lower <= 0.0));
}

inline bool operator<=(double x, const DoubleDouble& y)
{
    return y >= x;
}

inline bool DoubleDouble::operator>(const DoubleDouble& x) const
{
    return (upper > x.upper) || ((upper == x.upper) && (lower > x.lower));
}

inline bool DoubleDouble::operator>(double x) const
{
    return (upper > x) || ((upper == x) && (lower > 0.0));
}

inline bool operator>(double x, const DoubleDouble& y)
{
    return y <= x;
}

inline bool DoubleDouble::operator>=(const DoubleDouble& x) const
{
    return (upper > x.upper) || ((upper == x.upper) && (lower >= x.lower));
}

inline bool DoubleDouble::operator>=(double x) const
{
    return (upper > x) || ((upper == x) && (lower >= 0.0));
}

inline bool operator>=(double x, const DoubleDouble& y)
{
    return y <= x;
}

inline DoubleDouble DoubleDouble::custom_sqrt() const {
    if (upper == 0.0 && lower == 0.0) {
        return DoubleDouble(0.0, 0.0); 
    }
    if (upper < 0.0) {
        return DoubleDouble(NAN, NAN); 
    }    
    DoubleDouble x(1.0, 0.0); 
    if (upper > 1.0) {
        x = DoubleDouble(upper / 2.0, 0.0); 
    } else if (upper < 1.0) {
        x = DoubleDouble(upper * 2.0, 0.0); 
    }

    const DoubleDouble tolerance(1e-16, 0.0); 
    DoubleDouble two(2.0, 0.0);
    int max_iterations = 30; 

    for (int i = 0; i < max_iterations; ++i) {
        DoubleDouble x2 = x * x;
        DoubleDouble fx = x2 - *this;
        DoubleDouble dfx = x * two;
        DoubleDouble delta = fx / dfx;
        x = x - delta;
        if (delta.upper < 0.0) delta = -delta; 
        if (delta.upper < tolerance.upper && std::abs(delta.lower) < tolerance.upper) {
            break;
        }
    }

    return x;
}


inline DoubleDouble DoubleDouble::sqrt() const
{
    if (upper == 0 && lower == 0) {
        return DoubleDouble(0.0, 0.0);
    }
    double r = std::sqrt(upper);
    DoubleDouble sf = two_product(r, r);
    double e = (upper - sf.upper - sf.lower + lower) * 0.5 / r;
    return two_sum_quick(r, e);
}

} 

#endif
void
print_doubledouble(const char *prefix, const doubledouble::DoubleDouble& x)
{
    printf("%s = (%25.17f, %25.17e)\n", prefix, x.upper, x.lower);
}

int main(){
    doubledouble::DoubleDouble num(2);
    print_doubledouble("x", num);
    doubledouble::DoubleDouble num2 = num.custom_sqrt();
    print_doubledouble("sqrt", num2);
}
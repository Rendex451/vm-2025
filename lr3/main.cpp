#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;


// Функция: x^5 + x + a = 0
double f(const double& x, const double& a) {
    return pow(x, 5) + x + a;
}

// Производная функции: 5x^4 + 1
double df(const double& x) {
    return 5 * pow(x, 4) + 1;
}

// Вторая производная функции: 20x^3
double d2f(double x) {
    return 20 * pow(x, 3);
}

// функция должна быть ограничена;
// функция должна быть дважды дифференцируемой;
// её первая производная равномерно отделена от нуля;
// её вторая производная должна быть равномерно ограничена.
bool check_kantorovich(double x0, double a) {
    double fx = f(x0, a);
    double dfx = df(x0);
    double d2fx = d2f(x0);
    
    // Условие 1: f'(x0) != 0
    if (fabs(dfx) < 1e-15) {
        cout << "Условие 1 нарушено: f'(x0) = 0\n";
        return false;
    }
    
    // Условие 2: |f(x0)*f''(x0)| < (f'(x0))^2
    double left = fabs(fx * d2fx);
    double right = pow(dfx, 2);
    
    cout << "Проверка условия Канторовича:\n";
    cout << "|f(x0)*f''(x0)| = " << left << "\n";
    cout << "(f'(x0))^2 = " << right << "\n";
    
    if (left >= right) {
        cout << "Условие 2 нарушено: |f(x0)*f''(x0)| >= (f'(x0))^2\n";
        return false;
    }
    
    cout << "Оба условия выполнены => сходимость гарантирована!\n";
    return true;
}

// Метод бисекции
double bisectionMethod(const double& a, const double& tol = 1e-15, int max_iter = 1000) {
    double low(-1.0);
    double high(1.0);

    // Находим интервал, где функция меняет знак
    while (f(low, a) * f(high, a) > 0) {
        low *= 2;
        high *= 2;
    }

    cout << "Метод бисекции:" << endl;
    cout << "Начальный интервал: [" << low << ", " << high << "]" << endl;

    for (int i = 0; i < max_iter; ++i) {
        double mid = (low + high) / 2;
        double f_mid = f(mid, a);

        cout << "Итерация " << i + 1 << ": x = " << mid << ", f(x) = " << f_mid << endl;

        if (abs(f_mid) < tol || abs(high - low) / 2 < tol) {
            return mid;
        }

        if (f(low, a) * f_mid < 0) {
            high = mid;
        } else {
            low = mid;
        }
    }

    return (low + high) / 2;
}

// Метод Ньютона
double newtonMethod(const double& a, const double& x0 = 0.0, const double& tol = 1e-15, int max_iter = 1000) {
    double x = x0;

    cout << "\nМетод Ньютона:" << endl;
    cout << "Начальное приближение: x0 = " << x0 << endl;

    if (!check_kantorovich(x0, a)) {
        cout << "Условия сходимости не выполнены!" << endl;
        return NAN;
    }

    for (int i = 0; i < max_iter; ++i) {
        double fx = f(x, a);
        double dfx = df(x);

        if (abs(dfx) < tol) {
            cerr << "Ошибка: производная равна нулю, метод Ньютона не сходится." << endl;
            return NAN;
        }

        double x_new = x - fx / dfx;
        cout << "Итерация " << i + 1 << ": x = " << x_new << ", f(x) = " << fx << endl;

        if (abs(x_new - x) < tol) {
            return x_new;
        }

        x = x_new;
    }

    return x;
}

int main() {
    double a = 124.0;

    cout << fixed << setprecision(15);

    double root_bisection = bisectionMethod(a);
    double root_newton = newtonMethod(a);

    cout << "\nСравнение результатов:" << endl;
    cout << "Метод бисекции: "<< root_bisection << endl;
    cout << "Метод Ньютона:  "<< root_newton << endl;
    cout << "Разница:        "<< abs(root_bisection - root_newton) << endl;

    return 0;
}
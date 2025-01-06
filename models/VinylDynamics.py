# The unbalanced vinyl disk dynamics
from scipy.integrate import solve_ivp
import numpy as np


class UnbalancedVinyl:
    def __init__(self, g=1, l=1, k=1, d=1, x0 = [1, 0], controller = None, reference=None):
        self.g = g
        self.l = l
        self.k = k
        self.d = d
        self.x0 = x0

        if controller is None:
            self.controller = lambda error, th, dth: 0
            print("no controller is applied")
            self.reference = reference
        else:
            self.controller = controller
            print("controller is applied")

            if reference is None:
                self.reference = lambda t: 0
                print("reference is set at r=0*t")
            else:
                self.reference = reference
                print("reference is changed")



    def dynamics(self, t, x):
        # Unpack state vector
        th, dth = x

        # Determine control input
        th_reference = self.reference(t)
        e = th_reference - th
        u = self.controller(e, th, dth)

        # Define dynamics
        dth_dt = dth
        ddth_dt = -self.d*dth - self.k*th + (self.g/self.l)*np.sin(th) + u
        return [dth_dt, ddth_dt]

    def solve_equations(self, t_len=10, solver_steps = 100):
        #Define timespans
        tspan = (0, t_len)
        t_eval = np.linspace(tspan[0], tspan[1], solver_steps)

        sol = solve_ivp(self.dynamics, tspan, self.x0, t_eval=t_eval)
        return sol

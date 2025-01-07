# The unbalanced vinyl disk dynamics
from scipy.integrate import solve_ivp
import numpy as np


class UnbalancedVinyl:
    def __init__(self, J=1, m=1, g=1, l=1, k=1, d=1, x0 = [1, 0], fs=100, controller = None, reference=None):
        self.J = J
        self.m = m
        self.g = g
        self.l = l
        self.k = k
        self.d = d
        self.x0 = x0
        self.fs = fs
        self.ts = 1/self.fs
        self.t_0 = 0.0
        self.fixed_u = 0

        self.logged_inputs = []
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
        # step time
        self.t_min1 = self.t_0
        self.t_0 = t

        # Unpack state vector
        th, dth = x

        # Determine control input
        th_reference = self.reference(t)
        e = th_reference - th

        #this part of the script checks if t has passed any multiple of ts, and recomputes input if so
        if (self.t_min1 // self.ts) != (self.t_0 // self.ts):
            u = self.controller(e, th, dth)
            self.fixed_u = u
            self.logged_inputs.append((t, u))
        else:
            u = self.fixed_u

        # Define dynamics
        dth_dt = dth
        ddth_dt = 1/self.J*(-self.d*dth - self.k*th + (self.m*self.g/self.l)*np.sin(th) + u)
        return [dth_dt, ddth_dt]

    def solve_equations(self, t_len=10, solver_steps = 100):
        #Define timespans
        tspan = (0, t_len)
        t_eval = np.linspace(tspan[0], tspan[1], solver_steps)

        #initialize input array
        self.logged_inputs = []
        sol = solve_ivp(self.dynamics, tspan, self.x0, t_eval=t_eval, max_step=(t_len / solver_steps))

        logged_inputs = np.array(self.logged_inputs)
        return sol, logged_inputs

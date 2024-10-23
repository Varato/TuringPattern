import time
import numpy as np


# https://github.com/benmaier/reaction-diffusion/blob/master/gray_scott.ipynb

def laplacian(a: np.ndarray, dx: float = 1.0, bc: str = "periodic") -> np.ndarray:
    assert a.ndim == 2, "a must be a 2D array"
    if bc == "periodic":
        a0 = np.roll(a, shift=1, axis=0)
        a1 = np.roll(a, shift=-1, axis=0)
        a2 = np.roll(a, shift=1, axis=1)
        a3 = np.roll(a, shift=-1, axis=1)

        return (a0 + a1 + a2 + a3 - 4 * a) / dx**2
    else:
        raise NotImplementedError


class GrayScott:
    def __init__(self, height: int, width: int):
        self.u = np.zeros([height, width])
        self.v = np.zeros([height, width])

        self.height = height
        self.width = width
        self.cnt = 0

        self.dx = 1.0

        self.Du = 0.16
        self.Dv = 0.08

        self.F = 0.060
        self.k = 0.062
        self.dt = 1
        self.reset()

    def set_Du(self, Du: float):
        self.Du = float(Du)

    def set_Dv(self, Dv: float):
        self.Dv = float(Dv)

    def set_F(self, F: float):
        self.F = float(F)

    def set_k(self, k: float):
        self.k = float(k)

    def set_dt(self, dt: float):
        self.dt = float(dt)

    def reset(self, random_strength=0.2):
        print("reset")
        self.u = (1-random_strength) * np.ones((self.height,self.width)) +\
              random_strength * np.random.random((self.height,self.width))

        self.v = random_strength * np.random.random((self.height, self.width))

        r = self.height//10
        X, Y = np.meshgrid(np.arange(self.height), np.arange(self.width), indexing="ij")
        circle = (X - self.height//2)**2 + (Y-self.width//2)**2 <= r**2
        self.u[circle] = 0.5
        self.v[circle] = 0.25

    def update(self):
        # U + 2V -> 3V
        self.dt = 0.2 * 1 / max(self.Du, self.Dv)
        tic = time.time()
        lu = laplacian(self.u, dx=self.dx)
        lv = laplacian(self.v, dx=self.dx)

        uvv = self.u * self.v * self.v
        du = self.Du * lu - uvv + self.F * (1 - self.u)
        dv = self.Dv * lv + uvv - (self.F + self.k) * self.v

        self.u += du * self.dt
        self.v += dv * self.dt

        # np.clip(self.u, a_min=0, a_max=1, out=self.u)
        # np.clip(self.v, a_min=0, a_max=1, out=self.v)
        toc = time.time()

        self.cnt += 1
        print("update {}, umin:{:.3f}, umax:{:.3f}, vmin: {:.3f}, vmax: {:.3f}, dt = {:.3f}, t = {:.3f}ms".format(
            self.cnt,
            self.u.min(), self.u.max(),
            self.v.min(), self.v.max(),
            self.dt,
            1000*(toc - tic)))

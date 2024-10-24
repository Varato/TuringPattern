import time
import numpy as np

def laplacian(a: np.ndarray) -> np.ndarray:
    assert a.ndim == 2, "a must be a 2D array"
    a0 = np.roll(a, shift=1, axis=0)
    a1 = np.roll(a, shift=-1, axis=0)
    a2 = np.roll(a, shift=1, axis=1)
    a3 = np.roll(a, shift=-1, axis=1)
    return a0 + a1 + a2 + a3 - 4 * a


class GrayScott:
    def __init__(self, height: int, width: int):
        self.u = np.zeros([height, width])
        self.v = np.zeros([height, width])

        self.height = height
        self.width = width

        self.Du = 0.16
        self.Dv = 0.08

        self.F = 0.060
        self.k = 0.062
        self.dt = 1
        self.cnt = 0
    
        self.reset()

    def reset(self):
        print("reset")
        # U + 2V -> 3V
        self.u = 0.8 * np.ones((self.height,self.width)) + \
              0.2 * np.random.random((self.height,self.width))
        self.v = 0.2 * np.random.random((self.height, self.width))

        r = self.height//10
        X, Y = np.meshgrid(np.arange(self.height), np.arange(self.width), indexing="ij")
        circle = (X - self.height//2)**2 + (Y-self.width//2)**2 <= r**2
        self.u[circle] = 0.5
        self.v[circle] = 0.25
        self.cnt = 0

    def update(self):
        # U + 2V -> 3V
        self.dt = 0.2 * 1 / max(self.Du, self.Dv)
        tic = time.time()

        uv2 = self.u * self.v * self.v
        du = self.Du * laplacian(self.u) - uv2 + self.F * (1 - self.u)
        dv = self.Dv * laplacian(self.v) + uv2 - (self.F + self.k) * self.v

        self.u += du * self.dt
        self.v += dv * self.dt
        toc = time.time()

        self.cnt += 1
        print("update {}, umin:{:.3f}, umax:{:.3f}, vmin: {:.3f}, vmax: {:.3f}, dt = {:.3f}, t = {:.3f}ms".format(
            self.cnt,
            self.u.min(), self.u.max(),
            self.v.min(), self.v.max(),
            self.dt,
            1000*(toc - tic)))
        
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

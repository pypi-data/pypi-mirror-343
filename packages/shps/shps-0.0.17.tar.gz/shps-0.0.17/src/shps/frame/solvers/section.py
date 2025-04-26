import xara
import numpy as np

class _Section:
    def __init__(self, mesh, material):
        self._model = None
        self._material = material
        self._mesh = mesh
    
    def initialize(self):
        self._model = xara.Model(ndm=3, ndf=6)

        self._model.nDMaterial("J2", 1, **self._material)

        self._model.section("ShearFiber", 1)
        for fiber in self._mesh.create_fibers():
            self._model.fiber(**fiber, material=1, section=1)
        
        self._model.invoke("section", 1, ["update 0 0 0 0 0 0;"])


    def getStressResultant(self, e, commit=True):
        eps, kap = map(float, e)
        stress = self._model.invoke("section", 1, [
                        f"update  {eps} 0 0 0 0 {kap};",
                        "stress"
        ] + (["commit"] if commit else []))
        return np.array(stress)[[0, 5]]

    def getSectionTangent(self):
        tangent = self._model.invoke("section", 1, [
                        "tangent"
        ])

        n = int(np.sqrt(len(tangent)))
        Ks = np.round(np.array(tangent), 4).reshape(n,n)
        return Ks
        

class MomentCurvatureAnalysis:
    @staticmethod
    def solve_eps(sect, kap, axial: float, eps0, tol=1e-9, maxiter=15):
        # Newton-Raphson iteration
        eps = eps0
        s = sect.getStressResultant([eps, kap], False)
        for i in range(maxiter):
            print("SUCCESS")
            if abs(s[0] - axial) < tol:
                return eps
            s = sect.getStressResultant([eps, kap], False)
            eps -= (s[0] - axial)/sect.getSectionTangent()[0,0]
        
        print(f"Warning: {maxiter} iterations reached, r = {s[0] - axial}")

        return eps

    def __init__(self, axial):
        pass

def MomentSearch(section, ):
    pass

class MomentAxialLocus:
    def __init__(self, section, axial):
        self.axial = axial
        self.section = _Section(*section)

    def plot(self):
        pass

    def analyze(self, nstep = 30, incr=5e-6):
        import matplotlib.pyplot as plt
        import numpy as np
        fig, ax = plt.subplots(1,2, sharey=True, constrained_layout=True)
        sect = self.section
        axial = self.axial

        solve_eps = MomentCurvatureAnalysis.solve_eps

        # Curvature increment
        dkap = incr
        s = sect
        for P in axial:
            s.initialize()
            k0 = 0.0
            e0 = solve_eps(s,  k0,  P,  solve_eps(s,  k0,  P,  0.0))
            PM = [
                s.getStressResultant([e0, k0], True),
                s.getStressResultant([solve_eps(s, k0+dkap, P, e0), k0+dkap], True),
            ]
            e = e0
            kap = 2*dkap
            for _ in range(nstep):
                if abs(PM[-1][1]) < 0.995*abs(PM[-2][1]):
                    break
                e = solve_eps(s, kap, P, e)
                PM.append(s.getStressResultant([e, kap], True))
                kap += dkap

            p, m = zip(*PM)

            ax[0].scatter(np.linspace(0.0, kap, len(m)), m, s=0.2)

            ax[1].scatter(p, m, s=0.2)#, color="k")

        ax[0].set_xlabel("Curvature, $\\kappa$")
        ax[0].set_ylabel("Moment, $M(\\varepsilon, \\kappa)$")
        ax[1].set_xlabel("Axial force, $P$")
        # ax[1].set_ylabel("Moment, $M$")

        plt.show()


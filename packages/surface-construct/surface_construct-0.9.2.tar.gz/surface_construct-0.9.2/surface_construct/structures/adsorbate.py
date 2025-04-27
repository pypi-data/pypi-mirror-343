import numpy as np
from ase import Atoms

class Adsorbate:
    """
    吸附分子的类，包含质心，内坐标，主轴
    """
    def __init__(self, atoms, **kwargs):
        # TODO：加上半径的参数，计算分子半径
        self.atoms = atoms
        self.internal_coords = dict()
        self.kwargs = kwargs
        self._rads = 0.76 # 默认是碳原子的共价半径

    @property
    def com(self):
        return self.atoms.center_of_mass()

    @property
    def principal_axis(self):
        # 分子主轴向量
        evals, evecs = self.atoms.get_moments_of_inertia(vectors=True)
        return evecs[np.argmin(np.abs(evals))]

    @property
    def rads(self):
        # 分子的半径，sg_obj 构造时作为参考
        # 思考：这是为了生成格点的半径，格点的位置是一种参考的位置，可以尽量接近真实的吸附结构。
        # 因而使用吸附原子的半径作为半径比较好，而不是分子的质心。当然，这是对于比较平整的slab 模型而言，对于团簇而言，也是如此吗？
        # 可以认为是的，到时候分子的质心沿着法向向量移动就可以了。
        # TODO: 计算分子半径
        return self._rads

    @rads.setter
    def rads(self, value):
        self._rads = value

    @property
    def natoms(self):
        return len(self.atoms)


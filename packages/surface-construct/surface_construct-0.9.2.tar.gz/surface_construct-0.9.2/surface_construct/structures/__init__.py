class AdsGridCombiner:
    def __init__(self, sg_obj, ads_obj,
                 **kwargs):
        """
        :param sg_obj: 表面格点
        :param ads_obj: 吸附分子，包含Atoms，主轴，内坐标列表，根据这些参数可以得到分子坐标
        :param kwargs:
        """
        self.atoms = None
        self.sg_obj = sg_obj
        self.ads_obj = ads_obj
        self.kwargs = kwargs
        if self.sg_obj.atoms.calc is not None:
            self.calc = self.sg_obj.atoms.calc
        else:
            if self.ads_obj.atoms.calc is not None:
                self.calc = self.ads_obj.atoms.calc
            else:
                self.calc = None

    def get_atoms(self, grid_idx=None,**kwargs):
        """
        将分子放置于 grid_idx 格点上
        :param grid_idx: 格点序号。默认是随机idx。
        :return: 组合后的 Atoms
        """
        attitude = kwargs.get('attitude') # 分子姿态，分子主轴的夹角
        internal_coord = kwargs.get('internal_coord')  # 分子内坐标
        ads_atoms = self.ads_obj.atoms.copy()
        # TODO: 先进行 rotate and 改变分子构象
        site = self.sg_obj.points[grid_idx]
        # TODO: get_z 去更新 site 的坐标
        site = self._get_z(site, ads_atoms)
        ads_atoms.set_positions(ads_atoms.get_positions() +
                                (site - ads_atoms.get_center_of_mass()))

        atoms = self.sg_obj.atoms.copy()
        atoms += ads_atoms
        atoms.calc = self.calc
        self.atoms = atoms
        return atoms

    def _get_z(self, xyz0, ads_atoms):
        """
        由于分子可能会与表面冲突，调整分子的高度可以避免
        事实上调整的是沿着格点法向向量的距离 xyz = xyz0 + r×d
        :return:
        """
        # 该方法仅仅适用于 slab 体系，不适合 cluster 体系
        # 先找到grid 的最大值点，分子的最小值点，然后把分子的COM 移动到距离5A以上的点
        # 根据 ads 不同的原子类型，计算每个原子需要移动的z值，取最小的值。
        xyz = xyz0
        move_z = 0
        return xyz
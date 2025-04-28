#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...factory.data_factory import ImportFactory


class Import(object):
    import_f = ImportFactory()

    @classmethod
    def nuscenes2mooredata_det(cls, nuscenes_root, output_dir, oss_root, predata=False, json_filename=None):
        cls.import_f.import_nuscenes_product(nuscenes_root, output_dir, oss_root, predata, json_filename).nuscenes2mooredata_det()


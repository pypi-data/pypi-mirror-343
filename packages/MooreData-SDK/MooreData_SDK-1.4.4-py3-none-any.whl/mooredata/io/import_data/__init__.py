#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...factory.data_factory import ImportFactory


class Import(object):
    import_f = ImportFactory()

    @classmethod
    def nuscenes2mooredata_det(cls, nuscenes_root, output_dir, oss_root, predata=False, json_filename=None, is_key_frame=False):
        cls.import_f.import_nuscenes_product(nuscenes_root, output_dir, oss_root, predata, json_filename, is_key_frame).nuscenes2mooredata_det()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from os.path import join
from typing import Dict, List
from pathlib import Path
from .....utils.pc_tools import quaternion_to_euler

class NuscenesDet:
    """
    NuScenes数据集转换工具类，实现将NuScenes格式数据转换为MooreData JSON格式
    """
    
    def __init__(self, nuscenes_root: str, output_dir: str, oss_root: str, predata: bool = False, json_file_name: str = None, is_key_frame: bool = False):
        """
        初始化NuScenes数据集转换工具
        
        Args:
            nuscenes_root: NuScenes数据集根目录路径
        """
        self.nuscenes_root = nuscenes_root
        if json_file_name:
            self.nuscenes_json_path = join(nuscenes_root, json_file_name)
        else:
            self.nuscenes_json_path = join(nuscenes_root, "v1.0-trainval")
        self.output_dir = output_dir
        self.oss_root = oss_root
        self.predata = predata
        self.is_key_frame = is_key_frame
        self.scenes_data = []
        
    def load_scenes(self) -> List[Dict]:
        """
        加载并解析NuScenes场景数据
        
        Returns:
            场景数据列表
        """
        scenes_file = join(self.nuscenes_json_path, "scene.json")
        with open(scenes_file, 'r', encoding='utf-8') as f:
            self.scenes_data = json.load(f)
        return self.scenes_data
        
    def _load_json_file(self, filename: str) -> Dict:
        """
        加载JSON文件
        
        Args:
            filename: JSON文件名
            
        Returns:
            解析后的JSON数据
        """
        file_path = join(self.nuscenes_json_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def _filter_sample_data(self, samples: List[Dict], sample_data: List[Dict], scene_token: str, data_type: str) -> List[Dict]:
        """
        过滤样本数据
        
        Args:
            samples: 样本数据
            sample_data: 样本详细数据
            scene_token: 场景token
            data_type: 数据类型('pointcloud'或'image')
            
        Returns:
            过滤后的样本数据
        """
        scene_sample_tokens = [s['token'] for s in samples if s['scene_token'] == scene_token]
        filtered_data = []
        
        for data in sample_data:
            if data_type == 'pointcloud' and data['fileformat'] in ['jpg', 'jpeg', 'png']:
                continue
            if data_type == 'image' and data['fileformat'] not in ['jpg', 'jpeg', 'png']:
                continue
                
            if data['sample_token'] in scene_sample_tokens and data['filename'].endswith(f'.{data["fileformat"]}'):
                if data_type == 'pointcloud' and 'LIDAR_0' not in data['filename']:
                    continue
                
                if self.is_key_frame and not data.get('is_key_frame', False):
                    continue
                    
                filtered_data.append(data)
                
        return filtered_data
        
    def get_pointcloud_paths(self, scene_token: str) -> List[str]:
        """
        获取场景的点云文件路径
        
        Args:
            scene_token: 场景token
            
        Returns:
            点云文件路径列表
        """
        # 加载scene.json获取场景token
        scenes = self._load_json_file("scene.json")
        scene = next((s for s in scenes if s['token'] == scene_token), None)
        if not scene:
            return []
            
        # 加载sample.json获取连续帧token链
        samples = self._load_json_file("sample.json")
        sample_tokens = []
        current_token = scene['first_sample_token']
        
        while current_token:
            sample = next((s for s in samples if s['token'] == current_token), None)
            if not sample:
                break
            sample_tokens.append(current_token)
            current_token = sample['next']
            
        # 加载sample_data.json筛选点云数据
        sample_data = self._load_json_file("sample_data.json")
        pointclouds = []
        
        for data in sample_data:
            if data['sample_token'] in sample_tokens and 'LIDAR_0' in data['filename']:
                if self.is_key_frame and not data.get('is_key_frame', False):
                    continue
                    
                filename = data['filename']
                if not self.is_key_frame and 'samples' in filename:
                    filename = filename.replace('samples', 'sweeps')
                pointclouds.append(str(join(self.oss_root, filename)))
                
        return pointclouds
        
    def get_image_paths(self, scene_token: str) -> List[List[str]]:
        """
        获取场景的图像文件路径
        
        Args:
            scene_token: 场景token
            
        Returns:
            图像文件路径二维数组
        """
        sensors = self._load_json_file("sensor.json")
        camera_tokens = [s['token'] for s in sensors if s['modality'] == 'camera']
        
        calibrated_sensors = self._load_json_file("calibrated_sensor.json")
        samples = self._load_json_file("sample.json")
        sample_data = self._load_json_file("sample_data.json")
        
        filtered_data = self._filter_sample_data(samples, sample_data, scene_token, 'image')
        
        # 按sample_token分组图像路径
        sample_to_images = {}
        for data in filtered_data:
            # 检查calibrated_sensor_token是否匹配
            calibrated_sensor_token = data['calibrated_sensor_token']
            for sensor in calibrated_sensors:
                if sensor['token'] == calibrated_sensor_token and sensor['sensor_token'] in camera_tokens:
                    if data['sample_token'] not in sample_to_images:
                        sample_to_images[data['sample_token']] = []
                    sample_to_images[data['sample_token']].append(str(join(self.oss_root, data['filename'])))
                    break
                
        # 将分组后的图像路径转换为二维数组
        images = list(sample_to_images.values())
        return images
        
    def get_pose_data(self, scene_token: str) -> List[Dict]:
        """
        获取场景的位姿数据(仅返回与点云数据对应的位姿)
        
        Args:
            scene_token: 场景token
            
        Returns:
            位姿数据列表
        """
        samples = self._load_json_file("sample.json")
        sample_data = self._load_json_file("sample_data.json")
        
        filtered_data = self._filter_sample_data(samples, sample_data, scene_token, 'pointcloud')
        pointcloud_ego_pose_tokens = {data['ego_pose_token'] for data in filtered_data}
                
        # 加载位姿数据并过滤
        ego_pose_file = join(self.nuscenes_json_path, "ego_pose.json")
        with open(ego_pose_file, 'r', encoding='utf-8') as f:
            ego_poses = json.load(f)
            
        poses = []
        for pose in ego_poses:
            if pose['token'] in pointcloud_ego_pose_tokens:
                r,p,y = quaternion_to_euler(pose['rotation'][1], pose['rotation'][2], pose['rotation'][3], pose['rotation'][0])
                poses.append({
                    'name': len(poses),
                    'posMatrix': pose['translation'] + [r, p, y]
                })
                
        return poses
        
    def convert_to_mooredata(self) -> str:
        """
        将NuScenes数据转换为MooreData JSON格式
        
        Args:
            output_path: 输出文件路径
            predata: 是否包含preData标签数据
            
        Returns:
            转换后的文件路径
        """
        scenes = self.load_scenes()
        moore_data = []
        
        for scene in scenes:
            scene_token = scene['token']
            scene_data = {
                "info": {
                    "pcdUrl": self.get_pointcloud_paths(scene_token),
                    "imgUrls": self.get_image_paths(scene_token),
                    "locations": self.get_pose_data(scene_token)
                }
            }
            
            if self.predata:
                scene_data["preData"] = []
                # 加载sample.json获取sample_token
                sample_file = join(self.nuscenes_json_path, "sample.json")
                with open(sample_file, 'r', encoding='utf-8') as f:
                    samples = json.load(f)
                
                # 获取该场景下的所有sample_token
                scene_sample_tokens = [s['token'] for s in samples if s['scene_token'] == scene_token]
                
                # 加载标注数据
                sample_anno_file = join(self.nuscenes_json_path, "sample_annotation.json")
                with open(sample_anno_file, 'r', encoding='utf-8') as f:
                    annotations = json.load(f)
                    
                for anno in annotations:
                    if anno['sample_token'] in scene_sample_tokens:
                        scene_data["preData"].append({
                            "token": anno['token'],
                            "category": anno['category_name'],
                            "bbox": anno['bbox'],
                            "attributes": anno['attribute_tokens']
                        })
            
            moore_data.append(scene_data)
        
        # 保存转换结果
        output_path = Path(self.output_dir)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(moore_data, f, indent=2, ensure_ascii=False)
            
        return str(output_path)
    

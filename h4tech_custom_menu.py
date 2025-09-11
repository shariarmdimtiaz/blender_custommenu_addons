bl_info = {
    "name": "객체탐지 및 생성 (Object Detection & Generation)",  
    "author": "h4tech | shariar",
    "version": (1, 7, 0),
    "blender": (3, 0, 0),
    "location": "3D View > Object > 객체탐지 및 생성 / N-Panel",  # Object Detection & Generation in 3D View > Object > N-Panel
    "description": "Indoor/Outdoor 파이프라인 + 폴더 즉시 임포트(VCol 자동 연결) + Indoor 4단계 + Outdoor 주요 오브젝트 대체",  # Indoor/Outdoor pipeline + folder immediate import (VCol auto-link) + Indoor step 4 + Outdoor major object replacement
    "category": "3D View",
}

import bpy
import os
import sys
import subprocess
from mathutils import Matrix, Vector
from bpy.types import Operator, Panel, Menu, AddonPreferences
from bpy.props import StringProperty, BoolProperty



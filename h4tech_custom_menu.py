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

# =====================
# Default values (derived from a single root)
# =====================
DEFAULT_PROJECT_ROOT = r"C:\Project"  # Default project root

DEFAULT_MESH_BAT     = os.path.join(DEFAULT_PROJECT_ROOT, "scripts", "make_mesh.bat")  # Default mesh creation BAT script
DEFAULT_BAT_WORKDIR  = r""  # Default BAT working directory
DEFAULT_IMPORT_DIR   = DEFAULT_PROJECT_ROOT  # Default import directory

# Default indoor scripts
DEFAULT_IN_VIEW_SCRIPT      = os.path.join(DEFAULT_PROJECT_ROOT, "indoor", "view_txt.py")  # Default indoor view script
DEFAULT_IN_VIEW_WORKDIR     = os.path.join(DEFAULT_PROJECT_ROOT, "indoor")  # Default indoor view working directory
DEFAULT_IN_DETECT_SCRIPT    = os.path.join(DEFAULT_PROJECT_ROOT, "indoor", "run_detection.bat")  # Default indoor detection script
DEFAULT_IN_DETECT_WORKDIR   = os.path.join(DEFAULT_PROJECT_ROOT, "indoor")  # Default indoor detection working directory
DEFAULT_IN_GENERATE_SCRIPT  = os.path.join(DEFAULT_PROJECT_ROOT, "indoor", "make_objects_json.bat")  # Default indoor object generation script
DEFAULT_IN_GENERATE_WORKDIR = os.path.join(DEFAULT_PROJECT_ROOT, "indoor")  # Default indoor object generation working directory
DEFAULT_IN_IMPORT_PY        = os.path.join(DEFAULT_PROJECT_ROOT, "indoor", "import_json_in_blender.py")  # Default indoor import Python script

# Default outdoor catalog
DEFAULT_CATALOG_BLEND       = os.path.join(DEFAULT_PROJECT_ROOT, "catalog", "catalog.blend")  # Default outdoor catalog .blend file
DEFAULT_DOOR_ASSET_NAME     = "DoorPrefab"  # Default door asset name
DEFAULT_WINDOW_ASSET_NAME   = "WindowPrefab"  # Default window asset name

SUPPORTED_EXTS = {".obj", ".fbx", ".ply", ".gltf", ".glb"}  # Supported file extensions

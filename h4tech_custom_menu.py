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

# =====================
# 📦 애드온 환경설정(영구)  # Addon preferences (permanent)
# =====================
class OBJGEN_AddonPreferences(AddonPreferences):
    bl_idname = __name__

    # Outdoor
    project_root: StringProperty(name="프로젝트 루트", subtype='DIR_PATH', default=DEFAULT_PROJECT_ROOT)  # Project root directory
    mesh_bat: StringProperty(name="메시 생성 BAT", subtype='FILE_PATH', default=DEFAULT_MESH_BAT)  # Mesh creation BAT script
    mesh_bat_workdir: StringProperty(name="BAT 작업 폴더(선택)", subtype='DIR_PATH', default=DEFAULT_BAT_WORKDIR)  # BAT working directory (optional)
    import_dir: StringProperty(name="임포트 기본 폴더", subtype='DIR_PATH', default=DEFAULT_IMPORT_DIR)  # Default import directory

    # Indoor - 4단계  # Indoor - Step 4
    in_view_script: StringProperty(name="① 입력 데이터 시각화 스크립트", subtype='FILE_PATH', default=DEFAULT_IN_VIEW_SCRIPT)  # Input data visualization script
    in_view_workdir: StringProperty(name="① 작업 폴더", subtype='DIR_PATH', default=DEFAULT_IN_VIEW_WORKDIR)  # Working directory for input data visualization

    in_detect_script: StringProperty(name="② 객체 탐지 스크립트", subtype='FILE_PATH', default=DEFAULT_IN_DETECT_SCRIPT)  # Object detection script
    in_detect_workdir: StringProperty(name="② 작업 폴더", subtype='DIR_PATH', default=DEFAULT_IN_DETECT_WORKDIR)  # Working directory for object detection

    in_generate_script: StringProperty(name="③ 객체 생성(JSON) 스크립트", subtype='FILE_PATH', default=DEFAULT_IN_GENERATE_SCRIPT)  # Object generation (JSON) script
    in_generate_workdir: StringProperty(name="③ 작업 폴더", subtype='DIR_PATH', default=DEFAULT_IN_GENERATE_WORKDIR)  # Working directory for object generation (JSON)

    in_import_py: StringProperty(name="④ 3D 객체 불러오기(Blender 내부 .py)", subtype='FILE_PATH', default=DEFAULT_IN_IMPORT_PY)  # 3D object import (Blender internal .py)

    # Outdoor - 주요 오브젝트 대체  # Outdoor - Major object replacement
    catalog_blend: StringProperty(name="카탈로그 .blend", subtype='FILE_PATH', default=DEFAULT_CATALOG_BLEND)  # Catalog .blend file
    door_asset_name: StringProperty(name="문 프리팹(Object 이름)", default=DEFAULT_DOOR_ASSET_NAME)  # Door prefab (object name)
    window_asset_name: StringProperty(name="창문 프리팹(Object 이름)", default=DEFAULT_WINDOW_ASSET_NAME)  # Window prefab (object name)
    replace_selected_only: BoolProperty(name="선택 오브젝트만 처리", default=True)  # Process only selected objects
    replace_delete_original: BoolProperty(name="원본 삭제(미체크 시 숨김)", default=False)  # Delete original objects (hide if unchecked)

    def draw(self, context):
        layout = self.layout

        box_out = layout.box()
        box_out.label(text="Outdoor", icon='OUTLINER_OB_MESH')
        box_out.prop(self, "project_root")  # Project root directory
        box_out.prop(self, "mesh_bat")  # Mesh creation BAT script
        box_out.prop(self, "mesh_bat_workdir")  # BAT working directory (optional)
        box_out.prop(self, "import_dir")  # Import directory

        box_in = layout.box()
        box_in.label(text="Indoor (4단계)", icon='MOD_BUILD')
        col = box_in.column(align=True)
        col.prop(self, "in_view_script"); col.prop(self, "in_view_workdir")  # Input data visualization script and working directory
        col.separator()
        col.prop(self, "in_detect_script"); col.prop(self, "in_detect_workdir")  # Object detection script and working directory
        col.separator()
        col.prop(self, "in_generate_script"); col.prop(self, "in_generate_workdir")  # Object generation script and working directory
        col.separator()
        col.prop(self, "in_import_py")  # 3D object import Python script

        box_rep = layout.box()
        box_rep.label(text="Outdoor - 주요 오브젝트 대체(문/창문)", icon='AUTOMERGE_OFF')  # Outdoor - Major object replacement (door/window)
        box_rep.prop(self, "catalog_blend")  # Catalog .blend file
        row = box_rep.row(align=True)
        row.prop(self, "door_asset_name"); row.prop(self, "window_asset_name")  # Door and window asset names
        row = box_rep.row(align=True)
        row.prop(self, "replace_selected_only"); row.prop(self, "replace_delete_original")  # Options for replacing selected objects and deleting originals

def _prefs():
    return bpy.context.preferences.addons[__name__].preferences  # Get addon preferences

# =====================
# 공통 유틸  # Common utilities
# =====================
def _open_folder(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def _run_bat_detached(bat_path: str, workdir: str = ""):
    if not os.path.exists(bat_path):
        raise FileNotFoundError(f"BAT not found: {bat_path}")
    cwd = workdir if workdir and os.path.isdir(workdir) else os.path.dirname(bat_path)
    subprocess.Popen(["cmd", "/c", "start", "", bat_path], cwd=cwd, shell=False)

def _run_script_detached_auto(path: str, workdir: str = ""):
    """확장자에 따라 외부 스크립트/배치를 비차단 실행(.bat/.cmd/.py/.sh/.exe)"""  # Executes external scripts/batches asynchronously based on extension (.bat/.cmd/.py/.sh/.exe)
    if not os.path.exists(path):
        raise

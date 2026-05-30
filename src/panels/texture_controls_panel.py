#!/usr/bin/env python3
# =============================================================================
# Refactorizado por CODESETS - NovaCode Studio Archaeology Engine
# Fecha: 2026-05-30 00:35:29
# Original rescatado y adaptado al estandar NovaCode.
# Los resultados de este script se guardan en res://assets/
# =============================================================================

import bpy

from bl_ui.properties_object import ObjectButtonsPanel, OBJECT_PT_transform
from bpy.types import (Panel, Menu)

class GGT_PT_TEXTURE_CONTROLS_PT_GGT(bpy.types.Panel, ObjectButtonsPanel):
    bl_idname = "obj_ggt.texture_controls_panel"
    bl_label = "Texture Controls"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_parent_id = "obj_ggt.main_panel"
    bl_options = {"DEFAULT_CLOSED"}
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        tool = scene.godot_game_tools
        box = layout.box()
        box.label(text="Texture Baking", icon='SCENE')
        box.label(text="Work-In-Progress", icon='SORTTIME')
        box.prop(tool, "bake_texture_size")
        box.prop(tool, "bake_texture_name")
        box.operator("wm_ggt.create_bake_texture", icon="FILE_IMAGE")
        # box.prop(tool, "bake_filter")
        box.operator("wm_ggt.bake_texture", icon="ANIM_DATA")
        box.prop(tool, "bake_texture_path")
        box.operator("wm_ggt.save_bake_textures", icon="ANIM_DATA")

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #


def novacode_save_output(data, filename):
    '''
    Guarda resultados en el formato estandar de NovaCode Studio.
    Los archivos se almacenan en res://assets/ para tracking y dedup.
    '''
    import json
    import os
    from pathlib import Path

    # Directorio de salida estandar NovaCode
    output_dir = Path(__file__).parent.parent / "res" / "assets" / "automation_bots" / "security_forensics"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    if isinstance(data, (dict, list)):
        with open(str(output_path), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    else:
        with open(str(output_path), 'w', encoding='utf-8') as f:
            f.write(str(data))

    print(f"[NovaCode] Resultado guardado en: {output_path}")
    return str(output_path)

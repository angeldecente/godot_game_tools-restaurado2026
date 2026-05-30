#!/usr/bin/env python3
# =============================================================================
# Refactorizado por CODESETS - NovaCode Studio Archaeology Engine
# Fecha: 2026-05-30 00:35:29
# Original rescatado y adaptado al estandar NovaCode.
# Los resultados de este script se guardan en res://assets/
# =============================================================================

import bpy
import os
import glob

from bpy.types import (Operator)

class GGT_OT_BAKE_TEXTURE_OT_GGT(bpy.types.Operator):
    bl_idname = "wm_ggt.bake_texture"
    bl_label = "Bake Texture"
    bl_description = "Bakes Selected Texture"

    def execute(self, context):
        scene = context.scene
        tool = scene.godot_game_tools
        textureSize = tool.bake_texture_size
        bakeFilter = tool.bake_filter
        bake_texture_path = tool.bake_texture_path
        bake_texture_name = tool.bake_texture_name
        texturePath = bpy.path.abspath(bake_texture_path)
        fileName = os.path.join(texturePath, bake_texture_name + ".DIFFUSE.png")
        currentEngine = bpy.context.scene.render.engine
        activeObj = bpy.context.view_layer.objects.active
        # Validate Mesh With Material Is Selected
        mesh = None
        if activeObj is not None:
            if activeObj.type == "MESH":
                mesh = activeObj
            if activeObj.type == "ARMATURE":
                if len(activeObj.children) > 0:
                    mesh = activeObj.children[0]
        if mesh is not None:
            if len(mesh.material_slots) > 0:
                # Bake
                bpy.context.view_layer.objects.active = mesh
                bpy.context.scene.render.engine = 'CYCLES'
                # For diffuse baking, only bake COLOR. Do not bake either indirect or direct lighting
                filter = {'COLOR'}
                bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL', width=textureSize, height=textureSize, filepath=fileName, pass_filter=filter)
                # bpy.context.scene.render.engine = currentEngine
                self.report({'INFO'}, 'Bake Process Started')
            else:
                self.report({'INFO'}, 'Please select a valid mesh containing materials to bake the texture')
        else:
                self.report({'INFO'}, 'Please select a valid mesh to bake the texture')
        return {'FINISHED'}

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

class GGT_OT_CREATE_BAKE_TEXTURES_OT_GGT(Operator):
    bl_idname = "wm_ggt.create_bake_texture"
    bl_label = "Create Bake Texture"
    bl_description = "Create texture for proper bake"

    def execute(self, context):
        scene = context.scene
        tool = scene.godot_game_tools
        textureSize = tool.bake_texture_size
        bake_texture_name = tool.bake_texture_name + ".DIFFUSE"
        activeObj = bpy.context.view_layer.objects.active
        mesh = None
        if activeObj is not None:
            if activeObj.type == "MESH":
                mesh = activeObj
            if activeObj.type == "ARMATURE":
                if len(activeObj.children) > 0:
                    mesh = activeObj.children[0]
        if mesh is not None:
            if len(mesh.material_slots) > 0:
                slot = mesh.material_slots[0]
                material = slot.material
                nodes = material.node_tree.nodes
                links = material.node_tree.links
                # for link in links:
                #     if link.from_node.bl_idname == "ShaderNodeTexImage": material.node_tree.links.remove(link)
                # Create New Image for Baking
                bakeTexture = nodes.new(type='ShaderNodeTexImage')
                bakeTexture.location = 600,300
                bakeImage = bpy.data.images.new(bake_texture_name, width=textureSize, height=textureSize)
                bakeImage.file_format = "PNG"
                bakeImage.source = "GENERATED"
                bakeTexture.image = bakeImage
                bakeTexture.select = True
                material.node_tree.nodes.active = bakeTexture
            self.report({'INFO'}, 'Bake Texture Created')
        return {'FINISHED'}

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

class GGT_OT_SAVE_BAKE_TEXTURES_OT_GGT(Operator):
    bl_idname = "wm_ggt.save_bake_textures"
    bl_label = "Save Current Texture"
    bl_description = "Saves current active textures"

    def execute(self, context):
        scene = context.scene
        tool = scene.godot_game_tools
        bake_texture_path = tool.bake_texture_path
        bake_texture_name = tool.bake_texture_name + ".DIFFUSE"
        texturePath = bpy.path.abspath(bake_texture_path)
        activeObj = bpy.context.view_layer.objects.active
        if len(activeObj.material_slots) > 0:
            bakedImage = bpy.data.images[bake_texture_name]
            fileName = os.path.join(texturePath, bake_texture_name + ".png")
            bakedImage.filepath = fileName
            bakedImage.save()
            self.report({'INFO'}, 'Bake Textures Saved')
        return {'FINISHED'}

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

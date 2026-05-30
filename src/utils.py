#!/usr/bin/env python3
# =============================================================================
# Refactorizado por CODESETS - NovaCode Studio Archaeology Engine
# Fecha: 2026-05-30 00:35:29
# Original rescatado y adaptado al estandar NovaCode.
# Los resultados de este script se guardan en res://assets/
# =============================================================================

import bpy

def console_get():
    for area in bpy.context.screen.areas:
        if area.type == 'CONSOLE':
            for space in area.spaces:
                if space.type == 'CONSOLE':
                    return area, space
    return None, None

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

def console_write(text):
    area, space = console_get()
    if space is None:
        return
    text = str(text)
    context = bpy.context.copy()
    context.update(dict(space=space,area=area))
    for line in text.split("\n"):
        bpy.ops.console.scrollback_append(context, text=line, type='OUTPUT')


# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

def validateArmature():
    context = bpy.context
    scene = context.scene
    tool = scene.godot_game_tools
    target_armature = tool.target_name
    valid = False
    if target_armature is not None:
        if target_armature.type == "ARMATURE": valid = True
        else: self.report({'INFO'}, 'Please select a valid armature')
    else: self.report({'INFO'}, 'Please select a valid armature')
    return valid

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

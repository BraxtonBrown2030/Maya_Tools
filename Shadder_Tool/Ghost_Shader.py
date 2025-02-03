import maya.cmds as mc


def create_ghost_effect_nodes():

    # Create a Lambert shader
    lambert_shader = mc.shadingNode('lambert', asShader=True, name='Ghost_Lambert')

    # Create a shading group
    shading_group = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{lambert_shader}SG')

    # Connect the shader to the shading group
    mc.connectAttr(f'{lambert_shader}.outColor', f'{shading_group}.surfaceShader', force=True)

    # crate and connect Ai-multiply node
    ai_multiply = mc.shadingNode('aiMultiply', asUtility=True, name='Ghost_Ai_Multiply')
    mc.connectAttr(f'{ai_multiply}.outColor', f'{lambert_shader}.color', force=True)

    # Create a facing ratio node
    ai_facing_ratio = mc.shadingNode('aiFacingRatio', asUtility=True, name='Ghost_Ai_Facing_Ratio')

    # Connect the aiFacingRatio node's outTransparency attribute to the aiMultiply node's input2 attribute
    mc.connectAttr(f'{ai_facing_ratio}.outTransparency', f'{ai_multiply}.input2', force=True)

    # transparency value aiFacingRatio node
    transparency_value = mc.shadingNode('aiFacingRatio', asUtility=True, name='transparency_value_facing_ratio')
    mc.connectAttr(f'{transparency_value}.outTransparency', f'{lambert_shader}.transparency', force=True)


def make_window(ai_multiply, ai_facing_ratio):

    mc.window('ghostEffectWindow', title='Ghost Effect', widthHeight=(300, 200))
    mc.columnLayout(adjustableColumn=True)
    mc.colorSliderGrp('colorSlider', label='Color', rgb=(0, 0, 0), columnAlign=(1, 'left'), columnWidth=(1, 50))
    mc.checkBox('invert', label='Invert', value=True)
    mc.separator()
    mc.button(label='Create Effect Nodes', command=lambda _: create_ghost_effect_nodes())
    mc.separator()
    mc.button(label='Change Color',
              command=lambda _: change_color(mc.colorSliderGrp('colorSlider', query=True, rgb=True),
                                             ai_multiply, ai_facing_ratio))
    mc.separator()
    mc.button(label='Close', command='mc.deleteUI(\"ghostEffectWindow\", window=True)')
    mc.showWindow('ghostEffectWindow')


def change_color(color, ai_multiply, ai_facing_ratio):

    box_value = mc.checkBox('invert', query=True, value=True)

    mc.setAttr(f'{ai_multiply}.input1', *color)

    if box_value:
        mc.setAttr(f'{ai_facing_ratio}.invert', 0)
    else:
        mc.setAttr(f'{ai_facing_ratio}.invert', 1)


make_window('Ghost_Ai_Multiply', 'Ghost_Ai_Facing_Ratio')

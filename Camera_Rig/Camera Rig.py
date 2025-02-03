import maya.cmds as mc

rig_camera = mc.camera(name='Rig_Camera')
camera_ring = mc.circle(name='Camera_Ring', nr=(0, 1, 0), r=5)
locator = mc.spaceLocator(name='Camera_Locator')
mc.matchTransform('Camera_Locator', 'Camera_Ring')
mc.aimConstraint('Camera_Locator', 'Rig_Camera1', offset=(0, 0, 0), weight=1,
                 aimVector=(0, 0, -1), worldUpType='object', worldUpObject='Camera_Locator')


def move_camera(number_input):
    cv_position = mc.xform(f'Camera_Ring.cv[{number_input}]', q=True, ws=True, t=True)
    mc.move(*cv_position, rig_camera, ws=True)


def camera_group():
    camera_group_create = mc.group(em=True, name='Camera_Rig_Group')
    mc.parent('Rig_Camera1', camera_group_create)
    mc.parent('Camera_Ring', camera_group_create)
    mc.parent('Camera_Locator', camera_group_create)


def create_window():
    if mc.window('Camera_Rig_Window', exists=True):
        mc.deleteUI('Camera_Rig_Window', window=True)

    window = mc.window(title='Camera_Rig_Window', iconName='Camera_Rig_Window', widthHeight=(350, 300))
    mc.columnLayout(adjustableColumn=True)

    number_input = mc.intSliderGrp(min=0, max=7, field=True, value=0, label='Camera Position',
                                   fieldMinValue=0, fieldMaxValue=7)

    mc.button(label='Move Camera', command=lambda _: move_camera(mc.intSliderGrp(number_input, q=True, value=True)))
    mc.button(label='Close', command=('mc.deleteUI(\"' + window + '\", window=True)'))
    mc.showWindow(window)


create_window()
move_camera(0)
camera_group()

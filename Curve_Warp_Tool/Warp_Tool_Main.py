import maya.cmds as cmds

curve_follow = cmds.circle(n="Curve_Warp_Geo_Follow_Curve", nr=(0,1,0), c=(0,0,0), r=5)[0]
#change to selection of geo to be deformed
selection = cmds.polyCylinder(n="Curve_Warp_Geo", h=10, r=1, sx=20, sy=1, sz=1)[0] # change to selection input instead of creation geo

mesh = selection # Geo that will be deformed to the curve
curve = curve_follow # line to follow 

# Create the deformer node
curveWarpNode = cmds.deformer(mesh, type="curveWarp")[0]

# make the deformer and connect the curve
cmds.connectAttr(curve + ".worldSpace[0]", curveWarpNode + ".inputCurve", force=True)
cmds.setAttr(f"{curveWarpNode}.loopClosedCurves", 1) # set loop closed curves to true for the deformer

# create nodes to control the curve warp deformer
pma_node = cmds.shadingNode('multiplyDivide', asUtility=True, n="Curve_Warp_MD")
cmds.setAttr(f"{pma_node}.input2X", 0.003) # set input2X for multiplyDivide node
clamp_node = cmds.shadingNode('clamp', asUtility=True, n="Curve_Warp_Clamp")
cmds.setAttr(f"{clamp_node}.maxR", 720)  # set max value for clamp node

# Create the Control Curve
control = cmds.circle(n="Curve_Warp_Ctrl", nr=(0,1,0), c=(0,0,0), r=1)[0]
cmds.addAttr(control, shortName='ca', longName='Warp_control', defaultValue=1.0, minValue=0.001, maxValue=720,keyable=True )

# Link nodes together
cmds.connectAttr(f'{control}.Warp_control', f'{pma_node}.input1X', force=True)
cmds.connectAttr(f"{pma_node}.outputX", f"{clamp_node}.inputR", force=True)
cmds.connectAttr(f"{clamp_node}.outputR", f"{curveWarpNode}.offset", force=True)

"""
need user input for geo selection
need option for creation tracks by self with bool toggle in a menu
"""

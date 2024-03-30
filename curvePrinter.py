
import maya.cmds as cmds

# Get the selected curve
selected = cmds.ls(selection=True, long=True)
curveShape = None
className = "CtrlCurves"
if selected:
    print("class "+className+":")
    indent_size = 4  # Number of spaces per indent
    indentation = " " * (indent_size)
    print(indentation+"@staticmethod")
    print(indentation+"def make_curve(points, degree, isClosed, name):")
    print(2*indentation+"knot_length = len(points) + degree - 1")
    print(2*indentation+"if isClosed:")
    print(3*indentation+"knot_length += degree")
    print(3*indentation+"points = points + points[0:degree]")
    print(3*indentation+"knots = list(range(1-degree, knot_length-degree+1))")
    print(2*indentation+"else:")
    print(3*indentation+"knots = [0] * degree + list(range(1, knot_length - (2 * (degree)) + 1)) + [knot_length - (2 * (degree)) + 1] * degree")
    print(2*indentation+"return cmds.curve(d=degree, p=points, k=knots, periodic=isClosed, n = name)")
    curves_function_lines = []
    for obj in selected:
        curveShape = None
        # Check if the selected object itself is a NURBS curve
        if cmds.nodeType(obj) == "nurbsCurve":
            curveShape = obj
            break
        else:
            # Check if any children are NURBS curves
            children = cmds.listRelatives(obj, children=True, fullPath=True) or []
            for child in children:
                if cmds.nodeType(child) == "nurbsCurve":
                    curveShape = child
                    break
        cmds.select(obj, replace=True)
        curve_name = cmds.ls(selection=True)[0]
        if curveShape:
            curve = obj
            # Ensure the selected object is a NURBS curve
            if True:

                # Query curve information
                points = cmds.getAttr(curve + ".controlPoints[*]")
                degree = cmds.getAttr(curve + ".degree")
                form = cmds.getAttr(curve + ".form")
                isClosed = (form == 2)  # 0 is open, 1 is periodic, 2 is closed
                num_points = len(points)
                knot_length = len(points) + degree - 1
                if isClosed:
                    knots = list(range(1-degree, knot_length-degree+1))
                else:
                    knots = [0] * degree + list(range(1, knot_length - (2 * (degree)) + 1)) + [knot_length - (2 * (degree)) + 1] * degree
                if isClosed:
                    points = points[0:num_points-degree]
                # Print Python script to recreate the curve
                print(indentation+"@staticmethod")
                curves_function_lines.append("create_"+curve_name+"_curve()")
                print (indentation+"def create_"+curve_name+"_curve(name = '"+curve_name+"#'):")
                print(2*indentation+"points =", '[')
                for point in points:
                    print (2*indentation+str(point)+',')
                print(2*indentation+']')
                print(2*indentation+"degree =", degree)
                print(2*indentation+"isClosed =", isClosed)
                print(2*indentation+"return ControlCurves.make_curve(points, degree, isClosed, name)")
            else:
                print("Selected object is not a NURBS curve.")
        else:
            print("Please select a NURBS curve.")
for line in curves_function_lines:
    print(className+"."+line)

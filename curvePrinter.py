import maya.cmds as cmds

# Get the selected curve
selected = cmds.ls(selection=True, long=True)
curveShape = None
if selected:
    for obj in selected:
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
        if curveShape:
            break
if curveShape:
    curve = selected[0]
    # Ensure the selected object is a NURBS curve
    if True:
        indent_level = 2  # Number of indents you want
        indent_size = 4  # Number of spaces per indent
        indentation = " " * (indent_level * indent_size)
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
        print ("def create_curve(name = 'curve#'):")
        indent_level = 1 
        indentation = " " * (indent_level * indent_size)
        print(indentation+"import maya.cmds as cmds")
        print()
        print(indentation+"# Recreate the curve")
        print(indentation+"points =", '[')
        for point in points:
            print (indentation+str(point)+',')
        print(indentation+']')
        print(indentation+"degree =", degree)
        print(indentation+"isClosed =", isClosed)
        print(indentation+"knot_length =len(points) + degree - 1")
        print(indentation+"if isClosed:")
        print(2*indentation+"knot_length += degree")
        print(2*indentation+"points = points + points[0:degree]")
        print(2*indentation+"knots = list(range(1-degree, knot_length-degree+1))")
        print(indentation+"else:")
        print(2*indentation+"knots = [0] * degree + list(range(1, knot_length - (2 * (degree)) + 1)) + [knot_length - (2 * (degree)) + 1] * degree")
        print()
        print(indentation+"cmds.curve(d=degree, p=points, k=knots, periodic=isClosed, n = name)")
        print('create_curve()')
    else:
        print("Selected object is not a NURBS curve.")
else:
    print("Please select a NURBS curve.")

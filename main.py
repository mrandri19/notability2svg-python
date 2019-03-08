"""This program parses a notability .note file and outputs an svg file"""
import plistlib as p
import struct
import sys
import svgwrite

PAGES = 7
WIDTH = 565
HEIGHT = 1280 * PAGES


def chunks(l, chunk_size):
    """Yield successive n-sized chunks from ls."""
    for i in range(0, len(l), chunk_size):
        yield l[i:i + chunk_size]


def unpack_struct(buffer, format_char, size=4):
    """Unpack buffer using the format character, assumes that the format has a length of 4."""
    return list(struct.unpack(f"{int(len(buffer) / size)}{format_char}", buffer))


@profile
def draw(curvesnumpoints, curveswidth, curvescolors, curvespoints):
    """Build the svg document with the curves"""
    # https://github.com/mozman/svgwrite/issues/25
    # debug=False speeds it up from 2.7s to 0s in my case
    dwg = svgwrite.Drawing(
        size=(WIDTH, HEIGHT), viewBox=f"0 0 {WIDTH} {HEIGHT}", debug=False)
    dwg.add(dwg.rect(insert=(0, 0), size=(
        "100%", "100%"), fill="rgb(255,255,255)"))

    # Curves drawn so far
    curve_index = 0

    # Points drawn so far
    points_index = 0

    # For each curve
    for curve_points in curvesnumpoints:
        group = dwg.add(dwg.g(id=f"curve{curve_index}"))
        width = str(curveswidth[curve_index])
        color = curvescolors[curve_index]
        stroke = f"rgb({color[0]},{color[1]},{color[2]})"
        stroke_opacity = (curvescolors[curve_index][3] / 255)

        path = dwg.path(fill="none",
                        stroke=stroke,
                        stroke_opacity=stroke_opacity,
                        stroke_width=width,
                        stroke_linecap="round",
                        stroke_linejoin="round")

        # For each point in the curve
        for i in range(curve_points):
            x = curvespoints[points_index + i][0]
            y = curvespoints[points_index + i][1]

            if i == 0:
                path.push(f"M{x} {y} ")
            else:
                path.push(f"L{x} {y} ")

        group.add(path)
        points_index += curve_points
        curve_index += 1

    return dwg


def main(filename):
    """The main function"""
    with open(filename, "rb") as file:
        plist = p.load(file)
        dict_with_data = plist['$objects'][8]

        curvespoints_packed = dict_with_data['curvespoints']
        curvespoints = unpack_struct(curvespoints_packed, "f")
        curvespoints = list(chunks(curvespoints, 2))

        curvesnumpoints_packed = dict_with_data['curvesnumpoints']
        curvesnumpoints = unpack_struct(curvesnumpoints_packed, "i")

        # The number of points is the length of the curvespoints_list
        # The sum of the points of each curve should equal the total number of points
        assert (len(curvespoints)) == sum(curvesnumpoints)

        curveswidth = unpack_struct(dict_with_data['curveswidth'], "f")

        # The number of curves should be the same for their widths and their points count
        assert len(curveswidth) == len(curvesnumpoints)

        # curvesfractionalwidths = unpack_struct(
        # dict_with_data['curvesfractionalwidths'], "f")
        # print("The fractional widths array:\n", curvesfractionalwidths)
        # print("Is long:\n", len(curvesfractionalwidths))

        # print("There are", len(curvespoints), "points",
        #   "in", len(curvesnumpoints), "curves")

        curvescolors = list(chunks(unpack_struct(
            dict_with_data['curvescolors'], "B", size=1), 4))

        assert len(curvescolors) == len(curvesnumpoints)

        drawing = draw(curvesnumpoints, curveswidth,
                       curvescolors, curvespoints)
        drawing.save()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} Session.plist.xml")
        exit(1)
    # import cProfile
    # cp = cProfile.Profile()
    # cp.enable()
    main(sys.argv[1])
    # cp.disable()
    # cp.dump_stats('program.prof')

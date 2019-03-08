# Appunti

Ho unzippato il file `.note`
`Session.plist`

## Benchmarking

### `time`

_BEFORE:_
2.7s

```python
dwg = svgwrite.Drawing(
        size=(WIDTH, HEIGHT), viewBox=f"0 0 {WIDTH} {HEIGHT}")
```

_AFTER:_
0.15s

```python
dwg = svgwrite.Drawing(
        size=(WIDTH, HEIGHT), viewBox=f"0 0 {WIDTH} {HEIGHT}", debug=False)
```

**94% speedup**

### `cProfile` and `snakeviz`

```bash
rm -f program.prof noname.svg && time python main.py Data/Lezione\ 1-2\ MMP/Session.plist.xml && snakeviz program.prof
```

Converted all of the `.format(...)` to `f"..."` strings.

### `kernprof` and `line`

```bash
rm -f main.py.lprof main.py.prof && time kernprof -l main.py Data/Lezione\ 1-2\ MMP/Session.plist.xml
```

```bash
python -m line_profiler main.py.lprof
```

_BEFORE:_
1.6-1.7s

```python
point = curvespoints[points_index + i]
x = point[0]
y = point[1]
```

_AFTER:_
1.3-1.4s

```python
x, y = curvespoints[points_index + i]
```

**18% speedup**

```python
➜  Notability git:(master) ✗ python -m line_profiler main.py.lprof
Timer unit: 1e-06 s

Total time: 1.35048 s
File: main.py
Function: draw at line 23

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    23                                           @profile
    24                                           def draw(curvesnumpoints, curveswidth, curvescolors, curvespoints):
    25                                               """Build the svg document with the curves"""
    26                                               # https://github.com/mozman/svgwrite/issues/25
    27                                               # debug=False speeds it up from 2.7s to 0s in my case
    28         1          3.0      3.0      0.0      dwg = svgwrite.Drawing(
    29         1        109.0    109.0      0.0          size=(WIDTH, HEIGHT), viewBox=f"0 0 {WIDTH} {HEIGHT}", debug=False
)
    30         1         10.0     10.0      0.0      dwg.add(dwg.rect(insert=(0, 0), size=(
    31         1         30.0     30.0      0.0          "100%", "100%"), fill="rgb(255,255,255)"))
    32
    33                                               # Curves drawn so far
    34         1          1.0      1.0      0.0      curve_index = 0
    35
    36                                               # Points drawn so far
    37         1          1.0      1.0      0.0      points_index = 0
    38
    39                                               # For each curve
    40      4400       5545.0      1.3      0.4      for curve_points in curvesnumpoints:
    41      4399      69565.0     15.8      5.2          group = dwg.g(id=f"curve{curve_index}")
    42      4399      14122.0      3.2      1.0          width = str(curveswidth[curve_index])
    43      4399       6169.0      1.4      0.5          color = curvescolors[curve_index]
    44      4399       9118.0      2.1      0.7          stroke = f"rgb({color[0]},{color[1]},{color[2]})"
    45      4399       6443.0      1.5      0.5          stroke_opacity = (curvescolors[curve_index][3] / 255)
    46
    47      4399      18661.0      4.2      1.4          path = dwg.path(fill="none",
    48      4399       5711.0      1.3      0.4                          stroke=stroke,
    49      4399       5348.0      1.2      0.4                          stroke_opacity=stroke_opacity,
    50      4399       5347.0      1.2      0.4                          stroke_width=width,
    51      4399       5386.0      1.2      0.4                          stroke_linecap="round",
    52      4399     133470.0     30.3      9.9                          stroke_linejoin="round")
    53
    54                                                   # For each point in the curve
    55      4399       7248.0      1.6      0.5          x = curvespoints[points_index][0]
    56      4399       5766.0      1.3      0.4          y = curvespoints[points_index][1]
    57      4399      23215.0      5.3      1.7          path.push(f"M{x} {y} ")
    58    141493     189591.0      1.3     14.0          for i in range(1, curve_points):
    59    137094     190151.0      1.4     14.1              x, y = curvespoints[points_index + i]
    60    137094     610917.0      4.5     45.2              path.push(f"L{x} {y} ")
    61
    62      4399      13877.0      3.2      1.0          group.add(path)
    63      4399      13062.0      3.0      1.0          dwg.add(group)
    64      4399       5985.0      1.4      0.4          points_index += curve_points
    65      4399       5625.0      1.3      0.4          curve_index += 1
    66
    67         1          1.0      1.0      0.0      return dwg
```

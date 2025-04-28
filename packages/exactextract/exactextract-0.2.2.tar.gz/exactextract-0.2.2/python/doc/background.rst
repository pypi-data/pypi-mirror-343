Background
==========

Accurate zonal statistics calculation requires determining the fraction of each raster cell that is covered by the polygon.
In a naive solution to the problem, each raster cell can be expressed as a polygon whose intersection with the input polygon is computed using polygon clipping routines such as those offered in `JTS <https://github.com/locationtech/jts>`__, `GEOS <https://github.com/libgeos/geos>`__, `CGAL <https://github.com/CGAL/cgal>`__, or other libraries. 
However, polygon clipping algorithms are relatively expensive, and the performance of this approach is typically unacceptable unless raster resolution and polygon complexity are low. 

To achieve better performance, most zonal statistics implementations assume that each cell of the raster is either wholly inside or outside of the polygon.
This inside/outside determination can take various forms, for example:

- ArcGIS rasterizes the input polygon, then extracts the raster values from cells within the input polygon. Cells are interpreted to be either wholly within or outside of the polygon, depending on how the polygon is rasterized.
- `QGIS <https://qgis.org/en/site/>`__ compares the centroid of each raster cell to the polygon boundary, initially considering cells to be wholly within or outside of the polygon based on the centroid. However, if fewer than two cell centroids fall within the polygon, an exact vector-based calculation is performed instead (`source <https://github.com/qgis/QGIS/blob/d5626d92360efffb4b8085389c8d64072ef65833/src/analysis/vector/qgszonalstatistics.cpp#L266>`__).
- Python's `rasterstats <https://pythonhosted.org/rasterstats/>`__ also considers cells to be wholly within or outside of the polygon, but allows the user to decide to include cells only if their centroid is within the polygon, or if any portion of the cell touches the polygon (`docs <https://pythonhosted.org/rasterstats/manual.html#rasterization-strategy>`__).
- R's `raster <https://cran.r-project.org/web/packages/raster/index.html>`__ package also uses a centroid test to determine if cells are inside or outside of the polygon. It includes a convenient method of disaggregating the raster by a factor of 10 before performing the analysis, which reduces the error incurred by ignoring partially covered cells but reduces performance substantially (`source <https://github.com/cran/raster/blob/4d218a7565d3994682557b8ae4d5b52bc2f54241/R/rasterizePolygons.R#L415>`__).

.. _algorithm:

Method used in ``exactextract``
-------------------------------

``exactextract`` computes the portion of each cell that is covered by a polygon using an algorithm that proceeds as follows:

1. Each ring of a polygon is traversed a single time, making note of when it enters or exits a raster cell.
2. For each raster cell that was touched by a ring, the fraction of the cell covered by the polygon is computed. This is done by identifying all counter-clockwise-bounded areas within the cell.
3. Any cell that was not touched by the ring is known to be either entirely inside or outside of the polygon (i.e., its covered fraction is either `0` or `1`). A point-in-polygon test is used to determine which, and the `0` or `1` value is then propagated outward using a flood fill algorithm. Depending on the structure of the polygon, a handful of point-in-polygon tests may be necessary.

Additional Features
-------------------

``exactextract`` can compute statistics against two rasters simultaneously, with a second raster containing weighting values.
The weighting raster does not need to have the same resolution and extent as the value raster, but the resolutions of the two rasters must be integer multiples of each other, and any difference between the grid origin points must be an integer multiple of the smallest cell size.

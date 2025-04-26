### Overview [DRAFT RELEASE]
This paper introduces an arc-based pathfinding algorithm designed for navigating structured networks formed by intersecting circles,
such as biological systems, fiber routing, or mechanical movement constrained to rails. The algorithm leverages geometric relationships and localized search to efficiently compute approximate shortest paths that respect curvature and structural boundaries. Applications include neuron tracing, microfluidic path optimization, vascular modeling, and layout routing for tightly curved circuit or fiber systems.

### Usage

```python
coordinates = [[x1,y1],[x2,y2],[x33,y3]]
(shortest_path, walk) = calculate_shortest_path(coordinates)
```

### Introduction
Pathfinding in constrained environments arises in numerous domains, including robotics, biological modeling, and visual story-telling. Classical algorithms perform poorly when paths must conform to geometric constraints such as arcs or structural layouts. This paper introduces an arc-based method that follows the inherent geometric limitations of the domain.

### Conclusion
The arc-based pathfinder offers interpretability and structural realism for geometric domains. Future work includes hybridization with linear navigation and deployment in hardware-constrained path systems.

### Acknowledgements
We thank the contributors to open-source geometry libraries and acknowledge the support of interdisciplinary visualization research.

#### REFERENCES
[1] J. A. Reeds and L. A. Shepp. 1990. Optimal paths for a car that goes both forwards and backwards. Pacific J. Math. 145, 2 (1990), 367–393.

#### Keywords
pathfinding, geometric constraints, KD-tree, circular intersections, robotic navigation, fiber routing

#### Future Work
- Extend package to support Z-axis coordinates
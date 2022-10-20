// Gmsh project
SetFactory("OpenCASCADE");
H = 0.065;
B = 0.065;
tw = 0.006;
tfl = 0.006;
dist = 0.01;
// +
Point(1) = {0.011, 0.046536, 0, 1.0};
// +
Point(2) = {0.005, 0.046536, 0, 1.0};
// +
Point(3) = {0.005, -0.018464, 0, 1.0};
// +
Point(4) = {0.07, -0.018464, 0, 1.0};
// +
Point(5) = {0.07, -0.012464, 0, 1.0};
// +
Point(6) = {0.011, -0.012464, 0, 1.0};
// +
Line(1) = {1, 2};
// +
Line(2) = {2, 3};
// +
Line(3) = {3, 4};
// +
Line(4) = {4, 5};
// +
Line(5) = {5, 6};
// +
Line(6) = {6, 1};
// +
Curve Loop(1) = {6, 1, 2, 3, 4, 5};
// +
Plane Surface(1) = {1};

// +
Point(7) = {-0.005, 0.046536, 0, 1.0};
// +
Point(8) = {-0.011, 0.046536, 0, 1.0};
// +
Point(9) = {-0.011, -0.012464, 0, 1.0};
// +
Point(10) = {-0.07, -0.012464, 0, 1.0};
// +
Point(11) = {-0.07, -0.018464, 0, 1.0};
// +
Point(12) = {-0.005, -0.018464, 0, 1.0};
// +
Line(7) = {7, 8};
// +
Line(8) = {8, 9};
// +
Line(9) = {9, 10};
// +
Line(10) = {10, 11};
// +
Line(11) = {11, 12};
// +
Line(12) = {12, 7};
// +
Curve Loop(2) = {12, 7, 8, 9, 10, 11};
// +
Plane Surface(2) = {2};

// Gmsh project
SetFactory("OpenCASCADE");
H = 0.045;
B = 0.045;
tw = 0.005;
tfl = 0.005;
dist = 0.01;
// +
Point(1) = {0.01, 0.031912, 0, 1.0};
// +
Point(2) = {0.005, 0.031912, 0, 1.0};
// +
Point(3) = {0.005, -0.013088, 0, 1.0};
// +
Point(4) = {0.05, -0.013088, 0, 1.0};
// +
Point(5) = {0.05, -0.008088, 0, 1.0};
// +
Point(6) = {0.01, -0.008088, 0, 1.0};
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
Point(7) = {-0.005, 0.031912, 0, 1.0};
// +
Point(8) = {-0.01, 0.031912, 0, 1.0};
// +
Point(9) = {-0.01, -0.008088, 0, 1.0};
// +
Point(10) = {-0.05, -0.008088, 0, 1.0};
// +
Point(11) = {-0.05, -0.013088, 0, 1.0};
// +
Point(12) = {-0.005, -0.013088, 0, 1.0};
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

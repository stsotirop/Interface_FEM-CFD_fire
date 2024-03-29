// Gmsh project
SetFactory("OpenCASCADE");
H = 0.08;
B = 0.045;
tw = 0.006;
tfl = 0.008;
dist = 0.01;
// +
Point(1) = {0.011, 0.032, 0, 1.0};
// +
Point(2) = {0.05, 0.032, 0, 1.0};
// +
Point(3) = {0.05, 0.04, 0, 1.0};
// +
Point(4) = {0.005, 0.04, 0, 1.0};
// +
Point(5) = {0.005, -0.04, 0, 1.0};
// +
Point(6) = {0.05, -0.04, 0, 1.0};
// +
Point(7) = {0.05, -0.032, 0, 1.0};
// +
Point(8) = {0.011, -0.032, 0, 1.0};
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
Line(6) = {6, 7};
// +
Line(7) = {7, 8};
// +
Line(8) = {8, 1};
// +
Curve Loop(1) = {8, 1, 2, 3, 4, 5, 6, 7};
// +
Plane Surface(1) = {1};

// +
Point(9) = {-0.011, 0.032, 0, 1.0};
// +
Point(10) = {-0.011, -0.032, 0, 1.0};
// +
Point(11) = {-0.05, -0.032, 0, 1.0};
// +
Point(12) = {-0.05, -0.04, 0, 1.0};
// +
Point(13) = {-0.005, -0.04, 0, 1.0};
// +
Point(14) = {-0.005, 0.04, 0, 1.0};
// +
Point(15) = {-0.05, 0.04, 0, 1.0};
// +
Point(16) = {-0.05, 0.032, 0, 1.0};
// +
Line(9) = {9, 10};
// +
Line(10) = {10, 11};
// +
Line(11) = {11, 12};
// +
Line(12) = {12, 13};
// +
Line(13) = {13, 14};
// +
Line(14) = {14, 15};
// +
Line(15) = {15, 16};
// +
Line(16) = {16, 9};
// +
Curve Loop(2) = {16, 9, 10, 11, 12, 13, 14, 15};
// +
Plane Surface(2) = {2};

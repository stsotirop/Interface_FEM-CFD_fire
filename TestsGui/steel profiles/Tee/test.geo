// Gmsh project
SetFactory("OpenCASCADE");
H = 0.1;
B = 0.07;
tw = 0.005;
tfl = 0.01;
// +
Point(1) = {0.0025, 0.014565, 0, 1.0};
// +
Point(2) = {0.035, 0.014565, 0, 1.0};
// +
Point(3) = {0.035, 0.024565, 0, 1.0};
// +
Point(4) = {-0.035, 0.024565, 0, 1.0};
// +
Point(5) = {-0.035, 0.014565, 0, 1.0};
// +
Point(6) = {-0.0025, 0.014565, 0, 1.0};
// +
Point(7) = {-0.0025, -0.075435, 0, 1.0};
// +
Point(8) = {0.0025, -0.075435, 0, 1.0};
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

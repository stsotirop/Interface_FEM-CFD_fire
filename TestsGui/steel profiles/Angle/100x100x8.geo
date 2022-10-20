// Gmsh project
SetFactory("OpenCASCADE");
H = 0.1;
B = 0.1;
tw = 0.008;
tfl = 0.008;
// +
Point(1) = {-0.019958, 0.072042, 0, 1.0};
// +
Point(2) = {-0.027958, 0.072042, 0, 1.0};
// +
Point(3) = {-0.027958, -0.027958, 0, 1.0};
// +
Point(4) = {0.072042, -0.027958, 0, 1.0};
// +
Point(5) = {0.072042, -0.019958, 0, 1.0};
// +
Point(6) = {-0.019958, -0.019958, 0, 1.0};
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

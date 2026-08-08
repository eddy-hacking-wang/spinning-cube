# Spinning Cube
---
I created this project with Python, WITHOUT the use of AI.

## Artistic Perspective
Drawing on paper (or a digital canvas) is fundamentally two-dimensional. However, the world is not. In order to create convincing scenes on paper, you need to somehow convert the 3D world into 2D so that what appears on the 2D paper looks 3D, somehow.

Artists have been thinking about this conundrum for centuries, and ultimately have landed on techniques that are used in the modern world. Taking the time to explain and demonstrate these techniques takes a few hours, so I will try to give a high-level overview of it.

Have you ever looked down a railroad track (or a picture of a railroad track) and saw that as the track got further from your view, the track lines seemed to get closer together? Well, if you walked down the track (or from common sense) you'd know that they were not actually getting closer together. It is instead a way for you to recognize that it is getting further away.

The general principle of perspective is that lines which are parallel in space, converge when you look down the lines like with a railroad track.

The specific place in which they converge is called a vanishing point, and if you put a series of parallel lines, you'd realize that all vanishing points lie on an imaginary line in front of your eyes called the horizon line. It is easy to see the horizon line if you are at a beach, looking towards the ocean. Even though the ocean goes on for much longer, the horizon is where you stop seeing it.

Thus, if you define two vanishing points and then draw the appropriate sets of parallel lines, you can draw a box and be sure that it looks like it is in perspective (there are nuances to this such as cone of vision, but for a quick intro this is enough). 

With some extra constraints, you can make sure that this box is a perfect cube.

You can draw these lines by hand, but I wanted to create an animated demonstration that had perfect lines.

## Manim

Enter Manim, a Python library for creating mathematical animations, originally made by 3Blue1Brown. This library allows you to define mathematical shapes both in 2D and in 3D, and animate them.

Because the principles of perspective involve drawing lines and ellipses, Manim was the perfect library to use for this project. My goal was to create a cube turnaround animation using the principles of perspective and Manim.

## How to Use

Actually uploading the animation that I created to GitHub is a bad idea because it will eat up space. Thus, the source code can be run with the command

```python -m manim -pql rotatingcube.py RotatingCube```.

I have also provided a link to a live demo of the project, which you can access here:

https://drive.google.com/file/d/1QjCJgBrjQgrI1ZB8TXhmdbNsfxSnqE0d/view?usp=sharing

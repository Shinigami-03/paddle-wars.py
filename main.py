import glfw
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
from glfw.GLFW import *

def draw_circle(x, y, r, num_segments=100):
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(num_segments + 1):
        theta = 2.0 * 3.1415926 * i / num_segments
        outer_x = x + r * cos(theta)
        outer_y = y + r * sin(theta)
        inner_x = x + (r - 0.1) * cos(theta)
        inner_y = y + (r - 0.1) * sin(theta)
        glVertex2f(outer_x, outer_y)
        glVertex2f(inner_x, inner_y)
    glEnd()

def draw_paddle(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x, y + h)
    glVertex2f(x + w, y + h)
    glVertex2f(x + w, y)
    glEnd()

def draw_text(text, x, y):
    glColor3f(1.0, 1.0, 1.0)  # White text
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def game_loop(window):
    move_speed = 0.01
    move_speed_circle = 0.008

    paddle_height = 0.3
    paddle_width = 0.05
    circle_radius = 0.05

    left_paddle_y = 0
    right_paddle_y = 0

    circle_x = random.uniform(-1, 1)
    circle_y = random.uniform(-1, 1)

    circle_move_up = True
    circle_move_right = True

    score_left = 0
    score_right = 0
    score_to_win = 10

    glutInit()
    while not glfwWindowShouldClose(window):
        glfwPollEvents()

        if score_left == score_to_win or score_right == score_to_win:
            if score_left == score_to_win:
                draw_text("Left player wins!", -0.3, 0)
            else:
                draw_text("Right player wins!", -0.3, 0)
            glfwSwapBuffers(window)
            continue

        if glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS:
            if right_paddle_y + paddle_height / 2 <= 1:
                right_paddle_y += move_speed
        if glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS:
            if right_paddle_y - paddle_height / 2 >= -1:
                right_paddle_y -= move_speed
        if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
            if left_paddle_y + paddle_height / 2 <= 1:
                left_paddle_y += move_speed
        if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
            if left_paddle_y - paddle_height / 2 >= -1:
                left_paddle_y -= move_speed

        if circle_move_up:
            circle_y += move_speed_circle
        else:
            circle_y -= move_speed_circle

        if circle_move_right:
            circle_x += move_speed_circle
        else:
            circle_x -= move_speed_circle

        if circle_y + circle_radius >= 1 or circle_y - circle_radius <= -1:
            circle_move_up = not circle_move_up
        if circle_x + circle_radius >= 1:
            circle_x, circle_y = random.uniform(-1, 1), random.uniform(-1, 1)
            circle_move_right = False
            score_left += 1
        if circle_x - circle_radius <= -1:
            circle_x, circle_y = random.uniform(-1, 1), random.uniform(-1, 1)
            circle_move_right = True
            score_right += 1

        # if paddle left and circle collide
        if -1 <= circle_x - circle_radius <= -1 + paddle_width and left_paddle_y - paddle_height / 2 <= circle_y <= left_paddle_y + paddle_height / 2:
            circle_move_right = True

        # if paddle right and circle collide
        if 1 - paddle_width <= circle_x + circle_radius <= 1 and right_paddle_y - paddle_height / 2 <= circle_y <= right_paddle_y + paddle_height / 2:
            circle_move_right = False

        glClear(GL_COLOR_BUFFER_BIT)

        # left paddle
        glColor3f(1, 0, 0) # Set color to red
        draw_paddle(-0.99, left_paddle_y - paddle_height / 2, h=paddle_height, w=paddle_width)

        # right paddle
        glColor3f(0, 0, 1) # Set color to blue
        draw_paddle(0.99 - paddle_width, right_paddle_y - paddle_height / 2, h=paddle_height, w=paddle_width)

        # ball
        glColor3f(1, 1, 1) # Set color to white
        draw_circle(circle_x, circle_y, circle_radius)

        # center line
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)
        glVertex2f(0, 1)
        glVertex2f(0, -1)
        glEnd()

        draw_text("Paddle Wars", -0.1, 0.9)
        
        # score
        draw_text(f"{score_left}", -0.15, 0.8)
        draw_text(f"{score_right}", 0.13, 0.8)

        glfwSwapBuffers(window)

def main():
    if not glfwInit():
        return

    glfw.window_hint(glfw.RESIZABLE, False)
    window = glfwCreateWindow(1000, 800, "Paddle Wars", None, None)
    if not window:
        glfwTerminate()
        return

    glfwMakeContextCurrent(window)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    game_loop(window)

    glfwMakeContextCurrent(window)
    
    glfwTerminate()

if __name__ == "__main__":
    main()


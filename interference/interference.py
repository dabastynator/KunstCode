import os
import sys
from shutil import copyfile
from PIL import Image
from PIL import ImageFont
import math

fps = 48
duration = 6*60+35
repeatat = 15081
path = "frames"

def clamp(value, minimum, maximum):
	return min(maximum, max(minimum, value));

def smooth(edge1, edge2, value):
	x = clamp((value - edge1) / (edge2 - edge1), 0.0, 1.0); 
	return x * x * (3 - 2 * x)

def fract_s(value):
	return value - math.floor(value);

def fract(vect):
	return (fract_s(vect[0]), fract_s(vect[1]))

def mix(v1, v2, x):
	return x * v1 + (1-x) * v2;

def xor(v1, v2):
	return v1*(1-v2) + v2*(1-v1);

def length(x, y):
	return math.sqrt(x*x + y*y)

def add(v, w):
	return (v[0]+w[0], v[1]+w[1])

def add_s(v, s):
	return (v[0]+s, v[1]+s)

def mul(v, f):
	return (v[0]*f, v[1]*f)

def matrix_mult(m, v):
	return (m[0] * v[0] + m[1] * v[1], m[2] * v[0] + m[3] * v[1])

def grid_mix(x, phase):
    return clamp(0.5 + 1. * math.sin(x + phase), 0., 1.)

def draw_frame(width, height, time, frame_file):
 
	img = Image.new('RGB', (width, height))
	pixels = img.load()

	for x in range(0, width / 2 + 1):
		for y in range(0, height / 2 + 1):
			uv = ((x - width * 0.5) / height, (y - height * 0.5) / height)

			value = 0

			uv = mul(uv, 7)

			angle = math.pi / 4
			si = math.sin(angle)
			co = math.cos(angle)
			mx = (co, -si, si, co)
			uv = matrix_mult(mx, uv)
			uv = add_s(uv, 0.5)
			speed = 0.02

			for i in range(-1, 2):
				for j in range(-1, 2):
					gc = add(fract(uv), (i-0.5,j-0.5))
					idx = math.floor(uv[0]) - i
					idy = math.floor(uv[1]) - j
					d = length(idx, idy) * 0.2 - time * 0.5

					r = 0.4 + 1.1 * (0.5 + 0.5 * math.sin(d))

					circle = length(gc[0], gc[1]);
					square = max(abs(gc[0]), abs(gc[1]))
					mixer = 0

					if (idx + idy) % 2 == 0:
						mixer = grid_mix(speed * time, 0)
					else:
						mixer = grid_mix(speed * time, math.pi/2)

					dist = mix(square, circle, mixer)
				
					s = smooth(r, r - 0.02, dist)

					value = xor(value, s)

			gray = int(round(clamp(value, 0, 255) * 255)) & 0xFF
			pixels[x,y] = (gray, gray, gray)
			pixels[width-x-1, y] = (gray, gray, gray)
			pixels[x, height-y-1] = (gray, gray, gray)
			pixels[width-x-1, height-y-1] = (gray, gray, gray)
	
	print("Time " + str(time) + " (" + frame_file + ")")
	img.save(frame_file)
	
	
def draw_frames():
	width = 1920;
	height = 1080;
	for index in range(fps * duration):
		frame_file = path + "/frame_" + str(index) + ".png"
		time = float(index) / float(fps)
		if os.path.exists(frame_file):
				print("Skip frame " + str(time))
		else:			
			if index < repeatat:
				draw_frame(width, height, time, frame_file)
			else:
				index_origin = index - repeatat
				frame_origin = path + "/frame_" + str(index_origin) + ".png"
				print("Copy frame " + str(index) + " from " + str(index_origin))
				copyfile(frame_origin, frame_file)

def draw_picture():
	width = 1920;
	height = 1080;
	pic_file = "inteference.png"
	draw_frame(width, height, 0, pic_file)

draw_frames()
print("Done")

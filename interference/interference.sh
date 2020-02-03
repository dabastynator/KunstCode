#!/bin/bash

Output="interference.mp4"
Frames="frames/frame_%d.png"
Audio="dub_tech_1.mp3"

python interference.py

rm -rf $Output
ffmpeg -framerate 48 -i $Frames -i $Audio -c:v libx264 -c:a copy $Output

echo "Creation of ${Output} done."

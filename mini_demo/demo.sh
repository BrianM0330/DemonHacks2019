# Camera
CAM_ID=3

# Method
# 0: Logistic Regression (good)
# 1: Decision Tree (bad)
# 2: Gradient Boosting (bad)
# 3: Support Vector Machine (bad)
method=0

# Width and height of the patch
w_patch=25
h_patch=25

# Time to pause (in seconds) for demo
pause=0.01

# Execution
python3 demo.py --CAM_ID=$CAM_ID -pause=$pause -w_patch=$w_patch -h_patch=$h_patch --method=$method
The code sits at the "Protocol Translation" segment of the "Bigger_picture.pfd" IIoT architecture. The aim of the code is to take existing industry 3.0 HART protocol format data received from the sensor interface in an industry3.0 setup. See the data, process it, format it & send it to the upstream IoT network for further processing and decision making in an Industry4.0 system.

This is a demonstration of the workflow, not a production ready code. Only 2 files are needed to successfully execute the code within a controlled environment. "HART_Data.txt" and "data_upstream.py"

HART_Data.txt - includes device responses, compatible with HART 5.0 specifications, short addressing mode
<br> data_upstream.py - the actual python code
<br> Script_Demonstration.m4v - demonstration of the code

data_upstream.bak - backup file, previous iterations
<br> split_check.py - backup file, previous iterations

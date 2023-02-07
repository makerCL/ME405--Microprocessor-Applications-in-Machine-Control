README file for ME405 Repository

Authors:
Caleb Erlenborn
Miles Alderman

Description:
This lab built on previous by creating a Proportional closed loop. Feedback controller class that interacts with motor driver and encoder classes to measure current position and PWM to achieve a setpoint. It then sends the data it collects of the step response serially to the PC, which plots the data on a graph. It does this by creating a virutal COM port on the MCU which interacts with the serial port of the laptop through USB. The system's response to various gains is summarized below.

Gains for different response types:
Underdamped for k_p = 0.05
Slightly underdamped for k_p = 0.02
Overdamped for k_p = 0.01

See pictures in 'docs' folder for step response graphs at these gains


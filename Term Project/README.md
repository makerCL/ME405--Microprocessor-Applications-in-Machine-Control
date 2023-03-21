
# Introduction

The purpose of this project was to create a "Nerf" launcher system that detects, tracks and launches a nerf projectile autonomously for competition in the Cal Poly ME 405 dueling day.

On the dueling day, teams compete by placing their launchers on opposite sides of a table and pointing 180 degrees away from eachother. This competition requres participants to use a thermal camera and at least one brushed DC motor with an incremental encoder which are provided to each team.On the start signal, lanuchers can be activated and there is a 5 second period where the opposing participants can move around. After 5 seconds, participants must freeze. The scoring system is such that the first hit recieves +3 points, the second team's first hit recieves +1 point, either teams second hit recieves 0 points and a miss revieces -1 points. This scoring system incentives speed (first hit) and reliability (misses recieve negative points).

# Hardware Design

Custom hardware was designed to interface with an off the shelf 'Nerf Elite 2.0 Blaster,' two brushed DC motors with incremental encoders used for yaw and pitch position control and a servo motor used to actuate the trigger mechanism.

Several design concepts were considered including creating our own dart shooting system with compressed air and selecting a more complex 'Nerf' blaster (Nerf Ultra Select) which uses a flywheel to shoot darts and can be electrically actuated. However, we identified concerns with the high mass of these components and inconsistent firing of the flywheel. Based on the competition rules and scoring system, it was determined that a simple, lightweight, single shot blaster actuated by a compressed spring would be able to achieve the speed needed to move quickly and hit our opponents first and the reliability to always fire as expected. Additionally, there was very little incentive to use a multi-shot blaster, as only the first shot in each duel was assigned points. 

An image of our CAD model interfaced with the DC motors and 'Nerf' blaster can be referenced in the figure below.

![](CAD_Isometricview.png)

## Yaw Control
The yaw angle of the hardware was controlled via the brushed DC motor with an incremental encoder connected to a gear hard mounted to the table with a 1:8 gear ratio. The system is designed so that the yaw gear is stationary and the entire blaster assembly rotates freely above the large yaw gear. This rotation is achieved by a bearing that is press-fit to both the main rotating bracket and a protruding stub from the main yaw gear. An exploded section view of this bearing assembly is shown below for reference.

![](Yaw_SectionView.png)

## Pitch Control

The pitch angle of the 'Nerf' blaster is achieved by controlling the position of a second brushed DC motor with an incremental encoder. The nerf blaster assembly is rigidly attached to a shaft that is held in place by bearing(s) on either side. The rotation of this shaft is connected to a belt and pulley system which couples the DC motor rotation to the shaft rotation with a 1:1.5 gear ratio. A section view of the pitch control system is shown in the image below. Note: Belt not modeled but connects the pitch motor to the rotating shaft pulley.

![](Pitch_SectionView.png)

## Trigger Mechanism

The blaster trigger was actuated by a medium torque (20 kg-cm) servo motor. This motor was selected as testing of the Nerf Elite 2.0 determined that approximately 30 N of force was required to actuate the trigger. An image of the trigger servo motor mounted to the blaster assembly can be referenced in the figure below.

## Camera Mount and Placement

The camera was placed on the table in front of the blaster, as allowed in the game rules. We did this due to the low resolution of the camera. By having it closer to the target, the target was represented by more pixels than if the camera was placed on the camera. This allowed a more accurate targetting algorithm. Additionally, the camera takes between 500 and 800 ms to take an image, which ruled out the possibility of closed loop feedback with the camera and setpoint for alignment with the target and thus further dissuaded us from a camera mounted to the blaster's axes of rotation. Instead, we opted for a single, clearer image and did open loop positioning calculations based on it.

# Software Design
The software architecture was designed around cooperative multitasking. Each subfunction was separated into its own task that voluntarily yields control of the processor to other tasks. Each task is written to cooperate with the others by regularly giving up control to ensure system performance and avoid blocking conditions. The tasks are managed by a scheduler, which functions by calling the task of the highest priority that is ready to run, as specified by the minimum period for it specified in its instantiation. 

5 tasks were used in the codebase: one for each motor, one for the trigger servo, one for the thermal camera, and one for high level control of system operations and delegation to other tasks. This last task, "mastermind," handles all major logic and flow of operations of the blaster apparatus. The other 4 tasks represent no high-level logic, instead relying on flags/instructions such as set point to rotate to, whether or not it should fire, and whether or not to take an image. This approach was chosen to keep logic and system flow clear, simple, and centralized. It also minimized variables that needed to be shared between tasks, other than to mastermind. Inter-task data was handled with share variables, 6 of which were implemented to handle pitch/yaw angles of target as seen by camera, pitch/yaw angles to rotate to by motors, fire flag, and flag to take image.

In terms of duel sequencing, a 5 second timer was used after user button is pressed to wait until after the period in which each team may freely move behind their table. Due to the high latency of the thermal camera (1-2 Hz) we did not attempt to shoot while the target was moving. After this 5 seconds, the camera is queued to take an image, and after the motors are given to align with the new target, the trigger flag is raised to fire.

Within each motor task, 3 drivers classes are instiated for the encoder driver, motor driver, and position feedback control. The encoder_reader.py driver implements a class to read and manage the position of a quadrature encoder. It detects underflow/overflow conditions of the 16 bit counter and calculates the position delta. The motor_driver.py driver works by changing the direciton and duty cycle for a BDC motor based on a signed PWM duty cycle passed to it. The feedback_control.py file implments a closed feedback controller to control position of the motor based on the aforementioned encoder and motor objects. It can use any combination of P/I/D control.

# Testing and Results
Significant time was allocated for full-system integration to ensure proper operation before the duels. Yaw motor function worked relatively smoothly from the start, though there were fundamental issues with the pitch control. Due to the convenience of a mounting rail on the upper rear section of the Nerf blaster, we mounted the Nerf blaster with an asymmetric inertial distribution about its pitch axis. Estimates from CAD found online and rough estimations of center of mass suggested that we would have an appropriate amount of torque for pitch actuation. In the hardware iteration phase, however, the pitch gear ratio had to be reduced to properly fit the drive belt in the absense of a tensioning pulley. This resulted in a condition where if the blaster fell completely forwards, the pitch motor was not strong enough to pull it back up. Due to the accelerated timeline of this project set by the class, we did not have time to order a different blaster or change the drive system to have a higher torque. We also realized that pitch actuation mattered very little, as if a pitch was set that sent a dart about 1 foot above the opponents side of the table, it would always be vertically centered on their bodies. Therefore, we simplified the system by reducing control of the pitch axis to not actuate during the duel.

Another setback occured in the early implementation of the trigger servo. Since there wasn't time to implement a custom PCB with different power levels, we only had 12V from the power supply for the DC motors and the 3V3 and 5V lines of the Nucleo development board. We attempted to power the servo off this line since it was only predicted to need 100-200 mA, but ultimately it required more power than the board was able to supply. This resulted in reset conditions beign triggered in the MCU and led to issues with the trigger task's integration. We fixed this by using a second power supply.



# Lessons Learned

- Rigidity tests (issues with yaw motion causing vibration)
- Needed higher gear ratio for pitch control
- order backup critical components ahead of time


Worked well: lightweight design, quick motion, simplified and centralized logic, allow plenty of time for full system integration

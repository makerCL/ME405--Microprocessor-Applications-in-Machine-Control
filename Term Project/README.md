
# Introduction

The purpose of this project was to create a "Nerf" launcher system that detects, tracks and launches a nerf projectile autonomously for competition in the Cal Poly ME 405 dueling day.

On the dueling day, teams compete by placing their launchers on opposite sides of a table and pointing 180 degrees away from eachother. This competition requres participants to use a thermal camera and at least one brushed DC motor with an incremental encoder which are provided to each team.On the start signal, lanuchers can be activated and there is a 5 second period where the opposing participants can move around. After 5 seconds, participants must freeze. The scoring system is such that the first hit recieves +3 points, the second team's first hit recieves +1 point, either teams second hit recieves 0 points and a miss revieces -1 points. This scoring system incentives speed (first hit) and reliability (misses recieve negative points).

# Hardware Design

Custom hardware was designed to interface with an off the shelf 'Nerf Elite 2.0 Blaster,' two brushed DC motors with incremental encoders used for yaw and pitch position control and a servo motor used to actuate the trigger mechanism.

Several design concepts were considered including creating our own dart shooting system with compressed air and selecting a more complex 'Nerf' gun (Nerf Ultra Select) which uses a flywheel to shoot darts and can be electrically actuated. However, we identified concerns with the high mass of these components and inconsistent firing of the flywheel. Based on the competition rules and scoring system, it was determined that a simple, lightweight, single shot blaster actuated by a compressed spring would be able to achieve the speed needed to move quickly and hit our opponents first and the reliability to always fire as expected.

An image of our CAD model interfaced with the DC motors and 'Nerf' gun can be referenced in the figure below.

![](CAD_Isometricview.png)

## Yaw Control
The yaw angle of the hardware was controlled via the brushed DC motor with an incremental encoder connected to a gear hard mounted to the table with a 1:8 gear ratio. The system is designed so that the yaw gear is stationary and the entire gun assembly rotates freely above the large yaw gear. This rotation is achieved by a bearing that is press-fit to both the main rotating bracket and a protruding stub from the main yaw gear. An exploded section view of this bearing assembly is shown below for reference.

![](Yaw_SectionView.png)

## Pitch Control

The pitch angle of the 'Nerf' blaster is achieved by controlling the position of a second brushed DC motor with an incremental encoder. The nerf blaster assembly is rigidly attached to a shaft that is held in place by bearing(s) on either side. The rotation of this shaft is connected to a belt and pulley system which couples the DC motor rotation to the shaft rotation with a 1:1.5 gear ratio. A section view of the pitch control system is shown in the image below. Note: Belt not modeled but connects the pitch motor to the rotating shaft pulley.

![](Pitch_SectionView.png)

## Trigger Mechanism

The blaster trigger was actuated by a medium torque (20 kg-cm) servo motor. This motor was selected as testing of the Nerf Elite 2.0 determined that approximately 30 N of force was required to actuate the trigger. An image of the trigger servo motor mounted to the blaster assembly can be referenced in the figure below.

## Camera Mount and Placement

- Miles discuss reasons for placing the camera off the rotating components

# Software Design


# Testing and Results


# Lessons Learned

- Rigidity tests (issues with yaw motion causing vibration)
- Needed higher gear ratio for pitch control

Worked well: lightweight design, quick motion

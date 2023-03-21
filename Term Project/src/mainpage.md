@author Caleb Erlenborn
@author Miles Alderman
@date March 20, 2023


The software was designed to implement cooperative multi-tasking with five tasks as described in the task share diagram and finite state machines below. All high level processing, timing and intertask communication was handeled through the task 'mastermind' which was used to send encoder position set points to two motor tasks controlling both the yaw and pitch motors, respectively. 


# Section 1

A task diagram for our term project design can be referenced below.

![Figure 1](/TASK_Diagram.jpg)

A finite state machine for the first task (Read_Camera) can be referenced below.

![](/Camera_FSM.jpg)

A finite state machine to perform position control on each DC motor can be referenced below.

![](/Motor_Controller_FSM.PNG)

Finally a FSM for the trigger actuation system can be referenced below.

![](/Trigger_Actuation_FSM.PNG)
'''!
@section Software_Design Our software design currently implements 4 tasks as seperate finite state machines. Each task is outlined as subsections  below. Finite State Machines can be referenced in the README.md

@subsection Task_1 Read_Camera, Our first task reads the thermal camera and post-processes the image to determine the optimal location to fire.

@subsection Task_2 Yaw_Motor_Control, This task controls the yaw motor to the optimal position determined by the Read_Camera task

@subsection Task_3 Pitch_Motor_Control, This task controls the pitch motor to the optimal position determined by the Read_Camera task

@subsection Task_4 Trigger_Actuation, This task actuates the trigger when it is determined that the camera is pointed in the optimal direction
'''
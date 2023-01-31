'''


'''


class FeedbackControl:
    '''
    @param k_p
    @param setpoint
    @param time_step- in seconds
    '''
    def __init__(self, setpoint, k_p = 1, time_step = 0.1):
        self.k_p = k_p
        self.setpoint = setpoint
        self.time_step = time_step

    def run(self, current_theta):
        pass

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

#### TEST CODE #############################

if __name__ == '__main__':
    pass
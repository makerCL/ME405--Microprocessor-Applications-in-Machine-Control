'''


'''


class FeedbackControl:
    '''
    @param k_p
    @param setpoint
    @param time_step- in seconds
    '''
    def __init__(self, setpoint = 0, k_p = 0):
        self.k_p = k_p
        self.setpoint = setpoint

    def run(self, current_theta):
        pass

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

#### TEST CODE #############################

if __name__ == '__main__':
    pass
### TESTING, NOT IMPLEMENTED IN PROJECT

'''
from array import *
import numpy as np

width = 32
height = 24
arr = array('f', [-10.03338, -12.1083, -9.257389, -19.88462, -13.66068, -18.79534, -10.24189, -23.82467, -11.89964, -21.85465, -9.361126, -25.01823, -13.09368, -20.30172, -9.674435, -23.46642, -19.05032, -16.98613, -11.22742, -19.26891, -16.61665, -17.09038, -13.19744, -19.16528, -13.45351, -17.19525, -10.24291, -15.74655, -11.90061, -11.91076, -7.39267, -14.61137, -10.09074, -17.35887, -18.95645, -18.05596, -14.4951, -23.12499, -18.17933, -20.31448, -14.80788, -23.12554, -20.04511, -22.2845, -15.89774, -27.35412, -19.16558, -23.846, -19.10739, -20.47995, -19.94205, -16.97243, -17.45069, -18.94178, -17.97144, -16.97243, -14.28711, -19.78351, -18.85278, -14.44928, -12.73473, -16.56327, -15.01759, -12.79068, -12.78039, -13.19757, -12.10817, -20.97391, -15.63071, -17.13762, -14.07769, -25.89898, -15.83969, -22.94394, -14.95943, -26.98826, -18.79522, -25.12251, -13.40649, -24.45143, -20.81181, -18.076, -14.18296, -19.26954, -14.75089, -16.41813, -14.07869, -22.12032, -12.46805, -16.3145, -13.87015, -17.71657, -11.79633, -13.77718, -7.39267, -15.59639, -10.09134, -15.38884, -14.44778, -19.3289, -14.59936, -24.11056, -19.0601, -22.2845, -15.79347, -26.08058, -23.67358, -22.2845, -17.7635, -27.2107, -22.22489, -21.87659, -17.24215, -17.95676, -15.53769, -15.43359, -16.77848, -16.4186, -18.18057, -17.26035, -14.39191, -18.1014, -20.71911, -13.75218, -10.86956, -15.72294, -15.22554, -9.979622, -6.301838, -10.45106, -11.33168, -20.19693, -11.89964, -16.15312, -10.45092, -25.89898, -13.09368, -22.0632, -15.06371, -26.98877, -14.95943, -22.27229, -10.66, -24.55517, -15.63117, -14.55301, -13.51077, -16.83582, -12.10867, -13.77652, -11.54074, -20.56735, -10.91511, -14.55301, -13.19847, -16.94008, -12.10917, -10.25352, -6.720501, -11.86565, -12.94212, -19.76078, -19.26923, -20.45846, -16.56939, -20.60183, -22.68856, -22.42848, -14.80846, -25.38352, -22.8971, -25.52807, -15.12127, -24.97501, -17.61198, -20.48188, -17.45069, -15.57754, -17.71691, -13.89615, -13.92771, -14.88117, -21.03195, -16.56327, -11.64543, -16.70722, -18.18057, -11.37299, -9.316071, -11.51773, -11.70256, -8.729454, -8.689423, -13.61518, -7.704411, -17.55523, -16.8247, -17.45095, -10.55519, -23.25676, -10.45092, -19.42098, -12.52521, -25.43589, -15.48079, -19.73438, -8.017193, -22.12154, -18.37813, -16.21024, -14.28724, -17.50805, -17.39312, -15.32949, -15.06371, -23.10532, -15.42309, -19.16528, -13.97442, -19.58299, -15.84066, -13.88078, -10.24291, -14.61137, -11.59764, -17.38223, -17.50772, -16.10927, -17.09068, -23.8454, -21.44777, -20.04933, -11.59764, -22.01997, -21.44777, -24.13398, -17.4041, -23.29294, -17.92476, -19.92949, -21.39074, -20.35935, -22.22489, -15.72221, -14.80846, -17.54827, -21.13561, -15.57825, -13.71917, -18.38932, -20.92767, -13.0551, -13.9283, -16.01088, -16.21055, -11.25258, -5.838642, -9.002937, -8.017193, -16.10598, -9.465912, -11.07664, -7.032181, -18.0766, -9.674988, -17.86806, -9.002789, -22.01665, -9.106468, -16.21085, -5.583466, -17.7179, -17.8102, -13.77652, -9.987804, -12.32781, -13.19795, -10.14926, -10.76427, -14.19358, -12.00489, -13.98505, -12.52575, -13.52209, -10.55627, -11.44779, -4.958466, -13.26699, -13.46341, -19.06369, -20.46275, -21.87477, -17.86718, -24.68585, -21.44712, -23.70084, -17.09068, -29.46754, -22.32852, -26.65648, -19.16558, -26.80044, -21.55203, -22.45191, -21.59871, -19.37434, -20.4634, -14.04012, -16.88275, -17.69224, -22.32916, -17.54827, -15.58494, -24.15544, -23.00137, -16.01014, -15.89832, -17.8362, -19.06131, -16.8739, 1.416512, -7.241459, -4.389313, -14.91302, -8.793118, -14.91302, -8.121452, -20.71882, -5.942909, -17.6595, -11.85299, -22.68884, -7.704964, -18.85307, -12.06151, -22.2252, -14.95894, -18.38879, -13.61449, -19.58233, -15.94396, -17.50805, -15.27173, -23.20959, -18.48195, -21.1353, -19.8845, -19.58233, -19.46786, -16.62795, -15.84018, -21.29792, -12.37413, -21.03372, -22.22363, -22.86039, -19.94086, -22.85978, -27.04507, -24.68585, -19.73294, -28.33856, -30.67234, -30.30858, -16.10567, -26.9438, -23.41779, -23.72422, -15.12066, -19.10914, -20.77553, -13.63094, -14.34417, -18.12412, -22.43279, -17.69224, -19.52498, -22.47334, -25.95641, -18.12412, -16.98702, -19.10914, -21.13561, -17.01787, -14.49524, -11.74887, -12.52467, -18.54024, -12.21191, -14.59964, -15.37599, -24.3455, -13.97393, -23.15249, -19.00325, -27.09254, -14.28671, -19.62897, 0.07143402, -8.33075, 5.41354, 1.566631, -7.13644, -12.53634, -13.51023, -14.19358, -14.70376, -19.79086, -18.69094, -17.71657, -18.22729, -21.08866, -17.138, -13.20856, -12.42148, -14.81916, -14.19322, -18.24537, -19.11758, -18.10209, -12.89475, -21.05644, -20.98405, -19.92747, -14.65694, -23.58025, -25.59633, -21.61023, -12.99969, -20.21539, -0.6115646, 21.41961, 16.55069, 11.25957, -6.834412, -4.93251, -12.2232, -13.36575, -18.34179, -16.8739, -16.41908, -16.72995, -21.86549, -13.36575, -10.92608, -11.39571, -14.08966, -10.28947, -13.51023, -11.74887, -15.47971, -20.51027, -15.16695, -17.55468, -13.40596, -21.39047, -16.92897, -24.1375, -19.98827, -28.07755, -14.28671, -14.70391, 27.65179, 30.08475, 32.9939, 24.22192, 15.51885, 4.208878, -15.48025, -16.1636, -17.6588, -22.7459, -20.66097, -17.71657, -20.19732, -18.13363, -15.16798, -11.23854, -14.39151, -17.7742, -36.21025, -16.00865, 3.361252, -26.24543, 5.187073, -23.57763, -33.52427, -30.16233, -5.17717, -44.05451, -1.815979, -42.08139, -10.14961, -27.32973, 12.61339, 11.32711, 25.05698, 12.00211, 16.34288, 2.561142, -15.74554, -23.04919, -24.04264, -23.04919, -19.2686, -21.07916, -19.11758, -17.71496, -11.80549, -17.71496, -16.16254, -15.91161, -12.52467, -11.95739, -15.47971, -17.86747, -17.03273, -15.89744, -17.44973, -23.77755, -17.03273, -15.89744, -14.49469, -21.80752, -15.0627, -13.92742, 23.92081, 20.13097, 38.545, 36.30823, 20.96577, 2.400742, -18.01774, -19.26954, -20.40477, -27.14964, -20.55577, -20.25455, -18.43475, -22.64164, -18.01774, -16.73156, -15.47971, -18.55068, -16.16254, -18.53329, -24.04264, -19.5183, -21.65562, -22.47334, -28.9677, -22.47334, -19.68559, -22.47334, -23.05763, -22.47334, -19.68559, -22.47334, 1.567696, 31.12651, 40.81718, 38.59745, 16.34288, -9.25901, -16.73055, -24.0342, -25.02765, -23.04919, -19.2686, -23.04919, -20.10258, -18.69997, -17.71557, -17.71496, -19.11758, -18.86665, -10.40364, -5.89642, -11.38866, -13.77652, -16.88173, -10.82148, -13.35868, -18.70158, -15.89671, -14.76153, -15.32871, -21.65662, -14.9117, -15.74655, 4.371548, 4.521667, 48.54612, 49.2643, 19.14674, 3.536655, -11.95666, -10.25352, -12.37367, -19.11864, -15.47971, -11.23854, -12.37367, -12.64061, -12.94168, -10.67059, -9.418633, -14.45973, -16.01151, -16.72995, -23.89162, -16.72995, -19.53457, -21.65501, -21.92159, -16.72995, -18.54955, -21.65501, -24.87663, -20.67, -21.50459, -20.67, -10.10144, 21.1097, 41.95322, 32.52069, 17.47892, 11.25957, 9.0308, -4.500626, -16.99653, -16.32078, -15.17752, -15.33577, -17.98154, -13.94159, -12.63948, -13.94159, -14.04149, -10.16822, -20.25377, -6.881428, -16.31372, -15.74655, -20.82177, -12.79151, -16.31372, -19.6866, -20.82177, -15.74655, -15.32871, -20.67161, 1.833519, 0.01366043, 17.17672, 12.40177, 12.10065, 15.77386, 22.10178, 15.35681, 16.60871, 14.3718, 5.356564, -3.358433, -18.43475, -15.17859, -14.3437, -17.56567, -16.88173, -11.65559, -10.40364, -14.45973, -16.84551, -13.94159, -21.77057, -12.95657, -18.39854, -18.86665, -20.78555, -15.91161, -18.39854, -22.8067, -19.80054, -4.091461, 4.25676, 9.698715, 12.70488, 17.98798, 12.55386, 10.68373, 11.71986, 18.973, 18.04694, 15.03294, 13.68989, 1.242767, -9.116425, -15.50245, -14.87548, -9.183205, -7.563393, -11.15323, -11.92044, -7.379868, -8.282612, -0.8204575, -11.23765, -10.67059, -14.7607, -6.73053, -12.22267, -15.59565, -14.7607, -10.67059, 3.53754, -3.775497, 20.69977, 20.84983, 17.32772, 14.52269, 19.14674, 20.84983, 17.32772, 12.55267, 15.7747, 19.44776, 23.2378, 15.50771, -11.38866, -4.192551, -12.22267, -14.45973, -12.79067, -6.579636, -11.23765, -10.36878, -19.64952, -18.04832, -27.52962, -20.01835, -21.20255, -23.9584, -29.49965, -21.98837, -24.15759, -21.98837, -21.61955, 7.562012, 16.22794, 8.54702, 4.9758, 6.001152, 8.764832, 4.606972, 3.990784, 6.98616, 9.332848, 11.91122, 13.84091, 11.91122, -4.040337, -16.65414, -21.61955, -17.23, -16.27749, -16.24499, -16.69448, -13.45663])
np_arr = np.array(arr).astype(np.int8).reshape(height, width).round()

scale = 255 / (np.amax(np_arr) - np.amin(np_arr))
offset = 0.0

np_arr = np_arr * scale
'''

import numpy as np
import inspect

print(inspect.getmodule(np.array))
print(inspect.getmodule(np.int8))
print(inspect.getmodule(np.reshape))
print(inspect.getmodule(np.round))
print(inspect.getmodule(np.amax))
print(inspect.getmodule(np.amin))
print(inspect.getmodule(np.where))
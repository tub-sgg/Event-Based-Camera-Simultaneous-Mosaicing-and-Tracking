import os

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import sample.helpers.coordinate_transforms as coordinate_transforms
import sample.helpers as helpers
from sample.tracking import tracking as track


def compare_trajectories_2d(intensity_map, poses, event0):
    '''

    :param intensity_map:
    :param poses:
    :param event0:
    :return: plot with intensity map and ground truth trajectory
    '''
    poses_converted = pd.DataFrame(columns=
                          ['Rotation', 'Weight', 'theta',
                           'phi', 'v', 'u', 'pol',
                           'p_w1', 'p_w2', 'p_w3',
                           'z', 'logintensity_ttc',
                           'logintensity_t'])
    poses_converted['Rotation'] = poses['Rotation']
    poses_converted['Rotation'].astype('object')
    tracker = track.Tracker()
    calibration = tracker.camera_intrinsics()
    calibration_inv = np.linalg.inv(calibration)

    print(poses_converted['phi'])
    for idx, event in event0.iterrows():
        angles = tracker.event_and_particles_to_angles(event, poses_converted, calibration_inv)
        continue

    plt.figure()
    plt.imshow(intensity_map)
    plt.show()





def compare_trajectories_2d(fourevents, poses_ours, poses_gt, intensity_map):
    '''

    :param intensity_map:
    :param poses_gt:
    :param event0:
    :return: plot with intensity map and ground truth trajectory
    '''
    poses_converted = pd.DataFrame(columns=
                          ['Rotation', 'Weight', 'theta',
                           'phi', 'v', 'u', 'pol',
                           'p_w1', 'p_w2', 'p_w3',
                           'z', 'logintensity_ttc',
                           'logintensity_t'])
    poses_converted['Rotation'] = poses_gt['Rotation']
    poses_converted_ours = pd.DataFrame(columns=
                                   ['Rotation', 'Weight', 'theta',
                                    'phi', 'v', 'u', 'pol',
                                    'p_w1', 'p_w2', 'p_w3',
                                    'z', 'logintensity_ttc',
                                    'logintensity_t'])
    poses_converted_ours['Rotation'] = poses_ours['Rotation']
    poses_converted['Rotation'].astype('object')
    tracker = track.Tracker()
    calibration = tracker.camera_intrinsics()
    calibration_inv = np.linalg.inv(calibration)
    # print(calibration)
    # print(calibration_inv)


    angles = []
    mappoints = []
    for i in range(5):
        angle = tracker.event_and_particles_to_angles(fourevents.loc[i], poses_converted, calibration_inv)
        angles.append(angle.copy())
        mappoint = tracker.angles2map_df(angle)
        mappoints.append(mappoint.copy())


    plt.figure(1)
    plt.plot(angles[0]['theta'], angles[0]['phi'], 'b.', label='0')
    plt.plot(angles[1]['theta'], angles[1]['phi'], 'r.', label='1')
    plt.plot(angles[2]['theta'], angles[2]['phi'], 'g.', label='2')
    plt.plot(angles[3]['theta'], angles[3]['phi'], 'y.', label='3')
    plt.plot(angles[4]['theta'], angles[4]['phi'], 'k.', label='c')


    # plt.plot(angles_ours['theta'], angles_ours['phi'], 'r.')
    plt.xlabel('theta')
    plt.ylabel('phi')
    plt.legend()
    plt.xlim([-np.pi, np.pi])
    plt.ylim([-np.pi/2, np.pi/2])


    # plt.imshow(intensity_map)
    # plt.show()
    plt.figure(2)
    # plt.figure(3)
    # intensity_map = np.load('../output/intensity_map.npy')
    plt.imshow(intensity_map)

    # plt.plot(mappoints[0]['u'], mappoints[0]['v'], 'b.', label='0')
    # plt.plot(mappoints[1]['u'], mappoints[1]['v'], 'r.', label='1')
    # plt.plot(mappoints[2]['u'], mappoints[2]['v'], 'g.', label='2')
    # plt.plot(mappoints[3]['u'], mappoints[3]['v'], 'y.', label='3')
    plt.scatter(mappoints[4]['u'], mappoints[4]['v'], color='r', s=2, label='ground truth')

    angles = []
    mappoints = []
    for i in range(5):
        angle = tracker.event_and_particles_to_angles(fourevents.loc[i], poses_converted_ours, calibration_inv)
        angles.append(angle.copy())
        mappoint = tracker.angles2map_df(angle)
        mappoints.append(mappoint.copy())


    # plt.plot(mappoints[0]['u'], mappoints[0]['v'], 'b.', label='0')
    # plt.plot(mappoints[1]['u'], mappoints[1]['v'], 'r.', label='1')
    # plt.plot(mappoints[2]['u'], mappoints[2]['v'], 'g.', label='2')
    # plt.plot(mappoints[3]['u'], mappoints[3]['v'], 'y.', label='3')
    plt.scatter(mappoints[4]['u'], mappoints[4]['v'], color='y', s=2, label='tracker')


    # plt.plot(angles_ours['theta'], angles_ours['phi'], 'r.')
    plt.xlabel('u')
    plt.ylabel('v')
    plt.legend()
    plt.xlim([0+700, 2047-700])
    plt.ylim([1023-300, 0+300])






    plt.show()



def compare_trajectories(df_groundtruth, **kwargs):
    """
    :return: function checks whether the rotation matrices are really randomly distributed. muoltiplies rot matrix with Z-unit-vector. returns plotly and matplotlib plot which shows the distribution

    Function checks whether the rotation matrices are really randomly distributed.
    multiplies rot matrix with Z-unit-vector.
    :return: plotly and matplotlib plot which shows the distribution
    """
    # vec = np.array([1,0,0]).T
    vec = np.array([np.sqrt(1 / 3), np.sqrt(1 / 3), np.sqrt(1 / 3)]).T

    vecM_theirs = df_groundtruth['Rotation'].apply(lambda x: np.dot(x, vec))
    rotX_theirs= vecM_theirs.str.get(0)
    rotY_theirs = vecM_theirs.str.get(1)
    rotZ_theirs = vecM_theirs.str.get(2)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)

    q = ax.scatter(rotX_theirs, rotY_theirs, rotZ_theirs, s=1, color='r', label="Ground truth")
    ax.scatter(rotX_theirs[0], rotY_theirs[0], rotZ_theirs[0], s=10, color = 'm', marker = 'D')

    colormaps = ['spring', 'summer', 'autumn', 'bone']
    i=0
    for key, df in kwargs.items():
        print(key)
        print(colormaps[i])
        # the_file.write("{0}: {1}\n".format(key, value))

        vecM = df['Rotation'].apply(lambda x: np.dot(x, vec))
        rotX = vecM.str.get(0)
        rotY = vecM.str.get(1)
        rotZ = vecM.str.get(2)

        p = ax.scatter(rotX, rotY, rotZ, c=range(len(rotZ)), s=2, label=key, cmap=colormaps[i])

        # cbar = fig.colorbar(p, ax=ax)
        i+=1

    plt.legend()
    # cbar2 = fig.colorbar(q, ax=ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # cbar.set_label("Nr. of pose")
    plt.show()

def cut_df_wrt_time(rotations_ours, rotations_theirs):
    t_max = rotations_ours['t'].max()
    rotations_theirs_cut = rotations_theirs[rotations_theirs['t'] < t_max]

    return rotations_theirs_cut

def visualize_rotmats(rotation_matrices):
    vec = np.array([np.sqrt(1 / 3), np.sqrt(1 / 3), np.sqrt(1 / 3)]).T
    # vec = np.array([0, 0, 1]).T

    rotX = []
    rotY = []
    rotZ = []
    for rotmat in rotation_matrices:
        vecM = np.dot(vec, rotmat)
        rotX.append(vecM[0])
        rotY.append(vecM[1])
        rotZ.append(vecM[2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)
    p = ax.scatter(rotX, rotY, rotZ, c='b')
    p = ax.scatter(rotX[0], rotY[0], rotZ[0], c='r', s=200)

    # cbar = fig.colorbar(p, ax=ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # cbar.set_label("Nr. of pose")
    # return ax
    plt.show()


def visualize_particles(rotation_matrices, mean_value = None):
    """
    :return: function checks whether the rotation matrices are really randomly distributed. muoltiplies rot matrix with Z-unit-vector. returns plotly and matplotlib plot which shows the distribution

    Function checks whether the rotation matrices are really randomly distributed.
    multiplies rot matrix with Z-unit-vector.
    :return: plotly and matplotlib plot which shows the distribution
    """

    # vec = np.array([1,0,0]).T
    vec = np.array([np.sqrt(1 / 3), np.sqrt(1 / 3), np.sqrt(1 / 3)]).T
    # vec = np.array([0, 0, 1]).T

    print(rotation_matrices)
    exit()
    vecM = rotation_matrices.apply(lambda x: np.dot(x, vec))
    rotX = vecM.str.get(0)
    rotY = vecM.str.get(1)
    rotZ = vecM.str.get(2)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)
    p = ax.scatter(rotX, rotY, rotZ, c=range(len(rotZ)))
    if mean_value is not None:
        mean_vec = np.dot(mean_value, vec)
        q = ax.scatter3D(mean_vec[0],mean_vec[1],mean_vec[2], 'b')
    cbar = fig.colorbar(p, ax=ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    cbar.set_label("Nr. of pose")

    plt.show()


def plot_unitsphere_matplot():
    r = 1
    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0 * pi:100j]
    x = r * sin(phi) * cos(theta)
    y = r * sin(phi) * sin(theta)
    z = r * cos(phi)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot_surface(
        x, y, z, rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)
    plt.show()


if __name__ == '__main__':
    ##Loading Camera poses
    # data_dir = '../data/Datasets/BigRoom/2019-04-29-17-20-59'
    # print("Loading Camera Orientations")
    # filename_poses = os.path.join(data_dir, 'imu.txt')
    # poses = helpers.load_poses_angvel(filename_poses=filename_poses)
    #
    # # poses = pd.read_csv(filename_events, delimiter=' ', header=None, names=['time', 'x', 'y', 'qx', 'qy', 'qz', 'qw'])
    # num_poses = poses.size
    # print("Number of poses in file: ", num_poses)
    #
    # # print(first_event)
    # # poses['t'] = poses['time'] - poses['time'].loc[0]
    # # poses = poses[['t', 'qw', 'qx', 'qy', 'qz']] # Quaternions
    # print("Head: \n", poses.head(10))
    # print("Tail: \n", poses.tail(10))
    #
    # # Convert quaternions to rotation matrices and save in a dictionary TODO: UGLY AS HELL!!
    # rotmats = coordinate_transforms.angvel2R_df(poses)
    # print(rotmats)
    #
    # compare_trajectories(rotmats,
    #                      #onlymotionupdate=rotations_onlymotionupdate,
    #                      rotations_ours=rotmats)#,
    #
    # exit()














    directory_poses = '../output/poses/'
    data_dir = '../data/synth1'
    intensity_map = np.load('../output/intensity_map2.npy')
    event_file = os.path.join(data_dir, 'events.txt')
    events = helpers.load_events(filename=event_file, davis=False, head=4)
    print(events)

    events_gen = helpers.generate_events()
    print(events_gen)





    # poses_onlymotionupdate = helpers.load_poses(filename_poses=os.path.join(directory_poses, 'quaternions_16052019T082453_.txt'))
    # rotations_ours = coordinate_transforms.q2R_df(poses_onlymotionupdate)




    filename_groundtruth = 'poses.txt'
    filename_onlymotionupdate = 'quaternions_11052019T150554_onlymotionupdate.txt'
    filename_ours = 'quaternions_23052019T215921.txt'

    # filename_likelihoodTrue = 'quaternions_14052019T091627_50deg_True_1000particles.txt'
    # filename_likelihoodTruessmall = 'quaternions_13052019T191609_20deg_True_sx0p0002.txt'
    # filename_likelihoodTruessmall = 'quaternions_16052019T082453_.txt'

    poses_groundtruth = helpers.load_poses(filename_poses=os.path.join(directory_poses, filename_groundtruth), includes_translations=True)
    poses_onlymotionupdate = helpers.load_poses(filename_poses=os.path.join(directory_poses, filename_onlymotionupdate))
    poses_ours = helpers.load_poses(filename_poses=os.path.join(directory_poses, filename_ours))
    # poses_likelihoodTrue = helpers.load_poses(filename_poses=os.path.join(directory_poses, filename_likelihoodTrue))
    # poses_likelihoodTruessmall = helpers.load_poses(filename_poses=os.path.join(directory_poses, filename_likelihoodTruessmall))

    # print(poses_groundtruth.head())
    # print(poses_onlymotionupdate.head())


    rotations_groundtruth = coordinate_transforms.q2R_df(poses_groundtruth)
    rotations_onlymotionupdate = coordinate_transforms.q2R_df(poses_onlymotionupdate)
    rotations_ours = coordinate_transforms.q2R_df(poses_ours)
    rotations_groundtruth_cut = cut_df_wrt_time(rotations_ours, rotations_groundtruth)

    # rotations_likelihoodTrue = coordinate_transforms.q2R_df(pose                  s_likelihoodTrue)
    # rotations_likelihoodTruessmall = coordinate_transforms.q2R_df(poses_likelihoodTruessmall)

    compare_trajectories_2d(events_gen, rotations_ours, rotations_groundtruth_cut, intensity_map)

    # exit()
    compare_trajectories(rotations_groundtruth_cut,
                         #onlymotionupdate=rotations_onlymotionupdate,
                         rotations_ours=rotations_ours)#,
                         # likelihoodFlippedTrue=rotations_likelihoodTrue,
                         # likelihoodFlippedTruessmall=rotations_likelihoodTruessmall)
# '''
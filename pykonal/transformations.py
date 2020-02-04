"""
A module to facilitate coordinate-system transformations.
"""

import numpy as np


def sph2sph(nodes, origin):
    """
    Transform spherical coordinates to new spherical coordinate system.

    :param nodes: Coordinates (spherical) to transform.
    :type nodes: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    :param origin: Coordinates (spherical) of the origin of the new
                   coordinate system with respect to the old coordinate
                   system.
    :type origin: tuple(float, float, float)
    :return: Coordinates in new (spherical) coordinate system.
    :rtype: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    """

    xx = nodes[...,0] * np.sin(nodes[...,1]) * np.cos(nodes[...,2])
    yy = nodes[...,0] * np.sin(nodes[...,1]) * np.sin(nodes[...,2])
    zz = nodes[...,0] * np.cos(nodes[...,1])
    x0 = origin[0] * np.sin(origin[1]) * np.cos(origin[2])
    y0 = origin[0] * np.sin(origin[1]) * np.sin(origin[2])
    z0 = origin[0] * np.cos(origin[1])
    xx -= x0
    yy -= y0
    zz -= z0
    xyz = np.moveaxis(np.stack([xx, yy, zz]), 0, -1)
    rr  = np.sqrt(np.sum(np.square(xyz), axis=-1))
    old = np.seterr(divide='ignore', invalid='ignore')
    tt  = np.arccos(xyz[...,2] / rr)
    np.seterr(**old)
    pp  = np.arctan2(xyz[...,1], xyz[...,0])
    rtp = np.moveaxis(np.stack([rr, tt, pp]), 0, -1)
    return (rtp)


def xyz2sph(nodes, origin):
    """
    Transform Cartesian coordinates to new spherical coordinate system.

    :param nodes: Coordinates (Cartesian) to transform.
    :type nodes: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    :param origin: Coordinates (Cartesian) of the origin of the new
                   coordinate system with respect to the old coordinate
                   system.
    :type origin: tuple(float, float, float)
    :return: Coordinates in new (spherical) coordinate system.
    :rtype: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    """
    xyz = nodes - origin
    rr  = np.sqrt(np.sum(np.square(xyz), axis=-1))
    old = np.seterr(divide='ignore', invalid='ignore')
    tt  = np.arccos(xyz[...,2] / rr)
    np.seterr(**old)
    pp  = np.arctan2(xyz[...,1], xyz[...,0])
    rtp = np.moveaxis(np.stack([rr, tt, pp]), 0, -1)
    return (rtp)


def sph2xyz(nodes, origin):
    """
    Transform spherical coordinates to new Cartesian coordinate system.

    :param nodes: Coordinates (spherical) to transform.
    :type nodes: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    :param origin: Coordinates (spherical) of the origin of the new
                   coordinate system with respect to the old coordinate
                   system.
    :type origin: tuple(float, float, float)
    :return: Coordinates in new (Cartesian) coordinate system.
    :rtype: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    """
    xx  = nodes[...,0] * np.sin(nodes[...,1]) * np.cos(nodes[...,2])
    yy  = nodes[...,0] * np.sin(nodes[...,1]) * np.sin(nodes[...,2])
    zz  = nodes[...,0] * np.cos(nodes[...,1])
    origin = [
        origin[0] * np.sin(origin[1]) * np.cos(origin[2]),
        origin[0] * np.sin(origin[1]) * np.sin(origin[2]),
        origin[0] * np.cos(origin[1])
    ]
    xx -= origin[0]
    yy -= origin[1]
    zz -= origin[2]
    xyz = np.moveaxis(np.stack([xx, yy, zz]), 0, -1)
    return (xyz)


def xyz2xyz(nodes, origin):
    """
    Transform Cartesian coordinates to new Cartesian coordinate system.

    :param nodes: Coordinates (Cartesian) to transform.
    :type nodes: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    :param origin: Coordinates (Cartesian) of the origin of the new
                   coordinate system with respect to the old coordinate
                   system.
    :type origin: tuple(float, float, float)
    :return: Coordinates in new (Cartesian) coordinate system.
    :rtype: numpy.ndarray(shape=(...,3), dtype=numpy.float)
    """
    return (nodes - origin)


def rotation_matrix(alpha, beta, gamma):
    """
    Rotation matrix used to rotate a set of cartesian coordinates.

    The rotation matrix is defined such that coordinates are rotated by
    alpha radians about the z-axis, then beta radians about the y'-axis
    and then gamma radians about the z''-axis.

    :param alpha: Angle to rotate about the z-axis.
    :type alpha: float
    :param beta: Angle to rotate about the y'-axis.
    :type beta: float
    :param gamma: Angle to rotate about the z''-axis.
    :type gamma: float
    :return: Rotation matrix.
    :rtype: numpy.ndarray(shape=(3,3), dtype=numpy.float)
    """
    aa = np.array(
        [
            [np.cos(alpha), -np.sin(alpha), 0           ],
            [np.sin(alpha),  np.cos(alpha), 0           ],
            [0,              0,             1           ]
        ]
    )
    bb = np.array(
        [
            [ np.cos(beta), 0,              np.sin(beta)],
            [ 0,            1,              0           ],
            [-np.sin(beta), 0,              np.cos(beta)]
        ]
    )
    cc = np.array(
        [
            [np.cos(gamma), -np.sin(gamma), 0           ],
            [np.sin(gamma),  np.cos(gamma), 0           ],
            [0,              0,             1           ]
        ]
    )
    return (aa.dot(bb).dot(cc))

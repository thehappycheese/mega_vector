import numpy as np
import plotly.graph_objects as go
from typing import Optional
from ._Vector3 import Vector3

def trace_Vector3_list(vectors:list[Vector3]):
    coords = np.array([
        np.array(vector) for vector in vectors
    ])
    origins = np.zeros_like(coords)
    blanks = origins * np.nan
    blanks[:,0]=0
    lines = np.concatenate(
        [
            origins,
            coords,
            blanks
        ],
        axis = 1
    ).reshape((-1,3))
    return lines.transpose()


def mesh_arrow(
        tip            : Vector3,
        base           : Optional[Vector3] = None,
        ARROW_LENGTH   : float = 0.1,
        ARROW_DIAMETER : float = 0.1,
        RESOLUTION     : int   =   5,
    ) -> go.Mesh3d:
    if base is None:
        base = Vector3()
    vector = tip - base
    # basis vectors
    bx, by = (bz := vector.unit()).create_orthogonal_duff()

    angles = np.linspace(0, np.pi*2, RESOLUTION, endpoint=False)
    base_circle = (
        + np.array(bx) * np.cos(angles)[:, np.newaxis]
        + np.array(by) * np.sin(angles)[:, np.newaxis]
    ) * 0.02
    neck = base_circle + vector - bz*0.2
    flange = base_circle * 3 + vector - bz*0.2

    coords = np.concatenate([
        np.array(base)+base_circle,
        np.array(base)+neck,
        np.array(base)+flange,
        [np.array(tip)]
    ])
    indexes = np.concatenate([
        np.arange(0,len(angles)*3).reshape((3,-1)),
        np.full(len(angles),len(coords)-1).reshape((1,-1))
    ], axis=0)

    ii1 = np.arange(0,len(angles))[np.newaxis,:].repeat(4,axis=0)
    ii0 = np.arange(0,4)[:,np.newaxis].repeat(len(angles), axis=1)
    index_coords=np.concatenate([
        ii0[:,:,np.newaxis],
        ii1[:,:,np.newaxis],
    ], axis=2)

    triangle_first  = np.array([[0,0],[0,1],[1,0]])
    triangle_second = np.array([[1,0],[0,1],[1,1]])

    triangle_index_coordinates = np.concatenate([
        (index_coords[:-1,:,np.newaxis] + triangle_first).reshape((-1,3,2)),
        (index_coords[:-2,:,np.newaxis] + triangle_second).reshape((-1,3,2))
    ])
    triangle_index_coordinates[...,1] = triangle_index_coordinates[...,1] % index_coords.shape[1]

    triangle_indexes = indexes[
        triangle_index_coordinates[...,0],
        triangle_index_coordinates[...,1]
    ]
    
    return go.Mesh3d(
        **dict(zip("xyz",coords.transpose())),
        **dict(zip("ijk",triangle_indexes.transpose()))
    )

def mesh_plane(unit_normal:Vector3, base:Optional[Vector3]=None, size:float=1.0):
    basis_0, basis_1 = unit_normal.create_orthogonal_duff()
    if base is None:
        base = Vector3()
    base_np = np.array(base)
    coords = np.array([
        np.array(-basis_0 + -basis_1),
        np.array(-basis_0 +  basis_1),
        np.array( basis_0 +  basis_1),
        np.array( basis_0 + -basis_1),
    ])*0.5*size + base_np[np.newaxis, :]
    triangle_indexes = np.array([[0,1,2],[0,2,3]])
    return go.Mesh3d(
        **dict(zip("xyz",coords.transpose())),
        **dict(zip("ijk",triangle_indexes.transpose())),
        opacity=0.25
    )
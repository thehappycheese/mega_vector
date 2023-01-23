from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as _numpy

@dataclass(frozen=True,eq=True)
class Vector3:
    x:float = 0.0
    y:float = 0.0
    z:float = 0.0

    def __repr__(self):
        return f"❬{self.x:.2f}, {self.y:.2f}, {self.z:.2f}❭"

    def __format__(self, format:str=".2f"):
        return f"❬{{:{format}}}, {{:{format}}}, {{:{format}}}❭".format(self.x,self.y,self.z)

    def __add__(self, other:Vector3):
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other:Vector3):
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )
    
    def __neg__(self):
        return Vector3(
            -self.x,
            -self.y,
            -self.z,
        )
    
    def __mul__(self, scalar:float):
        return Vector3(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )
    
    def __truediv__(self, scalar:float):
        return Vector3(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
        )
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __array__(self):
        return _numpy.array([self.x, self.y, self.z])
    
    @staticmethod
    def from_numpy(item:_numpy.ndarray):
        return Vector3(
            float(item[0]),
            float(item[1]),
            float(item[2]),
        )
    
    def __abs__(self):
        return Vector3(
            abs(self.x),
            abs(self.y),
            abs(self.z),
        )
    
    def dot(self, other:Vector3):
        return (
              self.x * other.x
            + self.y * other.y
            + self.z * other.z
        )
    
    def elementwise_product(self, other:Vector3):
        """Hadamard product, or entry-wise product, of elements https://en.wikipedia.org/wiki/Hadamard_product_(matrices)"""
        return Vector3(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z
        )
    
    def cross(self, other:Vector3):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
    
    def mag(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def unit(self):
        len = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return self / len
    
    def create_orthogonal_stark(self):
        """Find some orthogonal/perpendicular axis using a method found by
        Michael M. Stark  which is an improvement on the Hughes-Möller approach.
        https://blog.selfshadow.com/2011/10/17/perp-vectors/
        
        Does not require the input vector to be unit length,
        but does not produce unit length output

        [1] Hughes, J. F., Möller, T., “Building an Orthonormal Basis from a 
        Unit Vector”, Journal of Graphics Tools 4:4 (1999), 33-35.
        [2] Stark, M. M., “Efficient Construction of Perpendicular Vectors
        without Branching”, Journal of Graphics Tools 14:1 (2009), 55-61."""
        a = abs(self)

        self_yx = int(math.copysign(1, a.x - a.y))
        self_zx = int(math.copysign(1, a.x - a.z))
        self_zy = int(math.copysign(1, a.y - a.z))

        axis_x = self_yx & self_zx
        axis_y = (1^axis_x) & self_zy
        axis_z = 1^(axis_x | axis_y)
        
        return self.cross(Vector3(axis_x, axis_y, axis_z))

    def create_orthogonal_xna(self) -> Vector3:
        """Find some orthogonal/perpendicular vector.

        Does not require the input vector to be unit length,
        but does not produce unit length output
        
        Uses a method lifted from the DirectX SDK source code and helpfully summarized here
        [Perpendicular Possibilities]
        (https://blog.selfshadow.com/2011/10/17/perp-vectors/) by Darren
        ```C++
        XMFINLINE XMVECTOR XMVector3Orthogonal(FXMVECTOR V){
            XMVECTOR NegativeV;
            XMVECTOR Z, YZYY;
            XMVECTOR ZIsNegative, YZYYIsNegative;
            XMVECTOR S, D;
            XMVECTOR R0, R1;
            XMVECTOR Select;
            XMVECTOR Zero;
            XMVECTOR Result;
            static CONST XMVECTORU32 Permute1X0X0X0X =
                {XM_PERMUTE_1X, XM_PERMUTE_0X, XM_PERMUTE_0X, XM_PERMUTE_0X};
            static CONST XMVECTORU32 Permute0Y0Z0Y0Y =
                {XM_PERMUTE_0Y, XM_PERMUTE_0Z, XM_PERMUTE_0Y, XM_PERMUTE_0Y};
            Zero = XMVectorZero();
            Z = XMVectorSplatZ(V);
            YZYY = XMVectorPermute(V, V, Permute0Y0Z0Y0Y.v);
            NegativeV = XMVectorSubtract(Zero, V);
            ZIsNegative = XMVectorLess(Z, Zero);
            YZYYIsNegative = XMVectorLess(YZYY, Zero);
            S = XMVectorAdd(YZYY, Z);
            D = XMVectorSubtract(YZYY, Z);
            Select = XMVectorEqualInt(ZIsNegative, YZYYIsNegative);
            R0 = XMVectorPermute(NegativeV, S, Permute1X0X0X0X.v);
            R1 = XMVectorPermute(V, D, Permute1X0X0X0X.v);
            Result = XMVectorSelect(R1, R0, Select);
            return Result;
        }
        ```
        """ 
        # I didn't derive it, but apparently it boils down to this:
        return self.cross(Vector3(0, -math.copysign(1,self.y*self.z), 1))
    
    def create_orthogonal_duff(self) -> tuple[Vector3, Vector3]:
        """
        Find any two orthogonal basis vectors. Fairly robust, and should
        be very fast.
        
        REQUIRES INPUT VECTOR TO BE UNIT LENGTH!

        Tom Duff, James Burgess, Per Christensen, Christophe Hery,
        Andrew Kensler, Max Liani, and Ryusuke Villemin, Building an Orthonormal
        Basis, Revisited, Journal of Computer Graphics Techniques (JCGT),
        vol. 6, no. 1, 1-8, 2017
        Available online http://jcgt.org/published/0006/01/01/

        ```C++
        void branchlessONB(const Vec3f &n, Vec3f &b1, Vec3f &b2) {
            float sign = copysignf(1.0f, n.z);
            const float a = -1.0f / (sign + n.z);
            const float b = n.x * n.y * a;
            b1 = Vec3f(1.0f + sign * n.x * n.x * a, sign * b, -sign * n.x);
            b2 = Vec3f(b, sign + n.y * n.y * a, -n.y);
        }
        ```

        As far as I can tell this is the state of the art developed by Pixar.
        In tests I found it faster than the other methods, despite returning two
        basis vectors instead of just one, and the robustness should be about as
        good as it gets.
        """
        sign = math.copysign(1.0, self.z)
        a = -1.0 / (sign + self.z)
        b = self.x * self.y * a
        return (
            Vector3(
                1.0 + sign * self.x * self.x * a,
                sign * b,
                -sign * self.x
            ),
            Vector3(
                b,
                sign + self.y * self.y * a,
                -self.y
            )
        )

    def project_onto(self,*, plane_unit_normal:Vector3) -> Vector3:
        distance_to_plane = self.dot(plane_unit_normal)
        return self - plane_unit_normal * distance_to_plane
    
    def rotate_about(self, *, axis_unit:Vector3, by_radians:float) -> Vector3:
        distance_to_plane = self.dot(axis_unit)
        projection_vector = axis_unit * distance_to_plane
        projected =  self - projection_vector
        projected_perpendicular = projected.cross(axis_unit)
        return projected*math.cos(by_radians) + projected_perpendicular*math.sin(by_radians) + projection_vector


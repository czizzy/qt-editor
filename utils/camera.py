import numpy as np
from PySide6.QtGui import QVector3D
from PySide6.QtGui import QMatrix4x4
from PySide6.QtGui import QVector4D


class QtCamera:
    "An abstract camera for 3d movement in world"

    def __init__(self):
        ""
        self.availableMoves = ["forward", "backward", "left", "right", "up", "down"]
        # Camera attributes
        self.position = QVector3D(0.0, 0.0, 0.0)
        self.front = QVector3D(0.0, 0.0, -0.5)
        self.worldUp = QVector3D(0.0, 1.0, 0.0)
        self.right = QVector3D(-1.0, 0.0, 0.0)
        self.up = QVector3D()

        self.distance = 3.0

        # Euler Angles for rotation
        self.yaw = -90.0
        self.pitch = 0.0

        # camera options
        self.movementSpeed = 2.5
        self.movementSensitivity = 0.00001
        self.zoom = 45.0

    def updateCameraVectors(self):
        "Update the camera vectors and compute a new front"
        yawRadian = np.radians(self.yaw)
        yawCos = np.cos(yawRadian)
        pitchRadian = np.radians(self.pitch)
        pitchCos = np.cos(pitchRadian)
        frontX = yawCos * pitchCos
        frontY = np.sin(pitchRadian)
        frontZ = np.sin(yawRadian) * pitchCos
        self.front = QVector3D(frontX, frontY, frontZ)
        self.front.normalize()
        self.right = QVector3D.crossProduct(
            self.front,
            self.worldUp)
        self.right.normalize()
        self.up = QVector3D.crossProduct(
            self.right,
            self.front)
        self.up.normalize()

    def move(self, direction: str, deltaTime: float):
        ""
        velocity = self.movementSpeed * deltaTime
        direction = direction.lower()
        if direction not in self.availableMoves:
            raise ValueError(
                "Unknown direction {0}, available moves are {1}".format(
                    direction, self.availableMoves
                )
            )
        if direction == "forward":
            self.position += self.front * velocity
        elif direction == "backward":
            self.position -= self.front * velocity
        elif direction == "right":
            self.position += self.right * velocity
        elif direction == "left":
            self.position -= self.right * velocity
        elif direction == "up":
            self.position += self.up * velocity
        elif direction == "down":
            self.position -= self.up * velocity

    def lookAround(self,
                   xoffset: float,
                   yoffset: float,
                   pitchBound: bool):
        "Look around with camera"
        xoffset *= self.movementSensitivity
        yoffset *= self.movementSensitivity
        self.yaw += xoffset
        self.pitch += yoffset

        if pitchBound:
            if self.pitch > 89.9:
                self.pitch = 89.9
            elif self.pitch < -89.9:
                self.pitch = -89.9
        #
        self.updateCameraVectors()

    def zoomInOut(self, yoffset: float,
                  zoomBound=45.0):
        "Zoom with camera"
        if self.zoom >= 1.0 and self.zoom <= zoomBound:
            self.zoom -= yoffset
        elif self.zoom <= 1.0:
            self.zoom = 1.0
        elif self.zoom >= zoomBound:
            self.zoom = zoomBound

    def getViewMatrix(self):
        "Obtain view matrix for camera"
        view = QMatrix4x4()
        view.lookAt(self.position,
                    self.position+self.front,
                    self.up
                    )
        return view

    def setCameraWithVectors(self,
                             position=QVector3D(0.0, 0.0, 0.0),
                             worldUp=QVector3D(0.0, 1.0, 0.0),
                             yaw=-90.0,
                             pitch=0.0,
                             zoom=45.0,
                             speed=2.5,
                             sensitivity=0.00001):
        "Set camera"
        self.position = position
        self.worldUp = worldUp
        self.pitch = pitch
        self.yaw = yaw
        self.movementSpeed = speed
        self.movementSensitivity = sensitivity
        self.zoom = zoom
        self.updateCameraVectors()

    def setCameraWithFloatVals(self,
                               posx=0.0,
                               posy=0.0,
                               posz=0.0,
                               upx=0.0,
                               upy=1.0,
                               upz=0.0,
                               yaw=-90.0,
                               pitch=0.0,
                               zoom=45.0,
                               speed=2.5,
                               sensitivity=0.00001,
                               ):
        "Set camera floats"
        self.position = QVector3D(posx, posy, posz)
        self.worldUp = QVector3D(upx, upy, upz)
        self.yaw = yaw
        self.pitch = pitch
        self.movementSpeed = speed
        self.movementSensitivity = sensitivity
        self.zoom = zoom
        self.updateCameraVectors()

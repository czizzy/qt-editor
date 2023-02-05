# Author: Kaan Eraslan
# purpose interactive widget

import os
import sys
from utils.camera import QtCamera

from PySide6.QtOpenGL import (QOpenGLShader, QOpenGLShaderProgram)
from PySide6.QtGui import QOpenGLContext, QMatrix4x4, QVector3D

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from PySide6.QtCore import QCoreApplication


try:
    from OpenGL import GL as pygl
except ImportError:
    app = QApplication(sys.argv)
    messageBox = QMessageBox(QMessageBox.Critical, "OpenGL hellogl",
                             "PyOpenGL must be installed to run this example.",
                             QMessageBox.Close)
    messageBox.setDetailedText(
        "Run:\npip install PyOpenGL PyOpenGL_accelerate")
    messageBox.exec_()
    sys.exit(1)


class SceneWindow(QOpenGLWidget):
    def __init__(self, store):
        QOpenGLWidget.__init__(self)
        self.store = store
        self.store.changed.connect(self.update)
        # camera
        self.camera = QtCamera()
        self.camera.position = QVector3D(0.0, 0.0, 3.0)
        self.camera.front = QVector3D(0.0, 0.0, -1.0)
        self.camera.up = QVector3D(0.0, 1.0, 0.0)
        self.camera.movementSensitivity = 0.05

        # shaders etc
        currentDir = os.path.dirname(__file__)
        parentDir = os.path.join(currentDir, os.pardir)

        shaderDir = os.path.join(parentDir, "shaders")

        availableShaders = ["render", "highlight"]
        self.shaders = {
            name: {
                "fragment": os.path.join(shaderDir, name + ".frag"),
                "vertex": os.path.join(shaderDir, name + ".vert")
            } for name in availableShaders
        }
        self.core = "--coreprofile" in QCoreApplication.arguments()

        # opengl data related
        self.context = QOpenGLContext()
        self.program = QOpenGLShaderProgram()
       

    def loadShader(self,
                   shaderName: str,
                   shaderType: str):
        "Load shader"
        shader = self.shaders[shaderName]
        shaderSourcePath = shader[shaderType]
        if shaderType == "vertex":
            shader = QOpenGLShader(QOpenGLShader.Vertex)
        else:
            shader = QOpenGLShader(QOpenGLShader.Fragment)
        #
        isCompiled = shader.compileSourceFile(shaderSourcePath)

        if isCompiled is False:
            print(shader.log())
            raise ValueError(
                "{0} shader {2} known as {1} is not compiled".format(
                    shaderType, shaderName, shaderSourcePath
                )
            )
        return shader

    def useShaders(
        self,
        shaderProgram: QOpenGLShaderProgram,
        shaders,
        attrLocs: dict
    ):
        ""
        print("program shaders: ",
              shaderProgram.shaders())
        for shaderName, shaderTypes in shaders.items():
            #
            if len(shaderTypes) == 2:
                self.useShaderSingleName(
                    shaderProgram=shaderProgram,
                    shaderName=shaderName,
                    attrLocs=attrLocs
                )
            elif len(shaderTypes) == 1:
                shaderType = shaderTypes[0]
                if shaderType == "vertex":
                    shader = self.loadVertexShader(
                        shaderName)
                else:
                    shader = self.loadFragmentShader(
                        shaderName
                    )

                shaderProgram.addShader(shader)
                # adding shader
                self.bindLinkProgram(
                    shaderProgram,
                    attrLocs)

    def loadVertexShader(self, shaderName: str):
        "load vertex shader"
        return self.loadShader(shaderName, "vertex")

    def loadFragmentShader(self, shaderName: str):
        "load fragment shader"
        return self.loadShader(shaderName, "fragment")

    def getGlInfo(self):
        "Get opengl info"
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
            """.format(
            pygl.glGetString(pygl.GL_VENDOR),
            pygl.glGetString(pygl.GL_RENDERER),
            pygl.glGetString(pygl.GL_VERSION),
            pygl.glGetString(pygl.GL_SHADING_LANGUAGE_VERSION)
        )
        return info

    def moveCamera(self, direction: str):
        "Move camera to certain direction and update gl widget"
        self.camera.move(direction, deltaTime=0.05)
        self.update()


    def cleanUpGl(self):
        "Clean up everything"
        self.context.makeCurrent()
        for i, model in enumerate(self.store.models):
            model.destroy()
        # self.vao.destroy()
        del self.program
        self.program = None
        self.doneCurrent()

    def resizeGL(self, width: int, height: int):
        "Resize the viewport"
        funcs = self.context.functions()
        funcs.glViewport(0, 0, width, height)

    def initializeGL(self):
        print('gl initial')
        print(self.getGlInfo())

        # create context and make it current
        self.context.create()
        self.context.aboutToBeDestroyed.connect(
            self.cleanUpGl)

        # initialize functions
        funcs = self.context.functions()
        funcs.initializeOpenGLFunctions()
        funcs.glClearColor(0.0, 0.4, 0.4, 0)
        funcs.glEnable(pygl.GL_DEPTH_TEST)
        funcs.glEnable(pygl.GL_TEXTURE_2D)
        funcs.glEnable(pygl.GL_CULL_FACE)

        # create uniform values for shaders
        # deal with shaders

        # shader
        self.highlightProgram = QOpenGLShaderProgram(
            self.context
        )
        vshader1 = self.loadVertexShader("highlight")
        fshader1 = self.loadFragmentShader("highlight")
        self.highlightProgram.addShader(vshader1)  # adding vertex shader
        self.highlightProgram.addShader(fshader1)  # adding fragment shader
        self.highlightProgram.bindAttributeLocation(
            "aPos", 0)
        self.highlightProgram.bindAttributeLocation(
            "aNormal", 1)

        isLinked = self.highlightProgram.link()
        print("shader program is linked: ",
              isLinked)
        self.highlightProgram.bind()

        self.program = QOpenGLShaderProgram(
            self.context
        )
        vshader = self.loadVertexShader("render")
        fshader = self.loadFragmentShader("render")
        self.program.addShader(vshader)  # adding vertex shader
        self.program.addShader(fshader)  # adding fragment shader
        self.program.bindAttributeLocation(
            "aPos", 0)
        self.program.bindAttributeLocation(
            "aNormal", 1)

        isLinked = self.program.link()
        print("shader program is linked: ",
              isLinked)
        # bind the program
        self.program.bind()

        print("gl initialized")

    def paintGL(self):
        "drawing loop"
        funcs = self.context.functions()

        # clean up what was drawn
        funcs.glClear(
            pygl.GL_COLOR_BUFFER_BIT | pygl.GL_DEPTH_BUFFER_BIT
        )
        funcs.glFrontFace(pygl.GL_CW)
        # funcs.glDisable(pygl.GL_DEPTH_TEST)
        # funcs.glDisable(pygl.GL_CULL_FACE)
        self.draw(self.highlightProgram, funcs, True)
        funcs.glFrontFace(pygl.GL_CCW)

        self.draw(self.program, funcs, False)

    def draw(self, program, funcs, isDrawHighlight):
        # actual drawing
        program.bind()
        # set projection matrix
        projectionMatrix = QMatrix4x4()
        projectionMatrix.perspective(
            self.camera.zoom,
            self.width() / self.height(),
            0.2, 100.0)

        program.setUniformValue('projection',
                                     projectionMatrix)

        # set view/camera matrix
        viewMatrix = self.camera.getViewMatrix()
        program.setUniformValue('view', viewMatrix)

        lightDirection = QVector3D(0.1, -0.1, -1.0)
        lightDirection.normalize()

        program.setUniformValue('uLightDirection', lightDirection)
        for i, model in enumerate(self.store.models):
            matrix = QMatrix4x4()
            matrix.setToIdentity()
            self.recursiveDraw(model, matrix, program, isDrawHighlight)
        program.release()

    def recursiveDraw(self, model, parentMatrix: QMatrix4x4, program, isDrawHighlight):
        funcs = self.context.functions()
        currentMatrix = parentMatrix.__mul__(model.modelMatrix)
        program.setUniformValue("model",
                                           currentMatrix)
        program.setUniformValue("uColor",
                                            model.color)
        model.initialize(funcs)
        model.bind()
        if isDrawHighlight == False:
            model.draw(funcs)
        elif isDrawHighlight and model.id == self.store.currentSelection: 
            model.draw(funcs)
        model.release()

        for i, child in enumerate(model.children):
            self.recursiveDraw(child, currentMatrix, program, isDrawHighlight)

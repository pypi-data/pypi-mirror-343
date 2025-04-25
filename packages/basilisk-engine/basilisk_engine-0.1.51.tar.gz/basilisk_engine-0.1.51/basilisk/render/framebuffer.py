import numpy as np
import moderngl as mgl
from PIL import Image
from ..render.shader import Shader
from ..generic.input_validation import validate_int


class Framebuffer:
    engine: ...
    """Reference to the parent engine"""
    size: tuple[int] | None=None
    """The dimensions of the framebuffer (x, y). Defaults to window size if None"""
    scale: float=1.0
    """Scaling factor applied to the size. Best for use with default size"""
    texture_filter: tuple[int]=(mgl.NEAREST, mgl.NEAREST)
    """The filter applied to the texture when rendering"""
    fbo: mgl.Framebuffer=None
    """The core framebuffer the object provides abstraction for."""
    texture: mgl.Texture=None
    """The color texture of the framebuffer"""
    depth: mgl.Texture=None
    """The depth texture of the framebuffer"""
    _color_attachments = None
    """"""
    _depth_attachment = None
    """"""

    def __init__(self, engine: ..., shader: Shader=None, size: tuple[int]=None, n_color_attachments: int=1, scale: float=1.0, linear_filter: bool=True) -> None:
        """
        Abstraction of the MGL framebuffer.
        Has the given number of color attachements (4-component) and 1 depth attachment.
        All textures are of uniform size.
        """

        self.engine         = engine
        self.ctx            = engine.ctx
        self._size          = size
        self.scale          = scale
        self.shader         = shader
        self.texture_filter = (mgl.LINEAR, mgl.LINEAR) if linear_filter else (mgl.NEAREST, mgl.NEAREST)
        self.n_attachments  = n_color_attachments

        self.load_pipeline()
        self.generate_fbo()

        self.engine.fbos.append(self)

    def generate_fbo(self):
        """
        Generates fresh depth texture and color textures and creates an FBO 
        """

        # Release existing memory
        if self._color_attachments: [tex.release() for tex in self._color_attachments]
        if self._depth_attachment: self._depth_attachment.release()

        # Create textures
        self._color_attachments = [self.ctx.texture(self.size, components=4, dtype='f4') for i in range(self.n_attachments)]
        for tex in self._color_attachments: 
            tex.filter = self.texture_filter
            tex.repeat_x = False
            tex.repeat_y = False

        self._depth_attachment  = self.ctx.depth_texture(self.size)

        # Create the internal fbo
        self.fbo = self.ctx.framebuffer(self._color_attachments, self._depth_attachment)

        # Set the show attachment to default
        self._show = -1
        self.show = 0

    def resize(self, new_size: tuple[int]=None) -> None:
        """
        Update set size framebuffers with the given size.
        """
        
        # Check that we are not updating the size to the existing size and
        if self._size and self._size == new_size: return

        # If we have a set size, update with the given size
        if self._size and new_size: self._size = new_size

        # Update the textures and fbo
        self.generate_fbo()

    def load_pipeline(self) -> None:
        """
        Loads the shader, vbo, and vao used to display the fbo
        """

        # Load Shaders
        if not self.shader: self.shader = Shader(self.engine, self.engine.root + '/shaders/frame.vert', self.engine.root + '/shaders/frame.frag')
        self.engine.shader_handler.add(self.shader)

        # Load VAO
        self.vbo = self.ctx.buffer(np.array([[-1, -1, 0, 0, 0], [1, -1, 0, 1, 0], [1, 1, 0, 1, 1], [-1, 1, 0, 0, 1], [-1, -1, 0, 0, 0], [1, 1, 0, 1, 1]], dtype='f4'))
        self.vao = self.ctx.vertex_array(self.shader.program, [(self.vbo, '3f 2f', 'in_position', 'in_uv')], skip_errors=True)

    def render(self, target=None, color_attachment: int=0, auto_bind=True) -> None:
        """
        Render the fbo to the screen
        If the fbo has multiple attachments, show will specifiy which is shown
        Depth is considered the last show element
        """

        # if not isinstance(show, type(None)): self.show = show

        target.use() if target else self.ctx.screen.use()

        if auto_bind: self.bind(self.color_attachments[min(color_attachment, len(self.color_attachments) - 1)], 'screenTexture', 0)
        self.vao.render()


    def use(self) -> None:
        """
        Select this framebuffer for use
        """

        self.fbo.use()

    def clear(self, color: tuple=(0, 0, 0, 0)) -> None:
        """
        Clear all data currently in the textures (set to black)        
        """

        self.fbo.clear(color=color)

    def bind(self, sampler: mgl.Texture | mgl.TextureArray | mgl.TextureCube , name: str, slot: int=None):
        """
        Binds a texture to the fbo's shader
        """
        
        self.shader.bind(sampler, name, slot)

    def save(self, destination: str=None) -> None:
        """
        Saves the frame as an image to the given file destination
        """

        path = destination if destination else 'screenshot'

        data = self.fbo.read(components=3, alignment=1)
        img = Image.frombytes('RGB', self.size, data).transpose(Image.FLIP_TOP_BOTTOM)
        img.save(f'{path}.png')


    @property
    def size(self) -> tuple[int]:
        """Size of the textures in the fbo in pixels (x: int, y: int)"""
        size = self._size if self._size else self.engine.win_size
        size = tuple(map((lambda x: int(x * self.scale)), size))
        return size
    @property
    def texture(self) -> mgl.Texture:
        """First color attachment in the fbo"""
        return self._color_attachments[0]
    @property
    def color_attachments(self) -> list[mgl.Texture]:
        """List of all color attachments in the fbo"""
        return self._color_attachments
    @property
    def depth(self) -> mgl.Texture:
        """Depth attachment of the fbo"""
        return self._depth_attachment
    @property
    def data(self) -> bytes:
        """Reads the data from the fbo"""
        return self.fbo.read()

    @size.setter
    def size(self, value: tuple[int]=None) -> tuple[int]:
        self.resize(value)
        return self.size

    def __repr__(self) -> str:
        return f'<bsk.Framebuffer | size: {self.size}>' 

    def __del__(self) -> None:
        """
        Releases all memory used by the fbo
        """

        if self._color_attachments: [tex.release() for tex in self._color_attachments]
        if self._depth_attachment: self._depth_attachment.release()
        if self.fbo: self.fbo.release()
        if self.vbo: self.vbo.release()
        if self.vao: self.vao.release()
        if self.shader: 
            if self.shader in self.engine.shader_handler.shaders: self.engine.shader_handler.shaders.remove(self.shader)
            self.shader.__del__()

        if self in self.engine.fbos: self.engine.fbos.remove(self)
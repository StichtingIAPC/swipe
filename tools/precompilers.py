from compressor.filters import CachedCompilerFilter
from compressor_toolkit.precompilers import SCSSCompiler, ES6Compiler


class CachedES6Compiler(CachedCompilerFilter, ES6Compiler):
    def __init__(self, *args, **kwargs):
        print(CachedES6Compiler.__mro__)
        super().__init__(*args, content=None, **kwargs)
        self.mimetype = "module"


class CachedSCSSCompiler(CachedCompilerFilter, SCSSCompiler):
    def __init__(self, *args, **kwargs):
        print(CachedSCSSCompiler.__mro__)
        super().__init__(*args, content=None, **kwargs)
        self.mimetype = "text/x-scss"

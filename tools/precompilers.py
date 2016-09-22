from compressor.filters import CachedCompilerFilter
from compressor_toolkit.precompilers import SCSSCompiler, ES6Compiler


class CachedES6Compiler(CachedCompilerFilter, ES6Compiler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, content=None, **kwargs)  # Content has to be given to CompilerFilter, but it doesn't do anything
        self.mimetype = "module"  # nessesary for mimetype checks in CachedCompiler


class CachedSCSSCompiler(CachedCompilerFilter, SCSSCompiler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, content=None, **kwargs)  # Content has to be given to CompilerFilter, but it doesn't do anything
        self.mimetype = "text/x-scss"  # nessesary for mimetype checks in CachedCompiler

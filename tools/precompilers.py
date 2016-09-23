from pathlib import Path

from compressor.filters import CachedCompilerFilter
from compressor_toolkit.precompilers import SCSSCompiler, ES6Compiler, \
    get_all_static


class OnceHelper(CachedCompilerFilter):
    def __init__(self, content, **kwargs):
        kwargs['mimetype'] = type(self).mimetype  # nessesary for mimetype checks in CachedCompiler
        super().__init__(content=content, **kwargs)  # Content has to be given to CompilerFilter, but it doesn't do anything


class CachedHelperFilter(OnceHelper):
    def input(self, **kwargs):
        return (
            """
            {file_contents}
            /*{last_changed}*/
            """
        ).format(
            file_contents=super().input(**kwargs),
            last_changed=self.last_changed_str()
        )

    def last_changed_str(self):
        static_paths = get_all_static()  #
        scss_files = []
        for path in static_paths:
            p = Path(path)
            scss_files += p.glob('**/*{}'.format(self.infile_ext))
        return str(max(file.stat().st_mtime for file in scss_files))


class CachedES6Compiler(CachedHelperFilter, ES6Compiler):
    mimetype = "module"


class CachedSCSSCompiler(CachedHelperFilter, SCSSCompiler):
    mimetype = "text/x-scss"


class OnceES6Compiler(OnceHelper, ES6Compiler):
    mimetype = "module-once"


class OnceSCSSCompiler(OnceHelper, SCSSCompiler):
    mimetype = "text/x-scss-once"

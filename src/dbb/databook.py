from . import compiler
import glob
import os
import shutil

from .util.config import config
from . import linker
from .util import log


class DataBook:
    def __init__(self):
        if not os.path.exists(config.root):
            raise Exception(f"Top-level (root) directory {config.root} doesn't exist.")

        for d in [config.build, config.buildRef]:
            if not os.path.exists(d):
                os.makedirs(d)

        clean = True
        if clean:
            for d in [config.build, config.buildRef]:
                r = glob.glob(os.path.join(d, "*"))
                for i in r:
                    log.debug(f"removing {i}")
                    os.remove(i)

    def compile(self):
        log.info(f"Compiling")
        c = compiler.Compiler()
        c.compile()
        log.info("Compiled source files")

    def link(self):
        log.info(f"Linking")
        # Linker has a context manager, so use it like so...
        l = linker.Linker()
        authoredFiles = glob.glob(os.path.join(config.build, "*.pdf"))
        log.debug(f"{config.build}, {authoredFiles}")
        l.linkAuthored(authoredFiles)
        log.info("Linked authored files")

        if config.refs:
            referenceFiles = glob.glob(os.path.join(config.buildRef, "*.pdf"))
            log.debug(referenceFiles)
            l.linkReferences(referenceFiles)
            log.info("Linked reference files")
        else:
            shutil.copy(l.outfileNoReferences, config.output)


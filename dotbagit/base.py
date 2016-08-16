'''where base clases go'''

import os
import textwrap
import logging
from bagit import Bag, _can_bag, _make_manifest
from collections import defaultdict, OrderedDict
import json

class DotBag(Bag):
    """extend a Bag to work as a dotbag"""

    def __init__(self, path=None, init=False):
        """Keep same init interface as bagit"""
        # path here is path to the .bagit directory

        self.log = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))
        self.log.debug("Got path: %s", path)
        if init is True:
            self.path = path
            self._init_bag()
        super(DotBag, self).__init__(path)

        self.candidates = defaultdict(list)

    def _validate_structure_payload_directory(self):
        '''Validate the data dir, always true, parent'''
        pass

    def payload_files(self):
        '''override to handle relocation of data'''
        payload_dir = os.path.abspath(os.path.join(self.path, '..'))
        self.log.debug("payload dir: %s", payload_dir)
        for dirpath, _, filenames in os.walk(payload_dir):
            if dirpath == os.path.abspath(self.path):
                continue
            else:
                for f in filenames:
                    # Jump through some hoops here to make the payload files come out
                    # looking like <rootdir>/dir/file, rather than having the entire path.
                    self.log.debug("dirpath: %s filename: %s", dirpath, f)
                    rel_path = os.path.join(dirpath, os.path.normpath(f.replace('\\', '/')))
                    self.log.debug("relpath1: %s", rel_path)
                    rel_path = rel_path.replace(payload_dir + os.path.sep, "", 1)
                    self.log.debug("relpath2: %s", rel_path)
                    yield os.path.join('data', rel_path)

    def _init_bag(self):
        '''init the current directory as a dotbag'''
        self.log.info("initting new dotbag")
        if os.path.isdir(self.path):
            if self._validate_bagittxt():
                raise DBError("already initted")
        else:
            try:
                os.mkdir(self.path)
                self.log.debug("made dir: %s", self.path)
            except OSError:
                raise DBError("could not create directory: %s" % self.path)

        self._write_bagittxt()

    def add(self, targets):
        '''Target files or directory to add'''
        self.log.info('adding dir: %s', "".join(targets))
        for target in targets:
            if os.path.isdir(target):
                # Add all non-ignored files in target dir
                for path in self._walk(target):
                    self.candidates['add'].append(path)
            else:
                # is it a glob or something?
                self.log.debug("non-dir target: %s", target)
        self.log.info('candidates: %s', ",".join(self.candidates['add']))

    def _walk(self, data_dir):
        for dirpath, dirnames, filenames in os.walk(data_dir):
            # if we don't sort here the order of entries is non-deterministic
            # which makes it hard to test the fixity of tagmanifest-md5.txt
            filenames.sort()
            dirnames.sort()
            for dir in dirnames:
                if self._ignored_dirs(dir):
                    dirnames.remove(dir)
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                # BagIt spec requires manifest to always use '/' as path separator
                if os.path.sep != '/':
                    parts = path.split(os.path.sep)
                    path = '/'.join(parts)
                yield path

    def _ignored_dirs(self, dir):
        if os.path.realpath(dir) == os.path.realpath(self.path):
            return True
        else:
            return False

    def save(self, processes=1, manifests=False):
        '''This saves state to disk, but usually this means just manipulating candidates'''
        self._write_candidates()

    def commit(self):
        '''This does what is more like save'''
        owd = os.getcwd()
        os.chdir(self.path)
        try:
            unbaggable = _can_bag(os.path.join(self.path, '..'))
            if unbaggable:
                self.log.error("no write permissions for the following directories and files: \n%s", unbaggable)
                raise DBError("Not all files/folders are writable")
            for c in ['md5']:
                self.log.info("writing manifest-%s.txt", c)
                Oxum = _make_manifest('manifest-%s.txt' % c, '..', 1, c)
                self.log.debug("manifest written: %s", os.path.realpath('manifest-%s.txt' % c))
        except Exception:
            self.log.exception("An error has occurred committing the bag")
            raise
        finally:
            os.chdir(owd)


    def _write_candidates(self):

        with open(os.path.join(self.path,"candidates.json"), "w") as candidates_file:
            json.dump(self.candidates, candidates_file)
            self.log.debug("writing candidates_file (%s): %s", "canddiates.json", json.dumps(self.candidates))

    def _write_bagittxt(self):
        self.log.info("writing bagit.txt")
        txt = textwrap.dedent("""
            BagIt-Version: 0.97
            DotBagIt-Version: 0.97
            Tag-File-Character-Encoding: UTF-8
            """)
        self.log.debug("writting txt: %s" % txt)
        if os.path.isdir(self.path):
            with open(os.path.join(self.path, "bagit.txt"), "w") as bagit_file:
                bagit_file.write(txt)
        else:
            raise DBError("dotbagit dir doesn't exist")


class DBError(Exception):
    """The base DotBagit exception"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

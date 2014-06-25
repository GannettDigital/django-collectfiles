from django.core.management.base import BaseCommand, CommandError
from django.contrib.staticfiles import finders, storage, utils
from django.utils.datastructures import SortedDict
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


class Command(BaseCommand):
    args = '<destination> <source_dir>...'
    help = """
Arguments:
  <destination>
                        Destination directory to collect files into
  <source_dir>
                        App source directory to collect, i.e. "features", "resources", etc
"""

    def add_argumunts(self, parser):
        parser.add_argument("destination", nargs=1)
        parser.add_argument("source_dir", nargs="+")

    def log(self, msg, level=2):
        """
        Small log helper
        """
        self.stdout.write(msg)

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError("You must provide at least 2 arguments, <destination> and <source_dir>")

        # I made up the base_url (arg 2), it isn't needed for this
        storage = FileSystemStorage(dest, "/ignored/")

        for source_dir in source_dirs:
            for path, source_storage in list_files_in_app(
                  settings.INSTALLED_APPS, source_dir, []):

                if getattr(source_storage, "prefix", None):
                    prefixed_path = os.path.join(source_storage.prefix, path)
                else:
                    prefixed_path = path

                copy_file(self.log, 
                          path,
                          prefixed_path,
                          source_storage,
                          storage)

class CustomAppStaticStorage(storage.AppStaticStorage):
    def __init__(self, source_dir, *args, **kwargs):
        self.source_dir = source_dir
        super(CustomAppStaticStorage, self).__init__(*args, **kwargs)


def list_files_in_app(app_names, source_dir, ignore_patterns):
    apps = []
    storages = SortedDict()

    for app in app_names:
       app_storage = CustomAppStaticStorage(source_dir, app)
       if os.path.isdir(app_storage.location):
           storages[app] = app_storage
           if app not in apps:
               apps.append(app)

    for storage in storages.itervalues():
        if storage.exists(''):  # check if storage location exists
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage


def copy_file(log, path, prefixed_path, source_storage, storage, dry_run=False):
    """
    Attempt to copy ``path`` with storage
    """
    # The full path of the source file
    copied_files = []
    source_path = source_storage.path(path)

    # Finally start copying
    if dry_run:
        log(u"Pretending to copy '%s'" % source_path, level=1)
    else:
        log(u"Copying '%s'" % source_path, level=1)
        full_path = storage.path(prefixed_path)
        try:
            os.makedirs(os.path.dirname(full_path))
        except OSError:
            pass
        with source_storage.open(path) as source_file:
            storage.save(prefixed_path, source_file)
    if not prefixed_path in copied_files:
        copied_files.append(prefixed_path)

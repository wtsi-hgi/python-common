from time import sleep

from watchdog.events import FileSystemEventHandler, os

from hgicommon.data_source import SynchronisedFilesDataSource


def block_until_synchronised_files_data_source_started(source: SynchronisedFilesDataSource):
    """
    Blocks until the given synchronised files data source has started to notice changes in the file system (may be a few
    milliseconds after it has been started).
    :param source: the synchronised files data source that has been started
    """
    blocked = True

    def unblock(*args):
        nonlocal blocked
        blocked = False

    event_handler = FileSystemEventHandler()
    event_handler.on_modified = unblock
    source._observer.schedule(event_handler, source._directory_location, recursive=True)

    temp_file_name = ".temp_%s" % block_until_synchronised_files_data_source_started.__name__
    temp_file_path = os.path.join(source._directory_location, temp_file_name)
    i = 0
    while blocked:
        with open(temp_file_path, 'a') as file:
            file.write(str(i))
        sleep(10 / 1000)
        i += 1

    # XXX: Not removing the temp file to avoid the notification.
    # XXX: Not unscheduling as observer does not like it for some reason.
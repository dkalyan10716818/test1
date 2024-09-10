import os
import shutil
import logging
import sys

log_delete_folder = logging.getLogger("delete_folder")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def delete_folder(path):
    log_delete_folder.info('Checked into delete_folder')
    if os.path.isdir(path):
        log_delete_folder.debug("Deleting files in Path:" + path)
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                log_delete_folder.error('Failed to delete {}. Reason: {}'.format(file_path, e))
                sys.exit(1)
    else:
        log_delete_folder.debug('Directory not found ' + path)


if __name__ == '__main__':
    if sys.argv.__len__() == 1:
        log_delete_folder.error("Enter path of the directory that needs to be deleted")
        sys.exit(1)
    else:
        path = sys.argv[1]
        delete_folder(path)


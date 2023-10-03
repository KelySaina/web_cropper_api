import os
import zipfile


class ArchiveFiles:
    def archive_files(self, filenames_to_keep, original, directory):
        # Get a list of all files in the directory
        files = os.listdir(directory)
        files_to_archive = []

        for file_name in filenames_to_keep:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                files_to_archive.append(file_path)

        # Check if there are files to archive
        if files_to_archive:
            # Create a zip file with the directory name
            archive_name = os.path.basename(directory)
            archive_path = os.path.join(directory, archive_name)

            # Create the zip archive with the list of files to archive
            with zipfile.ZipFile(archive_path + '.zip', 'w') as zipf:
                for file_to_archive in files_to_archive:
                    zipf.write(file_to_archive,
                               os.path.basename(file_to_archive))
                zipf.write(original, os.path.basename(original))

            return archive_path + '.zip'

        return 'No files to archive'

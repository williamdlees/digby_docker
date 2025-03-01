import csv
import os
from github import Github
import requests
import base64
import zipfile
import shutil
import glob
import subprocess


# This script manages the updating and organization of genomic and AIRR-seq data for a research study. It reads configurations
# from two CSV files, retrieves and stores updated files from specified GitHub repositories, and cleans up unneeded data.
# This helps in keeping the study data current and well-organized.


CREATE_PATHS = [r'VDJbase/db', r'Genomic/db', r'VDJbase/samples', r'Genomic/samples']
CONFIG_PATH = r'/config/study_data_conf.csv'
FILES_VERSION_PATH = r"/config/study_data_versions.csv"
BASE = r'/study_data'

# Configuration Files Description:
# 1. study_data_conf.csv - This file contains the configuration for the study data. Each row specifies a dataset with details
#    including data type, species, dataset name, GitHub repository URL, branch, and an optional authentication key.
#    the file is already created in the app folder.
#    Fields: ['Type', 'Species', 'Data_Set', 'Repo_URL', 'Repo_Branch', 'Authentication_Key']
#
# 2. study_data_versions.csv - This file tracks the versions of files downloaded from GitHub. It helps in determining
#    whether a file has been updated on the repository since the last download.
#    Fields: ['File_Path', 'Commit_ID', 'Repo_URL']

def check_and_create_csv(csv_path):
    # Checks if a file of the versions exists at the specified path, and if not, creates a new CSV file with the necessary headers.
    if not os.path.exists(csv_path):
        print(f"Creating new CSV at {csv_path}...")
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=['File_Path', 'Commit_ID', 'Repo_URL'])
            writer.writeheader()

def create_folders():
    for path in CREATE_PATHS:
        to_create = os.path.join(BASE, path)
        if not os.path.exists(to_create):
            os.makedirs(to_create)

def clean_file_versions(csv_entries, versions_csv_path=FILES_VERSION_PATH):
    # Create a set of all path and repo URL combinations listed in the CSV
    print("Cleaning file versions...")
    listed_combinations = set()
    for entry in csv_entries:
        data_path = f"{entry['Type']}/{entry['Species']}/{entry['Data_Set']}"
        repo_url = entry['Repo_URL']
        listed_combinations.add((data_path, repo_url))

    # Read the current file_versions.csv
    with open(versions_csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        all_versions = [row for row in reader]

    # Filter out rows not in the listed_combinations
    updated_versions = []
    for version in all_versions:
        version_path = version['File_Path'].rsplit('/', 1)[0]
        version_repo_url = version['Repo_URL']
        if (version_path, version_repo_url) in listed_combinations:
            updated_versions.append(version)

    # Write the updated rows back to file_versions.csv
    with open(versions_csv_path, mode='w', newline='') as file:
        fieldnames = ['File_Path', 'Commit_ID', 'Repo_URL']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_versions)

    print("File versions cleaned successfully.")


def validate_csv_entry(entry):
    # Validates a single entry from the configuration CSV, ensuring it contains all required fields.
    print("Validating CSV entry...")
    required_keys = ['Type', 'Species', 'Data_Set',
                     'Repo_URL', 'Repo_Branch', 'Authentication_Key']
    for key in required_keys:
        if key not in entry and key != 'Authentication_Key':  # Make Authentication_Key optional
            raise ValueError(f"Missing key: {key}")

    print("CSV entry validated successfully.")


def get_file_version(file_path, repo_url, csv_path=FILES_VERSION_PATH):
    # Updates or adds a file's version information in the versions CSV
    print(f"Looking up current version for {file_path} from {repo_url}...")
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['File_Path'] == file_path and row['Repo_URL'] == repo_url:
                print("Version fetched successfully.")
                return row['Commit_ID']

    print("Current version not found.")
    return None


def update_file_version(file_path, commit_id, repo_url, csv_path=FILES_VERSION_PATH):
    # Updates or adds a file's version info in the versions CSV, identified by file path and repo URL.
    print(f"Updating file version for {file_path}...")
    entries = []
    updated = False
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['File_Path'] == file_path and row['Repo_URL'] == repo_url:
                row['Commit_ID'] = commit_id
                updated = True
            entries.append(row)
    if not updated:
        entries.append(
            {'File_Path': file_path, 'Commit_ID': commit_id, 'Repo_URL': repo_url})
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=['File_Path', 'Commit_ID', 'Repo_URL'])
        writer.writeheader()
        writer.writerows(entries)

    print("File version updated successfully.")


def initialize_github(auth_key=None):
    # Initializes a Github object for API interactions, using an auth key if provided
    print("Initializing Github...")
    if auth_key:
        return Github(auth_key)

    print("Github initialized successfully.")
    return Github()  # No authentication


def retrieve_and_store_file(github, repo_url, repo_branch, data_path, filename, store_path):
    # Downloads and stores a file from a GitHub repo to a local path
    print(
        f"Retrieving {filename} from {repo_url}/{repo_branch}/{data_path}...")
    repo = repo_url.split('/')[-1]
    user = repo_url.split('/')[-2]
    github_repo = github.get_user(user).get_repo(repo)
    file_content = github_repo.get_contents(
        path=f"{data_path}/{filename}", ref=repo_branch)

    # If the content is empty, use the download_url to fetch the content
    if not file_content.content:
        response = requests.get(file_content.download_url)
        file_data = response.content
    else:
        file_data = base64.b64decode(file_content.content)

    with open(os.path.join(store_path, filename), 'wb') as file:
        file.write(file_data)

    print(f"{filename} retrieved and stored successfully.")


def list_files_in_repo_dir(github, repo_url, repo_branch, data_path):
    # list files in the specified path of the repo
    repo = repo_url.split('/')[-1]
    user = repo_url.split('/')[-2]
    github_repo = github.get_user(user).get_repo(repo)
    dir_contents = github_repo.get_contents(
        path=f"{data_path}", ref=repo_branch)

    files = [dir_content.path for dir_content in dir_contents]

    return files


def read_csv_entries():
    # Reads and validates entries from the configuration CSV, returning a list of valid entries
    print("Reading CSV entries...")
    csv_entries = []
    with open(CONFIG_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                validate_csv_entry(row)
                csv_entries.append(row)
            except ValueError as e:
                print(f"Invalid CSV entry: {e}")

    print("CSV entries read successfully.")
    return csv_entries


def determine_path_structure(entry):
    # Calculates the directory structure for storing files based on the entry type
    print("Determining path structure...")
    base_path = "/study_data"
    if entry['Type'] == "Genomic":
        db_path = os.path.join(base_path, "Genomic", "db",
                               entry['Species'], entry['Data_Set'])
        samples_path = os.path.join(
            base_path, "Genomic", "samples", entry['Species'], entry['Data_Set'])
    else:  # Assuming AIRR-seq
        db_path = os.path.join(base_path, "VDJbase", "db",
                               entry['Species'], entry['Data_Set'])
        samples_path = os.path.join(
            base_path, "VDJbase", "samples", entry['Species'], entry['Data_Set'])

    print("Path structure determined successfully.")
    return db_path, samples_path


def download_samples(zip_path, store_path):
    # Extracts files from a zip archive into a specified directory
    print(f"Downloading {zip_path}...")

    cwd = os.getcwd()
    os.chdir(store_path)
    cmd = ["curl", zip_path, "--output", "samples.zip"]
    print(cmd)
    subprocess.run(cmd)
    os.chdir(cwd)

    return

def unzip_samples(filename, store_path):
    # Extracts files from a zip archive into a specified directory
    print(f"Unzipping {store_path}/{filename}...")

    cwd = os.getcwd()
    os.chdir(store_path)
    cmd = ["unzip", "-o", "samples.zip"]
    print(cmd)
    subprocess.run(cmd)
    print(f"{filename} downloaded and unzipped")
    os.chdir(cwd)

    return


def clear_directory(directory_path):
    # Removes all contents within a specified directory
    print(f"Clearing directory {directory_path}...")
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        shutil.rmtree(item_path, ignore_errors=True)

    print(f"{directory_path} cleared successfully.")


def process_csv_entry(entry, files_to_download):
    # Processes a single CSV entry, managing file download, storage, and version updating
    print(f"Processing CSV entry...{entry['Type']}/{entry['Species']}/{entry['Data_Set']}")
    auth_key = entry['Authentication_Key'] if entry['Authentication_Key'] else None
    github = initialize_github(auth_key)

    data_path = f"{entry['Type']}/{entry['Species']}/{entry['Data_Set']}"
    db_path, samples_path = determine_path_structure(entry)

    # find the files in the top-level directory for this dataset
    files_in_dataset_root = list_files_in_repo_dir(github, entry['Repo_URL'], entry['Repo_Branch'], data_path)
    print(f'Files in dataset root: {",".join(files_in_dataset_root)}')

    for filename in files_to_download:
        file_version = get_file_version(f"{data_path}/{filename}", entry['Repo_URL'])
        # latest_commit_id = github.get_user(entry['Repo_URL'].split('/')[-2]).get_repo(
        #     entry['Repo_URL'].split('/')[-1]).get_commits(path=f"{data_path}/{filename}", sha=entry['Repo_Branch'])[0].sha
        url_parts = entry['Repo_URL'].split('/')
        username = url_parts[-2]
        repo_name = url_parts[-1]

        # Get the user object from GitHub
        user = github.get_user(username)

        # Get the repository object
        repo = user.get_repo(repo_name)

        # Retrieve the latest commit ID
        try:
            contents = repo.get_contents(path=f"{data_path}/{filename}", ref=entry['Repo_Branch'])
            if not contents:
                print(f'{data_path}/{filename} not found in this repo')
                continue
        except:
            print(f'{data_path}/{filename} not found in this repo')
            continue
        
        commits = repo.get_commits(path=f"{data_path}/{filename}", sha=entry['Repo_Branch'])
        if commits.totalCount:
            latest_commit_id = commits[0].sha
        else:
            print(f'{data_path}/{filename} not found in this repo')
            continue
            
        print(f'Processing filename {data_path}/{filename}')

        if file_version != latest_commit_id:
            if filename == "link_to_sample.txt" or filename == 'samples.zip':
                # clear_directory(samples_path)
                store_path = samples_path
                if os.path.exists(store_path):
                    print(f"Deleting existing content of {store_path}")
                    subprocess.run(f"rm -rf {store_path}/*.*", shell=True)
            else:
                store_path = db_path

            if not os.path.exists(store_path):
                os.makedirs(store_path)

            try:
                retrieve_and_store_file(
                    github, entry['Repo_URL'], entry['Repo_Branch'], data_path, filename, store_path)
            except:
                print(f"{data_path}/{filename} not found in GitHub")
                continue

            if filename == "link_to_sample.txt":
                with open(os.path.join(store_path, filename), 'r') as f:
                    zip_url = f.read()
                    
                download_samples(zip_url, store_path)
                
            if filename == "link_to_sample.txt" or filename == 'samples.zip':
                unzip_samples(filename, store_path)

            update_file_version(f"{data_path}/{filename}",
                                latest_commit_id, entry['Repo_URL'])

    print("CSV entry processed successfully.")


def remove_unlisted_data(csv_entries, base_path="/study_data"):
    # Create a set of all paths listed in the CSV
    print("Removing unlisted data...")
    listed_paths = set()
    for entry in csv_entries:
        if entry['Type'] == "Genomic":
            listed_paths.add(os.path.join(base_path, "Genomic",
                             "db", entry['Species'], entry['Data_Set']))
            listed_paths.add(os.path.join(base_path, "Genomic",
                             "samples", entry['Species'], entry['Data_Set']))
        else:  # Assuming AIRR-seq
            listed_paths.add(os.path.join(base_path, "VDJbase",
                             "db", entry['Species'], entry['Data_Set']))
            listed_paths.add(os.path.join(base_path, "VDJbase",
                             "samples", entry['Species'], entry['Data_Set']))

    # Check each subdirectory in the base_path
    # topdown=False to ensure we delete subdirs first
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            depth = full_path.replace(base_path, '').count(os.sep)

            if depth == 4 and full_path not in listed_paths:
                # Before removing the directory, explicitly remove any hidden files within
                for subdir, _, subfiles in os.walk(full_path):
                    for subfile in subfiles:
                        if subfile.startswith('.'):
                            hidden_file_path = os.path.join(subdir, subfile)
                            print(f"Removing hidden file: {hidden_file_path}")
                            try:
                                os.remove(hidden_file_path)
                            except OSError as e:
                                    if e.errno == 16:  # Device or resource busy
                                        print(f"Cannot remove {hidden_file_path}: Device or resource busy")
                                    else:
                                        print(e)
                try:
                    print(f"Removing unlisted directory: {full_path}")
                    shutil.rmtree(full_path)
                except Exception as e:
                    print(e)

    print("Unlisted data removed successfully.")


def main():
    print("Starting main execution...")
    create_folders()
    check_and_create_csv(FILES_VERSION_PATH)
    csv_entries = read_csv_entries()
    clean_file_versions(csv_entries)
    files_to_download = ['samples.zip', 'link_to_sample.txt', 'db.sqlite3', 'db_description.txt']

    for entry in csv_entries:
        #try:
        process_csv_entry(entry, files_to_download)
        #except Exception as e:
        #    print("error: ", e)

    remove_unlisted_data(csv_entries)
    print("Finished updating study_data.")


if __name__ == "__main__":
    main()

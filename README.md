# Addon CADBase Library

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Blender >= 4.1.0](https://img.shields.io/badge/Blender->=4.1.0-gren)](https://blender.org)


![Demonstration of all windows of the CADBase Library add-on.](./Resources/panels_collage.png "All windows of the CADBase Library add-on.")

This addon allows the user to interact with CADBase (upload and download parts) via the Blender interface.

CADBase is a platform for publishing and sharing information about 3D components (parts), drawings and manufacturers.

**Important Note:**  To use the addon, you must have an account on the [CADBase Platform](https://cadbase.rs).

## Description

![how to save a file to a file set of the Sphere component](./Resources/save_and_push.gif)

The addon is designed to use components from CADBase in the Blender interface.

Component modifications contain sets of files for various CAD systems. This addon will work with data from the Blender set, without downloading documentation and data from other file sets.

Files uploaded to file sets are versioned, allowing you to restore earlier versions, get the old state they were in before the changes, review the changes, and find out who last changed something and caused the problem.

### Dependencies

##### Installation Blake3

To use this addon to update files already in the CADBase storage, Blake3 must be installed.

```sh
  # Install on Unix/macOS
  python3 -m pip install "blake3"
  # Install on Windows
  py -m pip install "blake3"
```

**Please Note:** The addon will work without this _Blake3_ library, the only difference is that the files in the CADBase storage (cloud) that have already been uploaded will not be replaced.

### First start

Once installed, the addon will be available in the 3D View > Sidebar menu.

Select the **CADBase Library** addon in the Import-Export category.

#### Configuration CADBase Library

First you need to set the library location. CADBase cloud storage will be synchronized with this location. Also there will storage files with technical data for addon.

This location can be changed in the addon settings in the field _Library path_.

#### Getting an authorization token

In the _CADBase Library_ window, click the **Authorization** button.

When the _CADBase Library Authorization_ window opens, you need to set a **username** and **password** in order to access CADBase.

After entering these data to receive the token and pressing the **OK** button. Please wait until you receive the token.

**Important Note:**  If the access token has expired, you need to repeat the steps above.


### Control

 `Open` - open the next level (deeper). If a component of a list of user's favorite components is selected, it will open the list of modifications for that component; if a modification of a component modifications list is selected, it will open a set of files for Blender.

 `Go back` - return to the previous level (higher). If a set of files is open, the button opens a list of modifications of a component; if a list of modifications of a component is open, the button opens a list of a user's favorite component.

 `Pull data` - retrieves data from the remote server and updates the local library view.

 `Link file` - link creates a reference to the data in the source file such that changes made there will be reflected in the referencing file the next time it is reloaded.

 `Push changes` - button to upload files from Blender folder (set of files for Blender) of local library to CADBase storage. Before uploading, the hash of existing files in local and cloud storage is checked, if they are different, the files in cloud storage are updated. Blake3 library is used to calculate the hash, if it is unavailable, the hash is not checked and existing files in the cloud are not updated.

 `Settings` - this button opens a modal window where you can specify the path to the local library, where the files received from CADBase will be stored, and the address of CADBase server.

 `Authorization` - this button opens a modal window where you can specify login and password from CADBase profile to get a new authorization token. This action must be repeated if the access token is revoked or expired.

## Usage

Add target components to bookmarks (favorites) on the CADBase site.

In Blender will only display components that the user has bookmarked on CADBase platform, as well as those that have been previously downloaded.

### Getting data

To get the data, click on the **Pull Data** button. Depending on the open position (directory), this will start the process of retrieving a list of the user's favorite components, a list of component modifications, or downloading files from the file set of the selected component modification for Blender.

### Sending data

Open the modification from which you want to upload the files.

Click the **Push changes** button to upload the local files for the set of component modification files to CADBase storage (cloud).

Information about the upload process will be displayed in the Blender report.

After uploading the files, a message will be displayed in the Blender report with information about the number of successfully uploaded files.

## Additional Information

##### Blender modules and macros folders

The addon settings in Blender, such as the local library path, server address (API Point), and access token, will be saved in the `cadbase_library.dat` file, which will be located at the `bpy.utils.resource_path('USER')` path.

##### Used (reserved) names in the addon

Please don't use `cadbase_file_2018` and `cadbase_file_2018.log` as file or folder names in the CADBase library folder. These files store server responses and logs, if you use these filenames for your data, you may lose them.

If you need to save logs to a file (for example, for debugging, studying, or other purposes), you need to create a _cadbase_file_2018.log_ file in the local library folder.

In component folders, a `component` file is created with the technical data about the component.

In fileset folders, a `modification` file is created with the technical data about the component modification and fileset.

##### How the addon work with data

To avoid losing local data when downloading from CADBase storage (from the cloud), files already in local storage are skipped.

Before uploading files to CADBase storage (to the cloud), the addon checks for existing files in the cloud and excludes files from the upload list if their local and cloud hashes match. A hash is calculated using the Blake3 library.

This check is skipped and previously uploaded files (already in the cloud) are not updated unless the Blake3 library is installed.

## Links

Add-on development happens in [this](https://gitlab.com/cadbase/cadbaselibrary-blender) repository (GitLab).

Mirrors on [GitHub](https://github.com/mnnxp/cadbaselibrary-blender) and [Codeberg](https://codeberg.org/mnnxp/cadbaselibrary-blender).

About CADBase Platform on [YouTube](https://www.youtube.com/@cadbaseplatform)

## Version

v0.0.2 2024-04-18    * added blender manifest, description and fixed bugs

v0.0.1 2024-04-14    * first release

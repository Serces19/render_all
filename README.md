# Render All!

This is a simple queue-based renderer for Nuke (.nk) files.
![Texto alternativo](https://i.imgur.com/PDNg36u.jpg)

### Installation:
-Download the .zip file for your operating system (Windows or Linux).

  https://drive.google.com/drive/folders/1io6Bzk6VWzec3zipq8IImg4PL-oegFce?usp=drive_link

-Unzip the file and open the executable (Render all).

### Usage:
Follow these steps to use it:
1. Set the path to the Nuke executable file. The default path for Windows is 'C:\Program Files\Nuke14.0v4\Nuke14.0.exe'.
2. Enter the exact name of the Write node you want to render. It should have the same name in all scripts. It's recommended to use a standard nomenclature to name the Write nodes (it will render 'Write1' by default).
3. Add and remove files to/from the render queue. There are three ways to add new files:
   
    a) Dragging the scripts into the queue.

    b) Using the '+' button to browse and select files.

    c) Utilizing a database (this feature is not available yet; I'm currently working on a plugin to load scripts into the database from Nuke).


5. Optionally, there are two checkbox functions to enable:
   
    a) Open the folder containing the finished renders after each render.

    b) Automatically shut down the computer 10 minutes after finishing the entire render queue.

5. Click 'Render!' to execute the command and render all files in the queue. You can stop the render at any time, which will terminate the process.



### Notes on Possible Errors:
This program use nuke_i licence to work.

There might be conflicts with Linux (Not tested). Unfortunately, I cannot provide a macOS version at the moment, but I'll try to develop one soon.

I hope this tool is helpful. Any error reports are appreciated.



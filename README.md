# Photon

Photon laser tag project for UARK software engineering

# Team 14 Members
|   Github Usernames  |     Names     |
| ------------------- | ------------- |
| Lizzieh17           | Lizzie Howell |
| 0x01FE              | Jackson Hodge |
| LionsDevelopment    | Luke Lyons    |

# Setup
1. Open Virtual Box and run Debian VM.
2. Make sure a clear terminal is open.
3. Now you need to set up the dependencies needed for our app
   1. Check to see which Python version is installed by running `python3 --version`.
   2. Needs to be at least Python 3.9.2.
   3. Check to see if `pip` is installed on the device by running `pip --version` or `pip3 --version`.
   4. If `pip` is not installed, follow these steps:
      1. In a terminal, run `sudo apt update`.
      2. Then run `sudo apt install python3-venv python3-pip`.
      3. Check to see if `pip` is installed again by running `pip --version` or `pip3 --version`.
   5. Once Python and `pip` are correctly installed, clone the project onto the local device.
   6. When cloning into your preferred file location, use your selected IDE or within the terminal use the command `git clone (HTTPS web URL grabbed from GitHub)`.
4. You are now ready to move to the run program section
## Install Dependencies

```sh
python3 -m pip install -r requirements.txt

```

## Run Program
1. Open into the location you cloned the project into, make sure in that file you can see a README.md, a requirements.txt, and a folder named app
   1. Open a terminal with this location, if you are in GUI/file manager of the folder you can right click and open a terminal in that folder
   2. In this terminal run the command `python3 -m pip install -r requirements.txt`, this should install all library and dependencies needed to run the app
   3. Navigate back to the file manager once downloads are complete
2. Back in location of the project go into the app folder, in the folder open a new terminal like before (or you can cd from the previous location to app)  
   1. Now run `python3 app.py`
   3. Once the app is running it will show a url you can ctrl + click into or you can just go to `http://127.0.0.1:5000`
3. Now you are in the app, clicking the edit teams button will allow you to change the teams and submit them by using the submit button on the bottom

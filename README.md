# 2605_DS5111_dkn7rm
This is my repo for Summer 2026 DS5111 Software & Automation Skills

If you're starting up a VM, this is a short setup guide to make sure you have the same coding environment every time.
You'll need a github SSH key for this setup. If you don't have one, you'll have to do two things:

1. Go [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to create the SSH keys on the VM side. Navigate the hidden `.ssh` folder in the root directory for this step. (`ls -a` to see hidden directories)
2. Once you've created the SSH keys, you'll need to access the .pub file for the contents. On the github site, click on your profile picture on the top right > Settings > SSH and GPG keys under Access in the list on the left. Click on the green button on the top right that says "New SSH Key", copy and paste your .pub file contents in the text box, and the save key.

To automate the setup, we'll create 4 initialization files.
1. `init.sh`
- Create a new file named `init.sh` (`nano init.sh`). Inside the file, include these lines:
  ```
  sudo apt update                       #This updates the VM to the current versions
  sudo apt install make -y              #This allows us to use makefiles
  sudo apt install python3.14-venv -y   #This installs python
  sudo apt install tree                 #Allows you to list files in directory in tree form
  ```
- Save the file and close out. To make the file executable, use `chmod +x init.sh`
- Run the script with `bash init.sh`. If all goes well, you should be able to execute the `tree` command with no issue.
2. `init_git_creds.sh`
- To setup your git credentials, we'll create a new file named `init_git_creds.sh`. Inside the file include these lines:
  - ```
    !#/usr/bin/bash

    USER=<your github email>
    NAME=<your github user name>

    git config --global --list

    git config --global user.email ${USER} 
    git config --global user.name  ${NAME} 

    git config --global --list
    ```
  - Use the same process above to make the file executable and then run the file. If all goes well, your email and username should be echoed back to you when you run the file.
  - You can also use `ssh -T git@github.com` to verify you have connected to your github repo. 
  - Don't forget to change your username and email in the `<>`.
3.  `makefile`
- Create a new file named `makefile`. Inside the file include these lines:
  - ```
    default:
      @cat makefile

    init:
      bash init.sh

    init_git_creds: init
      bash init_git_creds.s

    env:
      python3 -m venv env; . env/bin/activate; pip install --upgrade pip

    update:  env
      . env/bin/activate; pip install -r requirements.txt
    ```
  - No need to make this file executable as the file should run when you use the `make` command.
  - The file should echo the contents if you use the `make` command alone.
4. `requirements.txt`
- Create a new file named `requirements.txt`. Inside the file include these dependancies:
  - pandas
  - numpy
- You should be able to run `make update` to update python with the requirements.
- To verify the virtual environment has been updated, you can run `. env/bin/activate`.
  - You should see `(env)` at the beginning of the command line now.
- You can run `pip list` to verify pandas and numpy are installed in the virtual enviroment.
5. Cloning and Pushing
- You can now clone your repo for this class using `git clone git@github.com:<username>/2605_DS5111_<NetID>.git`
  - Replace the username and NetId with your own.
- We'll create a new directory called `scripts` (`mkdir scripts`).
- Navigate to the new directory and move all the init scripts here (`mv ~/init.sh .`, `mv ~/init_git_creds.sh .`, `mv ~/makefile .`, `mv ~/requirements.txt .`).
- Run `git add .` to add the changes for staging.
- Run `git commit -m ""`, with a short but descriptive message inside the quotes.
- Run `git push` to send your work to your repo.

With all luck, you have now created an automated way to start up a new VM.

# quiverlocal-py
Tools for building local WordPress development environments in WSL (Windows Subsystem for Linux)

This tool should work in most Ubuntu/Debian environments, but it has not been fully tested.

## Background
There are tools available to create local WordPress environments on Windows and Linux platforms. The struggle I had was getting an environment that would run on WSL. This is the layer that allows you to run a Linux instance directly on your Windows machine. This was critical for me as I had little interest in developing in Windows and wanted the flexibility that WSL offered. Unfortunately, the tools I found for creating a WordPress environment did not work in WSL. 

So I decided to make my own.

## Approach
The first thing I needed to do was to fully document exactly how to create a local WordPress environmnet locally. I am not one to be content with relying on other tools to do the work. I first want to know how to do it myself and then I can use tools to make it easier.

WordPress is actually a very simple configuration. There is an underlying database with a number of core tables where all of the content is stored. There are then files in the form of configurations and php scripts that do all the management of that content. To setup a local environment you need a web server (like Apache), the WordPress files, and a database (MySQL).

After spending some time documenting all of the steps needed to build out an environment, I was ready to automate the process.

## Bash Scripts
I have a background in Unix, so my initial plan was to create bash scripts for each of the different tasks. These would include the following.
- New Installation
- Import Existing Website
- Delete Website
- Add SSL Certificate to a Site

These initial scripts have been moved to their own repository named [quiverlocal-bash](https://github.com/JohnStortaJr/quiverlocal-bash). It will be maintained separately from this Python implementation.

## Python
While working on the bash scripts, I hit a snag. I wanted to store the site configurations in json files so that they could be retrieved and referenced for the different scripts. Unfortunately, the tool that everyone seemed to use to retrieve json info within bash scripts was jq. This tools worked fine for retrieving information from a file and parsing it, but creating new json files and updating existing ones got very cumbersome, very fast. 

Meanwhile, I have been trying to learn Python and was interested in turning this into an actual Python app rather than just a set of bash scripts. This presented a different challenge in that there were a lot of linux commands I was using that did not have a direct, native option within Pyton. So I had to decide if it was better to figure out jq in bash and continue down that path or to figure out how to run the linux commands in Python. I settled on the latter as that gave me the most flexibility for the tool I was trying to build.

To run the linux commands from python, I was planning to use the os library with the run function. This was fine, except that it required the command to be passed as a list containing each word in the command. For example, if I wanted to run "curl https://wordpress.org/latest.tar.gz | tar zx -C domain_dir", I would need to a list similar to this.
- curl
- https://wordpress.org/latest.tar.gz
- |
- tar
- zx
- -C
- domain_dir

You can see how this could get cumbersome. So I came up with a different solution.

Instead of passing the commands I needed to run directly to the run() function, I would create a dynamic bash script containing the command. And then pass that script into the run function. I am not saying it is perfect, but it is much easier to work with and, so far, has worked great.

### Menu interface
Since the python app is more than just a collection of scripts, I was able to put together some nice menus as a user interface. And because I am now saving the configurations in json files, I can have an option to view the existing configurations and to validate inputs. It also allows me to check for things like duplicate names.

### Functions
The quiver app provides for the following functions...
- List Installed Sites
- Create a New WordPress Website
- Import Existing Websites from Backups
- Add/Remove SSL Certificates
- Delete Website

### Usage

Use the `quiversetup` script to install all the required packages and create the initial quiver database

To create and manage local WordPress sites, run `./quiver` and then follow the prompts


# Flet-Color-Browser

### What is this?

 A simple but sophisticated tool(Web and desktop UI) for easy color selection when developing [Flet](flet.dev) applications.
Here is a link to the online/web version of this tool -> <u>[flet-colors-browser.fly.io](flet-colors-browser.fly.io)</u>

### Inspiration

I decided to build up this tool after looking at the [Flet-Icons-Browser]() - a simple browser which eases Icon selection when developing Flet apps . 
This tool is actually a refactored-clone(or fork if you want) of it. 
I just added my personal UI touch and included more comments in the code :) 

### Screen captures
Below are some captures I made of the tool in execution.

- _**On PC:**_
  - _Dark Mode_
        <br><br>
      <image src= "assets/captures/pc_dark.png" align="center">
        <br><br>
  - _Light Mode_
        <br><br>
      <image src= "assets/captures/pc_dark.png" align="center">
        

- _**In a web browser:**_
  - _Dark Mode_
        <br><br>
      <image src= "assets/captures/web_dark.png" align="center">
        <br><br>
  - _Light Mode_
        <br><br>
      <image src= "assets/captures/web_light.png" align="center">
        <br><br>
  - **Video**
        <br><br>
      <video src= "assets/captures/web_video.mp4" align="center">

### How to get started?

Pretty easy and straight forward!

- Start by cloning and unzipping this repo: [how-to]()
- Enter the directory

        cd Flet-Color-Browser
- Install the requirements(only Flet is required):
    `pip install flet`
- Run the `main.py` file

      python main.py
- That's all! Easy and Straight-forward right?



### How to deploy to Fly.io?

A detailed version of how to deploy [Flet](https://flet.dev/) apps on [Fly.io](fly.io) could be found <u>[here](https://flet.dev/docs/guides/python/deploying-web-app/fly-io)</u>.

Deploy:

    flyctl deploy

Check deployment:

    flyctl status

Re-deploy:

    flyctl deploy --no-cache


### Issues/Contribution
I tried my best to make this project simple and easy to understand, but if you have problems/issues when using this :(, 
then you are free to raise an issue and I will happily respond.

If you instead want to contribute(new features, bug/typo fixes, etc), just fork this project and make a pull request. :)
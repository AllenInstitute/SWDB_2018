# git lesson 3: Working with Github

This material assumes that you have worked through the previous lessons.  At this point you should understand:

* How to create a repository on your computer
* Stage and commit changes to your repository
* Create topic branches
* Merge topic branches back to your master branch

## Step 1: Create a repository 

Github is an online code collaboration platform centered around git.  The first thing you should do is create a repository there.  While you can always create an new repository, in this lesson we will be showing you how to collaborate with others on a single repository.  You will do this by creating a copy of an existing repository.  

In `git` parlance, creating a copy of a repository is called `forking`.  Do this:

1. Go here: [https://github.com/alleninstitute/swdb_2018_tools](https://github.com/alleninstitute/swdb_2018_tools)

2. Click the 'Fork' button. 

3. If prompted, tell it to clone the repository to your profile.

You now have a copy of the `swdb_2018_tools` repository all to yourself!

## Step 2: Clone your repository to your computer

As before, we will be using `GitKraken` when using `git` on your computer.  Now we want to make changes to the fork we just created, so let's bring it down to our computers.

1. Open `GitKraken`
2. File => Clone Repo
3. Github.com
4. Choose a location on your computer to save the repository ("Where to clone to")
5. Browse to your fork (`<user_name>/swdb_2018_tools`)
6. Clone the repo!

## Step 3: Pull in some cool new feature from someone else!

Let's say someone has made some changes to the repository you forked and you would like to have those changes on your computer.  

### Step 3a: Tell GitKraken about AllenInstitute/swdb_2018_tools

First we need our repository to know where these changes are coming from.  We only need to do this once.

1. Click the "+" in the "Remote" section on the left.
2. Paste in: https://github.com/alleninstitute/swdb_2018_tools
3. Accept the default name ("AllenInstitute")

Now the "AllenInstitute" remote appears above your fork in the list below.  

### Step 3b: Pull changes from AllenInstitute


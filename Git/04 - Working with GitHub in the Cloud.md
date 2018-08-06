# git lesson 4: Working with GitHub in the Cloud

This material assumes that you have worked through the previous lessons.  At this point you should understand:

* How to create a repository on your computer
* Stage and commit changes to your repository
* Create topic branches
* Merge topic branches back to your master branch
* Work on a shared repository with forks and pull requests

## Oh no I don't have a GUI

Don't panic.  These instructions replicate the exact workflow from lesson three, this time with the Jupyter terminal.

## Step 1: Create a repository

(this one is the same as the previous section, since it just uses the GitHub browser interface)

Github is an online code collaboration platform centered around git.  The first thing you should do is create a repository there.  While you can always create an new repository, in this lesson we will be showing you how to collaborate with others on a single repository.  You will do this by creating a copy of an existing repository.  

In `git` parlance, creating a copy of a repository is called `forking`.  Do this:

1. Go here: [https://github.com/alleninstitute/swdb_2018_tools](https://github.com/alleninstitute/swdb_2018_tools)

2. Click the 'Fork' button. 

3. If prompted, tell it to clone the repository to your profile.

You now have a copy of the `swdb_2018_tools` repository all to yourself!

## Step 2: Clone your repository to your computer (in the cloud!)
 
As before, we will be using `GitKraken` when using `git` on your computer.  Now we want to make changes to the fork we just created, so let's bring it down to our computers.

1. Open the Jupyter Terminal ("new" => "terminal")
2. Copy the URL of the GitHub repository you want to clone to your clipboard.  (e.g. https://github.com/dyf/SWDB_2018.git)
3. Clone the repo!
```bash
$ git clone https://github.com/dyf/SWDB_2018.git
```

## Step 3: Someone made changes -- bring them to your computer.

Let's say someone has made some changes to the repository you forked and you would like to have those changes on your computer.  

### Step 3a: Tell `git` about AllenInstitute/swdb_2018_tools

Right now your repository only knows about your fork (`user/swdb_2018_tools`).  We need our repository to know where these changes are coming from.  We only need to do this once.

```bash
$ git remote add AllenInstitute https://github.com/alleninstitute/swdb_2018_tools
```

### Step 3b: Pull changes from AllenInstitute to your computer

Now we want to bring some changes from `AllenInstitute/master` down to your local master branch.  

```bash
$ git checkout master # let's make sure we're on the master branch
$ git pull AllenInstitute master
```

That's it -- now you've incorporated changes from `AllenInstitute/master` to your local repository.  You can now update the Github's copy of your fork's master branch by pushing it:

```bash
$ git push origin master
```




## Step 4: Make changes and push them to your fork on GitHub

Now we want to make some changes to this repository.  Not the AllenInstitute copy, but just your fork on GitHub.

### Step 4a: Create a topic branch and make a change

Branches are great because they let you work on multiple things at the same time.  So let's make our changes in a branch!

```bash
$ git checkout -b dyf_branch # create a new branch and check it out
$ touch dyf.txt # create an empty file
$ git add dyf.txt
$ git commit -m "adding dyf.txt"
```

### Step 4b: Push your branch to your fork on GitHub

Remember: we always want master to be consistent with `AllenInstitute/master`, so we aren't going to merge your topic branch back into `local/master`.  Instead, we are going to push it up to your fork on GitHub.

```bash
$ git push origin dyf_branch
```


## Step 5: Issue a pull request to AllenInstitute/master

(this is the same as before since it uses the GitHub browser interface)

We have your topic branch up on Github with your fork.  Now we want to merge your changes into `AllenInstitute/master`.  We ask for this via a "Pull Request":

1.   Open Github to http://github.com/user_name/SWDB_2018
2.   Github will notice your new branch.  Click "Compare and Pull Request".

## Step 6: Bring your own change back down to local/master

Once your request has been approved, just bring your changes back down to `local/master` and we're done.

```bash
$ git checkout master # just to be safe
$ git branch -d dyf_branch # delete the branch
$ git pull AllenInstitute master
```

You can now update the Github's copy of your fork's master branch by pushing it:

```bash
$ git push origin master
```

import git
from git import Repo
import os


#variable declaration

url = input ("Please input the git-repo, which you want to clone: ")
root = input ("Please input the path where you want to clone the repo: ")
Repo.clone_from(url, root)











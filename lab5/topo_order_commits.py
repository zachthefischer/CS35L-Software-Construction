# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.

#!/usr/local/cs/bin python3

"""
Testing with strace

Ran this command with 
$ strace -f -e trace=execve python3 ../../../topo_order_commits.py 2>&1 | grep git
execve traces the commands that call other programs, like git
Grepped with git as an argument to check, but I ran it without grep to check manually just in case and couldn't find anything 

"""


from typing import List

import os
import sys
import zlib
from collections import deque


class CommitNode:
    def __init__(self, commit_hash):
        """                                                                                                                             
        :type commit_hash: str                                                                                                          
        """
        self.commit_hash = commit_hash
        #self.message = message
        # Get commit message for debugging
        self.parents = set()
        self.children = set()



"""
Finds the path to the .git directory
Can be called from any subdirectory
Exits if no .git directory is found 
"""

def discover_git_directory():
    current_path = os.getcwd()
    
    while True:
        git_path = os.path.join(current_path, '.git')
        if os.path.isdir(git_path):
            return git_path  # Return the path if .git directory is found                                                               

        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            # NO .GIT FOUND                                                                                                             
            print("Not inside a Git repository", file=sys.stderr)
            sys.exit(1)  # Exit with status 1                                                                                           
        else:
            # Move up to the parent directory and continue the search                                                                   
            current_path = parent_path
    pass



"""
Creates a dictionary of branches, where the key is the branch
name and the value is the list of commits. 
"""

def get_branches():
    git_dir = discover_git_directory() 
    refs_dir = os.path.join(git_dir, 'refs/heads')
    branches = dict()
    #print(refs_dir)

    for (root, dirs, files) in os.walk(refs_dir):
        for filename in files:
            
            branch = os.path.join(root, filename)
            branch_name = os.path.relpath(os.path.join(root, filename), start=refs_dir)
            #print(branch_name)
            commit = (open(branch).read()).strip()
            branches[branch_name] = commit

    #print(branches)
    return branches



"""
Take the dictionary of branches from above
Map the commit hashes to the branch names, rather than the
branch names to the commits
"""

def map_hash_to_branch():
    branch = get_branches()
    hash_to_branch = dict()  # maps hash to branch name
    for b, commit in branch.items():
        hash_to_branch[commit] = b
    return hash_to_branch



"""
Build the commit graph by traversing the root nodes and creating or populating
nodes when necessary
"""

def build_commit_graph():
    branch  = get_branches()
    git_dir = discover_git_directory()
    
    graph = dict()
    stack = []
    root_commits = set()

    # Traverse commits by following each branch
    for b, commit in branch.items():
        # Add branch to
        stack.append(commit)

        while stack:
            current_commit = stack.pop()
            commit_node = CommitNode(current_commit)

            # Get git object
            with open(os.path.join(git_dir, "objects", commit_node.commit_hash[:2], commit_node.commit_hash[2:]), "rb") as f:
                content = zlib.decompress(f.read()).decode().split('\n')
                #parents = [line.split(' ')[1] for line in content if line.startswith('parent')]
                #message = content[5]
            has_parents = False
            
            for string in content:
                if string.startswith("parent"):
                    parent = string[7:]
                    # Add parent hash to parent list
                    commit_node.parents.add(parent)
                    stack.append(parent)
                    has_parents = True
                    
            if has_parents == False:
                # No parents means root commit
                root_commits.add(current_commit)

            # If the commit has not been stored already, add it to the dictionary
            if current_commit in graph:
                pass
            else:
                graph[current_commit] = commit_node

     # Add the children to all the nodes in graph
    for commit, node in graph.items():
        parents = node.parents
            
        for parent in parents:
            graph[parent].children.add(commit)




    #print(graph)
    
    return graph, root_commits




"""
Use khans algorithm  to create a topological sort
"""

def topological_sort(graph, root_commits):
    result = []
    queue = deque()

    # Add all the root nodes to the queue as starting points for the ordering
    for root in root_commits:
        queue.append(root)

    while queue:
        node = queue.popleft()
        result.append(node)

        # Sort the children of the current node
        children = sorted(graph[node].children)

        for child in children:
            graph[child].parents.remove(node)

            # If no parents, add child to the queue
            if len(graph[child].parents) == 0:
                queue.append(child)

    # Return the result in reversed order
    return result[::-1]

"""
Given the topological sorting, print all the commit hashes
If a commit hash is the head of a branch, print the branch name
If the next node 
"""


def print_hashes(sorted_nodes):
    graph, _ = build_commit_graph()
    git_dir = discover_git_directory()
    hash_branch_dict = map_hash_to_branch()
    empty_line = False
    branch_dict = get_branches()
    
    for i in range (len(sorted_nodes) -1):
        commit_hash = sorted_nodes[i]
        node = graph[commit_hash]

        # print commit (with branch names)
        if commit_hash in hash_branch_dict:
            print(commit_hash, end="")
            for branch, commit in branch_dict.items():
                if commit == commit_hash:
                    print(" "+branch, end="")
            print("")
        else:
            print(commit_hash)
        
        
        next_commit_hash = sorted_nodes[i+1]
        #print(graph[commit_hash].parents())

        if next_commit_hash not in graph[commit_hash].parents:
            # INSERT STICKY END
            # Print the parents, and include an = if it's the last line
            for parent in range(len(sorted(graph[commit_hash].parents))):
                if parent == len(graph[commit_hash].parents)-1:
                    print(sorted(graph[commit_hash].parents)[parent]+"=\n")
                else:
                    print(sorted(graph[commit_hash].parents)[parent], end=" ")
                
                    
            # STICKY START
            # Print the children, and include a newline if its the last line
            print("=", end="")

            if not graph[next_commit_hash].children:
                print("")
            else:
                for child in range(len(sorted(graph[next_commit_hash].children))):
                    if child == len(graph[next_commit_hash].children)-1:
                        print(sorted(graph[next_commit_hash].children)[child]+"\n")
                    else:
                        print(sorted(graph[next_commit_hash].children)[child], end=" ")

                    

    
    # Parent-est node is always printed last
    # Still must check if its a branch head
    commit_hash = sorted_nodes[-1]

    if commit_hash in hash_branch_dict:
        print(commit_hash, hash_branch_dict[commit_hash])
    else:
        print(commit_hash)


        
"""
Put all the functions together 
"""
def topo_order_commits():
    # direc = discover_git_directory()
    # branches = get_branches()
    graph, root_commits = build_commit_graph()
    ordered_commits = topological_sort(graph, root_commits)
    print_hashes(ordered_commits)

if __name__ == '__main__':
    topo_order_commits()

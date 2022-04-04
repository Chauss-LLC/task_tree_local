# task_tree_local

<img src="logo_task_tree.svg" alt="Logo of the project" width="200"/>

This is part of the big project `task_tree` for local use.

[Русская документация здесь.](README-ru.md)

## The problem

Many people have a need in something like a structural way to note their tasks.
Someone use a handle diary, someone - a calendar, but someone prefer to save his goals in a text file in the folder with documents or on the desktop.
In all that ways there are advantages and disadvantages. There are not infinite but big enough amount of utilities that allow to organize own tasks, set deadlines, attach files, share the list of tasks, etc. Anyway, many of them, will be paid.

We introduce new product - task_tree that, in fact, works like a simple hierarchical database. The branches go from the root task to sub-tasks, that allow to visually represent the problem and its internal structure. This may be useful for any people who need in a way to 
fixate their plans.

To not be unfounded, we recommend to refer to this source, where you can feel all positive sides of the approach on practice:

https://www.mindmeister.com/

## Base functionality

This part of the huge project is laconically called `task_tree_local` and it present all facilities for local usage.

After implementing the main functionality we will be able to focus on adding some extra abilities, creating our own web-service like
`mindmeister` etc.

Maybe, the application will be broke down into several modules, but the goal functionality must be the next:

- Ability to create, modify, edit and delete trees on the local machine.
	- Save and delete files with trees.
	- Implementation of a simple command-line interface, where the target user can:
		* Browse saved trees.
		* Add new tasks to trees.
		* Mark certain tasks as solved or not solved.
	- Export the tree to the text files, import the tree from the text file.
		* File must be human-readable so the user can edit it with text editor and then perform import.

## Suggested solution tools

* Python modules:
	* `json`;
	* `psycopg2`, `psycopg2-binary` or `sqlite3` (depending on the database we choose);
	* `cmd`, `shlex`, `argparse`, `Colorama` (for CLI);
	* `rich` (for printing the tree to the console).

### Linters and code checkers

Our team use `pylint` и `pydocstyle` for development.

Both can be installed via `pip`.

Before sending the commit to the `master` branch, please, check your code:
```
python -m pylint --py-version=3.8 $(git ls-files '*.py')
python -m pydocstyle --match='(?!tests).*\.py' --convention=google $(git ls-files '*.py')
```

## Suggested CLI

The way of work may be implemented as immediate appeal to the module:
```
python -m task_tree <command>           # Common scheme of the interactions with the project.
python -m task_tree show tree Homework  # Example.
```
The presented set of commands:
```
# Interactions with trees:
list                            # Print the identifiers of all saved trees.
show   tree <TREE-ID>           # Print certain tree.
add    tree <TREE-ID>           # Create a tree of tasks.
delete tree <TREE-ID>           # Tree deletion.
export tree <TREE-ID>           # Print the tree in a text way.
import tree <TREE-ID>           # Import tree from file.
check  tree <TREE-ID>           # Check that all tasks in the tree are solved.
# Interactions with certain tree:
show   task <TASK-ID> tree <TREE-ID>          # Show the state and other data of the certain task in the specified tree.
mark   task <TASK-ID> <STATUS> tree <TREE-ID> # Set the state of the certain task in the specified tree.
add    task <TASK-ID> tree <TREE-ID>
delete task <TASK-ID> tree <TREE-ID>
# For calling CLI:
cli
```
We will present the command-line interface if the user want one. The commands will be the same, but for convenience we provide
the ability to select the tree for interaction, so now the user don't need to type the `tree <TREE-ID>` every time.

The text for localization - it is additional messages or text of errors, that we will print for the user on appeal to the module.

## User workflow

* When the user sits down at the laptop, he/she then loads the OS.
* While OS is loading, the user thinks through all tasks that he/she must to solve in the current session of the work with laptop.
* The user then opens our product - runs the necessary module though the terminal.
* The user creates the task tree by sequence of commands. Every task have one of 3 states:
	* Pending. (the default one)
	* Solved.
	* Failed.
* Every task have task-parents and tasks-children. Our project surely offer the next functionality for automation:
	* If the user sets the task as solved, all the children tasks automatically are set to be solved.
	* Vice versa: if the user sets all the subtasks as solved, the task-parent is set to be solved.
	* If the user sets the task as failed, the task-parent is set to be failed.
* After that the user starts to solve problems, as he/she solves the new one he/she goes back to our module and mark the necessary task as solved or failed.
* In the session end the user checks the task tree (`check tree` command) for the fact that it was completely solved with success.
* If not all the tasks are solved the user saves the tree for the next work session.
	* Unlike notepad what may be a more convenient for the user, our product saves the file in the default directory.
	* In this way the user don't care about the place where all trees are stored.
* The session completion.

## Perspectives for this direction

* From frontend to REST API.
* From telegram bot to android apps.
* From pictures attachment to the tree sharing and attachment of any files or notes.
* Commenting.
* From automation events to the own scenarios management language.
* From import of github issues to the export to google calendar.
* Note, that our module may become the full-fledged python module and be flied to the `pypi`!
* Serialization and deserialization. Export of the tree into the picture. GUI.
* In the case of the backend we are able to make a selective share: we can share not only the tree but separate subtrees.
* Adding deadlines to the tasks. Print not in the tree form but like timetable.
* Reminders and notifications.
* Some statistics (presenting the state of the task in the percents solved).
* Tags with which it will be convenient to quickly navigate through the tree.
* It is possible to set the cost of each vertex and automatically count the cost of all the planned businesses.
* etc.

Here is the list of available development directions. Obviously, all that wont fit up into the semester project, anyway the existence of such a range of abilities and development directions itself already confirms our choose for `task_tree`.

# Implementation Issues

## Implementation Features or *what tasks can the project be divided into*

<ins>We will take care of the architecture in advance</ins>, so in future the addition of new features will not require editing of existing code.

The structure of the project *may be* like this:

1. Module *core*. Provide direct tree editing.
	* We need the next functionality:
	* The tree vertexes (tasks) may have status `SOLVED`, `FAILED`, or `PENDING` (the default one). 
	* You can add other tree vertexes to the tasks, also there must be different connections and automation (see [previous](#user-workflow))
	* See [this issue for details](https://github.com/KH9IZ/task_tree_local/issues/6).
2. Module *save/load*. Provide tree saving on the local machine.
	* It may be database or binary or text file.
	* However, if we separate this functionality in other module, in the future we can add other realization of this API: for example, access to the server and saving the tree on the remote device.
3. Module *cli*. That is command line interface.
	* The indispensable part of our product, because it is a mediator between the target user and the core module.
	* Here we show the list of saved trees, show trees in a convenient way and provide some ways to interact with the *core* module.
	* Of course, by separating the code, we make it possible to use some GUI instead of cli or something like frontend.
4. Module *of exporting and importing the tree into the file*. May be merged with the 2nd one.
	* The user may want to export the tree into the text file then make some editing in text editor and then perform the import.
	* Now you can use not only cli but your own text editor also.

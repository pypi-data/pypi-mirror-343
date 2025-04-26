# Automation Generator

> [!TIP]
> Concept kickstart. Intention is to add multiple tasks to automate.

This tool allows you to automate actions based on mouse clicks and keyboard inputs.

## Prerequisites

Make sure you have the latest version of Python installed on your machine.

To install the required dependencies, run the following command:

```sh
sh commands/install-python-dependencies.sh
```

## How to Use This Tool

1. Start the watch mode by running the following command. This command will activate the program to monitor mouse clicks and keyboard typing.

    ```sh
    sh commands/action-watch.sh
    ```

2. Perform the actions you want to automate. The program will track your mouse clicks and keyboard inputs.

3. To stop the watch mode and store the recorded actions, press the ESC key along with a mouse click. This action will trigger the program to save the information in a log file.

4. To execute the stored actions, run the following command. This command will read the stored actions from the log file and perform the steps that were previously done by the user.

    ```sh
    sh commands/action-perform.sh
    ```

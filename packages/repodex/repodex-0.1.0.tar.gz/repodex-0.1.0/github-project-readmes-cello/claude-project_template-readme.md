# Claude Project `Placeholder Project Name`

![logo](claude.svg)

[[toc]]

## Project Link

<https://placeholder-link.here>

## Project Name

>(aka: What are you working on?):

```txt
`Placeholder` - project name
```

## Project Description

Note to self: You should prompt the AI after the project is fully fleshed out to give a good descriptor of the project like this:

```txt
Im the admin of this project write a paragraph explainer of this project. It will be used as a brief summary for users at Cello to understand what this project is about.

Note: The first sentence needs to explain immediately. The reason is the GUI shows the first one or two sentences, then there's an ellipses to click that exposes the rest of the descriptor
```

>(aka; What are you trying to achieve?):

```txt
Placeholder - This project does this and that and the other thing.
```

## Project Knowledge

### Project System Prompt

[See here](./project-knowledge/system-prompt.md)

### Project Files

[See here](./project-knowledge/files/)

## Project Docs

`Placeholder` - Place your project documentation here if any is needed. Often not required, however some projects may require prompting specificity of optimal use.

`Placeholder` - Additionally, you could share a successful chat link example here as well. In the claude project open a past chat then hit share and copy the link here if you like too.

## Project Author

> @placeholder-username

---

> [!CAUTION]
> Delete this section before publishing your project

## Template Instructions

> [!NOTE]
> Recommended install: [GitHub CLI](https://github.com/cli/cli#installation)

1. Pull template:

    ```sh
    gh repo clone CelloCommunications/claude-project_template
    ```

2. Delete .git dir Immediately!

    ```sh
    # mac or linux
    rm -rf .git

    # windows
    rm .git -force
    ```

3. Rename the project folder:

    ```sh
    mv claude-project_template claude-project_project-name
    ```

4. Fill in all placeholder details

    I've put a `Placeholder` in front of all the fields you need to fill in. You can do a 'find in files` for `Placeholder` to find all the fields you need to fill in.

    - README.md
    - project-knowledge/system-prompt.md
    - project-knowledge/files/markdown-or-other-text-files-here-work-best.md

5. Add your project files to the `project-knowledge/files/` dir

    These will be sync to the Claude Project Knowledge Base. The Ai will reference these files when answering questions about your project.

6. Add any resources to the `resources/` dir

    Purpose of `resources` dir: Is for filles that are not in the Claude Project you will publish, but rather are resources you needed to form the project.

7. Lastly before pushing to GitHub, delete this section before publishing your project.

8. You can use the kickstart script to help you get the project Git ready and published to GitHub:

    ```sh
    ./kickstart.sh # or use the ps1 version
    ```

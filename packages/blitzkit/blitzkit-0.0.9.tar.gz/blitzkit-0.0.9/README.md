# BlitzKit Documentation 

BlitzKit is a command-line tool that helps student developers automate full-stack project setup. It generates a clean, organized folder structure with starter files to help you get started fast.

## Features

- **Flexible Project Setup**: Generate a full-stack project with customizable frontend and backend technologies.
- **CLI-based Automation**: Uses [Yargs](https://github.com/yargs/yargs) to parse command-line arguments.
- **Customizable Tech Stack**: Supports various frontend and backend frameworks (see [Supported Tech Stacks](#supported-tech-stacks)).
- **Stylish Terminal Output**: Uses [Chalk](https://github.com/chalk/chalk), and [Figlet](https://github.com/patorjk/figlet.js) for an enhanced CLI experience.

## Supported Tech Stacks


BlitzKit supports multiple frontend and backend technologies, allowing developers to customize their full-stack setup.


### **Frontend Options (`-f, --frontend`)**
| Framework / Library | Command Flag  |
|--------------------|--------------|
| Vanilla HTML/CSS/JS | `vanilla` |
| React (Vite Setup) | `react-js` |
| Vue.js (Vite Setup) | `vue-js`|
| Angular | `angular` |
| SvelteKit | coming soon... |

### **Backend Options (`-b, --backend`)**
| Framework / Library | Command Flag  |
|--------------------|--------------|
| Flask (Python) | `flask` |
| FastAPI (Python) | `fast-api` |
| Django (Python) | coming soon... |
| Express.js (Node.js) | coming soon... |
| Spring Boot (Java) | coming soon... |
| Ruby on Rails | coming soon... |


```

## Installation


1. **Clone the Repository(Optional)**

   ```bash
   git clone https://github.com/lennythecreator/BlitzKit.git
   cd Blitzkit
   ```



2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   or

   ```bash
   pip install blitzkit
   ```

   to install the package globally from PyPI.


## Usage

Once installed or linked globally, run BlitzKit from your terminal.

### Command Syntax


- `-p, --project`: Specifies the type of project to set up. Currently, the supported type is `web` and `data`.
- `-l, --level`: Specifies the level of experience, e.g., `beginner` or `advanced` the supported type is `beginner`.

### Flags
```
- `-p, --name`: Specifies project name.
- `-f, --frontend`: Defines the type of project (e.g., `react`, `vue`, ,`angular`).  
- `-b, --backend`: Defines the type of project (e.g., `django`, `flask`, ,`fastapi`,`express`,`spring`,).  

When executed, the CLI will:
- Display an ASCII art banner ("BlitzKit").
- Show a usage message inside a styled box.
- Create a structured folder in your current directory (insist on changing the project name)


## Troubleshooting

- **System Requirements**
  Before generating a project, make sure your system meets the necessary requirements for both the project setup tool and the specific technologies involved.

- **Figlet or Boxen Not Displaying Correctly:**  
  Ensure your terminal supports the required Unicode characters and colors.

- **Permission Issues on Windows:**  
  If you encounter permission issues, run your terminal as an Administrator or adjust your system's PATH variable after running `npm link`.

- **Project Creation Errors:**  
  Make sure you’re providing the correct arguments. For example, use `-p web -l beginner -f react -b express` to set up a React-Express project.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests with your improvements. For any issues or suggestions, please open an issue on GitHub.

## License

This project is licensed under the ISC License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please reach out via [GitHub Issues](https://github.com/lennythecreator/Bear_CLI/issues) or email [chuwa1@morgan.edu](mailto:chuwa1@morgan.edu).

---

Happy Coding! 🚀

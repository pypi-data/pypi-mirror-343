import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompileFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_dependency_file_content(self, file_path):
        """
        Read the content of a dependency file.

        Args:
            file_path (str): Path to the dependency file to read.

        Returns:
            str: Content of the dependency file, or None if an error occurs.
        """
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            logger.debug(f" #### `SnowX` encountered an error while reading dependency file:\n{file_path}\nError: {e}")
            return None


    async def get_compile_file_planning(self, userRequest, tree):
        """
        Identify critical build/run and dependency files in the project structure.

        Args:
            userRequest (str): The user's request or context.
            tree (str): The project structure.

        Returns:
            dict: Dictionary with the crucial file paths.
        """
        logger.debug("\n #### `SnowX` is identifying critical build/run and dependency files")
        
        # Define patterns for critical files
        dependency_patterns = [
            # JavaScript/Node.js
            "package.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json", "bower.json",
            # Python
            "requirements.txt", "Pipfile", "pyproject.toml", "setup.py", "poetry.lock", "conda.yaml", "environment.yml",
            # Ruby
            "Gemfile", "gems.rb",
            # Java/Kotlin/Scala
            "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "ivy.xml", "build.sbt",
            # .NET/C#
            "*.csproj", "*.fsproj", "packages.config", "paket.dependencies", "*.sln",
            # PHP
            "composer.json", "composer.lock",
            # Go
            "go.mod", "go.sum", "Gopkg.toml", "glide.yaml",
            # Rust
            "Cargo.toml", "Cargo.lock",
            # Swift/iOS/macOS
            "Podfile", "Package.swift", "Cartfile",
            # Docker/Containers
            "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
            # Web
            "webpack.config.js", "rollup.config.js", "vite.config.js", "tsconfig.json",
            # Other
            "pubspec.yaml", "mix.exs", "rebar.config", "deps.edn", "project.clj",
            "build.xml", "meson.build", "CMakeLists.txt", "Makefile", "configure.ac"
        ]
        
        # Main build/run file patterns
        main_file_patterns = [
            # Python
            "main.py", "app.py", "run.py", "wsgi.py", "asgi.py", "manage.py",
            # JavaScript/TypeScript
            "index.js", "main.js", "app.js", "server.js", "index.ts", "main.ts", "app.ts", "server.ts",
            # Java
            "Main.java", "App.java", "Application.java",
            # Go
            "main.go", "app.go", "server.go",
            # C#
            "Program.cs", "Startup.cs",
            # Ruby
            "main.rb", "app.rb", "application.rb", "config.ru",
            # PHP
            "index.php", "app.php",
            # Rust
            "main.rs", "lib.rs",
            # C/C++
            "main.c", "main.cpp", "app.c", "app.cpp",
            # Swift
            "main.swift", "App.swift",
            # Kotlin
            "Main.kt", "App.kt", "Application.kt",
            # Dart/Flutter
            "main.dart", "app.dart",
            # Scala
            "Main.scala", "App.scala",
            # Clojure
            "core.clj",
            # Elixir
            "application.ex",
            # Haskell
            "Main.hs", "App.hs",
            # Run scripts
            "run.bat", "start.bat", "run.sh", "start.sh", "Makefile", "makefile",
            # Configuration files
            "config.json", "config.yaml", "config.yml", "settings.json", ".env"
        ]
        
        # Files to exclude
        exclude_patterns = [
            "package-lock.json",
            "yarn.lock",
            "Podfile.lock",
            "Gemfile.lock",
            "node_modules/",
            "build/",
            "dist/",
            ".git/",
            "vendor/",
            "target/",
            "bin/",
            "obj/",
            "__pycache__/",
            ".venv/",
            "venv/",
            "env/"
        ]
        
        # Parse the tree to extract file paths
        lines = tree.split('\n')
        crucial_files = []
        
        for line in lines:
            # Skip empty lines and directory entries
            if not line.strip() or line.endswith('/') or line.endswith('\\'):
                continue
                
            # Skip excluded patterns
            if any(exclude in line for exclude in exclude_patterns):
                continue
                
            # Check if line contains a dependency file
            for pattern in dependency_patterns:
                # Handle wildcard patterns
                if '*' in pattern:
                    extension = pattern.replace('*', '')
                    if line.endswith(extension):
                        path_parts = line.split()
                        if len(path_parts) > 0:
                            file_path = path_parts[-1].strip()
                            # Ensure it's a full path
                            if not file_path.startswith(self.repo.get_repo_path()):
                                file_path = os.path.join(self.repo.get_repo_path(), file_path)
                            crucial_files.append(file_path)
                            break
                elif pattern in line:
                    path_parts = line.split()
                    if len(path_parts) > 0:
                        file_path = path_parts[-1].strip()
                        # Ensure it's a full path
                        if not file_path.startswith(self.repo.get_repo_path()):
                            file_path = os.path.join(self.repo.get_repo_path(), file_path)
                        crucial_files.append(file_path)
                        break
            
            # Check if line contains a main build/run file
            if len(crucial_files) < 5:  # Increased limit to capture more important files
                for pattern in main_file_patterns:
                    if pattern in line:
                        path_parts = line.split()
                        if len(path_parts) > 0:
                            file_path = path_parts[-1].strip()
                            # Ensure it's a full path
                            if not file_path.startswith(self.repo.get_repo_path()):
                                file_path = os.path.join(self.repo.get_repo_path(), file_path)
                            if file_path not in crucial_files:
                                crucial_files.append(file_path)
                                break
        
        # Limit to maximum 5 most critical files (increased from 3)
        crucial_files = crucial_files[:5]
        
        logger.debug(f"\n #### `SnowX` identified {len(crucial_files)} crucial files")
        
        # Always include snowx.md in the crucial files
        snowx_md_path = os.path.join(self.repo.get_repo_path(), "snowx.md")
        if snowx_md_path not in crucial_files:
            crucial_files.append(snowx_md_path)
            logger.debug("\n #### `SnowX` added snowx.md to crucial files")
        
        return {
            "crucial_files": crucial_files
        }


    async def get_compile_file_plannings(self, userRequest):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        logger.debug("\n #### `SnowX` is initiating the file processing task")
        all_dependency_file_contents = self.repo.print_tree()

        plan = await self.get_compile_file_planning(userRequest, all_dependency_file_contents)
        logger.debug("\n #### `SnowX` has successfully completed the file processing task")
        return plan

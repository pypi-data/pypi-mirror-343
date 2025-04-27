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

class DependencyFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_dependency_file_planning(self, tree):
        """
        Identify critical dependency and configuration files in the project structure.

        Args:
            tree (str): The project structure.

        Returns:
            dict: Dictionary with the dependency file paths.
        """
        logger.debug("\n #### `SnowX` is initiating dependency file planning")
        
        # Comprehensive dependency file patterns covering various tech stacks
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
            "obj/"
        ]
        
        # Parse the tree to extract file paths
        lines = tree.split('\n')
        file_paths = []
        
        for line in lines:
            # Skip empty lines and directory entries
            if not line.strip() or line.endswith('/') or line.endswith('\\'):
                continue
                
            # Check if line contains a file path
            for pattern in dependency_patterns:
                # Handle wildcard patterns
                if '*' in pattern:
                    extension = pattern.replace('*', '')
                    if line.endswith(extension):
                        # Check if it's not in excluded patterns
                        if not any(exclude in line for exclude in exclude_patterns):
                            # Extract the file path
                            path_parts = line.split()
                            if len(path_parts) > 0:
                                file_path = path_parts[-1].strip()
                                # Ensure it's a full path
                                if not file_path.startswith(self.repo.get_repo_path()):
                                    file_path = os.path.join(self.repo.get_repo_path(), file_path)
                                file_paths.append(file_path)
                elif pattern in line:
                    # Check if it's not in excluded patterns
                    if not any(exclude in line for exclude in exclude_patterns):
                        # Extract the file path
                        path_parts = line.split()
                        if len(path_parts) > 0:
                            file_path = path_parts[-1].strip()
                            # Ensure it's a full path
                            if not file_path.startswith(self.repo.get_repo_path()):
                                file_path = os.path.join(self.repo.get_repo_path(), file_path)
                            file_paths.append(file_path)
        
        # Limit to maximum 3 most critical files
        file_paths = file_paths[:3]
        
        # Always include snowx.md in the dependency files
        snowx_md_path = os.path.join(self.repo.get_repo_path(), "snowx.md")
        if snowx_md_path not in file_paths:
            file_paths.append(snowx_md_path)
            logger.debug("\n #### `SnowX` added snowx.md to dependency files")
        
        logger.debug(f"\n #### `SnowX` identified {len(file_paths)} dependency files")
        
        return {
            "dependency_files": file_paths
        }


    async def get_dependency_file_plannings(self):
        logger.debug("\n #### `SnowX` is starting to gather dependency file plannings")
        all_dependency_file_contents = self.repo.print_tree()

        logger.debug("\n #### `SnowX` is processing the project structure")
        plan = await self.get_dependency_file_planning(all_dependency_file_contents)
        return plan

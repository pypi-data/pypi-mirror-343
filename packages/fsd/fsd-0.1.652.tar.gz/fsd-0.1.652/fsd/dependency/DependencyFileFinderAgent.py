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
        current_path_parts = []
        
        for line in lines:
            if not line.strip():
                continue
                
            # Determine the indentation level to track directory structure
            indent = len(line) - len(line.lstrip())
            line_content = line.strip()
            
            # Check if it's a directory entry (usually ends with / or \)
            is_directory = line_content.endswith('/') or line_content.endswith('\\')
            
            # Adjust the current path based on indentation
            while len(current_path_parts) > 0 and indent <= len(current_path_parts) * 2:
                current_path_parts.pop()
            
            if is_directory:
                # Add directory to current path (remove trailing slashes)
                dir_name = line_content.rstrip('/\\')
                current_path_parts.append(dir_name)
            else:
                # This is a file entry
                file_name = line_content
                
                # Check if it matches our dependency patterns
                for pattern in dependency_patterns:
                    matches = False
                    if '*' in pattern:
                        extension = pattern.replace('*', '')
                        if file_name.endswith(extension):
                            matches = True
                    elif pattern in file_name:
                        matches = True
                        
                    if matches and not any(exclude in file_name for exclude in exclude_patterns):
                        # Construct the relative path within the repo
                        relative_path = "/".join(current_path_parts + [file_name]) if current_path_parts else file_name
                        
                        # Join with repo path to get absolute path
                        full_path = os.path.join(self.repo.get_repo_path(), relative_path)
                        
                        file_paths.append(full_path)
                        break
        
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

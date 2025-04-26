import os
import sys


from .DependencyPrePromptAgent import DependencyPrePromptAgent
from .DependencyProjectAnalysAgent import DependencyProjectAnalysAgent
from .DependencyFileFinderAgent import DependencyFileFinderAgent
from .DependencyGuiderAgent import DependencyGuiderAgent
from .DependencyTaskPlanner import DependencyTaskPlanner
from .DependencyCheckAgent import DependencyCheckAgent
from .DependencyCheckCLIAgent import DependencyCheckCLIAgent


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.system.CommandRunner import CommandRunner
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
logger = get_logger(__name__)

HOME_DIRECTORY = os.path.expanduser('~')
HIDDEN_ZINLEY_FOLDER = '.zinley'

class DependencyControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.analysAgent = DependencyProjectAnalysAgent(repo)
        self.preprompt = DependencyPrePromptAgent(repo)
        self.project = ProjectManager(repo)
        self.fileFinder = DependencyFileFinderAgent(repo)
        self.guider = DependencyGuiderAgent(repo)
        self.taskPlanner = DependencyTaskPlanner(repo)
        self.command = CommandRunner(repo)
        self.CLI = DependencyCheckCLIAgent(repo)
        self.checker = DependencyCheckAgent(repo)
        self.imageAgent = PromptImageUrlAgent(repo)
        self.directory_path = self.repo.get_repo_path()


    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def guider_pipeline(self, user_prompt):
        """Pipeline for regular coding tasks."""
        logger.info(" #### `SnowX` is initiating the guider pipeline.")

        while True:
            user_prompt_json = input("Do you need more help with dependency?: ")
            guide = await self.guider.get_guider_plans(user_prompt_json)
            finalPrompt = guide['processed_prompt']
            pipeline = guide['pipeline']
            explainer = guide['explainer']

            if pipeline == "0":
                break
            elif pipeline == "1":
                logger.info(explainer)
            elif pipeline == "2":
                logger.info(guide)
                await self.start_dependency_installation_process(user_prompt)
                break


    async def start_dependency_installation_process(self, instruction, file_attachments=None, focused_files=None):
        
        logger.info(instruction)
        logger.info(" #### In order to complete this run, I will need to install some dependencies.")

        os_architecture = self.repo.return_os()
        file_result = await self.fileFinder.get_dependency_file_plannings()
        dependency_files = file_result.get('dependency_files', [])
        all_files = set(file_result.get('dependency_files', []))
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"  - {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading files:\n{files_list}")

        logger.info(" #### `SnowX` is preparing to execute the finalized plan.")
        task = await self.taskPlanner.get_task_plan(instruction, dependency_files, os_architecture)
        await self.command.execute_steps(task, dependency_files)
        commits = task.get('commits', "")
        if commits:
            self.repo.add_all_files(f"{commits}")
        logger.info(f" #### `SnowX` has completed the task")

        logger.info("-------------------------------------------------")


    async def start_dependency_installation_process_normal(self, instruction, file_attachments=None, focused_files=None):
        os_architecture = self.repo.return_os()
        file_result = await self.fileFinder.get_dependency_file_plannings()
        dependency_files = file_result.get('dependency_files', [])

        all_files = set(file_result.get('dependency_files', []))
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"  - {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading files:\n{files_list}")

        self.analysAgent.initial_setup(dependency_files, os_architecture)

        image_result = await self.imageAgent.process_image_links(instruction)
        assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []

        #idea_plan = await self.analysAgent.get_idea_plans(instruction, file_attachments, focused_files, assets_link)
        
        logger.info(" #### `SnowX` is preparing to execute the plan.")
        task = await self.taskPlanner.get_task_plan(instruction, dependency_files, os_architecture)
        await self.command.execute_steps(task, dependency_files)
        commits = task.get('commits', "")
        if commits:
            self.repo.add_all_files(f"{commits}")
        logger.info(f" #### `SnowX` has completed the task")

        logger.info("-------------------------------------------------")


    async def get_started(self, user_prompt, file_attachments=None, focused_files=None):
        """Start the processing of the user prompt."""
        logger.info(" #### `SnowX` is beginning to process the user request.")

        prePrompt = await self.get_prePrompt(user_prompt)
        pipeline = prePrompt['pipeline']

        if pipeline == "0" or pipeline == 0:
            explainer = prePrompt['explainer']
            print(explainer)
        elif pipeline == "1" or pipeline == 1:
            explainer = prePrompt['explainer']
            print(explainer)
            self.guider.initial_setup(user_prompt)
            self.guider.conversation_history.append({"role": "assistant", "content": f"{prePrompt}"})
            await self.guider_pipeline(user_prompt)
        elif pipeline == "2" or pipeline == 2:
            await self.start_dependency_installation_process_normal(user_prompt, file_attachments, focused_files)

        logger.info(f" #### `SnowX` has completed processing the request: {user_prompt}")
        logger.info("-------------------------------------------------")


    async def get_started_coding_pipeline(self, user_prompt, file_attachments=None, focused_files=None):
        logger.info("-------------------------------------------------")
        logger.debug(" #### `SnowX` is assigned.")
        """Start the processing of the user prompt."""

        prePrompt = await self.get_prePrompt(user_prompt)
        pipeline = prePrompt['pipeline']

        if pipeline == "0" or pipeline == 0:
            explainer = prePrompt['explainer']
            print(explainer)
        elif pipeline == "2" or pipeline == 2:
            install_plan = prePrompt['install_plan']
            await self.start_dependency_installation_process(install_plan, file_attachments, focused_files)

        logger.info(" #### `SnowX` has installed all required dependencies. ")
        logger.info("-------------------------------------------------")

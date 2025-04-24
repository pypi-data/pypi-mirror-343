import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
import platform
logger = get_logger(__name__)

class IdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs, context, file_attachments, assets_link):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_tree()

        system_prompt = (
            f"You are a senior {role} architect. Analyze the project files and develop a production-ready implementation plan that balances scalability with maintainability. Your plan must be clear, specific, and build a foundation for future growth. Follow these guidelines:\n\n"
            
            "ARCHITECTURAL PRINCIPLES:\n"
            "- Modularity: Break down systems into small, focused components with single responsibilities\n"
            "- Granularity: Create many small files rather than few large ones\n"
            "- Decoupling: Ensure minimal dependencies between components\n"
            "- Scalability: Design small, independent services that can scale individually\n"
            "- Maintainability: Favor many simple files over complex monolithic structures\n"
            "- Testability: Small components are easier to test in isolation\n"
            "- Reusability: Smaller components promote code reuse across the application\n"
            "- UI/UX: Always prioritize intuitive user interfaces and seamless user experiences\n\n"
            
            "EXTERNAL RESOURCES INTEGRATION:\n"
            "- When Zinley crawler data is provided, design robust interfaces for data consumption\n"
            "- Implement proper error handling and data validation\n"
            "- Consider caching strategies and fallback mechanisms\n"
            "- Example: 'The DataService in src/services/DataService.js will handle crawler data with retry logic and validation'\n\n"
            
            "COMPONENT BREAKDOWN:\n"
            "IMPORTANT: Only include sections that are relevant to the current task. Do not include all sections if they are not appropriate for the task at hand.\n\n"
            
            "1.GOAL:\n"
            "- Define the goal overview what need to be implemented in 2-3 sentences\n"

            "2. EXISTING FILES ANALYSIS (only mention relevant files):\n"
            "- For each relevant existing file:\n"
            "  * Current purpose and responsibilities\n"
            "  * Required modifications to support new features\n"
            "  * Dependencies and integration points\n"
            "  * MANDATORY: Specify EXACTLY which files need to be updated or modified\n"
            "  * MANDATORY: List all changes required for each file with specific details\n"
            
            "3. NEW COMPONENTS AND FILES:\n\n"
            
            "DIRECTORY STRUCTURE (CRITICAL):\n"
            "- MANDATORY: Provide a tree structure showing ONLY:\n"
            "  2. Files being moved (showing source and destination)\n"
            "- DO NOT include unchanged existing files\n"
            "- Example:\n"
            "```plaintext\n"
            "project_main_folder/\n"
            "├── src/\n"
            "│   ├── components/\n"
            "│   │   └── LoginForm.js       # New component\n"
            "│   ├── services/\n"
            "│   │   └── ApiService.js      # New API client\n"
            "│   └── utils/\n"
            "│       └── validators.js      # Moved from: helpers/validation.js\n"
            "```\n\n"
            
            "COMPONENT DESIGN:\n"
            "- For each new component/module:\n"
            "  * Purpose and responsibilities\n"
            "  * Integration with other components\n"
            "- MANDATORY: Ensure component structure promotes modularity with clear separation of concerns\n"
            "- MANDATORY: Define interfaces between components to minimize coupling\n"
            "- MANDATORY: Specify reusable components that can be shared across features\n\n"
            
            "4. IMPLEMENTATION ORDER:\n"
            "- Organize implementation in a logical sequence:\n"
            "  * Start with core utilities and services\n"
            "  * Then build main components\n"
            "  * Finally integrate everything together\n"
            "- For each step, list files in implementation order\n\n"
            
            "5. FEATURES TO IMPLEMENT (CRITICAL):\n"
            "- List all core features that must be implemented in this iteration\n"
            "- Example: 'User Authentication (Critical): Allow users to register and login. Requirements: Email/password registration, secure password storage, session management. Acceptance: User can register, login, and access protected routes'\n\n"
            
            "6. CORE UI/UX FLOW DESCRIPTION:\n"
            "- Describe the primary success path for the main user goal\n"
            "- Outline the sequence of logical steps including:\n"
            "  * User actions (clicks, form submissions, etc.)\n"
            "  * System responses and screen transitions\n"
            "  * Key decision points in the flow\n"
            "- MANDATORY: Focus only on the core journey without detailing edge cases or error flows\n"
            "- MANDATORY: Ensure the flow is logical and addresses the main user goal\n"
            "- MANDATORY: Keep the flow description concise and focused on critical interactions\n"
            "- MANDATORY: Include only the steps necessary to complete the primary user goal\n"
            
            "7. DEPENDENCIES AND TECHNICAL STACK:\n"
            "- List only NEW dependencies required for this feature (marked as [REQUIRED])\n"
            "- Purpose of each new dependency within the architecture\n"
            "- NEVER request to modify package.json, package-lock.json, yarn.lock, or similar dependency files directly\n"
            "- All dependencies will be installed through the dependency installation process\n"
            "- Installation commands for new dependencies only\n"
            "- DO NOT include version numbers (like x.x.x) unless you are absolutely certain about the specific version needed\n"
            "- When listing required dependencies, only include the package name and installation command without version numbers\n"
            "- Example: '[REQUIRED] react-router-dom: Client-side routing library. Purpose: Navigate between pages. Install: npm install react-router-dom'\n\n"
            
            "8. API INTEGRATION:\n"
            "- For each API endpoint:\n"
            "  * Endpoint URL\n"
            "  * Basic request/response information\n"
            "- Example:\n"
            "  - API: https://api.example.com/data\n"
            "  - Purpose: Fetch user data\n"
            "  - Request: GET with user ID parameter\n\n"
            
            "9. DOCUMENTATION:\n"
            "- ALWAYS include a task to update the existing md file or create a new one if it doesn't exist to document the implementation\n"
            
            "CRITICAL INSTRUCTION: Only include sections that are relevant to the current task. Do not include all sections by default. Focus only on what needs to be done for this specific implementation.\n\n"
            
            "DO NOT INCLUDE:\n"
            "- Future enhancements or improvements\n"
            "- Focus only on what needs to be done now\n"
            "- Any code - only describe what needs to be implemented\n\n"
            
            "IMPORTANT NOTES:\n"
            "- When encountering empty existing files, treat them as placeholders to be filled\n"
            "- For empty projects, establish a viable structure\n"
            "- For existing projects, make targeted additions that align with current structure\n"
            "- NEVER suggest deleting existing files\n"
            f"- Reference the project root path {self.repo.get_repo_path()}:\n{all_file_contents}\n\n"
            
            "CODE FILE SIZE LIMIT:\n"
            "- Keep files concise and focused on specific functionality\n\n"
            
            "IMAGE FORMAT RULES:\n"
            "- ONLY consider PNG, JPG, JPEG, or ICO formats as eligible images for generation\n"
            "- SVG or other vector formats DO NOT count as images needing generation\n"
            "- Only flag image generation if the architecture explicitly requires new raster images\n\n"
            
            "SPECIAL ENDING RULES:\n"
            "- If plan includes BOTH dependencies AND new eligible images: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies needed: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible images needed: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible images: No special ending"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original implementation guidelines strictly. No additional crawling or API calls needed."})

        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE -  NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"


            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is the most picked relevant file that may related for this task, analysizing and use it properly. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})


        all_attachment_file_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            self.conversation_history.append({"role": "user", "content": f"User has attached files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the user prompt, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})

        if assets_link or image_files:
            image_detail_prompt = (
                "Analyze each image in detail according to user requirements.\n\n"
                "For each image, describe visual elements (shapes, colors, layout), "
                "content (text, fonts, icons), implementation details (dimensions, structure), "
                "and purpose (replica vs inspiration). Description should enable "
                "implementation without the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, providing comprehensive specifications for all visual elements, content, measurements, and implementation requirements. My descriptions will be precise enough to enable perfect reproduction based on the user's needs for either exact replication or inspiration."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Create a focused implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"Use correct OS-specific paths and separators.\n\n"
            "SPECIAL ENDING RULES:\n"
            "- If plan includes BOTH dependencies AND new eligible images: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies needed: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible images needed: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible images: No special ending"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)

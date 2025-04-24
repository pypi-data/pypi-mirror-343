import os
import sys
from datetime import datetime
import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class BugFixingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, crawl_logs, file_attachments, assets_link):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### `SnowX` is initializing setup with provided instructions and context")

        prompt = f"""You are an expert software engineer specializing in debugging and fixing code issues. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. CRITICAL: The SEARCH section MUST match the existing code with EXACT precision - every character, whitespace, indentation, newline, and comment must be identical.
                   - If the file contains code or other data wrapped/escaped in json/xml/quotes or other containers, you need to propose edits to the literal contents of the file, including the container markup.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.
                   - Keep SEARCH/REPLACE blocks concise
                   - Break large changes into a series of smaller blocks that each change a small portion of the file
                   - Include just the changing lines, and a few surrounding lines if needed for uniqueness
                   - Do not include long runs of unchanging lines

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                9. CRITICAL: Never include code markdown formatting, syntax highlighting, or any other decorative elements. Code must be provided in its raw form.

                10. STRICTLY FORBIDDEN: Do not hallucinate, invent, or make assumptions about code. Only provide concrete, verified code changes based on the actual codebase.

                11. MANDATORY: Code must be completely plain without any formatting, annotations, explanations or embellishments. Only pure code is allowed.

                12. SEARCH/REPLACE blocks will only replace the first match occurrence. Include multiple unique blocks if needed.

                13. Only create SEARCH/REPLACE blocks for files that have been added to the chat.

                14. To move code within a file, use 2 SEARCH/REPLACE blocks:
                    - One to delete it from its current location
                    - One to insert it in the new location

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Bug fix plan: {instructions['Implementation_plan']} and original raw request, use if Implementation_plan missing some pieces: {instructions['original_prompt']}"},
            {"role": "assistant", "content": "Understood!"},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "Understood!"},
        ]

        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this context when implementing changes."})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This is supported data for this entire process, use it if appropriate: {crawl_logs}"})
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

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the original Bug fix plan, and use these images as support!"}]

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



    async def get_coding_request(self, file, techStack, codingModel):
        """
        Get bug fixing response for the given instruction and context from Azure OpenAI.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be fixed.
            prompt (str): The specific task or instruction for bug fixing.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        is_svg = file_name.lower().endswith('.svg')

        # Read current file content
        current_file_content = read_file_content(file)
        if current_file_content:
            self.conversation_history.append({"role": "user", "content": f"Here is the current content of {file_name} that needs to be fixed:\n{current_file_content}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this file content as context for the bug fixes."})

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed fixes."

        user_prompt = f"As a world-class, highly experienced {'SVG designer' if is_svg else f'{techStack} developer'} specializing in debugging and bug fixing, implement the following task with utmost efficiency and precision:\n"

        if is_svg:
            user_prompt += (
                "Fix SVG issues while maintaining project's existing visual style and use case.\n"
                "For SVG bug fixes:\n"
                "- Maintain official colors, proportions and brand identity\n"
                "- Follow brand guidelines strictly\n"
                "- Fix SVG code performance and file size issues\n"
                "- Resolve cross-browser compatibility problems\n"
                "- Fix semantic element names and grouping\n"
                "- Correct ARIA labels and accessibility attributes\n"
                "- Debug animations and transitions if needed\n"
            )
        else:
            user_prompt += (
                f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}\n"
                "For Bug Fixing:\n"
                "- Fix only reported issues and errors\n"
                "- Maintain existing codebase structure and patterns\n"
                "- Focus on specific problems mentioned\n"
                "- Avoid introducing new features or changes\n"
                "- Keep fixes minimal and targeted\n"
                "\nFix Categories to Consider:\n"
                "- Logic & Flow Issues:\n"
                "  • Fix incorrect control flow\n" 
                "  • Debug edge case handling\n"
                "  • Correct validation errors\n"
                "  • Fix state management bugs\n"
                "- Code Quality Issues:\n"
                "  • Fix inefficient implementations\n"
                "  • Debug performance bottlenecks\n"
                "  • Correct error handling\n"
                "  • Fix memory leaks\n"
                "- Integration Issues:\n"
                "  • Fix API integration bugs\n"
                "  • Debug data flow problems\n"
                "  • Fix dependency issues\n"
                "  • Correct interface errors\n"
                "- UI/UX Issues:\n"
                "  • Fix layout and styling bugs\n"
                "  • Debug rendering problems\n"
                "  • Fix interaction issues\n"
                "  • Correct accessibility errors\n"
                "\nGuidelines:\n"
                "- Keep existing functionality intact\n"
                "- Maintain code style and conventions\n"
                "- Preserve business logic and rules\n"
                "- Focus on stability and reliability\n"
                "- Fix root causes not just symptoms\n"
                "- Add proper error handling\n"
                "- Ensure backwards compatibility\n"
            )

        user_prompt += f"{lazy_prompt}\n" if not is_svg else ""
        user_prompt += f"Providing bug fixes for this {file_name}.\n"
        user_prompt += "NOTICE: Your response must contain ONLY SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
            content = response.choices[0].message.content
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if lines and "> REPLACE" in lines[-1]:
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                logger.info(" #### Extending response - generating additional context (1/10)")
                # The response was cut off, need to continue
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue ONLY from where you left off without repeating or overlapping any preivous content, do no re-generate the same content which already there from last response for this coding file. Do NOT start from the beginning. Only provide the missing part that completes the last SEARCH/REPLACE block. Ensure the continuation ends with '>>>>>>> REPLACE'."
                
                # Store the initial incomplete response
                initial_content = content
                current_content = initial_content
                
                # Track conversation temporarily but don't add to history yet
                temp_conversation = self.conversation_history.copy()
                temp_conversation.append({"role": "assistant", "content": initial_content})
                temp_conversation.append({"role": "user", "content": continuation_prompt})
                
                # Make up to 10 attempts to get a complete response
                max_attempts = 10
                for attempt in range(1, max_attempts + 1):
                    logger.info(f" #### Extending response - generating additional context ({attempt}/10)")
                    
                    continuation_response = await self.ai.coding_prompt(temp_conversation, 4096, 0.2, 0.1)
                    continuation_content = continuation_response.choices[0].message.content
                    continuation_lines = [line.strip() for line in continuation_content.splitlines() if line.strip()]
                    
                    # Add to the accumulated content
                    current_content += continuation_content
                    
                    # Update temporary conversation
                    temp_conversation.append({"role": "assistant", "content": continuation_content})
                    
                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                        # Successfully completed the response
                        self.conversation_history.append({"role": "assistant", "content": current_content})
                        return current_content
                    
                    # Prepare for next attempt if needed
                    if attempt < max_attempts:
                        temp_conversation.append({"role": "user", "content": continuation_prompt})
                
                # If we've reached this point, we've made all attempts and still don't have a complete response
                # Add the best we have to the conversation history
                self.conversation_history.append({"role": "assistant", "content": current_content})
                logger.error(f"  `SnowX` encountered an error while getting bug fix request - incomplete response after {max_attempts} attempts")
                return current_content

        except Exception as e:
            logger.error(f" `SnowX` encountered an error while getting bug fix request")
            logger.error(f" {e}")
            raise


    async def get_coding_requests(self, file, techStack):
        """
        Get bug fixing responses for a file from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be fixed.
            prompt (str): The bug fixing task prompt.

        Returns:
            str: The code response or error reason.
        """
        return await self.get_coding_request(file, techStack)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.debug("\n #### `SnowX` is clearing conversation history")
        self.conversation_history = []

    def destroy(self):
        """De-initialize and destroy this instance."""
        logger.debug("\n #### `SnowX` is being destroyed")
        self.repo = None
        self.conversation_history = None
        self.ai = None

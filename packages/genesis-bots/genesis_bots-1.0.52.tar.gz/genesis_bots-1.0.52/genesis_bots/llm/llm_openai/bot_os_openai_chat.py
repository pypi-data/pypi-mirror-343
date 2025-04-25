'''
  Implements OpenAI interface based on Chat Completions API
'''
import json
import os, uuid, re
from collections import deque
import datetime
import time
import random
import types
from threading import Lock, Thread, local as ThreadLocal
from typing_extensions import override
import traceback

from genesis_bots.core import global_flags
from genesis_bots.core.bot_os_assistant_base import BotOsAssistantInterface, execute_function
from genesis_bots.core.bot_os_input import BotOsInputMessage, BotOsOutputMessage
from genesis_bots.core.bot_os_defaults import BASE_BOT_INSTRUCTIONS_ADDENDUM, BASE_BOT_DB_CONDUCT_INSTRUCTIONS,BASE_BOT_PROCESS_TOOLS_INSTRUCTIONS,BASE_BOT_SLACK_TOOLS_INSTRUCTIONS
from genesis_bots.llm.llm_openai.openai_utils import get_openai_client
from genesis_bots.core.logging_config import logger

thread_local = ThreadLocal()

class BotOsAssistantOpenAIChat(BotOsAssistantInterface):
    all_functions_backup = None

    _shared_done_map = {}  # Maps bot names to their completed runs
    _shared_tool_failure_map = {}  # Maps run hashes to failure counts and timestamps

    # Class-level timestamp for all instances to share
    _last_bots_active_update = datetime.datetime.now() - datetime.timedelta(minutes=1)

    def __init__(self, name:str, instructions:str,
                 tools:list[dict] = None, available_functions=None, files=None,
                 update_existing=False, log_db_connector=None, bot_id='default_bot_id',
                 bot_name='default_bot_name', all_tools:list[dict]=None,
                 all_functions=None,all_function_to_tool_map=None, skip_vectors=False,
                 assistant_id = None) -> None:
        logger.debug("BotOsAssistantOpenAIChat:__init__")
        super().__init__(name, instructions, tools, available_functions, files,
                         update_existing, skip_vectors=False, bot_id=bot_id, bot_name=bot_name)

        model_name = os.getenv("OPENAI_MODEL_NAME", default="gpt-4o-2024-11-20")
        self.client = get_openai_client()

        name = bot_id
        logger.info(f"-> OpenAI Model == {model_name}")
        self.file_storage = {}
        self.available_functions = available_functions or {}
        self.all_tools = all_tools or []
        self.all_functions = all_functions or {}
        if BotOsAssistantOpenAIChat.all_functions_backup == None and all_functions is not None:
            BotOsAssistantOpenAIChat.all_functions_backup = all_functions
        self.all_function_to_tool_map = all_function_to_tool_map or {}
        self.log_db_connector = log_db_connector
        my_tools = tools or []
        self.my_tools = my_tools
        self.clear_access_cache = False

        self.allowed_types_search = [".c", ".cs", ".cpp", ".doc", ".docx", ".html", ".java", ".json", ".md", ".pdf", ".php", ".pptx", ".py", ".rb", ".tex", ".txt", ".css", ".js", ".sh", ".ts"]
        self.allowed_types_code_i = [".c", ".cs", ".cpp", ".doc", ".docx", ".html", ".java", ".json", ".md", ".pdf", ".php", ".pptx", ".py", ".rb", ".tex", ".txt", ".css", ".js", ".sh", ".ts", ".csv", ".jpeg", ".jpg", ".gif", ".png", ".tar", ".xlsx", ".xml", ".zip"]

        self.instructions = instructions
        self.tools = my_tools
        
        genbot_internal_project_and_schema = os.getenv('GENESIS_INTERNAL_DB_SCHEMA','None')
        if genbot_internal_project_and_schema is not None:
            genbot_internal_project_and_schema = genbot_internal_project_and_schema.upper()
        self.genbot_internal_project_and_schema = genbot_internal_project_and_schema
        if genbot_internal_project_and_schema == 'None':
            logger.info("ENV Variable GENESIS_INTERNAL_DB_SCHEMA is not set.")

        self.db_schema = genbot_internal_project_and_schema.split('.')
        self.internal_db_name = self.db_schema[0]
        self.internal_schema_name = self.db_schema[1]

        my_assistant = None
        self.assistant = types.SimpleNamespace()
        self.assistant.id = "no_assistant"

        # Initialize shared done_map for this bot name
        if name not in self.__class__._shared_done_map:
            self.__class__._shared_done_map[name] = {}
        self.done_map = self.__class__._shared_done_map[name]

        if name not in self.__class__._shared_tool_failure_map:
            self.__class__._shared_tool_failure_map[name] = {}
        self.tool_failure_map = self.__class__._shared_tool_failure_map[name]

    @override
    def is_active(self) -> deque:
        return deque()

    @override
    def is_processing_runs(self) -> deque:
        return deque()

    @override
    def get_done_map(self) -> dict:
        return self.done_map

    def create_thread(self) -> str:
        thread_id = "completion_thread_" + str(uuid.uuid4())
        logger.info(f"{self.bot_name} openai completion new_thread -> {thread_id}")
        return thread_id

    def _upload_files(self, files, thread_id=None):
        file_ids = []
        file_map = []
        for f in files:
            original_file_location = f
            file_name = original_file_location.split('/')[-1]
            new_file_location = f"./runtime/downloaded_files/{thread_id}/{file_name}"

            # Convert .JPEG extension to .JPG if present
            if file_name.upper().endswith('.JPEG'):
                new_file_location = new_file_location[:-5] + '.jpg'
                file_name = file_name[:-5] + '.jpg'

            os.makedirs(f"./runtime/downloaded_files/{thread_id}", exist_ok=True)
            with open(original_file_location, 'rb') as source_file:
                with open(f"./runtime/downloaded_files/{thread_id}/{file_name}", 'wb') as dest_file:
                    dest_file.write(source_file.read())

            # Validate file type is allowed
            file_ext = os.path.splitext(new_file_location)[1].lower()
            allowed_types = self.allowed_types_search + self.allowed_types_code_i
            if not any(file_ext.endswith(ext) for ext in allowed_types):
                logger.warning(f"Skipping file {f} - extension {file_ext} not in allowed types")
                continue

            fo = open(new_file_location,"rb")
            file = self.client.files.create(file=(file_name, fo), purpose="assistants")

            file_ids.append(file.id)

            # make a copy based on the new openai file.id as well in case the bot needs it by this reference later
            new_file_location_file_id = f"./runtime/downloaded_files/{thread_id}/{file.id}"
            with open(original_file_location, 'rb') as source_file:
                with open(new_file_location_file_id, 'wb') as dest_file:
                    dest_file.write(source_file.read())


            self.file_storage[file.id] = new_file_location
            file_map.append({'file_id': file.id, 'file_name': file_name})

        logger.debug(f"BotOsAssistantOpenAIChat:_upload_files - uploaded {len(file_ids)} files")
        return file_ids, file_map

    def preprocess(self, input_message, bot_os_thread):
        '''look for special directives in the incoming message'''
        
        # Check for thread commands
        if input_message.msg.endswith('!thread'):
            input_message.msg = input_message.msg.replace('!thread', f'SYSTEM MESSAGE: The User has requested to know what thread ID is running. Respond by telling them that the current thread ID is: {bot_os_thread.thread_id}')
        
        thread_switch_match = re.match(r'^!thread\s+(\S+)(?:\s+(.*))?$|^(.*?)\s*!thread\s+(\S+)$', input_message.msg)
        if thread_switch_match:
            new_thread_id = thread_switch_match.group(1)
            old_thread_id = bot_os_thread.thread_id
            
            # Get rest of message, defaulting to continuation prompt if empty
            remaining_msg = thread_switch_match.group(2)
            if remaining_msg is not None:
                remaining_msg = remaining_msg.strip()
            input_message.msg = remaining_msg if remaining_msg else "Please continue our previous conversation."
            
            logger.info(f"{self.bot_name} switching thread from {old_thread_id} to {new_thread_id}")
            
            # Update thread ID
            bot_os_thread.thread_id = new_thread_id
            
            # Try to load existing messages from the new thread
            try:
                git_path = os.getenv('GIT_PATH', os.path.join(os.getcwd(), 'bot_git'))
                storage_file = os.path.join(git_path, 'threads', self.bot_id, f"{new_thread_id}.json")
                if os.path.exists(storage_file):
                    with open(storage_file, 'r') as f:
                        thread_data = json.load(f)
                        bot_os_thread.messages = thread_data.get('messages', [])
                        bot_os_thread.fast_mode = thread_data.get('fast_mode', False)
                        bot_os_thread.run_messg_count = thread_data.get('run_messg_count', 0)
                    input_message.msg = f"SYSTEM MESSAGE: Switched to existing thread {new_thread_id}. " + input_message.msg
                    logger.info(f"{self.bot_name} loaded existing thread {new_thread_id}")
                else:
                    # Start fresh message history if no existing thread found
                    bot_os_thread.messages = []
                    input_message.msg = f"SYSTEM MESSAGE: Started new thread {new_thread_id}. " + input_message.msg
                    logger.info(f"{self.bot_name} starting new thread {new_thread_id}")
            except Exception as e:
                logger.error(f"Error loading thread {new_thread_id}: {e}")
                bot_os_thread.messages = []
                input_message.msg = f"SYSTEM MESSAGE: Error loading thread {new_thread_id}, starting fresh. Error: {str(e)}. " + input_message.msg
        
        # Existing preprocessing
        if input_message.msg.endswith('<<!!FAST_MODE!!>>') or bot_os_thread.is_fast_mode():
            input_message.msg = input_message.msg.rstrip('<<!!FAST_MODE!!>>').rstrip()

        if input_message.msg.endswith(') says: !model') or input_message.msg=='!model':
            if bot_os_thread.is_fast_mode():
                input_message.msg = input_message.msg.replace ('!model',f'SYSTEM MESSAGE: The User has requested to know what LLM model is running.  Respond by telling them that the system is running in fast mode and that the current model is: { os.getenv("OPENAI_FAST_MODEL_NAME", default="gpt-4o-mini")}')
            else:
                input_message.msg = input_message.msg.replace ('!model',f'SYSTEM MESSAGE: The User has requested to know what LLM model is running.  Respond by telling them that the system is running in smart mode and that current model is: { os.getenv("OPENAI_MODEL_NAME", default="gpt-4o-2024-11-20")}')

        if input_message.msg.endswith(') says: !fast on') or input_message.msg == '!fast on':
            bot_os_thread.set_fast_mode(True)
            input_message.metadata['fast_mode'] = 'TRUE'
            input_message.msg = input_message.msg.replace('!fast on', f"SYSTEM MESSAGE: Tell the user that Fast mode activated for this thread. Model is now {os.getenv('OPENAI_FAST_MODEL_NAME', 'gpt-4o-mini')}")

        elif input_message.msg.endswith(') says: !fast off') or input_message.msg == '!fast off':
            bot_os_thread.set_fast_mode(False)
            input_message.msg = input_message.msg.replace('!fast off', f"SYSTEM MESSAGE:Tell the user that Fast mode deactivated for this thread. Model is now {os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-2024-11-20')}")

        elif bot_os_thread.is_fast_mode():
            input_message.metadata['fast_mode'] = 'TRUE'
            
    def get_model(self, input_message, bot_os_thread):
        '''calculate model name from message content and environment variables'''
        
        model_name = (
            os.getenv("OPENAI_FAST_MODEL_NAME", "gpt-4o-mini")
            if bot_os_thread.is_fast_mode()
            else os.getenv("OPENAI_MODEL_NAME", "gpt-4o-2024-11-20")
        )
        if '!o1!' in input_message.msg or input_message.metadata.get('o1_override', False)==True:
            model_name = 'o1'
            input_message.msg = input_message.msg.replace('!o1!', '').strip()
            input_message.metadata['o1_override'] = True
        elif '!o3-mini!' in input_message.msg or input_message.metadata.get('o3_override', False)==True:
            model_name = 'o3-mini'
            input_message.msg = input_message.msg.replace('!o3!', '').strip()
            input_message.metadata['o3_override'] = True
            input_message.metadata['reasoning_effort'] = 'low'
        elif '!o3-mini-low!' in input_message.msg or input_message.metadata.get('o3_mini_low_override', False)==True:
            model_name = 'o3-mini'
            input_message.msg = input_message.msg.replace('!o3-mini-low!', '').strip()
            input_message.metadata['o3_mini_low_override'] = True
            input_message.metadata['reasoning_effort'] = 'low'
        elif '!o3-mini-medium!' in input_message.msg or input_message.metadata.get('o3_mini_medium_override', False)==True:
            model_name = 'o3-mini'
            input_message.msg = input_message.msg.replace('!o3-mini-medium!', '').strip()
            input_message.metadata['o3_mini_medium_override'] = True
            input_message.metadata['reasoning_effort'] = 'medium'
        elif '!o3-mini-high!' in input_message.msg or input_message.metadata.get('o3_mini_high_override', False)==True:
            model_name = 'o3-mini'
            input_message.msg = input_message.msg.replace('!o3-mini-high!', '').strip()
            input_message.metadata['o3_mini_high_override'] = True
            input_message.metadata['reasoning_effort'] = 'high'
        return model_name

    def get_attachments(self, input_message):
        '''add note about uploaded files to message'''
        
        attachments = []
        if input_message.files is not None and len(input_message.files) > 0:
            files_info = "\n[User has attached the following files:\n"
            for file in input_message.files:
                files_info += f"- {file}\n"
            files_info += "You can reference these files in future calls using their full paths as shown above.]"
            input_message.msg += files_info
            attachments = input_message.files
        return attachments

    def get_openai_messages(self, bot_os_thread, model_name, input_message=None):
        '''append new incoming message to the existing thread or create a new one'''
        
        if bot_os_thread.messages:
            # Get existing messages and append new user message
            openai_messages = bot_os_thread.messages
            if input_message:
                openai_messages.append({
                    "role": "user",
                    "content": input_message.msg
                })
        else:
            # Initialize new message thread
            openai_messages = [
                {
                    "role": "user" if model_name in ['o1', 'o1-mini'] else "system",
                    "content": self.instructions
                },
                {
                    "role": "user",
                    "content": input_message.msg
                }
            ]
            bot_os_thread.messages = openai_messages
            
        openai_messages[0]["content"] = self.instructions
        return openai_messages

    def call_openai(self, openai_messages, model_name, params, thread_id, output_stream, output_event):
        '''call requested OpenAI model and return the response as a tuple: (content, usage, tool_calls)'''

        content = ''
        usage = None
        tool_calls = []

        stream = self.client.chat.completions.create(
            model=model_name,
            **({'tools': self.tools} if self.tools and len(self.tools) > 0 else {}),
            messages=openai_messages,
            stream=True,
            stream_options={"include_usage": True},
            **params
        )

        # Collect streaming response and periodically flush deltas to user (but not too often)
        last_flush_time = time.monotonic()
        flush_interval = 1 # sec

        for chunk in stream:
            if len(content) > 0 and (time.monotonic() - last_flush_time) >= flush_interval:
                output_event(status='in_progress', output=output_stream + content + " 💬", messages=None)
                last_flush_time = time.monotonic()

            if chunk.usage != None and chunk.choices == []:
                usage = chunk.usage
                continue

            if (len(chunk.choices) > 0 and hasattr(chunk.choices[0].delta, 'tool_calls') and
                chunk.choices[0].delta.tool_calls is not None):
                tc_chunk_list = chunk.choices[0].delta.tool_calls
                for tc_chunk in tc_chunk_list:
                    if len(tool_calls) <= tc_chunk.index:
                        tool_calls.append({"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
                    tc = tool_calls[tc_chunk.index]
                    if tc_chunk.id is not None:
                        tc['id'] += tc_chunk.id
                    if tc_chunk.function is not None and tc_chunk.function.name is not None:
                        tc['function']['name'] += tc_chunk.function.name
                    if tc_chunk.function is not None and tc_chunk.function.arguments is not None:
                        tc['function']['arguments'] += tc_chunk.function.arguments

            if len(chunk.choices) > 0 and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                delta_content = chunk.choices[0].delta.content
                if delta_content is not None and isinstance(delta_content, str):
                    content += delta_content

        return content, usage, tool_calls

    def decode_tool_response(self, run, thread_id, func_name, func_args, func_response):
        '''postprocess response received from a tool function call'''
        
        new_response = func_response
        if isinstance(func_response, dict) and len(func_response) == 1 and 'error' in func_response:
            # Handle both dictionary access patterns
            error_msg = func_response.get('error')  # Direct dict access
            if error_msg is None and isinstance(func_response.get(0), dict):  # List-style dict access
                error_msg = func_response[0].get('error')
            
            if error_msg is not None:
                new_response = {"success": False, "error": error_msg}
                func_response = new_response
                logger.info(f'openai submit_tool_outputs list with error converted to: {func_response}')

        if isinstance(func_response, str):
            try:
                new_response = {"success": False, "error": func_response}
                func_response = new_response
                logger.info(f'openai submit_tool_outputs string response converted call: {func_name=} {func_response=}')
            except:
                logger.info(f'openai submit_tool_outputs string response converted call to JSON.')

        if isinstance(func_response, dict) and func_response.get('success') == False and 'error' in func_response:
            # Create a string hash of the run details
            run_details_str = f"{run.id}_{thread_id}_{func_name}_{func_args}_{func_response}"
            run_hash = str(hash(run_details_str))

            if run_hash in self.tool_failure_map:
                self.tool_failure_map[run_hash]["fail_count"] += 1
                if self.tool_failure_map[run_hash]["fail_count"] == 2:
                    func_response['warning'] = "Note: Please do not retry this failed operation more than twice to avoid getting stuck in a retry loop. "
                if self.tool_failure_map[run_hash]["fail_count"] >= 3:
                    func_response = {
                       "success": False,
                       "message": "The tool call has repeatedly failed, please inform the user that this tool call has failed and cannot be immediately retried."
                    }
                if self.tool_failure_map[run_hash]["fail_count"] > 3:
                    err = f"Tool call has failed {self.tool_failure_map[run_hash]['fail_count']} times, cancelling request. {func_name=} {thread_id=} {run.id=}"
                    logger.warning(err)
                    raise Exception(err)
            else:
                self.tool_failure_map[run_hash] = {
                   "first_fail_timestamp": datetime.datetime.now(),
                   "fail_count": 1
                }
                
            # Randomly clean old failures from map (1% chance)
            if random.randint(0,100) >= 0:
                current_time = datetime.datetime.now()
                # Create list of keys to remove to avoid modifying dict during iteration
                keys_to_remove = []
                for run_hash, failure_data in self.tool_failure_map.items():
                    time_diff = current_time - failure_data["first_fail_timestamp"]
                    if time_diff.total_seconds() > 3600: # 60 minutes
                        keys_to_remove.append(run_hash)

                # Remove old entries
                for key in keys_to_remove:
                    del self.tool_failure_map[key]

        return func_response

    def postprocess_tool_response(self, func_name, func_args, func_response):
        try:
            if (func_name == '_modify_slack_allow_list' and
                (func_response.get('success', False) == True or func_response.get('Success', False) == True)):
                self.clear_access_cache = True

            if ((func_name == 'remove_tools_from_bot' or func_name == 'add_new_tools_to_bot') and
                (func_response.get('success',False)==True or func_response.get('Success',False)==True)):
                target_bot = json.loads(func_args).get('bot_id',None)
                if target_bot is not None:
                    logger.info(f"Bot tools for {target_bot} updated.")

            if (func_name == 'update_bot_instructions' and
                (func_response.get('success', False) == True or func_response.get('Success', False) == True)):
                new_instructions = func_response.get("new_instructions",None)
                if new_instructions:

                    target_bot = json.loads(func_args).get('bot_id',None)
                    bot_details = func_response.get('new_bot_details',None)
                    if bot_details is not None:
                        func_response.pop("new_bot_details", None)

                    if target_bot is not None:
                        instructions = new_instructions + "\n" + BASE_BOT_INSTRUCTIONS_ADDENDUM
                        instructions += f'\nNote current settings:\nData source: {global_flags.source}\nYour bot_id: {bot_details["bot_id"]}.\n'
                        if global_flags.runner_id is not None:
                            instructions += f'Runner_id: {global_flags.runner_id}\n'
                        if bot_details["slack_active"]=='Y':
                            instructions += "\nYour slack user_id: "+bot_details["bot_slack_user_id"]
                        if "snowflake_tools" in bot_details["available_tools"]:

                            workspace_schema_name = f"{global_flags.project_id}.{target_bot.replace(r'[^a-zA-Z0-9]', '_').replace('-', '_').replace('.', '_')}_WORKSPACE".upper()
                            instructions += f"\nYou have a workspace schema created specifically for you named {workspace_schema_name} that the user can also access. You may use this schema for creating tables, views, and stages that are required when generating answers to data analysis questions. Only use this schema if asked to create an object. Always return the full location of the object."
                            instructions += "\n" + BASE_BOT_DB_CONDUCT_INSTRUCTIONS

                        #add process mgr tools instructions
                        if "process_manager_tools" in bot_details["available_tools"] or "notebook_manager_tools" in bot_details["available_tools"]:
                            instructions += "\n" + BASE_BOT_PROCESS_TOOLS_INSTRUCTIONS

                        if "slack_tools" in bot_details["available_tools"]:
                            instructions += "\n" + BASE_BOT_SLACK_TOOLS_INSTRUCTIONS

                        logger.info(f"Bot instructions for {target_bot} updated, len={len(instructions)}")

        except Exception as e:
            logger.info(f'postprocess_tool_response(): {func_response=} {e=}')

    def record_tool_call(self, run, thread_id, func_name, func_args, tool_call_id, output_stream, chat_history, output_event, bot_os_thread=None):
        chat_history(message_type='Tool Call', message_payload=func_name+"("+func_args+")",
                     message_metadata={'tool_call_id':tool_call_id, 'func_name':func_name, 'func_args':func_args}, bot_os_thread=bot_os_thread)
                                    
        logger.telemetry('execute_function:', thread_id, self.bot_id, run.metadata.get('user_email', 'unknown_email'),
                         os.getenv("BOT_OS_DEFAULT_LLM_ENGINE", ""), func_name, 'arg len:'+str(len(func_args)))

        function_name_pretty = re.sub(r'(_|^)([a-z])', lambda m: m.group(2).upper(), func_name).replace('_', '')
        if function_name_pretty == "QueryDatabase" or function_name_pretty == "DataExplorer" or function_name_pretty == "SearchMetadata":
            try:
                db_connector = json.loads(func_args).get('connection_id')
                if db_connector:
                    function_name_pretty = f"{function_name_pretty}: {db_connector}"
            except:
                pass
        try:
            func_args_dict = json.loads(func_args)
            if 'action' in func_args_dict:
                action = func_args_dict['action']
                # Convert underscore separated action to camel case
                action = ''.join(word.capitalize() for word in action.split('_'))
                function_name_pretty = f"{function_name_pretty}: {action}"
        except:
            pass

        if output_stream.endswith('\n'):
            output_stream += "\n"
        else:
            output_stream += "\n\n"
        output_stream += f"🧰 Using tool: _{function_name_pretty}_...\n\n"

        output_event(status=run.status, output=output_stream + " 💬", messages=None)
        return output_stream

    def run_tool_function(self, run, thread_id, func_name, func_args, tool_call_id, status_callback):
        '''run openai-requested tool function'''
        
        func_args_dict = json.loads(func_args)

        if "image_data" in func_args_dict:
            func_args_dict["image_data"] = self.file_storage.get(func_args_dict["image_data"].removeprefix('/mnt/data/'))
            func_args = json.dumps(func_args_dict)

        if 'file_name' in func_args_dict:
            try:
                if func_args_dict['file_name'].startswith('/mnt/data/'):
                    file_id = func_args_dict['file_name'].split('/')[-1]
                    new_file_location = self.file_storage[file_id]
                    if '/' in new_file_location:
                        new_file_location = new_file_location.split('/')[-1]
                    func_args_dict['file_name'] = new_file_location
                    func_args = json.dumps(func_args_dict)
            except Exception as e:
                logger.warn(f"Failed to update file_name in func_args_dict with error: {e}")

        if 'openai_file_id' in func_args_dict:
            try:
                file_id = func_args_dict['openai_file_id'].split('/')[-1]
                existing_location = f"./runtime/downloaded_files/{thread_id}/{file_id}"
                if not os.path.exists(existing_location):
                    # If the file does not exist at the existing location, download it from OpenAI
                    try:
                        os.makedirs(os.path.dirname(existing_location), exist_ok=True)
                        self._download_openai_file(file_id, thread_id)
                    except:
                        pass
            except:
                pass

        self.validate_or_add_function(func_name)

        if func_name not in self.all_functions:
            self.all_functions = BotOsAssistantOpenAIChat.all_functions_backup
            if func_name in self.all_functions:
                logger.info('!! function was missing from self.all_functions, restored from backup, now its ok')
            else:
                logger.info(f'!! function was missing from self.all_functions, restored from backup, still missing func: {func_name}, len of backup={len(BotOsAssistantOpenAIChat.all_functions_backup)}')

        func_response = None
        def callback(resp):
            nonlocal func_response
            func_response = resp
            
        # Execute the tool function
        execute_function(func_name, func_args, self.all_functions, callback,
                         thread_id = thread_id, bot_id=self.bot_id,
                         status_update_callback=status_callback,
                         session_id=self.assistant.id if self.assistant.id is not None else None,
                         input_metadata=run.metadata if run.metadata is not None else None, run_id = run.id)

        func_response = self.decode_tool_response(run, thread_id, func_name, func_args, func_response)
        self.postprocess_tool_response(func_name, func_args, func_response)
        return func_response

    def send_response_to_user(self, run, thread_id, output_stream, model_name, chat_history, output_event, bot_os_thread=None):
        '''send OpenAI response back to user'''
        
        messages = types.SimpleNamespace()
        messages.data = []
        message = types.SimpleNamespace()
        message.content = [
            types.SimpleNamespace(
                type='text',
                text=types.SimpleNamespace(
                    value=output_stream
                )
            )
        ]
        message.run_id = run.id
        message.attachments = []
        message.id = f"msg_{run.id}"
        messages.data.append(message)

        latest_attachments = []
        input_tokens = 0
        output_tokens = 0

        meta = run.metadata

        files_in = self._store_files_locally(latest_attachments, thread_id)
            
        if os.getenv('SHOW_COST', 'false').lower() == 'true':
            if model_name.startswith("gpt-4o"):
                input_cost = 5.000 / 1000000
                output_cost = 15.000 / 1000000
            elif model_name == "gpt-4o-2024-08-06":
                input_cost = 2.500 / 1000000
                output_cost = 10.000 / 1000000
            elif model_name in ["gpt-4o-mini", "gpt-4o-mini-2024-07-18"]:
                input_cost = 0.150 / 1000000
                output_cost = 0.600 / 1000000
            else:
                # Default to gpt-4o prices if model is unknown
                input_cost = 5.000 / 1000000
                output_cost = 15.000 / 1000000
            if hasattr(run, 'usage'):
                total_cost = (run.usage.prompt_tokens * input_cost) + (run.usage.completion_tokens * output_cost)
                output_stream += f'  `${total_cost:.4f}`'
                input_tokens = run.usage.prompt_tokens
                output_tokens = run.usage.completion_tokens

        output_event(status=run.status, output=output_stream, messages=messages, files=files_in)

        chat_history(message_type='Assistant Response', message_payload=output_stream,
                     message_metadata=str(message.content), tokens_in=input_tokens,
                     tokens_out=output_tokens, files=files_in, bot_os_thread=bot_os_thread)
        
        logger.telemetry('add_answer:', thread_id, self.bot_id, run.metadata.get('user_email', 'unknown_email'),
                         os.getenv("BOT_OS_DEFAULT_LLM_ENGINE", ""), input_tokens, output_tokens)

    def add_message(self, input_message:BotOsInputMessage, bot_os_thread, event_callback):
        thread_id = input_message.thread_id

        primary_user = json.dumps({'user_id': input_message.metadata.get('user_id', 'unknown_id'),
                                   'user_name': input_message.metadata.get('user_name', 'unknown_name'),
                                   'user_email': input_message.metadata.get('user_email', 'unknown_email')})

        chat_history_params = {'bot_id': self.bot_id, 'bot_name': self.bot_name, 'thread_id': thread_id,
                               'primary_user': primary_user, 'channel_type': input_message.metadata.get("channel_type", None),
                               'channel_name': input_message.metadata.get("channel", None)}

        def chat_history(bot_os_thread=None, **row):
            self.log_db_connector.insert_chat_history_row(datetime.datetime.now(), bot_os_thread = bot_os_thread, **chat_history_params, **row)

        def output_event(**event):
            event_callback(self.assistant.id, BotOsOutputMessage(thread_id=thread_id, **event, input_metadata=input_message.metadata))

        self.preprocess(input_message, bot_os_thread)
        attachments = self.get_attachments(input_message)
        model_name = self.get_model(input_message, bot_os_thread)
        run_id = thread_id + "_" + str(datetime.datetime.now().timestamp())
        openai_messages = self.get_openai_messages(bot_os_thread, model_name, input_message)
        if '!o3-mini!' in openai_messages[0]["content"]:
            model_name = 'o3-mini'

        params = {'reasoning_effort': input_message.metadata.get('reasoning_effort', 'low')} if model_name == 'o3-mini' else {}
        response_format = input_message.metadata.get('response_format')
        if response_format:
            params['response_format'] = response_format
        temperature = input_message.metadata.get('temperature')
        if temperature:
            params['temperature'] = temperature
        if response_format:
            params['response_format'] = response_format

        run = types.SimpleNamespace(
            id = run_id,
            status = 'in_progress',
            metadata = input_message.metadata,
            created_at = datetime.datetime.now()
        )

        chat_history(message_type='User Prompt', message_payload=input_message.msg,
                     message_metadata=input_message.metadata, files=attachments, bot_os_thread=bot_os_thread)

        output_stream = ''
        
        while True:
            try:
                content, usage, tool_calls = self.call_openai(openai_messages, model_name, params,
                                                              thread_id, output_stream, output_event)

            except Exception as e:
                if bot_os_thread.recover(e):
                    openai_messages = self.get_openai_messages(bot_os_thread, model_name)
                    continue

                logger.error(f"Error during OpenAI streaming call: {e}")
                input_message.metadata['openai_error_info'] = str(e)        

                run.status = "completed"
                run.completed_at = datetime.datetime.now()

                self.send_response_to_user(run, thread_id, output_stream + str(e), model_name, chat_history, output_event, bot_os_thread=bot_os_thread)
                break

            if not tool_calls:
                bot_os_thread.messages.append({"role": "assistant", "content": content})
                
                run.status = "completed"
                run.completed_at = datetime.datetime.now()
                run.usage = usage

                self.send_response_to_user(run, thread_id, output_stream + content, model_name, chat_history, output_event, bot_os_thread=bot_os_thread)
                break

            # LLM requesting us to call tool function(s) and send back the result
        
            bot_os_thread.messages.append({"role": "assistant", "content": content if content != '' else None, "tool_calls": tool_calls})
            output_stream += content

            if output_stream:
                output_event(status=run.status, output=output_stream + " 💬", messages=None)

            results = []
            for tool_call in tool_calls:
                func_name = tool_call['function']['name']
                func_args = tool_call['function']['arguments']
                tool_call_id = tool_call['id']

                if bot_os_thread.stop_signal:
                    logger.info(f'bot={self.bot_id} {thread_id=} received stop signal')
                    run.status = 'completed'
                    run.completed_at = datetime.datetime.now()
                    self.send_response_to_user(run, thread_id, output_stream + f'..stopped!', model_name,
                                               chat_history, output_event, bot_os_thread=bot_os_thread)
                    break

                output_stream = self.record_tool_call(run, thread_id, func_name, func_args, tool_call_id,
                                                      output_stream, chat_history, output_event, bot_os_thread=bot_os_thread)

                # tool function may use below callback to update user on its progress
                def status_callback(session_id, update_message):
                    nonlocal output_stream, run
                    if output_stream.endswith('\n'):
                        output_stream += "\n"
                    else:
                        output_stream += "\n\n"

                    msg = update_message.output
                    if msg.endswith(" 💬"):
                        msg = msg[:-2]

                    output_event(status=run.status, output=output_stream + msg + " 💬", messages=None)
                    output_stream += msg + '\n'

                # pass bot_os_thread to tool function in thread_local_storage
                thread_local.bot_os_thread = bot_os_thread

                try:
                    func_response = self.run_tool_function(run, thread_id, func_name, func_args, tool_call_id, status_callback)
                except Exception as e:
                    logger.error(f'bot={self.bot_id} {thread_id=}: error making tool call:\n{traceback.format_exc()}')
                    run.status = 'completed'
                    run.completed_at = datetime.datetime.now()
                    self.send_response_to_user(run, thread_id, output_stream + f'\nError making tool call: {str(e)}', model_name,
                                               chat_history, output_event, bot_os_thread=bot_os_thread)
                    break       

                bot_os_thread.messages.append({"role": "tool", "tool_call_id": tool_call_id, "content": str(func_response)})

                results.append((tool_call_id, str(func_response)))
                continue # to next tool call

            if run.status == 'completed':
                break

            chat_history(message_type='User Prompt', message_payload='Tool call completed, results',
                         message_metadata=input_message.metadata, bot_os_thread=bot_os_thread)

            for tool_call_id, resp in results:
                chat_history(message_type='Tool Output', message_payload=resp,
                             message_metadata={'tool_call_id': tool_call_id}, bot_os_thread=bot_os_thread)
        
            openai_messages = self.get_openai_messages(bot_os_thread, model_name)
            continue # to submit tool calls results to OpenAI

        return True

    def is_bot_openai(self,bot_id):
        return False;

    def reset_bot_if_not_openai(self,bot_id):
        os.environ[f'RESET_BOT_SESSION_{bot_id}'] = 'True'
        return True


    def _download_openai_file(self, file_id, thread_id):
        logger.debug(f"BotOsAssistantOpenAIChat:download_openai_file - {file_id}")
        # Use the retrieve file contents API to get the file directly

        try:
            # logger.info(f"{self.bot_name} open_ai download_file file_id: {file_id}")

            try:
                file_id = file_id.get('file_id',None)
            except:
                try:
                    file_id = file_id.file_id
                except:
                    pass

            file_info = self.client.files.retrieve(file_id=file_id)
            file_contents = self.client.files.content(file_id=file_id)

            local_file_path = os.path.join(f"./runtime/downloaded_files/{thread_id}/", os.path.basename(file_info.filename))

            # Ensure the directory exists
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)


            # Save the file contents locally
            file_contents.write_to_file(local_file_path)

            # Save a copy of the file with the file_id as the file name
            try:
                file_id_based_path = f"./runtime/downloaded_files/{thread_id}/{file_id}"
                file_contents.write_to_file(file_id_based_path)
            except Exception as e:
                logger.info(f"{self.bot_name} open_ai download_file - error - couldnt write to {file_id_based_path} err: {e}")
                pass
        except Exception as e:
            logger.info(f"{self.bot_name} open_ai download_file ERROR: {e}")


        logger.debug(f"File downloaded: {local_file_path}")
        return local_file_path

    def _store_files_locally(self, file_ids, thread_id):
        return [self._download_openai_file(file_id, thread_id) for file_id in file_ids]

    def validate_or_add_function(self, function_name):
        """
        Validates if the given function_name is in self.all_functions. If not, it adds the function.

        Args:
            function_name (str): The name of the function to validate or add.

        Returns:
            bool: True if the function is valid or successfully added, False otherwise.
        """
        if function_name in self.all_functions:
            return True
        else:
            # make sure this works when adding tools
            logger.info(f'validate_or_add_function, fn name={function_name}')
            try:
                available_functions_load = {}
                fn_name = function_name.split('.')[-1] if '.' in function_name else function_name
                module_path = "generated_modules."+fn_name
                desc_func = "TOOL_FUNCTION_DESCRIPTION_"+fn_name.upper()
                functs_func = fn_name.lower()+'_action_function_mapping'
                try:
                    module = __import__(module_path, fromlist=[desc_func, functs_func])
                except:
                    return True

                # here's how to get the function for generated things even new ones...
                func = [getattr(module, desc_func)]
                self.all_tools.extend(func)
                self.all_function_to_tool_map[fn_name]=func
                func_af = getattr(module, functs_func)
                available_functions_load.update(func_af)

                for name, full_func_name in available_functions_load.items():
                    module2 = __import__(module_path, fromlist=[fn_name])
                    func = getattr(module2, fn_name)
                    self.all_functions[name] = func
            except:
                logger.warning(f"Function '{function_name}' is not in all_functions. Please add it before proceeding.")

            logger.info(f"Likely newly generated function '{function_name}' added all_functions.")
            return False

    def update_bots_active_table(self):
        """Update bots active table at most once per minute"""
        if not global_flags.multibot_mode:
            return

        current_time = datetime.datetime.now()
        
        # Simple timestamp check without locking
        if (current_time - self.__class__._last_bots_active_update).total_seconds() < 60:
            return
            
        self.__class__._last_bots_active_update = current_time

        try:
            timestamp_str = self.get_current_time_with_timezone()
            create_bots_active_table_query = f"""
            CREATE OR REPLACE TABLE {self.schema}.bots_active ("{timestamp_str}" STRING);
            """
            
            cursor = self.log_db_connector.connection.cursor()
            cursor.execute(create_bots_active_table_query)
            self.log_db_connector.connection.commit()
            logger.debug(f"Table {self.schema}.bots_active updated with timestamp: {timestamp_str}")
        except Exception as e:
            logger.debug(f"Failed to update bots_active table: {e}")
        finally:
            if cursor:
                cursor.close()


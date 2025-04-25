"""AI service integrations for Taskinator."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import re
import uuid
import logging
import os

import anthropic
from anthropic import AsyncAnthropic, AnthropicBedrock
from openai import OpenAI
from rich.progress import Progress

from .config import config
from .ui import create_loading_indicator
from .utils import logger, sanitize_prompt
from .complexity_training_logger import complexity_logger

def get_anthropic_client() -> Optional[Union[AsyncAnthropic, AnthropicBedrock]]:
    """Get appropriate Anthropic client based on configuration."""
    try:
        if config.use_bedrock:
            # Initialize Bedrock client
            client_kwargs = {
                "aws_region": config.aws_region
            }
            
            # Add AWS credentials if provided
            if config.aws_access_key and config.aws_secret_key:
                client_kwargs.update({
                    "aws_access_key": config.aws_access_key,
                    "aws_secret_key": config.aws_secret_key
                })
                
                if config.aws_session_token:
                    client_kwargs["aws_session_token"] = config.aws_session_token
            
            return AnthropicBedrock(**client_kwargs)
            
        elif config.anthropic_api_key:
            # Initialize direct Anthropic client
            return AsyncAnthropic(api_key=config.anthropic_api_key)
        
        return None
        
    except Exception as e:
        logger.warning(f"Failed to initialize Anthropic client: {e}")
        return None

def get_perplexity_client() -> Optional[OpenAI]:
    """Get Perplexity client if API key is available."""
    if not config.perplexity_api_key:
        return None
    try:
        return OpenAI(
            api_key=config.perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
    except Exception as e:
        logger.warning(f"Failed to initialize Perplexity client: {e}")
        return None

# Initialize clients
anthropic_client = get_anthropic_client()
perplexity_client = get_perplexity_client()

async def call_claude(
    content: str,
    prd_path: Union[str, Path],
    num_tasks: int = 10
) -> Dict[str, Any]:
    """Call Claude to generate tasks from PRD content."""
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )

    system_prompt = f"""You are a technical lead helping to break down a PRD into specific tasks.
Given a PRD, generate {num_tasks} concrete, actionable tasks that would be needed to implement it.
Do not reinvent the wheel unless necessary. For example, if you are making a chocolate cake, you might need to make it from scratch, but maybe a cake mix will do. It's all about outcomes, constraints, and context.


For each task, include:
1. A clear, specific title
2. A detailed description
3. Implementation details
4. A test strategy
5. Dependencies on other tasks (by ID)
6. Priority (low, medium, high)

Return the tasks as a JSON object with this structure:
{{
    "tasks": [
        {{
            "id": 1,
            "title": "Task title",
            "description": "Task description",
            "details": "Implementation details",
            "testStrategy": "How to test this task",
            "dependencies": [],
            "priority": "medium",
            "status": "pending"
        }}
    ]
}}"""

    with create_loading_indicator(
        "Generating tasks with Claude..." +
        (" (via AWS Bedrock)" if config.use_bedrock else "")
    ) as progress:
        try:
            # Create message
            messages = []
            
            # Handle system prompt differently for each client type
            if isinstance(anthropic_client, AnthropicBedrock):
                # For Bedrock, include system prompt as assistant message
                messages = [
                    {
                        "role": "assistant",
                        "content": f"I understand. I will act as a technical lead and follow these instructions:\n\n{system_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"Here is the PRD content from {prd_path}:\n\n{content}"
                    }
                ]
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages
                }
            else:
                # For direct API, use system parameter
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "system": system_prompt,
                    "messages": [{
                        "role": "user",
                        "content": f"Here is the PRD content from {prd_path}:\n\n{content}"
                    }]
                }
            
            # Call appropriate client
            if isinstance(anthropic_client, AnthropicBedrock):
                response = anthropic_client.messages.create(**message_params)
                response_content = response.content[0].text
            else:
                response = await anthropic_client.messages.create(**message_params)
                response_content = response.content[0].text
            
            # Extract JSON from response
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON found in Claude's response")
            
            tasks_data = json.loads(response_content[json_start:json_end])
            
            # Validate structure
            if not isinstance(tasks_data, dict) or 'tasks' not in tasks_data:
                raise ValueError("Invalid task data structure")
            
            return tasks_data
            
        except Exception as e:
            logger.error(f"Error calling Claude: {e}")
            raise

async def generate_subtasks(
    task: Dict[str, Any],
    num_subtasks: int = 5,
    use_research: bool = False,
    additional_context: str = "",
    progress: Optional[Progress] = None
) -> List[Dict[str, Any]]:
    """Generate subtasks for a given task."""
    if use_research and perplexity_client:
        return await generate_subtasks_with_perplexity(
            task,
            num_subtasks,
            additional_context,
            progress
        )
    
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )
    
    system_prompt = f"""You are helping to break down a development task into smaller subtasks.
Given a task, generate {num_subtasks} specific, actionable subtasks that would be needed to complete it.
Do not reinvent the wheel unless necessary. For example, if you are making a chocolate cake, you might need to make it from scratch, but maybe a cake mix will do. It's all about outcomes, constraints, and context.

For each subtask, include:
1. A clear, specific title
2. A description
3. Implementation details
4. Dependencies on other subtasks (by ID) or the parent task

Return the subtasks as a JSON array with this structure:
[
    {{
        "id": 1,
        "title": "Subtask title",
        "description": "Subtask description",
        "details": "Implementation details",
        "dependencies": [],
        "status": "pending"
    }}
]"""

    task_content = f"""Task {task['id']}: {task['title']}
Description: {task['description']}
Details: {task['details']}"""

    if additional_context:
        task_content += f"\n\nAdditional Context: {additional_context}"

    # Only create a new progress if one wasn't provided
    own_progress = False
    if progress is None:
        progress = create_loading_indicator(
            "Generating subtasks with Claude..." +
            (" (via AWS Bedrock)" if config.use_bedrock else "")
        )
        progress.start()
        own_progress = True
    
    try:
        # Create message
        if isinstance(anthropic_client, AnthropicBedrock):
            # For Bedrock, include system prompt as assistant message
            messages = [
                {
                    "role": "assistant",
                    "content": f"I understand. I will help break down the task following these instructions:\n\n{system_prompt}"
                },
                {
                    "role": "user",
                    "content": task_content
                }
            ]
            message_params = {
                "model": config.claude_model,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "messages": messages
            }
        else:
            # For direct API, use system parameter
            message_params = {
                "model": config.claude_model,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "system": system_prompt,
                "messages": [{
                    "role": "user",
                    "content": task_content
                }]
            }
        
        # Call appropriate client
        if isinstance(anthropic_client, AnthropicBedrock):
            response = anthropic_client.messages.create(**message_params)
            response_content = response.content[0].text
        else:
            response = await anthropic_client.messages.create(**message_params)
            response_content = response.content[0].text
        
        # Extract JSON from response
        json_start = response_content.find('[')
        json_end = response_content.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON found in Claude's response")
        
        subtasks = json.loads(response_content[json_start:json_end])
        
        # Validate structure
        if not isinstance(subtasks, list):
            raise ValueError("Invalid subtask data structure")
        
        return subtasks
        
    except Exception as e:
        logger.error(f"Error generating subtasks: {e}")
        raise
    finally:
        if own_progress:
            progress.stop()

async def generate_subtasks_with_perplexity(
    task: Dict[str, Any],
    num_subtasks: int = 5,
    additional_context: str = "",
    progress: Optional[Progress] = None
) -> List[Dict[str, Any]]:
    """Generate subtasks using Perplexity AI for research."""
    if not perplexity_client:
        raise RuntimeError(
            "Perplexity client not available. Please check your API key."
        )

    system_prompt = f"""You are a technical researcher helping to break down a workflow task.
Use your research capabilities to find domain-specific relevant information, best practices, and implementation details.
Then generate {num_subtasks} specific, actionable subtasks based on your research.

For each subtask, include:
1. A clear, specific title
2. A description incorporating research findings
3. Detailed implementation steps based on best practices
4. Dependencies on other subtasks (by ID) or the parent task

Return the subtasks as a JSON array."""

    task_content = f"""Task {task['id']}: {task['title']}
Description: {task['description']}
Details: {task['details']}"""

    if additional_context:
        task_content += f"\n\nAdditional Context: {additional_context}"

    # Only create a new progress if one wasn't provided
    own_progress = False
    if progress is None:
        progress = create_loading_indicator("Researching and generating subtasks with Perplexity...")
        progress.start()
        own_progress = True
    
    try:
        # The OpenAI client for Perplexity doesn't support async/await
        # Use sync version instead
        response = perplexity_client.chat.completions.create(
            model=config.perplexity_model,
            messages=[
                {"role": "system", "content": "You are a technical analysis AI that only responds with clean, valid JSON."},
                {"role": "user", "content": f"{system_prompt}\n\n{task_content}"}
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        
        # Extract JSON from response
        content = response.choices[0].message.content
        
        # Log the raw response for debugging
        logger.debug(f"Raw Perplexity response: {content[:200]}...")
        
        # Improved JSON extraction logic for Perplexity
        try:
            # First try: direct JSON parsing
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                pass
            
            # Second try: Find JSON array with square brackets
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                return json.loads(json_content)
            
            # Third try: Find JSON object with curly braces
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                # If this is a JSON object, wrap it in an array
                result = json.loads(json_content)
                if isinstance(result, dict):
                    return [result]
                return result
            
            raise ValueError("No valid JSON found in Perplexity's response")
        except Exception as e:
            error_msg = f"Error parsing Perplexity's response: {str(e)}. Response starts with: {content[:100]}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
    except Exception as e:
        logger.warning(f"Perplexity analysis failed: {e}. Falling back to Claude.")
        # Log the error for training data collection
        complexity_logger.log_analysis_response(
            request_id=None,
            response=[],
            error=f"Perplexity analysis failed: {e}"
        )
        
        # Fall back to regular generate_subtasks without research flag
        if not anthropic_client:
            error_msg = "Claude service not available. Please configure either direct API access or AWS Bedrock."
            # Log the error for training data collection
            complexity_logger.log_analysis_response(
                request_id=None,
                response=[],
                error=error_msg
            )
            raise RuntimeError(error_msg)
        
        # Use the regular generate_subtasks implementation
        try:
            # Create a system prompt for Claude
            claude_system_prompt = f"""You are a technical lead helping to break down a workflow task.
Generate {num_subtasks} specific, actionable subtasks.

For each subtask, include:
1. A clear, specific title
2. A description
3. Detailed implementation steps
4. Dependencies on other subtasks (by ID) or the parent task

Return the subtasks as a JSON array."""

            # Create message parameters
            if isinstance(anthropic_client, AnthropicBedrock):
                messages = [
                    {
                        "role": "assistant",
                        "content": f"I understand. I will help break down the task following these instructions:\n\n{claude_system_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"{task_content}"
                    }
                ]
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages
                }
            else:
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "system": claude_system_prompt,
                    "messages": [{
                        "role": "user",
                        "content": f"{task_content}"
                    }]
                }
            
            # Call appropriate client
            if isinstance(anthropic_client, AnthropicBedrock):
                response = anthropic_client.messages.create(**message_params)
                response_content = response.content[0].text
            else:
                response = await anthropic_client.messages.create(**message_params)
                response_content = response.content[0].text
            
            # Extract JSON from response
            json_start = response_content.find('[')
            json_end = response_content.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                # Try with curly braces
                json_start = response_content.find('{')
                json_end = response_content.rfind('}') + 1
                
                if json_start == -1 or json_end == 0:
                    raise ValueError("No valid JSON found in Claude's response")
                
                result = json.loads(response_content[json_start:json_end])
                if isinstance(result, dict):
                    return [result]
                return result
            
            return json.loads(response_content[json_start:json_end])
            
        except Exception as claude_error:
            logger.error(f"Claude fallback also failed: {claude_error}")
            raise RuntimeError(f"Both Perplexity and Claude failed: {e}. Claude error: {claude_error}")
    
    finally:
        if own_progress and progress:
            progress.stop()

def clean_json_response(json_text: str) -> Dict:
    """Clean and extract valid JSON from potentially malformed API responses.
    
    Args:
        json_text: The raw JSON text to clean
        
    Returns:
        Dictionary with extracted data (processes, research_insights, etc.)
    """
    logger.debug(f"Attempting to clean JSON response: {json_text[:100]}...")
    
    # First, try to parse the entire response as a JSON object
    try:
        # Look for JSON code blocks in markdown
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', json_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
            
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        logger.warning(f"Full JSON parsing failed: {e}")
    
    # Try to extract a complete JSON object
    try:
        obj_start = json_text.find('{')
        obj_end = json_text.rfind('}') + 1
        
        if obj_start >= 0 and obj_end > obj_start:
            obj_text = json_text[obj_start:obj_end]
            return json.loads(obj_text)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON object extraction failed: {e}")
    
    # Try to extract the processes array and other key sections
    result = {"processes": []}
    
    # Extract processes array
    try:
        processes_match = re.search(r'"processes"\s*:\s*(\[.*?\])', json_text, re.DOTALL)
        if processes_match:
            processes_text = processes_match.group(1)
            processes = json.loads(processes_text)
            result["processes"] = processes
    except json.JSONDecodeError as e:
        logger.warning(f"Processes array extraction failed: {e}")
        
        # Try to extract individual process objects
        processes = []
        depth = 0
        start_pos = None
        processes_text = json_text
        
        for i, char in enumerate(processes_text):
            if char == '{':
                if depth == 0:
                    start_pos = i
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0 and start_pos is not None:
                    obj_text = processes_text[start_pos:i+1]
                    try:
                        obj = json.loads(obj_text)
                        # Check if this looks like a process object
                        if any(key in obj for key in ["process_id", "id", "title"]):
                            processes.append(obj)
                    except json.JSONDecodeError:
                        # Try to clean this object
                        cleaned_obj_text = re.sub(r',\s*}', '}', obj_text)
                        cleaned_obj_text = re.sub(r'[\n\r]+', ' ', cleaned_obj_text)
                        try:
                            obj = json.loads(cleaned_obj_text)
                            if any(key in obj for key in ["process_id", "id", "title"]):
                                processes.append(obj)
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse process object: {obj_text[:50]}...")
        
        if processes:
            logger.info(f"Successfully extracted {len(processes)} process objects from malformed JSON")
            result["processes"] = processes
    
    # Extract analysis approach
    analysis_match = re.search(r'"analysis_approach"\s*:\s*"(.*?)"(?=,|\})', json_text, re.DOTALL)
    if analysis_match:
        result["analysis_approach"] = analysis_match.group(1).replace('\\n', '\n').replace('\\\"', '"')
    
    # Extract research insights if present
    research_match = re.search(r'"research_insights"\s*:\s*"(.*?)"(?=,|\})', json_text, re.DOTALL)
    if research_match:
        result["research_insights"] = research_match.group(1).replace('\\n', '\n').replace('\\\"', '"')
    
    # If we couldn't extract anything useful
    if not result["processes"]:
        logger.error("Failed to extract any valid process objects")
        
    return result

async def analyze_task_complexity(
    tasks: List[Dict],
    prompt: str = None,
    model_override: str = None,
    use_research: bool = False,
    request_id: str = None
) -> List[Dict]:
    """Analyze task complexity using AI.
    
    Args:
        tasks: List of tasks to analyze
        prompt: Optional custom prompt
        model_override: Optional model to use
        use_research: Whether to use research for analysis
        request_id: Optional request ID for logging
        
    Returns:
        List of task complexity analyses
    """
    if not request_id:
        # Log the analysis request for training data collection
        request_id = complexity_logger.log_analysis_request(
            tasks=tasks,
            prompt=prompt,
            use_research=use_research,
            model=model_override or (config.perplexity_model if use_research else config.claude_model)
        )
    
    # Try Perplexity first if research is requested
    if use_research and perplexity_client:
        try:
            # Add research context to prompt
            research_prompt = f"""You are conducting a detailed analysis of various workflow tasks.
Please research each task thoroughly, considering domain relevant best practices, industry standards, and potential implementation challenges.

{prompt}

CRITICAL: You MUST respond ONLY with a valid JSON array. Do not include ANY explanatory text or markdown formatting."""

            # Use synchronous API for Perplexity (no await)
            # Use sync version instead
            response = perplexity_client.chat.completions.create(
                model=config.perplexity_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical analysis AI that only responds with clean, valid JSON."
                    },
                    {
                        "role": "user",
                        "content": research_prompt
                    }
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            
            # Log the raw response for debugging
            logger.debug(f"Raw Perplexity response: {content[:200]}...")
            
            # Try to parse the response using the clean_json_response function
            result = clean_json_response(content)
            if result:
                # Log the analysis response for training data collection
                complexity_logger.log_analysis_response(
                    request_id=request_id,
                    response=result,
                    raw_response=content
                )
                return result
            
            # If clean_json_response failed, fall back to Claude
            logger.warning("Failed to extract valid JSON from Perplexity response. Falling back to Claude.")
            
        except Exception as e:
            logger.warning(f"Perplexity analysis failed: {e}. Falling back to Claude.")
            # Log the error for training data collection
            complexity_logger.log_analysis_response(
                request_id=request_id,
                response=[],
                error=f"Perplexity analysis failed: {e}"
            )
    
    if not anthropic_client:
        error_msg = "Claude service not available. Please configure either direct API access or AWS Bedrock."
        # Log the error for training data collection
        complexity_logger.log_analysis_response(
            request_id=request_id,
            response=[],
            error=error_msg
        )
        raise RuntimeError(error_msg)
    
    # Create message parameters with stronger JSON formatting instructions
    system_message = "You are an expert software architect analyzing task complexity. You MUST respond ONLY with a valid JSON array containing task complexity assessments. Do not include any explanatory text, markdown formatting, or code blocks."
    
    if isinstance(anthropic_client, AnthropicBedrock):
        messages = [
            {
                "role": "assistant",
                "content": f"I understand. I will analyze the tasks and provide complexity assessments as a valid JSON array."
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nIMPORTANT: Your response MUST be a valid JSON array only. No text before or after the JSON."
            }
        ]
        message_params = {
            "model": model_override or config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "messages": messages
        }
    else:
        message_params = {
            "model": model_override or config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "system": system_message,
            "messages": [{
                "role": "user",
                "content": f"{prompt}\n\nIMPORTANT: Your response MUST be a valid JSON array only. No text before or after the JSON."
            }]
        }
    
    # Call appropriate client
    if isinstance(anthropic_client, AnthropicBedrock):
        response = anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    else:
        response = await anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    
    # Log the raw response for debugging
    logger.debug(f"Raw Claude response: {response_content[:200]}...")
    
    # Try to parse the response using the clean_json_response function
    result = clean_json_response(response_content)
    if result:
        # Log the analysis response for training data collection
        complexity_logger.log_analysis_response(
            request_id=request_id,
            response=result,
            raw_response=response_content
        )
        return result
    
    # If we got here, all parsing attempts failed
    error_msg = f"Failed to extract valid JSON from Claude's response. Response starts with: {response_content[:100]}"
    logger.error(error_msg)
    # Log the error for training data collection
    complexity_logger.log_analysis_response(
        request_id=request_id,
        response=[],
        raw_response=response_content,
        error=error_msg
    )
    raise ValueError(error_msg)

def generate_complexity_analysis_prompt(data: Dict[str, Any]) -> str:
    """Generate a prompt for task complexity analysis."""
    tasks_content = "\n\n".join([
        f"""Task {task['id']}: {task['title']}
Description: {task['description']}
Details: {task['details']}"""
        for task in data['tasks']
    ])

    return f"""You are an expert software architect analyzing task complexity.
Please analyze each task and provide a detailed complexity assessment.

Tasks to analyze:

{tasks_content}

For each task, provide:
1. A complexity score (1-10, where 10 is most complex)
2. Recommended number of subtasks (if score >= 5)
3. A detailed expansion prompt for breaking down the task
4. Reasoning for the complexity assessment

Return your analysis as a JSON array with this structure:
[
    {{
        "taskId": 1,
        "taskTitle": "Task title",
        "complexityScore": 7,
        "recommendedSubtasks": 4,
        "expansionPrompt": "Detailed prompt for expansion",
        "reasoning": "Explanation of complexity assessment"
    }}
]

Consider:
1. Technical complexity and implementation challenges
2. Dependencies and integration points
3. Required expertise and domain knowledge
4. Testing requirements and validation complexity
5. Potential risks and edge cases
6. Estimated time investment"""

async def generate_task_details(prompt: str) -> Dict[str, str]:
    """Generate task details using AI.
    
    Args:
        prompt: Description of the task to generate details for
    
    Returns:
        Dictionary containing task details (title, description, details, testStrategy)
    """
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )
    
    system_prompt = """You are helping to create a detailed software development task.
Given a task description, generate a complete task specification including:
1. A clear, specific title
2. A detailed description
3. Implementation details
4. A test strategy

Return the task details as a JSON object with this structure:
{
    "title": "Task title",
    "description": "Task description",
    "details": "Implementation details",
    "testStrategy": "How to test this task"
}"""

    # Create message parameters
    if isinstance(anthropic_client, AnthropicBedrock):
        messages = [
            {
                "role": "assistant",
                "content": f"I understand. I will help create a task specification following these instructions:\n\n{system_prompt}"
            },
            {
                "role": "user",
                "content": f"Generate task details for: {prompt}"
            }
        ]
        message_params = {
            "model": config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "messages": messages
        }
    else:
        message_params = {
            "model": config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "system": system_prompt,
            "messages": [{
                "role": "user",
                "content": f"Generate task details for: {prompt}"
            }]
        }
    
    # Call appropriate client
    if isinstance(anthropic_client, AnthropicBedrock):
        response = anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    else:
        response = await anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    
    # Extract JSON from response
    json_start = response_content.find('{')
    json_end = response_content.rfind('}') + 1
    
    if json_start == -1 or json_end == 0:
        raise ValueError("No valid JSON found in Claude's response")
    
    task_details = json.loads(response_content[json_start:json_end])
    
    # Validate structure
    required_fields = {'title', 'description', 'details', 'testStrategy'}
    if not all(field in task_details for field in required_fields):
        raise ValueError("Invalid task details structure")
    
    return task_details

async def identify_processes_from_tasks(
    tasks: List[Dict],
    output_dir: str = "pdds",
    request_id: str = None,
    research_mode: bool = False,
    variations_count: int = 0
) -> Dict[str, Any]:
    """Identify processes from tasks using AI.
    
    This function analyzes existing tasks to identify domain-specific processes
    and creates a structured processes.json file and individual PDD text files.
    
    Args:
        tasks: List of tasks to analyze
        output_dir: Directory to store the identified processes
        request_id: Optional request ID for logging
        research_mode: Enable research mode for more in-depth analysis
        variations_count: Number of process variations to generate (0-5)
        
    Returns:
        Dictionary with identified processes
    """
    if not request_id:
        request_id = str(uuid.uuid4())
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Format tasks for the prompt
    tasks_content = "\n\n".join([
        f"""Task {task['id']}: {task['title']}\nDescription: {task['description']}\nDetails: {task.get('details', '')}"""
        for task in tasks
    ])
    
    # Create the prompt for process identification
    prompt = f"""You are an expert process designer analyzing tasks to identify meaningful processes.

Please analyze these tasks and identify domain-specific processes that would be needed to implement them.
For each process, provide:
1. A unique process ID (format: P001, P002, etc.)
2. A clear, specific title
3. A detailed description
4. Complexity level (simple, medium, complex, very_complex)
5. Dependencies on other processes (by ID)
6. Resources required
7. Domain-specific parameters

Tasks to analyze:

{tasks_content}

IMPORTANT: 
- Focus on identifying real-world processes, not just software development patterns
- Be specific to the domain of the tasks (e.g., cooking, baking, software development, etc.)
- Don't reinvent the wheel - if a standard process exists, use it
- Identify 3-7 key processes that cover the entire workflow
- Ensure processes have clear boundaries and responsibilities
- Consider the natural flow and dependencies between processes
- Use existing processes where possible
"""

    # Add research mode instructions if enabled
    if research_mode:
        prompt += """
RESEARCH MODE INSTRUCTIONS:
- Conduct a deeper analysis of the domain and best practices
- Consider industry standards and established methodologies
- Provide research-backed insights for each process
- Include references to relevant frameworks or methodologies where applicable
- Explain why certain approaches are recommended over others
- Consider edge cases and potential challenges
"""

    # Add variations instructions if requested
    if variations_count > 0:
        prompt += f"""
VARIATIONS INSTRUCTIONS:
- For each identified process, provide {variations_count} alternative implementation approaches
- Each variation should have:
  * A descriptive name
  * Key differences from the main approach
  * Potential advantages and disadvantages
  * Scenarios where this variation would be preferred
- Variations should represent meaningfully different approaches, not minor tweaks
"""

    # Final response format instructions
    prompt += """
Please respond with a JSON object containing:
1. An array of "processes", where each process has:
   - process_id (string, format P001, P002, etc.)
   - title (string)
   - description (string)
   - complexity (string: simple, medium, complex, very_complex)
   - dependencies (array of strings, e.g. ["P001", "P002"])
   - resources (array of strings)
   - parameters (object with string keys and any value type)
"""

    # Add variations format if requested
    if variations_count > 0:
        prompt += """
   - variations (array of objects), where each variation has:
     * name (string)
     * description (string)
     * advantages (array of strings)
     * disadvantages (array of strings)
     * scenarios (array of strings)
"""

    # Add analysis approach and research insights
    prompt += """
2. "analysis_approach" (string): A brief explanation of your analysis approach
"""

    # Add research insights request if in research mode
    if research_mode:
        prompt += """
3. "research_insights" (string): Domain-specific insights and best practices
"""

    # Call Claude to identify processes
    try:
        if not anthropic_client:
            raise RuntimeError(
                "Claude service not available. Please configure either direct API "
                "access or AWS Bedrock."
            )
        
        # Create message parameters
        system_message = "You are an expert process designer analyzing tasks to identify meaningful processes. Respond with a valid JSON object."
        
        # Adjust max tokens based on research mode and variations
        max_tokens = 4000
        if research_mode:
            max_tokens += 2000
        if variations_count > 0:
            max_tokens += variations_count * 500
            
        if isinstance(anthropic_client, AnthropicBedrock):
            messages = [
                {
                    "role": "assistant",
                    "content": "I understand. I will analyze the tasks and identify domain-specific processes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            message_params = {
                "model": config.claude_model,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "messages": messages
            }
        else:
            message_params = {
                "model": config.claude_model,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "system": system_message,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            }
        
        # Call appropriate client
        if isinstance(anthropic_client, AnthropicBedrock):
            response = anthropic_client.messages.create(**message_params)
            response_content = response.content[0].text
        else:
            response = await anthropic_client.messages.create(**message_params)
            response_content = response.content[0].text
        
        # Extract JSON from response
        result = clean_json_response(response_content)
        if not result:
            raise ValueError("Failed to extract valid JSON from Claude's response")
        
        # Create processes.json file
        processes_file = os.path.join(output_dir, "processes.json")
        with open(processes_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"Saved identified processes to {processes_file}")
        
        # Create individual PDD text files for each process
        processes = result.get("processes", [])
        for process in processes:
            # Check if we have process_id or id field
            process_id = process.get("process_id") or process.get("id", "")
            if not process_id:
                continue
                
            title = process.get("title", "")
            description = process.get("description", "")
            complexity = process.get("complexity", "")
            dependencies = process.get("dependencies", [])
            resources = process.get("resources", []) or process.get("resources_required", [])
            parameters = process.get("parameters", {}) or process.get("domain_parameters", {})
            variations = process.get("variations", [])
            
            # Format dependencies as a comma-separated string
            dependencies_str = ", ".join(str(dep) for dep in dependencies)
            
            # Format resources as a bulleted list
            resources_str = "\n".join([f"- {resource}" for resource in resources])
            
            # Format parameters as a bulleted list
            parameters_str = "\n".join([f"- {key}: {value}" for key, value in parameters.items()])
            
            # Format variations if present
            variations_str = ""
            if variations:
                variations_str = "## Variations\n\n"
                for i, variation in enumerate(variations, 1):
                    var_name = variation.get("name", f"Variation {i}")
                    var_desc = variation.get("description", "")
                    var_advantages = variation.get("advantages", [])
                    var_disadvantages = variation.get("disadvantages", [])
                    var_scenarios = variation.get("scenarios", [])
                    
                    variations_str += f"### {var_name}\n\n{var_desc}\n\n"
                    
                    if var_advantages:
                        variations_str += "**Advantages:**\n"
                        variations_str += "\n".join([f"- {adv}" for adv in var_advantages]) + "\n\n"
                        
                    if var_disadvantages:
                        variations_str += "**Disadvantages:**\n"
                        variations_str += "\n".join([f"- {dis}" for dis in var_disadvantages]) + "\n\n"
                        
                    if var_scenarios:
                        variations_str += "**When to use:**\n"
                        variations_str += "\n".join([f"- {scn}" for scn in var_scenarios]) + "\n\n"
            
            # Add research insights if available
            research_insights_str = ""
            if research_mode and "research_insights" in result:
                process_research = result.get("research_insights", "")
                if process_research:
                    research_insights_str = f"\n## Research Insights\n\n{process_research}\n\n"
            
            # Create PDD content
            pdd_content = f"""# Process ID: {process_id}
# Title: {title}
# Complexity: {complexity}
# Dependencies: {dependencies_str}

## Description
{description}

## Resources
{resources_str}

## Parameters
{parameters_str}
{research_insights_str}
{variations_str}
"""
            
            # Create PDD file
            pdd_filename = f"{process_id}_{title.lower().replace(' ', '_')}_pdd.txt"
            pdd_file = os.path.join(output_dir, pdd_filename)
            with open(pdd_file, 'w') as f:
                f.write(pdd_content)
            
            logger.info(f"Saved PDD file to {pdd_file}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error identifying processes: {e}")
        raise ValueError(f"Failed to identify processes: {e}")
#!/usr/bin/env python3
"""Script to force update research results for task 11 in tasks.json."""

import json
import os
import sys
from pathlib import Path

def extract_research_results(task_file_path):
    """Extract research results from a task file."""
    print(f"Extracting research results from {task_file_path}")
    
    with open(task_file_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Look for research results section
    in_research = False
    research_lines = []
    
    for i, line in enumerate(lines):
        if "Research Results" in line:
            in_research = True
            print(f"Found research results section at line {i}: {line}")
            continue
        
        if in_research and line.startswith('##') and not line.startswith('## Recommendations') and not line.startswith('## Resources') and not line.startswith('## Sources'):
            in_research = False
            print(f"End of research section at line {i}: {line}")
        
        if in_research:
            research_lines.append(line)
    
    if research_lines:
        research_content = '\n'.join(research_lines)
        print(f"Extracted {len(research_lines)} lines of research content")
        return research_content
    else:
        print("No research content found")
        return None

def update_tasks_json(tasks_file_path, task_id, subtask_id, research_content):
    """Update the research results in tasks.json."""
    print(f"Updating tasks.json at {tasks_file_path}")
    
    with open(tasks_file_path, 'r') as f:
        tasks_data = json.load(f)
    
    # Find the task
    task = next((t for t in tasks_data.get('tasks', []) if t.get('id') == task_id), None)
    if not task:
        print(f"Task {task_id} not found in tasks.json")
        return False
    
    # Find the subtask
    subtask = next((s for s in task.get('subtasks', []) if s.get('id') == subtask_id), None)
    if not subtask:
        print(f"Subtask {subtask_id} not found in task {task_id}")
        return False
    
    # Ensure research structure exists
    if 'research' not in subtask:
        subtask['research'] = {}
    
    # Extract the first line as summary
    lines = research_content.split('\n')
    if lines and lines[0].strip():
        subtask['research']['summary'] = lines[0].strip()
        print(f"Set research summary to: '{lines[0].strip()}'")
    
    # Update the key findings
    subtask['research']['key_findings'] = research_content
    print(f"Updated key_findings with research content")
    
    # Extract recommendations if they exist
    if '## Recommendations' in research_content or '**Recommendations' in research_content:
        print("Found Recommendations section")
        # Split content by recommendations
        parts = research_content.split('## Recommendations', 1)
        if len(parts) == 1:
            parts = research_content.split('**Recommendations', 1)
        
        if len(parts) > 1:
            recommendations = parts[1]
            
            # Check if there are sources/resources
            if '## Sources' in recommendations:
                rec_parts = recommendations.split('## Sources', 1)
                recommendations = rec_parts[0].strip()
                sources = rec_parts[1].strip()
                subtask['research']['sources'] = sources
                print(f"Found Sources section, length: {len(sources)}")
            elif '## Resources' in recommendations:
                rec_parts = recommendations.split('## Resources', 1)
                recommendations = rec_parts[0].strip()
                sources = rec_parts[1].strip()
                subtask['research']['resources'] = sources
                print(f"Found Resources section, length: {len(sources)}")
            
            subtask['research']['implementation_recommendations'] = recommendations.strip()
            print(f"Extracted recommendations, length: {len(recommendations.strip())}")
        else:
            subtask['research']['implementation_recommendations'] = research_content
            print(f"No recommendations section found, using full content")
    else:
        subtask['research']['implementation_recommendations'] = research_content
        print(f"No recommendations section found, using full content")
    
    # Write the updated tasks back to the file
    with open(tasks_file_path, 'w') as f:
        json.dump(tasks_data, f, indent=2)
    
    print(f"Successfully updated research results for task {task_id}, subtask {subtask_id}")
    return True

def main():
    """Main function."""
    # Default paths
    tasks_dir = Path("tasks")
    task_file_path = tasks_dir / "task_011.txt"
    tasks_file_path = tasks_dir / "tasks.json"
    
    # Check if files exist
    if not task_file_path.exists():
        print(f"Task file not found: {task_file_path}")
        return 1
    
    if not tasks_file_path.exists():
        print(f"Tasks file not found: {tasks_file_path}")
        return 1
    
    # Extract research results
    research_content = extract_research_results(task_file_path)
    if not research_content:
        return 1
    
    # Update tasks.json
    success = update_tasks_json(tasks_file_path, 11, 1, research_content)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

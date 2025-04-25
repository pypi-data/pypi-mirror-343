#!/usr/bin/env python3
"""
Script to convert a PDD document to a Mermaid diagram.
"""

import os
import sys
import yaml
from pathlib import Path

from taskinator.pdd_document import PDDDocument, PDDProcess, PDDDocumentManager

def generate_mermaid_from_pdd(pdd_path):
    """Generate a Mermaid diagram from a PDD document."""
    # Load the PDD document
    if pdd_path.endswith('.yaml') or pdd_path.endswith('.yml'):
        with open(pdd_path, 'r') as f:
            data = yaml.safe_load(f)
        pdd = PDDDocument.from_dict(data)
    elif pdd_path.endswith('.json'):
        manager = PDDDocumentManager()
        doc_id = os.path.splitext(os.path.basename(pdd_path))[0]
        pdd = PDDDocument.from_dict(data)
    else:
        raise ValueError(f"Unsupported file format: {pdd_path}")
    
    # Start building the Mermaid diagram
    mermaid = "```mermaid\nflowchart TD\n"
    
    # Add title as a comment
    mermaid += f"    %% {pdd.title}\n"
    
    # Add nodes for each process
    for process in pdd.processes:
        process_id = process.process_id
        difficulty = process.implementation_difficulty.value if process.implementation_difficulty else "unknown"
        
        # Create a node with shape based on difficulty
        if difficulty == "simple":
            shape = "([{title}])"  # Rounded box for simple processes
        elif difficulty == "moderate":
            shape = "[{title}]"    # Box for moderate processes
        elif difficulty == "complex":
            shape = "{{{{title}}}}"  # Hexagon for complex processes
        else:
            shape = "{{{title}}}"  # Rhombus for very complex/extreme processes
        
        # Replace {title} with the actual title
        node_def = shape.replace("{title}", process.title)
        
        # Add the node definition
        mermaid += f"    {process_id}{node_def}\n"
    
    # Add connections based on dependencies
    for process in pdd.processes:
        for dep in process.dependencies:
            mermaid += f"    {dep} --> {process.process_id}\n"
    
    # Add a subgraph for business objectives
    if pdd.business_objectives:
        mermaid += "    subgraph Business Objectives\n"
        for i, obj in enumerate(pdd.business_objectives):
            obj_id = f"obj{i+1}"
            mermaid += f"        {obj_id}[\"{obj}\"]\n"
        mermaid += "    end\n"
    
    # Add a subgraph for success criteria
    if pdd.success_criteria:
        mermaid += "    subgraph Success Criteria\n"
        for i, crit in enumerate(pdd.success_criteria):
            crit_id = f"crit{i+1}"
            mermaid += f"        {crit_id}[\"{crit}\"]\n"
        mermaid += "    end\n"
    
    # Add a legend for difficulty levels
    mermaid += "    subgraph Legend\n"
    mermaid += "        simple([Simple])\n"
    mermaid += "        moderate[Moderate]\n"
    mermaid += "        complex{{Complex}}\n"
    mermaid += "        extreme{Very Complex/Extreme}\n"
    mermaid += "    end\n"
    
    # Close the diagram
    mermaid += "```"
    
    return mermaid

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python pdd_to_mermaid.py <pdd_file>")
        sys.exit(1)
    
    pdd_path = sys.argv[1]
    if not os.path.exists(pdd_path):
        print(f"Error: File not found: {pdd_path}")
        sys.exit(1)
    
    try:
        mermaid = generate_mermaid_from_pdd(pdd_path)
        
        # Save the Mermaid diagram to a file
        output_path = os.path.splitext(pdd_path)[0] + ".mermaid.md"
        with open(output_path, "w") as f:
            f.write(f"# Mermaid Diagram for {os.path.basename(pdd_path)}\n\n")
            f.write(mermaid)
        
        print(f"Mermaid diagram saved to: {output_path}")
        
        # Also print to console
        print("\nMermaid Diagram:\n")
        print(mermaid)
        
    except Exception as e:
        print(f"Error generating Mermaid diagram: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

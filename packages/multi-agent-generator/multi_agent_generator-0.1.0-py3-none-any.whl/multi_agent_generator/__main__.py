"""
Command line interface for multi-agent-generator.
"""
import argparse
import json
from .generator import AgentGenerator
from .frameworks import (
    create_crewai_code,
    create_crewai_flow_code,
    create_langgraph_code,
    create_react_code
)

def main():
    """Command line entry point."""
    parser = argparse.ArgumentParser(description="Generate multi-agent AI code")
    parser.add_argument("prompt", help="Plain English description of what you need")
    parser.add_argument(
        "--framework", 
        choices=["crewai", "crewai-flow", "langgraph", "react"], 
        default="crewai",
        help="Agent framework to use (default: crewai)"
    )
    parser.add_argument(
        "--output", 
        help="Output file path (default: print to console)"
    )
    parser.add_argument(
        "--format",
        choices=["code", "json", "both"],
        default="code",
        help="Output format (default: code)"
    )
    
    args = parser.parse_args()
    
    # Analyze the prompt
    generator = AgentGenerator()
    config = generator.analyze_prompt(args.prompt, args.framework)
    
    # Generate code based on the framework
    if args.framework == "crewai":
        code = create_crewai_code(config)
    elif args.framework == "crewai-flow":
        code = create_crewai_flow_code(config)
    elif args.framework == "langgraph":
        code = create_langgraph_code(config)
    elif args.framework == "react":
        code = create_react_code(config)
    else:
        print(f"Unsupported framework: {args.framework}")
        return
    
    # Prepare output
    if args.format == "code":
        output = code
    elif args.format == "json":
        output = json.dumps(config, indent=2)
    else:  # both
        output = f"// Configuration:\n{json.dumps(config, indent=2)}\n\n// Generated Code:\n{code}"
    
    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
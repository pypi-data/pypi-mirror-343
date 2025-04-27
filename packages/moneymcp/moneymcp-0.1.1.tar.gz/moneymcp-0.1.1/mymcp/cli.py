#!/usr/bin/env python3
import argparse
import sys
import os

def main():
    """
    Command line interface for mymcp financial analysis server
    """
    parser = argparse.ArgumentParser(
        description="Financial Analysis MCP Server - A comprehensive financial analysis tool"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to run the server on (default: 8000)"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1",
        help="Host address to bind the server to (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Import here to avoid circular imports
    from mymcp.server import main as run_server
    
    # Set environment variables for configuration
    os.environ["MYMCP_HOST"] = args.host
    os.environ["MYMCP_PORT"] = str(args.port)
    os.environ["MYMCP_LOG_LEVEL"] = args.log_level
    
    # Run the server
    run_server()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 

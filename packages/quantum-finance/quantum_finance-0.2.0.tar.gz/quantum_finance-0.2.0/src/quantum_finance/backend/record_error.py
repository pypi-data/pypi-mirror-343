#!/usr/bin/env python3
"""
Error Recorder Script

This script demonstrates recording the import error we experienced with
our Flask app into the development insights system.
"""

from development_insights import DevelopmentTracker

def main():
    # Create a tracker instance
    tracker = DevelopmentTracker()
    
    # Record the import error
    tracker.record_error(
        error_type="ImportError",
        message="cannot import name 'get_prediction' from 'ml_framework'",
        resolution="Fixed import statement in app.py to only import MLFramework class",
        code_context="backend/app.py:2",
        tags=["flask", "import", "python"]
    )
    
    # Record the command formatting error
    tracker.record_error(
        error_type="CommandSyntaxError",
        message="Invalid flask run command with duplicate port flag",
        resolution="Fixed command syntax to use proper format: 'python -m flask run --port 5002'",
        code_context="terminal:1",
        tags=["cli", "flask"]
    )
    
    # Record the port conflict pattern as an anti-pattern
    tracker.record_pattern(
        pattern_type="workflow",
        name="hardcoded_port_assignment",
        description="Using hardcoded port assignments can lead to conflicts when multiple services are running",
        code_example="app.run(debug=True, port=5002)",
        is_anti_pattern=True,
        tags=["port", "configuration", "flask"]
    )
    
    # Record the dynamic port allocation as a good pattern
    tracker.record_pattern(
        pattern_type="workflow",
        name="dynamic_port_allocation",
        description="Using a port manager to dynamically allocate available ports prevents conflicts",
        code_example="port = port_mgr.get_available_port(preferred_port)",
        is_anti_pattern=False,
        tags=["port", "configuration", "flask"]
    )
    
    # Generate project health report
    health = tracker.analyze_project_health()
    print("\n=== Project Health Report ===")
    print(f"Health Score: {health['health_score']}/100")
    print(f"Total Errors: {health['error_analysis'].get('total_errors', 0)}")
    print(f"Resolved: {health['error_analysis'].get('resolved_errors', 0)}")
    
    # Print recommendations
    print("\n=== Top Recommendations ===")
    for i, rec in enumerate(health.get('top_recommendations', []), 1):
        print(f"{i}. {rec['title']}")
        print(f"   {rec['description']}")
        print()
    
    # Scan codebase for issues
    print("\n=== Scanning Codebase for Issues ===")
    
    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    scan_results = tracker.scan_codebase(backend_dir)
    
    print(f"Scanned {scan_results['scanned_files']} files")
    print(f"Found {scan_results['issues_found']} potential issues")
    
    if scan_results['issues_by_type']:
        print("\nIssues by type:")
        for issue_type, count in scan_results['issues_by_type'].items():
            print(f"- {issue_type}: {count}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
import sys
import os
import argparse
try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Please run 'pip install pyyaml' to use this script.", file=sys.stderr)
    sys.exit(1)

def load_config(path):
    """Load YAML config from file path."""
    if not os.path.exists(path):
        print(f"Config file not found: {path}", file=sys.stderr)
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return None

def save_config(path, data):
    """Save YAML config to file path."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            # allow_unicode=True ensures Chinese characters are readable
            # default_flow_style=False ensures block style for readability
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"Successfully updated tags in {path}")
    except Exception as e:
        print(f"Error saving config: {e}", file=sys.stderr)

def parse_tag(tag_str):
    """Parse a tag string like '#Topic/Agent/LLM' into components."""
    tag_str = tag_str.strip()
    if not tag_str.startswith('#'):
        return None
    
    parts = tag_str[1:].split('/')
    if len(parts) < 2:
        return None
    
    return parts

def update_tags(config, new_tags):
    """Update config with new tags, supporting unlimited nesting via 'items'."""
    if 'groups' not in config:
        config['groups'] = []
    
    updated = False
    
    for tag in new_tags:
        parts = parse_tag(tag)
        if not parts:
            continue
            
        group_name = parts[0]
        
        # 1. Find or create Group
        group = next((g for g in config['groups'] if g.get('tag-name') == group_name), None)
        if not group:
            group = {'tag-name': group_name, 'items': []}
            config['groups'].append(group)
            updated = True
            
        # 2. Iteratively find or create items for nested tags
        current_level = group
        for i in range(1, len(parts)):
            part_name = parts[i]
            
            if 'items' not in current_level:
                current_level['items'] = []
                
            next_level = next((item for item in current_level['items'] if item.get('tag-name') == part_name), None)
            if not next_level:
                next_level = {'tag-name': part_name}
                current_level['items'].append(next_level)
                updated = True
                
            current_level = next_level
    
    return updated

def main():
    parser = argparse.ArgumentParser(description='Update omni-tags.yaml with new tags.')
    parser.add_argument('--config', default=os.path.expanduser('~/.omnitag/omni-tags.yaml'),
                        help='Path to omni-tags.yaml configuration file')
    parser.add_argument('tags', nargs='*', help='List of tags to add (e.g. #PARA/Project/NewProj)')
    
    args = parser.parse_args()
    
    # If no tags provided via args, try reading from stdin
    tags = args.tags
    if not tags and not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            # Handle space or newline separated tags
            import re
            tags = re.split(r'\s+', stdin_content)
    
    if not tags:
        print("No tags provided to update.")
        return

    config = load_config(args.config)
    if not config:
        # If file doesn't exist, create basic structure
        print(f"Creating new config at {args.config}")
        os.makedirs(os.path.dirname(args.config), exist_ok=True)
        config = {'groups': []}
        
    if update_tags(config, tags):
        save_config(args.config, config)
    else:
        print("No new tags to add.")

if __name__ == '__main__':
    main()

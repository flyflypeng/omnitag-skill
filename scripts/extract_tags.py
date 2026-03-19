import yaml
import sys

def _extract_recursive(node, current_path, tags_list):
    """
    Recursively extract tags from nodes.
    node: Current dictionary node (can be group or item)
    current_path: String representing the path up to this node
    tags_list: List to append the full tag paths to
    """
    name = node.get('tag-name', '')
    if not name:
        return
        
    # Build the path for current node
    if current_path:
        new_path = f"{current_path}/{name}"
    else:
        new_path = f"#{name}"
        
    # If the node has items, recursively process them
    items = node.get('items', [])
    if items:
        # We only add the node as a tag if it's NOT a top-level standalone tag (level-1)
        # Top-level tags like #Meta, #Topic are just containers when they have items.
        # But if we want to allow #Inbox (which might not have items), we handle that below.
        if current_path:
            tags_list.append(new_path)
            
        for item in items:
            _extract_recursive(item, new_path, tags_list)
    else:
        # Leaf node
        tags_list.append(new_path)

def extract_tags(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        tags = []
        
        if not data or 'groups' not in data:
            return []
            
        for group in data['groups']:
            _extract_recursive(group, "", tags)
            
        return tags
        
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return []

if __name__ == "__main__":
    file_path = '/Users/pengfei/Code/AI-Agent/skills/omnitag-skill/omni-tags.yaml'
    output_path = '/Users/pengfei/Code/AI-Agent/skills/omnitag-skill/omni-tags.txt'
    tags = extract_tags(file_path)
    
    # Format tags: 10 tags per line
    lines = []
    for i in range(0, len(tags), 10):
        chunk = tags[i:i+10]
        lines.append(' '.join(chunk))
    
    output_content = '\n'.join(lines)
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Tags written to {output_path} successfully.")
        # Also print to stdout for verification
        print(output_content)
    except Exception as e:
        print(f"Error writing to file: {e}")

"""
Collaborative Versioning + Comments
Scenario history, comments, and multi-user features.
"""
import json
import datetime
import uuid
from pathlib import Path
import os

# Storage path for collaboration data (would be a database in production)
STORAGE_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "data"

def manage_collaboration(scenario_id, action, data=None):
    """
    Args:
        scenario_id (str): Unique scenario identifier.
        action (str): Action type ('comment', 'history', 'approve', etc).
        data (dict, optional): Additional data for the action.
    Returns:
        dict: { 'status': str, 'history': list, 'comments': list }
    """
    # In a real implementation, this would be backed by a database
    # Here we use a simple file-based storage for demonstration
    
    # Create storage directory if it doesn't exist
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    # Load existing data or create new
    scenario_file = STORAGE_DIR / f"{scenario_id}.json"
    
    if scenario_file.exists():
        try:
            with open(scenario_file, 'r') as f:
                scenario_data = json.load(f)
        except:
            scenario_data = create_new_scenario_data(scenario_id)
    else:
        scenario_data = create_new_scenario_data(scenario_id)
    
    # Process different actions
    if action == 'history':
        # Return version history
        return {
            'status': 'ok',
            'history': scenario_data.get('versions', []),
            'comments': scenario_data.get('comments', [])
        }
    
    elif action == 'comment':
        if not data:
            return {'status': 'error', 'message': 'Comment data required', 'history': [], 'comments': []}
        
        # Add a new comment
        new_comment = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.datetime.now().isoformat(),
            'user': data.get('user', 'Anonymous'),
            'text': data.get('text', ''),
            'location': data.get('location', None)  # could be coordinates, segment ID, etc.
        }
        
        if 'comments' not in scenario_data:
            scenario_data['comments'] = []
        scenario_data['comments'].append(new_comment)
        
        # Save changes
        with open(scenario_file, 'w') as f:
            json.dump(scenario_data, f, indent=2)
        
        return {
            'status': 'ok',
            'message': 'Comment added',
            'history': scenario_data.get('versions', []),
            'comments': scenario_data.get('comments', [])
        }
    
    elif action == 'version':
        if not data:
            return {'status': 'error', 'message': 'Version data required', 'history': [], 'comments': []}
        
        # Add a new version
        new_version = {
            'id': str(uuid.uuid4()),
            'number': len(scenario_data.get('versions', [])) + 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'user': data.get('user', 'Anonymous'),
            'description': data.get('description', 'No description'),
            'changes': data.get('changes', []),
            'parent_id': data.get('parent_id', scenario_data.get('versions', [])[-1]['id'] if scenario_data.get('versions', []) else None)
        }
        
        if 'versions' not in scenario_data:
            scenario_data['versions'] = []
        scenario_data['versions'].append(new_version)
        
        # Save changes
        with open(scenario_file, 'w') as f:
            json.dump(scenario_data, f, indent=2)
        
        return {
            'status': 'ok',
            'message': 'Version created',
            'history': scenario_data.get('versions', []),
            'comments': scenario_data.get('comments', [])
        }
    
    elif action == 'approve':
        if not data:
            return {'status': 'error', 'message': 'Approval data required', 'history': [], 'comments': []}
        
        version_id = data.get('version_id')
        if not version_id:
            return {'status': 'error', 'message': 'Version ID required', 'history': [], 'comments': []}
            
        # Find the version
        for version in scenario_data.get('versions', []):
            if version['id'] == version_id:
                # Add approval
                if 'approvals' not in version:
                    version['approvals'] = []
                
                approval = {
                    'user': data.get('user', 'Anonymous'),
                    'timestamp': datetime.datetime.now().isoformat(),
                    'comment': data.get('comment', '')
                }
                
                version['approvals'].append(approval)
                break
        
        # Save changes
        with open(scenario_file, 'w') as f:
            json.dump(scenario_data, f, indent=2)
        
        return {
            'status': 'ok',
            'message': 'Version approved',
            'history': scenario_data.get('versions', []),
            'comments': scenario_data.get('comments', [])
        }
    
    elif action == 'fork':
        # Create a fork of the scenario
        new_scenario_id = f"{scenario_id}_fork_{uuid.uuid4().hex[:8]}"
        
        # Copy scenario data with new ID
        new_scenario_data = scenario_data.copy()
        new_scenario_data['id'] = new_scenario_id
        new_scenario_data['parent_id'] = scenario_id
        new_scenario_data['fork_point'] = datetime.datetime.now().isoformat()
        new_scenario_data['fork_user'] = data.get('user', 'Anonymous') if data else 'Anonymous'
        
        # Save new scenario
        new_scenario_file = STORAGE_DIR / f"{new_scenario_id}.json"
        with open(new_scenario_file, 'w') as f:
            json.dump(new_scenario_data, f, indent=2)
        
        return {
            'status': 'ok',
            'message': f'Scenario forked as {new_scenario_id}',
            'new_scenario_id': new_scenario_id,
            'history': new_scenario_data.get('versions', []),
            'comments': new_scenario_data.get('comments', [])
        }
    
    # Default return for unknown actions
    return {
        'status': 'ok',
        'message': f'No action performed for: {action}',
        'history': scenario_data.get('versions', []),
        'comments': scenario_data.get('comments', [])
    }

def create_new_scenario_data(scenario_id):
    """Create a new scenario data structure"""
    return {
        'id': scenario_id,
        'created': datetime.datetime.now().isoformat(),
        'versions': [{
            'id': str(uuid.uuid4()),
            'number': 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'user': 'System',
            'description': 'Initial version',
            'changes': [],
            'parent_id': None
        }],
        'comments': []
    }
import subprocess
import os
import re

def run():
    print("Starting filename fix process...")
    # Get the commit hash of the problematic branch
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'origin/arena/019ff899-arab']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        print("Error: Could not find origin/arena/019ff899-arab. Did you fetch it?")
        return

    # Use a temporary index file so we don't mess up the working directory's index
    os.environ['GIT_INDEX_FILE'] = '.git/temp_index'
    
    try:
        # Pass -c core.protectNTFS=false to bypass Windows filesystem checks in index
        def git_cmd(*args):
            return subprocess.check_output(['git', '-c', 'core.protectNTFS=false'] + list(args))
        
        # Read the tree of the problematic commit into our temp index
        subprocess.check_call(['git', '-c', 'core.protectNTFS=false', 'read-tree', commit_hash])

        # Get all files in the index
        output = git_cmd('ls-files', '-s', '-z').decode('utf-8')
        files = output.split('\0')[:-1]

        changes_made = False

        for file_info in files:
            parts = file_info.split('\t')
            if len(parts) != 2: continue
            meta = parts[0]
            path = parts[1]
            
            # Check for invalid characters in Windows: ?, :, |
            if re.search(r'[?:|]', path):
                changes_made = True
                # Replace invalid characters with a hyphen
                new_path = re.sub(r'[?:|]', '-', path)
                print(f"Fixing: {path}\n     -> {new_path}")
                
                # Remove old path from index
                subprocess.check_call(['git', '-c', 'core.protectNTFS=false', 'rm', '--cached', '--', path])
                
                mode_sha_stage = meta.split(' ')
                mode = mode_sha_stage[0]
                sha = mode_sha_stage[1]
                
                # Add new path to index
                subprocess.check_call(['git', '-c', 'core.protectNTFS=false', 'update-index', '--add', '--cacheinfo', f"{mode},{sha},{new_path}"])

        if changes_made:
            new_tree = git_cmd('write-tree').decode('utf-8').strip()
            new_commit = subprocess.check_output(
                ['git', 'commit-tree', new_tree, '-p', commit_hash, '-m', 'Fix invalid Windows filenames (?, :, |)']
            ).decode('utf-8').strip()
            
            subprocess.check_call(['git', 'branch', '-f', 'fixed-arena', new_commit])
            print(f"\nSuccess! Created new branch 'fixed-arena' at commit {new_commit}")
        else:
            print("\nNo invalid filenames found.")
            
    finally:
        # Clean up temporary index
        if os.path.exists('.git/temp_index'):
            os.remove('.git/temp_index')
        if 'GIT_INDEX_FILE' in os.environ:
            del os.environ['GIT_INDEX_FILE']

if __name__ == "__main__":
    run()

import os
import json
import sys

def run_recursive_audit():
    print(f"[VIVOS-V13.0] Starting Recursive Audit for {os.getcwd()}")
    
    # 1. Local Compliance Check
    manifest_path = ".vivos/manifest.json"
    if not os.path.exists(manifest_path):
        print("[!] ERROR: Missing .vivos/manifest.json")
        return False
        
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[!] ERROR: Failed to parse manifest: {e}")
        return False
        
    print(f"[+] Local Manifest Verified: Aggregate={manifest.get('aggregate')}")

    # 2. Peer Discovery (Recursive Logic)
    # Scan the shared home directory for sibling repositories
    workspace_root = os.path.expanduser("~")
    print(f"[+] Scanning Workspace for Peer Nodes in {workspace_root}...")
    
    peers = []
    try:
        for entry in os.listdir(workspace_root):
            peer_path = os.path.join(workspace_root, entry)
            if os.path.isdir(peer_path) and os.path.exists(os.path.join(peer_path, ".vivos/manifest.json")):
                peers.append(entry)
    except Exception as e:
        print(f"[!] Scan Warning: {e}")
            
    print(f"[+] Discovered {len(peers)} Vivos Peer Nodes: {peers}")
    
    # 3. Aggregate Integrity
    my_aggregate = manifest.get("aggregate")
    aggregate_peers = []
    for peer in peers:
        peer_manifest_path = os.path.join(workspace_root, peer, ".vivos/manifest.json")
        try:
            with open(peer_manifest_path, "r") as pf:
                p_manifest = json.load(pf)
                if p_manifest.get("aggregate") == my_aggregate:
                    aggregate_peers.append(peer)
        except:
            continue
            
    print(f"[+] Aggregate '{my_aggregate}' Integrity: {len(aggregate_peers)} members active.")
    
    # 4. Result Affirmation
    if len(aggregate_peers) > 0:
        print("[TOTAL AFFIRMATION] Core resonance detected.")
    else:
        print("[!] WARNING: Isolated node detected. Check aggregate mapping.")
        
    return True

if __name__ == "__main__":
    success = run_recursive_audit()
    sys.exit(0 if success else 1)

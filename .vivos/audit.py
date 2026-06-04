import os
import json
import sys

# WRAITH-MESH members
EXPECTED_MEMBERS = ['oi', 'olocoo', 'Auto', 'Mutante-Apex-Functions']

def run_wraith_mesh_audit():
    print(f"[WRAITH-MESH-V13.0] Starting Recursive Fusion Audit for {os.getcwd()}")
    
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
        
    if manifest.get('aggregate') != "WRAITH-MESH":
        print(f"[!] ERROR: Repository not part of WRAITH-MESH aggregate (Current: {manifest.get('aggregate')})")
        return False

    print(f"[+] Local Manifest Verified: Role={manifest.get('nexus_role')}")

    # 2. Wraith-Mesh Fusion Check (Peer Discovery)
    workspace_root = os.path.expanduser("~")
    discovered_members = []
    
    for member in EXPECTED_MEMBERS:
        p_manifest_path = os.path.join(workspace_root, member, ".vivos/manifest.json")
        if os.path.exists(p_manifest_path):
            try:
                with open(p_manifest_path, "r") as pf:
                    p_manifest = json.load(pf)
                    if p_manifest.get("aggregate") == "WRAITH-MESH":
                        discovered_members.append(member)
            except:
                continue
                
    print(f"[+] WRAITH-MESH Fusion Status: {len(discovered_members)}/{len(EXPECTED_MEMBERS)} members active.")
    for member in EXPECTED_MEMBERS:
        status = "ONLINE" if member in discovered_members else "OFFLINE"
        print(f"  - {member}: {status}")
        
    # 3. Resonance Logic
    if len(discovered_members) == len(EXPECTED_MEMBERS):
        print("[TOTAL AFFIRMATION] WRAITH-MESH IS FULLY RESONANT.")
    else:
        print("[!] WARNING: Incomplete Fusion. Some members are missing or misconfigured.")
        
    return True

if __name__ == "__main__":
    success = run_wraith_mesh_audit()
    sys.exit(0 if success else 1)

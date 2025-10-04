import shlex
import subprocess
from pathlib import Path
import os

import modal

streamlit_script_local_path = Path(__file__).parent / "streamlit_run.py"
streamlit_script_remote_path = "/root/streamlit_run.py"
image = (
    modal.Image.debian_slim(python_version="3.9")
    .uv_pip_install("streamlit", "supabase", "pandas", "plotly", "python-dotenv")
    .env({"FORCE_REBUILD": "true"})  # 🚨 Add this line to force a rebuild
    .add_local_file(streamlit_script_local_path, streamlit_script_remote_path)
    .add_local_file("data_full.csv", "/root/data_full.csv")
    .add_local_file("half_marathon_results.csv", "/root/half_marathon_results.csv")
    .add_local_file("results_10k.csv", "/root/results_10k.csv")
    .add_local_file("results_5k.csv", "/root/results_5k.csv")
)
app = modal.App(name="Full-Marathon-Data", image=image)

if not streamlit_script_local_path.exists():
    raise RuntimeError(
        "Hey your starter streamlit isnt working"
    )

@app.function(
    allow_concurrent_inputs=100,
    secrets=[modal.Secret.from_name("custom-secret-jason")]
)
@modal.web_server(8000)
def run():
    target = shlex.quote(streamlit_script_remote_path)
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    # Build environment variables, filtering out None values
    env_vars = {}
    if os.getenv("SUPABASE_KEY"):
        env_vars["SUPABASE_KEY"] = os.getenv("SUPABASE_KEY")
    if os.getenv("SUPABASE_URL"):
        env_vars["SUPABASE_URL"] = os.getenv("SUPABASE_URL")
    
    # Include current environment to ensure PATH and other essential vars are available
    env_vars.update(os.environ)
        
    subprocess.Popen(cmd, shell=True, env=env_vars)
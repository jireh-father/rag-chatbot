import argparse
import llama_index
from dotenv import load_dotenv
from .ui import LocalChatbotUI
from .pipeline import LocalRAGPipeline
from .logger import Logger
from .ollama import run_ollama_server, is_port_open

load_dotenv()

# CONSTANTS
LOG_FILE = "logging.log"
DATA_DIR = "data/data"
AVATAR_IMAGES = ["./assets/user.png", "./assets/bot.png"]

# PARSER
parser = argparse.ArgumentParser()
parser.add_argument(
    "--host", type=str, default="localhost",
    help="Set host to local or in docker container"
)
parser.add_argument(
    "--pipeline_host", type=str, default="127.0.0.1",
    help="Set host to local or in docker container"
)
parser.add_argument(
    "--share", action='store_true',
    help="Share gradio app"
)
parser.add_argument(
    "--port", type=int, default=7860,
    help="Set port number"
)
# azure_api_key
parser.add_argument("--azure_api_key", type=str, default=None)
# azure_endpoint
parser.add_argument("--azure_endpoint", type=str, default=None)
# azure_api_version
parser.add_argument("--azure_api_version", type=str, default=None)
# azure_deployment_name
parser.add_argument("--azure_deployment_name", type=str, default=None)
# azure_embed_deployment_name
parser.add_argument("--azure_embed_deployment_name", type=str, default=None)
# azure_embed_api_version
parser.add_argument("--azure_embed_api_version", type=str, default=None)
args = parser.parse_args()

# OLLAMA SERVER
if args.host != "host.docker.internal":
    port_number = 11434
    if not is_port_open(port_number):
        run_ollama_server()

# LOGGER

llama_index.core.set_global_handler("simple")
logger = Logger(LOG_FILE)
logger.reset_logs()

# PIPELINE
pipeline = LocalRAGPipeline(host=args.pipeline_host, args=args)

# UI
ui = LocalChatbotUI(
    pipeline=pipeline,
    logger=logger,
    host=args.host,
    data_dir=DATA_DIR,
    avatar_images=AVATAR_IMAGES
)

ui.build().launch(
    share=args.share,
    server_name="0.0.0.0",
    debug=True,
    show_api=False,
    server_port=args.port,
    ssl_verify=False
)

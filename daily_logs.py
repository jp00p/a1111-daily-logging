import modules.scripts as scripts
from modules import shared
import gradio as gr
import os
from modules.processing import process_images, Processed
from modules.paths import script_path
from datetime import date
import csv

class Script(scripts.Script):
  
  def title(self):
    return "DailyLogs"
 
  def show(self, is_img2img):
    return scripts.AlwaysVisible

  def ui(self, is_img2img):
    enable_daily_logs = gr.Checkbox(True, label="Enable logging")
    return [enable_daily_logs]

  def process(self, p, enable_daily_logs):
    if enable_daily_logs:      
      model_checkpoint = shared.opts.sd_model_checkpoint
      filename = f"{date.today()}.csv"
      logpath = os.path.join(script_path, "daily_logs")
      file_exists = os.path.isfile(os.path.join(logpath, filename))
      if not os.path.exists(logpath):
        os.mkdir(logpath)
      with open(os.path.join(logpath, filename), "a+", encoding="utf-8-sig", newline='') as file:
        fieldnames = ["Prompt", "Negative Prompt", "Model", "Seed"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
          writer.writeheader()
        writer.writerow({"Prompt":p.prompt, "Negative Prompt":p.negative_prompt, "Model":model_checkpoint, "Seed":p.seed})
#!/usr/bin/env python3
"""
Manim动画编译API服务 - Bottle版本
使用Bottle框架替代FastAPI，更轻量级
"""

import json
import subprocess
import tempfile
import os
import uuid
import shutil
import time
import threading
from pathlib import Path
import logging
from bottle import Bottle, request, response, static_file, abort
from meta import generate_code
from pydantic import BaseModel
from os import system

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Bottle()
videos_dir = Path(__file__).parent / "videos"
srt_dir = Path(__file__).parent / "srt"
generate_video_dir = Path(__file__).parent / "media/videos/result/480p15/"
SCENE_NAME = "MainAnimation"

# 存储任务状态
tasks = {}

class CompileResponse(BaseModel):
    task_id: str
    status: str
    message: str
    video_url: str | None = None
    srt_url: str |None = None
def run_manim_compile(task_id: str, code: str, scene_name: str, quality: str, resolution: str):
    """
    在后台运行Manim编译任务
    """
    try:
        tasks[task_id]["status"] = "processing"
        tasks[task_id]["message"] = "开始编译..."

        # 使用generate_code生成result.py
        logger.info(f"任务 {task_id}: 生成Python代码...")
        generate_code(code)

        # 将生成的result.py复制到临时目录
        result_py_path = Path("result.py")
        if not result_py_path.exists():
            error_msg = "generate_code未生成result.py文件"
            logger.error(f"任务 {task_id}: {error_msg}")
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["message"] = error_msg
            return
        
        status = system(command:=f"manim -ql .\\result.py {SCENE_NAME} --disable_caching")

        if status != 0:
            error_msg = f"Manim编译失败"
            logger.error(f"任务 {task_id}: {error_msg}")
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["message"] = error_msg
            return

        logger.info(f"任务 {task_id}: Manim编译成功")

        video_file = generate_video_dir / f"{SCENE_NAME}.mp4"
        srt_file = generate_video_dir / f"{SCENE_NAME}.srt"
        assert video_file.exists() and srt_file.exists()
        
        logger.info(f"任务 {task_id}: 找到视频文件: {video_file}")
        # 将视频文件移动到videos文件夹，以task_id命名
        final_video_path = videos_dir / f"{task_id}.mp4"
        final_srt_path = srt_dir / f"{task_id}.srt"
        shutil.copy2(video_file, final_video_path)
        shutil.copy2(srt_file, final_srt_path)

        # 更新任务状态
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["message"] = "编译完成"
        tasks[task_id]["video_path"] = str(final_video_path)
        tasks[task_id]["video_url"] = f"/videos/{task_id}.mp4"
        tasks[task_id]["srt_url"] = f"/videos/{task_id}.srt"

        logger.info(f"任务 {task_id}: 视频文件已保存到 {final_video_path}")

    except Exception as e:
        error_msg = f"编译过程中发生错误: {str(e)}"
        logger.error(f"任务 {task_id}: {error_msg}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["message"] = error_msg

@app.route('/api/compile', method='POST')
def compile_animation():
    """
    提交Manim代码进行编译
    """
    try:
        # 直接读取请求体的原始内容作为code
        code = request.body.read().decode('utf-8')
        if not code:
            abort(400, "请求体不能为空")

        # 使用默认参数
        scene_name = "MainAnimation"
        quality = "medium"
        resolution = "480p15"

        task_id = str(uuid.uuid4())

        # 初始化任务状态
        tasks[task_id] = {
            "status": "pending",
            "message": "任务已创建，等待处理",
            "video_path": None,
            "video_url": None,
            "srt_url": None,
            "created_at": time.time()
        }

        # 在后台线程中运行编译任务
        thread = threading.Thread(
            target=run_manim_compile,
            args=(task_id, code, scene_name, quality, resolution)
        )
        thread.daemon = True
        thread.start()

        # 返回响应
        response.content_type = 'application/json'
        res = CompileResponse(
            task_id=task_id,
            status="pending",
            message="编译任务已提交，正在后台处理",
        )
        return json.dumps(res.__dict__)

    except Exception as e:
        logger.error(f"任务创建失败: {str(e)}")
        abort(500, f"任务创建失败: {str(e)}")

@app.route('/api/tasks/<task_id>')
def get_task_status(task_id):
    """
    获取任务状态
    """
    if task_id not in tasks:
        abort(404, "任务不存在")

    task = tasks[task_id]
    response.content_type = 'application/json'
    return json.dumps(CompileResponse(
        task_id=task_id,
        status=task["status"],
        message=task["message"],
        video_url=task.get("video_url")
    ).__dict__)

@app.route('/videos/<filename:path>')
def serve_video(filename):
    """
    提供videos文件夹的静态文件服务
    """
    video_path:Path = videos_dir / filename

    if not video_path.exists():
        abort(404, "视频文件不存在")

    return static_file(
        filename,
        root=str(videos_dir),
        download=filename
    )

@app.route('/srt/<filename:path>')
def serve_srt(filename):
    srt_path = srt_dir / filename

    if not srt_path.exists():
        abort(404, "字幕不存在")

    return static_file(
        filename,
        root=str(srt_dir),
        download=filename
    )

@app.route('/videos')
def list_videos():
    """
    列出所有生成的视频文件
    """
    video_files = list(videos_dir.glob("*.mp4"))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>视频文件索引</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
            a { color: #0066cc; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .empty { color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <h1>生成的视频文件</h1>
    """

    if video_files:
        html += "<ul>"
        for video_file in sorted(video_files):
            filename = video_file.name
            html += f'<li><a href="/videos/{filename}">{filename}</a></li>'
        html += "</ul>"
    else:
        html += '<p class="empty">暂无视频文件</p>'

    html += """
    </body>
    </html>
    """

    response.content_type = 'text/html; charset=utf-8'
    return html


if __name__ == "__main__":
    # 创建必要的目录
    videos_dir.mkdir(parents=True, exist_ok=True)
    srt_dir.mkdir(parents=True, exist_ok=True)
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=False)
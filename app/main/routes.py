""" all routes will end up here or loaded here for flask """
# pylint:disable=cyclic-import
import os
from time import sleep

import requests
from flask import jsonify, request

from app.main import BP as blueprint


@blueprint.route('/', methods=['POST'])
def main_route():
    """ Main route """
    api_key = request.headers.get('Authorization', request.args.get('api_key'))
    if api_key == f'Bearer {os.environ.get("API_KEY", '')}' or api_key == os.environ.get('API_KEY', ''): # pylint:disable=line-too-long
        for key in request.files:
            attachment = request.files[key]
            file_content = attachment.read()
            file_dir = os.environ.get('FILE_DIR', '/tmp')
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(f'{file_dir}/{attachment.filename}', 'wb') as file:  # pylint:disable=unspecified-encoding
                file.write(file_content)

            print(f'file saved to {file_dir}/{attachment.filename}', flush=True)

            with open(f'{file_dir}/{attachment.filename}', "rb") as file:
                tag_names = list(request.form.get('To', '').split('@')[0].split('+'))
                tags_resp = requests.get(
                    f'{os.environ.get("PAPERLESS_URL")}/api/tags/',
                    headers={"Authorization": f'Token {os.environ.get("PAPERLESS_API_KEY")}'},
                    timeout=10,
                ).json()
                tag_ids = [tag["id"] for tag in tags_resp["results"] if tag["name"] in tag_names] # pylint:disable=line-too-long

                print(f'Uploading {attachment.filename} to {os.environ.get("PAPERLESS_URL")} with tags {tag_ids}', flush=True) # pylint:disable=line-too-long
                resp = requests.post(
                    f'{os.environ.get("PAPERLESS_URL")}/api/documents/post_document/',
                    files={"document": file},
                    data={
                        "title": attachment.filename,
                        "tags": tag_ids,
                    },
                    headers={"Authorization": f'Token {os.environ.get("PAPERLESS_API_KEY")}'},
                    timeout=90,
                )

                task_id = resp.json()
                print(f'Upload complete. Task ID: {task_id}', flush=True)

                for _ in range(20):
                    print(f'Checking on task {task_id} ...', flush=True)
                    task_resp = requests.get(
                        f'{os.environ.get("PAPERLESS_URL")}/api/tasks/',
                        headers={"Authorization": f'Token {os.environ.get("PAPERLESS_API_KEY")}'}, # pylint:disable=line-too-long
                        params={'task_id': task_id},
                        timeout=10,
                    )
                    task_status = task_resp.json()[0]['status']

                    if task_status in ["STARTED", "PENDING"]:
                        print(f'waiting for task {task_id} to complete...', flush=True)
                        sleep(60)
                    elif task_status == "SUCCESS":
                        print(f'task {task_id} completed successfully', flush=True)
                        break
                    elif task_status == "FAILURE":
                        print(f'task {task_id} failed', flush=True)
                        break
                    else:
                        print(f'Unknown task status: {task_status}', flush=True)
                        break



            ## Print or log attachments
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'unauthorized'}), 401

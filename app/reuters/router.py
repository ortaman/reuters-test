
import json 
import pandas as pd
from fastapi import APIRouter, Depends

from app.reuters.dependencies import DMSApi
from app.reuters.schemas import DateRange


router = APIRouter()


@router.get("/casetext_sync/", tags=["casetext"])
async def casetext_syncronization(date_range: DateRange = Depends()):
    dms_api = DMSApi()

    yesterday_fs_path =  dms_api.get_content_file(date=date_range.start_date)
    today_fs_path =  dms_api.get_content_file(date=date_range.end_date)
 
    yesterday_files_stored = pd.read_json(path_or_buf=yesterday_fs_path, lines=True)
    today_files_stored = pd.read_json(path_or_buf=today_fs_path, lines=True)

    delete_files = []
    update_files_name = []
    update_files_meta = []

    for row in yesterday_files_stored.itertuples(index=False):
        id = row[0]
        
        today_file_stored = today_files_stored[today_files_stored['id'] == id]
        
        if today_file_stored.index.empty:
            delete_files.append({"id": row[0]})

        else:

            if row[1] != today_file_stored.iloc[0, 1]:
                update_files_name.append({"id": row[0], "name": today_file_stored.iloc[0, 1]})

            if row[2] != today_file_stored.iloc[0, 2]:
                update_files_meta.append({"id": row[0], "meta": today_file_stored.iloc[0, 2]})
            
        today_files_stored = today_files_stored.drop(today_file_stored.index)

    response = {
        "createFile": today_files_stored.to_dict(orient='records'),
        "deleteFile": delete_files,
        "updateFileName": update_files_name,
        "updateFileMeta": update_files_meta
    }

    return response


"""
@router.get("/casetext_sync_v1/", tags=["casetext"])
async def casetext_syncronization(date_range: DateRange = Depends()):
    dms_api = DMSApi()

    yesterday_fs_path =  dms_api.get_content_file(date=date_range.start_date)
    today_fs_path =  dms_api.get_content_file(date=date_range.end_date)

    response = {
        "createFile": [],
        "deleteFile": [],
        "updateFileName": [],
        "updateFileMeta": []
    }

    with open(yesterday_fs_path, 'r') as file1:

        for line1 in file1:
            exits_row = False
            dict_line1 = json.loads(line1)

            with open(today_fs_path, 'r') as file2:
                for line2 in file2:
                    dict_line2 = json.loads(line2)

                    if dict_line1["id"] == dict_line2["id"]:
                        exits_row = True

                        if dict_line1["name"] != dict_line2["name"]:
                            del dict_line2['meta']
                            response["updateFileName"].append(dict_line2)

                        elif dict_line1["meta"] != dict_line2["meta"]:
                            del dict_line2['name']
                            response["updateFileMeta"].append(dict_line2)
                        
                        break
                
                if not exits_row:
                    response["deleteFile"].append({"id": dict_line1["id"]})

    with open(today_fs_path, 'r') as file1:

        for line1 in file1:
            exits_row = False
            dict_line1 = json.loads(line1)

            with open(yesterday_fs_path, 'r') as file2:
                for line2 in file2:
                    dict_line2 = json.loads(line2)

                    if dict_line1["id"] == dict_line2["id"]:
                        exits_row = True
                        break
                
                if not exits_row:
                    response["createFile"].append(dict_line1)

    return response
"""
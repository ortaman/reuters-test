
import pandas as pd

from fastapi import APIRouter, Depends

from app.reuters.dependencies import DMSApi
from app.reuters.schemas import DateRange


router = APIRouter()


@router.get("/casetext_sync/", tags=["casetext"])
async def casetext_syncronization(date_range: DateRange = Depends()):
    dms_api = DMSApi()

    yesterday_files_stored =  dms_api.get_files_stored(date=date_range.start_date)
    today_files_stored =  dms_api.get_files_stored(date=date_range.end_date)
 
    yesterday_files_stored = pd.read_json(path_or_buf=yesterday_files_stored, lines=True)
    today_files_stored = pd.read_json(path_or_buf=today_files_stored, lines=True)

    delete_files = {}
    update_files_name = {}
    update_files_meta = {}
    i = 0


    for row in yesterday_files_stored.itertuples(index=False):
        id = row[0]
        
        today_file_stored = today_files_stored[today_files_stored['id'] == id]
        
        if today_file_stored.index.empty:
            delete_files[i] = {"id": row[0]}
            i += 1

        else:

            if row[1] != today_file_stored.iloc[0, 1]:
                update_files_name[i] = {"id": row[0], "name": today_file_stored.iloc[0, 1]}

            if row[2] != today_file_stored.iloc[0, 2]:
                update_files_meta[i] = {"id": row[0], "meta": today_file_stored.iloc[0, 2]}
            
            i += 1
            
            today_files_stored = today_files_stored.drop(today_file_stored.index)

    delete_files_df = pd.DataFrame.from_dict(delete_files, "index")
    update_files_name_df = pd.DataFrame.from_dict(update_files_name, "index")
    update_files_meta_df = pd.DataFrame.from_dict(update_files_meta, "index")

    response = {
        "createFile": today_files_stored.to_json(orient='records', lines=False),
        "deleteFile": delete_files_df.to_json(orient='records', lines=False),
        "updateFileName": update_files_name_df.to_json(orient='records', lines=False),
        "updateFileMeta": update_files_meta_df.to_json(orient='records', lines=False)
    }

    return response

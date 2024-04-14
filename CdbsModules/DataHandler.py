"""This file contains functions for log, processing responses, working with files, and checking"""

import time
import requests
import json
import logging
from pathlib import Path
from types import SimpleNamespace
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import CdbsModules.CdbsEvn as CdbsEvn
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


def validation_uuid(target_uuid):
    """Checking an uuid length. Return target UUID if valid or None if the uuid failed the test"""
    if target_uuid and len(target_uuid) == CdbsEvn.g_len_uuid:
        return target_uuid
    return None


def handle_response(reply):
    if reply.status_code == requests.codes.ok:
        logger('debug', translate('cdbs', 'Success.'))
        return True
    else:
        logger(
            'error',
            translate('cdbs', 'Failed, status code:')
            + f' {reply.status_code}',
        )
        return False

def get_file(args):
    """Downloads and saves a file of args data to the user's local storage.
    Argument (args) for this function have url and filepath (path/filename).
    """
    t0 = time.time()
    url = args[0]
    filepath = args[1]
    if filepath.exists():
        logger(
            'warning',
            translate('cdbs', 'File already exists and skipped:')
            + f' "{filepath}".',
        )
        return filepath, time.time() - t0
    try:
        headers = {'User-Agent': CdbsEvn.g_user_agent}
        reply = requests.get(url, headers=headers)
    except Exception as e:
        logger(
            'error',
            translate('cdbs', 'Exception in download file:')
            + f' {e}',
        )
    else:
        if handle_response(reply):
            with filepath.open('wb') as fd:
                for chunk in reply.iter_content(chunk_size=128):
                    fd.write(chunk)
        else:
            logger('error', translate('cdbs', 'Error:') + f' {reply.error()}')
    return filepath, time.time() - t0


def download_parallel(args):
    """Running the file download function in parallel streams and keeps track of the total download time (if available)"""
    t0 = time.time()
    results = ThreadPool(cpu_count() - 1).imap_unordered(get_file, args)
    for result in results:
        logger(
            'log',
            translate('cdbs', 'path:')
            + f' "{result[0]}"'
            + translate('cdbs', 'time:')
            + f' {result[1]} '
            + translate('cdbs', 'sec')
            + ')',
        )
    logger(
        'message',
        translate('cdbs', 'Total time:')
        + f'{time.time() - t0}'
        + translate('cdbs', 'sec'),
    )


def parsing_gpl():
    """Parsing data from file with a response into a namespace"""
    logger('debug', translate('cdbs', 'Data processing, please wait.'))
    if not CdbsEvn.g_response_path.exists():
        logger('error', translate('cdbs', 'Not found file with response.'))
        return
    try:
        with CdbsEvn.g_response_path.open('rb', buffering=0) as f:
            res = json.loads(f.readall(), object_hook=lambda d: SimpleNamespace(**d))
            if res.data:
                return res.data
            # if there is no data, tries to get an error message
            logger('error', translate('cdbs', 'There was an error with response processing.'))
            for error in res.errors:
                logger('error', error.message)
    except Exception as e:
        logger(
            'error',
            translate('cdbs', 'Exception occurred while parsing the server response:')
            + f' {str(e)}',
        )


def remove_object(rm_object: Path):
    """Removing directory or file from local storage"""
    if not rm_object.exists():
        logger('log', translate('cdbs', 'No data found to delete.'))
        return
    # saving the previous server response to a log file, if it exists
    if (
        rm_object == CdbsEvn.g_response_path
        and CdbsEvn.g_log_file_path.is_file()
    ):
        try:
            with open(CdbsEvn.g_response_path) as response_file:
                with open(CdbsEvn.g_log_file_path, 'a') as log_file:
                    log_file.write(f'\nResponse before {time.time()}:\n')
                    for line in response_file:
                        log_file.write(line)
            response_file.close()
            log_file.close()
        except Exception as e:
            logger(
                'error',
                translate('cdbs', 'Exception occurred while trying to save old response:')
                + f' {str(e)}',
            )
    if rm_object.is_dir():
        Path.rmdir(rm_object)
    else:
        Path.unlink(rm_object)
    logger('log', f'"{rm_object}" ' + translate('cdbs', 'removed'))


def create_object_path(new_dir: Path, object_info: str, object_type: str):
    """Creating a new object path"""
    if new_dir.is_file():
        logger(
            'error',
            translate('cdbs', 'Please delete this file for correct operation:')
            + f'\n"{new_dir}"\n',
        )
        return
    if not new_dir.is_dir():
        Path.mkdir(new_dir)
    if object_type == 'modification':
        new_dir = Path(new_dir / CdbsEvn.g_program_name)
        if not new_dir.is_dir():
            Path.mkdir(new_dir)
    new_info_file = new_dir / object_type
    try:
        with new_info_file.open('w') as f:
            f.write(json.dumps(object_info, default=lambda o: o.__dict__, indent=4))
            f.close()
    except Exception as e:
        logger(
            'error',
            translate('cdbs', 'Exception occurred while trying to write the file:')
            + f' {str(e)}',
        )


def read_object_info(info_file: Path, select_object: str):
    """Reading information about an object from a special file"""
    try:
        with info_file.open('r') as data_file:
            object_info = json.loads(data_file.read(), object_hook=lambda d: SimpleNamespace(**d))
            logger('log', translate('cdbs', 'Selected') + f' {select_object}: {object_info.uuid}')
            data_file.close()
    except Exception as e:
        logger(
            'error',
            translate('cdbs',  'Exception when trying to read information from the file:')
            + f' {str(e)}',
        )
    else:
        return object_info


def deep_parsing_gpl(target, try_dict=False):
    """Parsing response data with SimpleNamespace by target key and then return structure"""
    data = parsing_gpl()
    if not data:
        logger(
            'log',
            translate('cdbs', 'Failed to parse GraphQL before deep parsing:')
            + f' {data}',
        )
        return
    try:
        pre_result = getattr(data, target)
    except Exception as e:
        logger(
            'warning',
            translate('cdbs', 'Received data is not suitable for processing about')
                + f' "{target}": {e}',
            )
        return
    if not try_dict:
        return pre_result
    # converting namespace to dict
    result = []
    for rd in pre_result:
        result.append(vars(rd))
    return result


def get_uuid(structure_data):
    """Getting an uuid if it exists in the data. Returning None if not found uuid."""
    target_uuid = None
    logger('log', translate('cdbs', 'Structure data:') + f' {structure_data}')
    if not structure_data:
        logger(
            'log',
            translate('cdbs', 'Not found data for UUID selection:')
            + f' {structure_data}',
        )
        return
    vars_data = structure_data[0]
    logger('log', translate('cdbs', 'Structure vars:') + f' {vars_data}')
    # are the known fields that store the uuid of the object
    if vars_data.get('uuid'):
        target_uuid = vars_data.get('uuid')
    if vars_data.get('fileUuid'):
        target_uuid = vars_data.get('fileUuid')
    logger(
        'log',
        translate('cdbs', 'UUID of structure data:')
        + f' {target_uuid}',
    )
    return validation_uuid(target_uuid)

# -*- coding: utf-8 -*-

"""
why aiohttp over httpx?
    - Our module is fully using asynchronous which is aiohttp spesialization
    - has more mature asyncio support than httpx
    - aiohttp is more suitable for applications that require high concurrency and low latency, such as web scraping or real-time data processing.

references:
    - https://github.com/encode/httpx/issues/3215#issuecomment-2157885121
    - https://github.com/encode/httpx/discussions/3100
    - https://brightdata.com/blog/web-data/requests-vs-httpx-vs-aiohttp


"""

# built ins
import asyncio
from typing import Dict

# installed
import aiohttp
from aiohttp.helpers import BasicAuth

# user defined formula
from streaming_helper.utilities import string_modification as str_mod
from streaming_helper.restful_api.telegram import end_point_params_template as telegram_end_point


async def get_connected(
    connection_url: str,
    endpoint: str= None,
    client_id: str = None,
    client_secret: str = None,
    params: str = None,
) -> None:

    try:
            
        async with aiohttp.ClientSession() as session:

            if endpoint:
                
                connection_endpoint = connection_url + endpoint

            if client_id:

                if "telegram" in connection_url:

                    endpoint = telegram_end_point.message_end_point(
                        client_id,
                        client_secret,
                        params
                    )

                    connection_endpoint = connection_url + endpoint

                    async with session.get(connection_endpoint) as response:

                        # RESToverHTTP Response Content
                        response = await response.json()

                if "deribit" in connection_url:

                    id = str_mod.id_numbering(
                        endpoint,
                        endpoint,
                    )

                    payload: Dict = {
                        "jsonrpc": "2.0",
                        "id": id,
                        "method": f"{endpoint}",
                        "params": params,
                    }

                    async with session.post(
                        connection_endpoint,
                        auth=BasicAuth(client_id, client_secret),
                        json=payload,
                    ) as response:

                        # RESToverHTTP Status Code
                        status_code: int = response.status

                        # RESToverHTTP Response Content
                        response: Dict = await response.json()

            else:

                async with session.get(connection_endpoint) as response:

                    # RESToverHTTP Response Content
                    response: Dict = await response.json()

            return response
        
    except Exception as error:

        await system_tools.parse_error_message_with_redis(
            client_redis,
            error,
        )   

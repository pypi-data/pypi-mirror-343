from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from typing import List, Dict, Any
import json

# Initialize FastMCP server
mcp = FastMCP("metricool")

# Constants
METRICOOL_BASE_URL = "https://app.metricool.com/api"
METRICOOL_USER_TOKEN = os.getenv("METRICOOL_USER_TOKEN")
METRICOOL_USER_ID = os.getenv("METRICOOL_USER_ID")

DATA = {
  "providers": [
    {
      "network": "<string>",
      "id": "<string>",
      "status": "PUBLISHED",
      "publicUrl": "<string>",
      "detailedStatus": "<string>"
    },
    {
      "network": "<string>",
      "id": "<string>",
      "status": "ERROR",
      "publicUrl": "<string>",
      "detailedStatus": "<string>"
    }
  ],
  "publicationDate": {
    "dateTime": "<string>",
    "timezone": "<string>"
  },
  "text": "<string>",
  "id": "<integer>",
  "creationDate": {
    "dateTime": "<string>",
    "timezone": "<string>"
  },
  "firstCommentText": "<string>",
  "media": [
    "<string>",
    "<string>"
  ],
  "autoPublish": "<boolean>",
  "saveExternalMediaFiles": "<boolean>",
  "mediaAltText": [
    "<string>",
    "<string>"
  ],
  "shortener": "<boolean>",
  "draft": "<boolean>",
  "location": {
    "name": "<string>",
    "link": "<string>",
    "id": "<string>",
    "location": {
      "city": "<string>",
      "country": "<string>",
      "state": "<string>",
      "street": "<string>",
      "zip": "<string>",
      "latitude": "<double>",
      "longitude": "<double>"
    },
    "deleted": "<boolean>"
  },
  "videoCoverMilliseconds": "<long>",
  "videoThumbnailUrl": "<string>",
  "parentId": "<integer>",
  "twitterData": {
    "tags": [
      {
        "username": "<string>",
        "x": "<double>",
        "y": "<double>",
        "deleted": "<boolean>"
      },
      {
        "username": "<string>",
        "x": "<double>",
        "y": "<double>",
        "deleted": "<boolean>"
      }
    ]
  },
  "facebookData": {
    "boost": "<double>",
    "boostPayer": "<string>",
    "boostBeneficiary": "<string>",
    "type": "<string>",
    "title": "<string>"
  },
  "smartLinkData": {
    "targetUrl": "<string>",
    "ids": [
      "<integer>",
      "<integer>"
    ]
  },
  "instagramData": {
    "autoPublish": "<boolean>",
    "tags": [
      {
        "username": "<string>",
        "x": "<double>",
        "y": "<double>",
        "deleted": "<boolean>"
      },
      {
        "username": "<string>",
        "x": "<double>",
        "y": "<double>",
        "deleted": "<boolean>"
      }
    ],
    "productTags": [
      {
        "productName": "<string>",
        "productId": "<string>",
        "x": "<double>",
        "y": "<double>",
        "catalogId": "<string>"
      },
      {
        "productName": "<string>",
        "productId": "<string>",
        "x": "<double>",
        "y": "<double>",
        "catalogId": "<string>"
      }
    ],
    "carouselTags": {
      "enim1": [
        {
          "username": "<string>",
          "x": "<double>",
          "y": "<double>",
          "deleted": "<boolean>"
        },
        {
          "username": "<string>",
          "x": "<double>",
          "y": "<double>",
          "deleted": "<boolean>"
        }
      ]
    },
    "carouselProductTags": {
      "pariatur3": [
        {
          "productName": "<string>",
          "productId": "<string>",
          "x": "<double>",
          "y": "<double>",
          "catalogId": "<string>"
        },
        {
          "productName": "<string>",
          "productId": "<string>",
          "x": "<double>",
          "y": "<double>",
          "catalogId": "<string>"
        }
      ],
      "pariatur__": [
        {
          "productName": "<string>",
          "productId": "<string>",
          "x": "<double>",
          "y": "<double>",
          "catalogId": "<string>"
        },
        {
          "productName": "<string>",
          "productId": "<string>",
          "x": "<double>",
          "y": "<double>",
          "catalogId": "<string>"
        }
      ]
    },
    "type": "<string>",
    "showReelOnFeed": "<boolean>",
    "boost": "<double>",
    "boostPayer": "<string>",
    "boostBeneficiary": "<string>",
    "audioName": "<string>",
    "collaborators": [
      {
        "username": "<string>",
        "deleted": "<boolean>"
      },
      {
        "username": "<string>",
        "deleted": "<boolean>"
      }
    ]
  },
  "pinterestData": {
    "boardId": "<string>",
    "pinTitle": "<string>",
    "pinLink": "<string>",
    "pinNewFormat": "<boolean>"
  },
  "youtubeData": {
    "title": "<string>",
    "type": "<string>",
    "privacy": "<string>",
    "tags": [
      "<string>",
      "<string>"
    ],
    "category": "<string>",
    "madeForKids": "<boolean>"
  },
  "tiktokData": {
    "disableComment": "<boolean>",
    "disableDuet": "<boolean>",
    "disableStitch": "<boolean>",
    "privacyOption": "<string>",
    "commercialContentThirdParty": "<boolean>",
    "commercialContentOwnBrand": "<boolean>",
    "title": "<string>",
    "autoAddMusic": "<boolean>",
    "photoCoverIndex": "<integer>"
  },
  "linkedinData": {
    "documentTitle": "<string>",
    "publishImagesAsPDF": "<boolean>",
    "previewIncluded": "<boolean>",
    "type": "<string>",
    "poll": {
      "question": "<string>",
      "options": [
        {
          "text": "<string>"
        },
        {
          "text": "<string>"
        }
      ],
      "settings": {
        "duration": "<string>"
      }
    }
  },
  "autolistData": {
    "id": "<integer>",
    "name": "<string>"
  },
  "brandName": "<string>",
  "targetBrandId": "<integer>",
  "gmbData": {
    "type": "<string>"
  },
  "descendants": [
    {
      "value": "<Circular reference to #/components/schemas/ScheduledPost detected>"
    },
    {
      "value": "<Circular reference to #/components/schemas/ScheduledPost detected>"
    }
  ],
  "notes": [
    {
      "created": {
        "dateTime": "<string>",
        "timezone": "<string>"
      },
      "id": "<integer>",
      "postId": "<integer>",
      "userId": "<integer>",
      "userName": "<string>",
      "content": "<string>",
      "updatedDate": {
        "dateTime": "<string>",
        "timezone": "<string>"
      },
      "updated": "<boolean>",
      "deletedDate": {
        "dateTime": "<string>",
        "timezone": "<string>"
      },
      "deleted": "<boolean>"
    },
    {
      "created": {
        "dateTime": "<string>",
        "timezone": "<string>"
      },
      "id": "<integer>",
      "postId": "<integer>",
      "userId": "<integer>",
      "userName": "<string>",
      "content": "<string>",
      "updatedDate": {
        "dateTime": "<string>",
        "timezone": "<string>"
      },
      "updated": "<boolean>",
      "deletedDate": {
        "dateTime": "<string>",
        "timezone": "<string>"
      },
      "deleted": "<boolean>"
    }
  ],
  "hasNotReadNotes": "<boolean>",
  "uuid": "<string>",
  "copiedFrom": "<string>",
  "creatorUserMail": "<string>",
  "creatorUserId": "<integer>",
  "postApprovalData": {
    "approvalEvents": [
      {
        "postUuid": "<string>",
        "postId": "<integer>",
        "reviewerId": "<integer>",
        "reviewerMail": "<string>",
        "status": "<string>",
        "updatedDate": {
          "dateTime": "<string>",
          "timezone": "<string>"
        },
        "deletedDate": {
          "dateTime": "<string>",
          "timezone": "<string>"
        },
        "deleted": "<boolean>"
      },
      {
        "postUuid": "<string>",
        "postId": "<integer>",
        "reviewerId": "<integer>",
        "reviewerMail": "<string>",
        "status": "<string>",
        "updatedDate": {
          "dateTime": "<string>",
          "timezone": "<string>"
        },
        "deletedDate": {
          "dateTime": "<string>",
          "timezone": "<string>"
        },
        "deleted": "<boolean>"
      }
    ],
    "approvalStatus": "<string>",
    "approvalCriteria": "<string>",
    "sendMailToReviewers": "<boolean>",
    "saveData": "<boolean>"
  },
  "threadsData": {
    "allowedCountryCodes": [
      "<string>",
      "<string>"
    ]
  },
  "blueskyData": {
    "postLanguages": [
      "<string>",
      "<string>"
    ]
  },
  "libraryPostId": "<long>"
}

async def make_get_request(url: str) -> dict[str, Any] | None:
    """Make a get request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
async def make_post_request(url: str, data: json) -> dict[str, Any] | None:
    """Make a post request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
        "content-type": "application/json",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, data=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def make_put_request(url: str, data: json) -> dict[str, Any] | None:
    """Make a put request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
        "content-type": "application/json",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, headers=headers, data=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def make_patch_request(url: str, data: json) -> dict[str, Any] | None:
    """Make a patch request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
        "content-type": "application/json",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(url, headers=headers, data=data, timeout=30.0)
            response.raise_for_status()
            return response.status_code
        except Exception:
            return None

@mcp.tool()
async def get_brands(state: str) -> List[str]:
    """
    Get the list of brands from your Metricool account.
    Add to the result that the only networks with competitors are Instagram, Facebook, Twitch, YouTube, Twitter, and Bluesky.
    """

    url = f"{METRICOOL_BASE_URL}/v2/settings/brands?userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get brands")
    
    return response

@mcp.tool()
async def get_Instagram_Reels(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Instagram Reels from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/reels/instagram?from={init_date}T00%3A00%3A00&to={end_date}T00%3A00%3A00&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Instagram Reels")
    
    return response

@mcp.tool()
async def get_Instagram_Posts(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Instagram Posts from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/instagram?from={init_date}T00%3A00%3A00&to={end_date}T00%3A00%3A00&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Instagram Posts")
    
    return response

@mcp.tool()
async def get_Instagram_Stories(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Instagram Stories from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 20250101
     end date: End date of the period to get the data. The format is 20250101
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/stories/instagram?start={init_date}T00%3A00%3A00&end={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Instagram Stories")
    
    return response

@mcp.tool()
async def get_Tiktok_Videos(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Tiktok Videos from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/tiktok?from={init_date}T00%3A00%3A00&to={end_date}T00%3A00%3A00&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Tiktok Videos")
    
    return response

@mcp.tool()
async def get_Facebook_Reels(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Facebook Reels from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/reels/facebook?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Facebook Reels")
    
    return response

@mcp.tool()
async def get_Facebook_Posts(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Facebook Posts from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/facebook?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Facebook Posts")
    
    return response

@mcp.tool()
async def get_Facebook_Stories(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Facebook Stories from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/stories/facebook?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Facebook Stories")
    
    return response

@mcp.tool()
async def get_Thread_Posts(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Threads Posts from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/threads?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Threads Posts")
    
    return response

@mcp.tool()
async def get_X_Posts(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of X (Twitter) Posts from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 20250101
     end date: End date of the period to get the data. The format is 20250101
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/stats/twitter/posts?start={init_date}&end={end_date}&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get X Posts")
    
    return response

@mcp.tool()
async def get_Bluesky_Posts(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Bluesky Posts from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/bluesky?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Bluesky Posts")
    
    return response

@mcp.tool()
async def get_Linkedin_Posts(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Linkedin Posts from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/linkedin?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Linkedin Posts")
    
    return response

@mcp.tool()
async def get_Pinterest_Pins(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Pinterest Pins from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/pinterest?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Pinterest Pins")
    
    return response

@mcp.tool()
async def get_Youtube_Videos(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Youtube Videos from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/posts/youtube?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Youtube Videos")
    
    return response

@mcp.tool()
async def get_Twitch_Videos(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Twitch Videos from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 20250101
     end date: End date of the period to get the data. The format is 20250101
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/stats/twitch/videos?start={init_date}&end={end_date}&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Twitch Videos")
    
    return response

@mcp.tool()
async def get_FacebookAds_Campaigns(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Facebook Ads Campaigns from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 20250101
     end date: End date of the period to get the data. The format is 20250101
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/stats/facebookads/campaigns?start={init_date}&end={end_date}&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Facebook Ads Campaigns")
    
    return response

@mcp.tool()
async def get_GoogleAds_Campaigns(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Google Ads Campaigns from your Metricool account.
    
    Args:
     init date: Init date of the period to get the data. The format is 20250101
     end date: End date of the period to get the data. The format is 20250101
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/stats/adwords/campaigns?start={init_date}&end={end_date}&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Google Ads Campaigns")
    
    return response

@mcp.tool()
async def get_TiktokAds_Campaigns(init_date: str, end_date: str, blog_id: int) -> List[str]:
    """
    Get the list of Tiktok Ads Campaigns from your Metricool brand account.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/campaigns/tiktokads?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get Tiktok Ads Campaigns")
    
    return response

@mcp.tool()
async def get_Network_Competitors(network: str, init_date: str, end_date: str, blog_id: int, limit: int, timezone: str) -> List[str]:
    """
    Get the list of your competitors from your Metricool brand account.
    Add interesting conclusions for my brand about my competitors.
    
    Args:
     init date: Init date of the period to get the data. The format is 2025-01-01
     end date: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
     limit: Limit of competitors. By default = 10
     timezone: Timezone of the post. The format is "Europe%2FMadrid".  Use the timezone of the user extracted from the get_brands tool.
    """

    url = f"{METRICOOL_BASE_URL}/v2/analytics/competitors/{network}?from={init_date}T00%3A00%3A00&to={end_date}T23%3A59%3A59&blogId={blog_id}&userId={METRICOOL_USER_ID}&limit={limit}&timezone={timezone}&integrationSource=MCP"
    
    response = await make_get_request(url)

    if not response:
       return ("Failed to get competitors")
    
    return response

@mcp.tool()
async def post_Schedule_Post(date:str, blog_id: int, info: json) -> str:
    """
    Schedule a post to Metricool at a specific date and time. 
    To be able to schedule the post, you need to maintain the structure.
    You can use the tool get_Best_Time_To_Post to get the best time to post for a specific provider if the user doesn't specify the time to post.
    If the post include Instagram, is a must to have at least one image or video. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the post include Pinterest, is a must to have a image and the board where to publish the pin. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the post include Youtube, is a must to have a video, select the audience (if it's video made for kids or not) and the title of the video. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the post include Tiktok, is a must to have at least one image or video. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the posts is Facebook Reel, is a must to have a video. If is Facebook Story, image or video is needed. If you don't have more information, you can ask the user about it and wait until you have the information.
    The date can't be in the past.

    Args:
     date: Date and time to publish the post. The format is 2025-01-01T00:00:00
     blog id: Blog id of the Metricool brand account.
     info: Data of the post to be scheduled. Should be a json object with the following fields:
        autoPublish: True or False, default is True.
        draft: True or False, default is False.
        firstCommentText: Text of the first comment of the post. Default ""
        hasNotReadNotes: True or False, default is False.
        media: default is empty list.
        mediaAltText: default is empty list.
        providers: always need at least one provider with the format [{"network":"<string>"}]. Use "twitter" for X posts.
        publicationDate: Date and timezone of the post. The format is {dateTime:"2025-01-01T00:00:00", timezone:"Europe/Madrid"}. Use the timezone of the user extracted from the get_brands tool.
        shortener: True or False, default is False.
        smartLinkData: default is {ids:[]}
        text: Text of the post.
        Always you need to add the networkData for the posts, as empty if you don't have more information. Only include the networkData for the networks you have in the providers list. 
            The format is "twitterData": {"tags":[]}, Tags is used for tagging people on the images of the post, not hashtags.
                            "facebookData": {"boost":0, "boostPayer":"", "boostBeneficiary":"", "type":"", "title":""}, 
                            "instagramData": {"autoPublish":True, "tags":[]}, 
                            "linkedinData": {"documentTitle": "<string>", "publishImagesAsPDF": "<boolean>", "previewIncluded": "<boolean>", "type": "<string>", "poll": {"question": "<string>", "options": [{"text": "<string>"}, {"text": "<string>"}], "settings": {"duration": "<string>"}}},    
                            "pinterestData": {"boardId":"", "pinTitle":"","pinLink":"", "pinNewFormat":True}, 
                            "youtubeData": {"title": "<string>", "type": "<string>", "privacy": "<string>", "tags": [ "<string>", "<string>" ], "category": "<string>", "madeForKids": "<boolean>"}, 
                            "twitchData": {"autoPublish":True, "tags":[]}, 
                            "tiktokData": {"disableComment": "<boolean>", "disableDuet": "<boolean>", "disableStitch": "<boolean>", "privacyOption": "<string>", "commercialContentThirdParty": "<boolean>", "commercialContentOwnBrand": "<boolean>", "title": "<string>", "autoAddMusic": "<boolean>", "photoCoverIndex": "<integer>"},
                            "blueskyData": {"postLanguages":["",""]},
                            "threadsData":{"allowedCountryCodes:["",""]}
        The other fields are optional, but you need to add the ones you have. If you don't have more information, you can ask the user about it and wait until you have the information.
    
    """

    url = f"{METRICOOL_BASE_URL}/v2/scheduler/posts?blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_post_request(url, data=json.dumps(info))

    if not response:
       return ("Failed to schedule the post")
    
    return response


@mcp.tool()
async def get_Best_Time_To_Post(start: str, end: str, blog_id: int, provider: str, timezone: str) -> List[str]:
    """
    Get the best time to post for a specific provider. The return is a list of hours and days with a value. The higher the value, the best time to post.
    Try to get the best for as maximum of 1 week. If you have day to publish but not hours, choose the start and end of this day.
    
    Args:
     start: Start date of the period to get the data. The format is 2025-01-01
     end: End date of the period to get the data. The format is 2025-01-01
     blog id: Blog id of the Metricool brand account.
     provider: Provider of the post. The format is "twitter", "facebook", "instagram", "linkedin", "youtube", "tiktok". Only these are accepted.
     timezone: Timezone of the post. The format is "Europe%2FMadrid".  Use the timezone of the user extracted from the get_brands tool.
    """

    url = f"{METRICOOL_BASE_URL}/v2/scheduler/besttimes/{provider}?start={start}T00%3A00%3A00&end={end}T23%3A59%3A59&timezone={timezone}&blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"

    response = await make_get_request(url)
    
    if not response:
       return ("Failed to get the best time to post")
    
    return response

@mcp.tool()
async def update_Schedule_Post(id: str, date:str, blog_id: int, info: json) -> str:
    """
    Update a scheduled post in Metricool. You need the id of the post to update. Get it from the get_Scheduled_Posts tool previous on the conversation.
    Ask the user if they're sure they want to modify the post, including what will be changed, and require them to confirm.
    Do not retry if there is a problem.
    To update the post, ensure the full original content is included in the request, modifying only the new information while keeping the rest unchanged and maintaining the original structure.
    If the post include Instagram, is a must to have at least one image or video. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the post include Pinterest, is a must to have a image and the board where to publish the pin. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the post include Youtube, is a must to have a video, select the audience (if it's video made for kids or not) and the title of the video. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the post include Tiktok, is a must to have at least one image or video. If you don't have more information, you can ask the user about it and wait until you have the information.
    If the posts is Facebook Reel, is a must to have a video. If is Facebook Story, image or video is needed. If you don't have more information, you can ask the user about it and wait until you have the information.
    The date can't be in the past.

    Args:
     date: Date and time to publish the post. The format is 2025-01-01T00:00:00
     id: id of the post to update. Get it from the get_Scheduled_Posts tool previous on the conversation.
     blog id: Blog id of the Metricool brand account.
     info: Data of the post to be scheduled. You need to send only the fields you want to update. This is so important. Should be a json object with the following fields:
        id: id of the post to update. Get it from the get_Scheduled_Posts tool previous on the conversation. The format is "id":<integer>
        uuid: uuid of the post to update. Get it from the get_Scheduled_Posts tool previous on the conversation. The format is "uuid":"<string>"
        autoPublish: True or False, default is True.
        draft: True or False, default is False.
        firstCommentText: Text of the first comment of the post. Default ""
        hasNotReadNotes: True or False, default is False.
        media: default is empty list.
        mediaAltText: default is empty list.
        providers: always need at least one provider with the format [{"network":"<string>"}]. Use "twitter" for X posts.
        publicationDate: Date and timezone of the post. The format is {dateTime:"2025-01-01T00:00:00", timezone:"Europe/Madrid"}
        shortener: True or False, default is False.
        smartLinkData: default is {ids:[]}
        text: Text of the post.
        Always you need to add the networkData for the posts, as empty if you don't have more information. Only include the networkData for the networks you have in the providers list. 
            The format is "twitterData": {"tags":[]}, Tags is used for tagging people on the images of the post, not hashtags.
                            "facebookData": {"boost":0, "boostPayer":"", "boostBeneficiary":"", "type":"", "title":""}, 
                            "instagramData": {"autoPublish":True, "tags":[]}, 
                            "linkedinData": {"documentTitle": "<string>", "publishImagesAsPDF": "<boolean>", "previewIncluded": "<boolean>", "type": "<string>", "poll": {"question": "<string>", "options": [{"text": "<string>"}, {"text": "<string>"}], "settings": {"duration": "<string>"}}},    
                            "pinterestData": {"boardId":"", "pinTitle":"","pinLink":"", "pinNewFormat":True}, 
                            "youtubeData": {"title": "<string>", "type": "<string>", "privacy": "<string>", "tags": [ "<string>", "<string>" ], "category": "<string>", "madeForKids": "<boolean>"}, 
                            "twitchData": {"autoPublish":True, "tags":[]}, 
                            "tiktokData": {"disableComment": "<boolean>", "disableDuet": "<boolean>", "disableStitch": "<boolean>", "privacyOption": "<string>", "commercialContentThirdParty": "<boolean>", "commercialContentOwnBrand": "<boolean>", "title": "<string>", "autoAddMusic": "<boolean>", "photoCoverIndex": "<integer>"},
                            "blueskyData": {"postLanguages":["",""]},
                            "threadsData":{"allowedCountryCodes:["",""]}
    """

    url = f"{METRICOOL_BASE_URL}/v2/scheduler/posts/{id}?blogId={blog_id}&userId={METRICOOL_USER_ID}&integrationSource=MCP"
    
    response = await make_put_request(url, data=json.dumps(info))

    if not response:
       return ("Failed to update the post")
    
    return response
    

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

import os
import json
import logging
import asyncio
from typing import Awaitable, Callable, Dict, List, Any, Optional

import aiohttp
from google.oauth2 import service_account
from googleapiclient.discovery import build
import imaplib
import aiosmtplib
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

###############################################################################
#                             HELPER FUNCTIONS
###############################################################################

async def safe_json(response: aiohttp.ClientResponse) -> Any:
    """
    Safely parse JSON from an aiohttp response.
    Returns None if parsing fails.
    """
    try:
        return await response.json()
    except Exception:
        return None

###############################################################################
#                         TOOL TEST FUNCTIONS
###############################################################################

async def test_zerobounce(api_key: str) -> Dict[str, Any]:
    url = f"https://api.zerobounce.net/v2/validate?api_key={api_key}&email=contact@dhisana.ai"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as response:
                status = response.status
                data = await safe_json(response)

                if status != 200:
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": f"Non-200 from ZeroBounce: {status}"
                    }
                # If the API key is invalid, ZeroBounce might return status=200 but "api_key_invalid"
                if data and data.get("status") == "invalid" and data.get("sub_status") == "api_key_invalid":
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": "ZeroBounce indicates invalid API key"
                    }
                return {"success": True, "status_code": status, "error_message": None}
    except Exception as e:
        logger.error(f"ZeroBounce test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}

async def test_openai(api_key: str, model_name: str, reasoning_effort: str) -> Dict[str, Any]:
    """
    Tests OpenAI API key by making a simple chat completion request.
    - If the model name starts with 'o3-', includes 'reasoning_effort' in the request.
    - Otherwise, uses the model name as is.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Base request body
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": "Hello, world!"}],
        "max_completion_tokens": 5
    }

    # Only apply the reasoning parameter if it's an o3 series model
    if model_name.startswith("o"):
        data["reasoning_effort"] = reasoning_effort

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.post(url, headers=headers, json=data) as response:
                status = response.status
                resp_data = await response.json()

                if status != 200:
                    err_message = resp_data.get("error", {}).get("message", f"Non-200 from OpenAI: {status}")
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": err_message
                    }

                # Check if "error" is present in the response
                if "error" in resp_data:
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": resp_data["error"].get("message", "OpenAI error returned")
                    }

                return {"success": True, "status_code": status, "error_message": None}

    except Exception as e:
        logger.error(f"OpenAI test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}


async def test_google_workspace(api_key: str, subject: str) -> Dict[str, Any]:
    """
    Tests Google Workspace by listing Gmail messages using domain-wide delegation.
    Requires subject (email) to impersonate. 'me' then refers to that user mailbox.
    """
    try:
        creds_info = json.loads(api_key)
        creds = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=["https://mail.google.com/"]
        )

        # Domain-wide delegation requires specifying the email to impersonate
        delegated_creds = creds.with_subject(subject)

        service = build("gmail", "v1", credentials=delegated_creds)

        # Execute synchronous call in a background thread to avoid blocking
        def _list_messages():
            return service.users().messages().list(userId="me").execute()

        response = await asyncio.to_thread(_list_messages)

        if "messages" in response:
            return {"success": True, "status_code": 200, "error_message": None}
        return {
            "success": False,
            "status_code": 200,
            "error_message": "API responded but no 'messages' key found"
        }
    except Exception as e:
        logger.error(f"Google Workspace test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}

async def test_serpapi(api_key: str) -> Dict[str, Any]:
    url = f"https://serpapi.com/search?engine=google&q=hello+world&api_key={api_key}"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as response:
                status = response.status
                data = await safe_json(response)

                if status != 200:
                    err_message = None
                    if data and isinstance(data, dict):
                        err_message = data.get("error")
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": err_message or f"Non-200 from SERPAPI: {status}"
                    }
                # Some SERP API errors might still be 200 but contain an 'error' field
                if data and "error" in data:
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": data["error"]
                    }
                return {"success": True, "status_code": status, "error_message": None}
    except Exception as e:
        logger.error(f"SERP API test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}

async def test_proxycurl(api_key: str) -> Dict[str, Any]:
    url = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"linkedin_profile_url": "https://www.linkedin.com/in/satyanadella"}
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, headers=headers, params=params) as response:
                status = response.status
                data = await safe_json(response)

                if status != 200:
                    err_message = None
                    if data and isinstance(data, dict):
                        err_message = data.get("message") or data.get("detail")
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": err_message or f"Non-200 from Proxycurl: {status}"
                    }
                return {"success": True, "status_code": status, "error_message": None}
    except Exception as e:
        logger.error(f"Proxycurl test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}

async def test_apollo(api_key: str) -> Dict[str, Any]:
    organization_domain = 'microsoft.com'
    url = f'https://api.apollo.io/api/v1/organizations/enrich?domain={organization_domain}'
    logger.debug(f"Making GET request to Apollo for domain: {organization_domain}")
    headers = {"X-Api-Key": api_key}

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, headers=headers) as response:
                status = response.status
                if status == 200:
                    result = await response.json()
                    logger.info("Successfully retrieved organization info from Apollo.")
                    return {"success": True, "status_code": status}

                elif status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=429,
                        message=msg
                    )
                else:
                    err_message = None
                    if response.content_type == "application/json":
                        data = await response.json()
                        err_message = data.get("message")
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": err_message or f"Non-200 from Apollo: {status}"
                    }
    except Exception as e:
        logger.error(f"Apollo test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}

async def test_hubspot(api_key: str) -> Dict[str, Any]:
    url = "https://api.hubapi.com/account-info/v3/details"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            headers = {"Authorization": f"Bearer {api_key}"}
            async with session.get(url, headers=headers) as response:
                status = response.status
                data = await safe_json(response)

                if status != 200:
                    err_message = None
                    if data and isinstance(data, dict):
                        err_message = data.get("message") or data.get("error")
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": err_message or f"Non-200 from HubSpot: {status}"
                    }
                if data and "portalId" in data:
                    return {"success": True, "status_code": status, "error_message": None}

                return {
                    "success": False,
                    "status_code": status,
                    "error_message": "Did not find 'portalId' in the response."
                }
    except Exception as e:
        logger.error(f"HubSpot test failed: {e}")
        return {"success": False, "status_code": 0, "error_message": str(e)}

async def test_github(api_key: str) -> Dict[str, Any]:
    """
    Tests GitHub API connectivity using a Personal Access Token (PAT).
    Performs a GET /user call to verify token validity.
    """
    url = "https://api.github.com/user"
    # For GitHub tokens, 'token' prefix is common for classic tokens.
    # If you have a fine-grained token, adjust the prefix if needed.
    headers = {
        "Authorization": f"token {api_key}",
        "Accept": "application/vnd.github+json",
    }
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, headers=headers) as response:
                status = response.status
                data = await safe_json(response)

                if status != 200:
                    # For invalid tokens, GitHub often returns 401 or 403
                    # 422 can happen if the token has insufficient scope or is otherwise invalid
                    error_message = None
                    if data and isinstance(data, dict):
                        # Sometimes has "message" with details
                        error_message = data.get("message", f"GitHub error: {status}")
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": error_message or f"Non-200 from GitHub: {status}"
                    }

                # If valid, the response normally contains a "login" field with the username
                if data and "login" in data:
                    return {
                        "success": True,
                        "status_code": status,
                        "error_message": None
                    }
                else:
                    return {
                        "success": False,
                        "status_code": status,
                        "error_message": "GitHub API responded but 'login' not found."
                    }

    except Exception as e:
        logger.error(f"GitHub connectivity test failed: {e}")
        return {
            "success": False,
            "status_code": 0,
            "error_message": str(e)
        }

###############################################################################
#                   SMTP / IMAP CONNECTIVITY TEST FUNCTION
###############################################################################
async def test_smtp_accounts(
    usernames: str,
    passwords: str,
    smtp_host: str,
    smtp_port: int,
    imap_host: str,
    imap_port: int,
) -> Dict[str, Any]:
    """
    Quick “smoke test” for an SMTP + IMAP mailbox configuration.

    Parameters
    ----------
    usernames : str
        Comma-separated list of mailbox usernames.
    passwords : str
        Comma-separated list of passwords or app-passwords, **same order** as *usernames*.
    smtp_host : str
        SMTP server hostname (e.g. ``smtp.gmail.com``).
    smtp_port : int
        SMTP port (587 for STARTTLS, 465 for implicit SSL, etc.).
    imap_host : str
        IMAP server hostname (e.g. ``imap.gmail.com``).
    imap_port : int
        IMAP SSL port (usually 993).

    Returns
    -------
    dict
        {
          "success": bool,
          "status_code": int,          # 250 for SMTP OK, or last IMAP status-code on error
          "error_message": Optional[str]
        }
    """
    users: List[str] = [u.strip() for u in usernames.split(",") if u.strip()]
    pwds:  List[str] = [p.strip() for p in passwords.split(",") if p.strip()]

    if not users or len(users) != len(pwds):
        return {
            "success": False,
            "status_code": 0,
            "error_message": "Username / password list mismatch or empty."
        }

    # --- use the first account for the connectivity check ---
    user, pwd = users[0], pwds[0]

    # 1)  SMTP LOGIN ----------------------------------------------------------
    try:
        smtp_kwargs = dict(hostname=smtp_host, port=smtp_port, timeout=10)
        if smtp_port == 587:
            smtp_kwargs["start_tls"] = True          # STARTTLS upgrade
        else:
            smtp_kwargs["tls"] = smtp_port == 465    # implicit SSL on 465

        smtp = aiosmtplib.SMTP(**smtp_kwargs)
        await smtp.connect()

        code, _msg = await smtp.login(user, pwd)
        await smtp.quit()

        if code != 235 and code != 250:              # 235 = Auth OK, 250 = generic OK
            return {
                "success": False,
                "status_code": code,
                "error_message": f"SMTP login failed with code {code}"
            }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "error_message": f"SMTP error: {e}"
        }

    # 2)  IMAP LOGIN ----------------------------------------------------------
    try:
        conn = imaplib.IMAP4_SSL(imap_host, imap_port)  # SSL always for 993
        status, _ = conn.login(user, pwd)
        conn.logout()

        if status != "OK":
            return {
                "success": False,
                "status_code": 0,
                "error_message": f"IMAP login failed: {status}"
            }

    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "error_message": f"IMAP error: {e}"
        }

    # ------------------------------------------------------------------------
    return {
        "success": True,
        "status_code": 250,          # canonical “OK” code for SMTP success
        "error_message": None
    }

###############################################################################
#                         MAIN CONNECTIVITY FUNCTION
###############################################################################

async def test_connectivity(tool_config: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Checks connectivity for multiple tools and returns a dictionary
    with the result for each.

    Special-cases:
      • 'openai'           – needs modelName & reasoningEffort
      • 'googleworkspace'  – needs subjectEmail
      • 'smtpEmail'        – has *no* apiKey; instead requires usernames,
                             passwords, smtp/imap hosts & ports
    """
    test_mapping: Dict[str, Callable[..., Awaitable[Dict[str, Any]]]] = {
        "zerobounce":        test_zerobounce,
        "openai":            test_openai,
        "googleworkspace":   test_google_workspace,
        "serpapi":           test_serpapi,
        "proxycurl":         test_proxycurl,
        "apollo":            test_apollo,
        "hubspot":           test_hubspot,
        "github":            test_github,
        "smtpEmail":         test_smtp_accounts,          # handled explicitly below
    }

    results: Dict[str, Dict[str, Any]] = {}

    for tool in tool_config:
        tool_name: str = tool.get("name", "")
        config_entries: List[Dict[str, Any]] = tool.get("configuration", [])

        if not tool_name:
            logger.warning("Tool entry missing 'name' field.")
            results.setdefault("unknown_tool", {
                "success": False,
                "status_code": 0,
                "error_message": "Tool entry missing 'name'."
            })
            continue

        if tool_name not in test_mapping:
            logger.warning(f"No test function found for tool: {tool_name}")
            results[tool_name] = {
                "success": False,
                "status_code": 0,
                "error_message": f"No test function for tool '{tool_name}'."
            }
            continue

        # ------------------------------------------------------------------ #
        # 1) Special-case: SMTP / IMAP connectivity (no apiKey)
        # ------------------------------------------------------------------ #
        if tool_name == "smtpEmail":
            def _get(name: str, default: Any = None):
                return next((c["value"] for c in config_entries if c["name"] == name), default)

            usernames   = _get("usernames", "")
            passwords   = _get("passwords", "")
            smtp_host   = _get("smtpEndpoint", "smtp.gmail.com")
            smtp_port   = int(_get("smtpPort", 587))
            imap_host   = _get("imapEndpoint", "imap.gmail.com")
            imap_port   = int(_get("imapPort", 993))

            if not usernames or not passwords:
                results[tool_name] = {
                    "success": False,
                    "status_code": 0,
                    "error_message": "Missing usernames or passwords."
                }
            else:
                logger.info("Testing connectivity for smtpEmail…")
                results[tool_name] = await test_smtp_accounts(
                    usernames,
                    passwords,
                    smtp_host,
                    smtp_port,
                    imap_host,
                    imap_port,
                )
            continue  # handled – move to next tool

        # ------------------------------------------------------------------ #
        # 2) All other tools – expect an apiKey by default
        # ------------------------------------------------------------------ #
        api_key = next((c["value"] for c in config_entries if c["name"] == "apiKey"), None)
        if not api_key:
            logger.warning(f"Tool '{tool_name}' missing 'apiKey' in configuration.")
            results[tool_name] = {
                "success": False,
                "status_code": 0,
                "error_message": "Missing apiKey."
            }
            continue

        logger.info(f"Testing connectivity for {tool_name}…")

        # OpenAI needs extra args
        if tool_name == "openai":
            model_name = next((c["value"] for c in config_entries if c["name"] == "modelName"), "gpt-4o-mini")
            reasoning_effort = next((c["value"] for c in config_entries if c["name"] == "reasoningEffort"), "medium")
            results[tool_name] = await test_openai(api_key, model_name, reasoning_effort)

        # Google Workspace needs subjectEmail
        elif tool_name == "googleworkspace":
            subject_email = next((c["value"] for c in config_entries if c["name"] == "subjectEmail"), "")
            if not subject_email:
                results[tool_name] = {
                    "success": False,
                    "status_code": 0,
                    "error_message": "Missing subjectEmail for Google Workspace."
                }
            else:
                results[tool_name] = await test_google_workspace(api_key, subject_email)

        # Everything else takes only api_key
        else:
            results[tool_name] = await test_mapping[tool_name](api_key)

    return results

